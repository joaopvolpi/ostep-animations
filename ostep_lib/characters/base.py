"""Shared machinery for all characters.

Every character is a VGroup with three submobjects:

    [ref, core, extras]

* ``ref``    -- an invisible pair of tiny line segments that records the
               character's affine frame (position, scale, mirroring).  All
               geometry is designed in a fixed *local* frame and mapped
               through ``ref`` whenever the character is rebuilt.
* ``core``   -- the body, face and limbs.  Its sub-structure is identical for
               every expression, so expression changes morph smoothly.
* ``extras`` -- expression-specific decorations ("?", zZz, sweat drops, ...).
               These cross-fade on expression changes.

Rebuilding from state (expression, gaze) keeps the character always
consistent no matter what animations were applied before.
"""
from __future__ import annotations

import numpy as np
from manim import (
    Animation, AnimationGroup, CapStyleType, Circle, Ellipse, FadeOut, Mobject,
    VGroup, VMobject, Wait, BLACK, WHITE, ORIGIN, RIGHT, LEFT, UP,
    interpolate_color, there_and_back, smooth, config,
)
from manim.utils.color import ManimColor

# --------------------------------------------------------------------------
# Constants shared by every character (in local units, at default size)
# --------------------------------------------------------------------------
OUTLINE = 4          # main outline stroke width
from ..style import FONT  # series font (CMU Serif) for marks/labels
DETAIL = 3           # thin detail lines
INK = "#1E1A1E"      # outlines / pupils
MOUTH_DARK = "#3A1F27"
EYE_WHITE = "#FFFFFF"
_U = 0.25            # length of the reference segments


def P(x, y=0.0):
    return np.array([float(x), float(y), 0.0])


def mix(c1, c2, a):
    return interpolate_color(ManimColor(c1), ManimColor(c2), a)


def darker(c, a=0.35):
    return mix(c, BLACK, a)


def lighter(c, a=0.35):
    return mix(c, WHITE, a)


# --------------------------------------------------------------------------
# Small geometry helpers
# --------------------------------------------------------------------------
def poly(points, closed=False, **style):
    m = VMobject(**style)
    pts = [np.array(p, dtype=float) for p in points]
    if closed:
        pts = pts + [pts[0]]
    m.set_points_as_corners(pts)
    return m


def smooth_path(points, **style):
    m = VMobject(**style)
    m.set_points_smoothly([np.array(p, dtype=float) for p in points])
    return m


def round_stroke(m):
    m.cap_style = CapStyleType.ROUND
    return m


def lens(L, R, top, bot, **style):
    """Closed shape between corners L and R.

    The upper edge sags by ``top`` (positive = curves downward, like a smile)
    and the lower edge sags by ``bot``.  ``top == bot`` gives a single curve
    (drawn by the stroke).  Used for mouths, cap brims, beards...
    """
    L = np.array(L, dtype=float)
    R = np.array(R, dtype=float)
    hu = np.array([0, -top / 0.75, 0])
    hd = np.array([0, -bot / 0.75, 0])
    m = VMobject(**style)
    m.set_points(np.array([L, L + hu, R + hu, R, R, R + hd, L + hd, L]))
    return m


def mouth(center, w=0.15, cy=0.0, top=0.05, bot=0.05, tilt=0.0,
          fill=MOUTH_DARK, stroke=MOUTH_DARK, width=OUTLINE):
    c = np.array(center, dtype=float)
    L = c + P(-w, cy - tilt)
    R = c + P(w, cy + tilt)
    m = lens(L, R, top, bot)
    m.set_fill(fill, 1).set_stroke(stroke, width)
    round_stroke(m)
    return m


def zigzag(center, w=0.18, amp=0.04, n=5, color=MOUTH_DARK, width=OUTLINE):
    c = np.array(center, dtype=float)
    xs = np.linspace(-w, w, n)
    pts = [c + P(x, amp * (1 if i % 2 else -1)) for i, x in enumerate(xs)]
    m = poly(pts)
    m.set_fill(opacity=0).set_stroke(color, width)
    round_stroke(m)
    return m


