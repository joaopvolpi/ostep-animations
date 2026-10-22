"""Episode 07 (Scheduling: Introduction): constants, helpers and state builders.

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
from ostep_lib.props.p04_timeline import Timeline  # noqa: E402
from ostep_lib.props.p04_queue import Queue  # noqa: E402
from ostep_lib.props.p04_icons import *  # noqa: E402,F401,F403

# ---------------------------------------------------------------------------
# Persistent assignments
# ---------------------------------------------------------------------------
COL = {"A": PROCESS_COLORS[0], "B": PROCESS_COLORS[1], "C": PROCESS_COLORS[2], "D": PROCESS_COLORS[3]}
GREEN_OK = "#8BE07A"
CHAR_SCALE = 0.75
STUDENT_CORNER = np.array([-5.8, -2.8, 0.0])
PROF_CORNER = np.array([5.8, -2.8, 0.0])
BADGE_TEXT = "07 · Scheduling"
CRUX_Q = "How to develop scheduling policy?"
CRUX_SUB = "Key assumptions? What metrics are important? What basic approaches have been tried?"

# the Gantt world
GX = (-5.0, 5.0)
G_TOP, G_STEP, G_RH = 1.3, 0.62, 0.34
G_TICKS_Y = -1.6
RO_AT = (0.0, -2.4, 0.0)
TITLE_AT = np.array([0.0, 3.1, 0.0])
STRIP_AT = (-6.6, 3.1, 0.0)


def P3(x, y=0.0):
    return np.array([float(x), float(y), 0.0])


def bottom_to(mob, point):
    mob.shift(np.array(point, dtype=float) - mob.get_bottom())
    return mob


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


def label(text, size=24, color=TEXT, **kw):
    return Text(text, font_size=size, color=color, **kw)


# ---------------------------------------------------------------------------
# Gantt world
# ---------------------------------------------------------------------------
def make_gantt(cells, per, unit="s", every=1, jobs="ABC", cpu=True, top=G_TOP, step=G_STEP, height=G_RH,
               x_range=GX, tick_labels=True, label_font=24, tick_font=18, tick_y=G_TICKS_Y):
    return Timeline(list(jobs), ticks=cells, colors=[COL[j] for j in jobs], x_range=x_range, top=top,
                    row_height=height, row_step=step, cpu_row=cpu, label_mode="boundary", unit_per_tick=per,
                    label_every=every, unit=unit, tick_labels=tick_labels, tick_label_y=tick_y,
                    label_font=label_font, tick_font=tick_font)


def comp_of(run):
    c = {}
    for t, j in enumerate(run, 1):
        if j and j != ".":
            c[j] = t
    return c


def first_run(run):
    f = {}
    for t, j in enumerate(run, 1):
        if j and j != "." and j not in f:
            f[j] = t - 1
    return f


def cell_state(run, arrive, comp, job, t):
    if t <= len(run) and run[t - 1] == job:
        return "running"
    if arrive.get(job, 0) <= t - 1 and t <= comp.get(job, 0):
        return "ready"
    return None


def set_schedule(tl, run, arrive=None, jobs="ABC", upto=None, cpu=True):
    arrive = arrive or {}
    comp = comp_of(run)
    n = upto if upto is not None else len(run)
    for t in range(1, n + 1):
        for j in jobs:
            st = cell_state(run, arrive, comp, j, t)
            if st:
                tl.set_block(j, t, st)
        if cpu and run[t - 1] not in (".", None):
            tl.set_block("CPU", t, "running", color=COL[run[t - 1]])
    return tl


def cell_anims(tl, run, arrive, t, jobs="ABC", cpu=True, run_time=0.35):
    """Animations that fill column ``t`` (1-based) of a schedule."""
    comp = comp_of(run)
    out = []
    for j in jobs:
        st = cell_state(run, arrive or {}, comp, j, t)
        if st:
            out.append(tl.fill(j, t, st, run_time=run_time))
    if cpu and run[t - 1] not in (".", None):
        out.append(tl.fill("CPU", t, "running", color=COL[run[t - 1]], run_time=run_time))
    return out


# --- the book's figures ------------------------------------------------------
def _s(run):
    return list(run) + ["."] * 0


FIG = {
    "fifo": dict(cells=12, per=10, every=1, run=list("ABC") + ["."] * 9, arrive={},
                 terms=["10", "20", "30"], value="20", good=True, title="FIFO"),
    "convoy": dict(cells=12, per=10, every=1, run=list("A" * 10 + "BC"), arrive={},
                   terms=["100", "110", "120"], value="110", good=False, title="FIFO"),
    "sjf": dict(cells=12, per=10, every=1, run=list("BC" + "A" * 10), arrive={},
                terms=["10", "20", "120"], value="50", good=True, title="SJF"),
    "late": dict(cells=12, per=10, every=1, run=list("A" * 10 + "BC"), arrive={"B": 1, "C": 1},
                 terms=["100", "(110-10)", "(120-10)"], value="103.33", good=False, title="SJF"),
    "stcf": dict(cells=12, per=10, every=1, run=list("ABC" + "A" * 9), arrive={"B": 1, "C": 1},
                 terms=["(120-0)", "(20-10)", "(30-10)"], value="50", good=True, title="STCF"),
    "sjf5": dict(cells=15, per=1, every=5, run=list("A" * 5 + "B" * 5 + "C" * 5), arrive={},
                 terms=["0", "5", "10"], value="5", good=False, title="SJF"),
    "rr": dict(cells=15, per=1, every=5, run=list("ABC" * 5), arrive={},
               terms=["0", "1", "2"], value="1", good=True, title="RR"),
}


def turn_brackets(tl, sp, jobs="ABC", labels=None):
    comp = comp_of(sp["run"])
    out = {}
    for j in jobs:
        a = sp["arrive"].get(j, 0)
        c = comp[j]
        lab = (labels or {}).get(j, str((c - a) * sp["per"]))
        out[j] = tl.bracket(j, a, c, lab)
    return out


def resp_brackets(tl, sp, jobs="ABC"):
    fr = first_run(sp["run"])
    out = {}
    for j in jobs:
        a = sp["arrive"].get(j, 0)
        out[j] = tl.bracket(j, a, fr[j], str((fr[j] - a) * sp["per"]), style="dashed")
    return out


def comp_markers(tl, sp, jobs="ABC"):
    comp = comp_of(sp["run"])
    return {j: tl.completion_marker(j, comp[j]) for j in jobs}


class Chart:
    """A drawn schedule: ``tl`` + optional ``br`` (brackets) / ``mk`` (markers) / ``ro`` (readout).
    ``group()`` is everything visible, ready to add."""

    def __init__(self, key, brackets="turn", markers=True, readout=True, framed=True, jobs="ABC", at=None,
                 sp=None, tick_labels=True):
        self.sp = sp or FIG[key]
        sp = self.sp
        self.tl = make_gantt(sp["cells"], sp["per"], every=sp["every"], jobs=jobs, tick_labels=tick_labels)
        set_schedule(self.tl, sp["run"], sp["arrive"], jobs)
        self.br = {}
        if brackets == "turn":
            self.br = turn_brackets(self.tl, sp, jobs)
        elif brackets == "resp":
            self.br = resp_brackets(self.tl, sp, jobs)
        self.mk = comp_markers(self.tl, sp, jobs) if markers else {}
        self.ro = None
        if readout:
            self.ro = MetricReadout(sp["terms"], len(jobs), sp["value"], center=RO_AT)
            self.ro.show_all()
            if framed:
                self.ro.frame_now(sp["good"])

    def group(self):
        g = VGroup(self.tl, *self.br.values(), *self.mk.values())
        if self.ro is not None:
            g.add(self.ro.shown)
        return g

    def parts(self):
        return [self.tl, *self.br.values(), *self.mk.values()] + ([self.ro.shown] if self.ro else [])


def policy_title(text, at=TITLE_AT):
    return Text(text, font_size=36, color=VIRT, weight=BOLD).move_to(at)


def make_strip(opened=()):
    return PadlockStrip(5, size=0.28, at=STRIP_AT, opened=opened)


def make_badge():
    return SectionBadge(BADGE_TEXT, accent=VIRT)


def crux_strip_mobs():
    card = CruxCard(CRUX_Q, CRUX_SUB, accent=VIRT)
    st = card.strip((0, 3.2, 0), 24)
    return VGroup(st[0], st[2])


def work_bar(name, cells, per_cell, color, text=None, height=0.3, font=18):
    """A job's work as a bar (cells x per_cell wide) with a label inside."""
    r = Rectangle(width=cells * per_cell, height=height).set_fill(color, 1).set_stroke(TEXT, 1)
    t = Text(text if text is not None else name, font_size=font, color=INK_DARK).move_to(r)
    g = VGroup(r, t)
    g.rect, g.txt = r, t
    return g


