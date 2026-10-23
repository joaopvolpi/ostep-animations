"""Episode 04 (The Abstraction: The Process): constants, helpers and state builders.

Every scene starts from a builder here (``build_*``) so scenes can be rendered
independently and still match the previous scene's "Ends with" state.
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
from ostep_lib.props.p04_state_diagram import StateDiagram  # noqa: E402
from ostep_lib.props.p04_pcb import PCBCard  # noqa: E402
from ostep_lib.props.p04_registers import RegisterBank  # noqa: E402
from ostep_lib.props.p04_bus import Bus  # noqa: E402
from ostep_lib.props.p04_icons import *  # noqa: E402,F401,F403

# ---------------------------------------------------------------------------
# Persistent assignments
# ---------------------------------------------------------------------------
COL = {
    "A": PROCESS_COLORS[0],   # coral
    "B": PROCESS_COLORS[1],   # mint
    "C": PROCESS_COLORS[2],   # gold
    "D": PROCESS_COLORS[3],   # sky
}
COL["P0"], COL["P1"] = COL["A"], COL["B"]

CPU_HOME = np.array([0.0, 0.6, 0.0])
CPU_SIZE = 1.4
CHAR_SCALE = 0.75
STUDENT_CORNER = np.array([-5.8, -2.8, 0.0])
PROF_CORNER = np.array([5.8, -2.8, 0.0])
STUDENT_DIALOGUE = np.array([-2.6, -1.2, 0.0])
PROF_DIALOGUE = np.array([2.6, -1.2, 0.0])
# S01/S02: the laptop and the motherboard fill the center, so the dialogue
# positions move out to the sides (deviation from the spec's (+-2.6, -1.2)).
STUDENT_SIDE = np.array([-5.0, -1.6, 0.0])
PROF_SIDE = np.array([5.0, -1.6, 0.0])
BADGE_TEXT = "04 · The Process"
CRUX_Q = "How to provide the illusion of many CPUs?"
CRUX_SUB = ("Although there are only a few physical CPUs available, how can the OS provide "
            "the illusion of a nearly-endless supply of said CPUs?")
SAVE_SLOT_DOCK = np.array([6.3, 2.95, 0.0])
GREEN_OK = "#8BE07A"


def P3(x, y=0.0):
    return np.array([float(x), float(y), 0.0])


# ---------------------------------------------------------------------------
# Characters
# ---------------------------------------------------------------------------
def student_corner(expr="neutral"):
    s = Student(expr).scale(CHAR_SCALE)
    s.move_to(STUDENT_CORNER)
    return s


def prof_corner(expr="neutral"):
    p = Professor(expr).scale(CHAR_SCALE).flip()
    p.move_to(PROF_CORNER)
    return p


def student_dialogue(expr="neutral", pos=None):
    s = Student(expr)
    return bottom_to(s, (STUDENT_DIALOGUE if pos is None else pos) + DOWN * 1.05)


def prof_dialogue(expr="neutral", pos=None):
    p = Professor(expr).flip()
    return bottom_to(p, (PROF_DIALOGUE if pos is None else pos) + DOWN * 1.05)


def proc(name, expr="ready", scale=1.0, color=None, label=None):
    p = Process(expr, color=color or COL.get(name, PROCESS_COLORS[4]),
                label=name if label is None else label)
    if scale != 1.0:
        p.scale(scale)
    return p


# ---------------------------------------------------------------------------
# Placement helpers (the spec's "running process stands ON the chip" uses the
# process's full bottom edge, label included, so the label never covers the chip)
# ---------------------------------------------------------------------------
def bottom_to(mob, point):
    mob.shift(np.array(point, dtype=float) - mob.get_bottom())
    return mob


def feet_for_bottom(mob, point):
    """The base point (feet) that puts ``mob``'s bottom edge at ``point``."""
    return np.array(point, dtype=float) + (base_point(mob) - mob.get_bottom())


def seat(p, cpu):
    return bottom_to(p, cpu.slot_point() + UP * 0.02)


def hop_bottom(p, point, **kw):
    """hop_to so that the bottom edge (label) lands on ``point``."""
    return hop_to(p, feet_for_bottom(p, point), **kw)


def hop_seat(p, cpu, **kw):
    return hop_bottom(p, cpu.slot_point() + UP * 0.02, **kw)


def queue_mover(mob, point, run_time=0.5, **kw):
    return hop_bottom(mob, point, run_time=run_time, **kw)


# ---------------------------------------------------------------------------
# Overlays: badge, term highlight, docked term, save slot
# ---------------------------------------------------------------------------
def make_badge():
    cpu_icon = CPU(size=0.26, label=None, pins=2)
    b = SectionBadge(BADGE_TEXT, accent=VIRT)
    return b


def make_terms():
    return TermHighlight(accent=VIRT)


