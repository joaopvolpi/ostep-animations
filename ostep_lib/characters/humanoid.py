"""Professor and Student: bean-shaped "pi creature"-like humans."""
from __future__ import annotations

import numpy as np
from manim import (
    Circle, Ellipse, Rectangle, RoundedRectangle, Text, VGroup, WHITE,
)
from manim.mobject.geometry.boolean_ops import Intersection, Union

from ..style import PROFESSOR_COLOR, STUDENT_COLOR, TEXT
from .base import (
    Character, DETAIL, FONT, INK, MOUTH_DARK, OUTLINE, P, brow, darker, drop,
    gaze_offset, lens, lighter, make_eye, mouth, poly, round_stroke,
    smooth_path, upright,
)

_CACHE = {}


def _cached(key, fn):
    if key not in _CACHE:
        _CACHE[key] = fn()
    return _CACHE[key].copy()


def _bean():
    return Union(
        Circle(radius=0.85).shift(P(0, 0.15)),
        RoundedRectangle(width=1.7, height=1.15, corner_radius=0.3).shift(P(0, -0.43)),
    )


# Arm poses: front = (elbow, hand, finger), back = (elbow, hand)
# finger = (angle_degrees, length) or None
ARMS = {
    "neutral": dict(front=((0.88, -0.60), (0.92, -0.86), None),
                    back=((-0.80, -0.62), (-0.88, -0.86))),
    "point": dict(front=((0.98, -0.36), (1.22, -0.02), (55, 0.2)),
                  back=((-0.80, -0.62), (-0.88, -0.86))),
    "open": dict(front=((0.98, -0.52), (1.18, -0.24), None),
                 back=((-0.98, -0.52), (-1.18, -0.24))),
    "chin": dict(front=((0.98, -0.80), (0.50, -0.38), (100, 0.13)),
                 back=((-0.80, -0.62), (-0.88, -0.86))),
    "up": dict(front=((1.00, -0.18), (1.08, 0.22), None),
               back=((-1.00, -0.18), (-1.08, 0.22))),
    "clasp": dict(front=((0.84, -0.66), (0.62, -0.90), None),
                  back=((-0.80, -0.62), (-0.88, -0.86))),
    "hips": dict(front=((1.10, -0.50), (0.86, -0.78), None),
                 back=((-1.10, -0.50), (-0.86, -0.78))),
    "raise": dict(front=((0.86, 0.02), (0.92, 0.46), (88, 0.17)),
                  back=((-0.80, -0.62), (-0.88, -0.86))),
    "shrug": dict(front=((1.02, -0.62), (1.22, -0.40), None),
                  back=((-1.02, -0.62), (-1.22, -0.40))),
    "cheer": dict(front=((0.95, -0.06), (1.15, 0.40), None),
                  back=((-0.95, -0.06), (-1.15, 0.40))),
    "limp": dict(front=((0.70, -0.70), (0.72, -0.95), None),
                 back=((-0.70, -0.70), (-0.72, -0.95))),
    "fists": dict(front=((0.98, -0.52), (0.94, -0.86), None),
                  back=((-0.98, -0.52), (-0.94, -0.86))),
    "cheek": dict(front=((0.98, -0.88), (0.76, -0.38), None),
                  back=((-0.80, -0.62), (-0.88, -0.86))),
}

SHOULDER_FRONT = P(0.64, -0.36)
SHOULDER_BACK = P(-0.64, -0.36)


def spec(**kw):
    d = dict(upper=(1, 0), lower=(1, 0), lower_bow=0.0, upper_back=None, lower_back=None,
             pupil=1.0, gaze=(0, 0), eye_scale=1.0,
             brow=(0.0, 0.0, 0.03), brow_back=None,
             mouth=dict(w=0.14, top=0.05, bot=0.05),
             arms="neutral", extras=None)
    d.update(kw)
    return d


