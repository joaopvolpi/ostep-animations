import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403

CHIP_X = 2.6


class S16BackToTheMenu(Ep05Scene):
    def construct(self):
        self.add_badge()
        stu, prof = self.add_corner_chars("neutral", "happy")
        menu = MenuCardRows("Process API", ["Create", "Destroy", "Wait", "Misc. control", "Status"],
                            width=4.6, height=4.4, font_size=28).move_to(P3(-3.2, 0.3))
        hl = [None]

        def pick(*idx):
            new = [menu.highlight_row(i) for i in idx]
            if hl[0] is None:
                hl[0] = VGroup(*new)
                return FadeIn(hl[0], run_time=0.3)
            tgt = VGroup(*new)
            return Transform(hl[0], tgt, run_time=0.3)

        def link(i, chip):
            return Line(menu.card.get_right() + UP * (menu.row_y(i) - menu.card.get_y()),
                        chip.get_left() + LEFT * 0.05).set_stroke(DIM, 2)

        # S16.1
        self.say("Let's go back to the menu from last time.", FadeIn(menu, shift=RIGHT * 0.4), min_time=2.0)

        # S16.2
        c_fork = program_chip("fork()", PAR, 24)
        c_exec = program_chip("exec()", SKY, 24)
        row = VGroup(c_fork, c_exec).arrange(RIGHT, buff=0.3)
        row.move_to(P3(CHIP_X, menu.row_y(0)))
        l0 = link(0, row)
        with self.narrate("Create: that's fork(), and usually exec() right after."):
            self.play(pick(0), run_time=0.4)
            self.play(Create(l0), FadeIn(row, shift=LEFT * 0.3), run_time=0.8)
            self.wait(1.5)

        # S16.3
        c_wait = program_chip("wait()", CHI, 24)
        clk = ClockIcon(0.2)
        wrow = VGroup(c_wait, clk).arrange(RIGHT, buff=0.25).move_to(P3(CHIP_X, menu.row_y(2)))
        l2 = link(2, wrow)
        with self.narrate("Wait: that's wait()."):
            self.play(pick(2), run_time=0.4)
            self.play(Create(l2), FadeIn(wrow, shift=LEFT * 0.3), run_time=0.8)

        # S16.4
        br = menu.bracket(1, 3, VIRT)
        c_kill = program_chip("kill()", KERNEL_COLOR, 24)
        krow = VGroup(c_kill, bolt_glyph(0.5, CPU_COLOR)).arrange(RIGHT, buff=0.25)
        krow.move_to(P3(CHIP_X, (menu.row_y(1) + menu.row_y(3)) / 2))
        lk = Line(br.get_center() + RIGHT * 0.0, krow.get_left() + LEFT * 0.05).set_stroke(DIM, 2)
        with self.narrate("Destroy and miscellaneous control: signals, via kill()."):
            self.play(pick(1, 3), Create(br), run_time=0.5)
            self.play(Create(lk), FadeIn(krow, shift=LEFT * 0.3), run_time=0.8)

        # S16.5
        srow = VGroup(program_chip("ps", DIM, 24), program_chip("top", DIM, 24), info_tag("status", DIM, 18)).arrange(RIGHT, buff=0.25)
        srow.move_to(P3(CHIP_X + 0.3, menu.row_y(4)))
        ls = link(4, srow)
        with self.narrate("Status: ps and top."):
            self.play(pick(4), run_time=0.4)
            self.play(Create(ls), FadeIn(srow, shift=LEFT * 0.3), run_time=0.8)
            self.wait(0.5)

        # S16.6
        chain = VGroup(program_chip("fork()", PAR, 22), program_chip("exec()", SKY, 22),
                       program_chip("wait()", CHI, 22)).arrange(RIGHT, buff=0.35)
        term_ic = VGroup(RoundedRectangle(width=0.8, height=0.55, corner_radius=0.08).set_fill("#111111", 1).set_stroke(DIM, 2),
                         Text(">_", font=MONO_FONT, font_size=20, color=TEXT)).move_to(ORIGIN)
        gt = mono(">", 44, VIRT)
        pp = mono("|", 44, VIRT)
        outs = VGroup(term_ic, gt, pp).arrange(RIGHT, buff=0.5)
        grp = VGroup(chain, outs).arrange(DOWN, buff=0.5).move_to(P3(CHIP_X, 0.3))
        links = VGroup(*[Line(chain[i].get_right(), chain[i + 1].get_left()).set_stroke(CPU_COLOR, 3) for i in range(2)])
        with self.narrate("A handful of simple calls, combined, are enough to build a shell, redirection, pipes, and more."):
            self.play(FadeOut(VGroup(row, wrow, krow, srow, l0, l2, lk, ls, br)), FadeOut(hl[0]), FadeOut(menu), run_time=0.7)
            self.play(FadeIn(chain), run_time=0.5)
            self.play(Create(links), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(o, shift=DOWN * 0.3, scale=0.5) for o in outs], lag_ratio=0.3), run_time=1.2)
            self.wait(1.0)

        # S16.7
        bk = book_icon("Stevens", "& Rago", width=1.1, height=1.4, font_size=16).move_to(P3(-3.5, 0.3))
        with self.narrate("And we've only skimmed the surface. The book recommends reading Stevens and Rago to go deeper."):
            self.play(FadeIn(bk, scale=0.6), run_time=0.6)
            self.wait(2.5)
            self.play(FadeOut(bk), run_time=0.5)

        # S16.8
        tg1 = ep_tag("→ Ep. 39").next_to(gt, UP, buff=0.15)
        tg2 = ep_tag("→ Ep. 39").next_to(pp, UP, buff=0.15)
        with self.narrate("We'll return to file descriptors when we get to file systems."):
            self.play(FadeIn(tg1, scale=0.6), FadeIn(tg2, scale=0.6), run_time=0.6)
            self.wait(1.5)
            self.play(FadeOut(VGroup(chain, links, outs, tg1, tg2)), run_time=0.8)
