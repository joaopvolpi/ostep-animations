"""Raffle drum, tickets and the seesaw (episode 09; also used by 08 and 11).

    drum = RaffleDrum(size=1.4)
    self.play(drum.spin(turns=1, run_time=1.5))          # the cage turns
    ball, anim = drum.draw(63, color=PROCESS_COLORS[0])   # numbered ball rolls out of the chute
    self.play(anim)                                       # (the ball is added by the animation)
    self.play(hop_to(ball, point, anchor="center"))

    t = Ticket(PROCESS_COLORS[0])                         # one stub
    st = TicketStack(75, PROCESS_COLORS[0])               # fanned stubs + count label
    self.play(st.set_count(80))
    self.play(st.hop_to(point))

    ss = Seesaw(width=3.0, left="often", right="rarely")  # beam + pivot + two labelled pans
    self.play(ss.tilt(12))                                # degrees; > 0: left side goes down
"""
from __future__ import annotations

import numpy as np
from manim import (
    AnimationGroup, Arc, Circle, Dot, FadeIn, Line, Polygon, Rectangle, Rotate, RoundedRectangle,
    Succession, Text, Transform, UpdateFromAlphaFunc, VGroup, DEGREES, DOWN, LEFT, ORIGIN, RIGHT, TAU, UP,
    rate_functions,
)

from ..style import BG, DIM, TEXT, CPU_COLOR, PROCESS_COLORS
from .core import INK, hop_to, outline_of

__all__ = ["RaffleDrum", "Ticket", "TicketStack", "Seesaw"]


def _P(x, y=0.0):
    return np.array([float(x), float(y), 0.0])


# ---------------------------------------------------------------------------
class Ticket(VGroup):
    """A raffle stub, notched on both sides, in the owner's color with ``TEXT`` stub lines.

    ``Ticket(color=PROCESS_COLORS[0], label=None, width=0.35, height=0.2)``.  Parts: ``body``,
    ``notches``, ``lines``, ``label`` (optional text on the stub)."""

    def __init__(self, color=PROCESS_COLORS[0], label=None, width=0.35, height=0.2, **kwargs):
        super().__init__(**kwargs)
        self.color = color
        body = RoundedRectangle(width=width, height=height, corner_radius=height * 0.18)
        body.set_fill(color, 1).set_stroke(outline_of(color), max(1.5, height * 10))
        r = height * 0.2
        notches = VGroup(*[Circle(radius=r).set_fill(BG, 1).set_stroke(outline_of(color), 1.5)
                           .move_to(body.get_center() + RIGHT * s * width / 2) for s in (-1, 1)])
        # the notch circles would show their outline inside the body; clip visually with a BG half
        lines = VGroup(*[Line(LEFT * width * 0.22, RIGHT * width * 0.22).set_stroke(TEXT, 1.2, opacity=0.8)
                         .shift(UP * dy * height) for dy in ((0.18, -0.18) if label is None else (0.3, -0.3))])
        lines.move_to(body.get_center())
        self.body, self.notches, self.lines = body, notches, lines
        self.label = VGroup()
        self.add(body, notches, lines)
        if label is not None:
            self.label = Text(str(label), font_size=max(10, height * 70), color=TEXT).move_to(body)
            self.lines.set_opacity(0)
            self.add(self.label)


