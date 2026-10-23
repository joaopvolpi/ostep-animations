"""Episode 09 (Scheduling: Proportional Share): constants, helpers and state builders."""
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
from ostep_lib.props.p04_timeline import Timeline  # noqa: E402
from ostep_lib.props.p04_queue import Queue  # noqa: E402
from ostep_lib.props.p04_icons import *  # noqa: E402,F401,F403
from ostep_lib.props.p05_code import CodeWalker  # noqa: E402
from ostep_lib.props.p09_drum import *  # noqa: E402,F401,F403
from ostep_lib.props.p09_props import *  # noqa: E402,F401,F403
from ostep_lib.props.p09_icons import *  # noqa: E402,F401,F403

COL = {"A": PROCESS_COLORS[0], "B": PROCESS_COLORS[1], "C": PROCESS_COLORS[2], "D": PROCESS_COLORS[3]}
GREEN_OK = "#8BE07A"
CHAR_SCALE = 0.75
STUDENT_CORNER = np.array([-5.8, -2.8, 0.0])
PROF_CORNER = np.array([5.8, -2.8, 0.0])
STU_DIALOGUE = np.array([-2.6, -1.2, 0.0])
PROF_DIALOGUE = np.array([2.6, -1.2, 0.0])
BADGE_TEXT = "09 · Proportional Share"
CRUX_Q = "How to share the CPU proportionally?"
CRUX_SUB = "What are the key mechanisms for doing so? How effective are they?"
INK_DARK = "#1C1C1C"
TARGET_AT = np.array([6.2, 2.0, 0.0])     # the small target pie (below the chrome rows)


def P3(x, y=0.0):
    return np.array([float(x), float(y), 0.0])


def feet_for_bottom(mob, point):
    return np.array(point, dtype=float) + (base_point(mob) - mob.get_bottom())


def hop_bottom(p, point, **kw):
    return hop_to(p, feet_for_bottom(p, point), **kw)


def proc(name, expr="ready", scale=1.0, color=None, label=None):
    p = Process(expr, color=color or COL.get(name, PROCESS_COLORS[4]), label=name if label is None else label)
    if scale != 1.0:
        p.scale(scale)
    return p


def student_corner(expr="neutral"):
    return Student(expr).scale(CHAR_SCALE).move_to(STUDENT_CORNER)


def prof_corner(expr="neutral"):
    return Professor(expr).scale(CHAR_SCALE).flip().move_to(PROF_CORNER)


def lab(text, size=22, color=TEXT, **kw):
    return Text(text, font_size=size, color=color, **kw)


def mono(text, size=20, color=TEXT):
    return Text(text, font_size=size, color=color, font=MONO_FONT)


def make_badge():
    return SectionBadge(BADGE_TEXT, accent=VIRT)


def crux_strip_mobs():
    card = CruxCard(CRUX_Q, CRUX_SUB, accent=VIRT)
    st = card.strip((0, 3.0, 0), 24)
    return VGroup(st[0], st[2])


def target_pie(label="target"):
    return TargetPie((0.75, 0.25), radius=0.4, label=label, font_size=18).move_to(TARGET_AT)


def card_rect(w, h, color=DIM, fill=CARD_FILL):
    return RoundedRectangle(width=w, height=h, corner_radius=0.12).set_fill(fill, 1).set_stroke(color, 2.5)


def caption_at(text, y=-2.9, size=26, color=TEXT):
    return Text(text, font_size=size, color=color).move_to(P3(0, y))


def token(text, color, size=22, w=None):
    """A small rounded text badge."""
    t = Text(text, font_size=size, color=color)
    r = RoundedRectangle(width=(w or t.width + 0.35), height=t.height + 0.22, corner_radius=0.1) \
        .set_fill(CARD_FILL, 1).set_stroke(color, 2)
    t.move_to(r)
    return VGroup(r, t)


# the 20 draws of S04 (book's output): who ran each slice
DRAWS = [(63, "A"), (85, "B"), (70, "A"), (39, "A"), (76, "B")]
REST = list("ABAABAAAAAABABAAAAAA")[5:]          # 15 remaining slices
REST_NUMS = [17, 29, 41, 36, 39, 10, 99, 68, 83, 63, 62, 43, 0, 49, 12]
RUN20 = [w for _, w in DRAWS] + REST
assert len(RUN20) == 20


