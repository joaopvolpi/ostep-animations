"""Small glyphs and icons introduced in episode 04 (The Process).

Everything is built from Manim primitives and series colors. All icons are
``VGroup``s roughly ``size`` units across and centered on ORIGIN, so place them
with ``.move_to()`` / ``.scale()``.
"""
from __future__ import annotations

import numpy as np
from manim import (
    Arc, Circle, Dot, Line, Polygon, Rectangle, RoundedRectangle, Text, VGroup,
    VMobject, Square, AnnularSector, Triangle, WHITE, BLACK, ORIGIN, UP, DOWN,
    LEFT, RIGHT, PI, TAU, interpolate_color,
)
from manim.utils.color import ManimColor

from ..style import (
    TEXT, DIM, BG, CPU_COLOR, MEM_COLOR, DISK_COLOR, KERNEL_COLOR, USER_COLOR,
    MONO_FONT, FONT, VIRT,
)

from .core import CARD_FILL  # shared card background
IDLE_GREY = "#333333"


def _P(x, y=0.0):
    return np.array([float(x), float(y), 0.0])


def mix(c1, c2, a):
    return interpolate_color(ManimColor(c1), ManimColor(c2), a)


# ---------------------------------------------------------------------------
# Tiny glyphs used inside other props
# ---------------------------------------------------------------------------
def mini_clock(radius=0.12, color=TEXT, fill="#2A2A2A", stroke_width=2):
    """A minimal clock face (circle + two hands)."""
    face = Circle(radius=radius).set_fill(fill, 1).set_stroke(color, stroke_width)
    hands = VGroup(
        Line(ORIGIN, _P(0, radius * 0.7)),
        Line(ORIGIN, _P(radius * 0.5, 0)),
    ).set_stroke(color, stroke_width)
    return VGroup(face, hands)


def hatch_rect(width, height, color=DIM, spacing=0.12, stroke_width=1.5, fill=IDLE_GREY,
               fill_opacity=1.0, angle=PI / 4):
    """A rectangle filled with diagonal hatching (used for 'idle')."""
    rect = Rectangle(width=width, height=height).set_fill(fill, fill_opacity).set_stroke(width=0)
    lines = VGroup()
    hw, hh = width / 2, height / 2
    # lines y = x - c  (45 degrees); clip to the rectangle
    span = width + height
    c = -span
    while c <= span:
        pts = []
        # intersection with x = -hw, x = hw, y = -hh, y = hh
        for x in (-hw, hw):
            y = x - c
            if -hh - 1e-9 <= y <= hh + 1e-9:
                pts.append(_P(x, y))
        for y in (-hh, hh):
            x = y + c
            if -hw - 1e-9 <= x <= hw + 1e-9:
                pts.append(_P(x, y))
        # unique
        uniq = []
        for p in pts:
            if all(np.linalg.norm(p - q) > 1e-6 for q in uniq):
                uniq.append(p)
        if len(uniq) == 2:
            lines.add(Line(uniq[0], uniq[1]).set_stroke(color, stroke_width))
        c += spacing
    return VGroup(rect, lines)


def check_mark(size=0.3, color="#8BE07A", stroke_width=6):
    m = VMobject().set_points_as_corners([_P(-0.5, 0.0), _P(-0.15, -0.35), _P(0.5, 0.4)])
    m.set_stroke(color, stroke_width).set_fill(opacity=0)
    return VGroup(m).scale(size)


def cross_mark(size=0.3, color=KERNEL_COLOR, stroke_width=6):
    g = VGroup(Line(_P(-0.5, -0.5), _P(0.5, 0.5)), Line(_P(-0.5, 0.5), _P(0.5, -0.5)))
    g.set_stroke(color, stroke_width)
    return g.scale(size)


def ep_tag(text, color=VIRT, font_size=20):
    """A small rounded 'see episode' tag, e.g. ep_tag("→ Ep. 06")."""
    t = Text(text, font_size=font_size, color=TEXT)
    box = RoundedRectangle(width=t.width + 0.25, height=t.height + 0.18, corner_radius=0.08)
    box.set_fill(CARD_FILL, 1).set_stroke(color, 2)
    box.move_to(t)
    return VGroup(box, t)


