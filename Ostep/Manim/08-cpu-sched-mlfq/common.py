"""Episode 08 (Scheduling: the Multi-Level Feedback Queue): constants, helpers and state builders.

Every scene starts from ``Ep08Scene.build(...)`` so scenes render independently and still match
the previous scene's "Ends with" state.
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
from ostep_lib.props.p04_timeline import Timeline  # noqa: E402
from ostep_lib.props.p04_queue import Queue  # noqa: E402
from ostep_lib.props.p04_icons import *  # noqa: E402,F401,F403

COL = {"A": PROCESS_COLORS[0], "B": PROCESS_COLORS[1], "C": PROCESS_COLORS[2], "D": PROCESS_COLORS[3]}
GREEN_OK = "#8BE07A"
CHAR_SCALE = 0.75
STUDENT_CORNER = np.array([-6.1, -2.8, 0.0])
PROF_CORNER = np.array([5.8, -2.8, 0.0])
STUDENT_DLG = np.array([-2.6, -1.2, 0.0])
PROF_DLG = np.array([2.6, -1.2, 0.0])
BADGE_TEXT = "08 · MLFQ"
CRUX_Q = "How to schedule without perfect knowledge?"
CRUX_SUB = "Low response time for interactive jobs, low turnaround time, and no a priori knowledge of job length."
CPU_AT = np.array([2.0, 0.95, 0.0])
BLOCK_SPOT = np.array([0.85, 0.8, 0.0])    # where a blocked job waits (feet point)
BLOCK_AT = np.array([0.85, 1.95, 0.0])     # its clock icon
TL_X = (-4.4, 3.0)

RULES = {
    "R1": "If Priority(A) > Priority(B), A runs.",
    "R2": "Equal priority? Round robin.",
    "R3": "A new job enters at the top queue.",
    "R4a": "Used its allotment? Move down one queue.",
    "R4b": "Gave up the CPU early? Stay put; allotment resets.",
    "R4": "Allotment spent at a level? Move down.",
    "R5": "After a period S, move all jobs to the top queue.",
}


def P3(x, y=0.0):
    return np.array([float(x), float(y), 0.0])


def student_corner(expr="neutral"):
    return Student(expr).scale(CHAR_SCALE).move_to(STUDENT_CORNER)


def prof_corner(expr="neutral"):
    return Professor(expr).scale(CHAR_SCALE).flip().move_to(PROF_CORNER)


def student_dlg(expr="neutral"):
    return Student(expr).move_to(STUDENT_DLG)


def prof_dlg(expr="neutral"):
    return Professor(expr).flip().move_to(PROF_DLG)


def label(text, size=22, color=TEXT, **kw):
    return Text(text, font_size=size, color=color, **kw)


def make_tl(ticks=20, unit="ms"):
    """The level-versus-time chart: rows Q2/Q1/Q0, one tick = 10 ms."""
    return Timeline(["Q2", "Q1", "Q0"], ticks=ticks, colors=[TEXT] * 3, x_range=TL_X, top=-0.9,
                    row_height=0.45, row_step=0.6, label_mode="boundary", unit_per_tick=10,
                    label_every=5 if ticks <= 20 else 10, unit=unit, tick_label_y=-2.62, label_font=22, tick_font=16)


def job(name, scale=0.6, expr="ready", label_text=None):
    p = Process(expr, color=COL.get(name, PROCESS_COLORS[4]), label=name if label_text is None else label_text)
    p.scale(scale)
    return p


def cell_run(tl, row, tick, name, run_time=0.3):
    return tl.fill(row, tick, "running", color=COL[name], run_time=run_time)


def set_cells(tl, spec):
    """spec: list of (row, tick, name) placed instantly."""
    for row, tick, name in spec:
        tl.set_block(row, tick, "running", color=COL[name])
    return tl


FIG82 = [("Q2", 1, "A"), ("Q1", 2, "A")] + [("Q0", t, "A") for t in range(3, 21)]


def fig83_left():
    """Figure 8.3 (left): A sinks, B arrives at 100 ms and runs 20 ms at Q2/Q1, A resumes."""
    return ([("Q2", 1, "A"), ("Q1", 2, "A")] + [("Q0", t, "A") for t in range(3, 11)]
            + [("Q2", 11, "B"), ("Q1", 12, "B")] + [("Q0", t, "A") for t in range(13, 21)])


class SetExpr(Animation):
    """Instantly switch a character's expression when it starts (no cross-fade ghost labels)."""

    def __init__(self, mob, expr, **kw):
        kw.setdefault("run_time", 0.02)
        super().__init__(mob, **kw)
        self.expr = expr

    def begin(self):
        self.mobject.set_expression(self.expr)
        super().begin()


