"""Small icons for episode 09 (proportional share).  All are VGroups centered on ORIGIN."""
from __future__ import annotations

import numpy as np
from manim import (
    Arc, Circle, Dot, Line, Polygon, Rectangle, RoundedRectangle, Text, VGroup, Rotate, TAU, PI,
    DOWN, LEFT, RIGHT, UP, ORIGIN,
)

from ..style import BG, DIM, TEXT, CPU_COLOR, PROCESS_COLORS, KERNEL_COLOR
from .core import INK, outline_of

__all__ = ["cloud_icon", "vm_window", "coin_icon", "die_icon", "handshake_icon", "paper_chip",
           "bad_luck_cloud", "sched_chip", "text_editor_icon"]

CLOUD = "#B9C7D6"


def _P(x, y=0.0):
    return np.array([float(x), float(y), 0.0])


def cloud_icon(width=2.0, color=CLOUD):
    """A flat cloud made of overlapping circles."""
    w = width
    parts = [Circle(radius=w * 0.2).move_to(_P(-w * 0.25, -w * 0.02)),
             Circle(radius=w * 0.27).move_to(_P(0.0, w * 0.1)),
             Circle(radius=w * 0.2).move_to(_P(w * 0.26, -w * 0.02)),
             Rectangle(width=w * 0.7, height=w * 0.22).move_to(_P(0, -w * 0.1))]
    g = VGroup(*parts).set_fill(color, 1).set_stroke(color, 0)
    outline = VGroup(*[p.copy() for p in parts]).set_fill(color, 1).set_stroke(outline_of(color), 3)
    outline.set_z_index(-1)
    base = VGroup(outline, g)
    return base.move_to(ORIGIN)


def vm_window(label, color, width=1.5, height=1.0, share=None):
    """A little window: title bar with 3 dots, a colored body, label (and optional share text)."""
    body = RoundedRectangle(width=width, height=height, corner_radius=0.08).set_fill(color, 0.25).set_stroke(color, 3)
    bar = Rectangle(width=width, height=height * 0.2).set_fill(color, 0.9).set_stroke(color, 0)
    bar.move_to(body.get_top() + DOWN * height * 0.1)
    dots = VGroup(*[Dot(radius=0.03, color=INK).move_to(bar.get_left() + RIGHT * (0.12 + 0.1 * k)) for k in range(3)])
    t = Text(label, font_size=22, color=TEXT).move_to(body.get_center() + DOWN * height * 0.08)
    g = VGroup(body, bar, dots, t)
    if share:
        g.add(Text(share, font_size=20, color=color).next_to(t, DOWN, buff=0.05))
    return g


def coin_icon(size=0.5, color=CPU_COLOR):
    c = Circle(radius=size / 2).set_fill(color, 1).set_stroke(outline_of(color), 3)
    inner = Circle(radius=size * 0.33).set_fill(color, 0).set_stroke(outline_of(color), 2)
    return VGroup(c, inner)


def die_icon(size=0.55, color=TEXT, pips=5):
    body = RoundedRectangle(width=size, height=size, corner_radius=size * 0.18).set_fill(color, 1).set_stroke(DIM, 2)
    pos = {1: [(0, 0)], 2: [(-1, 1), (1, -1)], 3: [(-1, 1), (0, 0), (1, -1)],
           4: [(-1, 1), (1, 1), (-1, -1), (1, -1)], 5: [(-1, 1), (1, 1), (0, 0), (-1, -1), (1, -1)],
           6: [(-1, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (1, -1)]}[pips]
    dots = VGroup(*[Dot(_P(x * size * 0.25, y * size * 0.25), radius=size * 0.07, color=INK) for x, y in pos])
    return VGroup(body, dots)


def handshake_icon(size=0.8, color_a=PROCESS_COLORS[0], color_b=PROCESS_COLORS[1]):
    """Two hands meeting: two rounded cuffs and clasped middle."""
    l = RoundedRectangle(width=size * 0.5, height=size * 0.3, corner_radius=0.08).set_fill(color_a, 1) \
        .set_stroke(outline_of(color_a), 2).move_to(_P(-size * 0.28, 0))
    r = RoundedRectangle(width=size * 0.5, height=size * 0.3, corner_radius=0.08).set_fill(color_b, 1) \
        .set_stroke(outline_of(color_b), 2).move_to(_P(size * 0.28, 0))
    mid = Circle(radius=size * 0.17).set_fill(TEXT, 1).set_stroke(DIM, 2)
    return VGroup(l, r, mid)


def paper_chip(text="Waldspurger & Weihl, 1994", font_size=20, color=TEXT):
    t = Text(text, font_size=font_size, color=INK)
    page = RoundedRectangle(width=t.width + 0.5, height=t.height + 0.35, corner_radius=0.08) \
        .set_fill("#E9E4D4", 1).set_stroke("#B8B09A", 2)
    lines = VGroup(*[Line(LEFT * 0.0, RIGHT * 0.2).set_stroke("#B8B09A", 2) for _ in range(0)])
    t.move_to(page)
    return VGroup(page, t)


def bad_luck_cloud(text="bad luck", width=1.6):
    c = cloud_icon(width, color="#7C8794")
    t = Text(text, font_size=20, color=TEXT).move_to(c.get_center() + DOWN * width * 0.03)
    bolt = Polygon(_P(0.06, 0.2), _P(-0.08, -0.02), _P(0.0, -0.02), _P(-0.06, -0.24), _P(0.1, 0.02), _P(0.01, 0.02)) \
        .set_fill(CPU_COLOR, 1).set_stroke(INK, 1).scale(width * 0.45).next_to(c, DOWN, buff=-0.05)
    return VGroup(c, t, bolt)


def sched_chip(text, width=1.0, height=0.5, color=DIM, font_size=22):
    r = RoundedRectangle(width=width, height=height, corner_radius=0.12).set_fill(BG, 1).set_stroke(color, 2.5)
    t = Text(text, font_size=font_size, color=TEXT).move_to(r)
    return VGroup(r, t)


def text_editor_icon(width=0.9):
    body = RoundedRectangle(width=width, height=width * 0.7, corner_radius=0.06).set_fill("#2B2B2B", 1).set_stroke(TEXT, 2)
    lines = VGroup(*[Line(LEFT * width * 0.3, RIGHT * width * (0.3 - 0.08 * k)).set_stroke(TEXT, 2)
                     .shift(UP * width * (0.2 - 0.12 * k)) for k in range(3)])
    lines.align_to(body.get_left() + RIGHT * 0.12, LEFT)
    return VGroup(body, lines)
