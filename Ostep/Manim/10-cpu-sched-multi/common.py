"""Episode 10 (Multiprocessor Scheduling): constants, helpers and state builders.

Every scene starts from a builder here so scenes can be rendered independently and still
match the previous scene's "Ends with" state.
"""
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_ROOT = _HERE.parents[2]
for _p in (str(_ROOT), str(_HERE)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import numpy as np  # noqa: E402
from manim import *  # noqa: E402,F401,F403
from ostep_lib import *  # noqa: E402,F401,F403
from ostep_lib.props.p04_timeline import Timeline  # noqa: E402,F401
from ostep_lib.props.p04_queue import Queue  # noqa: E402
from ostep_lib.props.p04_icons import mix, hatch_rect, IDLE_GREY  # noqa: E402
from ostep_lib.props.core import INK, CARD_FILL, outline_of  # noqa: E402
from ostep_lib.props.p04_icons import *  # noqa: E402,F401,F403
from ostep_lib.props.p07_padlock import Padlock  # noqa: E402
from ostep_lib.props.p10_cache import CacheCPU, ScheduleGrid, bus_pulse  # noqa: E402
from ostep_lib.props.p10_eye import EyeIcon  # noqa: E402
from ostep_lib.props.p10_icons import suitcase_icon, pin_icon, flame_icon, hand_up_icon  # noqa: E402

# ---------------------------------------------------------------------------
# Persistent assignments
# ---------------------------------------------------------------------------
COL = {"A": PROCESS_COLORS[0], "B": PROCESS_COLORS[1], "C": PROCESS_COLORS[2], "D": PROCESS_COLORS[3],
       "E": PROCESS_COLORS[4]}
GREEN_OK = "#8BE07A"
CHAR_SCALE = 0.75
STUDENT_CORNER = np.array([-5.8, -2.8, 0.0])
PROF_CORNER = np.array([5.8, -2.8, 0.0])
BADGE_TEXT = "10 · Multi-CPU Scheduling"
CRUX_Q = "How to schedule jobs on multiple CPUs?"
CRUX_SUB = "What new problems arise? Do the same old techniques work, or are new ideas required?"
CRUX2_Q = "How to deal with load imbalance?"
CRUX2_SUB = ("How should a multi-queue multiprocessor scheduler handle load imbalance, "
             "so as to better achieve its desired scheduling goals?")
STRIP_Y = 3.0


def P3(x, y=0.0):
    return np.array([float(x), float(y), 0.0])


def proc(name, expr="ready", scale=1.0, color=None, label=None):
    p = Process(expr, color=color or COL.get(name, PROCESS_COLORS[4]), label=name if label is None else label)
    if scale != 1.0:
        p.scale(scale)
    return p


def student_corner(expr="neutral"):
    return Student(expr).scale(CHAR_SCALE).move_to(STUDENT_CORNER)


def prof_corner(expr="neutral"):
    return Professor(expr).scale(CHAR_SCALE).flip().move_to(PROF_CORNER)


def label(text, size=24, color=TEXT, **kw):
    return Text(text, font_size=size, color=color, **kw)


def mono(text, size=22, color=TEXT):
    return Text(text, font=MONO_FONT, font_size=size, color=color)


def make_badge():
    return SectionBadge(BADGE_TEXT, accent=VIRT)


def crux_strip_mobs(second=False):
    card = CruxCard(CRUX2_Q if second else CRUX_Q, accent=VIRT)
    st = card.strip((0, STRIP_Y, 0), 24)
    return VGroup(st[0], st[2])


def tag(text, size=20, color=DIM, stroke=None):
    """A small rounded text tag."""
    t = Text(text, font_size=size, color=color)
    r = RoundedRectangle(width=t.width + 0.3, height=t.height + 0.22, corner_radius=0.1)
    r.set_fill(CARD_FILL, 1).set_stroke(stroke or color, 1.5)
    return VGroup(r, t.move_to(r))


def mini_chip(lit=False, size=0.32):
    c = CPU(size=size, label=None, pins=2, color=CPU_COLOR if lit else mix(CPU_COLOR, BG, 0.78))
    return c


def cpu_at(x, y_chip, name, size=1.2):
    """A CacheCPU whose chip centre is at (x, y_chip)."""
    c = CacheCPU(name, size=size)
    c.shift(P3(x, y_chip) - c.cpu.get_center())
    # strip and cells sit below their texts even when an Indicate/pulse re-adds them to the scene
    for m in (c.strip, *c.cells):
        m.set_z_index(-1)
    for t in (c.cache_label, *c.texts):
        t.set_z_index(6)
    return c


def stopwatch(text, size=26, color=TEXT, radius=0.3):
    sw = stopwatch_icon(radius=radius)
    t = mono(text, size, color)
    t.next_to(sw, RIGHT, buff=0.15)
    g = VGroup(sw, t)
    g.sw, g.txt = sw, t
    return g


def on_chip(p, cc, outline=True):
    """Instantly seat process ``p`` on a CacheCPU (or CPU) chip."""
    chip = cc.cpu if hasattr(cc, "cpu") else cc
    place_on(p, chip.slot_point())
    return p


def hop_on(p, cc, **kw):
    chip = cc.cpu if hasattr(cc, "cpu") else cc
    return hop_to(p, chip.slot_point(), **kw)


class Ep10Scene(NarratedScene):
    def setup(self):
        super().setup()
        self.terms = TermHighlight(accent=VIRT)

    def term(self, text, **kw):
        return self.terms.show(text, **kw)

    def note(self, text, **kw):
        return self.terms.note(text, **kw)

    def on_trays(self, procs, queues):
        """Jobs walking through a queue tray: the letter under their feet crosses the tray border."""
        for p in procs:
            for q in queues:
                self.allow_overlap(p, q.tray, "a job hops onto / off its slot on the tray")

    def add_docked(self, text):
        m = self.terms.docked_now(text)
        self.add(m)
        self._docked_m = m
        return m

    def fade_stage(self, *keep, run_time=0.8, extra=()):
        """Fade out everything except the chrome (badge, strip, hosts, docked term) and ``keep``;
        ``extra`` animations play along.  Looks inside scene-level groups so a kept mobject that a
        play() nested in a group is not faded with it."""
        chrome = [getattr(self, n, None) for n in ("badge", "strip", "stu", "prof", "_docked_m")]
        kept = {id(k) for k in (*chrome, *keep) if k is not None}
        gone = []

        def collect(m):
            if id(m) in kept or getattr(m, "is_scrim", False):
                return
            if any(id(x) in kept for x in m.get_family()[1:]):
                for s in m.submobjects:
                    collect(s)
            else:
                gone.append(m)
        for m in self.mobjects:
            collect(m)
        if gone or extra:
            self.play(*[FadeOut(m) for m in gone], *extra, run_time=run_time)

    def world(self, term=None, stu="neutral", prof="neutral", strip=0, badge=True, chars=True):
        """Badge, crux strip (0 none, 1 first, 2 second), corner characters, docked term."""
        if badge:
            self.badge = make_badge()
            self.add(self.badge)
        if strip:
            self.strip = crux_strip_mobs(strip == 2)
            self.add(self.strip)
        if chars:
            self.stu, self.prof = student_corner(stu), prof_corner(prof)
            self.add(self.stu, self.prof)
        if term:
            self.add_docked(term)


# ---------------------------------------------------------------------------
# Small pictures
# ---------------------------------------------------------------------------
def desk_icon(size=1.0):
    top = Rectangle(width=size, height=size * 0.12).set_fill("#8A6A44", 1).set_stroke("#5E4630", 2)
    legs = VGroup(*[Rectangle(width=size * 0.08, height=size * 0.4).set_fill("#8A6A44", 1).set_stroke("#5E4630", 2)
                    for _ in range(2)])
    legs[0].next_to(top, DOWN, buff=0, aligned_edge=LEFT).shift(RIGHT * size * 0.06)
    legs[1].next_to(top, DOWN, buff=0, aligned_edge=RIGHT).shift(LEFT * size * 0.06)
    books = VGroup(*[Rectangle(width=size * 0.12, height=size * h).set_fill(c, 1).set_stroke(INK, 1.5)
                     for h, c in ((0.3, "#E06C75"), (0.36, "#61AFEF"), (0.26, "#98C379"))])
    books.arrange(RIGHT, buff=0.01, aligned_edge=DOWN).next_to(top, UP, buff=0).shift(LEFT * size * 0.2)
    return VGroup(legs, top, books)


def library_icon(size=1.6):
    body = Rectangle(width=size, height=size * 0.55).set_fill("#6B6F7A", 1).set_stroke(INK, 2)
    roof = Triangle().scale_to_fit_width(size * 1.15).set_fill("#8A8F9C", 1).set_stroke(INK, 2)
    roof.stretch_to_fit_height(size * 0.28).next_to(body, UP, buff=0)
    cols = VGroup(*[Rectangle(width=size * 0.08, height=size * 0.45).set_fill("#C9CBD2", 1).set_stroke(width=0)
                    for _ in range(4)]).arrange(RIGHT, buff=size * 0.15).move_to(body)
    return VGroup(body, roof, cols)


def x_flash(point, size=0.3):
    return x_mark(size).move_to(point)


def ok_tick(point, size=0.3):
    return tick_mark(size).move_to(point)


def aside_card(body, title=None, width=4.4, font_size=22, icon=None):
    return AsideCard(body, title=title, width=width, font_size=font_size)


# ---------------------------------------------------------------------------
# S01 world
# ---------------------------------------------------------------------------
def build_laptop():
    lap = Laptop(5.0, fill_opacity=0.0).move_to(P3(0, 0.3))
    sc = lap.screen_center()
    xs = [(-1.575 + 0.45 * i) for i in range(8)]
    chips = VGroup(*[mini_chip(False).move_to(P3(x, sc[1])) for x in xs])
    return lap, chips


def build_s01_end():
    """Laptop with eight chips (first lit with a coral A), stopwatch 1x, Student sad, Prof, Computer."""
    lap, chips = build_laptop()
    lit = mini_chip(True).move_to(chips[0])
    chips[0].become(lit)
    a = proc("A", "running", 0.3)
    place_on(a, chips[0].get_top() + DOWN * 0.05)
    sw = stopwatch("1× speed", 24).move_to(P3(4.3, 0.3))
    stu, prof = student_corner("sad"), prof_corner("neutral")
    comp = Computer("idle").scale(0.35).move_to(P3(0, -2.6))
    return dict(lap=lap, chips=chips, a=a, sw=sw, stu=stu, prof=prof, comp=comp)
