"""Simple primitive icons introduced in episode 01-03.  No brand logos.

Every function returns a VGroup roughly ``size`` units tall (centered at ORIGIN).
"""
from __future__ import annotations

import numpy as np
from manim import (
    Arc, ArcBetweenPoints, Circle, Dot, Ellipse, Line, Polygon, Rectangle, RoundedRectangle,
    Rotate, Square, Star, Text, VGroup, VMobject, DashedVMobject, Cross,
    DOWN, LEFT, ORIGIN, RIGHT, UP, UL, UR, DL, DR, PI, TAU, BOLD,
)

from ..style import (
    BG, CPU_COLOR, DIM, DISK_COLOR, FONT, KERNEL_COLOR, MEM_COLOR, MONO_FONT, PERS, SEC,
    TEXT, USER_COLOR, COMPUTER_COLOR,
)
from ..characters.base import darker, lighter, mix
from .core import CARD_FILL, INK, outline_of

OK_GREEN = "#8BE07A"
BAD_RED = "#FF5A5A"
PAPER = "#E9E1C9"
CABINET = "#6E7B8B"

__all__ = [
    "OK_GREEN", "BAD_RED", "PAPER",
    "tick_mark", "x_mark", "next_tag", "question_mark", "book_icon", "editor_icon",
    "punch_cards_icon", "mainframe_icon", "minicomputer_icon", "operator_icon",
    "server_rack_icon", "phone_icon", "desktop_icon", "PowerSwitch", "ssd_icon",
    "journal_icon", "cow_icon", "sticky_note", "padlock_icon", "leaf_icon",
    "stopwatch_icon", "ecg_icon", "scroll_icon", "pipe_glyph", "poster_frame",
    "net_boxes", "letter_icon", "chair_icon", "bookshelf_icon", "layers_icon",
    "walls_icon", "hand_icon", "name_tag", "money_meter", "loop_arrow",
]


def _poly(pts, closed=True):
    m = VMobject()
    pts = [np.array(p, dtype=float) for p in pts]
    if closed:
        pts = pts + [pts[0]]
    m.set_points_as_corners(pts)
    return m


def tick_mark(size=0.4, color=OK_GREEN, width=8):
    m = _poly([[-0.5, 0.0, 0], [-0.15, -0.38, 0], [0.5, 0.42, 0]], closed=False)
    m.set_stroke(color, width).set_fill(opacity=0).scale(size)
    return VGroup(m)


def x_mark(size=0.4, color=BAD_RED, width=8):
    a = Line([-0.5, -0.5, 0], [0.5, 0.5, 0])
    b = Line([-0.5, 0.5, 0], [0.5, -0.5, 0])
    return VGroup(a, b).set_stroke(color, width).scale(size)


def next_tag(text="→ Ep. 04", font_size=20, color=DIM):
    """Small rounded tag pointing to a later episode."""
    t = Text(text, font=FONT, font_size=font_size, color=color)
    r = RoundedRectangle(width=t.width + 0.25, height=t.height + 0.18, corner_radius=0.08)
    r.set_fill(CARD_FILL, 1).set_stroke(color, 1.5)
    return VGroup(r, t.move_to(r))


def question_mark(size=0.6, color=CPU_COLOR):
    return Text("?", font=FONT, font_size=60, color=color, weight=BOLD).scale_to_fit_height(size)


def book_icon(title="", subtitle="", color="#6FA8F7", width=1.3, height=1.7, font_size=20):
    cover = RoundedRectangle(width=width, height=height, corner_radius=0.06)
    cover.set_fill(color, 1).set_stroke(outline_of(color), 3)
    spine = Rectangle(width=width * 0.12, height=height).align_to(cover, LEFT).set_fill(darker(color, 0.3), 1)
    spine.set_stroke(outline_of(color), 2)
    pages = Rectangle(width=width * 0.92, height=height * 0.06).next_to(cover, DOWN, buff=-height * 0.03)
    pages.set_fill(PAPER, 1).set_stroke(outline_of(color), 2)
    g = VGroup(pages, cover, spine)
    if title:
        t = Text(title, font=FONT, font_size=font_size, color=INK, weight=BOLD)
        if t.width > width * 0.78:
            t.scale_to_fit_width(width * 0.78)
        t.move_to(cover.get_center() + UP * height * 0.12 + RIGHT * width * 0.05)
        g.add(t)
    if subtitle:
        s = Text(subtitle, font=FONT, font_size=font_size - 4, color=INK)
        if s.width > width * 0.78:
            s.scale_to_fit_width(width * 0.78)
        s.move_to(cover.get_center() + DOWN * height * 0.2 + RIGHT * width * 0.05)
        g.add(s)
    return g