def drop(center, r=0.08, color="#8FD3FF"):
    """Tear / sweat drop with the tip pointing up."""
    c = np.array(center, dtype=float)
    ts = np.linspace(0, 2 * np.pi, 33)
    pts = [c + P(r * 1.05 * np.sin(t) * np.sin(t / 2), r * 1.35 * np.cos(t)) for t in ts]
    m = VMobject()
    m.set_points_smoothly(pts)
    m.set_fill(color, 1).set_stroke(darker(color, 0.45), DETAIL)
    m.add(Circle(radius=r * 0.22).move_to(c + P(-r * 0.25, -r * 0.35))
          .set_fill(WHITE, 0.8).set_stroke(width=0))
    return m


def lid_shapes(c, rx, ry, h, ang, upper=True, n_arc=40, n_chord=9, bow=0.0):
    """Eyelid covering the part of an ellipse beyond a chord.

    ``h`` in [-1, 1]: 1 = lid fully open (degenerate), 0 = half closed,
    -1 = fully closed.  ``ang`` tilts the chord (radians).
    Returns (fill_polygon, chord_line).  Point counts are fixed so lids morph.
    """
    c = np.array(c, dtype=float)
    n = np.array([-np.sin(ang), np.cos(ang)])
    if not upper:
        n = -n
    phi = np.arctan2(n[1] * ry, n[0] * rx)
    half = np.arccos(np.clip(h, -1.0, 1.0))
    ts = np.linspace(phi - half, phi + half, n_arc)
    arc = [c + P(rx * np.cos(t), ry * np.sin(t)) for t in ts]
    a, b = arc[-1], arc[0]
    toward = P(-n[0], -n[1]) * np.linalg.norm(b - a) * bow
    chord = [a + (b - a) * k + toward * 4 * k * (1 - k) for k in np.linspace(0, 1, n_chord)]
    fill = VMobject()
    fill.set_points_as_corners(arc + chord[1:])
    line = VMobject()
    line.set_points_smoothly(chord)
    return fill, line


def make_eye(c, rx, ry, pupil_r, pupil_off, upper=(1, 0), lower=(1, 0),
             side=1, lid_color="#888888", sclera=EYE_WHITE, outline=INK,
             pupil_color=INK, lid_width=OUTLINE, sclera_stroke=OUTLINE, lower_bow=0.0):
    """A cartoon eye: sclera, pupil, highlight and upper/lower lids.

    ``side`` is +1 for the eye on the facing side (front), -1 for the back
    eye; lid angles use an "inner corner down is positive" convention.
    """
    c = np.array(c, dtype=float)
    s = Ellipse(width=2 * rx, height=2 * ry).move_to(c)
    s.set_fill(sclera, 1).set_stroke(outline, sclera_stroke)
    pc = c + np.array(pupil_off, dtype=float)
    pupil = Circle(radius=pupil_r).move_to(pc).set_fill(pupil_color, 1).set_stroke(width=0)
    hl = Circle(radius=pupil_r * 0.32).move_to(pc + P(-0.33 * pupil_r, 0.38 * pupil_r))
    hl.set_fill(WHITE, 1).set_stroke(width=0)
    pad = 0.045
    uf, ul = lid_shapes(c, rx + pad, ry + pad, upper[0], upper[1] * side, True)
    lf, ll = lid_shapes(c, rx + pad, ry + pad, lower[0], lower[1] * side, False, bow=lower_bow)
    for f in (uf, lf):
        f.set_fill(lid_color, 1).set_stroke(lid_color, 2)
    for ln in (ul, ll):
        ln.scale(rx / (rx + pad))
        ln.set_fill(opacity=0).set_stroke(outline, lid_width)
        round_stroke(ln)
    return VGroup(s, pupil, hl, uf, lf, ul, ll)


def brow(eye_c, rx, ry, raise_=0.0, ang=0.0, side=1, arch=0.03,
         color=INK, width=7, gap=0.11, length=None):
    c = np.array(eye_c, dtype=float) + P(0, ry + gap + raise_)
    L = (length or rx * 0.95)
    a = ang * side
    d = P(np.cos(a), np.sin(a)) * L
    m = lens(c - d, c + d, -arch, -arch)
    m.set_fill(opacity=0).set_stroke(color, width)
    round_stroke(m)
    return m


