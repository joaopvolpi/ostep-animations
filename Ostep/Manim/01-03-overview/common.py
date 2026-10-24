"""Episode 01-03 (Overview): constants, persistent assignments and shared builders."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

import numpy as np  # noqa: E402
from manim import *  # noqa: E402,F403
from ostep_lib import *  # noqa: E402,F403

# --------------------------------------------------------------------------
# Persistent assignments
# --------------------------------------------------------------------------
A_COLOR, B_COLOR, C_COLOR, D_COLOR = PROCESS_COLORS[:4]
ABCD_COLORS = PROCESS_COLORS[:4]
PID1_COLOR, PID2_COLOR = PROCESS_COLORS[4], PROCESS_COLORS[5]
T1_COLOR, T2_COLOR = PROCESS_COLORS[1], PROCESS_COLORS[3]

CPU_HOME = np.array([0, 0.6, 0])
CORNER_SCALE = 0.75
STU_CORNER = np.array([-5.8, -2.8, 0])
PROF_CORNER = np.array([5.8, -2.8, 0])
STU_DIALOG = np.array([-2.6, -1.2, 0])
PROF_DIALOG = np.array([2.6, -1.2, 0])

BADGE_TEXT = "01–03 · Overview"
PIECES = [("Virtualization", VIRT), ("Concurrency", CONC), ("Persistence", PERS)]
CARD_XS = (-4, 0, 4)
CARD_Y = 1.0
CARD_W, CARD_H = 3.2, 1.6

GOOD = "#8BE07A"   # = ov_icons.OK_GREEN
BAD = "#FF5A5A"    # = ov_icons.BAD_RED


# --------------------------------------------------------------------------
# Hosts
# --------------------------------------------------------------------------
def make_hosts(mode="corner", stu_expr="neutral", prof_expr="neutral"):
    """Student (facing right) and Professor (flipped, facing left) in a mode."""
    stu = Student(stu_expr)
    prof = Professor(prof_expr).flip()
    stu.mode_scale = 1.0
    prof.mode_scale = 1.0
    if mode == "corner":
        stu.scale(CORNER_SCALE).move_to(STU_CORNER)
        prof.scale(CORNER_SCALE).move_to(PROF_CORNER)
        stu.mode_scale = prof.mode_scale = CORNER_SCALE
    else:
        stu.move_to(STU_DIALOG)
        prof.move_to(PROF_DIALOG)
    stu.set_look(prof)
    prof.set_look(stu)
    return stu, prof


def mode_anims(stu, prof, mode, run_time=1.0):
    """Glide both hosts to 'corner' or 'dialog' mode (returns a list of animations)."""
    s = CORNER_SCALE if mode == "corner" else 1.0
    out = []
    for ch, pos in ((stu, STU_CORNER if mode == "corner" else STU_DIALOG),
                    (prof, PROF_CORNER if mode == "corner" else PROF_DIALOG)):
        f = s / getattr(ch, "mode_scale", 1.0)
        ch.mode_scale = s
        out.append(ch.animate(run_time=run_time).scale(f).move_to(pos))
    return out


def center_base(ch, center):
    """Base point ``ch`` would have if its center were at ``center``."""
    return base_point(ch) - ch.get_center() + np.array(center, dtype=float)


def badge(accent=INTRO):
    return SectionBadge(BADGE_TEXT, accent=accent)


def terms(accent=INTRO):
    return TermHighlight(accent=accent)


def bubble_kw(font_size=26, max_width=4.0):
    return dict(font_size=font_size, max_width=max_width)


# --------------------------------------------------------------------------
# S01-S03: title and piece cards
# --------------------------------------------------------------------------
def make_title():
    a = Text("Operating Systems:", font_size=44, color=TEXT)
    b = Text("Three Easy Pieces", font_size=44, color=TEXT)
    t = VGroup(a, b).arrange(RIGHT, buff=0.25, aligned_edge=DOWN).move_to([0, 2.6, 0])
    credit = Text("Remzi H. Arpaci-Dusseau & Andrea C. Arpaci-Dusseau · free at ostep.org",
                  font_size=22, color=DIM).next_to(t, DOWN, buff=0.25)
    return t, credit


def small_title(title):
    """Target for the title after S02.1: (0, 3.3), font 28."""
    return title.copy().scale(28 / 44).move_to([0, 3.3, 0])


def mini_cpu_icon():
    cpu = CPU(size=0.42, label=None, pins=2)
    p = Process("running", color=A_COLOR).scale(0.26)
    cpu.seat(p)
    return VGroup(cpu, p)


def mini_mem_icon():
    m = Memory(cells=4, width=0.36, height=0.56, addresses=False)
    spill = VGroup(*[Rectangle(width=0.36, height=0.14).set_fill(MEM_COLOR, 0.5).set_stroke(MEM_COLOR, 2)
                     for _ in range(2)])
    spill[0].next_to(m, UP, buff=0.02).rotate(-0.35).shift(RIGHT * 0.12)
    spill[1].next_to(m, RIGHT, buff=0.02).align_to(m, UP).rotate(-0.9).shift(DOWN * 0.08)
    for c in m.cells:
        c.set_fill(MEM_COLOR, 0.5)
    return VGroup(m, spill)


def mini_conc_icon():
    """Two threads reaching for one shared cell (the concurrency card's icon)."""
    t1 = make_thread("", T1_COLOR, 0.24)
    t2 = make_thread("", T2_COLOR, 0.24)
    row = VGroup(t1, t2).arrange(RIGHT, buff=0.22)
    cell = Rectangle(width=0.34, height=0.22).set_fill(MEM_COLOR, 0.6).set_stroke(MEM_COLOR, 2)
    cell.next_to(row, DOWN, buff=0.12)
    links = VGroup(*[Line(t.get_bottom() + DOWN * 0.02, cell.get_top() + RIGHT * dx, buff=0).set_stroke(DIM, 2)
                     for t, dx in ((t1, -0.07), (t2, 0.07))])
    g = VGroup(row, links, cell)
    g.threads, g.cell = row, cell
    return g


def mini_disk_icon():
    return Disk(width=0.62, height=0.55)


def piece_card(i, w=CARD_W, h=CARD_H):
    name, col = PIECES[i]
    r = RoundedRectangle(width=w, height=h, corner_radius=0.18).set_fill(col, 0.15).set_stroke(col, 4)
    lab = Text(name, font_size=30, color=TEXT)
    lab.move_to(r.get_top() + DOWN * 0.38)
    g = VGroup(r, lab)
    g.frame, g.label = r, lab
    g.icons = VGroup()
    g.add(g.icons)
    return g


def icon_slot(card, k=0, n=1):
    """Where the k-th of n mini icons sits inside a card."""
    c = card.frame.get_center() + DOWN * 0.33
    if n == 1:
        return c
    return c + RIGHT * (k - (n - 1) / 2) * 0.9


def piece_cards(with_icons=True):
    cards = VGroup(*[piece_card(i).move_to([x, CARD_Y, 0]) for i, x in enumerate(CARD_XS)])
    if with_icons:
        cards[0].icons.add(mini_cpu_icon().move_to(icon_slot(cards[0], 0, 2)),
                           mini_mem_icon().move_to(icon_slot(cards[0], 1, 2)))
        cards[1].icons.add(mini_conc_icon().move_to(icon_slot(cards[1])))
        cards[2].icons.add(mini_disk_icon().move_to(icon_slot(cards[2])))
    return cards


def card_strip(cards):
    """S03 layout: cards shrunk (x0.45) into a strip at y = 3.0 (returns a target copy)."""
    t = cards.copy().scale(0.45)
    t.move_to([0, 3.0, 0])
    return t


def motto_lines():
    rows = [("I hear", "I forget", DIM), ("I see", "I remember", TEXT), ("I do", "I understand", TEXT)]
    lines = VGroup()
    for a, b, c in rows:
        lines.add(Text(f"{a} → {b}", font_size=36, color=c))
    lines.arrange(DOWN, buff=0.32).move_to([0, 1.55, 0])
    return lines


def glow_for(text_mob, color=INTRO):
    g = VGroup()
    for w, o in ((14, 0.10), (8, 0.18)):
        c = text_mob.copy().set_fill(opacity=0).set_stroke(color, w, opacity=o)
        g.add(c)
    return g


# --------------------------------------------------------------------------
# S04: fetch / decode / execute world
# --------------------------------------------------------------------------
INSTRUCTIONS = ["add r1, r2", "load r3, [x]", "cmp r3, 0", "jmp f", "sub r1, 1",
                "store [y], r1", "call g", "ret"]
S04_CPU_POS = np.array([-2.8, 0.4, 0])
S04_MEM_POS = np.array([2.8, 0.4, 0])


def s04_cpu():
    return CPU(size=1.6).move_to(S04_CPU_POS)


def s04_memory():
    return Memory(cells=8, contents=INSTRUCTIONS, width=1.9, height=4.4, font_size=18,
                  addresses=[f"{4 * i:02d}" for i in range(8)]).move_to(S04_MEM_POS)


def other_program(k):
    """A second/third program's instruction list (S04.11), stacked to the right."""
    texts = [["mov r1, 7", "add r1, r1", "jmp h", "ret"], ["load r2, [z]", "cmp r2, 1", "call k", "ret"]][k]
    m = Memory(cells=4, contents=texts, width=1.6, height=2.0, font_size=15, addresses=False)
    return m


def s04_end_world():
    """Exact S04 end state: cpu (label hidden), memory, the two other programs, plus
    (ring, pc, aims) which S05 fades out."""
    cpu = s04_cpu()
    cpu.label.set_opacity(0.0)
    mem = s04_memory()
    p2, p3 = other_program(0), other_program(1)
    p2.move_to([5.2, 1.5, 0])
    p3.move_to([5.2, -0.75, 0])
    for p in (p2, p3):
        for c in p.cells:
            c.set_stroke(DIM)
    aims = VGroup(*[DashedLine(p.get_left(), cpu.get_right() + RIGHT * 0.1, dash_length=0.12)
                    .add_tip(tip_length=0.18).set_color(DIM) for p in (p2, p3)])
    aims.set_z_index(-1)
    ring = fde_ring([-2.8, -1.8, 0])
    for b_ in ring.boxes:
        b_[0].set_stroke(DIM).set_fill(CARD_FILL, 1)
        b_[1].set_color(DIM)
    pc = pc_arrow(mem, 7)
    return cpu, mem, VGroup(p2, p3), VGroup(ring, pc, aims)


# --------------------------------------------------------------------------
# S05/S06: system stack
# --------------------------------------------------------------------------
PROG_XS = (-3, 0, 3)
PROG_Y = 0.8


def make_stack():
    return SystemStack(hw_y=-2.3, band_y=-0.9, programs_y=PROG_Y, hw_x=(-3, 0, 3), band_width=10,
                       cpu_size=0.84, mem_size=(0.9, 1.4), disk_width=1.1)


def stack_programs():
    ps = VGroup()
    for i, x in enumerate(PROG_XS):
        p = Process(color=ABCD_COLORS[i], label="ABC"[i]).scale(0.8)
        place_on(p, [x, PROG_Y - 0.45, 0])
        ps.add(p)
    return ps


# --------------------------------------------------------------------------
# S07/S08: peach world
# --------------------------------------------------------------------------
EATER_XS = (-3.6, -1.2, 1.2, 3.6)
EATER_Y = 0.4
PEACH_HOME = np.array([0, 0.4, 0])
TABLE_Y = -0.2


def make_eaters():
    es = VGroup()
    for i, x in enumerate(EATER_XS):
        e = Process(color=ABCD_COLORS[i]).scale(0.8)
        place_on(e, [x, TABLE_Y, 0])
        es.add(e)
    return es


def virtual_peach_for(eater, scale=0.7):
    v = Peach().virtual_copy().scale(scale)
    side = RIGHT if eater.get_center()[0] < 0 else LEFT
    v.move_to(eater.get_center() + side * 0.85 + UP * 0.15)
    return v


# --------------------------------------------------------------------------
# S09-S10: cpu demo
# --------------------------------------------------------------------------
CPU_C = '''char *str = argv[1];
while (1) {
    Spin(1);
    printf("%s\\n", str);
}'''


def code_block(src, font_size=20, language="c"):
    c = Code(code_string=src, language=language, formatter_style="monokai", add_line_numbers=False,
             background="rectangle", paragraph_config={"font": MONO_FONT, "font_size": font_size},
             background_config={"stroke_color": DIM, "stroke_width": 2, "fill_color": "#272822",
                                "corner_radius": 0.15, "buff": 0.25})
    return c


def code_title(code, text):
    return Text(text, font=MONO_FONT, font_size=22, color=DIM).next_to(code, UP, buff=0.15).align_to(code, LEFT)


def line_bar(code, i, color=CPU_COLOR, opacity=0.25):
    """Highlight bar behind line ``i`` of a Code mobject."""
    line = code.code_lines[i] if hasattr(code, "code_lines") else code[1][i]
    bg = code[0]
    bar = Rectangle(width=bg.width - 0.1, height=line.height + 0.12)
    bar.set_fill(color, opacity).set_stroke(width=0)
    bar.move_to([bg.get_center()[0], line.get_center()[1], 0])
    return bar


CPU_ORDER = "ABDCABDCA"


def mini_timeline(x0=1.0, x1=6.3, y=-2.2, n=9, h=0.4):
    axis = Line([x0, y - h / 2 - 0.05, 0], [x1, y - h / 2 - 0.05, 0]).set_stroke(DIM, 2)
    lab = Text("time →", font_size=16, color=DIM).next_to(axis, DOWN, buff=0.08).align_to(axis, RIGHT)
    g = VGroup(axis, lab)
    g.x0, g.x1, g.y, g.n, g.h = x0, x1, y, n, h
    return g


def timeline_slot(tl, k, color):
    w = (tl.x1 - tl.x0) / tl.n
    r = Rectangle(width=w - 0.04, height=tl.h).set_fill(color, 1).set_stroke(TEXT, 1)
    r.move_to([tl.x0 + w * (k + 0.5), tl.y, 0])
    return r


# --------------------------------------------------------------------------
# misc helpers
# --------------------------------------------------------------------------
def late(delay, anim):
    """Start ``anim`` after ``delay`` seconds inside a larger play, WITHOUT the t=0 flash that
    ``Succession(Wait(delay), anim)`` causes (Scene.play adds the mobjects of a Succession's
    non-introducer members, e.g. ``th.show``'s veil and big term, at full opacity at t=0)."""
    return AnimationGroup(Wait(delay), anim, lag_ratio=1)


def finish_now(anim):
    """Run an animation to its end state instantly (builds a 'starts with' state)."""
    anim.scene = None
    anim.begin()
    anim.finish()
    return anim


def set_docked(th, text):
    """Start a scene with ``text`` already docked top-right (continuity)."""
    return th.docked_now(text)


def counter_text(tracker, fmt="{:,.0f} instructions/s", font_size=24, color=TEXT, pos=ORIGIN):
    """Text counter driven by a ValueTracker (fast, no LaTeX)."""
    def make():
        return Text(fmt.format(tracker.get_value()), font=MONO_FONT, font_size=font_size, color=color).move_to(pos)
    return always_redraw(make)


def fde_ring(center, w=1.15, gap=0.35, font_size=18):
    """FETCH -> DECODE -> EXECUTE row with a return arrow (S04)."""
    names = ["FETCH", "DECODE", "EXECUTE"]
    boxes = VGroup()
    for n in names:
        r = RoundedRectangle(width=w, height=0.5, corner_radius=0.1).set_fill(CARD_FILL, 1).set_stroke(DIM, 2.5)
        t = Text(n, font_size=font_size, color=DIM, weight=BOLD).move_to(r)
        if t.width > w * 0.88:
            t.scale_to_fit_width(w * 0.88)
        boxes.add(VGroup(r, t))
    boxes.arrange(RIGHT, buff=gap).move_to(center)
    arrows = VGroup(*[Arrow(boxes[i].get_right(), boxes[i + 1].get_left(), buff=0.04, stroke_width=3,
                            max_tip_length_to_length_ratio=0.5, tip_length=0.12).set_color(DIM) for i in range(2)])
    back = CurvedArrow(boxes[2].get_bottom() + DOWN * 0.04, boxes[0].get_bottom() + DOWN * 0.04, angle=-PI / 3,
                       tip_length=0.14).set_color(DIM).set_stroke(width=3)
    g = VGroup(boxes, arrows, back)
    g.boxes = boxes
    return g


def light(ring, i, color=CPU_COLOR):
    """Animation: light ring stage i, dim the others."""
    anims = []
    for k, b in enumerate(ring.boxes):
        on = k == i
        anims.append(b[0].animate.set_stroke(color if on else DIM).set_fill(color if on else CARD_FILL,
                                                                            0.3 if on else 1))
        anims.append(b[1].animate.set_color(TEXT if on else DIM))
    return AnimationGroup(*anims)


def ring_lit(ring, i, color=CPU_COLOR):
    """Instant version of ``light``."""
    for k, b in enumerate(ring.boxes):
        on = k == i
        b[0].set_stroke(color if on else DIM).set_fill(color if on else CARD_FILL, 0.3 if on else 1)
        b[1].set_color(TEXT if on else DIM)
    return ring


def pc_arrow(mem, i):
    a = Arrow(LEFT, RIGHT, buff=0, stroke_width=6, tip_length=0.22).set_color(CPU_COLOR).scale(0.5)
    lab = Text("PC", font_size=18, color=CPU_COLOR, weight=BOLD)
    g = VGroup(a, lab.next_to(a, LEFT, buff=0.08))
    g.next_to(mem.cell(i), LEFT, buff=0.45)
    return g


# --------------------------------------------------------------------------
# S07/S08 peach world builders
# --------------------------------------------------------------------------
STU_PEACH = np.array([-2.6, -2.15, 0])     # dialogue mode, lowered to clear the table (deviation)
PROF_PEACH = np.array([2.6, -2.15, 0])
PEACH_HOST_SCALE = 0.9


def table_line():
    return Line([-4.4, TABLE_Y, 0], [4.4, TABLE_Y, 0]).set_stroke("#8A6A4A", 6)


def peach_on_table(peach, x=0.0):
    return peach.move_to([x, TABLE_Y + peach.body.height / 2 + 0.02, 0])


def vpeach_above(eater, scale=0.62):
    v = Peach().virtual_copy().scale(scale)
    v.move_to([eater.get_center()[0], 1.75, 0])
    return v


def view_cone(eater, target, color=TEXT):
    eye = eater.to_global(np.array([0.26, 0.34, 0]))
    r = target.width / 2 * 0.8
    c = target.get_center()
    cone = Polygon(eye, c + LEFT * r, c + RIGHT * r).set_fill(color, 0.12).set_stroke(width=0)
    return cone


def peach_world_s07_end():
    """Returns dict: table, peach (dimmed), phys_tag, eaters, vpeaches, vtags, cones."""
    table = table_line()
    peach = peach_on_table(Peach())
    phys = Text("physical", font_size=22, color=TEXT).next_to(table, DOWN, buff=0.12).set_x(0)
    eaters = make_eaters()
    for e in eaters:
        e.set_look(peach)
    vps = VGroup(*[vpeach_above(e) for e in eaters])
    vtags = VGroup(*[Text("virtual", font_size=18, color=VIRT).next_to(v, UP, buff=0.08) for v in vps])
    cones = VGroup(*[view_cone(e, v) for e, v in zip(eaters, vps)])
    peach.set_opacity(0.5)
    return dict(table=table, peach=peach, phys=phys, eaters=eaters, vps=vps, vtags=vtags, cones=cones)


def peach_hosts():
    stu, prof = make_hosts("dialog")
    stu.scale(PEACH_HOST_SCALE).move_to(STU_PEACH)
    prof.scale(PEACH_HOST_SCALE).move_to(PROF_PEACH)
    stu.mode_scale = prof.mode_scale = PEACH_HOST_SCALE
    return stu, prof


# --------------------------------------------------------------------------
# S09/S10 cpu demo builders
# --------------------------------------------------------------------------
S09_CODE_POS = np.array([-3.4, 0.6, 0])
S09_TERM_POS = np.array([3.2, 0.4, 0])


def s09_code():
    c = code_block(CPU_C, 20).move_to(S09_CODE_POS)
    t = code_title(c, "cpu.c")
    return c, t


def s09_terminal(fresh_prompt=True):
    term = Terminal(width=5.6, height=3.6, font_size=20, cpus=1).move_to(S09_TERM_POS)
    if fresh_prompt:
        term.prompt_line()   # builds the line instantly (animation discarded)
    return term


# --------------------------------------------------------------------------
# S11/S12 mem demo
# --------------------------------------------------------------------------
MEM_C = r'''int *p = malloc(sizeof(int));
printf("(%d) addr of p: %p\n", getpid(), p);
*p = 0;
while (1) {
    Spin(1);
    *p = *p + 1;
    printf("(%d) p: %d\n", getpid(), *p);
}'''
STRIP_VALUES = ["3", "7", "2", "0", "5", "1", "8", "4", "6", "2", "9", "0"]
S11_P_INDEX = 1          # 0x200000
S11_CODE_POS = np.array([-3.65, -0.55, 0])
S11_TERM_POS = np.array([3.4, -0.8, 0])
S11_PID_POS = np.array([0.1, -1.55, 0])   # base point of PID 2134


def s11_strip():
    return MemoryStrip(n=12, cell_width=0.9, cell_height=0.7, values=STRIP_VALUES).move_to([0, 2.0, 0])


def s11_code():
    c = code_block(MEM_C, 16).move_to(S11_CODE_POS)
    return c, code_title(c, "mem.c")


def s11_terminal():
    return Terminal(width=5.0, height=3.0, font_size=17).move_to(S11_TERM_POS)


def pid_process(pid, color, scale=0.55):
    p = Process(color=color, label=f"PID {pid}").scale(scale)
    return p


# --------------------------------------------------------------------------
# S15-S17 persistence
# --------------------------------------------------------------------------
S15_MEM_POS = np.array([-3.0, 0.2, 0])
S15_DISK_POS = np.array([3.0, 0.0, 0])
S15_SWITCH_POS = np.array([0.0, 1.0, 0])   # spec (0, 2.4); lowered to clear the term highlight
DRAM_VALUES = ["42", "7", "13", "99", "3", "58"]


def s15_memory(values=True):
    return Memory(cells=6, contents=DRAM_VALUES if values else None, width=1.4, height=3.3, font_size=22,
                  addresses=True, title="DRAM").move_to(S15_MEM_POS)


def s15_disk():
    d = Disk(width=1.8, height=1.5).move_to(S15_DISK_POS)
    files = VGroup(*[FileIcon(n, color=TEXT, width=0.5, font_size=14) for n in ("notes", "photo", "main.c")])
    files.arrange(RIGHT, buff=0.15).next_to(d.top, UP, buff=-0.05)
    return d, files


def s15_extras(disk):
    hdd = Text("HDD", font_size=20, color=DISK_COLOR).next_to(disk, DOWN, buff=0.15)
    ssd = ssd_icon(1.3).move_to(disk.get_center() + RIGHT * 2.2 + DOWN * 0.2)
    ssd_lab = Text("SSD", font_size=20, color=DISK_COLOR).next_to(ssd, DOWN, buff=0.15)
    fs = RoundedRectangle(width=4.4, height=0.55, corner_radius=0.1).set_fill(PERS, 0.18).set_stroke(PERS, 3)
    fs.move_to([disk.get_center()[0] + 1.1, 2.35, 0])
    fs_lab = Text("file system", font_size=24, color=TEXT).move_to(fs)
    return hdd, VGroup(ssd, ssd_lab), VGroup(fs, fs_lab)


# --------------------------------------------------------------------------
# S19-S22 history
# --------------------------------------------------------------------------
ERAS = ["mainframes", "Atlas", "minicomputers / UNIX", "PCs", "today"]
HIST_TERM_AT = np.array([0, 1.75, 0])     # the ribbon owns y = 2.6, so terms are written lower


def era_ribbon(start=0):
    return EraRibbon(ERAS, y=2.6, x_range=(-6, 6), font_size=20, accent=INTRO, start=start)


def hist_terms(at=HIST_TERM_AT, size=42):
    th = terms(INTRO)
    th.at = np.array(at, dtype=float)
    th.size = size
    return th


MAINFRAME_POS = np.array([-2.0, -0.4, 0])
OPERATOR_POS = np.array([2.0, -0.4, 0])


def s19_end():
    mf = mainframe_icon(2.4, 3.0).move_to(MAINFRAME_POS)
    shelf = bookshelf_icon(1.1).move_to([-4.6, -0.5, 0])
    shelf_lab = Text("OS = library", font_size=20, color=TEXT).next_to(shelf, UP, buff=0.12)
    cpu = CPU(size=0.6, label=None, pins=2).move_to(mf.get_center() + DOWN * 0.85)
    job = Process("running", color=A_COLOR).scale(0.35)
    cpu.seat(job)
    op = operator_icon(1.6).move_to(OPERATOR_POS)
    cards = punch_cards_icon(4, 0.5).next_to(op, LEFT, buff=0.0).shift(DOWN * 0.15)
    return mf, VGroup(shelf, shelf_lab), VGroup(cpu, job), VGroup(op, cards)
