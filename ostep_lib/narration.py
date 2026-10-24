"""NarratedScene: a Scene base that paces animations to the narration.

    class S01Welcome(NarratedScene):
        def construct(self):
            self.say("Welcome! This is a series about operating systems.",
                     FadeIn(prof), prof.change("happy"))
            self.beat(1.0)
            with self.narrate("A longer line with several steps."):
                self.play(...)
                self.play(...)

Every ``say``/``narrate`` adds the text as a subcaption, so Manim writes an .srt
next to the video.  Duration = max(words / 2.5, min_time) seconds (~150 wpm).
"""
import os
from contextlib import contextmanager

import numpy as np
from manim import AnimationGroup, MarkupText, Scene, SingleStringMathTex, Text, VMobject, config

from .style import apply_style

WORDS_PER_SECOND = 2.5
TEXT_TYPES = (Text, MarkupText, SingleStringMathTex)


def speech_time(text, min_time=None):
    words = len(str(text).split())
    return max(words / WORDS_PER_SECOND, min_time or 0.0)


class NarratedScene(Scene):
    """Scene with ``say``, ``narrate`` and ``beat`` helpers; applies the series style."""

    def setup(self):
        super().setup()
        apply_style(self)

    # ------------------------------------------------------------------
    def say(self, text, *animations, min_time=None, stretch=False, **play_kwargs):
        """Narrate ``text`` while playing ``animations`` together.

        The call lasts ``max(speech_time, animation time)``: shorter animations are
        padded with a wait (or stretched to the speech time with ``stretch=True``).
        With no animations it just waits.  The subcaption spans the whole call."""
        d = speech_time(text, min_time)
        if not animations:
            if text:
                self.add_subcaption(text, duration=d)
            self.wait(d)
            return
        group = animations[0] if len(animations) == 1 else AnimationGroup(*animations)
        if "run_time" in play_kwargs:
            group.run_time = play_kwargs.pop("run_time")
        if stretch and group.run_time < d:
            group.run_time = d
        t = group.run_time
        if text:
            self.add_subcaption(text, duration=max(d, t))
        self.play(group, **play_kwargs)
        if t < d:
            self.wait(d - t)

    def say_crux(self, card, *head_anims, sub_anims=(), dock=False, hold=0.8, prefix="The crux:",
                 lead=None, **dock_kw):
        """Show a ``CruxCard`` AND read it aloud: the crux is part of the narration, so it is
        captioned too.  The narrator says "The crux: <question>" while the frame, header and
        question write, then reads the subtitle (when the card has one) as it fades in.

            self.say_crux(card, stu.change("curious", look_at=card))        # extras go with the question
            self.say_crux(card, dock=True)                                  # ... and dock it afterwards
            self.say_crux(card, dock=True, font_size=22)                    # dock kwargs pass through

        The words around the question should sound spoken, not mechanical: pass ``lead`` as the
        sentence that carries it, with ``{q}`` where the card's question goes, e.g.
        ``lead="So here's the crux: {q}"`` or ``lead="Which brings us to the real problem: {q}"``
        (vary it from episode to episode and crux to crux).  The question itself is always read
        verbatim, so it matches the card.  ``prefix`` is the old mechanical form, kept as the fallback."""
        if lead:
            text = lead.format(q=card.question_str)
        else:
            text = f"{prefix} {card.question_str}".strip()
        self.say(text, card.write_head(), *head_anims)
        if getattr(card, "subtitle_str", ""):
            self.say(card.subtitle_str, card.write_sub(), *sub_anims)
        self.beat(hold)
        if dock:
            self.play(card.dock(**dock_kw))

    @contextmanager
    def narrate(self, text, min_time=None):
        """Context manager for a narration chunk that needs several ``play`` calls.
        Pads with a wait so the block lasts at least the speech time."""
        d = speech_time(text, min_time)
        t0 = self.time
        yield
        el = self.time - t0
        if el < d:
            self.wait(d - el)
            el = d
        if text:
            # start at t0 exactly: ``time - el`` can come out as -1e-16 for the first block of a scene,
            # and srt.compose silently drops entries that start before zero (a missing caption)
            self.add_subcaption(text, duration=el, offset=max(t0 - self.time, -self.time) + 1e-9)

    # ------------------------------------------------------------------
    def play(self, *args, **kwargs):
        super().play(*args, **kwargs)
        if os.environ.get("OSTEP_CHECK"):
            self._check_bounds()
            self._check_overlaps()

    def update_to_time(self, t):
        super().update_to_time(t)
        # sample text overlaps during animations too (~4x per second): a title written over
        # a label and then moved away never shows up in the end-of-play check
        if os.environ.get("OSTEP_CHECK"):
            n = getattr(self, "_frame_n", 0) + 1
            self._frame_n = n
            if n % max(1, round(config.frame_rate / 4)) == 0:
                self._check_overlaps()

    def _text_boxes(self):
        """(label, lo, hi) of every visible text mobject, skipping text veiled by a scrim."""
        # a scrim only hides what's under it once it is mostly opaque
        # (animations nest their mobjects in groups, so search whole families)
        veil_z = max((sm.z_index for m in self.mobjects for sm in m.get_family()
                      if getattr(sm, "is_scrim", False) and sm.get_fill_opacity() >= 0.6), default=None)
        boxes, visited = [], set()

        def walk(m):
            # a mobject can sit in several groups (nested Successions); the renderer draws it once
            if id(m) in visited:
                return
            visited.add(id(m))
            if isinstance(m, TEXT_TYPES):
                if veil_z is not None and m.z_index <= veil_z:
                    return
                # > 0.6: of two texts cross-fading in place, at most one is counted
                fam = [sm for sm in m.family_members_with_points() if sm.get_fill_opacity() > 0.6]
                if fam:
                    pts = np.concatenate([sm.points for sm in fam])
                    label = getattr(m, "text", None) or getattr(m, "tex_string", "?")
                    boxes.append((str(label)[:40], pts.min(axis=0)[:2], pts.max(axis=0)[:2]))
                return
            for sm in m.submobjects:
                walk(sm)

        for m in self.mobjects:
            walk(m)
        return boxes

    def _check_overlaps(self, frac=0.15):
        """Debug (env OSTEP_CHECK=1): warn when two visible texts overlap by more than
        ``frac`` of the smaller one's box (titles over labels, leftovers under new text…)
        in two consecutive samples (so things merely sliding past each other are ignored)."""
        seen = getattr(self, "_overlap_seen", set())
        self._overlap_seen = seen
        prev, now = getattr(self, "_overlap_prev", set()), set()
        self._overlap_prev = now
        boxes = self._text_boxes()
        for i in range(len(boxes)):
            for j in range(i + 1, len(boxes)):
                (ta, alo, ahi), (tb, blo, bhi) = boxes[i], boxes[j]
                w = min(ahi[0], bhi[0]) - max(alo[0], blo[0])
                h = min(ahi[1], bhi[1]) - max(alo[1], blo[1])
                if w <= 0 or h <= 0:
                    continue
                small = min(np.prod(ahi - alo), np.prod(bhi - blo))
                if small > 0 and w * h > frac * small:
                    key = (ta, tb)
                    now.add(key)
                    if key in prev and key not in seen:
                        seen.add(key)
                        print(f"[overlap] t={self.time:.1f}s {ta!r} @({(alo[0]+ahi[0])/2:.1f},{(alo[1]+ahi[1])/2:.1f})"
                              f" x {tb!r} @({(blo[0]+bhi[0])/2:.1f},{(blo[1]+bhi[1])/2:.1f})")

    def _check_bounds(self, tol=0.05):
        """Debug (env OSTEP_CHECK=1): warn about visible mobjects that cross the frame
        edge (partly in, partly out).  Fully off-screen mobjects are ignored."""
        hw, hh = config.frame_width / 2, config.frame_height / 2
        seen = getattr(self, "_bounds_seen", set())
        self._bounds_seen = seen
        for m in self.mobjects:
            if any(getattr(sm, "is_scrim", False) for sm in m.get_family()):   # full-frame by design
                continue
            fam = [sm for sm in m.get_family() if isinstance(sm, VMobject) and len(sm.points)
                   and (sm.get_fill_opacity() > 0.02 or sm.get_stroke_opacity() > 0.02)]
            if not fam:
                continue
            pts = np.concatenate([sm.points for sm in fam])
            lo, hi = pts.min(axis=0), pts.max(axis=0)
            inside = hi[0] > -hw and lo[0] < hw and hi[1] > -hh and lo[1] < hh
            crosses = lo[0] < -hw - tol or hi[0] > hw + tol or lo[1] < -hh - tol or hi[1] > hh + tol
            if inside and crosses:
                key = (type(m).__name__, tuple(np.round(lo[:2], 1)), tuple(np.round(hi[:2], 1)))
                if key not in seen:
                    seen.add(key)
                    print(f"[bounds] t={self.time:.1f}s {type(m).__name__} x[{lo[0]:.2f},{hi[0]:.2f}] "
                          f"y[{lo[1]:.2f},{hi[1]:.2f}]")

    def beat(self, seconds=1.0):
        """A pause marked '(pause …)' or '(hold)' in the scene file."""
        self.wait(seconds)