INK_DARK = "#1C1C1C"


def ghost(mob, opacity=0.3):
    return mob.animate.set_opacity(opacity)


# ---------------------------------------------------------------------------
# Scene base
# ---------------------------------------------------------------------------
class Ep07Scene(NarratedScene):
    def setup(self):
        super().setup()
        self.terms = TermHighlight(accent=VIRT)

    def check_bounds(self, label="end", xlim=6.9, ylim=3.85):
        for m in self.mobjects:
            pts = [sm.points for sm in m.get_family() if len(sm.points)
                   and (getattr(sm, "stroke_opacity", 1) > 0.01 or sm.get_fill_opacity() > 0.01)]
            if not pts:
                continue
            pts = np.vstack(pts)
            x0, x1 = pts[:, 0].min(), pts[:, 0].max()
            y0, y1 = pts[:, 1].min(), pts[:, 1].max()
            if x0 < -xlim or x1 > xlim or y0 < -ylim or y1 > ylim:
                print(f"OOB[{label}]: {type(m).__name__} x=({x0:.2f},{x1:.2f}) y=({y0:.2f},{y1:.2f})")

    def tear_down(self):
        self.check_bounds()
        super().tear_down()

    def term(self, text, **kw):
        return self.terms.show(text, **kw)

    def add_docked(self, text):
        m = self.terms._make(text, self.terms.dock_size, self.terms.accent, self.terms.dock_at, right_aligned=True)
        self.terms.docked = m
        self.add(m)
        return m

    def world(self, opened=(), term=None, stu="neutral", prof="neutral", strip=True, badge=True, chars=True):
        """Badge, padlock strip, corner characters (and a docked term)."""
        if badge:
            self.badge = make_badge()
            self.add(self.badge)
        if strip:
            self.strip = make_strip(opened)
            self.add(self.strip)
        if chars:
            self.stu, self.prof = student_corner(stu), prof_corner(prof)
            self.add(self.stu, self.prof)
        if term:
            self.add_docked(term)

    def check(self, *mobs, label="check"):
        """Print an OOB line for specific mobjects crossing the safe area."""
        for m in mobs:
            pts = np.vstack([sm.points for sm in m.get_family() if len(sm.points)])
            x0, x1, y0, y1 = pts[:, 0].min(), pts[:, 0].max(), pts[:, 1].min(), pts[:, 1].max()
            if x0 < -6.6 or x1 > 6.6 or y0 < -3.6 or y1 > 3.6:
                print(f"SAFE[{label}]: {type(m).__name__} x=({x0:.2f},{x1:.2f}) y=({y0:.2f},{y1:.2f})")