def editor_icon(width=1.6):
    """Code-editor window with a few colored code lines and a cursor (``[-1]``)."""
    h = width * 0.7
    win = RoundedRectangle(width=width, height=h, corner_radius=0.08).set_fill("#111111", 1).set_stroke(DIM, 2.5)
    bar = Line(win.get_corner(UL) + DOWN * 0.18, win.get_corner(UR) + DOWN * 0.18).set_stroke(DIM, 1.5)
    cols = [CPU_COLOR, USER_COLOR, TEXT, PERS]
    lines = VGroup()
    for k, (c, L) in enumerate(zip(cols, (0.5, 0.75, 0.4, 0.6))):
        y = win.get_top()[1] - 0.33 - k * h * 0.17
        x0 = win.get_left()[0] + 0.15 + (0.12 if k in (1, 2) else 0)
        lines.add(Line([x0, y, 0], [x0 + width * L * 0.7, y, 0]).set_stroke(c, 3))
    cur = Rectangle(width=0.05, height=0.14).set_fill(TEXT, 1).set_stroke(width=0)
    cur.next_to(lines[-1], RIGHT, buff=0.06)
    return VGroup(win, bar, lines, cur)


def punch_cards_icon(n=5, width=0.9, color=PAPER):
    g = VGroup()
    for k in range(n):
        c = Polygon([-0.5, 0.3, 0], [0.38, 0.3, 0], [0.5, 0.18, 0], [0.5, -0.3, 0], [-0.5, -0.3, 0])
        c.set_fill(color, 1).set_stroke(darker(color, 0.5), 2).scale(width)
        holes = VGroup(*[Rectangle(width=0.05, height=0.1).move_to([x, y, 0])
                         for x in np.linspace(-0.35, 0.3, 6) for y in (0.1, -0.12) if (int(x * 10) + k) % 3])
        holes.set_fill(INK, 0.7).set_stroke(width=0).scale(width, about_point=ORIGIN)
        g.add(VGroup(c, holes).shift(UP * 0.07 * k + RIGHT * 0.04 * k))
    return g


def mainframe_icon(width=2.4, height=3.0, color=CABINET):
    """Tall cabinets with blinking dots (``.lights``) and tape reels."""
    cabs = VGroup()
    lights = VGroup()
    n = 3
    cw = width / n
    for i in range(n):
        r = Rectangle(width=cw * 0.96, height=height).move_to([-width / 2 + cw * (i + 0.5), 0, 0])
        r.set_fill(color, 1).set_stroke(outline_of(color), 3)
        cabs.add(r)
        if i == 1:
            for y in (0.8, 0.2):
                reel = Circle(radius=cw * 0.25).move_to(r.get_center() + UP * y * height / 3)
                reel.set_fill(darker(color, 0.4), 1).set_stroke(outline_of(color), 2)
                cabs.add(reel, Dot(reel.get_center(), radius=0.04).set_fill(TEXT, 1))
        else:
            for row in range(5):
                for col in range(3):
                    d = Dot(r.get_center() + np.array([(col - 1) * cw * 0.25, height * 0.35 - row * 0.22, 0]), radius=0.045)
                    c = [CPU_COLOR, OK_GREEN, BAD_RED][(row + col + i) % 3]
                    d.set_fill(c, 1)
                    lights.add(d)
    g = VGroup(cabs, lights)
    g.lights = lights
    g.cabinets = cabs
    return g


def minicomputer_icon(width=1.4, height=1.8, color="#8A9BB0"):
    body = RoundedRectangle(width=width, height=height, corner_radius=0.06).set_fill(color, 1).set_stroke(outline_of(color), 3)
    panel = Rectangle(width=width * 0.8, height=height * 0.25).move_to(body.get_top() + DOWN * height * 0.2)
    panel.set_fill(darker(color, 0.4), 1).set_stroke(outline_of(color), 2)
    sw = VGroup(*[Rectangle(width=0.05, height=0.14).set_fill(CPU_COLOR if k % 3 == 0 else TEXT, 1).set_stroke(width=0)
                  for k in range(8)]).arrange(RIGHT, buff=0.06).move_to(panel)
    reels = VGroup(*[Circle(radius=width * 0.16).set_fill(darker(color, 0.45), 1).set_stroke(outline_of(color), 2)
                     for _ in range(2)]).arrange(RIGHT, buff=width * 0.15).move_to(body.get_center() + DOWN * height * 0.12)
    return VGroup(body, panel, sw, reels)


