"""Episode 11 (Summary Dialogue on CPU Virtualization): constants, builders and the scene base."""
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

COL = {"A": PROCESS_COLORS[0], "B": PROCESS_COLORS[1], "C": PROCESS_COLORS[2], "D": PROCESS_COLORS[3]}
GREEN_OK = "#8BE07A"
BADGE_TEXT = "11 · Summary Dialogue"
CHAR_SCALE = 0.75
STUDENT_CORNER = np.array([-5.8, -2.8, 0.0])
PROF_CORNER = np.array([5.8, -2.8, 0.0])
STUDENT_DLG = np.array([-2.6, -1.2, 0.0])
PROF_DLG = np.array([2.6, -1.2, 0.0])
RED = "#E5534B"


def P3(x, y=0.0):
    return np.array([float(x), float(y), 0.0])


def proc(name, expr="ready", scale=1.0, color=None, label=None):
    p = Process(expr, color=color or COL.get(name, PROCESS_COLORS[4]), label=label)
    if scale != 1.0:
        p.scale(scale)
    return p


def bottom_to(mob, point):
    mob.shift(np.array(point, dtype=float) - mob.get_bottom())
    return mob


def feet_to(mob, point):
    """Instantly put a Process's base point (feet) on ``point``."""
    place_on(mob, np.array(point, dtype=float))
    return mob


def student_corner(expr="neutral"):
    return Student(expr).scale(CHAR_SCALE).move_to(STUDENT_CORNER)


def prof_corner(expr="neutral"):
    return Professor(expr).scale(CHAR_SCALE).flip().move_to(PROF_CORNER)


def student_dlg(expr="neutral"):
    return Student(expr).move_to(STUDENT_DLG)


def prof_dlg(expr="neutral"):
    return Professor(expr).flip().move_to(PROF_DLG)


def label(text, size=24, color=TEXT, **kw):
    return Text(text, font_size=size, color=color, **kw)


def make_badge():
    return SectionBadge(BADGE_TEXT, accent=VIRT)


# ---------------------------------------------------------------------------
# Scene base
# ---------------------------------------------------------------------------
class Ep11Scene(NarratedScene):
    def setup(self):
        super().setup()
        self.terms = TermHighlight(accent=VIRT)

    def term(self, text, **kw):
        return self.terms.show(text, **kw)

    def add_docked(self, text):
        m = self.terms._make(text, self.terms.dock_size, self.terms.accent, self.terms.dock_at, right_aligned=True)
        self.terms.docked = m
        self.add(m)
        return m

    def world(self, stu="neutral", prof="neutral", mode="corner", badge=True, term=None):
        if badge:
            self.badge = make_badge()
            self.add(self.badge)
        if mode == "corner":
            self.stu, self.prof = student_corner(stu), prof_corner(prof)
        else:
            self.stu, self.prof = student_dlg(stu), prof_dlg(prof)
        self.add(self.stu, self.prof)
        if term:
            self.add_docked(term)


# ---------------------------------------------------------------------------
# S02 / S03 panels: boundary, CPU + clock, save slot
# ---------------------------------------------------------------------------
PANEL_Y = 0.8
PX = (-3.2, 0.0, 3.2)


def build_panels():
    """Three unframed mini panels (centered on y=0.8) as one VGroup:
    [boundary_panel, cpu_panel, slot_panel]; each has named parts."""
    # left: user/kernel boundary
    bd = UserKernelBoundary(y=PANEL_Y, x_range=(PX[0] - 1.3, PX[0] + 1.3), top=PANEL_Y + 1.5, bottom=PANEL_Y - 1.3,
                            label_x=PX[0] - 1.25, label_size=16)
    p_user = proc("A", "running", scale=0.5, label=None)
    feet_to(p_user, P3(PX[0] + 0.5, PANEL_Y + 0.35))
    left = VGroup(bd, p_user)
    left.bd, left.proc = bd, p_user
    # middle: CPU + clock
    cpu = CPU(size=1.0).move_to(P3(PX[1], PANEL_Y - 0.1))
    pa = proc("A", "running", scale=0.55, label=None)
    feet_to(pa, cpu.slot_point())
    clock = ClockIcon(radius=0.3).move_to(P3(PX[1] + 1.2, PANEL_Y + 0.55))
    mid = VGroup(cpu, pa, clock)
    mid.cpu, mid.proc, mid.clock = cpu, pa, clock
    # right: save slot
    slot = save_slot(0.8).move_to(P3(PX[2], PANEL_Y - 0.3))
    pa2 = proc("A", "ready", scale=0.4, label=None)
    pb2 = proc("B", "ready", scale=0.4, label=None)
    feet_to(pa2, P3(PX[2] - 0.75, PANEL_Y - 0.6))
    feet_to(pb2, P3(PX[2] + 0.75, PANEL_Y - 0.6))
    right = VGroup(slot, pa2, pb2)
    right.slot, right.pa, right.pb = slot, pa2, pb2
    panels = VGroup(left, mid, right)
    panels.left, panels.mid, panels.right = left, mid, right
    return panels


