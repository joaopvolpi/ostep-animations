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
            self.add_subcaption(text, duration=el, offset=-el)

    # ------------------------------------------------------------------
    def play(self, *args, **kwargs):
        super().play(*args, **kwargs)
        if os.environ.get("OSTEP_CHECK"):
            self._check_bounds()

    def _check_bounds(self, tol=0.05):
        """Debug (env OSTEP_CHECK=1): warn about visible mobjects that cross the frame
        edge (partly in, partly out).  Fully off-screen mobjects are ignored."""
        hw, hh = config.frame_width / 2, config.frame_height / 2
        seen = getattr(self, "_bounds_seen", set())
        self._bounds_seen = seen
        for m in self.mobjects:
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
