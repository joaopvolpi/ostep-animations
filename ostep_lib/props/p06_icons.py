"""Icons and small devices for episode 06: the timer (AlarmClock), the interrupt shield
(ShieldGate) and the baby-proofing / permission icons."""
from __future__ import annotations

import numpy as np
from manim import (
    Animation, AnimationGroup, Arc, Circle, Dot, Ellipse, Line, Polygon, Rectangle, RoundedRectangle,
    Rotate, Succession, Text, UpdateFromAlphaFunc, VGroup, Wait, Wiggle, linear, smooth,
    LEFT, RIGHT, UP, DOWN, ORIGIN, PI, TAU, BOLD, UR,
)

from ..characters.base import mix
from ..style import TEXT, DIM, BG, FONT, MONO_FONT, KERNEL_COLOR, CPU_COLOR, USER_COLOR
from .core import CARD_FILL, INK, outline_of
from .ov_icons import padlock_icon, OK_GREEN, BAD_RED

__all__ = ["AlarmClock", "ShieldGate", "cabinet_lock", "socket_cover", "fence_glyph", "magnifier_icon",
           "door_in_line", "booth_gate", "bench_ring"]

HW_GREY = "#7C8894"


def _P(x, y=0.0):
    return np.array([float(x), float(y), 0.0])


class AlarmClock(VGroup):
    """The timer device: a hardware-grey box with an alarm clock (two bells, two hands) and
    a status LED, labeled "timer (hardware)".

    ``AlarmClock(radius=0.4, boxed=True, label="timer (hardware)")``.
    Parts: ``box``, ``face``, ``bells``, ``hand_m``, ``hand_h``, ``waves``, ``led``, ``caption``.
    ``ring(run_time=0.9)`` (two curved waves each side + a shake), ``spin(turns=1, run_time=1)``
    (minute hand), ``start()`` / ``stop()`` (LED green / grey).
    """

    def __init__(self, radius=0.4, boxed=True, label="timer (hardware)", **kwargs):
        super().__init__(**kwargs)
        r = radius
        self.r = r
        col = TEXT
        self.face = Circle(radius=r).set_fill(CARD_FILL, 1).set_stroke(col, 4)
        bells = VGroup(*[Arc(radius=r * 0.42, start_angle=0, angle=PI).set_fill(HW_GREY, 1).set_stroke(col, 3)
                         .move_to(_P(sx * r * 0.7, r * 0.82)).rotate(-sx * 0.5) for sx in (-1, 1)])
        self.bells = bells
        self.hand_m = Line(ORIGIN, UP * r * 0.68).set_stroke(CPU_COLOR, 4)
        self.hand_h = Line(ORIGIN, RIGHT * r * 0.42).set_stroke(col, 4)
        self.dot = Dot(radius=r * 0.07).set_fill(col, 1)
        feet = VGroup(*[Line(_P(sx * r * 0.55, -r * 0.8), _P(sx * r * 0.8, -r * 1.12)).set_stroke(col, 4) for sx in (-1, 1)])
        self.body = VGroup(bells, feet, self.face, self.hand_m, self.hand_h, self.dot)
        self.waves = VGroup()
        for sx in (-1, 1):
            for k, rad in enumerate((r * 1.25, r * 1.6)):
                a = Arc(radius=rad, start_angle=-0.4 if sx > 0 else PI - 0.4, angle=0.8).set_stroke(CPU_COLOR, 3, opacity=0)
                self.waves.add(a)
        self.box = RoundedRectangle(width=r * 4.1, height=r * 3.3, corner_radius=0.12) if boxed else VGroup()
        if boxed:
            self.box.set_fill(mix(HW_GREY, BG, 0.75), 1).set_stroke(HW_GREY, 3)
            self.box.move_to(self.face.get_center() + _P(0, 0.0))
        self.led = Dot(radius=0.07).set_fill(DIM, 1)
        self.is_running = False
        if boxed:
            self.led.move_to(self.box.get_corner(UR) + _P(-0.18, -0.18))
            self.caption = Text(label, font=FONT, font_size=18, color=HW_GREY).next_to(self.box, DOWN, buff=0.08)
        else:
            self.led.move_to(self.face.get_center() + _P(r * 1.0, r * 1.0))
            self.caption = VGroup()
        self.add(self.box, self.waves, self.body, self.led, self.caption)

    def ring(self, run_time=0.9):
        c = self.face.get_center()
        w0 = self.waves.copy()
        mob = self.waves

        def upd(m, alpha):
            m.become(w0)
            for i, sm in enumerate(m):
                tier = i % 2
                t = float(np.clip(alpha * 1.5 - 0.3 * tier, 0, 1))
                sm.scale(1 + 0.25 * t, about_point=c)
                sm.set_stroke(opacity=float(np.sin(PI * t)) * 0.9)
        return AnimationGroup(UpdateFromAlphaFunc(mob, upd, run_time=run_time, rate_func=linear),
                              Wiggle(self.body, scale_value=1.05, rotation_angle=0.12, n_wiggles=6, run_time=run_time),
                              run_time=run_time)

    def spin(self, turns=1.0, run_time=1.0):
        return Rotate(self.hand_m, -TAU * turns, about_point=self.face.get_center(), rate_func=linear, run_time=run_time)

    def start(self, run_time=0.4):
        self.is_running = True
        return self.led.animate(run_time=run_time).set_fill(OK_GREEN, 1)

    def stop(self, run_time=0.4):
        self.is_running = False
        return self.led.animate(run_time=run_time).set_fill(DIM, 1)