def dock_term_now(terms, text):
    """Instantly create the docked term strip (top-right) and register it."""
    m = terms._make(text, terms.dock_size, terms.accent, terms.dock_at, right_aligned=True)
    terms.docked = m
    return m


def docked_save_slot():
    return save_slot(0.5).move_to(SAVE_SLOT_DOCK)


def crux_strip():
    card = CruxCard(CRUX_Q, CRUX_SUB, accent=VIRT)
    return card.strip()


# ---------------------------------------------------------------------------
# Scene base for the episode
# ---------------------------------------------------------------------------
class Ep04Scene(NarratedScene):
    """NarratedScene + the episode's overlays."""

    def setup(self):
        super().setup()
        self.terms = make_terms()

    def check_bounds(self, label="end", xlim=6.9, ylim=3.85):
        """Print an 'OOB:' line for every visible top-level mobject that leaves the frame."""
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

    def add_badge(self):
        self.badge = make_badge()
        self.add(self.badge)
        return self.badge

    def add_corner_chars(self, s_expr="neutral", p_expr="neutral"):
        self.stu = student_corner(s_expr)
        self.prof = prof_corner(p_expr)
        self.add(self.stu, self.prof)
        return self.stu, self.prof

    def add_docked_term(self, text):
        m = dock_term_now(self.terms, text)
        self.add(m)
        return m

    def term(self, text, **kw):
        """Animation: the term highlight (write big, hold, dock)."""
        return self.terms.show(text, **kw)


# ---------------------------------------------------------------------------
# App icons and task manager (S01 / S20)
# ---------------------------------------------------------------------------
APP_SPOTS = [P3(-3, 2.2), P3(-1, 2.8), P3(1, 2.8), P3(3, 2.2), P3(3.8, 0.8)]


def app_icons(size=0.6):
    return VGroup(browser_icon(size), music_icon(size), chat_icon(size),
                  gamepad_icon(size), envelope_icon(size))


def counter_group(programs=137, cpus=None, at=P3(4.8, 3.0)):
    """'programs: N' (+ optional 'CPUs: N' below). Returns (group, prog_num, cpu_num)."""
    lab = Text("programs:", font_size=28, color=TEXT)
    num = Integer(programs, font_size=34, color=TEXT)
    num.next_to(lab, RIGHT, buff=0.15).align_to(lab, DOWN)
    g = VGroup(lab, num)
    cnum = None
    if cpus is not None:
        clab = Text("CPUs:", font_size=28, color=CPU_COLOR)
        cnum = Integer(cpus, font_size=34, color=CPU_COLOR)
        crow = VGroup(clab, cnum)
        clab.align_to(lab, LEFT)
        clab.next_to(lab, DOWN, buff=0.25, aligned_edge=LEFT)
        cnum.next_to(clab, RIGHT, buff=0.15).align_to(clab, DOWN)
        g.add(clab, cnum)
    g.shift(at - VGroup(lab, num).get_center())
    return g, num, cnum


class TaskManager(VGroup):
    """Panel over the laptop screen with scrolling grey rows (clipped by hand)."""

    def __init__(self, width=3.4, height=2.1, rows=7, **kwargs):
        super().__init__(**kwargs)
        self.frame = RoundedRectangle(width=width, height=height, corner_radius=0.08)
        self.frame.set_fill("#202020", 1).set_stroke(DIM, 2)
        self.title = Text("Task Manager", font_size=18, color=TEXT).move_to(
            self.frame.get_top() + DOWN * 0.18).align_to(self.frame, LEFT).shift(RIGHT * 0.15)
        self.top_y = self.frame.get_top()[1] - 0.38
        self.bot_y = self.frame.get_bottom()[1] + 0.08
        self.row_h = 0.22
        self.w = width
        self.rows = VGroup()
        n = int((self.top_y - self.bot_y) / self.row_h) + 2
        for i in range(n):
            self.rows.add(self._row(i))
        self.offset = 0.0
        self.add(self.frame, self.title, self.rows)
        self._layout()

    def _row(self, i):
        wname = 0.5 + 0.9 * ((i * 37) % 7) / 7
        r = VGroup(
            Rectangle(width=wname, height=0.09).set_fill(DIM, 0.8).set_stroke(width=0),
            Rectangle(width=0.35, height=0.09).set_fill(DIM, 0.5).set_stroke(width=0),
        )
        return r

    def _layout(self):
        self.top_y = self.frame.get_top()[1] - 0.4
        self.bot_y = self.frame.get_bottom()[1] + 0.1
        n = len(self.rows)
        span = n * self.row_h
        x_left = self.frame.get_left()[0] + 0.2
        for i, r in enumerate(self.rows):
            y = self.top_y - ((i * self.row_h + self.offset) % span)
            r[0].move_to(P3(x_left, y), aligned_edge=LEFT)
            r[1].move_to(P3(self.frame.get_right()[0] - 0.25, y), aligned_edge=RIGHT)
            vis = self.bot_y <= y <= self.top_y + 0.01
            r.set_opacity(1.0 if vis else 0.0)

    def start_scrolling(self, speed=0.3):
        """Adds an updater scrolling at ``self.speed`` units/second (change
        ``self.speed`` any time)."""
        self.speed = speed

        def upd(m, dt):
            m.offset += m.speed * dt
            m._layout()
        self.add_updater(upd)
        return self