class _Humanoid(Character):
    BODY_COLOR = "#888888"
    ARM_COLOR = None
    BROW_COLOR = INK
    BROW_WIDTH = 7
    BROW_MAX = 1.0
    SCLERA_STROKE = OUTLINE
    EYE_BACK = P(0.12, 0.38)
    EYE_FRONT = P(0.56, 0.38)
    EYE_RX, EYE_RY = 0.17, 0.21
    PUPIL_R = 0.085
    MOUTH_C = P(0.36, -0.07)
    EYE_ANCHOR = P(0.34, 0.38)
    BUBBLE_ANCHOR = P(0.55, 1.02)
    SPECS: dict = {}

    def __init__(self, expression=None, color=None, **kwargs):
        if color is not None:
            self.BODY_COLOR = color
        super().__init__(expression, **kwargs)

    # hooks for features
    def _behind_body(self, sp):
        return VGroup()

    def _on_body(self, sp):
        return VGroup()

    def _on_face(self, sp):
        return VGroup()

    def _extras(self, name):
        return VGroup()

    # ------------------------------------------------------------------
    def _arm(self, S, E, H, finger=None):
        col = self.ARM_COLOR or darker(self.BODY_COLOR, 0.12)
        S, E, H = np.array(S), P(*E), P(*H)
        path = smooth_path([S, E, H])
        outer = round_stroke(path.copy().set_fill(opacity=0).set_stroke(INK, 15))
        inner = round_stroke(path.copy().set_fill(opacity=0).set_stroke(col, 9))
        if finger is None:
            f_end = H
        else:
            a = np.radians(finger[0])
            f_end = H + P(np.cos(a), np.sin(a)) * finger[1]
        fpath = poly([H, (H + f_end) / 2, f_end])
        f_out = round_stroke(fpath.copy().set_fill(opacity=0).set_stroke(INK, 10))
        f_in = round_stroke(fpath.copy().set_fill(opacity=0).set_stroke(self.BODY_COLOR, 5))
        hand = Circle(radius=0.1).move_to(H).set_fill(self.BODY_COLOR, 1).set_stroke(INK, DETAIL)
        return VGroup(outer, inner, f_out, hand, f_in)

    def _build(self, expression, look, blinking):
        sp = self.SPECS[expression]
        arms = ARMS[sp["arms"]]
        body_col = self.BODY_COLOR
        core = VGroup()
        # back arm (behind everything)
        E, H = arms["back"]
        core.add(self._arm(SHOULDER_BACK, E, H))
        core.add(self._behind_body(sp))
        body = _cached("bean", _bean)
        body.set_fill(body_col, 1).set_stroke(darker(body_col, 0.55), OUTLINE)
        core.add(body)
        core.add(self._on_body(sp))

        # eyes
        es = sp["eye_scale"]
        rx, ry = self.EYE_RX * es, self.EYE_RY * es
        pr = self.PUPIL_R * sp["pupil"]
        maxoff = min(rx, ry) - pr - 0.02
        eyes = VGroup()
        for c, side in ((self.EYE_BACK, -1), (self.EYE_FRONT, 1)):
            upper = sp["upper_back"] if (side < 0 and sp["upper_back"]) else sp["upper"]
            lower = sp["lower_back"] if (side < 0 and sp["lower_back"]) else sp["lower"]
            if blinking:
                upper, lower = (0.0, 0.0), (0.0, 0.0)
            off = gaze_offset(look, sp["gaze"], maxoff)
            eyes.add(make_eye(c, rx, ry, pr, off, upper, lower, side, lid_color=body_col,
                              sclera_stroke=self.SCLERA_STROKE,
                              lower_bow=0 if blinking else sp["lower_bow"]))
        core.add(eyes)

        # brows
        brows = VGroup()
        for c, side in ((self.EYE_BACK, -1), (self.EYE_FRONT, 1)):
            b = sp["brow_back"] if (side < 0 and sp["brow_back"]) else sp["brow"]
            brows.add(brow(c, rx, ry, min(b[0], self.BROW_MAX), b[1], side, b[2], color=self.BROW_COLOR,
                           width=self.BROW_WIDTH))
        core.add(brows)

        m = dict(sp["mouth"])
        core.add(self._mouth_backdrop(sp))
        core.add(mouth(self.MOUTH_C, **m))
        core.add(self._on_face(sp))

        # front arm (on top)
        E, H, F = arms["front"]
        core.add(self._arm(SHOULDER_FRONT, E, H, F))

        extras = self._extras(sp["extras"]) if sp["extras"] else VGroup()
        return core, extras

    def _mouth_backdrop(self, sp):
        return VGroup()

    # shared extras -------------------------------------------------------
    @staticmethod
    def _mark(char, pos, height=0.42, color=TEXT):
        t = Text(char, font=FONT, weight="BOLD", color=color).set_height(height).move_to(P(*pos))
        return upright(t)