def operator_icon(height=1.6, color="#B9B2A3"):
    """Generic humanoid (circle head + body), not a series character."""
    head = Circle(radius=height * 0.15).move_to(UP * height * 0.33).set_fill(color, 1).set_stroke(outline_of(color), 3)
    body = RoundedRectangle(width=height * 0.42, height=height * 0.5, corner_radius=height * 0.12)
    body.move_to(DOWN * height * 0.08).set_fill(darker(color, 0.25), 1).set_stroke(outline_of(color), 3)
    legs = VGroup(*[Line([x, -height * 0.3, 0], [x, -height * 0.5, 0]) for x in (-0.08 * height, 0.08 * height)])
    legs.set_stroke(outline_of(color), 5)
    return VGroup(legs, body, head)


def server_rack_icon(width=1.0, height=1.8, color="#7C8894"):
    frame = RoundedRectangle(width=width, height=height, corner_radius=0.05).set_fill(darker(color, 0.4), 1)
    frame.set_stroke(outline_of(color), 3)
    units = VGroup()
    for k in range(5):
        u = Rectangle(width=width * 0.84, height=height * 0.14).move_to(frame.get_top() + DOWN * height * (0.13 + 0.18 * k))
        u.set_fill(color, 1).set_stroke(outline_of(color), 2)
        d = Dot(u.get_right() + LEFT * 0.12, radius=0.04).set_fill(OK_GREEN, 1)
        units.add(u, d)
    return VGroup(frame, units)


def phone_icon(height=1.3, color=TEXT):
    body = RoundedRectangle(width=height * 0.52, height=height, corner_radius=height * 0.08)
    body.set_fill(CARD_FILL, 1).set_stroke(color, 3)
    screen = RoundedRectangle(width=height * 0.42, height=height * 0.78, corner_radius=height * 0.03)
    screen.set_fill("#2A3A4A", 1).set_stroke(width=0)
    btn = Circle(radius=height * 0.035).move_to(body.get_bottom() + UP * height * 0.055).set_stroke(color, 1.5)
    return VGroup(body, screen, btn)


def desktop_icon(width=1.4, color=TEXT):
    mon = RoundedRectangle(width=width, height=width * 0.65, corner_radius=0.06).set_fill(CARD_FILL, 1).set_stroke(color, 3)
    scr = Rectangle(width=width * 0.86, height=width * 0.5).move_to(mon).set_fill("#2A3A4A", 1).set_stroke(width=0)
    neck = Rectangle(width=width * 0.1, height=width * 0.15).next_to(mon, DOWN, buff=0).set_fill(color, 1).set_stroke(width=0)
    foot = RoundedRectangle(width=width * 0.45, height=width * 0.06, corner_radius=0.02).next_to(neck, DOWN, buff=0)
    foot.set_fill(color, 1).set_stroke(width=0)
    return VGroup(mon, scr, neck, foot)


class PowerSwitch(VGroup):
    """Toggle switch with ON/OFF labels.  ``flip(on)`` animation rotates the lever."""

    def __init__(self, size=0.9, on=True, **kwargs):
        super().__init__(**kwargs)
        self.plate = RoundedRectangle(width=size * 0.7, height=size, corner_radius=0.08)
        self.plate.set_fill(CARD_FILL, 1).set_stroke(TEXT, 3)
        self.pivot = Dot(radius=size * 0.07).set_fill(DIM, 1)
        self.lever = RoundedRectangle(width=size * 0.14, height=size * 0.42, corner_radius=size * 0.06)
        self.lever.set_fill(TEXT, 1).set_stroke(INK, 2)
        self.lever.next_to(self.pivot, UP, buff=-size * 0.05)
        self.on_lab = Text("ON", font=FONT, font_size=16, color=OK_GREEN).next_to(self.plate, UP, buff=0.08)
        self.off_lab = Text("OFF", font=FONT, font_size=16, color=BAD_RED).next_to(self.plate, DOWN, buff=0.08)
        self.is_on = True
        self.add(self.plate, self.lever, self.pivot, self.on_lab, self.off_lab)
        if not on:
            self.lever.rotate(PI, about_point=self.pivot.get_center())
            self.is_on = False

    def flip(self, on=None, run_time=0.4):
        on = (not self.is_on) if on is None else on
        ang = 0 if on == self.is_on else PI
        self.is_on = on
        return Rotate(self.lever, ang, about_point=self.pivot.get_center(), run_time=run_time)


