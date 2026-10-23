"""EyeIcon: an eye whose pupil can look at a point (episode 10 snooping / peeking, episode 11 paranoid OS).

    eye = EyeIcon(width=0.5)
    self.play(eye.look_at(point))          # pupil slides toward the point
    self.play(eye.blink())
    self.play(eye.close_lids())            # eye shut (thin slit); eye.open_lids() opens it
    eye = EyeIcon(width=0.5, opened=False) # starts closed
    eye.set_look(point)                    # instant

Parts: ``ball`` (VGroup: white, iris, pupil, glint; rebuilt on every animation frame, so do not
edit it directly), ``lid_line`` (the outline).  The eye can be moved and scaled like any mobject
(the geometry is derived from the current white's size and center).
"""
from __future__ import annotations

import numpy as np
from manim import (
    Animation, Circle, Ellipse, Succession, VGroup, UP, DOWN, LEFT, RIGHT, smooth, there_and_back,
)

from ..style import TEXT, MEM_COLOR, BG

__all__ = ["EyeIcon"]

_WHITE = "#F2F2F2"
_PUPIL = "#101010"


class _EyeAnim(Animation):
    """Interpolates the pupil offset (fraction of the free travel, 2-vector) and the lid opening."""

    def __init__(self, eye, offset=None, openness=None, **kw):
        super().__init__(eye, **kw)
        self.eye = eye
        self.t_off = np.array(eye.offset if offset is None else offset, dtype=float)
        self.t_open = eye.openness if openness is None else float(openness)

    def begin(self):
        self.s_off = np.array(self.eye.offset, dtype=float)
        self.s_open = self.eye.openness
        super().begin()

    def interpolate_mobject(self, alpha):
        a = self.rate_func(alpha)
        self.eye._apply(self.s_off + (self.t_off - self.s_off) * a,
                        self.s_open + (self.t_open - self.s_open) * a)

    def clean_up_from_scene(self, scene):
        super().clean_up_from_scene(scene)
        self.eye._apply(self.t_off, self.t_open)


class EyeIcon(VGroup):
    """``EyeIcon(width=0.6, iris=MEM_COLOR, opened=True)``."""

    def __init__(self, width=0.6, iris=MEM_COLOR, opened=True, **kwargs):
        super().__init__(**kwargs)
        self.w = width
        self.h = width * 0.62
        self.iris_color = iris
        self.offset = np.zeros(2)
        self.openness = 1.0 if opened else 0.06
        self.ball = self._ball(self.offset, self.openness)
        self.add(self.ball)

    # ----------------------------------------------------------- geometry
    def _ball(self, off, openness):
        w, h = self.w, self.h
        hh = max(h * openness, 0.012)
        white = Ellipse(width=w, height=hh).set_fill(_WHITE, 1).set_stroke(TEXT, max(1.5, w * 4))
        r = h * 0.42
        free_x = max((w / 2) * 0.55 - r * 0.2, 0.0)
        free_y = max((hh / 2) * 0.35, 0.0)
        c = np.array([off[0] * free_x, off[1] * free_y, 0.0])
        scale_o = min(1.0, hh / h * 1.6)
        iris = Circle(radius=r * scale_o).set_fill(self.iris_color, 1).set_stroke(_PUPIL, 1.2)
        pupil = Circle(radius=r * 0.45 * scale_o).set_fill(_PUPIL, 1).set_stroke(width=0)
        glint = Circle(radius=r * 0.16 * scale_o).set_fill(_WHITE, 1).set_stroke(width=0)
        iris.move_to(c)
        pupil.move_to(c)
        glint.move_to(c + np.array([r * 0.25, r * 0.25, 0]) * scale_o)
        g = VGroup(white, iris, pupil, glint)
        return g

    def _apply(self, off, openness):
        self.offset = np.array(off, dtype=float)
        self.openness = float(openness)
        center = self.ball[0].get_center()
        scale = self.ball[0].width / self.w if self.w else 1.0
        new = self._ball(self.offset, self.openness)
        new.scale(scale).move_to(center)
        self.ball.become(new)
        return self

    # --------------------------------------------------------------- API
    def _offset_to(self, target):
        t = target.get_center() if hasattr(target, "get_center") else np.array(target, dtype=float)
        d = np.array(t, dtype=float)[:2] - self.ball[0].get_center()[:2]
        n = np.linalg.norm(d)
        if n < 1e-6:
            return np.zeros(2)
        # saturate quickly so the pupil visibly points at things that are a little way off
        mag = min(1.0, n / 0.8)
        u = d / n
        return np.array([u[0] * mag, u[1] * mag])

    def set_look(self, target):
        return self._apply(self._offset_to(target), self.openness)

    def look_at(self, target, run_time=0.4):
        return _EyeAnim(self, offset=self._offset_to(target), run_time=run_time, rate_func=smooth)

    def open_lids(self, run_time=0.4):
        return _EyeAnim(self, openness=1.0, run_time=run_time, rate_func=smooth)

    def close_lids(self, run_time=0.3):
        return _EyeAnim(self, openness=0.06, run_time=run_time, rate_func=smooth)

    def blink(self, run_time=0.3):
        return Succession(self.close_lids(run_time * 0.5), self.open_lids(run_time * 0.5))
