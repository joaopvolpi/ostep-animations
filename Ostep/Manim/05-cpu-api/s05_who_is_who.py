import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


class S05WhoIsWho(Ep05Scene):
    def construct(self):
        w = build_s04_end()
        pw, cw = w["pw"], w["cw"]
        self.add_badge()
        self.add(crux_strip())
        self.add_docked_term("child")
        stu, prof = self.add_corner_chars("surprised", "happy")
        self.add(*pw.parts(), *cw.parts(), w["pm"], w["cm"], w["mt"], w["b1"], w["b2"])
        lab_p = Text("parent", font_size=26, color=PAR, weight="BOLD").next_to(pw.creature, LEFT, buff=0.35)
        lab_c = Text("child", font_size=26, color=CHI, weight="BOLD").next_to(cw.creature, RIGHT, buff=0.35)
        self.add(lab_p, lab_c)

        # S05.1
        walker = p1_walker(caption=False).move_to(S5_CODE_AT)
        b_par = walker.add_bar(PAR, 2)
        b_chi = walker.add_bar(CHI, 2)
        icon_p, an_p = pw.collapse(S5_CREATURE_L)
        icon_c, an_c = cw.collapse(S5_CREATURE_R)
        term = mk_term(6.0, 3, 16)
        fill_term(term, ["hello (pid:29146)"]).move_to(S5_TERM_AT)
        qs = VGroup(question_mark(0.4).move_to(S5_CREATURE_L + UP * 1.2), question_mark(0.4).move_to(S5_CREATURE_R + UP * 1.2))
        with self.narrate("But if they're identical, how does each one know whether it's the parent or the child? "
                          "They run the same code."):
            self.play(stu.change("confused"), FadeOut(w["pm"]), FadeOut(w["cm"]), FadeOut(lab_p), FadeOut(lab_c), FadeOut(w["b1"]), FadeOut(w["b2"]),
                      an_p, an_c, FadeOut(w["mt"]), run_time=1.2)
            self.play(FadeIn(walker), FadeIn(term), FadeIn(b_par), FadeIn(b_chi), FadeIn(qs), run_time=0.8)
            self.wait(2.0)

        # S05.2
        cell_p = tagged("x = 100", PAR, 20, PAR).next_to(icon_p, RIGHT, buff=0.15)
        cell_c = tagged("x = 100", CHI, 20, CHI).next_to(icon_c, LEFT, buff=0.15)
        lock = padlock_icon(0.5).move_to(P3(0, -1.0))
        wall = VGroup(DashedLine(P3(-4.5, -1.0), P3(-0.4, -1.0)), DashedLine(P3(0.4, -1.0), P3(4.5, -1.0))).set_stroke(DIM, 2)
        with self.narrate("They're not quite identical. The child has the same memory, but a private copy."):
            self.play(FadeOut(qs), FadeIn(cell_p), FadeIn(cell_c), run_time=0.6)
            self.play(Create(wall), FadeIn(lock, scale=0.5), run_time=0.8)

        # S05.3
        new_p = tagged("x = 101", PAR, 20, PAR).move_to(cell_p)
        with self.narrate("What either one changes afterwards, the other never sees."):
            self.play(Transform(cell_p, new_p), Flash(cell_p.get_center(), color=PAR, flash_radius=0.4), run_time=0.8)
            self.wait(1.5)

        # S05.4
        with self.narrate("And there's one more difference: the value that fork() returns."):
            self.play(FadeOut(cell_p), FadeOut(cell_c), FadeOut(wall), FadeOut(lock), FadeOut(icon_p), FadeOut(icon_c),
                      FadeIn(proc(PAR, "ready", scale=0.7, label=f"PID {PID_P}").move_to(S5_CREATURE_L)),
                      FadeIn(proc(CHI, "ready", scale=0.7, label=f"PID {PID_C}").move_to(S5_CREATURE_R)), run_time=0.5)
            self.play(walker.circumscribe(2), pw.creature.look_at(walker.line_mob(2)),
                      cw.creature.look_at(walker.line_mob(2)), run_time=1.2)
            self.wait(0.5)

        # S05.5
        t_par = tagged("rc = 29147", PAR, 20, PAR)
        t_chi = tagged("rc = 0", CHI, 20, CHI)
        t_par.move_to(walker.line_point(2, "left") + RIGHT * 1.2)
        t_chi.move_to(walker.line_point(2, "left") + RIGHT * 1.2)
        d_par = P3(-5.0, 1.95)
        d_chi = P3(5.0, 1.95)
        with self.narrate("The parent gets back the PID of the new child, 29147."):
            self.play(FadeIn(t_par, scale=0.6), run_time=0.4)
            self.play(t_par.animate.move_to(d_par), run_time=1.0)
            self.wait(1.2)

        # S05.6
        with self.narrate("The child gets back zero."):
            self.play(FadeIn(t_chi, scale=0.6), run_time=0.4)
            self.play(t_chi.animate.move_to(d_chi), run_time=1.0)

        # S05.7
        chk_p = VGroup(mono("29147 == 0", 20, PAR), x_mark(0.25)).arrange(RIGHT, buff=0.12).move_to(P3(-5.0, 2.55))
        chk_c = VGroup(mono("0 == 0", 20, CHI), tick_mark(0.25)).arrange(RIGHT, buff=0.12).move_to(P3(5.0, 2.55))
        with self.narrate("That single number is the whole trick. The if checks it."):
            self.play(walker.move_bar(0, 3), walker.move_bar(1, 3), run_time=0.7)
            self.play(FadeIn(chk_p, shift=DOWN * 0.15), FadeIn(chk_c, shift=DOWN * 0.15), run_time=0.7)
            self.wait(1.0)

        # S05.8
        with self.narrate("Zero? You're the child, take this branch. Anything else? You're the parent, take that one."):
            self.play(walker.move_bar(1, 4), run_time=0.7)
            self.play(walker.move_bar(0, 6), run_time=0.7)
            self.play(term.print(P1_OUT[1]))
            self.play(term.print(P1_OUT[2]))
            self.wait(0.8)

        # S05.9
        self.play(FadeOut(chk_p), FadeOut(chk_c), run_time=0.4)
        with self.narrate("So the code is the same, but the world is different. Each process walks down its own branch."):
            self.play(stu.change("excited"), run_time=0.6)
            self.play(walker.move_bar(0, 7), walker.move_bar(1, 5), run_time=1.0)
            self.wait(1.0)

        # S05.10
        self.say("Both processes, one program, two paths.", prof.change("proud"))
        self.beat(1.0)