def ssd_icon(width=1.4, label="SSD"):
    body = RoundedRectangle(width=width, height=width * 0.55, corner_radius=0.06)
    body.set_fill(darker(DISK_COLOR, 0.35), 1).set_stroke(outline_of(DISK_COLOR), 3)
    chips = VGroup(*[Rectangle(width=width * 0.17, height=width * 0.22).set_fill(INK, 1).set_stroke(DIM, 1)
                     for _ in range(4)]).arrange(RIGHT, buff=width * 0.05).move_to(body.get_center() + UP * width * 0.04)
    pins = VGroup(*[Rectangle(width=width * 0.04, height=width * 0.06).set_fill(CPU_COLOR, 1).set_stroke(width=0)
                    for _ in range(9)]).arrange(RIGHT, buff=width * 0.04).next_to(body, DOWN, buff=-width * 0.08)
    g = VGroup(body, chips, pins)
    return g


def journal_icon(size=0.7, color="#C9A36B"):
    cover = RoundedRectangle(width=size * 0.78, height=size, corner_radius=0.05).set_fill(color, 1).set_stroke(outline_of(color), 2.5)
    rings = VGroup(*[Circle(radius=size * 0.05).move_to(cover.get_left() + UP * y * size).set_stroke(TEXT, 2)
                     for y in (0.3, 0.1, -0.1, -0.3)])
    lines = VGroup(*[Line([-size * 0.2, y * size, 0], [size * 0.28, y * size, 0]).set_stroke(INK, 2)
                     for y in (0.2, 0.0, -0.2)])
    return VGroup(cover, rings, lines)


def cow_icon(size=0.7):
    """Copy-on-write: two overlapping pages."""
    def page(c):
        p = RoundedRectangle(width=size * 0.6, height=size * 0.8, corner_radius=0.04).set_fill(mix(c, BG, 0.4), 1).set_stroke(c, 2.5)
        ls = VGroup(*[Line([-size * 0.18, y * size, 0], [size * 0.18, y * size, 0]).set_stroke(c, 1.5) for y in (0.15, 0, -0.15)])
        return VGroup(p, ls)
    a = page(DIM).shift(LEFT * size * 0.15 + UP * size * 0.1)
    b = page(TEXT).shift(RIGHT * size * 0.15 + DOWN * size * 0.1)
    return VGroup(a, b)


def sticky_note(text="later!", size=0.9, color="#F2E27A"):
    n = Polygon([-0.5, 0.5, 0], [0.5, 0.5, 0], [0.5, -0.3, 0], [0.3, -0.5, 0], [-0.5, -0.5, 0]).scale(size)
    n.set_fill(color, 1).set_stroke(darker(color, 0.4), 2)
    t = Text(text, font=FONT, font_size=22, color=INK)
    if t.width > size * 0.85:
        t.scale_to_fit_width(size * 0.85)
    return VGroup(n, t.move_to(n.get_center() + UP * size * 0.05)).rotate(0.12)


def padlock_icon(size=0.5, color=SEC):
    body = RoundedRectangle(width=size, height=size * 0.75, corner_radius=size * 0.1).set_fill(color, 1)
    body.set_stroke(outline_of(color), 3).shift(DOWN * size * 0.2)
    shackle = Arc(radius=size * 0.32, start_angle=0, angle=PI).set_stroke(TEXT, size * 10).move_to(
        body.get_top() + UP * size * 0.16)
    hole = Dot(body.get_center(), radius=size * 0.08).set_fill(INK, 1)
    return VGroup(shackle, body, hole)


def leaf_icon(size=0.6, color=PERS):
    top, tip = np.array([0, -0.5, 0]) * size, np.array([0, 0.5, 0]) * size
    a1 = ArcBetweenPoints(top, tip, angle=1.2)
    a2 = ArcBetweenPoints(tip, top, angle=1.2)
    leaf = VMobject()
    leaf.set_points(np.concatenate([a1.points, a2.points]))
    leaf.set_fill(color, 1).set_stroke(outline_of(color), 3)
    vein = Line(top, tip * 0.8).set_stroke(outline_of(color, 0.3), 2)
    return VGroup(leaf, vein).rotate(-0.5)