# ---------------------------------------------------------------------------
# S01 checkout world
# ---------------------------------------------------------------------------
Q_X = {"front": 0.8, "mid": -0.9, "back": -2.6}
FLOOR_Y = -0.92
COUNTER_AT = P3(4.5, -0.45)


def checkout_tray():
    q = Queue(label="Checkout", center=(-0.9, FLOOR_Y - 0.06), slots=3, spacing=1.7, font_size=24)
    return q


def build_s01_end():
    desk = Checkout(2.2).move_to(COUNTER_AT)
    q = checkout_tray()
    family = proc("A", scale=0.8, label="family")
    bottom_to(family, P3(Q_X["front"], FLOOR_Y + 0.02))
    you = proc("B", scale=0.8, label="you")
    bottom_to(you, P3(Q_X["back"], FLOOR_Y + 0.02))
    carton = milk_carton(0.42).next_to(you, RIGHT, buff=-0.1).shift(UP * 0.05)
    carts = VGroup(*[Cart(0.6, boxes=4).move_to(P3(1.75 + 0.62 * i, -0.62)) for i in range(3)])
    checkbook = checkbook_icon(0.4).move_to(P3(0.8, 0.95))
    spot = Spotlight(height=1.7, spread=0.5)
    spot.move_beam_to(P3(Q_X["front"], FLOOR_Y + 0.05))
    tag = Text("who goes next?", font_size=22, color=DIM).next_to(spot.lamp, UP, buff=0.12)
    stu = Student("frustrated")
    bottom_to(stu, P3(-4.6, -2.75))
    stu.scale(0.9, about_point=stu.get_bottom())
    prof = Professor("thinking").flip()
    prof.scale(0.8, about_point=prof.get_bottom())
    bottom_to(prof, P3(5.3, -2.85))
    return dict(desk=desk, q=q, family=family, you=you, carton=carton, carts=carts, checkbook=checkbook,
                spot=spot, tag=tag, stu=stu, prof=prof)