# ===========================================================================
class Professor(_Humanoid):
    """The guide: lavender bean with round glasses, grey hair fringe,
    grey beard and a navy bow tie."""

    EXPRESSIONS = ("neutral", "explaining", "happy", "thinking", "surprised",
                   "worried", "proud")
    DEFAULT_EXPRESSION = "neutral"
    BODY_COLOR = PROFESSOR_COLOR
    BROW_COLOR = "#E4E4E4"
    BROW_WIDTH = 9
    SCLERA_STROKE = 0
    HAIR = "#D9D9D9"

    SPECS = {
        "neutral": spec(upper=(0.6, 0), brow=(0.0, 0.0, 0.02),
                        mouth=dict(w=0.13, top=0.05, bot=0.05)),
        "explaining": spec(upper=(0.75, 0), gaze=(0.3, 0.3), brow=(0.05, -0.05, 0.04),
                           brow_back=(0.02, 0.05, 0.03),
                           mouth=dict(w=0.13, top=0.02, bot=0.17), arms="point"),
        "happy": spec(lower=(0.2, 0.0), lower_bow=0.3, brow=(0.05, -0.05, 0.05),
                      mouth=dict(w=0.18, cy=0.01, top=0.05, bot=0.28), arms="open"),
        "thinking": spec(upper=(0.55, -0.1), gaze=(-0.35, 0.95), brow=(0.1, -0.15, 0.04),
                         brow_back=(-0.02, 0.2, 0.02),
                         mouth=dict(w=0.08, cy=-0.01, top=-0.015, bot=-0.015, tilt=0.025),
                         arms="chin"),
        "surprised": spec(eye_scale=1.15, pupil=0.62, brow=(0.14, 0.0, 0.05),
                          mouth=dict(w=0.075, cy=-0.04, top=-0.11, bot=0.15), arms="up",
                          extras="!"),
        "worried": spec(upper=(0.45, -0.4), gaze=(-0.25, -0.35), brow=(0.06, -0.42, 0.02),
                        mouth=dict(w=0.12, top=-0.045, bot=-0.045, tilt=0.03),
                        arms="clasp", extras="sweat"),
        "proud": spec(upper=(0.1, 0.0), lower=(0.6, 0.0), lower_bow=0.3, gaze=(0.25, 0.7),
                      brow=(0.05, -0.05, 0.03),
                      mouth=dict(w=0.16, top=0.09, bot=0.09, tilt=0.035),
                      arms="hips", extras="sparkle"),
    }

    def _behind_body(self, sp):
        hair = VGroup()
        for (x, y, r) in ((-0.80, 0.20, 0.17), (-0.88, 0.45, 0.18), (-0.80, 0.70, 0.16),
                          (-0.62, 0.88, 0.13), (0.84, 0.58, 0.10)):
            hair.add(Circle(radius=r).move_to(P(x, y)))
        hair.set_fill(self.HAIR, 1).set_stroke(darker(self.HAIR, 0.5), DETAIL)
        return hair

    def _mouth_backdrop(self, sp):
        m = sp["mouth"]
        beard = lens(P(0.02, 0.0), P(0.70, 0.0), -0.02, 0.40)
        beard.set_fill(self.HAIR, 1).set_stroke(darker(self.HAIR, 0.5), DETAIL)
        return VGroup(beard)

    def _on_face(self, sp):
        g = VGroup()
        # mustache over mouth
        c = self.MOUTH_C + P(0, 0.075)
        mus = VGroup(
            lens(c + P(-0.18, -0.035), c + P(0.0, 0.015), -0.05, 0.03),
            lens(c + P(0.0, 0.015), c + P(0.18, -0.035), -0.05, 0.03),
        )
        mus.set_fill(lighter(self.HAIR, 0.25), 1).set_stroke(darker(self.HAIR, 0.5), DETAIL)
        g.add(mus)
        # glasses
        es = sp["eye_scale"]
        r = max(self.EYE_RX, self.EYE_RY) * min(es, 1.08) + 0.03
        rims = VGroup(*[Circle(radius=r).move_to(c2) for c2 in (self.EYE_BACK, self.EYE_FRONT)])
        rims.set_fill(WHITE, 0.07).set_stroke("#2A2A2A", OUTLINE + 1)
        mid = (self.EYE_BACK + self.EYE_FRONT) / 2
        bridge = lens(mid + P(-0.05, 0.05), mid + P(0.05, 0.05), -0.03, -0.03)
        bridge.set_fill(opacity=0).set_stroke("#2A2A2A", OUTLINE)
        temple = poly([self.EYE_BACK + P(-r, 0.03), self.EYE_BACK + P(-r - 0.3, 0.06)])
        temple.set_stroke("#2A2A2A", OUTLINE)
        g.add(temple, rims, bridge)
        return g

    def _on_body(self, sp):
        c = P(0.24, -0.60)
        wing_l = poly([c, c + P(-0.17, 0.09), c + P(-0.17, -0.09)], closed=True)
        wing_r = poly([c, c + P(0.17, 0.09), c + P(0.17, -0.09)], closed=True)
        knot = Circle(radius=0.045).move_to(c)
        tie = VGroup(wing_l, wing_r, knot)
        tie.set_fill("#2C3A5E", 1).set_stroke(INK, DETAIL)
        return tie

    def _extras(self, name):
        if name == "!":
            return VGroup(self._mark("!", (0.95, 1.25), 0.45))
        if name == "sweat":
            return VGroup(drop(P(-0.62, 0.85), 0.09))
        if name == "sparkle":
            return VGroup(*[_sparkle(P(x, y), s) for x, y, s in
                            ((0.95, 1.05, 0.13), (1.15, 0.75, 0.08), (-0.75, 1.1, 0.09))])
        return VGroup()