class Ep08Scene(NarratedScene):
    def setup(self):
        super().setup()
        self.terms = TermHighlight(accent=VIRT)
        self.jobs = {}
        self.ladder = self.cpu = self.tl = self.board = None
        self.stu = self.prof = self.badge = None

    # ---------------------------------------------------------------- terms
    # KEY terms of ep 08 (veil + center): MLFQ, allotment, starvation, priority boost.
    # Everything else uses note() (slides into the dock, no veil).
    def term(self, text, **kw):
        return self.terms.show(text, **kw)

    def note(self, text, **kw):
        return self.terms.note(text, **kw)

    def add_docked(self, text):
        m = self.terms.docked_now(text)
        self.add(m)
        return m

    # ---------------------------------------------------------------- world
    def build(self, lanes=3, cpu=True, ticks=None, rules=(), stu="neutral", prof="neutral", badge=True,
              mode="corner", term=None, board=True, board_n=6, holders=()):
        """Add badge, characters, ladder, CPU, timeline, rule board (all optional).  Returns self."""
        if badge:
            self.badge = SectionBadge(BADGE_TEXT, accent=VIRT)
            self.add(self.badge)
        if mode == "corner":
            self.stu, self.prof = student_corner(stu), prof_corner(prof)
        elif mode == "dialogue":
            self.stu, self.prof = student_dlg(stu), prof_dlg(prof)
        if self.stu is not None:
            self.add(self.stu, self.prof)
        if lanes:
            self.ladder = MLFQLadder(levels=lanes)
            self.add(self.ladder)
        if cpu:
            self.cpu = CPU(size=1.2).move_to(CPU_AT)
            self.add(self.cpu)
        if ticks:
            self.tl = make_tl(ticks)
            self.add(self.tl)
        if board:
            self.board = RuleBoard(n_rows=board_n)
            if rules == "skeleton":
                self.board.skeleton(5)
            elif rules:
                self.board.place_now([(t, RULES[t]) for t in rules])
            for t in holders:
                row = self.board._row(t, None, len(self.board.order), color=DIM)
                self.board.order.append(t)
                self.board.rows[t] = row
                self.board.add(row)
            self.add(self.board)
        if term:
            self.add_docked(term)
        return self

    def put(self, name, level, slot=None, scale=None, expr="ready"):
        """Create job ``name``, seat it in a lane (instantly) and add it."""
        j = job(name, scale or self.ladder.job_scale, expr)
        self.ladder.place(j, level, slot)
        self.jobs[name] = j
        self.add(j)
        return j

    def seat_cpu(self, j, expr="running"):
        """Instantly put job on the CPU."""
        self.ladder.release(j)
        j.set_expression(expr)
        place_on(j, self.cpu.slot_point())
        return j

    # ------------------------------------------------------- common anims
    def to_cpu(self, j, t=0.55):
        self.ladder.release(j)
        return Succession(SetExpr(j, "running"), hop_to(j, self.cpu.slot_point(), run_time=t))

    def to_lane(self, j, level, slot=None, expr="ready", t=0.6):
        return Succession(SetExpr(j, expr), self.ladder.promote(j, level, slot, run_time=t))

    def attach_gauge(self, j, value=1.0, width=1.0):
        g = AllotmentGauge(width, value)
        g.attach_to(j)
        return g

    def check_here(self, *mobs, tag="chk"):
        for m in mobs:
            pts = np.vstack([sm.points for sm in m.get_family() if len(sm.points)])
            x0, x1, y0, y1 = pts[:, 0].min(), pts[:, 0].max(), pts[:, 1].min(), pts[:, 1].max()
            if x0 < -6.8 or x1 > 6.8 or y0 < -3.9 or y1 > 3.9:
                print(f"SAFE[{tag}]: x=({x0:.2f},{x1:.2f}) y=({y0:.2f},{y1:.2f})")


