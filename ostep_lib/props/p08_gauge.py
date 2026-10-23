"""AllotmentGauge: the series' icon for *allotment* (a fuel bar that drains while a job runs).

    g = AllotmentGauge(width=1.2, value=1.0)
    g.attach_to(process)                # sits above the process head and follows it
    self.play(g.drain(1.0, run_time=1.5))     # drain to empty (amount is a fraction of the full bar)
    self.play(g.reset())                      # snaps back to full (with a flash)
    self.play(g.chunk(0.3))                   # ledger mode: use 30%, leaving a tick on the ledger

``value`` is the remaining fraction (1 = full).  The tracker is *not* a submobject
(a ValueTracker would distort the bounding box); it is ``g.tracker``.
"""
from __future__ import annotations

import numpy as np
from manim import (
    AnimationGroup, Line, Rectangle, Succession, ValueTracker, VGroup, Indicate, FadeIn,
    UP, LEFT, DOWN, linear, smooth, Flash, ORIGIN,
)

from ..style import TEXT, DIM, CPU_COLOR, KERNEL_COLOR, BG


class AllotmentGauge(VGroup):
    def __init__(self, width=1.2, value=1.0, height=None, color=CPU_COLOR, **kwargs):
        super().__init__(**kwargs)
        self.w = float(width)
        self.h = float(height) if height else max(0.09, width * 0.14)
        self.color = color
        self.tracker = ValueTracker(float(value))
        self.outline = Rectangle(width=self.w, height=self.h).set_fill(BG, 1).set_stroke(TEXT, 2)
        self.fill = Rectangle(width=self.w, height=self.h).set_fill(color, 1).set_stroke(width=0)
        self.fill.move_to(self.outline)
        self.marks = VGroup()
        self.add(self.outline, self.fill, self.marks)
        self.fill.add_updater(self._sync)
        self._sync(self.fill)
        self._followed = None

    # fill follows the tracker, left-aligned to the outline
    def _sync(self, m):
        v = float(np.clip(self.tracker.get_value(), 0.0, 1.0))
        if v < 0.005:
            m.set_fill(opacity=0)
            return
        m.set_fill(self.color, 1)
        m.stretch_to_fit_width(self.w * v)
        m.align_to(self.outline, LEFT)
        m.match_y(self.outline)

    @property
    def value(self):
        return self.tracker.get_value()

    def drain(self, amount=1.0, run_time=1.5):
        """Animation draining ``amount`` (fraction of the full bar)."""
        return self.tracker.animate(run_time=run_time, rate_func=linear).set_value(max(0.0, self.value - amount))

    def drain_to(self, value, run_time=1.0):
        return self.tracker.animate(run_time=run_time, rate_func=linear).set_value(value)

    def reset(self, run_time=0.5):
        """Snap back to full, with a flash."""
        return AnimationGroup(self.tracker.animate(run_time=run_time, rate_func=smooth).set_value(1.0),
                              Indicate(self.outline, color=self.color, scale_factor=1.15, run_time=run_time))

    def set_now(self, value):
        self.tracker.set_value(value)
        self._sync(self.fill)
        return self

    def chunk(self, amount, run_time=0.6):
        """Ledger mode: use ``amount`` of the bar and leave a separator tick at the new edge."""
        new = max(0.0, self.value - amount)
        x = self.outline.get_left()[0] + self.w * new
        tick = Line([x, self.outline.get_bottom()[1], 0], [x, self.outline.get_top()[1], 0]).set_stroke(BG, 3)
        self.marks.add(tick)
        return AnimationGroup(self.tracker.animate(run_time=run_time, rate_func=linear).set_value(new),
                              FadeIn(tick, run_time=run_time))

    def attach_to(self, mob, gap=0.08):
        """Make the gauge sit above ``mob``'s top edge and follow it."""
        self._followed = mob

        def _follow(g):
            g.move_to(np.array([mob.get_center()[0], mob.get_top()[1] + gap + g.h / 2, 0]))

        self.add_updater(_follow)
        _follow(self)
        return self

    def detach(self):
        self.clear_updaters()
        self.fill.add_updater(self._sync)
        return self


__all__ = ["AllotmentGauge"]