# ---------------------------------------------------------------------------
# Motherboard (S02)
# ---------------------------------------------------------------------------
MOBO_GREEN = "#1F3B2A"


def motherboard():
    board = Rectangle(width=8, height=3.5).move_to(P3(0, 0.25))
    board.set_fill(MOBO_GREEN, 1).set_stroke("#2F5A3F", 3)
    traces = VGroup()
    rng = np.random.default_rng(3)
    for k in range(14):
        y = -1.3 + k * 0.23
        x0 = -3.8 + rng.uniform(0, 1.5)
        x1 = 3.8 - rng.uniform(0, 1.5)
        if abs(y - 0.6) < 0.9 and x0 < 0 < x1:
            # route around the chip area
            traces.add(Line(P3(x0, y), P3(-1.2, y)), Line(P3(1.2, y), P3(x1, y)))
        else:
            traces.add(Line(P3(x0, y), P3(x1, y)))
    traces.set_stroke("#3E7A52", 1.5, opacity=0.6)
    return VGroup(board, traces)


def virtual_cpu_row(n=5, y=2.6, size=0.55, xs=None):
    icons = [browser_icon, music_icon, chat_icon, gamepad_icon, envelope_icon]
    xs = xs if xs is not None else np.linspace(-3.6, 2.4, n)
    g = VGroup()
    for i in range(n):
        chip = CPU(size=size, label=None, pins=2, color=PROCESS_COLORS[i % 6])
        make_translucent(chip, 0.5, 0.8)
        chip.move_to(P3(xs[i], y))
        ic = icons[i % 5](0.3).next_to(chip, UP, buff=0.12)
        g.add(VGroup(chip, ic))
    return g


# ---------------------------------------------------------------------------
# Terminal thumbnail (S03 callback). Local stand-in for the ov_ Terminal.
# ---------------------------------------------------------------------------
def terminal_thumb(lines=("prompt> ./cpu A & ./cpu B & ./cpu C & ./cpu D &",), width=5.4, height=1.6):
    frame = RoundedRectangle(width=width, height=height, corner_radius=0.1)
    frame.set_fill("#101010", 1).set_stroke(DIM, 2)
    bar = Rectangle(width=width, height=0.22).move_to(frame.get_top() + DOWN * 0.11)
    bar.set_fill("#2A2A2A", 1).set_stroke(width=0)
    dots = VGroup(*[Dot(radius=0.04, color=c) for c in (KERNEL_COLOR, CPU_COLOR, GREEN)]).arrange(RIGHT, buff=0.06)
    dots.move_to(bar).align_to(bar, LEFT).shift(RIGHT * 0.12)
    g = VGroup(frame, bar, dots)
    g.frame = frame
    return g


# ---------------------------------------------------------------------------
# World builders
# ---------------------------------------------------------------------------
def build_s01_end():
    """Laptop + 5 icons + task manager + counter + Student (dialogue)."""
    laptop = Laptop(width=5).move_to(P3(0, 0.3))
    icons = app_icons()
    for ic, p in zip(icons, APP_SPOTS):
        ic.move_to(p)
    tm = TaskManager(width=laptop.screen.width * 0.92, height=laptop.screen.height * 0.9)
    tm.move_to(laptop.screen_center())
    counter, num, _ = counter_group(137)
    stu = student_dialogue("curious", STUDENT_SIDE)
    return dict(laptop=laptop, icons=icons, tm=tm, counter=counter, num=num, stu=stu)


def build_s02_end():
    board = motherboard()
    cpu = CPU(CPU_SIZE).move_to(CPU_HOME)
    vcpus = virtual_cpu_row()
    counter, num, cnum = counter_group(137, 1)
    stu = student_dialogue("confused", STUDENT_SIDE)
    prof = prof_dialogue("proud", PROF_SIDE)
    comp = Computer("surprised").scale(0.7).move_to(P3(0, -2.6))
    return dict(board=board, cpu=cpu, vcpus=vcpus, counter=counter, num=num, cnum=cnum,
                stu=stu, prof=prof, comp=comp)


S04_A, S04_B = P3(1, 0.3), P3(3, 0.3)
S04_DISK = P3(-4, -0.3)


def s04_file(disk):
    return FileIcon("browser", width=0.7).move_to(disk.top_point() + UP * 0.95)


def s04_brace(a, b):
    brace = Brace(VGroup(a, b), DOWN, color=DIM)
    blab = Text("1 program → 2 processes", font_size=28, color=TEXT).next_to(brace, DOWN, buff=0.12)
    return brace, blab