def _sparkle(c, s, color="#FFE38A"):
    pts = []
    for i in range(8):
        a = np.pi / 2 + i * np.pi / 4
        r = s if i % 2 == 0 else s * 0.3
        pts.append(c + P(r * np.cos(a), r * np.sin(a)))
    m = poly(pts, closed=True)
    m.set_fill(color, 1).set_stroke(width=0)
    return m


# ===========================================================================
class Student(_Humanoid):
    """The curious learner: smaller rose bean with a slate baseball cap
    (brim forward), a hoodie with drawstrings and freckles."""

    EXPRESSIONS = ("neutral", "curious", "confused", "excited", "sad",
                   "frustrated", "surprised", "bored")
    DEFAULT_EXPRESSION = "neutral"
    DEFAULT_SCALE = 0.85
    BODY_COLOR = STUDENT_COLOR
    HOODIE = "#5A6E96"
    CAP = "#39486B"
    BROW_COLOR = "#4A2E2A"
    EYE_RX, EYE_RY = 0.18, 0.22
    PUPIL_R = 0.095
    BROW_MAX = 0.06
    EYE_BACK = P(0.12, 0.28)
    EYE_FRONT = P(0.56, 0.28)
    EYE_ANCHOR = P(0.34, 0.28)
    MOUTH_C = P(0.36, -0.16)
    BUBBLE_ANCHOR = P(0.6, 1.1)

    @property
    def ARM_COLOR(self):
        return self.HOODIE

    SPECS = {
        "neutral": spec(upper=(0.85, 0), mouth=dict(w=0.13, top=0.06, bot=0.06)),
        "curious": spec(eye_scale=1.06, pupil=1.15, gaze=(0.45, 0.55),
                        brow=(0.11, -0.12, 0.04), brow_back=(0.03, 0.0, 0.03),
                        mouth=dict(w=0.06, cy=-0.01, top=-0.06, bot=0.09), arms="raise"),
        "confused": spec(upper_back=(0.4, 0.2), gaze=(-0.25, 0.55),
                         brow=(0.11, -0.25, 0.03), brow_back=(-0.03, 0.3, 0.02),
                         mouth=dict(w=0.12, top=-0.03, bot=-0.03, tilt=0.05),
                         arms="shrug", extras="?"),
        "excited": spec(eye_scale=1.12, pupil=1.25, brow=(0.12, -0.05, 0.06),
                        mouth=dict(w=0.19, cy=0.02, top=0.03, bot=0.32),
                        arms="cheer", extras="bulb"),
        "sad": spec(upper=(0.35, -0.45), gaze=(-0.05, -0.8), brow=(0.03, -0.45, 0.02),
                    mouth=dict(w=0.12, cy=-0.04, top=-0.08, bot=-0.08),
                    arms="limp", extras="tear"),
        "frustrated": spec(upper=(0.3, 0.42), lower=(0.75, 0), brow=(-0.03, 0.5, 0.0),
                           mouth=dict(w=0.17, top=-0.04, bot=0.08, tilt=0.02, fill=WHITE),
                           arms="fists", extras="anger"),
        "surprised": spec(eye_scale=1.18, pupil=0.62, brow=(0.15, 0.0, 0.05),
                          mouth=dict(w=0.08, cy=-0.04, top=-0.12, bot=0.17), arms="up",
                          extras="!"),
        "bored": spec(upper=(0.05, 0), lower=(0.8, 0), gaze=(-0.8, -0.45),
                      brow=(-0.04, 0.0, 0.0),
                      mouth=dict(w=0.10, cy=-0.02, top=0.0, bot=0.0, tilt=-0.02),
                      arms="cheek", extras="dots"),
    }

    def _behind_body(self, sp):
        return VGroup()

    def _on_body(self, sp):
        g = VGroup()
        hood = _cached("hoodie", lambda: Intersection(
            _bean(), Rectangle(width=3, height=1.0).move_to(P(0, -0.47 - 0.5))))
        hood.set_fill(self.HOODIE, 1).set_stroke(darker(self.HOODIE, 0.5), OUTLINE)
        collar = lens(P(-0.05, -0.47), P(0.75, -0.47), 0.09, 0.09)
        collar.set_fill(opacity=0).set_stroke(darker(self.HOODIE, 0.45), OUTLINE + 2)
        round_stroke(collar)
        strings = VGroup()
        for x0, x1 in ((0.20, 0.17), (0.52, 0.55)):
            ln = poly([P(x0, -0.56), P(x1, -0.76)]).set_stroke("#EDEDED", DETAIL + 1)
            dot = Circle(radius=0.035).move_to(P(x1, -0.78)).set_fill("#EDEDED", 1).set_stroke(width=0)
            strings.add(ln, dot)
        pocket = RoundedRectangle(width=0.62, height=0.22, corner_radius=0.08).move_to(P(0.3, -0.9))
        pocket.set_fill(opacity=0).set_stroke(darker(self.HOODIE, 0.45), DETAIL)
        g.add(hood, collar, strings, pocket)
        # freckles
        fr = VGroup(*[Circle(radius=0.022).move_to(P(x, y)) for x, y in
                      ((0.70, -0.01), (0.78, 0.02), (0.74, -0.07), (-0.02, -0.01), (0.06, -0.05))])
        fr.set_fill(darker(self.BODY_COLOR, 0.3), 1).set_stroke(width=0)
        g.add(fr)
        return g

    def _on_face(self, sp):
        crown = _cached("cap", lambda: Intersection(
            Circle(radius=0.84).move_to(P(0, 0.22)),
            Rectangle(width=3, height=1).move_to(P(0, 0.80 + 0.5))))
        crown.set_fill(self.CAP, 1).set_stroke(darker(self.CAP, 0.5), OUTLINE)
        brim = lens(P(0.28, 0.83), P(1.12, 0.76), -0.07, 0.07)
        brim.set_fill(darker(self.CAP, 0.15), 1).set_stroke(darker(self.CAP, 0.5), OUTLINE)
        button = Circle(radius=0.05).move_to(P(0, 1.06)).set_fill(darker(self.CAP, 0.2), 1)
        button.set_stroke(darker(self.CAP, 0.5), DETAIL)
        seam = lens(P(-0.08, 1.04), P(0.30, 0.82), 0.0, 0.0).set_fill(opacity=0)
        seam.set_stroke(darker(self.CAP, 0.35), DETAIL)
        return VGroup(crown, seam, brim, button)

    def _extras(self, name):
        if name == "?":
            return VGroup(self._mark("?", (0.98, 1.38), 0.5, "#FFD866"))
        if name == "!":
            return VGroup(self._mark("!", (1.0, 1.35), 0.5, TEXT))
        if name == "tear":
            return VGroup(drop(P(0.74, 0.02), 0.075))
        if name == "anger":
            return VGroup(_anger(P(-0.66, 0.98)))
        if name == "bulb":
            return VGroup(_bulb(P(0.25, 1.55)))
        if name == "dots":
            return VGroup(*[Circle(radius=0.035).move_to(P(0.95 + 0.13 * i, 1.0 + 0.0 * i))
                            .set_fill(TEXT, 1).set_stroke(width=0) for i in range(3)])
        return VGroup()


