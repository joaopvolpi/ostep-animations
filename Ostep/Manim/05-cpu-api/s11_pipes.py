import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


class S11Pipes(Ep05Scene):
    def construct(self):
        self.add_badge()
        self.add_docked_term("redirection")
        stu, prof = self.add_corner_chars("excited", "happy")
        d = build_s11_end(dim=None)
        pipe, grep, wcp, p1, p0, c1, c0, term = (d[k] for k in ("pipe", "grep", "wc", "p1", "p0", "c1", "c0", "term"))
        term2 = mk_term(7.0, 2, 18).move_to(P3(0, -1.9))

        # S11.1
        glyph = pipe_glyph(1.6).move_to(S11_PIPE)
        glyph[0].stretch_to_fit_height(0.55)     # taller pill so the | glyph stays inside its border
        with self.narrate("Redirection connects a program to a file. A close relative connects it to another program: the pipe."):
            self.play(self.terms.note("pipe"), Create(glyph))

        # S11.2
        with self.narrate("The pipe() call makes a queue inside the kernel."):
            self.play(FadeOut(glyph), FadeIn(pipe.tube), FadeIn(pipe.dividers), FadeIn(term2), run_time=0.8)
            self.play(FadeIn(pipe.band_group()), run_time=0.8)
            self.wait(1.0)

        # S11.3
        g_start = grep.copy().shift(LEFT * 3)
        w_start = wcp.copy().shift(RIGHT * 3)
        with self.narrate("One process's output is connected to one end, another process's input to the other."):
            self.play(FadeIn(grep, shift=RIGHT * 1.5), FadeIn(wcp, shift=LEFT * 1.5), run_time=0.9)
            self.play(FadeIn(p1), FadeIn(p0), run_time=0.4)
            self.play(Create(c1), Create(c0), run_time=0.8)
            self.wait(1.2)
        self.remove(g_start, w_start)

        # S11.4
        counter = mono("0", 28, CPU_COLOR).next_to(wcp, UP, buff=0.15)
        ctab = VGroup(Text("count:", font_size=20, color=DIM), counter).arrange(RIGHT, buff=0.12).next_to(wcp, UP, buff=0.15)
        with self.narrate("So you can chain tools: look for a word in a file with grep, and pipe the result into "
                          "wc to count how many."):
            self.play(term2.type("grep -o foo file | wc -l"), FadeIn(ctab), run_time=1.6)
            for k in (1, 2, 3):
                self.play(pipe.send("foo", color=CPU_COLOR, run_time=1.0),
                          late(0.9, Transform(counter, mono(str(k), 28, CPU_COLOR).move_to(counter))))
            self.play(term2.print("3"))

        # S11.5
        lk1 = VGroup(padlock_icon(0.3), Text("code unchanged", font_size=18, color=TEXT)).arrange(RIGHT, buff=0.1)
        lk2 = lk1.copy()
        lk1.next_to(grep, DOWN, buff=0.15)
        lk2.next_to(wcp, DOWN, buff=0.15)
        with self.narrate("All without changing a single line in either program."):
            self.play(FadeIn(lk1, shift=UP * 0.1), FadeIn(lk2, shift=UP * 0.1), stu.look_at(pipe), run_time=0.8)
            self.wait(1.2)
        self.beat(1.0)

        # transition: dim to 25% for the Tip
        self.play(*[m.animate.set_opacity(0.25) for m in (pipe, grep, wcp, p1, p0, c1, c0, term2, ctab, lk1, lk2)],
                  run_time=0.8)
