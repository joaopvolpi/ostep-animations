"""Episode 06 (Mechanism: Limited Direct Execution): constants, helpers, the LDE world.

The signature motion of this episode is the CPU chip riding across the dashed
User/Kernel boundary.  ``World`` bundles the chip, the OS token, the boundary, the
privilege gauge and the process benches, and offers ``down()`` / ``up()`` (a trap and a
return-from-trap) as single animations.
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

# ---------------------------------------------------------------------------
# Constants (spec "Persistent assignments")
# ---------------------------------------------------------------------------
COL = {"A": PROCESS_COLORS[0], "B": PROCESS_COLORS[1], "C": PROCESS_COLORS[2], "D": PROCESS_COLORS[3]}
GREEN_OK = "#8BE07A"
RED_BAD = "#FF5A5A"
BADGE_TEXT = "06 · Direct Execution"
CRUX_Q1 = "How to efficiently virtualize the CPU with control?"
CRUX_SUB1 = ("The OS must virtualize the CPU in an efficient manner while retaining control over the system. "
             "Both hardware and operating-system support will be required.")
CRUX_Q2 = "How to perform restricted operations?"
CRUX_Q3 = "How to regain control of the CPU?"
CRUX_SUB3 = "...so that it can switch between processes?"
CRUX_Q4 = "How to gain control without cooperation?"

BY = -0.3                                   # boundary y
USER_SEAT = np.array([0.0, 0.55, 0.0])      # chip center, user seat
KERNEL_SEAT = np.array([0.0, -1.9, 0.0])    # chip center, kernel seat
CHIP = 1.12
PS = 0.85                                   # process scale in the LDE world
BENCH = {"A": np.array([-3.4, 1.0, 0.0]), "B": np.array([3.4, 1.0, 0.0])}   # bottom points
GAUGE_POS = np.array([5.95, -0.2, 0.0])
TIMER_POS = np.array([5.0, 2.3, 0.0])
KSTACK_POS = {"A": np.array([-3.6, -1.9, 0.0]), "B": np.array([3.6, -1.9, 0.0])}


def P3(x, y=0.0):
    return np.array([float(x), float(y), 0.0])


# ---------------------------------------------------------------------------
# Placement helpers (as in episode 04: the bottom edge, label included, sits on the point)
# ---------------------------------------------------------------------------
def bottom_to(mob, point):
    mob.shift(np.array(point, dtype=float) - mob.get_bottom())
    return mob


def feet_for_bottom(mob, point):
    return np.array(point, dtype=float) + (base_point(mob) - mob.get_bottom())


def hop_bottom(p, point, **kw):
    return hop_to(p, feet_for_bottom(p, point), **kw)


def proc(name, expr="ready", scale=PS, color=None, label=None):
    p = Process(expr, color=color or COL.get(name, PROCESS_COLORS[4]), label=name if label is None else label)
    if scale != 1.0:
        p.scale(scale)
    return p


def apply_now(anim):
    """Run an animation to its end state instantly (to build a "starts with" state)."""
    anim.begin()
    anim.finish()
    return anim


def snippet(text, font_size=20, color=TEXT, pad=0.18):
    """A one-line code chip (mono text on a dark card)."""
    t = Text(text, font=MONO_FONT, font_size=font_size, color=color)
    box = RoundedRectangle(width=t.width + 2 * pad, height=t.height + 2 * pad, corner_radius=0.08)
    box.set_fill("#272822", 1).set_stroke(DIM, 2)
    t.move_to(box)
    g = VGroup(box, t)
    g.box, g.text = box, t
    return g


def strip(q, font_size=22):
    return CruxCard(q, accent=VIRT).strip(font_size=font_size)


def tag(text, color=DIM, font_size=20, fill=CARD_FILL):
    t = Text(text, font=FONT, font_size=font_size, color=TEXT)
    box = RoundedRectangle(width=t.width + 0.3, height=t.height + 0.2, corner_radius=0.08)
    box.set_fill(fill, 1).set_stroke(color, 2)
    t.move_to(box)
    return VGroup(box, t)


def bolt(size=0.5, color=CPU_COLOR):
    """Lightning bolt glyph."""
    pts = [(0.1, 0.5), (-0.25, -0.02), (-0.02, -0.02), (-0.12, -0.5), (0.27, 0.06), (0.04, 0.06)]
    p = Polygon(*[P3(x * size * 2, y * size * 2) for x, y in pts])
    p.set_fill(color, 1).set_stroke(outline_of(color), 2)
    return p


def zigzag_arrow(start, end, color=CPU_COLOR):
    return Arrow(start, end, buff=0, stroke_width=5, tip_length=0.2, color=color, max_tip_length_to_length_ratio=0.3)


# ---------------------------------------------------------------------------
# Characters
# ---------------------------------------------------------------------------
def corner_chars(small=False, s_expr="neutral", p_expr="neutral"):
    if small:
        sc, sp, pp = 0.6, P3(-5.9, -2.95), P3(5.9, -2.95)
    else:
        sc, sp, pp = 0.75, P3(-5.8, -2.8), P3(5.8, -2.8)
    stu = Student(s_expr).scale(sc).move_to(sp)
    prof = Professor(p_expr).scale(sc).flip().move_to(pp)
    return stu, prof


STUDENT_DIALOGUE = P3(-2.6, -1.2)
PROF_DIALOGUE = P3(2.6, -1.2)


def student_dialogue(expr="neutral", pos=None):
    return bottom_to(Student(expr), (STUDENT_DIALOGUE if pos is None else pos) + DOWN * 1.05)


def prof_dialogue(expr="neutral", pos=None):
    return bottom_to(Professor(expr).flip(), (PROF_DIALOGUE if pos is None else pos) + DOWN * 1.05)


# ---------------------------------------------------------------------------
# The LDE world
# ---------------------------------------------------------------------------
class World:
    """Boundary + gauge + chip (+ token, + processes on benches).

    ``World(level="user", chip_size=CHIP, user_seat=USER_SEAT, kernel_seat=KERNEL_SEAT, ps=PS,
    token_scale=1.0, rest=None)``.  ``rest`` is the base point where the OS token waits when
    it is not on the chip.  Parts: ``boundary, gauge, chip, token, procs, rings``.
    """

    def __init__(self, level="user", chip_size=CHIP, user_seat=USER_SEAT, kernel_seat=KERNEL_SEAT, ps=PS,
                 token_scale=1.0, rest=None, gauge=True):
        self.cs, self.useat, self.kseat, self.ps = chip_size, np.array(user_seat), np.array(kernel_seat), ps
        self.rest = np.array(rest if rest is not None else P3(3.3, -1.4))
        self.boundary = UserKernelBoundary(y=BY)
        self.boundary.set_z_index(-5)
        self.gauge = PrivilegeGauge(height=1.6, width=0.4, level=level).move_to(GAUGE_POS)
        self.chip = CPU(chip_size, label="CPU", pins=3)
        self.chip.move_to(self.useat if level == "user" else self.kseat).set_z_index(2)
        self.token = KernelToken(scale=token_scale).set_z_index(5)
        bottom_to(self.token, self.rest)
        self.procs = {}
        self.rings = {}
        self.level = level

    # -- geometry
    def slot(self, seat):
        """Bottom point of whatever stands on a chip at ``seat``."""
        return np.array(seat) + UP * (self.cs / 2 + 0.02)

    def chip_slot(self):
        return self.chip.get_center() + UP * (self.cs / 2 + 0.02)

    # -- building
    def add_proc(self, name, expr="ready", where="bench"):
        p = proc(name, expr, scale=self.ps).set_z_index(4)
        self.procs[name] = p
        if where == "chip":
            bottom_to(p, self.chip_slot())
        elif where == "bench":
            bottom_to(p, BENCH[name])
        return p

    def add_ring(self, name):
        r = bench_ring(COL[name]).move_to(BENCH[name] + DOWN * 0.1).set_z_index(1)
        self.rings[name] = r
        return r

    def token_on_chip(self):
        bottom_to(self.token, self.chip_slot())
        return self.token

    def mobs(self):
        return [self.boundary, self.gauge, self.chip, *self.rings.values(), *self.procs.values(), self.token]

    # -- animations
    def hop_to_bench(self, name, rt=0.5):
        return hop_bottom(self.procs[name], BENCH[name], run_time=rt)

    def hop_on_chip(self, name, seat=None, rt=0.5):
        p = self.procs[name]
        return hop_bottom(p, self.slot(self.useat if seat is None else seat), run_time=rt)

    def token_hop_chip(self, seat=None, rt=0.5):
        return hop_bottom(self.token, self.slot(self.kseat if seat is None else seat), run_time=rt)

    def token_hop_rest(self, rt=0.5):
        return hop_bottom(self.token, self.rest, run_time=rt)

    def ride(self, to, riders=(), rt=0.8):
        seat = self.useat if to == "user" else self.kseat
        self.level = to
        return cpu_ride(self.chip, seat, self.boundary, self.gauge, riders=riders, run_time=rt)

    def down(self, name=None, riders=(), rt=0.8, token=True):
        """A trap: the process (if any) hops to its bench, the chip rides to the kernel seat and
        the OS token hops on."""
        seq = []
        if name is not None:
            self.procs[name].set_expression("ready")
            seq.append(hop_bottom(self.procs[name], BENCH[name], run_time=0.5))
        ride = self.ride("kernel", riders, rt)
        if token:
            ride = AnimationGroup(ride, Succession(Wait(rt * 0.45), self.token_hop_chip(rt=0.5)))
        seq.append(ride)
        return Succession(*seq)

    def up(self, name=None, riders=(), rt=0.8, token=True, expr="running"):
        """A return-from-trap: the token steps off, the chip rides up, the process hops on."""
        seq = []
        if token:
            seq.append(self.token_hop_rest(rt=0.45))
        seq.append(self.ride("user", riders, rt))
        if name is not None:
            self.procs[name].set_expression(expr)
            seq.append(hop_bottom(self.procs[name], self.slot(self.useat), run_time=0.5))
        return Succession(*seq)


# ---------------------------------------------------------------------------
# Scene base
# ---------------------------------------------------------------------------
class Ep06Scene(NarratedScene):
    """NarratedScene + overlays (badge, term highlight) and an end-of-scene bounds check."""

    def setup(self):
        super().setup()
        self.terms = TermHighlight(accent=VIRT)

    def check_bounds(self, label="end", xlim=6.75, ylim=3.85):
        for m in self.mobjects:
            pts = [sm.points for sm in m.get_family() if len(sm.points)
                   and (sm.get_stroke_opacity() > 0.01 or sm.get_fill_opacity() > 0.01)]
            if not pts:
                continue
            pts = np.vstack(pts)
            if pts[:, 0].min() <= -7.1 and pts[:, 0].max() >= 7.1:
                continue
            x0, x1 = pts[:, 0].min(), pts[:, 0].max()
            y0, y1 = pts[:, 1].min(), pts[:, 1].max()
            if x0 < -xlim or x1 > xlim or y0 < -ylim or y1 > ylim:
                print(f"OOB[{label}]: {type(m).__name__} x=({x0:.2f},{x1:.2f}) y=({y0:.2f},{y1:.2f})")

    def tear_down(self):
        self.check_bounds()
        super().tear_down()

    def add_badge(self):
        self.badge = SectionBadge(BADGE_TEXT, accent=VIRT)
        self.add(self.badge)
        return self.badge

    def add_docked_term(self, text):
        m = self.terms._make(text, self.terms.dock_size, self.terms.accent, self.terms.dock_at, right_aligned=True)
        self.terms.docked = m
        self.add(m)
        return m

    def term(self, text, **kw):
        return self.terms.show(text, **kw)

    def note(self, text, **kw):
        return self.terms.note(text, **kw)


# ---------------------------------------------------------------------------
# Small builders
# ---------------------------------------------------------------------------
def chart_legend():
    """The small "LDE protocol" legend the figure shrinks to (top-left, under the badge)."""
    box = RoundedRectangle(width=1.7, height=0.9, corner_radius=0.08).set_fill(CARD_FILL, 1).set_stroke(DIM, 2)
    cols = VGroup(*[Rectangle(width=0.38, height=0.5).set_fill(c, 0.35).set_stroke(c, 1.5)
                    for c in (KERNEL_COLOR, CPU_COLOR, USER_COLOR)]).arrange(RIGHT, buff=0.1)
    cols.move_to(box.get_center() + UP * 0.12)
    t = Text("LDE protocol", font_size=16, color=DIM).move_to(box.get_bottom() + UP * 0.14)
    return VGroup(box, cols, t).move_to(P3(-5.7, 2.85))


class LDEThumb(VGroup):
    """Live thumbnail of the LDE world (boundary, chip, mode label, kernel stack)."""

    def __init__(self, width=2.6, height=1.5, **kwargs):
        super().__init__(**kwargs)
        self.w, self.h = width, height
        frame = RoundedRectangle(width=width, height=height, corner_radius=0.1).set_fill(CARD_FILL, 1).set_stroke(DIM, 2)
        mid = P3(0, 0.0)
        user = Rectangle(width=width, height=height / 2).set_fill(USER_COLOR, 0.12).set_stroke(width=0)
        kern = Rectangle(width=width, height=height / 2).set_fill(KERNEL_COLOR, 0.15).set_stroke(width=0)
        user.move_to(P3(0, height / 4))
        kern.move_to(P3(0, -height / 4))
        line = DashedLine(P3(-width / 2, 0), P3(width / 2, 0), dash_length=0.1).set_stroke(TEXT, 2)
        self.chip = Square(0.34).set_fill(CPU_COLOR, 1).set_stroke(outline_of(CPU_COLOR), 2)
        self.up_pos, self.down_pos = P3(-0.2, height / 4), P3(-0.2, -height / 4)
        self.chip.move_to(self.down_pos)
        self.mode = Text("KERNEL", font=MONO_FONT, font_size=16, color=KERNEL_COLOR)
        self.mode.move_to(P3(width / 2 - 0.5, height / 2 - 0.2))
        self.kst = Rectangle(width=0.5, height=0.4).set_fill(MEM_COLOR, 0.2).set_stroke(MEM_COLOR, 2)
        self.kst.move_to(P3(-width / 2 + 0.5, -height / 4))
        self.kst_label = Text("k-stack", font=MONO_FONT, font_size=11, color=MEM_COLOR).next_to(self.kst, UP, buff=0.03)
        self.pk = Rectangle(width=0.3, height=0.1).set_fill(COL["A"], 1).set_stroke(width=0).move_to(self.kst).set_opacity(0)
        self.add(frame, user, kern, line, self.kst, self.kst_label, self.pk, self.chip, self.mode)
        self.frame = frame

    def ride(self, level, run_time=0.8):
        tgt = self.up_pos if level == "user" else self.down_pos
        col = USER_COLOR if level == "user" else KERNEL_COLOR
        new = Text(level.upper(), font=MONO_FONT, font_size=16, color=col).move_to(self.mode)
        new.align_to(self.mode, RIGHT)
        return AnimationGroup(self.chip.animate(run_time=run_time).move_to(self.get_center() + tgt),
                              Transform(self.mode, new), run_time=run_time)

    def packet(self):
        return self.pk.animate.set_opacity(1)


# ---------------------------------------------------------------------------
# S03 chart rows (Figure 6.1) and tiny row icons
# ---------------------------------------------------------------------------
def row_icon(kind):
    if kind == "pcb":
        r = Rectangle(width=0.5, height=0.36).set_fill(CARD_FILL, 1).set_stroke(COL["A"], 2)
        h = Rectangle(width=0.14, height=0.36).set_fill(COL["A"], 1).set_stroke(width=0).align_to(r, LEFT)
        return VGroup(r, h)
    if kind == "mem":
        return VGroup(*[Rectangle(width=0.36, height=0.1).set_fill(MEM_COLOR, 0.4).set_stroke(MEM_COLOR, 1.5)
                        for _ in range(4)]).arrange(DOWN, buff=0)
    if kind == "load":
        d = Circle(radius=0.14).set_fill(DISK_COLOR, 0.6).set_stroke(DISK_COLOR, 2)
        a = Arrow(LEFT * 0.12, RIGHT * 0.26, buff=0, stroke_width=3, tip_length=0.1)
        m = Rectangle(width=0.16, height=0.34).set_fill(MEM_COLOR, 0.5).set_stroke(MEM_COLOR, 1.5)
        return VGroup(d, a, m).arrange(RIGHT, buff=0.04)
    if kind == "stack":
        return VGroup(*[Rectangle(width=0.4, height=0.1).set_fill(COL["A"], 0.7).set_stroke(TEXT, 1) for _ in range(3)]).arrange(UP, buff=0.02)
    if kind == "regs":
        return VGroup(*[Square(0.12).set_fill(CPU_COLOR, 0.6).set_stroke(TEXT, 1) for _ in range(3)]).arrange(RIGHT, buff=0.03)
    return VGroup()


S03_ROWS = [
    (0, "Create entry for process list", False, "pcb"),
    (0, "Allocate memory for program", False, "mem"),
    (0, "Load program into memory", False, "load"),
    (0, "Set up stack with argc/argv", False, "stack"),
    (0, "Clear registers", False, "regs"),
    (0, "Execute call main()", True, None),
    (1, "Run main()", False, None),
    (1, "Execute return from main", True, None),
    (0, "Free memory of process", False, None),
    (0, "Remove from process list", False, None),
]


def make_s03_chart():
    return ProtocolChart(["OS", "Program"], colors=[KERNEL_COLOR, USER_COLOR], col_x=[-3.2, 3.2], col_width=5.6,
                         top=2.2, bottom=-3.0, row_h=0.42, font_size=22, header_size=30)


def s03_write(chart, i, run_time=0.7):
    col, text, bold, icon = S03_ROWS[i]
    return chart.write_row(col, text, bold=bold, icon=row_icon(icon) if icon else None, run_time=run_time)


def build_s03_end():
    """The S03 end state: the full chart, the two arrows, the FAST tag and the numerals."""
    chart = make_s03_chart()
    apply_now(chart.draw())
    for i in range(len(S03_ROWS)):
        apply_now(s03_write(chart, i))
    apply_now(chart.link(5, 6))
    apply_now(chart.link(7, 8))
    fast = tag("FAST", GREEN_OK, 24).move_to(P3(3.2, 1.55))
    n1 = numeral(1).move_to(P3(6.15, 1.5))
    n2 = numeral(2).move_to(P3(6.15, 0.3))
    icon_cpu = CPU(0.5, label=None, pins=2).move_to(P3(6.1, -0.6))
    wall = Rectangle(width=0.08, height=0.6).set_fill(USER_COLOR, 0.4).set_stroke(USER_COLOR, 2).move_to(P3(6.1, -1.3))
    ib = proc("B", "ready", scale=0.3).next_to(wall, DOWN, buff=0.02)
    return dict(chart=chart, fast=fast, n1=n1, n2=n2, extras=VGroup(icon_cpu, wall, ib))


def numeral(n, color=VIRT, radius=0.3):
    c = Circle(radius=radius).set_fill(CARD_FILL, 1).set_stroke(color, 4)
    t = Text(str(n), font=FONT, font_size=34, color=color, weight=BOLD).move_to(c)
    return VGroup(c, t)


# ---------------------------------------------------------------------------
# xv6 code (S14)
# ---------------------------------------------------------------------------
SWTCH = """swtch:
  # save old registers
  movl 4(%esp), %eax
  popl 0(%eax)
  movl %esp, 4(%eax)
  movl %ebx, 8(%eax)
  # load new registers
  movl 4(%esp), %eax
  movl 28(%eax), %ebp
  movl 4(%eax), %esp
  pushl 0(%eax)
  ret"""


def swtch_code(font_size=18):
    return Code(code_string=SWTCH, language="gas", formatter_style="monokai", add_line_numbers=False,
                background="rectangle",
                background_config={"fill_color": "#272822", "stroke_color": DIM, "stroke_width": 2,
                                   "corner_radius": 0.15, "buff": 0.25},
                paragraph_config={"font": MONO_FONT, "font_size": font_size, "line_spacing": 0.6})


def code_line_bar(code, i, j=None, color=CPU_COLOR, opacity=0.25):
    """Highlight rectangle over lines i..j (inclusive) of a Code block."""
    j = i if j is None else j
    lines = code.code_lines
    top = lines[i].get_top()[1] + 0.05
    bot = lines[j].get_bottom()[1] - 0.05
    bg = code.background
    bar = Rectangle(width=bg.width - 0.15, height=top - bot)
    bar.move_to(P3(bg.get_x(), (top + bot) / 2)).set_fill(color, opacity).set_stroke(color, 1.5, opacity=0.8)
    bar.set_z_index(12)
    return bar


def handler_box(label="trap handler", center=P3(3.3, -1.9), width=2.2, height=1.0):
    box = RoundedRectangle(width=width, height=height, corner_radius=0.12).set_fill(KERNEL_COLOR, 0.15).set_stroke(KERNEL_COLOR, 3)
    t = Text(label, font=FONT, font_size=24, color=TEXT).move_to(box)
    return VGroup(box, t).move_to(center)
