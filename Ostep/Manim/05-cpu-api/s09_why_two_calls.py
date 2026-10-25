import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


class S09WhyTwoCalls(Ep05Scene):
    def construct(self):
        self.add_badge()
        self.add_docked_term("exec()")
        strip = crux_strip()
        self.add(strip)
        stu, prof = self.add_corner_chars("surprised", "explaining")

        # S09.1
        run = program_chip('run("wc")', DIM, 24).move_to(P3(0, 0.5))
        q = question_mark(0.5).next_to(run, UP, buff=0.1)
        with self.narrate("Hold on. All of this seems like a strange way to launch a program. First clone yourself, "
                          'then replace yourself? Why not one simple call, "run this program"?'):
            self.play(FadeOut(strip), stu.change("frustrated"), run_time=0.6)
            self.play(FadeIn(run, scale=0.6), FadeIn(q), run_time=0.6)
            self.wait(3.0)

        # S09.2
        term = mk_term(5.0, 6, 18).move_to(P3(-3.4, 1.0))
        fill_term(term, [])
        loop = ShellLoop(cx=3.4)
        sh = proc(SHC, "ready", scale=0.55, label="sh")
        bottom_to(sh, loop.stand_point("prompt"))
        sh.shift(RIGHT * 3.0 + UP * 0.0)
        with self.narrate("That's the question the whole design hangs on. Let's look at who launches programs "
                          "for a living: the shell."):
            self.play(prof.change("proud"), FadeOut(q), run.animate.scale(0.6).move_to(P3(-5.6, 2.75)).set_opacity(0.4),
                      run_time=0.8)
            self.play(FadeIn(term), run_time=0.5)
            self.play(FadeIn(sh, shift=LEFT * 0.5), run_time=0.6)
            self.play(sh.animate.move_to(sh.get_center() + LEFT * 3.0), self.terms.note("shell"))

        # S09.3
        ut = tagged("user program", USER_COLOR, 18, USER_COLOR).move_to(P3(1.6, 1.75))
        with self.narrate("The shell is just an ordinary user program."):
            self.play(FadeIn(ut, shift=UP * 0.1), run_time=0.6)
            self.wait(1.0)

        # S09.4
        with self.narrate("It shows you a prompt, and waits."):
            self.play(Create(loop.nodes["prompt"][0]), Write(loop.nodes["prompt"][1]), run_time=0.7)
            self.play(loop.light("prompt"), Indicate(sh, scale_factor=1.05), term.prompt_line(), run_time=0.7)
            self.wait(0.5)

        # S09.5
        with self.narrate("You type a command: a program name and its arguments."):
            self.play(term.pop(run_time=0.1))
            self.play(term.type("wc p3.c"))
            self.wait(0.8)

        # S09.6
        c_sh = None
        with self.narrate("The shell finds the executable, calls fork() to create a child…"):
            self.play(Create(loop.arrows["p_f"]), Create(loop.nodes["fork"][0]), Write(loop.nodes["fork"][1]),
                      run_time=0.7)
            self.play(loop.light("fork"), loop.unlight("prompt"), run_time=0.4)
            c_sh, anim = clone_process(sh, color=CHI, label="sh", spread=0.0, move_time=0.1)
            self.add(c_sh)
            self.play(anim)
            self.play(Create(loop.arrows["f_e"]), Create(loop.arrows["f_w"]),
                      Create(loop.nodes["exec"][0]), Write(loop.nodes["exec"][1]),
                      Create(loop.nodes["wait"][0]), Write(loop.nodes["wait"][1]), run_time=1.0)

        # S09.7
        wc_new = proc(CHI, "ready", scale=0.55, label="wc")
        chipwc = program_chip("wc", SKY, 16)
        with self.narrate("…calls some variant of exec() in the child to run the command…"):
            self.play(hop_bottom(c_sh, loop.stand_point("exec")), loop.light("exec"), loop.unlight("fork"))
            wc_new.move_to(c_sh)
            self.play(FadeOut(c_sh), FadeIn(wc_new), run_time=0.8)
            chipwc.next_to(wc_new, DOWN, buff=0.1)
            self.play(FadeIn(chipwc), run_time=0.4)
            self.wait(0.5)

        # S09.8
        ring = progress_ring(0.25, CPU_COLOR, 0.0).next_to(wc_new, UP, buff=0.1)
        prog = ValueTracker(0.0)
        ring.add_updater(lambda m: m[1].become(
            Arc(radius=0.25, start_angle=PI / 2, angle=-TAU * max(prog.get_value(), 1e-3),
                arc_center=m[0].get_center()).set_stroke(CPU_COLOR, 5)))
        with self.narrate("…and calls wait() in the parent until the command finishes."):
            self.play(Create(loop.arrows["e_p"]), Create(loop.arrows["w_p"]), run_time=0.6)
            self.play(hop_bottom(sh, loop.stand_point("wait")), loop.light("wait"), loop.unlight("exec"), run_time=0.7)
            self.play(sh.change("blocked"), FadeIn(ring), run_time=0.5)
            self.play(prog.animate.set_value(1.0), run_time=1.5, rate_func=linear)
            ring.clear_updaters()
            self.play(term.print("29  107  1030 p3.c"), FadeOut(ring), run_time=0.4)

        # S09.9
        with self.narrate("Then it prints the prompt again."):
            self.play(wc_new.change("done"), run_time=0.5)
            self.play(FadeOut(wc_new), FadeOut(chipwc), loop.unlight("wait"), run_time=0.5)
            self.play(sh.change("ready"), hop_bottom(sh, loop.stand_point("prompt")), loop.light("prompt"), run_time=0.8)
            self.play(term.prompt_line(), Indicate(loop.arrows["e_p"], color=CPU_COLOR, scale_factor=1.0), run_time=0.8)

        # S09.10
        gap_anim, gap_lab = loop.highlight_gap()
        gap_mid = loop.arrows["f_e"].point_from_proportion(0.5)
        gap_sh = proc(CHI, "ready", scale=0.4, label="sh").move_to(gap_mid + RIGHT * 0.2)
        with self.narrate("And here's the key. Between fork() and exec(), there's a gap, where the code is running "
                          "in the child, but it's still the shell's code."):
            self.play(loop.unlight("prompt"), gap_anim, run_time=0.8)
            self.play(FadeIn(gap_sh, scale=0.5), run_time=0.6)
            self.wait(2.0)

        # S09.11
        shop, shop_anim = loop.workshop()
        with self.narrate("That gap is a chance to rearrange the child's world before the new program starts."):
            self.play(shop_anim, prof.change("proud"))
            self.wait(1.0)