def build_panels_end():
    """The panels exactly as S02 ends (trap label, A off the CPU, B on it, save/restore tag)."""
    panels = build_panels()
    L, M, R = panels.left, panels.mid, panels.right
    L.add(label("trap handler", 18, KERNEL_COLOR).move_to(P3(PX[0] + 0.3, PANEL_Y - 1.1)))
    feet_to(M.proc, P3(PX[1] - 1.05, PANEL_Y - 0.45))
    rb = R.pb
    feet_to(rb, M.cpu.slot_point())
    M.add(rb)
    R.remove(rb)
    arrow = DoubleArrow(P3(PX[2] - 0.45, PANEL_Y - 0.95), P3(PX[2] + 0.45, PANEL_Y - 0.95), buff=0, tip_length=0.12)
    arrow.set_stroke(DIM, 3)
    R.add(arrow, label("save / restore", 18, DIM).next_to(arrow, DOWN, buff=0.08))
    return panels


def build_s03_end(scene):
    """Terminal with three ticks + shrunken panels (as S03 ends)."""
    panels = build_panels_end()
    panels.scale(0.5).move_to(P3(0, 1.85))
    term = Terminal(width=5.2, height=2.6, font_size=18, prompt="$").move_to(P3(0, -0.15))
    scene.add(term)
    scene.play(term.type("make test"), run_time=0.05)
    for name in ("trap handler ... ok", "timer ... ok", "switch ... ok"):
        scene.play(term.print(name), run_time=0.05)
        tick = tick_mark(0.18, GREEN_OK, 5).next_to(term.last_line(), RIGHT, buff=0.15)
        term.add(tick)
    return panels, term


# S04 world
BOUND_Y = 0.4
CPU_AT = P3(-2.2, 1.15)
GAUGE_AT = P3(5.4, 1.5)


def make_boundary():
    return UserKernelBoundary(y=BOUND_Y, x_range=(-6.6, 6.6), top=2.5, bottom=-2.0, label_x=-6.4, label_size=20)


def make_stack():
    st = SystemStack()
    procs = VGroup(*[proc(n, "ready", scale=0.6, label=None) for n in "ABC"])
    for i, p in enumerate(procs):
        feet_to(p, st.program_point(i))
    return st, procs


def build_s04_end():
    bd = make_boundary()
    bd.set_opacity(0.3)
    gauge = PrivilegeGauge(height=1.3, level="user")
    gauge.move_to(GAUGE_AT)
    st, procs = make_stack()
    puzzle = puzzle_piece(0.5).move_to(P3(4.2, -0.9))
    return bd, gauge, st, procs, puzzle


# S05 checkout world
Q_CENTER = P3(0.6, -0.3)
COUNTER_AT = P3(-3.9, -0.45)


def hop_mover(mob, bottom_point, run_time=0.6):
    target = np.array(bottom_point, dtype=float) + (mob.get_center() - mob.get_bottom())
    return hop_to(mob, target, anchor="center", run_time=run_time)


def job_item(name, scale, tag, expr="ready"):
    p = proc(name, expr, scale=scale, label=None)
    t = label(tag, 20, DIM).next_to(p, UP, buff=0.05)
    return VGroup(p, t)


def make_counter():
    desk = RoundedRectangle(width=1.4, height=0.8, corner_radius=0.1).set_fill(CARD_FILL, 1).set_stroke(DIM, 3)
    card = RoundedRectangle(width=0.4, height=0.3, corner_radius=0.05).set_fill(DIM, 1).set_stroke(TEXT, 2)
    card.next_to(desk, UP, buff=0.0).shift(RIGHT * 0.3)
    return VGroup(desk, card).move_to(COUNTER_AT)


