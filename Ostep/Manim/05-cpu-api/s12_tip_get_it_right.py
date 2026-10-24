import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


class S12TipGetItRight(Ep05Scene):
    def construct(self):
        self.add_badge()
        self.add_docked_term("pipe")
        stu, prof = self.add_corner_chars("excited", "happy")
        d = build_s11_end(dim=0.25)
        ex12 = build_s11_extras(d)
        self.add(d["group"], ex12)

        card = TipCard("", title="TIP: GET IT RIGHT (LAMPSON'S LAW)", width=6.2, height=4.2)
        card.move_to(P3(3.3, 0.4))
        big = Text("Get it right.", font_size=46, color=TEXT, weight="BOLD").move_to(card.content_center() + UP * 1.0)
        sent = centered_text("Neither abstraction nor simplicity is a substitute for getting it right.", 5.2, 26, TEXT)
        sent.move_to(card.content_center() + UP * 0.0)
        abs_ic = VGroup(layers_icon(0.5), Text("abstraction", font_size=20, color=DIM)).arrange(RIGHT, buff=0.15)
        sim_ic = VGroup(Circle(radius=0.22).set_stroke(TEXT, 3), Text("simplicity", font_size=20, color=DIM)).arrange(RIGHT, buff=0.15)
        icons = VGroup(abs_ic, sim_ic).arrange(RIGHT, buff=0.7).move_to(card.content_center() + DOWN * 1.2)
        x1 = x_mark(0.25).next_to(abs_ic, UP, buff=0.05)
        x2 = x_mark(0.25).next_to(sim_ic, UP, buff=0.05)

        # S12.1
        with self.narrate("Pipes, redirection, a whole shell, from two small calls. One reason to see this design as a classic is a rule named after Butler Lampson: get it right."):
            self.play(card.slide_in(RIGHT), run_time=0.8)
            self.play(Write(big), run_time=1.0)
            self.wait(1.5)

        # S12.2
        with self.narrate("Neither abstraction nor simplicity is a substitute for getting it right."):
            self.play(Write(sent), run_time=1.5)
            self.play(FadeIn(icons), run_time=0.5)
            self.play(FadeIn(x1, scale=2), FadeIn(x2, scale=2), run_time=0.6)
            self.wait(0.8)

        # S12.3
        c_fork = program_chip("fork()", PAR, 24)
        c_exec = program_chip("exec()", SKY, 24)
        pair = VGroup(c_fork, c_exec).arrange(RIGHT, buff=0.9).move_to(P3(-2.0, 0.4))
        with self.narrate("There are many ways to design process creation. But the UNIX designers' combination "
                          "of fork() and exec() is simple, and immensely powerful."):
            self.play(FadeIn(pair, shift=UP * 0.2), run_time=0.8)
            self.wait(1.5)
            self.play(c_fork.animate.shift(RIGHT * 0.45), c_exec.animate.shift(LEFT * 0.45), run_time=0.6)
            self.play(Flash(pair.get_center(), color=CPU_COLOR, flash_radius=0.7), run_time=0.6)
            self.wait(1.0)

        # S12.4
        sp = program_chip("spawn()", DIM, 24).move_to(P3(-2.0, -1.0) + LEFT * 3)
        qm = question_mark(0.4)
        with self.narrate("Not everybody agrees. A recent paper argues for a simpler call, spawn(). "
                          "The authors of the book have opinions. You're allowed to have your own."):
            self.play(prof.change("neutral"), sp.animate.move_to(P3(-2.0, -1.0)), run_time=0.8)
            qm.next_to(sp, UP, buff=0.1)
            self.play(FadeIn(qm), run_time=0.3)
            self.wait(1.2)
            self.play(sp.animate.shift(LEFT * 4), FadeOut(qm), run_time=0.8)
            self.wait(0.8)

        # end: card slides out; scene fades; only the badge remains
        self.play(card.slide_out(RIGHT), FadeOut(big), FadeOut(sent), FadeOut(icons), FadeOut(x1), FadeOut(x2),
                  FadeOut(pair), FadeOut(sp), FadeOut(d["group"]), FadeOut(ex12), FadeOut(stu), FadeOut(prof), run_time=1.0)