# ---------------------------------------------------------------------------
# App icons (S01): browser, music note, chat bubble, game pad, envelope
# ---------------------------------------------------------------------------
def browser_icon(size=0.7, color=USER_COLOR):
    w, h = size * 1.2, size
    body = RoundedRectangle(width=w, height=h, corner_radius=0.08).set_fill(CARD_FILL, 1)
    body.set_stroke(color, 3)
    strip = Rectangle(width=w, height=h * 0.22).move_to(body.get_top() + DOWN * h * 0.11)
    strip.set_fill(color, 0.6).set_stroke(width=0)
    tab = RoundedRectangle(width=w * 0.35, height=h * 0.16, corner_radius=0.03)
    tab.move_to(body.get_corner(UP + LEFT) + _P(w * 0.25, h * 0.04)).set_fill(color, 1).set_stroke(width=0)
    dots = VGroup(*[Dot(radius=0.025 * size / 0.7, color=TEXT) for _ in range(3)]).arrange(RIGHT, buff=0.04)
    dots.move_to(strip).align_to(strip, RIGHT).shift(LEFT * 0.06)
    lines = VGroup(*[Line(_P(-w * 0.35, 0), _P(w * (0.35 - 0.15 * (i % 2)), 0)) for i in range(3)])
    lines.arrange(DOWN, buff=h * 0.12, aligned_edge=LEFT).set_stroke(DIM, 2)
    lines.move_to(body).shift(DOWN * h * 0.1)
    return VGroup(body, strip, tab, dots, lines)


def music_icon(size=0.7, color="#C792EA"):
    s = size
    h1 = Circle(radius=0.13 * s / 0.7).set_fill(color, 1).set_stroke(width=0).move_to(_P(-0.18 * s, -0.25 * s))
    h2 = h1.copy().move_to(_P(0.22 * s, -0.17 * s))
    st1 = Line(h1.get_right() + _P(-0.01, 0), h1.get_right() + _P(-0.01, 0.55 * s))
    st2 = Line(h2.get_right() + _P(-0.01, 0), h2.get_right() + _P(-0.01, 0.55 * s))
    beam = Polygon(st1.get_end(), st2.get_end(), st2.get_end() + _P(0, -0.1 * s), st1.get_end() + _P(0, -0.1 * s))
    beam.set_fill(color, 1).set_stroke(color, 2)
    VGroup(st1, st2).set_stroke(color, 4)
    return VGroup(st1, st2, beam, h1, h2).move_to(ORIGIN)


def eighth_note(size=0.25, color="#C792EA"):
    head = Circle(radius=0.3 * size).set_fill(color, 1).set_stroke(width=0)
    stem = Line(head.get_right(), head.get_right() + _P(0, 1.1 * size)).set_stroke(color, 3)
    flag = VMobject().set_points_smoothly([stem.get_end(), stem.get_end() + _P(0.3 * size, -0.3 * size),
                                           stem.get_end() + _P(0.25 * size, -0.65 * size)])
    flag.set_stroke(color, 3)
    return VGroup(head, stem, flag).move_to(ORIGIN)


def chat_icon(size=0.7, color="#5FC6A8"):
    w, h = size * 1.1, size * 0.75
    body = RoundedRectangle(width=w, height=h, corner_radius=0.18 * size).set_fill(CARD_FILL, 1)
    body.set_stroke(color, 3)
    tail = Polygon(body.get_bottom() + _P(-0.25 * w, 0.02), body.get_bottom() + _P(-0.05 * w, 0.02),
                   body.get_bottom() + _P(-0.32 * w, -0.22 * size))
    tail.set_fill(CARD_FILL, 1).set_stroke(color, 3)
    cover = Line(tail.get_vertices()[0], tail.get_vertices()[1]).set_stroke(CARD_FILL, 4)
    dots = VGroup(*[Dot(radius=0.05 * size / 0.7, color=color) for _ in range(3)]).arrange(RIGHT, buff=0.1 * size)
    dots.move_to(body)
    return VGroup(tail, body, cover, dots).move_to(ORIGIN)


