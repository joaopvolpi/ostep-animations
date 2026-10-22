import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from manim import *  # noqa: E402,F403
from ostep_lib import *  # noqa: E402,F403
from common import *  # noqa: E402,F403
from s21_multiprogramming_unix import s21_left, s21_right  # noqa: E402

PC_POS = np.array([0, 0.25, 0])
STRIP_Y = -1.75


def mem_regions():
    cells = VGroup()
    for k in range(8):
        r = Rectangle(width=0.5, height=0.45).set_fill(ABCD_COLORS[k // 2], 0.6).set_stroke(MEM_COLOR, 2)
        cells.add(r)
    cells.arrange(RIGHT, buff=0).move_to([0, STRIP_Y, 0])
    return cells


class S22PcToday(NarratedScene):
    def construct(self):
        stu, prof = make_hosts("corner", stu_expr="curious", prof_expr="happy")
        th = hist_terms()
        bdg = badge(INTRO)
        era = era_ribbon(2)
        mini, cpu, procs, disk, mems, walls = s21_left()
        unix, sub, pipeline = s21_right()
        self.add(stu, prof, bdg, era, mini, cpu, procs, disk, mems, walls, unix, sub, pipeline,
                 set_docked(th, "pipes"))

        pc = Computer("happy").scale(0.9).move_to(PC_POS)
        # S22.1
        self.say("Then the personal computer.",
                 FadeOut(VGroup(mini, cpu, procs, disk, mems, walls, unix, sub, pipeline)), era.move_marker("PCs"),
                 Succession(Wait(0.5), FadeIn(pc, shift=UP * 0.3)),
                 Succession(Wait(0.8), th.show("personal computer", size=36, hold=0.6)))

        # S22.2 skid backwards
        with self.narrate("At first it was a great leap backwards."):
            self.play(era.marker.animate.shift(LEFT * 2.2).rotate(0.4), run_time=0.6, rate_func=rush_from)
            self.play(Wiggle(era.marker), run_time=0.4)
            self.play(era.marker.animate.shift(RIGHT * 2.2).rotate(-0.4), run_time=0.6)

        # S22.3 DOS: no memory protection
        cells = mem_regions()
        bad = Process(color=BAD).scale(0.35)
        place_on(bad, cells[0].get_top())
        with self.narrate("Early systems like DOS had no memory protection,"):
            self.play(FadeIn(cells), FadeIn(bad), run_time=0.5)
            for k in range(1, 8):
                self.play(hop_to(bad, cells[k].get_top(), height=0.2, run_time=0.18),
                          cells[k].animate(run_time=0.18).set_fill(BAD, 0.8))
            self.play(pc.change("error"), run_time=0.4)

        # S22.4 Mac: one stuck program freezes the machine
        mcpu = CPU(size=0.7).move_to([2.9, 0.1, 0])
        stuck = Process("running", color=D_COLOR).scale(0.4)
        mcpu.seat(stuck)
        loop = loop_arrow(0.28).next_to(stuck, RIGHT, buff=0.05)
        freeze = Rectangle(width=16, height=10).set_fill(BG, 0.6).set_stroke(width=0)
        black = Rectangle(width=16, height=10).set_fill("#000000", 1).set_stroke(width=0)
        with self.narrate("and early Mac OS let one stuck program freeze the entire machine."):
            self.play(FadeOut(bad), FadeIn(VGroup(mcpu, stuck, loop)), pc.change("overwhelmed"), run_time=0.6)
            self.add(freeze)
            self.bring_to_front(mcpu, stuck, loop)
            self.play(FadeIn(freeze), Rotate(loop, -TAU, about_point=loop.get_center()), run_time=1.0)
            self.play(Rotate(loop, -TAU, about_point=loop.get_center()), run_time=0.8)
            self.add(black)
            self.wait(0.3)
            self.remove(black, freeze, mcpu, stuck, loop)
            pc.set_expression("idle")
            for c, k in zip(cells, range(8)):
                c.set_fill(ABCD_COLORS[k // 2], 0.6)
            self.wait(0.3)

        # S22.5 today: laptop + desktop, walls return
        lap = Laptop(width=1.7).move_to([-1.7, 0.45, 0])
        desk = desktop_icon(1.3).move_to([1.3, 0.45, 0])
        lap_tag = Text("UNIX-like ideas", font_size=18, color=TEXT).next_to(lap, DOWN, buff=0.12)
        desk_tag = Text("NT", font_size=18, color=TEXT).next_to(desk, DOWN, buff=0.12)
        mwalls = VGroup(*[Rectangle(width=0.06, height=0.6).set_fill(TEXT, 1).set_stroke(width=0)
                          .move_to(cells[2 * k + 1].get_right()) for k in range(3)])
        with self.narrate("Eventually the old lessons returned. macOS has UNIX at its core. Windows NT adopted "
                          "the great ideas."):
            self.play(era.move_marker("today"), pc.animate.scale(0.65).move_to([-4.6, 0.35, 0]), run_time=0.8)
            self.play(FadeIn(lap, shift=UP * 0.2), FadeIn(lap_tag), run_time=0.6)
            self.wait(0.6)
            self.play(FadeIn(desk, shift=UP * 0.2), FadeIn(desk_tag), run_time=0.6)
            self.play(FadeIn(mwalls, lag_ratio=0.3), run_time=0.6)

        # S22.6 Linux
        rack = server_rack_icon(0.8, 1.4).move_to([3.6, 0.45, 0])
        phone = phone_icon(1.0).move_to([4.8, 0.3, 0])
        linux = Text("Linux", font_size=20, color=TEXT).next_to(VGroup(rack, phone), DOWN, buff=0.15)
        self.say("Linux, started by Linus Torvalds, runs most of the internet and Android.",
                 FadeIn(rack, shift=UP * 0.2), Succession(Wait(0.4), FadeIn(phone, shift=UP * 0.2)),
                 Succession(Wait(0.8), FadeIn(linux)))

        # S22.7 phone ~ minicomputer, != early PC
        mini2 = minicomputer_icon(1.1, 1.4).move_to([-0.9, 0.35, 0])
        approx = MathTex(r"\approx", font_size=72, color=GOOD).move_to([0.45, 0.35, 0])
        neq = MathTex(r"\neq", font_size=72, color=BAD).move_to([-2.85, 0.35, 0])
        with self.narrate("Your phone runs an OS far closer to a 1970s minicomputer's than to an early PC's."):
            self.play(FadeOut(VGroup(lap, lap_tag, desk, desk_tag, rack, linux, cells, mwalls)), run_time=0.6)
            self.play(phone.animate.move_to([1.7, 0.35, 0]), FadeIn(mini2, shift=RIGHT * 0.3), run_time=0.8)
            self.play(Write(approx), run_time=0.5)
            self.play(Write(neq), run_time=0.5)
        self.beat(1.0)
