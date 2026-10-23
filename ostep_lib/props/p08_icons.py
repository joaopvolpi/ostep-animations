"""Episode 08 icons and small props.

* ``gamer_shades(width)``: the dark sunglasses of the scheduler-gamer (process B in 08 and 11).
  Put it on a Process face with ``shades.move_to(proc.get_center() + ...)`` (see ``put_shades``).
* ``mystery_box``, ``tag_chip``, ``history_clock``, ``rr_ring``, ``Dial``, ``SliderPanel``,
  ``voodoo_glyph``, ``mini_pie``, ``medal_glyph``, ``config_glyph``, ``neural_glyph``,
  ``fork_glyph``, ``cache_grid``, ``bookmark_glyph``, ``io_button``.
"""
from __future__ import annotations

import numpy as np
from manim import (
    Arc, Annulus, AnnularSector, Circle, CurvedArrow, Dot, Line, Polygon, Rectangle, RoundedRectangle, Sector,
    Star, Text, VGroup, Rotate, Succession, AnimationGroup, Arrow, ArcBetweenPoints,
    UP, DOWN, LEFT, RIGHT, ORIGIN, PI, TAU,
)

from ..style import TEXT, DIM, BG, VIRT, CPU_COLOR, KERNEL_COLOR, PERS, MONO_FONT, INTRO
from .core import CARD_FILL, ClockIcon, outline_of

GOLD = "#F2C94C"
_INK = "#101010"


def _P(x, y=0.0):
    return np.array([float(x), float(y), 0.0])


def gamer_shades(width=0.5, color=_INK):
    """Dark sunglasses (two rounded lenses, bridge, arms, glints). Centered at the origin."""
    w = width
    lens = lambda dx: RoundedRectangle(width=w * 0.42, height=w * 0.3, corner_radius=w * 0.1).set_fill(color, 1).set_stroke(TEXT, 2).move_to(_P(dx * w * 0.26, 0))
    l, r = lens(-1), lens(1)
    bridge = Line(_P(-w * 0.05, w * 0.05), _P(w * 0.05, w * 0.05)).set_stroke(TEXT, 3)
    arms = VGroup(Line(l.get_left() + _P(0, w * 0.06), l.get_left() + _P(-w * 0.1, w * 0.1)),
                  Line(r.get_right() + _P(0, w * 0.06), r.get_right() + _P(w * 0.1, w * 0.1))).set_stroke(TEXT, 3)
    glints = VGroup(*[Line(m.get_center() + _P(-w * 0.1, w * 0.04), m.get_center() + _P(-w * 0.03, w * 0.1)) for m in (l, r)])
    glints.set_stroke("#FFFFFF", 2, opacity=0.8)
    g = VGroup(l, r, bridge, arms, glints)
    g.lenses = VGroup(l, r)
    return g


def put_shades(proc, scale=1.0):
    """Create shades sized for a Process and put them on its face."""
    sh = gamer_shades(0.5 * proc.get_height() / 1.0 * 0.62 * scale)
    sh.move_to(proc.get_center() + UP * 0.12 * proc.get_height())
    return sh


def tag_chip(text, color=TEXT, font_size=20, stroke=None, fill=CARD_FILL):
    t = Text(text, font_size=font_size, color=color)
    r = RoundedRectangle(width=t.width + 0.3, height=t.height + 0.2, corner_radius=0.1)
    r.set_fill(fill, 1).set_stroke(stroke or color, 2)
    t.move_to(r)
    g = VGroup(r, t)
    g.rect, g.txt = r, t
    return g


def mystery_box(size=1.0, color=DIM):
    r = RoundedRectangle(width=size, height=size, corner_radius=size * 0.15).set_fill(CARD_FILL, 1).set_stroke(color, 3)
    q = Text("?", font_size=int(60 * size), color=CPU_COLOR, weight="BOLD").move_to(r)
    g = VGroup(r, q)
    g.box, g.q = r, q
    return g


def history_clock(radius=0.35, color=INTRO):
    """A clock face ringed by a counterclockwise arrow (look back at the past)."""
    clk = ClockIcon(radius * 0.7, color=color)
    arc = Arc(radius=radius * 1.35, start_angle=PI * 0.15, angle=PI * 1.5, stroke_width=4, color=color)
    tip = arc.copy()
    arc.add_tip(tip_length=0.18, tip_width=0.18)
    g = VGroup(clk, arc)
    g.clock, g.arc = clk, arc
    return g


