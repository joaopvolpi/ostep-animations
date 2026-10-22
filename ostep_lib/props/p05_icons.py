"""Small glyphs and icons introduced in episode 05 (the Process API).

All are ``VGroup``s roughly ``size`` units across, centered on ORIGIN: place them with
``.move_to()`` / ``.scale()``.  Built from Manim primitives and series colors only.
"""
from __future__ import annotations

import numpy as np
from manim import (
    Arc, Circle, DashedVMobject, Line, Polygon, Rectangle, RoundedRectangle, Text, VGroup,
    VMobject, AnimationGroup, Succession, there_and_back, ORIGIN, UP, DOWN, LEFT, RIGHT, PI, TAU,
)

from ..style import (
    TEXT, DIM, BG, CPU_COLOR, KERNEL_COLOR, USER_COLOR, MONO_FONT, FONT, PROCESS_COLORS,
)
from ..characters import Process
from .core import CARD_FILL

__all__ = [
    "bolt_glyph", "Keycap", "handler_box", "shield_arc", "crown_tag", "glass_pane",
    "wrench_glyph", "program_chip", "mem_icon_small",
    "zombie_mini", "stop_sign_tag",
]


def _P(x, y=0.0):
    return np.array([float(x), float(y), 0.0])


def bolt_glyph(size=0.7, color=CPU_COLOR, label=None, font_size=18):
    """A lightning bolt (``size`` tall); with ``label`` a mono caption under it.
    ``.bolt`` is the polygon, ``.label`` the caption (or None)."""
    pts = [_P(0.12, 0.5), _P(-0.3, -0.06), _P(-0.04, -0.06), _P(-0.14, -0.5), _P(0.3, 0.1), _P(0.04, 0.1)]
    bolt = Polygon(*pts).set_fill(color, 1).set_stroke(TEXT, 2).scale(size)
    g = VGroup(bolt)
    g.bolt, g.label = bolt, None
    if label:
        t = Text(label, font=MONO_FONT, font_size=font_size, color=color)
        t.next_to(bolt, DOWN, buff=0.08)
        g.add(t)
        g.label = t
    return g


class Keycap(VGroup):
    """A keyboard key (``Keycap("ctrl")``).  ``press()`` is a short push-down animation."""

    def __init__(self, text, size=0.55, font_size=22, **kwargs):
        super().__init__(**kwargs)
        t = Text(text, font=MONO_FONT, font_size=font_size, color=TEXT)
        w = max(size, t.width + 0.28)
        base = RoundedRectangle(width=w, height=size, corner_radius=0.08).set_fill(CARD_FILL, 1).set_stroke(DIM, 3)
        top = RoundedRectangle(width=w - 0.1, height=size - 0.12, corner_radius=0.06)
        top.set_fill("#333333", 1).set_stroke(TEXT, 1.5).move_to(base.get_center() + UP * 0.03)
        t.move_to(top)
        self.add(base, top, t)
        self.top_cap = VGroup(top, t)

    def press(self, run_time=0.3):
        return self.top_cap.animate(run_time=run_time, rate_func=there_and_back).shift(DOWN * 0.05)


def handler_box(label="handler()", font_size=20, color=USER_COLOR):
    """A small code box (the signal handler a process holds up)."""
    t = Text(label, font=MONO_FONT, font_size=font_size, color=TEXT)
    box = RoundedRectangle(width=t.width + 0.3, height=t.height + 0.25, corner_radius=0.08)
    box.set_fill(CARD_FILL, 1).set_stroke(color, 3).move_to(t)
    g = VGroup(box, t)
    g.box = box
    return g


def shield_arc(radius=1.6, facing=LEFT, spread=PI * 0.75, color=USER_COLOR, center=ORIGIN):
    """A translucent dashed force-field arc around ``center``, bulging toward ``facing``."""
    ang = np.arctan2(facing[1], facing[0])
    arc = Arc(radius=radius, start_angle=ang - spread / 2, angle=spread, arc_center=center)
    glow = arc.copy().set_stroke(color, 16, opacity=0.18)
    dashed = DashedVMobject(arc, num_dashes=18).set_stroke(color, 5)
    g = VGroup(glow, dashed)
    g.arc = arc
    return g