def crux_strip():
    card = CruxCard(CRUX_Q, CRUX_SUB, accent=VIRT)
    st = card.strip((0, 3.0, 0), 24)
    return VGroup(st[0], st[2])


def tip_history_card():
    """The 'learn from history' tip card (body: branch-predictor fork + cache grid)."""
    f = VGroup(fork_glyph(0.5), label("branch predictor", 18, DIM)).arrange(RIGHT, buff=0.15)
    c = VGroup(cache_grid(0.5), label("cache", 18, DIM)).arrange(RIGHT, buff=0.15)
    body = VGroup(f, c).arrange(RIGHT, buff=0.5)
    card = TipCard(body=body, title="TIP: LEARN FROM HISTORY", width=4.6, height=1.3, accent=DIM)
    card.move_to(P3(0.7, -2.1))
    return card


def s03_end(sc):
    """S03's end state: 8-lane ladder (A,B on Q8; C on Q4; D on Q1), CPU, skeleton board, tip card."""
    sc.build(lanes=8, cpu=True, rules="skeleton", stu="neutral", prof="worried")
    sc.put("A", 8, 0); sc.put("B", 8, 1); sc.put("C", 4, 0); sc.put("D", 1, 0)
    card = tip_history_card()
    sc.add(card)
    return card


def s04_end(sc, stu="neutral", prof="worried"):
    """S04's end state (8-lane ladder with the four jobs, CPU, board R1-R2 + placeholders)."""
    sc.build(lanes=8, cpu=True, rules=("R1", "R2"), holders=("R3", "R4", "R5"), stu=stu, prof=prof)
    sc.put("A", 8, 0); sc.put("B", 8, 1); sc.put("C", 4, 0); sc.put("D", 1, 0)


def s05_end(sc, stu="neutral", prof="explaining"):
    """S05's end state: 3-lane ladder, B on Q2, A on Q0, board R1-R2 + placeholders."""
    sc.build(lanes=3, cpu=True, rules=("R1", "R2"), holders=("R3", "R4", "R5"), stu=stu, prof=prof)
    sc.put("B", 2, 0); sc.put("A", 0, 0)


def s06_end(sc, stu="curious", prof="happy", ticks=20):
    """S06's end state: empty 3-lane ladder, CPU, empty timeline, board R1..R4b + R5 holder, slice tag."""
    sc.build(lanes=3, cpu=True, ticks=ticks, rules=("R1", "R2", "R3", "R4a", "R4b"), holders=("R5",), stu=stu, prof=prof)
    tag = label("slice = 10 ms", 20, CPU_COLOR).move_to(P3(1.7, -0.15))
    sc.add(tag)
    sc.slice_tag = tag
    return tag


def s07_end(sc, stu="neutral", prof="neutral"):
    """S07's end state: Figure 8.2 on the timeline, A on the CPU, example tag, R1-R4b on the board."""
    s06_end(sc, stu=stu, prof=prof)
    sc.remove(sc.slice_tag)
    A = job("A", sc.ladder.job_scale, "running")
    sc.ladder.release(A)
    place_on(A, sc.cpu.slot_point())
    set_cells(sc.tl, FIG82)
    ex = label("Example 1: one long job", 22, DIM).move_to(P3(-0.7, -3.05))
    sc.jobs["A"] = A
    sc.add(A, ex)
    sc.ex_tag = ex
    return A