def build_chart_world(key, opened=(), **kw):
    return Chart(key, **kw)


# ---------------------------------------------------------------------------
# glyphs used inline
# ---------------------------------------------------------------------------
def ruler_glyph(width=1.6, color="#E8E2D0"):
    r = Rectangle(width=width, height=width * 0.22).set_fill(color, 1).set_stroke(outline_of(color, 0.5), 2)
    ticks = VGroup(*[Line([-width / 2 + k * width / 10, r.get_bottom()[1], 0],
                          [-width / 2 + k * width / 10, r.get_bottom()[1] + (0.12 if k % 5 == 0 else 0.07) * width / 1.6, 0])
                     for k in range(1, 10)]).set_stroke(INK_DARK, 2)
    return VGroup(r, ticks)


def cake_glyph(size=0.9):
    plate = Ellipse(width=size * 1.2, height=size * 0.25).set_fill(DIM, 1).set_stroke(TEXT, 2)
    body = Rectangle(width=size, height=size * 0.5).set_fill("#F7A1C4", 1).set_stroke(outline_of("#F7A1C4"), 3)
    icing = Rectangle(width=size, height=size * 0.14).set_fill("#E8E2D0", 1).set_stroke(outline_of("#E8E2D0"), 2)
    cherry = Circle(radius=size * 0.09).set_fill(KERNEL_COLOR, 1).set_stroke(width=0)
    body.next_to(plate.get_center(), UP, buff=-size * 0.05)
    icing.move_to(body.get_top() + DOWN * size * 0.05)
    cherry.move_to(icing.get_top() + UP * size * 0.07)
    return VGroup(plate, body, icing, cherry)


def proof_sheet(size=0.8):
    page = Rectangle(width=size * 0.8, height=size).set_fill("#E9E1C9", 1).set_stroke(DIM, 2)
    lines = VGroup(*[Line([-size * 0.3, y * size, 0], [size * 0.3, y * size, 0]) for y in (0.3, 0.12, -0.06, -0.24)])
    lines.set_stroke(INK_DARK, 2)
    return VGroup(page, lines)