def gaze_offset(look, gaze, maxoff):
    v = np.array(look[:2], dtype=float) + np.array(gaze[:2], dtype=float)
    n = np.linalg.norm(v)
    if n > 1:
        v = v / n
    return P(v[0] * maxoff, v[1] * maxoff)


def upright(m):
    """Mark a mobject (usually text) so it is never mirrored by flip()."""
    m.upright = True
    return m


# --------------------------------------------------------------------------
# Generic multi-part morph animation
# --------------------------------------------------------------------------
class _Morph(Animation):
    """Interpolates several (mobject, start, end, t0, t1) tracks."""

    def _setup(self):  # pragma: no cover - overridden
        return []

    def begin(self):
        self._pairs = self._setup()
        if self.suspend_mobject_updating:
            self.mobject.suspend_updating()
        self.interpolate(0)

    def interpolate_mobject(self, alpha):
        a = self.rate_func(alpha)
        for mob, s, e, t0, t1 in self._pairs:
            b = float(np.clip((a - t0) / max(t1 - t0, 1e-6), 0, 1))
            for m, ms, me in zip(mob.get_family(), s.get_family(), e.get_family()):
                m.interpolate(ms, me, b)

    def get_all_mobjects(self):
        return [self.mobject]


class CharacterChange(_Morph):
    """Morphs a character to a new expression and/or gaze (or blinks).

    Created by ``Character.change``, ``look_at``, ``look`` and ``blink``.
    The target is computed when the animation *begins*, so it composes with
    ``Succession`` and with earlier animations.
    """

    def __init__(self, character, expression=None, look=None, blink=False, **kwargs):
        if blink:
            kwargs.setdefault("rate_func", there_and_back)
            kwargs.setdefault("run_time", 0.3)
        else:
            kwargs.setdefault("run_time", 0.7)
        if expression is not None:
            character._check_expression(expression)
        self.new_expression = expression
        self.new_look = None if look is None else np.array(look, dtype=float)[:2]
        self.blink = blink
        super().__init__(character, **kwargs)

    def _setup(self):
        ch = self.mobject
        expr = self.new_expression or ch.expression
        look = ch.gaze if self.new_look is None else self.new_look
        self._final = (expr, look)
        core_t, extras_t = ch._build_placed(expr, look, self.blink)
        pairs = []
        core = ch.core
        core.align_data(core_t)
        pairs.append((core, core.copy(), core_t, 0, 1))
        if expr == ch.expression:
            ex = ch.extras
            ex.align_data(extras_t)
            pairs.append((ex, ex.copy(), extras_t, 0, 1))
        else:
            old = ch.extras
            ch.submobjects[2] = VGroup(old, extras_t)
            pairs.append((old, old.copy(), old.copy().set_opacity(0), 0, 0.6))
            start = extras_t.copy().set_opacity(0)
            for sub in start.submobjects:
                sub.scale(0.6)
            pairs.append((extras_t, start, extras_t.copy(), 0.3, 1))
        return pairs

    def finish(self):
        super().finish()
        ch = self.mobject
        ch.expression, ch.gaze = self._final
        ch._rebuild()


