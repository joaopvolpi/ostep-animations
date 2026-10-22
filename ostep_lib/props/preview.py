"""Preview sheets for the props library.

Render from the project root:
    python -m manim -ql -s ostep_lib/props/preview.py PropSheet        # core props (still)
    python -m manim -ql -s ostep_lib/props/preview.py OverviewSheet    # 01-03 props (still)
    python -m manim -ql ostep_lib/props/preview.py PropDemo            # animations (hop, dock...)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from manim import *  # noqa: E402,F403
from ostep_lib import *  # noqa: E402,F403


def _cap(mob, text):
    t = Text(text, font_size=18, color=DIM).next_to(mob, DOWN, buff=0.15)
    return VGroup(mob, t)


class PropSheet(Scene):
    """Every core prop in one still."""

    def construct(self):
        apply_style(self)
        badge = SectionBadge("01–03 · Overview", accent=INTRO)
        terms = TermHighlight(accent=VIRT)
        docked = terms._make("process", 26, VIRT, (6.6, 3.6, 0), right_aligned=True)
        self.add(badge, docked)

        cpu = CPU().move_to([-5.6, 1.3, 0])
        p = Process("running", color=PROCESS_COLORS[0], label="A").scale(0.8)
        cpu.seat(p)
        mem = Memory(cells=6, contents=["add r1, r2", "load r3,[x]", "cmp r3, 0", "jmp f", "", "ret"],
                     width=1.5, height=3.0, title="Memory").move_to([-3.0, 1.1, 0])
        mem2 = Memory(regions=["code", "static data", "heap", ("free", 1.6), "stack"],
                      width=1.3, height=3.0).move_to([-0.9, 1.1, 0])
        mem2.region("code").set_fill(PROCESS_COLORS[0], 0.6)
        mem2.region("stack").set_fill(PROCESS_COLORS[0], 0.6)
        disk = Disk(label="Disk").move_to([1.2, 1.2, 0])
        f = FileIcon("main.c").next_to(disk, UP, buff=0.05)
        peach = Peach().move_to([3.0, 1.9, 0])
        vpeach = peach.virtual_copy().move_to([4.4, 1.9, 0])
        icons = VGroup(ClockIcon(), GearPair(radius=0.4), PauseGlyph(0.45), PlayGlyph(0.45))
        icons.arrange(RIGHT, buff=0.35).move_to([4.0, 0.5, 0])
        spot = Spotlight(height=1.6, spread=0.45).move_beam_to([6.0, 0.0, 0])
        lap = Laptop(width=2.0).move_to([4.9, -1.2, 0])
        vcpu = CPU(size=0.8).virtual_copy().move_to([2.9, -1.1, 0])

        crux = CruxCard("How to virtualize resources?",
                        "What mechanisms and policies? How, efficiently? What hardware support?",
                        accent=INTRO, width=6.2, question_size=28, subtitle_size=20).move_to([-3.2, -2.3, 0])
        tip = AsideCard("needs ASLR off", width=3.0, font_size=22).move_to([1.2, -2.0, 0])
        self.add(cpu, p, mem, mem2, disk, f, peach, vpeach, icons, spot, lap, vcpu, crux, tip)
        split = IllusionSplit("sees", "happens", title_size=18, top_y=-0.3, bottom_y=-3.4, at=3.2,
                              left_x=1.0, right_x=6.6)
        split.left_title.move_to([2.6, -2.9, 0]); split.right_title.move_to([3.9, -2.9, 0])
        self.add(split.divider.set_opacity(0.5))


class PropDemo(Scene):
    """Short demo of the animated helpers."""

    def construct(self):
        apply_style(self)
        terms = TermHighlight(accent=VIRT)
        cpu = CPU().move_to([0, 0.6, 0])
        disk = Disk().move_to([4, -1, 0])
        procs = [Process(color=PROCESS_COLORS[i], label="ABCD"[i]) for i in range(4)]
        for i, p in enumerate(procs):
            place_on(p, [-3 + 2 * i, -2.2, 0])
        self.add(cpu, disk, *procs)
        self.play(terms.show("hop_to"))
        for p in procs:
            self.play(hop_to(p, cpu.slot_point()))
            self.play(p.change("running"), run_time=0.3)
            self.play(hop_to(p, base_point(p) + DOWN * 2.2 * 0 + (np.array([-3 + 2 * procs.index(p), -2.2, 0]) - base_point(p))))
            self.play(p.change("ready"), run_time=0.2)
        self.play(disk.spin(2, run_time=1.5))
        crux = CruxCard("How to virtualize resources?", "What mechanisms and policies?", accent=INTRO)
        self.play(crux.write())
        self.wait(0.5)
        self.play(crux.dock())
        self.play(terms.show("docked twice"))
        self.wait(1)


class OverviewSheet(Scene):
    """The 01-03 props in one still."""

    def construct(self):
        apply_style(self)
        term = Terminal(width=4.2, height=2.2, cpus=1, font_size=18).move_to([-4.6, 2.6, 0])
        term.lines.add(term._make_line("prompt>", "./cpu \"A\"", TEXT).move_to(term._slot(0), aligned_edge=LEFT))
        term.lines.add(term._make_line(None, "A", TEXT).move_to(term._slot(1), aligned_edge=LEFT))
        strip = MemoryStrip(n=6, values=["", "7", "", "9", "", ""]).move_to([0.6, 3.1, 0])
        strip.cell(2).set_fill(PROCESS_COLORS[4], 0.55)
        ss = SystemStack(hw_y=-0.2, band_y=1.0, programs_y=2.0, hw_x=(-0.6, 0.6, 1.8), band_width=3.6,
                         cpu_size=0.6, mem_size=(0.5, 0.9), disk_width=0.7, label_size=20).move_to([5, 1.4, 0])
        uk = UserKernelBoundary(y=-0.6, x_range=(-7.1, -1.2), top=0.6, bottom=-1.6, label_x=-7.0, label_size=16)
        gauge = PrivilegeGauge(height=1.4).move_to([-0.6, -0.5, 0])
        era = EraRibbon(["mainframes", "Atlas", "UNIX", "PCs", "today"], y=-2.0, x_range=(-7, -0.5), font_size=14, start=1)
        demo = InterleavingDemo().scale(0.42).move_to([3.7, -1.9, 0])
        self.add(term, strip, ss, uk, gauge, era, demo)
        icons = VGroup(book_icon("Six Easy", "Pieces", width=0.6, height=0.8, font_size=14), editor_icon(0.9),
                       punch_cards_icon(width=0.5), mainframe_icon(0.9, 1.0), minicomputer_icon(0.6, 0.8),
                       operator_icon(0.8), server_rack_icon(0.5, 0.9), phone_icon(0.8), desktop_icon(0.8),
                       PowerSwitch(0.6), ssd_icon(0.8), journal_icon(0.6), cow_icon(0.6), sticky_note(size=0.6),
                       padlock_icon(0.4), leaf_icon(0.5), stopwatch_icon(0.35), ecg_icon(1.0),
                       pipe_glyph(0.7), net_boxes(spacing=0.6, size=0.3), letter_icon(), chair_icon(0.6),
                       bookshelf_icon(0.8), layers_icon(0.6), name_tag("Professor", 16), money_meter(width=1.2),
                       loop_arrow(0.25), tick_mark(0.3), x_mark(0.3), next_tag("→ Ep. 06", 16))
        icons.arrange_in_grid(rows=3, buff=0.18).scale_to_fit_width(13.4).move_to([0, -3.35 + 0.0, 0])
        icons.next_to([0, -4, 0], UP, buff=0.05)
        self.add(icons)
