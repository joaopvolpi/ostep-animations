import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from manim import *  # noqa: E402,F403
from ostep_lib import *  # noqa: E402,F403
from common import *  # noqa: E402,F403
from s13_two_threads import s13_end  # noqa: E402

INTERLEAVE = [(0, "load"), (1, "load"), (0, "add"), (1, "add"), (0, "store"), (1, "store")]


class S14LoadAddStore(NarratedScene):
    def construct(self):
        stu, prof = make_hosts("corner", stu_expr="frustrated", prof_expr="worried")
        th = terms(CONC)
        th.at = np.array([-3.6, 2.75, 0])
        th.size = 44
        bdg = badge(CONC)
        code, title, cell, t1, t2, links, term = s13_end()
        self.add(stu, prof, bdg, code, title, cell, t1, t2, links, term, set_docked(th, "thread"))

        demo = InterleavingDemo(value=5, colors=(T1_COLOR, T2_COLOR))
        line = code.code_lines[3].copy()

        # S14.1 counter++ splits into three steps
        three = VGroup(*[Text(InterleavingDemo.OP_TEXT[op], font=MONO_FONT, font_size=24, color=TEXT)
                         for op in InterleavingDemo.OPS]).arrange(DOWN, buff=0.25).move_to([0, 0.3, 0])
        with self.narrate("Here's why. Adding one to the counter isn't one step. It's three:"):
            self.play(prof.change("explaining"), FadeOut(VGroup(code, title, cell, t1, t2, links, term)),
                      line.animate.move_to([0, 0.3, 0]).scale(1.4), run_time=1.0)
            self.wait(0.4)
            self.play(ReplacementTransform(VGroup(*[line.copy() for _ in range(3)]), three), FadeOut(line),
                      run_time=0.9)

        # S14.2 T1 alone, slow motion
        others = VGroup(demo.cell, demo.cell_title, demo.cell_value, demo.threads, demo.regs)
        with self.narrate("load the value from memory into a register, add one, store it back."):
            self.play(ReplacementTransform(three, VGroup(*[b[1] for b in demo.lanes[0]])),
                      FadeIn(VGroup(*[b[0] for b in demo.lanes[0]])),
                      FadeIn(demo.lanes[1]), FadeIn(others), run_time=1.0)
            for op in ("load", "add", "store"):
                self.play(demo.play_step(0, op, run_time=1.4, show_step=False))
                self.wait(0.3)
            self.wait(0.4)
            self.play(demo.reset(5))

        # S14.3 atomically
        with self.narrate("Those three don't happen atomically, all at once."):
            self.play(th.show("atomically", hold=0.8))
            self.play(*[Indicate(b[0], color=CONC, scale_factor=1.06) for lane in demo.lanes for b in lane],
                      run_time=0.8)

        # S14.4 interleave
        demo.step_label.set_opacity(1)
        with self.narrate("So if the two threads interleave in the middle,"):
            self.play(FadeIn(demo.step_label), run_time=0.3)
            for anim in demo.steps(INTERLEAVE[:5], run_time=1.0):
                self.play(anim)
                self.wait(0.35)

        # S14.5 overwrite
        ghost = Text("7", font=MONO_FONT, font_size=40, color=GOOD, weight=BOLD).next_to(demo.cell, RIGHT, buff=0.35)
        crack = x_mark(0.3, BAD, 6).move_to(ghost)
        cap = Text("2 increments, +1 result", font_size=26, color=BAD).next_to(demo.cell, LEFT, buff=0.5)
        with self.narrate("one update can overwrite the other."):
            for anim in demo.steps(INTERLEAVE[5:], run_time=1.0):
                self.play(anim)
                self.wait(0.4)
            self.play(FadeIn(ghost, scale=1.3), run_time=0.4)
            self.play(Create(crack), ghost.animate.set_opacity(0.3), FadeIn(cap), run_time=0.6)
            self.wait(1.8)

        # S14.6 crux
        crux = CruxCard("How to build correct concurrent programs?",
                        "Many threads, one memory: what primitives from the OS? from the hardware?",
                        accent=CONC).move_to([0, 0.2, 0])
        self.add_subcaption("THE CRUX: How to build correct concurrent programs? When many threads execute "
                            "concurrently in the same memory space, how can we build a correctly working program? "
                            "What primitives does the OS need to provide, and what does the hardware need to provide?",
                            duration=6.5)
        self.play(crux.write())
        self.beat(3.0)

        # S14.7 tag, dock, fade
        tag = next_tag("→ Ep. 26–28", 20).next_to(crux, DOWN, buff=0.2)
        self.play(FadeIn(tag), run_time=0.4)
        self.wait(0.6)
        self.play(crux.dock((0, 3.2, 0)), FadeOut(tag), run_time=0.9)
        self.wait(0.8)
        demo_all = VGroup(demo, demo.step_label, *demo.reg_texts, demo.cell_value, ghost, crack, cap)
        self.play(FadeOut(demo_all), FadeOut(crux), th.clear(), run_time=0.8)
        self.beat(0.4)