# --------------------------------------------------------------------------
# Character base class
# --------------------------------------------------------------------------
class Character(VGroup):
    """Base class for all characters (see README for the full API)."""

    EXPRESSIONS: tuple = ()
    DEFAULT_EXPRESSION: str = None
    DEFAULT_SCALE = 1.0
    #: local point the speech/thought bubble tail points to
    BUBBLE_ANCHOR = P(0.5, 1.0)
    #: local point between the eyes (used by look_at)
    EYE_ANCHOR = P(0.3, 0.4)
    #: default gaze in local coordinates (x>0 = facing direction)
    DEFAULT_LOOK = (0.3, 0.0)

    def __init__(self, expression=None, **kwargs):
        super().__init__(**kwargs)
        expression = expression or self.DEFAULT_EXPRESSION
        self._check_expression(expression)
        self.expression = expression
        self.gaze = np.array(self.DEFAULT_LOOK, dtype=float)
        self.bubble = None
        d = self.DEFAULT_SCALE
        r1 = poly([ORIGIN, P(_U * d, 0)])
        r2 = poly([ORIGIN, P(0, _U * d)])
        self.ref = VGroup(r1, r2)
        self.ref.set_stroke(opacity=0, width=0).set_fill(opacity=0)
        self.submobjects = [self.ref, VGroup(), VGroup()]
        self._rebuild()

    # --------------------------------------------------------------- center
    # A character's "center" (``get_center``, ``move_to``, ``scale``, ``center_base``...) is the
    # center of its DEFAULT-expression body in the design frame, mapped to the scene.  The plain
    # bounding-box center moves with the expression (raised arms, props, extras), so placing
    # "Student(excited)" with ``move_to(P)`` used to land ~0.4 units away from where a neutral
    # Student had been standing: characters visibly jumped at scene cuts.  Edges
    # (``get_top()``, ``get_left()``...) still use the real bounding box.
    _DESIGN_CENTERS: dict = {}

    def _design_center(self):
        key = type(self)
        c = Character._DESIGN_CENTERS.get(key)
        if c is None:
            core, _ = self._build(self.DEFAULT_EXPRESSION, np.array(self.DEFAULT_LOOK, dtype=float), False)
            pts = np.concatenate([m.points for m in core.get_family() if len(m.points)])
            c = (pts.min(axis=0) + pts.max(axis=0)) / 2
            Character._DESIGN_CENTERS[key] = c
        return c

    def get_critical_point(self, direction):
        if len(self.submobjects) == 3 and not np.any(direction):
            return self.to_global(self._design_center())
        return super().get_critical_point(direction)

    # ---------------------------------------------------------------- frame
    @property
    def core(self):
        return self.submobjects[1]

    @property
    def extras(self):
        return self.submobjects[2]

    def _frame(self):
        r1, r2 = self.ref.submobjects
        o = r1.points[0]
        ex = (r1.points[-1] - o) / _U
        ey = (r2.points[-1] - r2.points[0]) / _U
        return o, ex, ey

    def _det(self):
        _, ex, ey = self._frame()
        return ex[0] * ey[1] - ex[1] * ey[0]

    def _scale_factor(self):
        return float(np.sqrt(abs(self._det())))

    def to_global(self, p):
        """Map a point from the character's local design frame to the scene."""
        o, ex, ey = self._frame()
        return o + p[0] * ex + p[1] * ey

    def to_local_vector(self, v):
        _, ex, ey = self._frame()
        M = np.array([[ex[0], ey[0]], [ex[1], ey[1]]])
        if abs(np.linalg.det(M)) < 1e-9:
            return np.zeros(2)
        return np.linalg.solve(M, np.array(v[:2], dtype=float))

    @property
    def facing(self):
        """RIGHT or LEFT: the direction the character is facing."""
        return LEFT if self._det() < 0 else RIGHT

    @property
    def is_flipped(self):
        return self._det() < 0

    # ------------------------------------------------------------ building
    def _check_expression(self, expression):
        if expression not in self.EXPRESSIONS:
            raise ValueError(
                f"{type(self).__name__} has no expression {expression!r}. "
                f"Valid expressions: {', '.join(self.EXPRESSIONS)}"
            )

    def _build(self, expression, look, blinking):
        """Return (core, extras) VGroups in local coordinates. Override."""
        raise NotImplementedError

    def _place(self, mob):
        o, ex, ey = self._frame()
        k = self._scale_factor() / self.DEFAULT_SCALE
        det = ex[0] * ey[1] - ex[1] * ey[0]
        for sm in mob.get_family():
            if len(sm.points):
                pts = sm.points
                sm.points = o + pts[:, :1] * ex + pts[:, 1:2] * ey
            if isinstance(sm, VMobject):
                sm.stroke_width = sm.stroke_width * k
                if getattr(sm, "background_stroke_width", 0):
                    sm.background_stroke_width *= k
        if det < 0:
            for sm in mob.get_family():
                if getattr(sm, "upright", False):
                    sm.stretch(-1, 0)
        return mob

    def _build_placed(self, expression, look, blinking=False):
        core, extras = self._build(expression, np.array(look, dtype=float), blinking)
        return self._place(core), self._place(extras)

    def _rebuild(self):
        core, extras = self._build_placed(self.expression, self.gaze, False)
        self.submobjects = [self.ref, core, extras]
        return self

    # ------------------------------------------------------ transformations
    def scale(self, scale_factor, scale_stroke=True, **kwargs):
        """Scales like any mobject; line widths scale too so proportions hold."""
        super().scale(scale_factor, **kwargs)
        if scale_stroke:
            f = abs(scale_factor)
            for sm in self.get_family():
                if isinstance(sm, VMobject):
                    sm.stroke_width = sm.stroke_width * f
        return self

    def flip(self, axis=UP, **kwargs):
        """Mirror horizontally in place so the character faces the other way."""
        center = self.to_global(ORIGIN)
        self.stretch(-1, 0, about_point=center)
        self._rebuild()
        return self

    # ---------------------------------------------------------- expressions
    def set_expression(self, expression):
        """Instantly switch expression. Returns self."""
        self._check_expression(expression)
        self.expression = expression
        return self._rebuild()

    def change(self, expression, look_at=None, **kwargs):
        """Animation morphing to ``expression`` (optionally also re-aiming the
        eyes at ``look_at``: a point or mobject)."""
        look = None if look_at is None else self._look_vector(look_at)
        return CharacterChange(self, expression=expression, look=look, **kwargs)

    def blink(self, **kwargs):
        """Animation: close and reopen the eyes."""
        return CharacterChange(self, blink=True, **kwargs)

    def _look_vector(self, target):
        if isinstance(target, Mobject):
            target = target.get_center()
        target = np.array(target, dtype=float)
        d = target - self.to_global(self.EYE_ANCHOR)
        v = self.to_local_vector(d)
        n = np.linalg.norm(v)
        return v / n if n > 1e-6 else np.zeros(2)

    def look_at(self, target, **kwargs):
        """Animation moving the pupils toward a point or mobject."""
        return CharacterChange(self, look=self._look_vector(target), **kwargs)

    def look(self, direction, **kwargs):
        """Animation: look in a scene direction (e.g. UP, LEFT, DL). ORIGIN
        resets to the default forward gaze."""
        direction = np.array(direction, dtype=float)
        if np.linalg.norm(direction) < 1e-6:
            v = np.array(self.DEFAULT_LOOK)
        else:
            v = self.to_local_vector(direction)
            v = v / max(np.linalg.norm(v), 1e-6)
        return CharacterChange(self, look=v, **kwargs)

    def set_look(self, target):
        """Instantly aim the eyes at a point/mobject. Returns self."""
        self.gaze = self._look_vector(target)
        return self._rebuild()

    # -------------------------------------------------------------- bubbles
    def get_bubble(self, content, kind="speech", **kwargs):
        """Build (but do not show) a Bubble anchored at this character's head."""
        from .bubbles import Bubble
        kwargs.setdefault("side", self.facing)
        return Bubble(content, kind=kind, tip=self.to_global(self.BUBBLE_ANCHOR), **kwargs)

    def _show_bubble(self, content, kind, expression=None, run_time=0.8, **kwargs):
        from .bubbles import BubbleIn
        bubble = self.get_bubble(content, kind=kind, **kwargs)
        anims = []
        if self.bubble is not None:
            anims.append(FadeOut(self.bubble, run_time=0.4))
        anims.append(BubbleIn(bubble, run_time=run_time))
        if expression is not None:
            anims.append(self.change(expression))
        self.bubble = bubble
        return AnimationGroup(*anims)

    def says(self, content, expression=None, run_time=0.8, **kwargs):
        """Animation showing a speech bubble with ``content`` (str or Mobject).

        The bubble is stored in ``self.bubble``; an existing bubble is faded
        out.  Extra kwargs go to :class:`Bubble` (font_size, max_width, ...).
        """
        return self._show_bubble(content, "speech", expression, run_time, **kwargs)

    def thinks(self, content, expression=None, run_time=0.8, **kwargs):
        """Like :meth:`says` but with a thought (cloud) bubble."""
        return self._show_bubble(content, "thought", expression, run_time, **kwargs)

    def remove_bubble(self, run_time=0.5):
        """Animation fading out the current bubble (no-op Wait if none)."""
        if self.bubble is None:
            return Wait(run_time=0.01)
        b, self.bubble = self.bubble, None
        return FadeOut(b, run_time=run_time)