def build_s04_end():
    """Disk + file at left, two 'browser' processes, brace label (S04 end)."""
    disk = Disk().move_to(S04_DISK)
    file = s04_file(disk)
    a = proc("A", label="browser")
    b = proc("B", label="browser")
    a.move_to(S04_A)
    b.move_to(S04_B)
    brace, blab = s04_brace(a, b)
    return dict(disk=disk, file=file, a=a, b=b, brace=brace, blab=blab)


def row_positions(xs=(-2, 0, 2), y=-1.15):
    return [P3(x, y) for x in xs]


def build_world_s05_end():
    cpu = CPU(CPU_SIZE).move_to(CPU_HOME)
    ps = {}
    for n, p in zip("ABC", row_positions()):
        ps[n] = proc(n).move_to(p)
    return cpu, ps


S06_CPU = P3(3.5, 0.35)
S06_SPOTS = {n: P3(x, -1.25) for n, x in zip("ABC", (2.3, 3.5, 4.7))}   # centers (ready)
S06_VX = {"A": -5.2, "B": -3.5, "C": -1.8}


def center_bottom(name, center):
    """Bottom point of a ready process ``name`` centered at ``center``."""
    return proc(name).move_to(center).get_bottom()


def build_s06_parts(final=True):
    """Illusion split world. ``final`` adds the end-state extras (filled
    timeline, labels, gauges at ~33%)."""
    d = {}
    d["split"] = IllusionSplit()
    d["cpu"] = CPU(CPU_SIZE).move_to(S06_CPU)
    d["spots"] = {n: center_bottom(n, S06_SPOTS[n]) for n in "ABC"}   # bottoms
    d["ps"] = {n: bottom_to(proc(n), d["spots"][n]) for n in "ABC"}
    vcpus = VGroup()
    vps = {}
    for n in "ABC":
        c = CPU(1.0, label=None).move_to(P3(S06_VX[n], 0.6))
        make_translucent(c, 0.35, 0.7)
        vcpus.add(c)
        vp = proc(n, "running", scale=0.8)
        seat(vp, c)
        make_translucent(vp, 0.55, 0.7)
        vps[n] = vp
    d["vcpus"], d["vps"] = vcpus, vps
    d["tl"] = s06_timeline()
    d["vlabel"] = Text("virtual", font_size=24, color=DIM).move_to(P3(-3.5, -0.25))
    d["plabel"] = Text("physical", font_size=24, color=CPU_COLOR).next_to(d["cpu"], RIGHT, buff=0.35)
    d["gauges"] = VGroup(*[SpeedGauge(1.0, width=1.2).move_to(P3(S06_VX[n], -1.0)) for n in "ABC"])
    if final:
        fill_s06_timeline(d["tl"])
        d["ps"]["C"].set_expression("running")
        seat(d["ps"]["C"], d["cpu"])
        for g in d["gauges"]:
            bar, lab = g.value_targets(1 / 3, "~33%")
            g.bar.become(bar)
            g.label.become(lab)
    return d


def add_s06_world(scene, d, extras=True):
    scene.add(d["split"], d["vcpus"], *d["vps"].values(), d["cpu"], *d["ps"].values(), d["tl"])
    if extras:
        scene.add(d["vlabel"], d["plabel"], d["gauges"])


def s06_timeline():
    return Timeline(["A", "B", "C"], ticks=12, colors=[COL["A"], COL["B"], COL["C"]],
                    x_range=(1.0, 4.7), top=-2.25, row_height=0.28, row_step=0.34,
                    tick_labels=False, label_font=20)


S06_ORDER = ["A", "B", "C"] * 4


def fill_s06_timeline(tl, n=12):
    for t in range(1, n + 1):
        run = S06_ORDER[t - 1]
        for r in "ABC":
            tl.set_block(r, t, "running" if r == run else "ready")
    return tl


# ---- S09 machine state --------------------------------------------------
S09_CPU_POS = P3(-0.5, -0.2)


def s09_memory(colored=True):
    m = Memory(regions=["code", "static data", ("heap", 1.2), ("free", 1.6), ("stack", 1.4)],
               width=1.4, height=4.4, addresses=["0", "", "", "", ""], font_size=20)
    m.move_to(P3(-4.6, 0.2))
    if not colored:
        return m
    for name in ("code", "static data", "heap", "stack"):
        m.region(name).set_fill(COL["A"], 0.35).set_stroke(COL["A"], 3)
    m.region("free").set_fill(BG, 0).set_stroke(MEM_COLOR, 2)
    return m


S09_REGS = [("PC", "0x400"), ("SP", "0xff8"), ("FP", "0xffc"), ("eax", "42"),
            ("ebx", "7"), ("ecx", "0"), ("edx", "13"), ("esi", "99")]


