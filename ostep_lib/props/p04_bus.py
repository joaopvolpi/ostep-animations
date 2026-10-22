"""Bus: a horizontal system bus with vertical stubs to devices (Figure 4.1).

    bus = Bus(y=-0.6, x_range=(-5, 5), taps=[cpu.get_bottom(), mem.get_bottom(), disk.get_top()])
    path = bus.path(disk.get_top(), mem.get_bottom())    # VMobject along the wires
    self.play(MoveAlongPath(chunk, path))

``taps`` are device anchor points; each gets a vertical stub to the bus line.
``path(a, b)`` returns a polyline a -> (a.x, bus) -> (b.x, bus) -> b.
"""
from __future__ import annotations

import numpy as np
from manim import Arrow, DoubleArrow, Line, VGroup, VMobject, StealthTip, Dot

from ..style import DIM, TEXT


def _P(x, y=0.0):
    return np.array([float(x), float(y), 0.0])


def _pt(p):
    p = np.array(p, dtype=float).flatten()
    return np.array([p[0], p[1], 0.0])


class Bus(VGroup):
    """Parameters: ``y`` (bus height), ``x_range``, ``taps`` (list of points),
    ``color``, ``stroke_width``, ``arrows`` (arrow tips at both ends)."""

    def __init__(self, y=-0.6, x_range=(-5, 5), taps=(), color=DIM, stroke_width=5, arrows=True,
                 **kwargs):
        super().__init__(**kwargs)
        self.bus_y = float(y)
        self.color = color
        x0, x1 = x_range
        if arrows:
            self.line = DoubleArrow(_P(x0, y), _P(x1, y), buff=0, stroke_width=stroke_width,
                                    tip_length=0.22, color=color, max_tip_length_to_length_ratio=0.1)
        else:
            self.line = Line(_P(x0, y), _P(x1, y)).set_stroke(color, stroke_width)
        self.stubs = VGroup()
        self.add(self.line, self.stubs)
        for t in taps:
            self.add_tap(t)

    @property
    def y(self):
        return self.line.get_center()[1]

    def add_tap(self, point):
        p = _pt(point)
        stub = Line(p, _P(p[0], self.y)).set_stroke(self.color, self.line.get_stroke_width() * 0.8)
        joint = Dot(_P(p[0], self.y), radius=0.06, color=self.color)
        g = VGroup(stub, joint)
        self.stubs.add(g)
        return g

    def path(self, a, b):
        """Polyline from point ``a`` down/up to the bus, along it, then to ``b``."""
        a = _pt(a)
        b = _pt(b)
        pts = [a, _P(a[0], self.y), _P(b[0], self.y), b]
        m = VMobject()
        m.set_points_as_corners(pts)
        return m


__all__ = ["Bus"]