def stopwatch_icon(radius=0.5, color=TEXT):
    face = Circle(radius=radius).set_fill(CARD_FILL, 1).set_stroke(color, 4)
    knob = RoundedRectangle(width=radius * 0.35, height=radius * 0.22, corner_radius=0.03).next_to(face, UP, buff=0.02)
    knob.set_fill(color, 1).set_stroke(width=0)
    ticks = VGroup(*[Line(radius * 0.8 * np.array([np.cos(a), np.sin(a), 0]), radius * 0.95 * np.array([np.cos(a), np.sin(a), 0]))
                     for a in np.arange(0, TAU, TAU / 12)]).set_stroke(color, 2)
    hand = Line(ORIGIN, UP * radius * 0.7).set_stroke(CPU_COLOR, 4)
    g = VGroup(face, knob, ticks, hand)
    g.hand = hand
    return g


def ecg_icon(width=2.0, color=OK_GREEN):
    xs = [0, 0.3, 0.38, 0.45, 0.52, 0.6, 1.0]
    ys = [0, 0, 0.12, -0.15, 0.5, 0, 0]
    pts = []
    for rep in range(2):
        for x, y in zip(xs, ys):
            pts.append([(x + rep) * width / 2 - width / 2, y * width * 0.35, 0])
    m = VMobject().set_points_as_corners([np.array(p) for p in pts])
    m.set_stroke(color, 4).set_fill(opacity=0)
    return VGroup(m)


def scroll_icon(width=6.0, height=3.2, color=PAPER):
    sheet = Rectangle(width=width, height=height).set_fill(color, 0.9).set_stroke(darker(color, 0.4), 3)
    rolls = VGroup(*[RoundedRectangle(width=width + 0.4, height=0.3, corner_radius=0.15).move_to(sheet.get_edge_center(d))
                     .set_fill(darker(color, 0.15), 1).set_stroke(darker(color, 0.45), 3) for d in (UP, DOWN)])
    return VGroup(sheet, rolls)


def pipe_glyph(length=1.0, color=DIM):
    tube = RoundedRectangle(width=length, height=0.3, corner_radius=0.15).set_fill(CARD_FILL, 1).set_stroke(color, 3)
    bar = Text("|", font=MONO_FONT, font_size=28, color=TEXT).move_to(tube)
    return VGroup(tube, bar)


def poster_frame(text="A PEACH FOR EVERY PERSON!", width=5.0, color=KERNEL_COLOR):
    t = Text(text, font=FONT, font_size=34, color=TEXT, weight=BOLD)
    if t.width > width - 0.6:
        t.scale_to_fit_width(width - 0.6)
    outer = Rectangle(width=width, height=t.height + 1.0).set_fill(darker(color, 0.55), 0.95).set_stroke(color, 6)
    inner = Rectangle(width=width - 0.2, height=t.height + 0.8).set_fill(opacity=0).set_stroke(USER_COLOR, 3)
    stars = VGroup(*[Star(5, outer_radius=0.15).set_fill(CPU_COLOR, 1).set_stroke(width=0) for _ in range(2)])
    stars[0].next_to(t, LEFT, buff=0.15)
    stars[1].next_to(t, RIGHT, buff=0.15)
    return VGroup(outer, inner, t, stars)


def net_boxes(n=3, spacing=1.4, size=0.5, color=TEXT):
    """``n`` small boxes linked by lines, each with a status light (``[-1]`` = lights)."""
    boxes = VGroup()
    lights = VGroup()
    for i in range(n):
        b = RoundedRectangle(width=size, height=size * 0.8, corner_radius=0.06).set_fill(CARD_FILL, 1).set_stroke(color, 2.5)
        b.move_to([(i - (n - 1) / 2) * spacing, 0, 0])
        boxes.add(b)
        lights.add(Dot(b.get_center(), radius=size * 0.13).set_fill(OK_GREEN, 1))
    links = VGroup(*[Line(boxes[i].get_right(), boxes[i + 1].get_left()).set_stroke(DIM, 2) for i in range(n - 1)])
    g = VGroup(links, boxes, lights)
    return g