def s09_registers():
    r = RegisterBank(S09_REGS, cols=2, box_width=1.35, box_height=0.42, font_size=20,
                     title="registers")
    r.move_to(P3(3.4, 1.3))
    return r


def s09_files():
    title = Text("open files", font_size=22, color=TEXT)
    rows = VGroup(*[Text(s, font=MONO_FONT, font_size=20, color=TEXT)
                    for s in ("0 stdin", "1 stdout", "2 stderr", "3 notes.txt")])
    rows.arrange(DOWN, buff=0.08, aligned_edge=LEFT)
    box = RoundedRectangle(width=2.8, height=rows.height + 0.3, corner_radius=0.08)
    box.set_fill(CARD_FILL, 1).set_stroke(DIM, 2)
    rows.move_to(box)
    rows.align_to(box, LEFT).shift(RIGHT * 0.25)
    title.next_to(box, UP, buff=0.1)
    g = VGroup(title, box, rows)
    g.move_to(P3(3.4, -1.6))
    g.rows = rows
    return g


def mem_pointer_tag(name, color, y, mem):
    x0 = mem.cells.get_right()[0]
    arr = Arrow(P3(x0 + 0.85, y), P3(x0 + 0.05, y), buff=0, stroke_width=4, tip_length=0.18,
                max_tip_length_to_length_ratio=0.4, color=color)
    t = Text(name, font=MONO_FONT, font_size=22, color=color, weight="BOLD").next_to(arr, RIGHT, buff=0.08)
    return VGroup(arr, t)


def build_s09_end():
    """Everything S09 leaves on screen (the S10 start state)."""
    cpu = CPU(CPU_SIZE).move_to(S09_CPU_POS)
    a = proc("A", "running")
    seat(a, cpu)
    mem = s09_memory()
    regs = s09_registers()
    for n, c in (("PC", CPU_COLOR), ("SP", MEM_COLOR), ("FP", USER_COLOR)):
        regs.boxes[n].set_stroke(c, 3).set_fill(c, 0.25)
        regs.name_texts[n].set_color(c)
    files = s09_files()
    slot = docked_save_slot()
    code, stack = mem.region("code"), mem.region("stack")
    mem.texts[mem.index_of("stack")].set_opacity(0)
    hl = Rectangle(width=code.width * 0.8, height=0.14).set_fill(CPU_COLOR, 0.9).set_stroke(width=0)
    hl.move_to(code.get_center() + DOWN * code.height * 0.28)
    fh = stack.height / 3.4
    frames = VGroup()
    for k, lab in enumerate(("ret addr", "locals", "params")):
        r = Rectangle(width=stack.width * 0.86, height=fh).set_fill(COL["A"], 0.6).set_stroke(TEXT, 1)
        r.move_to(stack.get_bottom() + UP * (fh * (k + 0.5) + 0.04))
        frames.add(VGroup(r, Text(lab, font_size=15, color=TEXT).move_to(r)))
    tags = VGroup(mem_pointer_tag("PC", CPU_COLOR, hl.get_y(), mem),
                  mem_pointer_tag("SP", MEM_COLOR, frames[2].get_top()[1], mem),
                  mem_pointer_tag("FP", USER_COLOR, frames[1].get_top()[1] - 0.02, mem))
    aspace = DashedVMobject(SurroundingRectangle(mem.cells, buff=0.1, corner_radius=0.08),
                            num_dashes=44).set_stroke(COL["A"], 3)
    link = DashedLine(cpu.get_left(), mem.cells.get_right(), dash_length=0.1).set_stroke(COL["A"], 2)
    panels = VGroup(mem, hl, frames, tags, aspace, link, regs, files)
    return dict(cpu=cpu, a=a, mem=mem, regs=regs, files=files, slot=slot, panels=panels)


# ---- S11/S12 Figure 4.1 -------------------------------------------------
S11_CPU_POS = P3(-2.6, 1.6)
S11_MEM_POS = P3(2.6, 1.3)
S11_DISK_POS = P3(0, -2.4)
BUS_Y = -0.6


def s11_memory():
    m = Memory(regions=["code", "static data", ("heap", 0.9), ("free", 1.5), ("stack", 1.1)],
               width=1.4, height=3.4, addresses=["0", "", "", "", ""], font_size=18)
    m.move_to(S11_MEM_POS)
    for t in m.texts:
        t.set_opacity(0)
    return m


def s11_bus(cpu, mem, disk):
    return Bus(y=BUS_Y, x_range=(-5, 5),
               taps=[cpu.get_bottom() + DOWN * 0.15, mem.get_bottom(), disk.get_top() + UP * 0.02])