def ex_tag(text):
    return label(text, 22, DIM).move_to(P3(-0.7, -3.05))


def s08_end(sc, stu="excited", prof="proud"):
    """S08's end state: Figure 8.3 (left) on the timeline, A on the CPU, '≈ SJF' tag."""
    A = s07_end(sc, stu=stu, prof=prof)
    sc.remove(sc.tl)
    sc.tl = make_tl(20)
    set_cells(sc.tl, fig83_left())
    sc.add(sc.tl)
    sc.remove(sc.ex_tag)
    sc.ex_tag = ex_tag("Example 2: a short job arrives")
    sc.add(sc.ex_tag)
    sc.board.rows  # noqa
    approx = VGroup(MathTex(r"\approx", color=TEXT), label("SJF", 30, TEXT)).arrange(RIGHT, buff=0.15).move_to(P3(-1.5, -0.25))
    sc.add(approx)
    sc.approx = approx
    return A


def comb_cells(tl, upto=20.0):
    """Figure 8.3 (right): A sinks, then B's 1 ms slivers in Q2 every 40 ms with A's long bars in Q0."""
    set_cells(tl, FIG82[:2])
    a0 = 2.1
    for b0 in (6, 10, 14, 18):
        tl.set_span("Q0", a0, b0, "running", COL["A"])
        a0 = b0 + 0.1
    tl.set_span("Q0", a0, upto, "running", COL["A"])
    for b0 in (2, 6, 10, 14, 18):
        tl.set_span("Q2", b0, b0 + 0.1, "running", COL["B"])
    return tl


def s09_end(sc, stu="neutral", prof="neutral"):
    s06_end(sc, stu=stu, prof=prof)
    sc.remove(sc.slice_tag)
    comb_cells(sc.tl)
    A = sc.put("A", 0, 0)
    sc.ladder.release(A)
    sc.seat_cpu(A)
    B = sc.put("B", 2, 0)
    sc.ex_tag = ex_tag("Example 3: interactive job with I/O")
    sc.add(sc.ex_tag)
    return A, B


def card_frame(title, width=3.0, height=2.3, accent=DIM):
    fr = RoundedRectangle(width=width, height=height, corner_radius=0.18).set_fill(CARD_FILL, 1).set_stroke(accent, 2.5)
    t = Text(title, font_size=22, color=TEXT, weight=BOLD).move_to(fr.get_top() + DOWN * 0.3)
    g = VGroup(fr, t)
    g.frame, g.title = fr, t
    return g


def make_half(x_range, ticks=20, label_every=10):
    return Timeline(["Q2", "Q1", "Q0"], ticks=ticks, colors=[TEXT] * 3, x_range=x_range, top=-0.9,
                    row_height=0.4, row_step=0.55, label_mode="boundary", unit_per_tick=10, label_every=label_every,
                    tick_label_y=-2.4, label_font=18, tick_font=14)


LEFT_X = (-4.9, -1.9)
RIGHT_X = (-0.5, 2.5)


def fig84_left(tl):
    set_cells(tl, FIG82[:2])
    tl.set_span("Q0", 2, 10, "running", COL["A"])
    for t in range(11, 21):
        tl.set_block("Q2", t, "running", color=COL["B"] if t % 2 else COL["C"])
    return tl


FIG84_RIGHT = ([("Q2", 1, "A"), ("Q1", 2, "A")] + [("Q0", t, "A") for t in range(3, 11)]
               + [("Q2", 11, "A"), ("Q2", 12, "B"), ("Q2", 13, "C"), ("Q1", 14, "B"), ("Q1", 15, "C"), ("Q1", 16, "A")]
               + [("Q0", t, "A") for t in range(17, 21)])