class Ep09Scene(NarratedScene):
    def setup(self):
        super().setup()
        self.terms = TermHighlight(accent=VIRT)

    def tear_down(self):
        super().tear_down()

    KEY_TERMS = ("proportional share", "lottery scheduling", "stride scheduling", "vruntime")

    def term(self, text, **kw):
        """Key terms (the 4 the episode hinges on) get the veil; every other term slides in with note()."""
        if text in self.KEY_TERMS:
            return self.terms.show(text, **kw)
        return self.terms.note(text)

    def add_docked(self, text):
        m = self.terms._make(text, self.terms.dock_size, self.terms.accent, self.terms.dock_at, right_aligned=True)
        self.terms.docked = m
        self.add(m)
        return m

    def world(self, term=None, stu="neutral", prof="neutral", strip=True, badge=True, chars=True, pie=False):
        """Badge, crux strip, corner characters (and a docked term / target pie)."""
        if badge:
            self.badge = make_badge()
            self.add(self.badge)
        if strip:
            self.strip = crux_strip_mobs()
            self.add(self.strip)
        if chars:
            self.stu, self.prof = student_corner(stu), prof_corner(prof)
            self.add(self.stu, self.prof)
        if term:
            self.add_docked(term)
        if pie:
            self.pie = target_pie()
            self.add(self.pie)


# ---------------------------------------------------------------------------
# State builders ("Starts with")
# ---------------------------------------------------------------------------
def build_s01_end():
    rack = server_rack_icon(1.0, 1.8).scale(1.1).move_to(P3(0, 0.9))
    chip = CPU(size=0.42, label="", pins=3).move_to(rack.get_center() + UP * 0.1)
    a, b = proc("A", scale=0.6).move_to(P3(-3.4, 2.1)), proc("B", scale=0.6).move_to(P3(-3.4, 0.5))
    pie = TargetPie((0.75, 0.25), radius=1.0, label=None).move_to(P3(3.4, 1.0))
    l75 = Text("75%", font_size=26, color=INK_DARK).move_to(P3(3.4, 1.0) + P3(-0.35, -0.2))
    l25 = Text("25%", font_size=26, color=INK_DARK).move_to(P3(3.4, 1.0) + P3(0.42, 0.45))
    stu = Student("confused").move_to(STU_DIALOGUE + DOWN * 0.0)
    prof = Professor("happy").flip().move_to(PROF_DIALOGUE + DOWN * 0.0)
    chips = VGroup(*[sched_chip(n, 0.95, 0.46).move_to(P3(x, -3.0)).set_opacity(0.3)
                     for n, x in (("RR", -1.2), ("SJF", 0.0), ("MLFQ", 1.25))])
    tags = VGroup(*[Text(t, font_size=18, color=DIM).next_to(c, UP, buff=0.08).set_opacity(0.3)
                    for t, c in zip(("turnaround", "response", "guess"), chips)])
    drum = RaffleDrum(1.4).move_to(P3(5.6, -0.6))
    return dict(rack=rack, chip=chip, a=a, b=b, pie=pie, l75=l75, l25=l25, stu=stu, prof=prof, chips=chips,
                tags=tags, drum=drum)


# S03/S04 world geometry
CPU3_AT = P3(0, 1.2)
STRIP3_Y = -0.6
A3_AT, B3_AT = P3(-5.0, 1.2), P3(5.0, 1.2)


def build_s03_world():
    """The lottery world (S03 final state): CPU, drum, A/B with stacks, strip, marker at 63."""
    cpu = CPU(size=1.1, label="CPU").move_to(CPU3_AT)
    drum = RaffleDrum(1.1).move_to(P3(-2.0, 1.2))
    a = proc("A", scale=0.7).move_to(A3_AT)
    b = proc("B", scale=0.7).move_to(B3_AT)
    sa = TicketStack(75, COL["A"]).move_to(P3(-3.8, 1.3))
    sb = TicketStack(25, COL["B"]).move_to(P3(3.8, 1.3))
    strip = NumberStrip(100, [("A", 75, COL["A"]), ("B", 25, COL["B"])], x_range=(-5, 5), y=STRIP3_Y,
                        ticks=None)
    return dict(cpu=cpu, drum=drum, a=a, b=b, sa=sa, sb=sb, strip=strip)


def strip_labels(strip):
    out = VGroup()
    for n, y in ((0, None), (74, None), (75, None), (99, None)):
        pass
    for n, dx in ((0, 0.0), (74, -0.0), (75, 0.0), (99, 0.0)):
        t = Text(str(n), font_size=18, color=DIM)
        x = strip.x_of(n if n in (0, 99) else n)
        if n == 99:
            x = strip.x_of(100) - 0.1
        if n == 74:
            x = strip.x_of(75) - 0.25
        if n == 75:
            x = strip.x_of(75) + 0.25
        t.move_to(P3(x, strip.y - 0.4))
        out.add(t)
    return out


def glide(mob, p1, run_time=0.6, rate=None):
    """Move ``mob`` (center) to ``p1``; safe inside Succession (start point read at begin)."""
    st = {}
    p1 = np.array(p1, dtype=float)

    def f(m, al):
        if "p0" not in st:
            st["p0"] = m.get_center().copy()
        m.move_to(st["p0"] + (p1 - st["p0"]) * al)

    return UpdateFromAlphaFunc(mob, f, run_time=run_time, rate_func=rate or rate_functions.smooth)