def build_s11_end():
    cpu = CPU(CPU_SIZE).move_to(S11_CPU_POS)
    mem = s11_memory()
    disk = Disk().move_to(S11_DISK_POS)
    bus = s11_bus(cpu, mem, disk)
    for name in ("code", "static data"):
        mem.region(name).set_fill(COL["D"], 0.6).set_stroke(MEM_COLOR, 3)
        mem.texts[mem.index_of(name)].set_opacity(1)
    outline = DashedVMobject(SurroundingRectangle(mem.cells, buff=0.12, corner_radius=0.08),
                             num_dashes=40).set_stroke(COL["D"], 3)
    olab = Text("address space of D", font_size=20, color=COL["D"]).next_to(outline, UP, buff=0.08)
    tag = step_tag(1, "load")
    file = s11_file()
    return dict(cpu=cpu, mem=mem, disk=disk, bus=bus, outline=outline, olab=olab, tag=tag, file=file)


S11_FILE_POS = P3(1.45, -2.35)
S11_TERM_AT = P3(0, 1.9)


def s11_file():
    return FileIcon("program", width=0.55).move_to(S11_FILE_POS)


def step_tag(i, name):
    t = Text(f"{i} / 5 · {name}", font_size=26, color=TEXT)
    box = RoundedRectangle(width=t.width + 0.4, height=t.height + 0.25, corner_radius=0.1)
    box.set_fill(CARD_FILL, 1).set_stroke(VIRT, 2.5).move_to(t)
    return VGroup(box, t).move_to(P3(0, 3.2))


# ---- S13 state diagram ---------------------------------------------------
def make_state_diagram():
    chip = CPU(size=0.75, label=None, pins=3)
    sd = StateDiagram(running_icon=chip, font_size=30, arrow_font=24)
    sd.disk_icon = None
    return sd


SD_PROC_SCALE = 0.55


def sd_proc(name, expr="ready", label=None):
    return proc(name, expr, scale=SD_PROC_SCALE, label=label)


def build_s13_end():
    """Complete diagram; A running, B and D ready. Returns dict."""
    sd = make_state_diagram()
    disk = Disk(width=0.9, height=0.75).move_to(P3(2.4, -2.6))
    a = sd_proc("A", "running")
    b = sd_proc("B")
    dd = sd_proc("D")
    bottom_to(a, sd.zone_points("running", 1)[0])
    pts = sd.zone_points("ready", 2)
    bottom_to(b, pts[0])
    bottom_to(dd, pts[1])
    return dict(sd=sd, disk=disk, a=a, b=b, d=dd)


# ---- S14-S16 traces ------------------------------------------------------
TRACE_CPU_POS = P3(-3.2, 1.0)
TRACE_P0_SPOT = P3(-1.4, 0.45)     # bottoms of the waiting spots beside the CPU
TRACE_P1_SPOT = P3(-0.2, 0.45)
LEGEND_POS = (4.1, 1.9)
LEGEND_SCALE = 0.42


TRACE_X0 = -3.8
TRACE_TICK_W = 0.82


def trace_x_range(ticks):
    return (TRACE_X0, TRACE_X0 + TRACE_TICK_W * ticks)


def trace_timeline(ticks=8):
    return Timeline(["P0", "P1"], ticks=ticks, colors=[COL["P0"], COL["P1"]], x_range=trace_x_range(ticks),
                    top=-1.2, row_height=0.45, row_step=0.6, cpu_row=True, tick_label_y=None,
                    label_font=24, tick_font=20)


def work_bar(cells, color, cell=0.18):
    """'work: ▮▮▮▮' as small cells. ``cells`` is a list of 'w' (work) / 'io' / gap."""
    lab = Text("work:", font_size=18, color=DIM)
    g = VGroup()
    for c in cells:
        if c == "io":
            t = Text("I/O", font_size=14, color=DIM)
            g.add(t)
        else:
            r = Rectangle(width=cell, height=cell * 1.3).set_fill(color, 1).set_stroke(TEXT, 1)
            g.add(r)
    g.arrange(RIGHT, buff=0.05)
    bar = VGroup(lab, g).arrange(RIGHT, buff=0.1)
    bar.cells = g
    return bar


def build_trace_world(ticks=8):
    """CPU + P0/P1 beside it + legend (with tracking dots) + empty timeline."""
    cpu = CPU(1.2).move_to(TRACE_CPU_POS)
    p0 = proc("P0", scale=0.8)
    p1 = proc("P1", scale=0.8)
    bottom_to(p0, TRACE_P0_SPOT)
    bottom_to(p1, TRACE_P1_SPOT)
    sd = make_state_diagram()
    sd.set_legend(LEGEND_POS, LEGEND_SCALE)
    d0 = sd.make_dot(COL["P0"], label="0", radius=0.13)
    d1 = sd.make_dot(COL["P1"], label="1", radius=0.13)
    sd.place_dot(d0, "ready").place_dot(d1, "ready")
    tl = trace_timeline(ticks)
    return dict(cpu=cpu, p0=p0, p1=p1, sd=sd, d0=d0, d1=d1, tl=tl)