def rr_ring(radius=0.35, color=TEXT):
    a = CurvedArrow(_P(radius, 0), _P(-radius, 0), angle=-PI * 0.9, color=color, tip_length=0.15, stroke_width=4)
    b = CurvedArrow(_P(-radius, 0), _P(radius, 0), angle=-PI * 0.9, color=color, tip_length=0.15, stroke_width=4)
    return VGroup(a, b)


def io_button(size=0.5):
    r = RoundedRectangle(width=size * 1.5, height=size * 0.8, corner_radius=0.1).set_fill(KERNEL_COLOR, 1).set_stroke(outline_of(KERNEL_COLOR), 3)
    t = Text("I/O", font_size=int(34 * size), color=TEXT, weight="BOLD").move_to(r)
    return VGroup(r, t)


class Dial(VGroup):
    """A dial with a needle and a label.  ``frac`` 0 = far left, 1 = far right."""

    def __init__(self, radius=1.0, label="S", frac=0.5, color=VIRT, **kwargs):
        super().__init__(**kwargs)
        self.r = radius
        self.arc = Arc(radius=radius, start_angle=PI, angle=-PI).set_stroke(TEXT, 4)
        self.ticks = VGroup(*[Line(_P(0.85 * radius * np.cos(a), 0.85 * radius * np.sin(a)),
                                   _P(radius * np.cos(a), radius * np.sin(a))) for a in np.linspace(PI, 0, 9)]).set_stroke(TEXT, 2)
        self.needle = Line(ORIGIN, _P(0.8 * radius, 0)).set_stroke(color, 5)
        self.hub = Dot(radius=0.07 * radius + 0.03, color=color)
        self.label = Text(label, font_size=int(34 * max(radius, 0.6)), color=color, weight="BOLD").next_to(self.hub, DOWN, buff=0.2)
        self.frac = 0.5
        self.add(self.arc, self.ticks, self.needle, self.hub, self.label)
        self.set_now(frac)

    def _angle(self, frac):
        return PI * (1 - frac)

    def set_now(self, frac):
        self.needle.rotate(self._angle(frac) - self._angle(self.frac), about_point=self.hub.get_center())
        self.frac = frac
        return self

    def swing_to(self, frac, run_time=1.0, **kw):
        d = self._angle(frac) - self._angle(self.frac)
        self.frac = frac
        return Rotate(self.needle, angle=d, about_point=self.hub.get_center(), run_time=run_time, **kw)

    def wiggle(self, fracs=(0.2, 0.8, 0.35, 0.65, 0.5), run_time=1.6):
        return Succession(*[self.swing_to(f, run_time=run_time / len(fracs)) for f in fracs])


class SliderPanel(VGroup):
    """Control panel: ``names`` -> one slider each (track, knob, label)."""

    def __init__(self, names, width=3.6, fracs=None, color=VIRT, font_size=20, **kwargs):
        super().__init__(**kwargs)
        n = len(names)
        h = 0.45 + n * 0.62
        self.frame = RoundedRectangle(width=width + 0.5, height=h, corner_radius=0.15).set_fill(CARD_FILL, 1).set_stroke(DIM, 2)
        self.add(self.frame)
        self.tracks, self.knobs, self.labels = [], [], []
        self.w = width
        for i, nm in enumerate(names):
            y = h / 2 - 0.5 - i * 0.62
            lab = Text(nm, font_size=font_size, color=TEXT).move_to(_P(-width / 2, y + 0.2), aligned_edge=LEFT)
            tr = Line(_P(-width / 2, y - 0.08), _P(width / 2, y - 0.08)).set_stroke(DIM, 4)
            f = (fracs[i] if fracs else 0.5)
            kn = Circle(radius=0.12).set_fill(color, 1).set_stroke(TEXT, 2).move_to(_P(-width / 2 + f * width, y - 0.08))
            self.add(lab, tr, kn)
            self.tracks.append(tr)
            self.knobs.append(kn)
            self.labels.append(lab)
        self.fr = list(fracs) if fracs else [0.5] * n

    def move_knob(self, i, frac, run_time=0.8):
        self.fr[i] = frac
        kn, tr = self.knobs[i], self.tracks[i]
        return kn.animate(run_time=run_time).move_to(_P(tr.get_left()[0] + frac * self.w, tr.get_center()[1]))


