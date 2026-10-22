"""Episode-07 icons: CrystalBall (the oracle), Cart, Checkout, milk carton, checkbook.

    ball = CrystalBall(0.5)
    self.play(ball.glow_up())            # warm glow          (glow_down() to fade it)
    self.play(ball.crack())              # a zigzag crack draws and the glow dies

    cart = Cart(1.0, boxes=4)            # outline basket on two wheels, colored boxes inside
    desk = Checkout(2.4)                 # counter + register; desk.blink() blinks the light
"""
from __future__ import annotations

import numpy as np
from manim import (
    AnimationGroup, Circle, Dot, Ellipse, Indicate, Line, Polygon, Rectangle, RoundedRectangle,
    Text, UpdateFromAlphaFunc, VGroup, VMobject, LEFT, RIGHT, UP, DOWN, PI,
)

from ..style import TEXT, DIM, BG, CPU_COLOR, PROCESS_COLORS, CONC, VIRT, KERNEL_COLOR
from ..characters.base import mix
from .core import CARD_FILL, INK, outline_of


class CrystalBall(VGroup):
    """A glass ball on a stand.  ``CrystalBall(radius=0.5, color=CONC)``.
    Parts: ``glow``, ``ball``, ``shine``, ``stand``, ``crack`` (invisible until ``crack()``).
    ``glow_up()`` / ``glow_down()`` animations, ``crack()`` animation."""

    def __init__(self, radius=0.5, color=CONC, **kwargs):
        super().__init__(**kwargs)
        r = radius
        self.stand = Polygon([-r * 0.55, -r * 1.15, 0], [r * 0.55, -r * 1.15, 0], [r * 0.38, -r * 0.82, 0],
                             [-r * 0.38, -r * 0.82, 0]).set_fill("#7A5C3A", 1).set_stroke(outline_of("#7A5C3A", 0.5), 3)
        self.glow = Circle(radius=r * 1.3).set_fill(color, 0).set_stroke(width=0)
        self.ball = Circle(radius=r).set_fill(mix(color, BG, 0.45), 0.9).set_stroke(outline_of(color, 0.4), 4)
        self.shine = Ellipse(width=r * 0.5, height=r * 0.28).rotate(0.7).move_to([-r * 0.4, r * 0.45, 0])
        self.shine.set_fill("#FFFFFF", 0.5).set_stroke(width=0)
        sparkle = Dot([r * 0.3, -r * 0.1, 0], radius=r * 0.06).set_fill("#FFFFFF", 0.6).set_stroke(width=0)
        pts = [[r * 0.25, r * 0.95, 0], [r * 0.05, r * 0.55, 0], [r * 0.3, r * 0.3, 0], [-r * 0.05, -r * 0.05, 0],
               [r * 0.2, -r * 0.35, 0], [-r * 0.1, -r * 0.7, 0]]
        self.crack_full = VMobject().set_points_as_corners([np.array(p) for p in pts])
        self.crack_full.set_stroke(TEXT, 4, opacity=0).set_fill(opacity=0)   # reference path (invisible)
        self.crack_mob = self.crack_full.copy().set_stroke(opacity=0)
        self.add(self.glow, self.stand, self.ball, self.shine, sparkle, self.crack_full, self.crack_mob)

    def glow_up(self, run_time=0.8, amount=0.25):
        return self.glow.animate(run_time=run_time).set_fill(CPU_COLOR, amount)

    def glow_down(self, run_time=0.6):
        return self.glow.animate(run_time=run_time).set_fill(opacity=0)

    def crack(self, run_time=1.0):
        full = self.crack_full

        def upd(m, a):
            m.set_stroke(TEXT, 4, opacity=1)
            m.pointwise_become_partial(full, 0, a)
        return AnimationGroup(UpdateFromAlphaFunc(self.crack_mob, upd, run_time=run_time),
                              self.glow.animate(run_time=run_time).set_fill(opacity=0),
                              self.ball.animate(run_time=run_time).set_fill(DIM, 0.6))


def _box(w, h, color):
    return Rectangle(width=w, height=h).set_fill(color, 1).set_stroke(outline_of(color), 2)