class TicketStack(VGroup):
    """A few stubs fanned out, with a count label.

    ``TicketStack(count=75, color=PROCESS_COLORS[0], show_count=True, stubs=None, scale=1.0)``.
    ``stubs`` defaults to 2-5 depending on ``count``.  ``set_count(n)`` returns an animation
    (the label morphs); ``hop_to(point)`` returns the hop animation.  Parts: ``stack`` (the stubs),
    ``label``."""

    def __init__(self, count=10, color=PROCESS_COLORS[0], show_count=True, stubs=None, scale=1.0, **kwargs):
        super().__init__(**kwargs)
        self.count, self.color, self.show_count = count, color, show_count
        n = stubs if stubs is not None else int(np.clip(2 + count // 25, 2, 5))
        self.stubs = n
        stack = VGroup()
        for i in range(n):
            t = Ticket(color)
            t.rotate((i - (n - 1) / 2) * 0.16)
            t.shift(UP * 0.045 * i + RIGHT * (i - (n - 1) / 2) * 0.05)
            stack.add(t)
        self.stack = stack
        self.add(stack)
        self.label = self._make_label(count)
        if show_count:
            self.add(self.label)
        if scale != 1.0:
            self.scale(scale)

    def _make_label(self, n):
        lab = Text(f"{n:,}" if n >= 10000 else str(n), font_size=22, color=TEXT)
        lab.next_to(self.stack, UP, buff=0.07)
        return lab

    def set_count(self, n, run_time=0.5):
        new = self._make_label(n)
        self.count = n
        return Transform(self.label, new, run_time=run_time)

    def hop_to(self, point, **kw):
        return hop_to(self, point, anchor="center", **kw)


# ---------------------------------------------------------------------------
class RaffleDrum(VGroup):
    """A wire cage on a stand with a chute.

    ``RaffleDrum(size=1.4, color=CPU_COLOR)``: ``size`` is the cage diameter.  Parts: ``cage``
    (rotates), ``stand``, ``chute``, ``crank``.  ``spin(turns, run_time)`` is an animation;
    ``draw(number, color=None, run_time=1.2)`` returns ``(ball, animation)``: a numbered ball
    appears in the cage and rolls out of the chute (the animation adds the ball).
    ``chute_point()`` is where balls land; ``cage_center()``."""

    def __init__(self, size=1.4, color="#C8C8C8", **kwargs):
        super().__init__(**kwargs)
        self.size = size
        r = size / 2
        ring = Circle(radius=r).set_stroke(color, 3).set_fill(BG, 0.0)
        spokes = VGroup(*[Line(_P(-r, 0), _P(r, 0)).rotate(k * TAU / 6).set_stroke(color, 2) for k in range(3)])
        ring2 = Circle(radius=r * 0.55).set_stroke(color, 1.5, opacity=0.6)
        hub = Circle(radius=r * 0.1).set_fill(color, 1).set_stroke(INK, 2)
        # a few little balls rattling inside (rotate with the cage)
        cols = [PROCESS_COLORS[0], PROCESS_COLORS[1], PROCESS_COLORS[2], PROCESS_COLORS[3]]
        balls = VGroup(*[Dot(radius=size * 0.065).set_fill(cols[k % 4], 1).set_stroke(outline_of(cols[k % 4]), 1)
                         .move_to(_P(np.cos(a) * r * 0.62, np.sin(a) * r * 0.62))
                         for k, a in enumerate(np.linspace(0.4, TAU + 0.4, 5)[:-1])])
        self.cage = VGroup(ring, ring2, spokes, balls, hub)
        stand = Polygon(_P(-r * 0.55, -r * 1.35), _P(r * 0.55, -r * 1.35), _P(r * 0.12, -r * 0.1),
                        _P(-r * 0.12, -r * 0.1)).set_fill("#6B6B6B", 1).set_stroke(INK, 2)
        foot = RoundedRectangle(width=r * 1.5, height=r * 0.18, corner_radius=r * 0.06).set_fill("#6B6B6B", 1) \
            .set_stroke(INK, 2).move_to(_P(0, -r * 1.35))
        self.stand = VGroup(stand, foot)
        chute = Polygon(_P(r * 0.7, -r * 0.55), _P(r * 1.15, -r * 0.8), _P(r * 1.15, -r * 0.95), _P(r * 0.62, -r * 0.7)) \
            .set_fill("#8E8E8E", 1).set_stroke(INK, 2)
        self.chute = chute
        self.crank = VGroup(Line(_P(r, 0), _P(r * 1.25, r * 0.0)).set_stroke(color, 3),
                            Dot(_P(r * 1.25, 0), radius=size * 0.05).set_fill(CPU_COLOR, 1)).set_opacity(1)
        self.add(self.stand, self.cage, self.chute, self.crank)
        self._r = r

    def cage_center(self):
        return self.cage.get_center()

    def chute_point(self):
        c = self.chute.get_center()
        return c + RIGHT * self._r * 0.38 + DOWN * self._r * 0.12

    def spin(self, turns=1, run_time=1.5):
        return Rotate(self.cage, angle=-TAU * turns, about_point=self.cage_center(),
                      rate_func=rate_functions.linear, run_time=run_time)

    def make_ball(self, number, color=None):
        color = color or CPU_COLOR
        rad = self._r * 0.28
        ball = VGroup(Circle(radius=rad).set_fill(color, 1).set_stroke(outline_of(color), 2),
                      Text(str(number), font_size=max(14, rad * 80), color=TEXT)
                      )
        ball[1].set_color("#1C1C1C")
        ball[1].move_to(ball[0])
        ball.move_to(self.cage_center())
        return ball

    def draw(self, number, color=None, run_time=1.2):
        ball = self.make_ball(number, color)
        start = ball.copy().scale(0.3)
        ball.move_to(self.cage_center()).scale(1.0)
        end = self.chute_point()
        mid = self.chute.get_center() + UP * self._r * 0.15
        def glide(p0, p1, rt):
            return UpdateFromAlphaFunc(ball, lambda m, al: m.move_to(p0 + (p1 - p0) * al), run_time=rt,
                                       rate_func=rate_functions.smooth)

        c0 = self.cage_center()
        anim = Succession(FadeIn(ball, scale=0.3, run_time=run_time * 0.3),
                          glide(c0, mid, run_time * 0.35), glide(mid, end, run_time * 0.35))
        return ball, anim


# ---------------------------------------------------------------------------
class Seesaw(VGroup):
    """A beam on a pivot with two labelled pans.

    ``Seesaw(width=3.0, left="", right="", color=TEXT, font_size=22)``.  ``tilt(angle_deg, run_time)``
    animates the beam to an absolute angle (positive: left side down, 0 = level).  ``set_angle_now``
    jumps there.  Parts: ``beam``, ``pivot``, ``left_pan``, ``right_pan`` (each a VGroup:
    ``[plate, label]``; the pans stay upright), ``angle``."""

    def __init__(self, width=3.0, left="", right="", color=TEXT, font_size=22, **kwargs):
        super().__init__(**kwargs)
        self.w = width
        self.angle = 0.0
        pivot = Polygon(_P(-0.28, -0.5), _P(0.28, -0.5), _P(0, 0)).set_fill(DIM, 1).set_stroke(INK, 2)
        self.pivot = pivot
        self.beam = Line(_P(-width / 2, 0), _P(width / 2, 0)).set_stroke(color, 6)
        self.left_pan = self._pan(left, font_size, color)
        self.right_pan = self._pan(right, font_size, color)
        self.add(pivot, self.beam, self.left_pan, self.right_pan)
        self._place_pans()

    def _pan(self, text, fs, color):
        plate = Line(_P(-0.5, 0), _P(0.5, 0)).set_stroke(color, 4)
        lab = Text(text, font_size=fs, color=color) if text else Text(" ", font_size=fs)
        lab.next_to(plate, UP, buff=0.08)
        g = VGroup(plate, lab)
        g.plate, g.label = plate, lab
        return g

    def _end(self, side):
        return self.beam.get_start() if side < 0 else self.beam.get_end()

    def _place_pans(self):
        for side, pan in ((-1, self.left_pan), (1, self.right_pan)):
            e = self._end(side)
            pan.shift(e + UP * 0.03 - pan.plate.get_center())

    def set_angle_now(self, deg):
        d = deg - self.angle
        c = self.pivot.get_top()
        self.beam.rotate(d * DEGREES, about_point=c)
        self.angle = deg
        self._place_pans()
        return self

    def tilt(self, deg, run_time=0.9):
        a0 = self.angle

        def f(m, alpha):
            m.set_angle_now(a0 + (deg - a0) * alpha)

        return UpdateFromAlphaFunc(self, f, run_time=run_time, rate_func=rate_functions.smooth)
