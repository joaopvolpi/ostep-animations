"""Computer: a friendly retro CRT monitor with a face on its screen."""
from __future__ import annotations

import numpy as np
from manim import Arc, Circle, Ellipse, Rectangle, RoundedRectangle, Text, VGroup, WHITE

from ..style import COMPUTER_COLOR, TEXT, DIM
from .base import (
    Character, DETAIL, FONT, INK, OUTLINE, P, darker, drop, gaze_offset, lens,
    lid_shapes, lighter, mouth, poly, round_stroke, upright, zigzag,
)

GLOW = "#E6FFF0"          # phosphor face color
SCREEN = "#1F2C36"
SCREEN_SLEEP = "#141B21"
SCREEN_ERROR = "#3E1C22"
SCREEN_PANIC = "#2C2530"

LED = {
    "idle": "#6EE68A", "happy": "#6EE68A", "surprised": "#6EE68A",
    "busy": "#FFB347", "overwhelmed": "#FF7A45", "sleeping": "#3A3A3A",
    "error": "#FF4747",
}


class Computer(Character):
    """The machine: beige retro monitor on a stand; the face glows on the
    dark CRT screen, a power LED and floppy slot sit on the chin."""

    EXPRESSIONS = ("idle", "happy", "busy", "overwhelmed", "sleeping", "error", "surprised")
    DEFAULT_EXPRESSION = "idle"
    EYE_BACK = P(-0.22, 0.47)
    EYE_FRONT = P(0.30, 0.47)
    EYE_RX, EYE_RY = 0.12, 0.17
    MOUTH_C = P(0.04, 0.08)
    EYE_ANCHOR = P(0.04, 0.47)
    BUBBLE_ANCHOR = P(0.6, 1.12)
    DEFAULT_LOOK = (0.25, 0.0)

    def __init__(self, expression=None, color=None, **kwargs):
        self.casing_color = color or COMPUTER_COLOR
        super().__init__(expression, **kwargs)

    # ------------------------------------------------------------------
    def _eye(self, kind, c, side, look, blinking):
        rx, ry = self.EYE_RX, self.EYE_RY
        off = gaze_offset(look, (0, 0), 0.07)
        c = np.array(c) + off
        if blinking and kind in ("oval", "big", "focus"):
            kind = "closed"
        if kind in ("oval", "big"):
            s = 1.3 if kind == "big" else 1.0
            m = Ellipse(width=2 * rx * s, height=2 * ry * s).move_to(c)
            m.set_fill(GLOW, 1).set_stroke(GLOW, 2)
            return VGroup(m)
        if kind == "focus":   # determined: flat-topped, angled
            f, _ = lid_shapes(c, rx, ry, -0.25, -0.35 * side, upper=False)
            f.set_fill(GLOW, 1).set_stroke(GLOW, 2)
            return VGroup(f)
        if kind == "happy":   # ^
            a = Arc(radius=rx, start_angle=0.15, angle=np.pi - 0.3, arc_center=c + P(0, -0.04))
            return VGroup(round_stroke(a.set_stroke(GLOW, 8).set_fill(opacity=0)))
        if kind == "closed":  # u
            a = Arc(radius=rx, start_angle=np.pi + 0.25, angle=np.pi - 0.5, arc_center=c + P(0, 0.06))
            return VGroup(round_stroke(a.set_stroke(GLOW, 7).set_fill(opacity=0)))
        if kind == "x":
            d = 0.1
            g = VGroup(poly([c + P(-d, d), c + P(d, -d)]), poly([c + P(-d, -d), c + P(d, d)]))
            for ln in g:
                round_stroke(ln.set_stroke("#FF8A8A", 8))
            return g
        if kind == "chevron":  # > on back eye, < on front eye
            d = 0.1
            pts = [c + P(d * side, d), c + P(-d * side, 0), c + P(d * side, -d)]
            return VGroup(round_stroke(poly(pts).set_stroke(GLOW, 8).set_fill(opacity=0)))
        raise ValueError(kind)

    def _build(self, expression, look, blinking):
        e = expression
        casing_col = self.casing_color
        dark_case = darker(casing_col, 0.5)
        core = VGroup()
        neck = Rectangle(width=0.5, height=0.22).move_to(P(0, -0.76))
        neck.set_fill(darker(casing_col, 0.15), 1).set_stroke(dark_case, OUTLINE)
        base = RoundedRectangle(width=1.4, height=0.2, corner_radius=0.08).move_to(P(0, -0.9))
        base.set_fill(casing_col, 1).set_stroke(dark_case, OUTLINE)
        casing = RoundedRectangle(width=2.1, height=1.76, corner_radius=0.2).move_to(P(0, 0.2))
        casing.set_fill(casing_col, 1).set_stroke(dark_case, OUTLINE)
        bezel = RoundedRectangle(width=1.8, height=1.32, corner_radius=0.16).move_to(P(0, 0.34))
        bezel.set_fill(darker(casing_col, 0.12), 1).set_stroke(darker(casing_col, 0.3), DETAIL)
        scr_col = {"sleeping": SCREEN_SLEEP, "error": SCREEN_ERROR,
                   "overwhelmed": SCREEN_PANIC}.get(e, SCREEN)
        screen = RoundedRectangle(width=1.62, height=1.14, corner_radius=0.14).move_to(P(0, 0.34))
        screen.set_fill(scr_col, 1).set_stroke(INK, OUTLINE)
        glare = lens(P(-0.72, 0.78), P(-0.38, 0.86), 0.0, 0.0).set_fill(opacity=0)
        glare.set_stroke(WHITE, 5, opacity=0.18)
        round_stroke(glare)
        slot = RoundedRectangle(width=0.62, height=0.07, corner_radius=0.03).move_to(P(0.42, -0.47))
        slot.set_fill(INK, 1).set_stroke(dark_case, DETAIL)
        led = Circle(radius=0.055).move_to(P(-0.72, -0.47)).set_fill(LED[e], 1)
        led.set_stroke(darker(LED[e], 0.5), DETAIL)
        vents = VGroup(*[poly([P(x, -0.42), P(x, -0.52)]) for x in (-0.48, -0.40, -0.32)])
        vents.set_stroke(darker(casing_col, 0.35), DETAIL)
        round_stroke(vents)
        core.add(neck, base, casing, bezel, screen, glare, slot, led, vents)

        eye_kind = {"idle": "oval", "happy": "happy", "busy": "focus",
                    "overwhelmed": "chevron", "sleeping": "closed", "error": "x",
                    "surprised": "big"}[e]
        lk = look if e not in ("sleeping", "error", "overwhelmed", "happy") else np.zeros(2)
        eyes = VGroup(self._eye(eye_kind, self.EYE_BACK, -1, lk, blinking),
                      self._eye(eye_kind, self.EYE_FRONT, 1, lk, blinking))
        core.add(eyes)

        M = self.MOUTH_C
        if e == "idle":
            mo = mouth(M, w=0.15, top=0.06, bot=0.06, fill=GLOW, stroke=GLOW, width=6)
        elif e == "happy":
            mo = mouth(M, w=0.19, cy=0.02, top=0.03, bot=0.24, fill=GLOW, stroke=GLOW, width=5)
        elif e == "busy":
            mo = mouth(M, w=0.1, top=0.0, bot=0.0, tilt=-0.03, fill=GLOW, stroke=GLOW, width=6)
        elif e == "overwhelmed":
            mo = zigzag(M, w=0.2, amp=0.04, n=7, color=GLOW, width=5)
        elif e == "sleeping":
            mo = mouth(M, w=0.05, top=-0.04, bot=0.05, fill=scr_col, stroke=GLOW, width=5)
        elif e == "error":
            mo = zigzag(M, w=0.18, amp=0.045, n=5, color="#FF8A8A", width=6)
        else:  # surprised
            mo = mouth(M + P(0, -0.02), w=0.075, top=-0.1, bot=0.14, fill=scr_col, stroke=GLOW, width=6)
        core.add(mo)

        extras = VGroup()
        if e == "busy":
            sp = Arc(radius=0.08, start_angle=np.pi / 2, angle=-1.5 * np.pi, arc_center=P(0.66, 0.8))
            sp.set_stroke(GLOW, 6).set_fill(opacity=0)
            dots = VGroup(*[Circle(radius=0.025).move_to(P(0.48 + 0.08 * i - 0.0, 0.78))
                            for i in range(0)])
            extras.add(round_stroke(sp), dots, drop(P(1.1, 0.9), 0.1))
        elif e == "overwhelmed":
            extras.add(drop(P(1.12, 0.88), 0.1), drop(P(-1.12, 0.75), 0.09), drop(P(1.2, 0.45), 0.075))
            puffs = VGroup()
            for (x, y, r) in ((-0.55, 1.28, 0.16), (-0.38, 1.40, 0.13), (-0.70, 1.42, 0.11),
                              (0.45, 1.30, 0.15), (0.62, 1.44, 0.12)):
                puffs.add(Circle(radius=r).move_to(P(x, y)))
            puffs.set_fill("#B5B5B5", 0.85).set_stroke("#7A7A7A", DETAIL)
            extras.add(puffs)
        elif e == "sleeping":
            for (x, y, h) in ((0.95, 1.15, 0.2), (1.18, 1.38, 0.28), (1.48, 1.68, 0.36)):
                extras.add(upright(Text("z", font=FONT, weight="BOLD", color=TEXT).set_height(h).move_to(P(x, y))))
        elif e == "error":
            tri = poly([P(1.0, 1.42), P(1.22, 1.05), P(0.78, 1.05)], closed=True)
            tri.set_fill("#FF4747", 1).set_stroke(darker("#FF4747", 0.5), DETAIL)
            mark = upright(Text("!", font=FONT, weight="BOLD", color=WHITE).set_height(0.22).move_to(P(1.0, 1.17)))
            extras.add(tri, mark)
        elif e == "surprised":
            extras.add(upright(Text("!", font=FONT, weight="BOLD", color=TEXT).set_height(0.42).move_to(P(1.0, 1.35))))
        elif e == "happy":
            from .humanoid import _sparkle
            extras.add(_sparkle(P(1.12, 1.0), 0.12), _sparkle(P(-1.05, 1.1), 0.09))
        return core, extras