def scale_glyph(width=1.2, color=TEXT):
    """Balance scale."""
    pole = Line([0, -0.45, 0], [0, 0.4, 0]).set_stroke(color, 4)
    beam = Line([-width / 2, 0.4, 0], [width / 2, 0.4, 0]).set_stroke(color, 4)
    base = Line([-0.3, -0.45, 0], [0.3, -0.45, 0]).set_stroke(color, 5)
    pans = VGroup(*[Arc(radius=width * 0.18, start_angle=PI, angle=PI).move_to([x * width / 2, 0.1, 0]).set_stroke(color, 4)
                    for x in (-1, 1)])
    cords = VGroup(*[Line([x * width / 2, 0.4, 0], [x * width / 2 + dx, 0.15, 0]) for x in (-1, 1) for dx in (-width * 0.15, width * 0.15)])
    cords.set_stroke(color, 2)
    return VGroup(base, pole, beam, cords, pans)


def gauge_glyph(size=0.9, color=PERS):
    arc = Arc(radius=size / 2, start_angle=PI, angle=-PI).set_stroke(DIM, 6)
    val = Arc(radius=size / 2, start_angle=PI, angle=-PI * 0.7).set_stroke(color, 6)
    needle = Line(ORIGIN, size * 0.4 * np.array([np.cos(PI * 0.3), np.sin(PI * 0.3), 0])).set_stroke(TEXT, 3)
    return VGroup(arc, val, needle).shift(UP * size * 0.2)


def pairs_tag(text, color=DIM, size=22):
    return Text(text, font_size=size, color=color)


# ---------------------------------------------------------------------------
# More helpers: dimming, schedule reshuffle, scoreboard, bars
# ---------------------------------------------------------------------------
def dimmer(mob, buff=0.4, opacity=0.85):
    """BG-colored translucent rectangle that dims whatever lies under it (add above it)."""
    r = Rectangle(width=mob.width + 2 * buff, height=mob.height + 2 * buff)
    r.set_fill(BG, opacity).set_stroke(width=0).move_to(mob)
    return r


def reshuffle(tl, old_run, old_arr, new_run, new_arr, jobs="ABC", run_time=1.0):
    """Animations that turn the schedule drawn on ``tl`` into another one: running blocks
    move to their new cells, ready outlines vanish / regrow, the CPU lane recolors.
    Call ``tl.purge()`` after playing them."""
    oc, nc = comp_of(old_run), comp_of(new_run)
    n = max(len(old_run), len(new_run))
    old_run = list(old_run) + ["."] * (n - len(old_run))
    new_run = list(new_run) + ["."] * (n - len(new_run))
    anims = []
    for j in jobs:
        i = tl.row_index(j)
        old = {t: cell_state(old_run, old_arr, oc, j, t) for t in range(1, n + 1)}
        new = {t: cell_state(new_run, new_arr, nc, j, t) for t in range(1, n + 1)}
        for t in range(1, n + 1):
            if old[t] == "ready" and new[t] != "ready":
                anims.append(tl.unfill(i, t, run_time=run_time * 0.6))
        ro = sorted(t for t in old if old[t] == "running")
        rn = sorted(t for t in new if new[t] == "running")
        moved = [(tl.block_at.pop((i, a)), b) for a, b in zip(ro, rn)]
        for a in ro[len(rn):]:
            anims.append(tl.unfill(i, a, run_time=run_time * 0.6))
        for (blk, t), a in zip(moved, ro):
            tl.block_at[(i, t)] = blk
            if t != a:
                anims.append(Transform(blk, tl.make_block(i, t, "running", COL[j]), run_time=run_time))
        for t in rn[len(ro):]:
            anims.append(tl.fill(i, t, "running", COL[j], run_time=run_time * 0.5))
        for t in range(1, n + 1):
            if new[t] == "ready" and old[t] != "ready":
                anims.append(tl.fill(i, t, "ready", COL[j], run_time=run_time * 0.5))
    ci = len(tl.rows)
    for t in range(1, n + 1):
        oj, nj = old_run[t - 1], new_run[t - 1]
        if oj == nj:
            continue
        if nj == ".":
            anims.append(tl.unfill(ci, t, run_time=run_time * 0.6))
        elif oj == ".":
            anims.append(tl.fill(ci, t, "running", COL[nj], run_time=run_time * 0.5))
        else:
            b = tl.block_at[(ci, t)]
            anims.append(Transform(b, tl.make_block(ci, t, "running", COL[nj]), run_time=run_time))
    return anims