def make_checkout_queue():
    q = Queue(label="Checkout", center=tuple(Q_CENTER), slots=3, spacing=1.5, mover=hop_mover)
    A = job_item("A", 0.9, "long")
    B = job_item("B", 0.6, "short")
    q.place(A, B)
    return q, A, B


def make_mini_timeline():
    return Timeline(["A", "B"], ticks=8, colors=[COL["A"], COL["B"]], x_range=(-2.6, 2.6), top=-1.55,
                    row_height=0.3, row_step=0.42, tick_labels=False, label_font=20)


def build_s05_end():
    """Static replica of S05's end state (queue, A at the counter, B waiting, spotlight dimmed)."""
    q, A, B = make_checkout_queue()
    q.items = [B]
    q.remove_item(A)
    q._snap(B, 0)
    counter = make_counter()
    A.move_to(P3(-2.5, COUNTER_AT[1]) + (A.get_center() - A.get_bottom()))
    A[0].set_expression("blocked")
    spot = Spotlight(height=1.4, spread=0.5).move_to(P3(0.6, 1.9)).set_opacity(0.3)
    return VGroup(q, A, B, counter, spot)


MLFQ_X = (-4.0, 0.4)


def make_ladder():
    return MLFQLadder(levels=3, labels=["Q2", "Q1", "Q0"], x_range=MLFQ_X, arrows=False)


def build_s06_end():
    """Static replica of S06's end state: ladder with C in Q0, three tags, censored BFS, thumbs-up."""
    ladder = make_ladder()
    C = proc("C", "running", scale=0.6, label=None)
    ladder.place(C, 0)
    tags = VGroup(name_tag("CFS", 22), name_tag("BFS", 22), name_tag("O(1)", 22))
    tags[0].move_to(P3(2.7, 1.6)); tags[1].move_to(P3(3.7, 0.5)); tags[2].move_to(P3(4.9, 1.6))
    lines = VGroup(*[Line(ORIGIN, RIGHT * w).set_stroke(DIM, 6) for w in (2.0, 1.7, 2.1)]).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
    lines.move_to(P3(3.7, -0.5))
    bar = censor_bar(2.4, 0.9).move_to(lines)
    return VGroup(ladder, C, tags, lines, bar)


def sched_strip(rows, x0, top, cw=0.36, ch=0.22, gap=0.1, names="ABC"):
    """Mini schedule strip. rows: strings of 'r' (running), 'w' (ready outline), '.' (idle)."""
    out = VGroup()
    labels = VGroup()
    for i, row in enumerate(rows):
        y = top - i * (ch + gap)
        c = COL[names[i]]
        cells = VGroup()
        for j, ch_ in enumerate(row):
            r = Rectangle(width=cw, height=ch).move_to(P3(x0 + cw / 2 + j * cw, y))
            if ch_ == "r":
                r.set_fill(c, 1).set_stroke(TEXT, 1)
            elif ch_ == "w":
                r.set_fill(c, 0.0).set_stroke(c, 2)
            else:
                r.set_fill(DIM, 0.08).set_stroke(DIM, 0.8)
            cells.add(r)
        out.add(cells)
        labels.add(label(names[i], 16, DIM).move_to(P3(x0 - 0.2, y)))
    out.labels = labels
    return VGroup(labels, out)


def build_s07_end():
    """Static replica of S07's end state: level seesaw with ring, RR strips, Lampson card."""
    see = Seesaw(width=3.2, left="turnaround", right="response").move_to(P3(-1.6, 1.1))
    ring = Circle(radius=0.4, color=GREEN_OK).set_stroke(GREEN_OK, 4).move_to(see.pivot.get_center() + DOWN * 0.2)
    ls, rs = sched_strip(["rwwrww", "wrwwrw", "wwrwwr"], -4.0, -0.2), sched_strip(["rwwrww", "wrwwrw", "wwrwwr"], -1.2, -0.2)
    card = TipCard(body="Don't find the best. Avoid disaster.", title="LAMPSON", width=3.4, font_size=24,
                   accent=VIRT).move_to(P3(4.2, 0.9))
    return VGroup(see, ring, ls, rs, card)
