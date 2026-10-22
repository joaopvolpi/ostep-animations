import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from manim import *  # noqa: E402,F403
from ostep_lib import *  # noqa: E402,F403
from common import *  # noqa: E402,F403
from s08_snatch_the_peach import split_world  # noqa: E402


class S09CpuProgram(NarratedScene):
    def construct(self):
        stu, prof = make_hosts("corner", stu_expr="bored", prof_expr="happy")
        split, left, cpu, procs = split_world()
        th = terms(VIRT)
        bdg = badge(VIRT)
        self.add(stu, prof, bdg, split, left, cpu, procs, set_docked(th, "virtual"))

        code, title = s09_code()
        # S09.1
        self.say("Here's a tiny program called cpu.",
                 FadeOut(VGroup(split, left, cpu, procs)),
                 Succession(Wait(0.4), AnimationGroup(FadeIn(code.background), Write(code.code_lines),
                                                      FadeIn(title), run_time=1.4)), min_time=3.2)

        # S09.2 highlight bar loops
        bar = line_bar(code, 1)
        clock = ClockIcon(0.25).next_to(code.code_lines[2], RIGHT, buff=0.5)
        out_arrow = Arrow(code.code_lines[3].get_right() + RIGHT * 0.2, code.code_lines[3].get_right() + RIGHT * 1.7,
                          buff=0, stroke_width=4, tip_length=0.18).set_color(CPU_COLOR)
        with self.narrate("All it does is wait for one second, print the word you gave it, and repeat. Forever."):
            self.play(FadeIn(bar), run_time=0.3)
            for loop in range(2):
                self.play(bar.animate.move_to([bar.get_x(), code.code_lines[2].get_y(), 0]), run_time=0.3)
                if loop == 0:
                    self.play(FadeIn(clock, scale=0.5), run_time=0.2)
                self.play(clock.spin(1, run_time=0.8))
                self.play(bar.animate.move_to([bar.get_x(), code.code_lines[3].get_y(), 0]), run_time=0.3)
                self.play(GrowArrow(out_arrow), run_time=0.4)
                self.play(FadeOut(out_arrow), bar.animate.move_to([bar.get_x(), code.code_lines[1].get_y(), 0]),
                          run_time=0.4)
            self.play(FadeOut(bar), FadeOut(clock), run_time=0.3)

        # S09.3 terminal
        term = Terminal(width=5.6, height=3.6, font_size=20, cpus=1).move_to(S09_TERM_POS)
        with self.narrate("Run it with \"A\" on a computer with one processor,"):
            self.play(FadeIn(VGroup(term.frame, term.bar, term.glyph, *term.submobjects[2:3])), run_time=0.6)
            self.play(term.type('./cpu "A"'))
            self.play(Indicate(term.glyph, color=CPU_COLOR), run_time=0.6)
            self.beat(0.8)

        # S09.4
        with self.narrate("and every second you get… an A. Then another A. Not thrilling."):
            for k in range(4):
                self.wait(0.75)
                self.play(term.print("A"), run_time=0.25)
                if k == 1:
                    self.play(stu.change("bored"), run_time=0.3)
            self.wait(0.4)
            self.play(term.print("^C", color=DIM), run_time=0.25)
            self.play(term.prompt_line())
        self.play(term.clear(), run_time=0.4)
        self.play(term.prompt_line())
        self.beat(0.5)
