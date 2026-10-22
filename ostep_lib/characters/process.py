"""Process: small blob creatures representing running programs."""
from __future__ import annotations

import itertools

import numpy as np
from manim import Circle, Ellipse, RoundedRectangle, Text, VGroup, WHITE
from manim.mobject.geometry.boolean_ops import Union

from ..style import BG, PROCESS_COLORS, TEXT
from .base import (
    Character, DETAIL, FONT, INK, OUTLINE, P, darker, gaze_offset, lighter, make_eye,
    mix, mouth, poly, round_stroke, upright,
)

_BODY = None
_color_cycle = itertools.count()
ZOMBIE = "#8C978A"


def _body():
    global _BODY
    if _BODY is None:
        _BODY = Union(
            Circle(radius=1.0).shift(P(0, 0.1)),
            RoundedRectangle(width=2.0, height=1.0, corner_radius=0.36).shift(P(0, -0.4)),
        )
    return _BODY.copy()


SPECS = {
    #          upper lid      lower lid     pupil gaze        mouth
    "ready":   dict(upper=(1, 0), lower=(1, 0), pupil=1.15, gaze=(0.5, 0.3),
                    mouth=dict(w=0.2, cy=0.02, top=0.04, bot=0.26), deform="tall"),
    "running": dict(upper=(0.45, 0.35), lower=(0.85, 0), pupil=1.0, gaze=(0.9, 0.0),
                    mouth=dict(w=0.22, cy=0.03, top=0.02, bot=0.3), deform="lean"),
    "blocked": dict(upper=(0.0, 0.0), lower=(0.0, 0.0), pupil=1.0, gaze=(0, 0),
                    mouth=dict(w=0.12, top=-0.0, bot=0.0, tilt=0.0), deform=None),
    "done":    dict(upper=(1, 0), lower=(0.15, 0), lower_bow=0.3, pupil=1.0, gaze=(0, 0.3),
                    mouth=dict(w=0.2, cy=0.02, top=0.06, bot=0.26), deform=None),
    "zombie":  dict(upper=(0.1, -0.2), upper_back=(-0.25, 0.1), lower=(1, 0), pupil=0.55,
                    gazes=((-0.7, -0.2), (0.6, 0.5)),
                    mouth=dict(w=0.15, cy=-0.04, top=-0.06, bot=0.10, tilt=-0.05),
                    deform="droop"),
}


