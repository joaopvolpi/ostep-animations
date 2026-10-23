"""Episode 11 small icons: Flame, puzzle_piece, censor_bar, neck_bolts."""
import numpy as np
from manim import *

from ..style import *
from .core import outline_of

__all__ = ["Flame", "puzzle_piece", "censor_bar", "neck_bolts"]

FLAME_OUTER = "#FF8A3D"
FLAME_INNER = "#FFD84D"


def _P(x, y=0.0):
    return np.array([float(x), float(y), 0.0])


class Flame(VGroup):
    """Two overlapping polygons (orange outer, yellow inner), ~``height`` tall.

    ``flicker()`` starts a gentle sway/scale updater (``stop_flicker()`` removes it).
    """

    def __init__(self, height=0.8, **kwargs):
        super().__init__(**kwargs)
        outer = Polygon(_P(0, 0.5), _P(0.16, 0.2), _P(0.32, -0.05), _P(0.3, -0.3), _P(0.12, -0.5),
                        _P(-0.12, -0.5), _P(-0.3, -0.3), _P(-0.32, -0.05), _P(-0.14, 0.15))
        outer.round_corners(0.12).set_fill(FLAME_OUTER, 1).set_stroke("#C4561A", 3)
        inner = Polygon(_P(0, 0.12), _P(0.15, -0.12), _P(0.14, -0.32), _P(0, -0.42),
                        _P(-0.14, -0.32), _P(-0.15, -0.12))
        inner.round_corners(0.1).set_fill(FLAME_INNER, 1).set_stroke(width=0)
        self.outer, self.inner = outer, inner
        self.add(outer, inner)
        self.scale(height)
        self._t = 0.0

    def flicker(self, speed=9.0):
        base_h = self.inner.height

        def upd(m, dt):
            m._t += dt
            m.inner.stretch_to_fit_height(base_h * (1 + 0.12 * np.sin(m._t * speed)), about_edge=DOWN)
            m.outer.set_stroke(opacity=0.8 + 0.2 * np.sin(m._t * speed * 1.3))

        self.add_updater(upd)
        return self

    def stop_flicker(self):
        self.clear_updaters()
        return self


def puzzle_piece(size=0.7, color=KERNEL_COLOR):
    """A square puzzle piece with a round knob on top and a notch on the right."""
    s = size
    base = Square(side_length=s).set_fill(color, 1).set_stroke(outline_of(color), 3)
    knob = Circle(radius=s * 0.17).set_fill(color, 1).set_stroke(outline_of(color), 3)
    knob.move_to(base.get_top() + UP * s * 0.12)
    cover = Rectangle(width=s * 0.26, height=s * 0.1).set_fill(color, 1).set_stroke(width=0)
    cover.move_to(base.get_top() + DOWN * 0.02)
    notch = Circle(radius=s * 0.15).set_fill(BG, 1).set_stroke(outline_of(color), 3)
    notch.move_to(base.get_right())
    return VGroup(base, knob, cover, notch)


def censor_bar(width=1.6, height=0.32):
    """Black rounded bar with a small white X-glyph, to cover text."""
    bar = RoundedRectangle(width=width, height=height, corner_radius=0.06).set_fill("#000000", 1)
    bar.set_stroke(DIM, 2)
    x = VGroup(Line(_P(-1, -1), _P(1, 1)), Line(_P(-1, 1), _P(1, -1))).scale(height * 0.18)
    x.set_stroke(TEXT, 3).move_to(bar)
    return VGroup(bar, x)


def neck_bolts(width=0.7, color="#9AA0A6"):
    """Two small bolts (rectangles with a cap) for a Frankenstein neck, ``width`` apart."""
    out = VGroup()
    for sx in (-1, 1):
        shaft = Rectangle(width=0.1, height=0.2).set_fill(color, 1).set_stroke(outline_of(color), 2)
        cap = Rectangle(width=0.1, height=0.07).set_fill(color, 1).set_stroke(outline_of(color), 2)
        cap.next_to(shaft, sx * RIGHT, buff=0)
        cap.rotate(PI / 2).move_to(shaft.get_center() + sx * RIGHT * 0.1)
        b = VGroup(shaft, cap)
        b.move_to(_P(sx * width / 2, 0))
        out.add(b)
    return out