def make_scoreboard(rows, width=4.2, font=22, title_font=18):
    """Table 'policy | turnaround | response'. ``rows`` = [(name, turn, resp)] with True/False/None.
    Returns a VGroup with ``.frame``, ``.heads``, ``.row_groups`` (each ``.name``, ``.marks``)."""
    step = 0.5
    h = step * (len(rows) + 1) + 0.25
    frame = RoundedRectangle(width=width, height=h, corner_radius=0.15).set_fill(CARD_FILL, 1).set_stroke(DIM, 2)
    x_name = -width / 2 + 0.2
    x_t, x_r = width / 2 - 2.0, width / 2 - 0.6
    top = h / 2 - 0.12 - step / 2
    heads = VGroup(Text("turnaround", font_size=16, color=DIM).move_to(P3(x_t, top)),
                   Text("response", font_size=16, color=DIM).move_to(P3(x_r, top)))
    g = VGroup(frame, heads)
    g.frame, g.heads, g.row_groups = frame, heads, []
    for k, (name, tv, rv) in enumerate(rows):
        y = top - step * (k + 1)
        nm = Text(name, font_size=font, color=TEXT).move_to(P3(x_name, y), aligned_edge=LEFT)
        marks = VGroup()
        for x, v in ((x_t, tv), (x_r, rv)):
            if v is None:
                m = VGroup().move_to(P3(x, y))
            else:
                m = (tick_mark(0.3) if v else x_mark(0.26)).move_to(P3(x, y))
            marks.add(m)
        rg = VGroup(nm, marks)
        rg.name, rg.marks = nm, marks
        g.row_groups.append(rg)
        g.add(rg)
    return g


def mini_proc(name, scale=0.38):
    return proc(name, scale=scale)


def sj_bar(cells, per, color, text, x_left, y, height=0.3, font=18):
    b = work_bar("", cells, per, color, text=text, height=height, font=font)
    b.move_to(P3(x_left + cells * per / 2, y))
    return b


def bar_to(bar, cells, per, text, color=None):
    """Target bar with the same left edge and y as ``bar`` (for ``Transform``)."""
    t = work_bar("", cells, per, color or bar.rect.get_fill_color(), text=text,
                 height=bar.rect.height, font=18)
    t.move_to(P3(bar.rect.get_left()[0] + cells * per / 2, bar.get_center()[1]))
    return t


CELL10 = 10.0 / 12   # width of one cell of the 12-cell charts

BARS_Y = 2.45
LANE_X = (-4.2, 5.4)
CELL14 = (LANE_X[1] - LANE_X[0]) / 14


def make_lanes():
    """Two-lane (CPU / Disk) Gantt, 14 cells of 10 ms."""
    return Timeline(["CPU", "Disk"], ticks=14, x_range=LANE_X, top=0.8, row_height=0.4, row_step=0.6,
                    row_kinds=["cpu", "disk"], label_mode="boundary", unit_per_tick=10, label_every=2, unit="ms",
                    tick_label_y=-0.7, label_font=22, tick_font=18)


NAIVE_CPU = {1: "A", 2: ".", 3: "A", 4: ".", 5: "A", 6: ".", 7: "A", 8: ".", 9: "A",
             10: "B", 11: "B", 12: "B", 13: "B", 14: "B"}