class Process(Character):
    """A running program as a small blob creature.

    ``Process(expression="ready", color=None, label=None)``. ``color``
    defaults to the next color of PROCESS_COLORS; ``label`` (e.g. "PID 1",
    "A") is shown under the blob.
    """

    EXPRESSIONS = ("ready", "running", "blocked", "done", "zombie")
    DEFAULT_EXPRESSION = "ready"
    DEFAULT_SCALE = 0.5
    EYE_BACK = P(-0.06, 0.34)
    EYE_FRONT = P(0.58, 0.34)
    EYE_RX, EYE_RY = 0.28, 0.34
    PUPIL_R = 0.14
    MOUTH_C = P(0.28, -0.26)
    EYE_ANCHOR = P(0.26, 0.34)
    BUBBLE_ANCHOR = P(0.55, 1.15)

    def __init__(self, expression=None, color=None, label=None, **kwargs):
        if color is None:
            color = PROCESS_COLORS[next(_color_cycle) % len(PROCESS_COLORS)]
        self.base_color = color
        self.label_text = label
        self._label_mob = None
        super().__init__(expression, **kwargs)

    @property
    def label(self):
        return self.label_text

    def _label(self):
        if self.label_text is None:
            return VGroup()
        if self._label_mob is None:
            t = Text(str(self.label_text), font=FONT, color=TEXT, weight="BOLD").set_height(0.3)
            if t.width > 2.2:
                t.scale_to_fit_width(2.2)
            self._label_mob = t.move_to(P(0, -1.42))
        return upright(self._label_mob.copy())

    def _build(self, expression, look, blinking):
        sp = SPECS[expression]
        col = ZOMBIE if expression == "zombie" else self.base_color
        out = darker(col, 0.55)
        core = VGroup()
        feet = VGroup(*[Ellipse(width=0.56, height=0.3).move_to(P(x, -0.9)) for x in (-0.45, 0.45)])
        feet.set_fill(darker(col, 0.25), 1).set_stroke(out, OUTLINE)
        body = _body().set_fill(col, 1).set_stroke(out, OUTLINE)
        shine = Ellipse(width=0.32, height=0.18).rotate(0.6).move_to(P(-0.6, 0.72))
        shine.set_fill(WHITE, 0.35).set_stroke(width=0)
        core.add(feet, body, shine)

        eyes = VGroup()
        rx, ry = self.EYE_RX, self.EYE_RY
        pr = self.PUPIL_R * sp["pupil"]
        maxoff = min(rx, ry) - pr - 0.03
        for i, (c, side) in enumerate(((self.EYE_BACK, -1), (self.EYE_FRONT, 1))):
            upper = sp.get("upper_back") if (side < 0 and sp.get("upper_back")) else sp["upper"]
            lower = sp["lower"]
            if blinking:
                upper, lower = (0.0, 0.0), (0.0, 0.0)
            if "gazes" in sp:
                off = gaze_offset((0, 0), sp["gazes"][i], maxoff)
            else:
                off = gaze_offset(look, sp["gaze"], maxoff)
            eyes.add(make_eye(c, rx, ry, pr, off, upper, lower, side, lid_color=col,
                              lower_bow=0 if blinking else sp.get("lower_bow", 0)))
        core.add(eyes)
        core.add(mouth(self.MOUTH_C, **sp["mouth"]))
        # cheeks
        cheeks = VGroup(*[Ellipse(width=0.2, height=0.11).move_to(P(x, -0.12)) for x in (-0.22, 0.86)])
        cheeks.set_fill(mix(col, "#FF6F91", 0.45), 0.6).set_stroke(width=0)
        core.add(cheeks)

        d = sp["deform"]
        if d:
            for sm in core.get_family():
                if len(sm.points):
                    x, y = sm.points[:, 0].copy(), sm.points[:, 1].copy()
                    yb = y + 1.05
                    if d == "tall":
                        sm.points[:, 0] = x * 0.95
                        sm.points[:, 1] = -1.05 + yb * 1.05
                    elif d == "lean":
                        sm.points[:, 0] = x + 0.13 * yb
                    elif d == "droop":
                        sm.points[:, 0] = x * (1.12 - 0.08 * yb / 2.2)
                        sm.points[:, 1] = -1.05 + yb * 0.84
        core.add(self._label())

        if expression == "done":
            # fade toward the background
            for sm in core.get_family():
                if getattr(sm, "upright", False):
                    continue
                if hasattr(sm, "fill_rgbas") and len(sm.points):
                    sm.set_fill(mix(sm.get_fill_color(), BG, 0.45), family=False)
                    sm.set_stroke(mix(sm.get_stroke_color(), BG, 0.45), family=False)

        extras = VGroup()
        if expression == "running":
            glow = VGroup()
            for k, (sc, w, op) in enumerate(((1.1, 8, 0.75), (1.2, 6, 0.35))):
                g = _body().scale(sc, about_point=P(0, -0.1)).shift(P(0.12, 0.0))
                g.set_fill(opacity=0).set_stroke(lighter(col, 0.5), w, opacity=op)
                glow.add(g)
            lines = VGroup(*[round_stroke(poly([P(-1.5, y), P(-1.2, y)]).set_stroke(lighter(col, 0.3), 6))
                             for y in (0.35, 0.0, -0.35)])
            extras.add(glow, lines)
        elif expression == "blocked":
            c = P(0.95, 1.3)
            face = Circle(radius=0.3).move_to(c).set_fill("#2A2A2A", 1).set_stroke(TEXT, OUTLINE)
            hands = VGroup(poly([c, c + P(0, 0.2)]), poly([c, c + P(0.14, 0)]))
            hands.set_stroke(TEXT, OUTLINE)
            round_stroke(hands)
            ticks = VGroup(*[poly([c + P(0.24 * np.cos(a), 0.24 * np.sin(a)),
                                   c + P(0.29 * np.cos(a), 0.29 * np.sin(a))])
                             for a in np.arange(0, 2 * np.pi, np.pi / 2)]).set_stroke(TEXT, DETAIL)
            extras.add(face, ticks, hands)
        elif expression == "done":
            chk = poly([P(0.62, 1.32), P(0.82, 1.1), P(1.2, 1.55)])
            chk.set_fill(opacity=0).set_stroke("#8BE07A", 10)
            extras.add(round_stroke(chk))
        elif expression == "zombie":
            scar = VGroup(poly([P(-0.55, 0.62), P(-0.12, 0.82)]))
            for t in (0.2, 0.5, 0.8):
                p = P(-0.55, 0.62) + (P(-0.12, 0.82) - P(-0.55, 0.62)) * t
                scar.add(poly([p + P(0.04, -0.09), p + P(-0.04, 0.09)]))
            scar.set_stroke(darker(ZOMBIE, 0.6), DETAIL + 1)
            # apply same droop
            for sm in scar.get_family():
                if len(sm.points):
                    x, y = sm.points[:, 0].copy(), sm.points[:, 1].copy()
                    yb = y + 1.05
                    sm.points[:, 0] = x * (1.12 - 0.08 * yb / 2.2)
                    sm.points[:, 1] = -1.05 + yb * 0.84
            extras.add(scar)
        return core, extras