# Figure 4.4 (P0, P1 per tick; None = not present/done)
FIG44_P0 = ["running"] * 3 + ["blocked"] * 3 + ["ready"] * 2 + ["running"] * 2
FIG44_P1 = ["ready"] * 3 + ["running"] * 5 + [None, None]


# ---- S17 process list ----------------------------------------------------
S17_SD_POS = P3(-3.6, 0.4)
S17_SD_SCALE = 0.7
PCB_YS = [2.15, 1.05, -0.05, -1.15]
PCB_X = 3.75


def s17_os_box():
    b = RoundedRectangle(width=4.2, height=5.05, corner_radius=0.2).move_to(P3(3.75, 0.52))
    return b.set_stroke(KERNEL_COLOR, 2.5).set_fill(KERNEL_COLOR, 0.03)


def s17_os_label(box):
    return Text("OS", font_size=24, color=KERNEL_COLOR, weight="BOLD").next_to(box.get_corner(UL), DR, buff=0.1)


def pcb_for(name, state, pid, extra=None):
    fields = [("pid", str(pid)), ("state", state), ("mem", "…"), ("files", "…")]
    if extra:
        fields[2] = extra
    return PCBCard(name, COL[name], fields, width=3.3, height=1.0, font_size=18, col_widths=(0.42, 0.58))


def build_s17_end():
    sd = make_state_diagram()
    sd.arrow_label_group.set_opacity(1)
    sd.scale(S17_SD_SCALE).move_to(S17_SD_POS)
    ps = {}
    a = sd_proc("A", "running").scale(S17_SD_SCALE)
    bottom_to(a, sd.zone_points("running", 1)[0])
    b = sd_proc("B").scale(S17_SD_SCALE)
    dd = sd_proc("D").scale(S17_SD_SCALE)
    c = sd_proc("C", "ready").scale(S17_SD_SCALE)
    rp = sd.zone_points("ready", 3, spacing=sd.radius * 0.62)
    for m, p in zip((b, dd, c), rp):
        bottom_to(m, p)
    ps = dict(A=a, B=b, C=c, D=dd)
    os_box = s17_os_box()
    os_box.set_stroke(KERNEL_COLOR, 2.5).set_fill(KERNEL_COLOR, 0.03)
    os_lab = s17_os_label(os_box)
    cards = {
        "A": pcb_for("A", "running", 1),
        "B": pcb_for("B", "ready", 2),
        "D": pcb_for("D", "ready", 4),
        "C": pcb_for("C", "ready", 3, ("wait", "—")),
    }
    for (n, card), y in zip(cards.items(), PCB_YS):
        card.move_to(P3(PCB_X, y))
    brace, blab = s17_brace(cards)
    return dict(sd=sd, ps=ps, os_box=os_box, os_lab=os_lab, cards=cards, brace=brace, blab=blab)


def s17_brace(cards):
    g = VGroup(*cards.values())
    brace = Brace(g, LEFT, color=KERNEL_COLOR, buff=0.12)
    lab = Text("process\nlist", font_size=22, color=KERNEL_COLOR, line_spacing=0.8).next_to(brace, LEFT, buff=0.28)
    return brace, lab


# ---- S18 xv6 struct ------------------------------------------------------
XV6_PROC = """struct proc {
  char *mem;
  uint sz;
  enum proc_state state;
  int pid;
  struct proc *parent;
  struct file *ofile[NOFILE];
  struct context context;
  ...
};"""
XV6_ENUM = """enum proc_state { UNUSED, EMBRYO,
  SLEEPING, RUNNABLE, RUNNING, ZOMBIE };"""


def code_block(src, font_size=20, line_numbers=False):
    c = Code(code_string=src, language="c", formatter_style="monokai", add_line_numbers=line_numbers,
             background="rectangle",
             background_config={"fill_color": "#272822", "stroke_color": DIM, "stroke_width": 2,
                                "corner_radius": 0.15, "buff": 0.25},
             paragraph_config={"font": MONO_FONT, "font_size": font_size, "line_spacing": 0.6})
    return c


def code_line_bar(code, i, color=CPU_COLOR, opacity=0.25):
    line = code.code_lines[i]
    bg = code.background
    bar = Rectangle(width=bg.width - 0.15, height=max(line.height, 0.22) + 0.1)
    bar.move_to(P3(bg.get_x(), line.get_y())).set_fill(color, opacity).set_stroke(color, 1.5, opacity=0.8)
    return bar


# ---- S20 laptop world ----------------------------------------------------
S20_CPU = P3(0, 0.65)
S20_QUEUE_C = (-1.3, -0.6)
S20_BLOCK_SPOT = P3(0.95, -0.55)     # bottom of the blocked spot (next to the disk)
S20_DISK = P3(1.6, -0.45)
S20_PROC_SCALE = 0.45
S20_LIST_X = 5.0
S20_LIST_YS = [1.45, 0.8, 0.15, -0.5]


