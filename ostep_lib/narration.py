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
from manim import AnimationGroup, Scene, VMobject, config

from .style import apply_style

WORDS_PER_SECOND = 2.5


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
    def allow_overlap(self, a, b=None, why=""):
        """Declare a deliberate overlap between ``a`` and ``b`` (or ``a`` and anything when ``b``
        is None) so the layout check never reports it.  ``why`` documents the intent."""
        fa = {id(x) for x in a.get_family()}
        fb = None if b is None else {id(x) for x in b.get_family()}
        self._allowed_overlaps = getattr(self, "_allowed_overlaps", []) + [(fa, fb)]

    def _layout_sample(self, mid_play=False):
        """Debug (env OSTEP_CHECK=1): the shape-aware overlap check (``ostep_lib/layout.py``)."""
        from .layout import OverlapTracker
        tr = getattr(self, "_layout_tracker", None)
        if tr is None:
            tr = self._layout_tracker = OverlapTracker(type(self).__name__)
        tr.sample(self, mid_play)

    def _check_ghosts(self, args):
        """Debug (env OSTEP_CHECK=1): warn when any animation that is not an entrance (FadeOut,
        ``.animate``, Indicate, Transform...) targets a mobject that is not on screen.  Manim adds
        it back for the animation, so something that already left flashes in again (a stale bar, a
        zombie), or, if the animation does not remove it, comes back for good (a cut cable)."""
        from manim import ValueTracker
        from manim.animation.animation import Wait, prepare_animation

        def label(x):
            s = getattr(x, "text", None)
            c = x.get_center()
            return repr(" ".join(s.split())[:24]) if isinstance(s, str) and s else f"{type(x).__name__}@({c[0]:.1f},{c[1]:.1f})"
        # on screen now, or at the end of the previous play (a prop may detach a part while building
        # the animation that fades it, e.g. Terminal.clear(): that part was visible until now)
        on = {id(m) for top in self.mobjects for m in top.get_family()} | getattr(self, "_shown_ids", set())
        self._ever_ids = getattr(self, "_ever_ids", set()) | on
        seen = self.__dict__.setdefault("_ever_seen", {})
        for top in self.mobjects:
            for m in top.get_family():
                seen[id(m)] = m

        def visible_leaves(m):          # what actually draws (a fresh VGroup of on-screen parts is fine)
            return [x for x in m.get_family() if x.has_points() and not x.submobjects
                    and (x.get_fill_opacity() > 0 or x.get_stroke_opacity() > 0 and x.get_stroke_width() > 0)]

        def walk(a):
            subs = getattr(a, "animations", None)
            if subs is not None:
                for s in subs:
                    yield from walk(s)
            else:
                yield a
        for arg in args:
            try:
                anim = prepare_animation(arg)
            except TypeError:
                continue
            for a in walk(anim):
                m = getattr(a, "mobject", None)
                if m is None or isinstance(a, Wait) or isinstance(m, ValueTracker):
                    continue
                if a.is_introducer():
                    on |= {id(x) for x in m.get_family()}
                else:       # a remover, .animate, Indicate, Transform...: all draw their mobject
                    # only parts that were on screen before and left since: a new mobject animated
                    # in by a custom entrance (BubbleIn...) is not a flash-back
                    off = [x for x in visible_leaves(m) if id(x) not in on and id(x) in self._ever_ids]
                    if off:
                        print(f"[ghost] t={self.renderer.time:.1f}s {type(a).__name__}({label(m)}) re-shows "
                              f"{len(off)} part(s) not on screen, e.g. {label(off[0])}")

    def play(self, *args, **kwargs):
        if os.environ.get("OSTEP_CHECK"):
            self._check_ghosts(args)
        super().play(*args, **kwargs)        # Scene.wait plays a Wait, so this covers holds too
        if os.environ.get("OSTEP_CHECK"):
            self._shown_ids = {id(m) for top in self.mobjects for m in top.get_family()}
            # keep every mobject ever shown alive: a freed one's id() could be reused by a new
            # mobject, which would then look like one that left (a false ghost)
            seen = self.__dict__.setdefault("_ever_seen", {})
            for top in self.mobjects:
                for m in top.get_family():
                    seen[id(m)] = m
            self._ever_ids = getattr(self, "_ever_ids", set()) | self._shown_ids
            self._check_bounds()
            self._layout_sample()

    def update_to_time(self, t):
        super().update_to_time(t)
        # sample during animations too (~4x per second): a title written over a label and then
        # moved away never shows up in the end-of-play check
        if os.environ.get("OSTEP_CHECK"):
            n = getattr(self, "_frame_n", 0) + 1
            self._frame_n = n
            if n % max(1, round(config.frame_rate / 4)) == 0:
                self._layout_sample(mid_play=True)

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