class ShieldGate(VGroup):
    """A short vertical gate with a shield emblem that drops in front of an arrow or bolt
    ("disable interrupts").

    ``ShieldGate(height=1.2, color=KERNEL_COLOR)``.  Built **closed**.  ``close()`` / ``open()``
    return animations (the gate slides down / up by ``height``); ``open_offset`` = the shift.
    """

    def __init__(self, height=1.2, color=KERNEL_COLOR, **kwargs):
        super().__init__(**kwargs)
        self.height_ = height
        bar = RoundedRectangle(width=0.2, height=height, corner_radius=0.06).set_fill(color, 1).set_stroke(outline_of(color), 3)
        sh = Polygon(_P(-0.3, 0.3), _P(0.3, 0.3), _P(0.3, -0.05), _P(0, -0.38), _P(-0.3, -0.05))
        sh.set_fill(mix(color, BG, 0.2), 1).set_stroke(TEXT, 2.5).scale(1.0)
        sh.next_to(bar, UP, buff=-0.04)
        mark = Line(_P(-0.1, 0.0), _P(0.1, 0.0)).set_stroke(TEXT, 3).move_to(sh.get_center() + _P(0, 0.0))
        self.bar, self.shield = bar, VGroup(sh, mark)
        self.open_offset = UP * (height * 1.3)
        self.add(bar, self.shield)

    def close(self, run_time=0.4):
        return self.animate(run_time=run_time, rate_func=smooth).shift(-self.open_offset)

    def open(self, run_time=0.4):
        return self.animate(run_time=run_time, rate_func=smooth).shift(self.open_offset)


# ---------------------------------------------------------------------------
# Icons
# ---------------------------------------------------------------------------
def cabinet_lock(size=1.0):
    """A cabinet with two doors and a padlock on the handles."""
    s = size
    body = Rectangle(width=0.75 * s, height=1.0 * s).set_fill("#6B5B4A", 1).set_stroke("#3E3329", 3)
    mid = Line(body.get_top(), body.get_bottom()).set_stroke("#3E3329", 3)
    hs = VGroup(*[Dot(radius=0.04 * s).set_fill(TEXT, 1).move_to(_P(sx * 0.09 * s, 0.0)) for sx in (-1, 1)])
    lock = padlock_icon(0.38 * s, KERNEL_COLOR).move_to(_P(0, -0.02 * s))
    return VGroup(body, mid, hs, lock)