def gamepad_icon(size=0.7, color="#F4845F"):
    s = size
    body = RoundedRectangle(width=1.3 * s, height=0.7 * s, corner_radius=0.3 * s).set_fill(CARD_FILL, 1)
    body.set_stroke(color, 3)
    cross = VGroup(Rectangle(width=0.32 * s, height=0.1 * s), Rectangle(width=0.1 * s, height=0.32 * s))
    cross.set_fill(color, 1).set_stroke(width=0).move_to(body.get_center() + _P(-0.33 * s, 0))
    btns = VGroup(Dot(radius=0.06 * s, color=color).move_to(_P(0.28 * s, 0.07 * s)),
                  Dot(radius=0.06 * s, color=color).move_to(_P(0.42 * s, -0.07 * s)))
    btns.shift(body.get_center())
    return VGroup(body, cross, btns).move_to(ORIGIN)


def envelope_icon(size=0.7, color="#F2CC5B"):
    w, h = size * 1.15, size * 0.75
    body = Rectangle(width=w, height=h).set_fill(CARD_FILL, 1).set_stroke(color, 3)
    flap = VMobject().set_points_as_corners([body.get_corner(UP + LEFT), body.get_center() + _P(0, -0.05 * h),
                                             body.get_corner(UP + RIGHT)])
    flap.set_stroke(color, 3)
    return VGroup(body, flap)


# ---------------------------------------------------------------------------
# S04: sheet music, zZ
# ---------------------------------------------------------------------------
def sheet_music(width=0.9, height=1.15, color=DIM, note_color=None):
    page = Rectangle(width=width, height=height).set_fill(CARD_FILL, 1).set_stroke(color, 3)
    staffs = VGroup()
    notes = VGroup()
    nc = note_color or color
    for k, yc in enumerate((height * 0.22, -height * 0.2)):
        lines = VGroup(*[Line(_P(-width * 0.4, yc + i * 0.055 * height / 1.15 * 1.15 - 0.11),
                              _P(width * 0.4, yc + i * 0.055 * height / 1.15 * 1.15 - 0.11))
                         for i in range(5)]).set_stroke(color, 1.2)
        staffs.add(lines)
        for j, dx in enumerate((-0.25, -0.05, 0.15, 0.32)):
            y = yc - 0.11 + (j % 3) * 0.055 + 0.03
            n = eighth_note(0.11, nc).move_to(_P(dx * width, y + 0.05))
            notes.add(n)
    g = VGroup(page, staffs, notes)
    g.page, g.staffs, g.notes = page, staffs, notes
    return g


def zz_glyph(size=0.35, color=TEXT):
    a = Text("z", font_size=24, color=color, weight="BOLD").scale(size / 0.35 * 0.8)
    b = Text("Z", font_size=24, color=color, weight="BOLD").scale(size / 0.35)
    b.next_to(a, UP + RIGHT, buff=0.02)
    return VGroup(a, b)