class Cart(VGroup):
    """Shopping cart (outline basket, handle, two wheels) with ``boxes`` colored boxes piled
    inside.  ``Cart(size=1.0, boxes=0, color=TEXT)``; ``size`` is the basket width.
    Parts: ``basket``, ``handle``, ``wheels``, ``boxes`` (VGroup)."""

    def __init__(self, size=1.0, boxes=0, color=TEXT, **kwargs):
        super().__init__(**kwargs)
        s = size
        self.basket = Polygon([-s * 0.5, s * 0.3, 0], [s * 0.5, s * 0.3, 0], [s * 0.38, -s * 0.1, 0],
                              [-s * 0.38, -s * 0.1, 0]).set_fill(CARD_FILL, 1).set_stroke(color, 3)
        self.handle = Line([-s * 0.5, s * 0.3, 0], [-s * 0.62, s * 0.52, 0]).set_stroke(color, 3)
        self.wheels = VGroup(*[Circle(radius=s * 0.07).set_fill(color, 1).set_stroke(color, 1).move_to([x * s, -s * 0.2, 0])
                               for x in (-0.25, 0.25)])
        self.boxes = VGroup()
        cols = [PROCESS_COLORS[0], PROCESS_COLORS[2], PROCESS_COLORS[3], PROCESS_COLORS[4], PROCESS_COLORS[1]]
        for k in range(boxes):
            row, col = divmod(k, 3)
            b = _box(s * 0.22, s * 0.18, cols[k % len(cols)])
            b.move_to([(col - 1) * s * 0.26, s * (0.4 + 0.18 * row), 0])
            self.boxes.add(b)
        self.add(self.boxes, self.basket, self.handle, self.wheels)


class Checkout(VGroup):
    """Counter with a register.  ``Checkout(width=2.4)``.  Parts: ``counter``, ``register``,
    ``screen``, ``light``.  ``blink()`` pulses the light."""

    def __init__(self, width=2.4, **kwargs):
        super().__init__(**kwargs)
        w = width
        self.counter = RoundedRectangle(width=w, height=w * 0.38, corner_radius=0.08).set_fill(CARD_FILL, 1).set_stroke(DIM, 3)
        self.register = RoundedRectangle(width=w * 0.34, height=w * 0.3, corner_radius=0.05)
        self.register.set_fill("#2E2E2E", 1).set_stroke(TEXT, 2).move_to(self.counter.get_top() + UP * w * 0.12 + RIGHT * w * 0.22)
        self.screen = Rectangle(width=w * 0.22, height=w * 0.09).set_fill("#101010", 1).set_stroke(DIM, 1.5)
        self.screen.move_to(self.register.get_center() + UP * w * 0.05)
        self.light = Dot(self.register.get_center() + DOWN * w * 0.07, radius=w * 0.03).set_fill(KERNEL_COLOR, 1)
        belt = Line(self.counter.get_left() + RIGHT * w * 0.08 + UP * w * 0.08, self.counter.get_center() + LEFT * w * 0.05 + UP * w * 0.08)
        belt.set_stroke(DIM, 2)
        self.add(self.counter, belt, self.register, self.screen, self.light)

    def blink(self, run_time=0.6):
        return Indicate(self.light, scale_factor=2.0, color=CPU_COLOR, run_time=run_time)


def milk_carton(size=0.5, color="#E8E2D0"):
    """Little milk carton glyph (gable top, blue label). ``size`` = height."""
    s = size
    body = Rectangle(width=s * 0.55, height=s * 0.65).set_fill(color, 1).set_stroke(outline_of(color, 0.5), 2)
    roof = Polygon([-s * 0.275, s * 0.325, 0], [s * 0.275, s * 0.325, 0], [s * 0.2, s * 0.5, 0], [-s * 0.2, s * 0.5, 0])
    roof.set_fill(mix(color, "#FFFFFF", 0.3), 1).set_stroke(outline_of(color, 0.5), 2)
    label = Rectangle(width=s * 0.55, height=s * 0.22).set_fill("#6FA8F7", 1).set_stroke(width=0).move_to(body.get_center() + DOWN * s * 0.05)
    return VGroup(body, roof, label)


def checkbook_icon(size=0.5):
    """Small checkbook glyph (booklet with lines and a pen stripe). ``size`` = width."""
    s = size
    cover = RoundedRectangle(width=s, height=s * 0.62, corner_radius=s * 0.05).set_fill("#5FC6A8", 1).set_stroke(outline_of("#5FC6A8"), 2)
    lines = VGroup(*[Line([-s * 0.35, y * s, 0], [s * 0.35, y * s, 0]) for y in (0.08, -0.02, -0.12)]).set_stroke(TEXT, 1.5, opacity=0.8)
    stripe = Rectangle(width=s * 0.1, height=s * 0.62).set_fill(outline_of("#5FC6A8"), 1).set_stroke(width=0).align_to(cover, LEFT)
    return VGroup(cover, stripe, lines)


__all__ = ["CrystalBall", "Cart", "Checkout", "milk_carton", "checkbook_icon"]