def letter_icon(size=0.45, color=PAPER):
    e = Rectangle(width=size, height=size * 0.65).set_fill(color, 1).set_stroke(darker(color, 0.5), 2)
    flap = _poly([e.get_corner(UL), e.get_center() + DOWN * size * 0.05, e.get_corner(UR)], closed=False)
    flap.set_stroke(darker(color, 0.5), 2)
    return VGroup(e, flap)


def chair_icon(size=0.8, color=DIM):
    seat = Line([-0.3, 0, 0], [0.3, 0, 0])
    back = Line([-0.3, 0, 0], [-0.3, 0.6, 0])
    l1 = Line([-0.3, 0, 0], [-0.3, -0.5, 0])
    l2 = Line([0.3, 0, 0], [0.3, -0.5, 0])
    return VGroup(seat, back, l1, l2).set_stroke(color, 5).scale(size)


def bookshelf_icon(width=1.2, color="#A0764B"):
    frame = Rectangle(width=width, height=width * 0.9).set_fill(opacity=0).set_stroke(color, 4)
    shelf = Line(frame.get_left(), frame.get_right()).set_stroke(color, 4)
    books = VGroup()
    cols = ["#6FA8F7", "#F4845F", "#5FC6A8", "#F2CC5B", "#C792EA"]
    for row, y0 in enumerate((frame.get_bottom()[1], frame.get_center()[1])):
        x = frame.get_left()[0] + 0.08
        for k in range(4):
            h = width * (0.32 + 0.05 * ((k + row) % 2))
            b = Rectangle(width=width * 0.14, height=h).set_fill(cols[(k + row) % 5], 1).set_stroke(INK, 1.5)
            b.move_to([x + width * 0.08, y0 + h / 2 + 0.02, 0])
            books.add(b)
            x += width * 0.2
    return VGroup(books, frame, shelf)


def layers_icon(size=0.9, color=TEXT):
    g = VGroup()
    for k in range(3):
        d = Polygon([-0.5, 0, 0], [0, 0.25, 0], [0.5, 0, 0], [0, -0.25, 0]).scale(size)
        d.set_fill(mix(color, BG, 0.3 + 0.2 * k), 1).set_stroke(INK, 2).shift(DOWN * k * size * 0.22)
        g.add(d)
    return VGroup(*reversed(g.submobjects))


def walls_icon(n_walls=2, height=1.0, color="#B0886A"):
    return VGroup(*[RoundedRectangle(width=0.12, height=height, corner_radius=0.04).set_fill(color, 1).set_stroke(outline_of(color), 2)
                    for _ in range(n_walls)])


def hand_icon(size=0.4, color=COMPUTER_COLOR):
    palm = RoundedRectangle(width=size, height=size * 0.6, corner_radius=size * 0.2).set_fill(color, 1).set_stroke(outline_of(color), 2)
    arm = Rectangle(width=size * 0.35, height=size * 0.9).next_to(palm, DOWN, buff=-0.02).set_fill(color, 1).set_stroke(outline_of(color), 2)
    return VGroup(arm, palm)


def name_tag(text, font_size=22, color="#FFFFFF"):
    t = Text(text, font=FONT, font_size=font_size, color=INK, weight=BOLD)
    hdr = Text("HELLO, I'M", font=FONT, font_size=font_size * 0.55, color="#FFFFFF", weight=BOLD)
    r = RoundedRectangle(width=max(t.width, hdr.width) + 0.3, height=t.height + hdr.height + 0.35, corner_radius=0.06)
    r.set_fill(color, 1).set_stroke(KERNEL_COLOR, 3)
    band = Rectangle(width=r.width, height=hdr.height + 0.12).align_to(r, UP).set_fill(KERNEL_COLOR, 1).set_stroke(width=0)
    hdr.move_to(band)
    t.move_to(r.get_center() + DOWN * (hdr.height + 0.06) / 2)
    return VGroup(r, band, hdr, t)


def money_meter(label="$$$ / hour", width=1.6):
    box = RoundedRectangle(width=width, height=0.55, corner_radius=0.08).set_fill(CARD_FILL, 1).set_stroke(CPU_COLOR, 2.5)
    t = Text(label, font=MONO_FONT, font_size=20, color=CPU_COLOR).move_to(box)
    return VGroup(box, t)


def loop_arrow(radius=0.35, color=BAD_RED):
    a = Arc(radius=radius, start_angle=PI / 2, angle=-1.7 * PI).set_stroke(color, 5)
    a.add_tip(tip_length=0.16)
    a.tip.set_fill(color, 1).set_stroke(color)
    return VGroup(a)
