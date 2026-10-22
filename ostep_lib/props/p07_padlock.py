"""Padlock with open/close animations and the numbered strip (episode 07 and later).

Same look as ``ov_icons.padlock_icon`` (rounded body, light shackle, keyhole), but the
shackle can swing open.  Closed = red (KERNEL_COLOR), open = green (PERS).

    lock = Padlock(size=0.5, number=1)
    self.play(lock.open())            # shackle lifts and swings, body turns green
    self.play(lock.close())
    self.play(lock.wobble())          # small rotation shake  (also .shake(), .pulse())

    strip = PadlockStrip(5, size=0.28, at=(-6.6, 3.1))   # five numbered padlocks in a row
    self.play(strip.open(0))          # 0-based index
"""
from __future__ import annotations

import numpy as np
from manim import (
    AnimationGroup, Arc, Dot, Indicate, Rotate, RoundedRectangle, Succession, Text, Transform,
    VGroup, PI, LEFT, RIGHT, UP, DOWN,
)

from ..style import TEXT, DIM, KERNEL_COLOR, PERS
from .core import INK, outline_of


class Padlock(VGroup):
    """``Padlock(size=0.5, number=None, color=KERNEL_COLOR, open_color=PERS, opened=False,
    number_size=None)``.  Parts: ``shackle``, ``body``, ``hole``, ``lock`` (those three),
    ``num`` (numeral under the lock, or an empty VGroup)."""

    def __init__(self, size=0.5, number=None, color=KERNEL_COLOR, open_color=PERS, opened=False,
                 number_size=None, **kwargs):
        super().__init__(**kwargs)
        self.size = size
        self.closed_color, self.open_color = color, open_color
        self.is_open = bool(opened)
        c = open_color if opened else color
        self.body = RoundedRectangle(width=size, height=size * 0.75, corner_radius=size * 0.1)
        self.body.set_fill(c, 1).set_stroke(outline_of(c), 3).shift(DOWN * size * 0.2)
        self.hole = Dot(self.body.get_center(), radius=size * 0.08).set_fill(INK, 1)
        self.shackle = self._shackle(opened)
        self.lock = VGroup(self.shackle, self.body, self.hole)
        self.add(self.lock)
        self.num = VGroup()
        if number is not None:
            self.num = Text(str(number), font_size=number_size or max(12, int(size * 50)), color=DIM)
            self.num.next_to(self.lock, DOWN, buff=size * 0.12)
            self.add(self.num)

    def _shackle(self, opened):
        s = self.size
        sh = Arc(radius=s * 0.32, start_angle=0, angle=PI).set_stroke(TEXT, s * 10)
        sh.move_to(self.body.get_top() + UP * s * 0.16)
        if opened:
            foot = sh.get_right()
            sh.rotate(-0.6, about_point=foot).shift(UP * s * 0.12)
        return sh

    # ------------------------------------------------------------ animations
    def open(self, run_time=0.6):
        self.is_open = True
        return AnimationGroup(
            Transform(self.shackle, self._shackle(True)),
            self.body.animate.set_fill(self.open_color, 1).set_stroke(outline_of(self.open_color), 3),
            run_time=run_time)

    def close(self, run_time=0.5):
        self.is_open = False
        return AnimationGroup(
            Transform(self.shackle, self._shackle(False)),
            self.body.animate.set_fill(self.closed_color, 1).set_stroke(outline_of(self.closed_color), 3),
            run_time=run_time)

    def wobble(self, run_time=0.8, angle=0.22):
        p = self.body.get_bottom()
        return Succession(Rotate(self.lock, angle, about_point=p, run_time=run_time * 0.25),
                          Rotate(self.lock, -2 * angle, about_point=p, run_time=run_time * 0.5),
                          Rotate(self.lock, angle, about_point=p, run_time=run_time * 0.25))

    def shake(self, run_time=0.6, dx=0.06):
        d = RIGHT * dx
        seg = run_time / 4
        return Succession(self.lock.animate(run_time=seg).shift(d), self.lock.animate(run_time=seg * 2).shift(-2 * d),
                          self.lock.animate(run_time=seg).shift(d))

    def pulse(self, run_time=0.8):
        return Indicate(self.lock, scale_factor=1.3, run_time=run_time)


class PadlockStrip(VGroup):
    """A row of numbered padlocks: ``PadlockStrip(n=5, size=0.28, gap=0.22, at=(-6.6, 3.1),
    opened=())``.  ``at`` is the left end (x) and the lock center line (y).  ``locks`` is the
    list of Padlocks; ``open(i)`` / ``close(i)`` (0-based) return the animations."""

    def __init__(self, n=5, size=0.28, gap=0.22, at=(-6.6, 3.1, 0), opened=(), **kwargs):
        super().__init__(**kwargs)
        self.size = size
        self.locks = [Padlock(size, number=i + 1, opened=(i in opened)) for i in range(n)]
        self.add(*self.locks)
        self.arrange(RIGHT, buff=gap)
        self.move_to(np.array([at[0], at[1], 0.0]), aligned_edge=LEFT)

    def open(self, i, **kw):
        return self.locks[i].open(**kw)

    def close(self, i, **kw):
        return self.locks[i].close(**kw)


__all__ = ["Padlock", "PadlockStrip"]
