"""Episode 10 icons: suitcase (migration), pushpin (affinity), flame (warmth), hand-up.

All are plain VGroups built from primitives; ``size`` is roughly the height.
"""
from __future__ import annotations

import numpy as np
from manim import (
    Arc, Circle, Line, Polygon, Rectangle, RoundedRectangle, VGroup, VMobject, DOWN, UP, PI,
)

from ..style import TEXT, DIM, BG, KERNEL_COLOR, CPU_COLOR, VIRT
from .core import INK, outline_of
from .p04_icons import mix

__all__ = ["suitcase_icon", "pin_icon", "flame_icon", "hand_up_icon"]


def _P(x, y=0.0):
    return np.array([float(x), float(y), 0.0])


def suitcase_icon(size=0.45, color="#C9A36B"):
    """Small rounded suitcase with a handle and two straps."""
    body = RoundedRectangle(width=size * 1.3, height=size * 0.9, corner_radius=size * 0.1)
    body.set_fill(color, 1).set_stroke(outline_of(color), 2.5)
    handle = Arc(radius=size * 0.2, start_angle=0, angle=PI).set_stroke(outline_of(color), 3)
    handle.next_to(body, UP, buff=-size * 0.02)
    straps = VGroup(*[Line(_P(x * size, -size * 0.45), _P(x * size, size * 0.45)) for x in (-0.3, 0.3)])
    straps.set_stroke(outline_of(color), 2.5).move_to(body)
    clasp = Rectangle(width=size * 0.14, height=size * 0.12).set_fill(INK, 1).set_stroke(width=0).move_to(body)
    return VGroup(handle, body, straps, clasp)


def pin_icon(size=0.45, color=KERNEL_COLOR):
    """Pushpin seen from the side: round head, short stem, needle."""
    head = Circle(radius=size * 0.26).set_fill(color, 1).set_stroke(outline_of(color), 2.5)
    shine = Circle(radius=size * 0.07).set_fill("#FFFFFF", 0.7).set_stroke(width=0)
    shine.move_to(head.get_center() + _P(-size * 0.08, size * 0.08))
    collar = Rectangle(width=size * 0.5, height=size * 0.08).set_fill(color, 1).set_stroke(outline_of(color), 2)
    collar.next_to(head, DOWN, buff=-size * 0.03)
    needle = Polygon(_P(-size * 0.04, 0), _P(size * 0.04, 0), _P(0, -size * 0.34))
    needle.set_fill("#C9C9C9", 1).set_stroke("#888888", 1.5)
    needle.next_to(collar, DOWN, buff=-0.01)
    return VGroup(needle, collar, head, shine)


def flame_icon(size=0.45, color=CPU_COLOR):
    """A small flame (warmth)."""
    outer = Polygon(
        _P(0, 0.55), _P(0.22, 0.12), _P(0.36, -0.2), _P(0.18, -0.5), _P(-0.18, -0.5), _P(-0.36, -0.2),
        _P(-0.2, 0.1))
    outer.round_corners(0.12)
    outer.set_fill(color, 1).set_stroke(outline_of(color), 2.5)
    inner = Polygon(_P(0, 0.05), _P(0.14, -0.2), _P(0.08, -0.4), _P(-0.08, -0.4), _P(-0.14, -0.2))
    inner.round_corners(0.06)
    inner.set_fill(mix(color, "#FFFFFF", 0.6), 1).set_stroke(width=0)
    g = VGroup(outer, inner)
    g.scale_to_fit_height(size)
    return g


def hand_up_icon(size=0.5, color="#F2D0A9"):
    """A raised palm ("hold that thought"): palm + four fingers + thumb."""
    palm = RoundedRectangle(width=size * 0.8, height=size * 0.7, corner_radius=size * 0.15)
    fingers = VGroup(*[
        RoundedRectangle(width=size * 0.16, height=size * (0.55 + 0.12 * (1 - abs(i - 1.5) / 1.5)), corner_radius=size * 0.08)
        for i in range(4)
    ]).arrange(1 * 1.0 * np.array([1, 0, 0]), buff=size * 0.03, aligned_edge=DOWN)
    fingers.next_to(palm, UP, buff=-size * 0.1)
    thumb = RoundedRectangle(width=size * 0.16, height=size * 0.4, corner_radius=size * 0.08)
    thumb.rotate(-0.8).move_to(palm.get_left() + _P(-size * 0.02, size * 0.0))
    g = VGroup(thumb, palm, fingers)
    g.set_fill(color, 1).set_stroke(outline_of(color), 2.5)
    return g