def voodoo_glyph(size=1.0):
    """A witch-hat with a few stars: 'black magic'."""
    hat = Polygon(_P(-0.5, 0), _P(0.5, 0), _P(0.08, 0.9), _P(-0.1, 0.9)).set_fill("#5B3A8C", 1).set_stroke(outline_of("#5B3A8C"), 3)
    brim = RoundedRectangle(width=1.3, height=0.14, corner_radius=0.07).set_fill("#4A2F73", 1).set_stroke(outline_of("#5B3A8C"), 3).move_to(_P(0, -0.02))
    band = Rectangle(width=0.62, height=0.1).set_fill(GOLD, 1).set_stroke(width=0).move_to(_P(0, 0.18))
    stars = VGroup(*[Star(5, outer_radius=r, inner_radius=r * 0.45).set_fill(GOLD, 1).set_stroke(width=0).move_to(_P(x, y))
                     for r, x, y in ((0.13, -0.75, 0.7), (0.1, 0.8, 0.5), (0.08, 0.55, 1.0))])
    return VGroup(hat, brim, band, stars).scale(size)


def mini_pie(shares, radius=0.5, colors=None, start=PI / 2):
    """``shares``: list of (fraction, color).  Returns a VGroup of Sectors (clockwise from 12 o'clock)."""
    g = VGroup()
    a = start
    for f, c in shares:
        if f > 0.001:
            g.add(Sector(radius=radius, start_angle=a, angle=-TAU * f).set_fill(c, 1).set_stroke(BG, 2))
        a -= TAU * f
    return g


def medal_glyph(size=0.5):
    ribbon = Polygon(_P(-0.18, 0.4), _P(0.18, 0.4), _P(0.3, -0.1), _P(0.0, 0.05), _P(-0.3, -0.1)).set_fill(KERNEL_COLOR, 1).set_stroke(width=0)
    disc = Circle(radius=0.26).set_fill(GOLD, 1).set_stroke(outline_of(GOLD), 3).move_to(_P(0, -0.15))
    star = Star(5, outer_radius=0.14, inner_radius=0.06).set_fill(outline_of(GOLD, 0.4), 1).set_stroke(width=0).move_to(disc)
    return VGroup(ribbon, disc, star).scale(size / 0.8)


def config_glyph(text="S = 1000  # default", width=3.2, font_size=20):
    page = RoundedRectangle(width=width, height=0.9, corner_radius=0.08).set_fill("#2B2B2B", 1).set_stroke(DIM, 2)
    t = Text(text, font=MONO_FONT, font_size=font_size, color=PERS).move_to(page)
    lines = VGroup(*[Line(_P(-width / 2 + 0.2, y), _P(-width / 2 + 0.2 + w, y)).set_stroke(DIM, 2) for y, w in ((0.3, 1.2), (-0.3, 0.8))])
    lines.move_to(page.get_center() + _P(0, 0))
    lines[0].move_to(page.get_top() + _P(-width / 2 + 1.0, -0.12))
    lines[1].move_to(page.get_bottom() + _P(-width / 2 + 0.8, 0.12))
    return VGroup(page, lines, t)


def neural_glyph(size=1.0):
    cols = [[_P(-0.5, 0.3), _P(-0.5, -0.3)], [_P(0, 0.45), _P(0, 0), _P(0, -0.45)], [_P(0.5, 0.0)]]
    edges = VGroup(*[Line(a, b) for ca, cb in zip(cols, cols[1:]) for a in ca for b in cb]).set_stroke(DIM, 2)
    dots = VGroup(*[Dot(p, radius=0.08, color=VIRT) for c in cols for p in c])
    return VGroup(edges, dots).scale(size)


def fork_glyph(size=0.6, color=TEXT):
    """A branching path (branch predictor)."""
    stem = Line(_P(0, -0.4), _P(0, 0.0))
    l = Line(_P(0, 0.0), _P(-0.3, 0.4))
    r = Line(_P(0, 0.0), _P(0.3, 0.4))
    return VGroup(stem, l, r).set_stroke(color, 4).scale(size / 0.8)


def cache_grid(size=0.6, color=TEXT):
    g = VGroup(*[Rectangle(width=0.22, height=0.22).set_stroke(color, 2).set_fill(CPU_COLOR if (i + j) % 2 else BG, 0.5)
                 for i in range(3) for j in range(2)]).arrange_in_grid(2, 3, buff=0)
    return g.scale(size / 0.7)


def bookmark_glyph(size=0.4, color=KERNEL_COLOR):
    return Polygon(_P(-0.15, 0.25), _P(0.15, 0.25), _P(0.15, -0.25), _P(0, -0.1), _P(-0.15, -0.25)).set_fill(color, 1).set_stroke(outline_of(color), 2).scale(size / 0.5)


__all__ = ["gamer_shades", "put_shades", "tag_chip", "mystery_box", "history_clock", "rr_ring", "io_button", "Dial",
           "SliderPanel", "voodoo_glyph", "mini_pie", "medal_glyph", "config_glyph", "neural_glyph", "fork_glyph",
           "cache_grid", "bookmark_glyph", "GOLD"]