NAIVE_DISK = (2, 4, 6, 8)
OVERLAP_CPU = {t: ("A" if t % 2 else "B") for t in range(1, 11)}
OVERLAP_DISK = (2, 4, 6, 8)


def set_lane_blocks(tl, cpu, disk):
    for t, j in cpu.items():
        if j == ".":
            tl.set_block("CPU", t, "idle")
        else:
            tl.set_block("CPU", t, "running", color=COL[j])
    for t in disk:
        tl.set_block("Disk", t, "ready", color=COL["A"])
    return tl


def lane_bursts(y, x0=LANE_X[0]):
    """A's five 10 ms bursts separated by I/O gaps, as a work bar at height y."""
    g = VGroup()
    for k in range(9):
        cx = x0 + (k + 0.5) * CELL14
        if k % 2 == 0:
            r = Rectangle(width=CELL14, height=0.3).set_fill(COL["A"], 1).set_stroke(TEXT, 1)
        else:
            r = Rectangle(width=CELL14, height=0.3).set_fill(COL["A"], 0.12).set_stroke(COL["A"], 2)
        r.move_to(P3(cx, y))
        g.add(r)
    return g


SB_AT = P3(-2.3, 2.55)
CLOCK_AT = P3(0.8, 2.4)


def scoreboard_at(rows, y=None):
    sb = make_scoreboard(rows, width=4.2)
    sb.move_to(SB_AT if y is None else P3(SB_AT[0], y))
    return sb


def build_rr_end():
    """S11 end state pieces (the chart, response brackets, readout, queue, clock, scoreboard)."""
    ch = Chart("rr", brackets="resp", markers=False)
    title = policy_title("RR")
    sb = scoreboard_at([("SJF · STCF", True, False), ("RR", None, True)])
    clk = ClockIcon(0.3, color=CPU_COLOR).move_to(CLOCK_AT)
    clklab = Text("1 s", font_size=24, color=CPU_COLOR).next_to(clk, RIGHT, buff=0.12)
    queue = Queue(label="Run queue", center=(3.6, 2.2), slots=3, spacing=0.8, font_size=18)
    ps = [proc(n, scale=0.38) for n in "ABC"]
    queue.place(*ps)
    return dict(ch=ch, title=title, sb=sb, clk=clk, clklab=clklab, queue=queue, ps=ps)


def convoy_bars(labels=("A", "B", "C"), y=BARS_Y):
    """The three work bars at the top: A = 100 s (10 cells), B and C = 10 s (1 cell)."""
    xs = (-5.0, 3.55, 4.6)
    ls = (10, 1, 1)
    return VGroup(*[sj_bar(l, CELL10, COL[n], t, x, y) for n, l, x, t in zip("ABC", ls, xs, labels)])


def bars_labelled():
    return convoy_bars(("100 s", "10 s", "10 s"))


def shopper_line(x_front=-1.5, y=-0.5):
    """Mini checkout queue (family A at the front on the right, B 'you', C)."""
    tray = Queue(label="Checkout", center=(x_front - 1.45, y - 0.55), slots=3, spacing=1.4, font_size=22)
    ps = [proc(n, scale=0.6) for n in "ABC"]
    xs = (x_front, x_front - 1.4, x_front - 2.8)
    for p, x in zip(ps, xs):
        bottom_to(p, P3(x, y - 0.55 + 0.1))
    cart = Cart(0.5, boxes=4).move_to(ps[0].get_right() + RIGHT * 0.1 + DOWN * 0.1)
    milk = milk_carton(0.3).next_to(ps[1], RIGHT, buff=-0.15)
    return tray, ps, VGroup(cart, milk)


def thumb(key, width=2.0):
    ch = Chart(key, brackets=None, markers=False, readout=False, tick_labels=False)
    g = VGroup(ch.tl.grid, ch.tl.blocks)
    g.scale_to_fit_width(width)
    return g