def crown_tag(text="root", font_size=22, color=CPU_COLOR):
    """A small crown above a 'root' tag."""
    crown = Polygon(_P(-0.3, -0.15), _P(-0.34, 0.2), _P(-0.15, 0.02), _P(0, 0.26), _P(0.15, 0.02),
                    _P(0.34, 0.2), _P(0.3, -0.15))
    crown.set_fill(color, 1).set_stroke(TEXT, 2)
    t = Text(text, font=MONO_FONT, font_size=font_size, color=color, weight="BOLD")
    box = RoundedRectangle(width=t.width + 0.3, height=t.height + 0.2, corner_radius=0.08)
    box.set_fill(CARD_FILL, 1).set_stroke(color, 2.5).move_to(t)
    crown.next_to(box, UP, buff=0.04)
    return VGroup(crown, box, t)


def glass_pane(width=6.0, height=1.2, color=TEXT):
    """A translucent rounded rectangle with two diagonal highlight stripes."""
    pane = RoundedRectangle(width=width, height=height, corner_radius=0.12)
    pane.set_fill(color, 0.07).set_stroke(color, 2.5, opacity=0.5)
    stripes = VGroup()
    for x0, w in ((-0.3 * width, 0.25), (-0.18 * width, 0.08)):
        s = Polygon(_P(x0, -height / 2 + 0.08), _P(x0 + w, -height / 2 + 0.08),
                    _P(x0 + w + height * 0.5, height / 2 - 0.08), _P(x0 + height * 0.5, height / 2 - 0.08))
        s.set_fill(color, 0.12).set_stroke(width=0)
        stripes.add(s)
    return VGroup(pane, stripes)


def wrench_glyph(size=0.6, color=DIM):
    """A wrench (handle plus open jaw)."""
    handle = Line(_P(-0.3, -0.3), _P(0.12, 0.12)).set_stroke(color, 9)
    jaw = Arc(radius=0.17, start_angle=PI / 4 + 0.55, angle=TAU - 1.1, arc_center=_P(0.22, 0.22))
    jaw.set_stroke(color, 8)
    return VGroup(handle, jaw).scale(size / 0.6).move_to(ORIGIN)


def program_chip(name, color=DIM, font_size=18, mono=True):
    """A rounded 'program' chip (e.g. ``p3``, ``wc``, ``fork()``): DIM by default."""
    t = Text(name, font=MONO_FONT if mono else FONT, font_size=font_size, color=TEXT)
    box = RoundedRectangle(width=t.width + 0.28, height=t.height + 0.2, corner_radius=0.08)
    box.set_fill(CARD_FILL, 1).set_stroke(color, 2).move_to(t)
    g = VGroup(box, t)
    g.box, g.text = box, t
    return g


def mem_icon_small(color=PROCESS_COLORS[0], width=0.55, height=0.75, cells=4):
    """A tiny memory column icon (stacked cells in ``color``)."""
    col = VGroup(*[Rectangle(width=width, height=height / cells).set_fill(color, 0.35).set_stroke(color, 2)
                   for _ in range(cells)]).arrange(DOWN, buff=0)
    return col


def zombie_mini(scale=0.4, label=None):
    """The 04 zombie expression at a small scale (for timeline rows)."""
    return Process("zombie", label=label).scale(scale)


def stop_sign_tag(text="stop 29146", font_size=20, color=KERNEL_COLOR):
    """A tag with a pause glyph in front of a mono command."""
    from .core import PauseGlyph
    t = Text(text, font=MONO_FONT, font_size=font_size, color=TEXT)
    p = PauseGlyph(0.3, color=color)
    row = VGroup(p, t).arrange(RIGHT, buff=0.12)
    box = RoundedRectangle(width=row.width + 0.3, height=row.height + 0.22, corner_radius=0.08)
    box.set_fill(CARD_FILL, 1).set_stroke(color, 2.5).move_to(row)
    return VGroup(box, row)
