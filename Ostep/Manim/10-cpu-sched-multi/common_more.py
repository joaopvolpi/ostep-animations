"""More episode-10 builders (state at the end of earlier scenes)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


def build_s02_end():
    """Laptop (scaled 0.8 at y=1.0) with eight lit chips and threads, stopwatch 8x, characters,
    and four other processes around it."""
    w = build_s01_end()
    lap, chips = w["lap"], w["chips"]
    cores = label("8 cores", 26)
    threads = [make_thread("", COL["A"], scale=0.4) for _ in chips]
    laptop = VGroup(lap, chips)
    laptop.scale(0.8).move_to(P3(0, 1.0))
    cores.move_to(P3(0, 2.3))
    for c in chips:
        c.become(mini_chip(True, size=0.32 * 0.8).move_to(c))
    for t, c in zip(threads, chips):
        place_on(t, c.get_top() + DOWN * 0.04)
    sw = stopwatch("8×", 24).move_to(P3(4.3, 1.0))
    others = [proc(n, "ready", 0.4) for n in "BCDE"]
    for p, pt in zip(others, [P3(-3.9, -1.2), P3(-3.2, -1.2), P3(3.2, -1.2), P3(3.9, -1.2)]):
        place_on(p, pt)
    return dict(lap=lap, chips=chips, threads=threads, cores=cores, sw=sw, others=others,
                stu=student_corner("neutral"), prof=prof_corner("neutral"))


# ---------------------------------------------------------------------------
# S04 world: one CPU + cache + memory
# ---------------------------------------------------------------------------
S04_X = -1.5
S04_CHIP_Y = 1.3
READ_MEM_Y, READ_CACHE_Y = -1.8, -0.1


def make_main_memory(x=0.0, y=-1.9, vals=("7", "3", "5", "1"), width=1.2, height=1.6, title=None):
    m = Memory(cells=4, contents=list(vals), width=width, height=height, addresses=False, font_size=20,
               title=title)
    m.move_to(P3(x, y))
    return m


def readout_group(kind):
    """The S04 readouts: memory ~ 100 ns and cache ~ a few ns."""
    sw = stopwatch_icon(radius=0.28)
    if kind == "mem":
        parts = VGroup(label("memory", 24), MathTex(r"\approx", color=TEXT).scale(0.8),
                       label("100 ns", 24, KERNEL_COLOR))
    else:
        parts = VGroup(label("cache", 24), MathTex(r"\approx", color=TEXT).scale(0.8),
                       label("a few ns", 24, CPU_COLOR))
    parts.arrange(RIGHT, buff=0.15)
    return VGroup(sw, parts).arrange(RIGHT, buff=0.2)


def cache_with(cc, cell, value, color):
    """Instantly put ``value`` into a cache cell."""
    cc.cells[cell].set_fill(color, 0.75).set_stroke(outline_of(color), 2)
    cc.texts[cell].become(Text(str(value), font=MONO_FONT, font_size=max(10, int(17 * cc.k)),
                               color=INK).move_to(cc.cells[cell]))
    cc.used = max(cc.used, cell + 1)
    return cc


def build_s04_end():
    cc = cpu_at(S04_X, S04_CHIP_Y, "CPU")
    cache_with(cc, 0, "7", COL["A"])
    mem = make_main_memory(S04_X)
    ro1 = readout_group("mem").move_to(P3(3.4, READ_MEM_Y))
    ro2 = readout_group("cache").move_to(P3(3.4, READ_CACHE_Y))
    return dict(cc=cc, mem=mem, ro1=ro1, ro2=ro2)


X1, X2, CHIP_Y, BUS_Y = -2.8, 2.8, 1.3, -0.8


def two_cpu_stage(with_a=False):
    """Two CacheCPUs, bus, memory (cell 0 = 0x40 -> 7)."""
    c1, c2 = cpu_at(X1, CHIP_Y, "CPU 1"), cpu_at(X2, CHIP_Y, "CPU 2")
    mem = Memory(cells=4, contents=["7", "3", "5", "1"], width=1.2, height=1.6, addresses=["0x40", "0x44", "0x48", "0x4C"],
                 font_size=20).move_to(P3(0, -2.2))
    bus = Bus(y=BUS_Y, x_range=(-4.4, 4.4), taps=[c1.cache_bottom(), c2.cache_bottom(), mem.get_top()])
    bus_lab = label("Bus", 24, DIM).move_to(P3(5.0, BUS_Y))
    return c1, c2, mem, bus, bus_lab


def build_s06_end():
    c1, c2, mem, bus, bus_lab = two_cpu_stage()
    cache_with(c1, 0, "9", COL["A"])
    cache_with(c2, 0, "7", COL["A"])
    a = proc("A", "running", 0.5)
    place_on(a, c2.slot_point())
    neq = MathTex(r"7\neq 9", color=KERNEL_COLOR).scale(1.8).move_to(P3(0, 1.3))
    stale = DashedVMobject(Rectangle(width=1.3, height=0.5).move_to(mem.cell(0)).set_stroke(KERNEL_COLOR, 4))
    stale_t = label("stale!", 22, KERNEL_COLOR).next_to(mem.cell(0), RIGHT, buff=0.55)
    return dict(c1=c1, c2=c2, mem=mem, bus=bus, bus_lab=bus_lab, a=a, neq=neq, stale=stale, stale_t=stale_t)



# ---------------------------------------------------------------------------
# Four-CPU stage (S11-S13) and two-CPU MQMS stage (S14-S18)
# ---------------------------------------------------------------------------
SQ_XS = [-4.5, -1.5, 1.5, 4.5]
SQ_CHIP_Y = 1.1


def four_cpus(y=SQ_CHIP_Y):
    return [cpu_at(x, y, f"CPU {i}") for i, x in enumerate(SQ_XS)]


def job_queue(jobs="ABCDE", center=(0, -1.15), label_text="the queue", spacing=1.0, scale=0.5, slots=None):
    q = Queue(label=label_text, center=center, slots=slots or max(len(jobs), 1), spacing=spacing)
    ps = [proc(j, "ready", scale) for j in jobs]
    q.place(*ps)
    return q, ps


def grid_colors():
    return dict(COL)


# --- MQMS stage (two CPUs, two queues, 2 x N grid) ---------------------------
MQ_X = (-3.0, 3.0)
MQ_CHIP_Y = 1.4
MQ_Q_Y = -0.8
MQ_GRID_AT = P3(0.2, -2.35)


def hop_mover(m, pt, **kw):
    return hop_to(m, pt, run_time=kw.pop("run_time", 0.7), height=0.12)


def mq_stage(items0="AC", items1="BD", cols=12, cell_w=0.6, fill_grid=None):
    c0, c1 = cpu_at(MQ_X[0], MQ_CHIP_Y, "CPU 0"), cpu_at(MQ_X[1], MQ_CHIP_Y, "CPU 1")
    q0 = Queue(label="Q0", center=(MQ_X[0], MQ_Q_Y), slots=3, spacing=0.9, mover=hop_mover)
    q1 = Queue(label="Q1", center=(MQ_X[1], MQ_Q_Y), slots=3, spacing=0.9, mover=hop_mover)
    p0 = [proc(j, "ready", 0.4) for j in items0]
    p1 = [proc(j, "ready", 0.4) for j in items1]
    q0.place(*p0)
    q1.place(*p1)
    grid = ScheduleGrid(rows=2, columns=cols, cell_w=cell_w, cell_h=0.5, colors=grid_colors(), label_size=18,
                        letter_size=20).move_to(MQ_GRID_AT)
    if fill_grid:
        for r, row in enumerate(fill_grid):
            grid.set_row(r, row)
    return dict(c0=c0, c1=c1, q0=q0, q1=q1, p0=p0, p1=p1, grid=grid)


def cpu_power(cc, lit, run_time=0.8):
    """Animation: the chip of a CacheCPU lights up (CPU_COLOR) or goes dark."""
    new = CPU(size=cc.cpu.size, label=cc.cpu.label.text,
              color=CPU_COLOR if lit else mix(CPU_COLOR, BG, 0.8), font_size=max(12, int(22 * cc.k)))
    new.move_to(cc.cpu)
    return Transform(cc.cpu, new, run_time=run_time)


def set_cpu_power(cc, lit):
    """Instant version of cpu_power."""
    new = CPU(size=cc.cpu.size, label=cc.cpu.label.text,
              color=CPU_COLOR if lit else mix(CPU_COLOR, BG, 0.8), font_size=max(12, int(22 * cc.k)))
    new.move_to(cc.cpu)
    cc.cpu.become(new)
    return cc