def _anger(c, color="#FF5A5A"):
    from manim import Arc
    g = VGroup()
    for dx, dy in ((1, 1), (-1, 1), (-1, -1), (1, -1)):
        ctr = c + P(dx, dy) * 0.12
        start = np.arctan2(-dy, -dx) - np.pi / 4
        a = Arc(radius=0.075, start_angle=start, angle=np.pi / 2, arc_center=ctr)
        a.set_stroke(color, 6).set_fill(opacity=0)
        g.add(round_stroke(a))
    return g


def _bulb(c, color="#FFE066"):
    from manim import Line
    glass = Circle(radius=0.2).move_to(c).set_fill(color, 1).set_stroke(darker(color, 0.5), DETAIL)
    base = RoundedRectangle(width=0.16, height=0.13, corner_radius=0.03).move_to(c + P(0, -0.25))
    base.set_fill("#9A9A9A", 1).set_stroke(INK, DETAIL)
    fil = lens(c + P(-0.06, -0.05), c + P(0.06, -0.05), -0.07, -0.07).set_fill(opacity=0)
    fil.set_stroke(darker(color, 0.55), DETAIL)
    rays = VGroup()
    for k in range(7):
        a = np.radians(200 - k * 36.67)
        d = P(np.cos(a), np.sin(a))
        rays.add(round_stroke(poly([c + d * 0.29, c + d * 0.42]).set_stroke(color, 5)))
    return VGroup(rays, glass, fil, base)