def s20_mini_pcb(name, state):
    return PCBCard(name, COL[name], [("state", state)], width=2.4, height=0.5, cols=1, font_size=16,
                   header_width=0.42, title_font=22)


def build_s20_world():
    """The laptop world of S20 in its starting arrangement (A running, B and C
    ready, D blocked). Returns a dict."""
    laptop = Laptop(width=6).move_to(P3(0, 0.3))
    counter, num, cnum = counter_group(137, 1)
    cpu = CPU(0.7, label=None, pins=3).move_to(S20_CPU)
    q = Queue(label=None, center=S20_QUEUE_C, slots=3, spacing=0.55)
    disk = Disk(width=0.6, height=0.5).move_to(S20_DISK)
    ps = {n: proc(n, scale=S20_PROC_SCALE) for n in "ABCD"}
    ps["A"].set_expression("running")
    seat(ps["A"], cpu)
    q.place(ps["B"], ps["C"])
    ps["D"].set_expression("blocked")
    bottom_to(ps["D"], S20_BLOCK_SPOT)
    states = {"A": "running", "B": "ready", "C": "ready", "D": "blocked"}
    cards = {n: s20_mini_pcb(n, states[n]).move_to(P3(S20_LIST_X, y)) for n, y in zip("ABCD", S20_LIST_YS)}
    list_lab = Text("process list", font_size=22, color=KERNEL_COLOR).next_to(cards["A"], UP, buff=0.15)
    brace = Brace(VGroup(*cards.values()), LEFT, color=KERNEL_COLOR, buff=0.1)
    tl = Timeline(list("ABCD"), ticks=10, colors=[COL[n] for n in "ABCD"], x_range=(-3.0, 3.0), top=-1.95,
                  row_height=0.17, row_step=0.21, tick_labels=False, label_font=14)
    return dict(laptop=laptop, counter=counter, cpu=cpu, q=q, disk=disk, ps=ps, cards=cards,
                list_lab=list_lab, brace=brace, tl=tl, states=states)


# ---- S10 process menu ----------------------------------------------------
S10_CPU = P3(2.2, -0.6)
S10_SIDE = P3(4.3, 0.15)     # center of the process beside the CPU


# ---- S15/S16 trace with I/O ----------------------------------------------
TRACE_DISK_POS = P3(-3.2, -0.38)
TRACE_BLOCK_SPOT = P3(-1.95, -0.85)     # bottom of P0's waiting spot beside the disk
TRACE_COMP_POS = P3(1.7, 0.4)
P0_IO_BAR = ["w", "w", "w", "io", "w", "w"]


def trace_disk():
    return Disk(width=1.0, height=0.8).move_to(TRACE_DISK_POS)


def io_tag(disk):
    return Text("I/O: 3 ticks", font_size=20, color=DIM).next_to(disk, LEFT, buff=0.15)


def build_s15_end():
    t = build_trace_world(10)
    cpu, p0, p1, tl, sd = t["cpu"], t["p0"], t["p1"], t["tl"], t["sd"]
    p0.set_expression("running")
    seat(p0, cpu)
    for k in range(1, 4):
        tl.set_block("P0", k, "running")
        tl.set_block("P1", k, "ready")
        tl.set_block("CPU", k, "busy")
    sd.place_dot(t["d0"], "running")
    disk = trace_disk()
    bar = work_bar(P0_IO_BAR, COL["P0"]).next_to(cpu, LEFT, buff=0.25).shift(UP * 0.9)
    for k in range(3):
        bar.cells[k].set_fill(opacity=0.1)
    packet = Square(0.14).set_fill(CPU_COLOR, 1).set_stroke(TEXT, 1).move_to(disk.top_point() + RIGHT * 0.25)
    comp = Computer("idle").scale(0.6).move_to(TRACE_COMP_POS)
    t.update(disk=disk, bar=bar, packet=packet, comp=comp, iotag=io_tag(disk))
    return t


# ---- S21/S22 recap --------------------------------------------------------
RECAP_ITEMS = [
    "1.  A process is a running program.",
    "2.  Time sharing the CPU creates the illusion of many CPUs, at the cost of performance.",
    "3.  Mechanisms answer how; policies answer which.",
    "4.  A process is its machine state: address space, registers, open files.",
    "5.  Processes move between running, ready and blocked, and the OS tracks them all in the process list.",
]


def recap_header():
    return Text("Recap", font_size=44, color=VIRT, weight="BOLD").move_to(P3(-6.0, 2.85), aligned_edge=LEFT)


def recap_lines():
    lines = VGroup(*[Text(wrap_text(s, 7.6, 28), font_size=28, color=TEXT, line_spacing=0.75) for s in RECAP_ITEMS])
    lines.arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to(P3(-6.0, 2.3), aligned_edge=UL)
    if lines.get_bottom()[1] < -3.3:
        lines.scale_to_fit_height(5.5).move_to(P3(-6.0, 2.3), aligned_edge=UL)
    return lines