# ---------------------------------------------------------------------------
# S08: robotic arm, mini bar chart, tag, dial
# ---------------------------------------------------------------------------
class RoboticArm(VGroup):
    """A two-segment arm (base, shoulder joint, upper arm, elbow, forearm, claw).

    ``shoulder`` is the pivot. Use ``arm.pose(a1, a2)`` (radians from +x) to
    get a target copy, or ``arm.animate_pose(a1, a2)`` for an animation.
    The claw tip is ``arm.tip()``.
    """

    def __init__(self, l1=1.2, l2=1.0, color=DIM, joint_color=KERNEL_COLOR, a1=PI / 3, a2=-PI / 6,
                 **kwargs):
        super().__init__(**kwargs)
        self.l1, self.l2 = l1, l2
        self.arm_color, self.joint_color = color, joint_color
        self.a1, self.a2 = a1, a2
        self._origin = ORIGIN.copy()
        self._build()

    def _build(self):
        o = self._origin
        e = o + self.l1 * _P(np.cos(self.a1), np.sin(self.a1))
        t = e + self.l2 * _P(np.cos(self.a2), np.sin(self.a2))
        base = Polygon(o + _P(-0.35, -0.3), o + _P(0.35, -0.3), o + _P(0.18, 0), o + _P(-0.18, 0))
        base.set_fill(mix(self.arm_color, BG, 0.4), 1).set_stroke(self.arm_color, 3)
        up = Line(o, e).set_stroke(self.arm_color, 9)
        fo = Line(e, t).set_stroke(self.arm_color, 7)
        j1 = Circle(radius=0.11).move_to(o).set_fill(self.joint_color, 1).set_stroke(TEXT, 2)
        j2 = Circle(radius=0.09).move_to(e).set_fill(self.joint_color, 1).set_stroke(TEXT, 2)
        d = (t - e) / max(np.linalg.norm(t - e), 1e-6)
        n = _P(-d[1], d[0])
        claw = VGroup(
            VMobject().set_points_as_corners([t, t + 0.18 * n + 0.12 * d, t + 0.1 * n + 0.25 * d]),
            VMobject().set_points_as_corners([t, t - 0.18 * n + 0.12 * d, t - 0.1 * n + 0.25 * d]),
        ).set_stroke(self.arm_color, 5)
        self.submobjects = [base, up, fo, claw, j1, j2]
        self._tip = t + 0.2 * d

    def tip(self):
        return self._tip.copy()

    def move_origin(self, point):
        self._origin = np.array(point, dtype=float)
        self._build()
        return self

    def set_pose(self, a1, a2):
        self.a1, self.a2 = a1, a2
        self._build()
        return self

    def pose(self, a1, a2):
        c = self.copy()
        c._origin = self._origin.copy()
        return c.set_pose(a1, a2)

    def tip_for(self, a1, a2):
        return self.pose(a1, a2).tip()


def mini_bar_chart(size=0.6, color=CPU_COLOR):
    axes = VMobject().set_points_as_corners([_P(-0.5, 0.5), _P(-0.5, -0.5), _P(0.5, -0.5)])
    axes.set_stroke(TEXT, 2)
    bars = VGroup(*[Rectangle(width=0.18, height=h).set_fill(color, 0.9).set_stroke(width=0)
                    .move_to(_P(-0.3 + 0.27 * i, -0.5 + h / 2)) for i, h in enumerate((0.4, 0.8, 0.55))])
    return VGroup(axes, bars).scale(size)


def tag_icon(size=0.6, color=USER_COLOR):
    body = Polygon(_P(-0.5, 0.28), _P(0.25, 0.28), _P(0.5, 0), _P(0.25, -0.28), _P(-0.5, -0.28))
    body.set_fill(CARD_FILL, 1).set_stroke(color, 3)
    hole = Circle(radius=0.07).move_to(_P(0.22, 0)).set_stroke(color, 2)
    return VGroup(body, hole).scale(size)


def dial_icon(size=0.7, color=VIRT, value=0.5):
    arc = Arc(radius=0.5, start_angle=PI, angle=-PI).set_stroke(TEXT, 3)
    ticks = VGroup(*[Line(_P(0.42 * np.cos(a), 0.42 * np.sin(a)), _P(0.5 * np.cos(a), 0.5 * np.sin(a)))
                     for a in np.linspace(PI, 0, 5)]).set_stroke(TEXT, 2)
    a = PI * (1 - value)
    needle = Line(ORIGIN, _P(0.4 * np.cos(a), 0.4 * np.sin(a))).set_stroke(color, 4)
    hub = Dot(radius=0.05, color=color)
    g = VGroup(arc, ticks, needle, hub).scale(size)
    g.needle = needle
    return g