def socket_cover(size=1.0):
    """A wall socket with a safety cover over the two slots."""
    s = size
    plate = RoundedRectangle(width=0.7 * s, height=0.7 * s, corner_radius=0.08 * s).set_fill("#D9D2C0", 1).set_stroke("#8A8472", 3)
    slots = VGroup(*[Rectangle(width=0.06 * s, height=0.2 * s).set_fill(INK, 1).set_stroke(width=0).move_to(_P(sx * 0.1 * s, 0.05 * s)) for sx in (-1, 1)])
    ground = Circle(radius=0.045 * s).set_fill(INK, 1).set_stroke(width=0).move_to(_P(0, -0.15 * s))
    cover = RoundedRectangle(width=0.5 * s, height=0.4 * s, corner_radius=0.06 * s).set_fill(KERNEL_COLOR, 0.85).set_stroke(outline_of(KERNEL_COLOR), 3)
    cover.move_to(_P(0, 0.0))
    return VGroup(plate, slots, ground, cover)


def fence_glyph(width=0.9, color="#B0886A"):
    """A short picket fence (the guard rails of "limited")."""
    n = 5
    w = width / (n * 1.6)
    pickets = VGroup(*[Polygon(_P(-w / 2, -0.3), _P(w / 2, -0.3), _P(w / 2, 0.22), _P(0, 0.34), _P(-w / 2, 0.22))
                       .set_fill(color, 1).set_stroke(outline_of(color), 2) for _ in range(n)])
    pickets.arrange(RIGHT, buff=w * 0.6)
    rails = VGroup(*[Line(pickets.get_left() + _P(-0.05, y), pickets.get_right() + _P(0.05, y)).set_stroke(outline_of(color), 4)
                     for y in (-0.12, 0.1)])
    return VGroup(rails, pickets)


def magnifier_icon(size=0.8, color=TEXT):
    lens = Circle(radius=0.28 * size).set_fill("#7FB8E8", 0.25).set_stroke(color, 4)
    handle = Line(lens.get_center() + _P(0.2, -0.2) * size, lens.get_center() + _P(0.5, -0.5) * size).set_stroke(color, 6)
    return VGroup(lens, handle)


def door_in_line(width=0.55, height=0.75):
    """The little doorway in the User/Kernel boundary (a system-call door)."""
    frame = Rectangle(width=width, height=height).set_fill(BG, 1).set_stroke(CPU_COLOR, 3)
    door = Rectangle(width=width * 0.78, height=height * 0.9).set_fill(mix(CPU_COLOR, BG, 0.75), 1).set_stroke(width=0)
    door.move_to(frame.get_center())
    knob = Dot(radius=0.045).set_fill(CPU_COLOR, 1).move_to(door.get_right() + _P(-0.1, 0))
    return VGroup(frame, door, knob)


def booth_gate(size=1.0):
    """The file-system permission checkpoint: a small booth with a barrier arm.
    ``.bar`` is the arm (rotate it to open)."""
    s = size
    booth = RoundedRectangle(width=0.6 * s, height=0.8 * s, corner_radius=0.06 * s).set_fill(CARD_FILL, 1).set_stroke(TEXT, 3)
    win = Rectangle(width=0.36 * s, height=0.26 * s).set_fill("#2F4A5F", 1).set_stroke(TEXT, 2).move_to(booth.get_center() + _P(0, 0.12 * s))
    roof = Rectangle(width=0.74 * s, height=0.08 * s).set_fill(KERNEL_COLOR, 1).set_stroke(width=0).next_to(booth, UP, buff=0)
    bar = Rectangle(width=0.9 * s, height=0.07 * s).set_fill(BAD_RED, 1).set_stroke(TEXT, 1.5)
    bar.next_to(booth, RIGHT, buff=0).shift(RIGHT * 0.45 * s + DOWN * 0.15 * s)
    bar.move_to(booth.get_right() + _P(0.45 * s, -0.15 * s))
    pivot = Dot(radius=0.05 * s).set_fill(TEXT, 1).move_to(bar.get_left())
    g = VGroup(booth, win, roof, bar, pivot)
    g.bar = bar
    return g


def bench_ring(color, width=1.1):
    """The outline ring under a process that waits on a "bench" (frozen, ready)."""
    e = Ellipse(width=width, height=width * 0.26).set_fill(color, 0.14).set_stroke(color, 3)
    return e