# ---------------------------------------------------------------------------
# S06: speed gauge
# ---------------------------------------------------------------------------
class SpeedGauge(VGroup):
    """A small horizontal bar gauge with a percentage label."""

    def __init__(self, value=1.0, width=1.2, height=0.16, color=CPU_COLOR, font_size=18, **kwargs):
        super().__init__(**kwargs)
        self.w, self.h, self.bar_color, self.fs = width, height, color, font_size
        self.track = RoundedRectangle(width=width, height=height, corner_radius=height / 2)
        self.track.set_fill(CARD_FILL, 1).set_stroke(DIM, 1.5)
        self.bar = self._bar(value)
        self.label = self._label(value)
        self.add(self.track, self.bar, self.label)

    def _bar(self, v):
        w = max(self.w * v, 0.02)
        b = RoundedRectangle(width=w, height=self.h * 0.8, corner_radius=self.h * 0.4)
        b.set_fill(self.bar_color, 1).set_stroke(width=0)
        b.align_to(self.track, LEFT).shift(RIGHT * self.h * 0.1)
        b.set_y(self.track.get_y())
        return b

    def _label(self, v, text=None):
        t = Text(text or f"{round(v * 100)}%", font_size=self.fs, color=TEXT)
        t.next_to(self.track, DOWN, buff=0.08)
        return t

    def value_targets(self, value, text=None):
        """Return (bar_target, label_target) for a Transform."""
        return self._bar(value), self._label(value, text)


# ---------------------------------------------------------------------------
# S09 / S18: notepad and save slot
# ---------------------------------------------------------------------------
class Notepad(VGroup):
    """A notepad with a title and N empty bullet lines; ``fill_line(i, text)``
    returns the Text to write on line i (already positioned)."""

    def __init__(self, title="To resume:", lines=3, width=3.6, font_size=22, color=TEXT, **kwargs):
        super().__init__(**kwargs)
        lh = 0.36
        height = 0.6 + lines * lh
        self.page = RoundedRectangle(width=width, height=height, corner_radius=0.08)
        self.page.set_fill("#2E2B25", 1).set_stroke("#D9CCAE", 2.5)
        rings = VGroup(*[Circle(radius=0.05).set_stroke("#D9CCAE", 2) for _ in range(5)])
        rings.arrange(RIGHT, buff=(width - 0.6) / 5).move_to(self.page.get_top())
        self.title = Text(title, font_size=font_size, color=color, weight="BOLD")
        self.title.move_to(self.page.get_top() + DOWN * 0.3).align_to(self.page, LEFT).shift(RIGHT * 0.2)
        self.bullets = VGroup()
        self.slots = []
        for i in range(lines):
            y = self.page.get_top()[1] - 0.62 - i * lh
            b = Dot(radius=0.035, color=DIM).move_to(_P(self.page.get_left()[0] + 0.3, y))
            ln = Line(_P(b.get_x() + 0.15, y - 0.1), _P(self.page.get_right()[0] - 0.2, y - 0.1))
            ln.set_stroke(DIM, 1, opacity=0.6)
            self.bullets.add(VGroup(b, ln))
            self.slots.append(_P(b.get_x() + 0.15, y))
        self.font_size = font_size
        self.add(self.page, rings, self.title, self.bullets)

    def line_text(self, i, text, color=TEXT):
        t = Text(text, font_size=self.font_size, color=color)
        if t.width > self.page.width - 0.6:
            t.scale_to_fit_width(self.page.width - 0.6)
        t.move_to(self.slots[i] + self.get_center() * 0, aligned_edge=LEFT)
        t.align_to(self.bullets[i][1], LEFT).set_y(self.bullets[i][0].get_y())
        return t


def save_slot(size=1.0, color=USER_COLOR, label="SAVE SLOT"):
    """A floppy-disk-like 'save slot' icon (~size units tall)."""
    s = size
    body = Polygon(_P(-0.5, 0.5), _P(0.36, 0.5), _P(0.5, 0.36), _P(0.5, -0.5), _P(-0.5, -0.5))
    body.set_fill(mix(color, BG, 0.55), 1).set_stroke(color, 3)
    shutter = Rectangle(width=0.5, height=0.3).move_to(_P(-0.02, 0.33)).set_fill(mix(color, WHITE, 0.4), 1)
    shutter.set_stroke(width=0)
    notch = Rectangle(width=0.1, height=0.2).move_to(_P(0.1, 0.33)).set_fill(mix(color, BG, 0.55), 1).set_stroke(width=0)
    lab = RoundedRectangle(width=0.78, height=0.42, corner_radius=0.04).move_to(_P(0, -0.2))
    lab.set_fill(TEXT, 1).set_stroke(width=0)
    t = Text(label, font_size=48, color=BG, weight="BOLD")
    t.scale_to_fit_width(0.66)
    if t.height > 0.3:
        t.scale_to_fit_height(0.3)
    t.move_to(lab)
    return VGroup(body, shutter, notch, lab, t).scale(s)


# ---------------------------------------------------------------------------
# S10: menu card, cursor, puff, info tag
# ---------------------------------------------------------------------------
class MenuCard(VGroup):
    """A restaurant-style menu: title, divider and numbered rows.

    ``row_highlight(i)`` returns a highlight rectangle (not added) for row i.
    """

    def __init__(self, title="Menu", items=(), width=4.0, height=4.6, font_size=28,
                 accent=VIRT, **kwargs):
        super().__init__(**kwargs)
        self.card = RoundedRectangle(width=width, height=height, corner_radius=0.18)
        self.card.set_fill(CARD_FILL, 1).set_stroke(accent, 3)
        self.title = Text(title, font_size=font_size + 6, color=TEXT, weight="BOLD")
        self.title.move_to(self.card.get_top() + DOWN * 0.45)
        orn = VGroup(Line(LEFT * 0.9, RIGHT * 0.9).set_stroke(accent, 2),
                     Dot(radius=0.05, color=accent))
        orn.next_to(self.title, DOWN, buff=0.15)
        self.rows = VGroup()
        top = orn.get_bottom()[1] - 0.25
        avail = top - (self.card.get_bottom()[1] + 0.25)
        step = avail / max(len(items), 1)
        for i, it in enumerate(items):
            t = Text(it, font_size=font_size, color=TEXT)
            t.move_to(_P(self.card.get_left()[0] + 0.4, top - step * (i + 0.5)), aligned_edge=LEFT)
            self.rows.add(t)
        self.step = step
        self.add(self.card, self.title, orn, self.rows)

    def row_highlight(self, i, color=VIRT):
        r = self.rows[i]
        h = RoundedRectangle(width=self.card.width - 0.3, height=min(self.step * 0.85, 0.6), corner_radius=0.08)
        h.move_to(_P(self.card.get_x(), r.get_y())).set_fill(color, 0.2).set_stroke(color, 2)
        return h


def cursor_icon(size=0.4, color=TEXT):
    arrow = Polygon(_P(0, 0), _P(0, -1.0), _P(0.28, -0.75), _P(0.48, -1.15), _P(0.62, -1.08),
                    _P(0.42, -0.68), _P(0.75, -0.68))
    arrow.set_fill(color, 1).set_stroke(BG, 2)
    return VGroup(arrow).scale(size, about_point=ORIGIN)


def puff(radius=0.5, color=DIM, n=7):
    g = VGroup()
    for i in range(n):
        a = TAU * i / n
        g.add(Circle(radius=radius * 0.3).move_to(_P(radius * np.cos(a), radius * np.sin(a)))
              .set_fill(color, 0.7).set_stroke(TEXT, 1.5))
    return g


def info_tag(text, color=TEXT, font_size=22, stroke=DIM):
    t = Text(text, font_size=font_size, color=color)
    box = RoundedRectangle(width=t.width + 0.3, height=t.height + 0.22, corner_radius=0.1)
    box.set_fill(CARD_FILL, 1).set_stroke(stroke, 2).move_to(t)
    return VGroup(box, t)


def progress_ring(radius=0.3, color=CPU_COLOR, value=0.0, width=5):
    """Ring background + an arc from 12 o'clock covering ``value`` (0..1)."""
    bg = Circle(radius=radius).set_stroke(DIM, width, opacity=0.5)
    arc = Arc(radius=radius, start_angle=PI / 2, angle=-TAU * max(value, 1e-3)).set_stroke(color, width)
    return VGroup(bg, arc)


# ---------------------------------------------------------------------------
# S12: keyboard, plug
# ---------------------------------------------------------------------------
def keyboard_icon(size=0.8, color=TEXT):
    body = RoundedRectangle(width=1.4, height=0.55, corner_radius=0.08).set_fill(CARD_FILL, 1)
    body.set_stroke(color, 2.5)
    keys = VGroup()
    for r in range(3):
        for c in range(8 if r < 2 else 5):
            k = Square(side_length=0.11).set_fill(DIM, 1).set_stroke(width=0)
            k.move_to(_P(-0.56 + c * 0.16 + (0.24 if r == 2 else 0), 0.14 - r * 0.15))
            keys.add(k)
    return VGroup(body, keys).scale(size / 1.4)


def plug_glyph(label, color=TEXT, font_size=18):
    t = Text(label, font=MONO_FONT, font_size=font_size, color=color)
    box = RoundedRectangle(width=t.width + 0.22, height=0.32, corner_radius=0.06)
    box.set_fill(CARD_FILL, 1).set_stroke(color, 2).move_to(t)
    prongs = VGroup(Line(LEFT * 0.12, ORIGIN), Line(LEFT * 0.12, ORIGIN)).set_stroke(color, 2)
    prongs[0].next_to(box, LEFT, buff=0).shift(UP * 0.06)
    prongs[1].next_to(box, LEFT, buff=0).shift(DOWN * 0.06)
    return VGroup(prongs, box, t)


# ---------------------------------------------------------------------------
# S16: scheduler whistle
# ---------------------------------------------------------------------------
def whistle_icon(size=0.7, color=TEXT, accent=VIRT):
    s = size
    body = Circle(radius=0.3).set_fill(mix(accent, BG, 0.2), 1).set_stroke(color, 3).move_to(_P(-0.1, -0.05))
    mouth = Rectangle(width=0.55, height=0.22).set_fill(mix(accent, BG, 0.2), 1).set_stroke(color, 3)
    mouth.move_to(_P(0.32, 0.12))
    cover = Rectangle(width=0.2, height=0.18).set_fill(mix(accent, BG, 0.2), 1).set_stroke(width=0)
    cover.move_to(_P(0.08, 0.1))
    hole = Circle(radius=0.07).set_fill(BG, 1).set_stroke(color, 2).move_to(_P(-0.1, -0.05))
    ring = Circle(radius=0.09).set_stroke(color, 3).move_to(_P(-0.45, 0.22))
    lines = VGroup(*[Line(_P(0.7, 0.12 + d), _P(0.88, 0.12 + 1.6 * d)) for d in (-0.12, 0.0, 0.12)])
    lines.set_stroke(accent, 3)
    return VGroup(ring, body, mouth, cover, hole, lines).scale(s / 0.9).move_to(ORIGIN)


# ---------------------------------------------------------------------------
# S19: tombstone-free zombie stitches are in Process("zombie"); here: exit tag
# ---------------------------------------------------------------------------
def exit_tag(code=0, font_size=22):
    ok = code == 0
    col = "#8BE07A" if ok else KERNEL_COLOR
    t = Text(f"exit code: {code}", font_size=font_size, color=TEXT)
    mark = (check_mark(0.22, col, 5) if ok else cross_mark(0.14, col, 5)).next_to(t, RIGHT, buff=0.12)
    g = VGroup(t, mark)
    box = RoundedRectangle(width=g.width + 0.3, height=g.height + 0.22, corner_radius=0.08)
    box.set_fill(CARD_FILL, 1).set_stroke(col, 2.5).move_to(g)
    return VGroup(box, t, mark)


__all__ = [
    "IDLE_GREY", "mini_clock", "hatch_rect", "check_mark", "cross_mark", "ep_tag",
    "browser_icon", "music_icon", "eighth_note", "chat_icon", "gamepad_icon", "envelope_icon",
    "sheet_music", "zz_glyph", "RoboticArm", "mini_bar_chart", "tag_icon", "dial_icon",
    "SpeedGauge", "Notepad", "save_slot", "MenuCard", "cursor_icon", "puff", "info_tag",
    "progress_ring", "keyboard_icon", "plug_glyph", "whistle_icon", "exit_tag",
]
