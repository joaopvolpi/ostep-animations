import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


class S06WhoGoesFirst(Ep05Scene):
    def construct(self):
        w = build_s05_end()
        walker, term, cp, cc = w["walker"], w["term"], w["cp"], w["cc"]
        self.add_badge()
        self.add(crux_strip())
        self.add_docked_term("child")
        stu, prof = self.add_corner_chars("excited", "proud")
        self.add(walker, *walker.bars, term, cp, cc, w["t_par"], w["t_chi"])

        # S06.1
        run1 = mk_term(3.6, 4, 14)
        fill_term(run1, [("cmd", "./p1"), "hello (pid:29146)", "parent of 29147 (pid:29146)", "child (pid:29147)"])
        run1.move_to(P3(-2.3, -2.5))
        run2 = mk_term(3.6, 4, 14).move_to(P3(2.3, -2.5))
        l1 = Text("run 1", font_size=18, color=DIM).next_to(run1, UP, buff=0.08)
        l2 = Text("run 2", font_size=18, color=DIM).next_to(run2, UP, buff=0.08)
        with self.narrate('Now look at the output again. "Parent" printed before "child". '
                          "But run it another time, and you might get the opposite order."):
            self.play(FadeOut(walker.everything()), FadeOut(w["t_par"]), FadeOut(w["t_chi"]),
                      FadeOut(term), FadeIn(run1), FadeIn(l1), run_time=1.0)
            self.play(Indicate(run1.lines[2], color=PAR), run_time=0.7)
            self.play(Indicate(run1.lines[3], color=CHI), run_time=0.7)
            self.play(FadeIn(run2), FadeIn(l2), run_time=0.5)
            self.play(run2.type("./p1"))
            for t in ("hello (pid:29146)", "child (pid:29147)", "parent of 29147 (pid:29146)"):
                self.play(run2.print(t, run_time=0.3))
            self.wait(0.5)

        # S06.2
        neq = MathTex(r"\neq", color=CPU_COLOR).scale(1.4).move_to(P3(0, -2.5))
        self.say("The same program, the same input, and different output? Is it broken?",
                 stu.change("frustrated"), FadeIn(neq, scale=0.5))

        # S06.3
        with self.narrate("It's non-deterministic, and it isn't broken."):
            self.play(prof.change("explaining"), FadeOut(neq), run_time=0.6)
            self.play(self.terms.show("non-deterministic", hold=0.8))

        # S06.4
        cpu = CPU(1.1).move_to(P3(0, 1.0))
        q = Queue(label="Ready queue", center=(0, -0.8), slots=2, spacing=2.0)
        qm = P3(0, 1.0)
        mark = question_mark(0.45).next_to(cpu, RIGHT, buff=0.2)
        cc.set_expression("ready")
        with self.narrate("Say we have a single CPU. After fork(), there are two processes ready to run. "
                          "Which one goes first?"):
            self.play(GrowFromCenter(cpu), FadeIn(q), run_time=0.7)
            self.play(hop_bottom(cp, q.slot_point(0)), hop_bottom(cc, q.slot_point(1)), run_time=0.8)
            self.play(FadeIn(mark, scale=0.5), run_time=0.4)
            self.wait(1.5)

        # S06.5
        whistle = whistle_icon(0.7).move_to(P3(2.1, 1.0))
        wlab = Text("scheduler", font_size=20, color=DIM).next_to(whistle, DOWN, buff=0.1)
        spot = Spotlight(height=1.5, spread=0.55).move_beam_to(q.slot_point(0))
        with self.narrate("That's the job of the CPU scheduler, and from our point of view it's unpredictable."):
            self.play(FadeOut(mark), FadeIn(whistle, scale=0.5), FadeIn(wlab), run_time=0.6)
            self.play(FadeIn(spot), run_time=0.6)
            self.wait(1.5)

        # S06.6
        with self.narrate("Both processes sit in the ready queue, and either could be picked."):
            self.play(cp.change("running"), run_time=0.3)
            self.play(hop_seat(cp, cpu), run_time=0.6)
            self.play(Indicate(run1.lines[2], color=PAR), run_time=0.7)
            self.play(hop_bottom(cp, q.slot_point(0)), run_time=0.6)
            self.play(cp.change("ready"), spot.animate.move_beam_to(q.slot_point(1)), run_time=0.6)
            self.play(cc.change("running"), run_time=0.3)
            self.play(hop_seat(cc, cpu), run_time=0.6)
            self.play(Indicate(run2.lines[2], color=CHI), run_time=0.7)
            self.play(hop_bottom(cc, q.slot_point(1)), run_time=0.6)
            self.play(cc.change("ready"), run_time=0.3)

        # S06.7
        with self.narrate("We can't make strong assumptions about what it will choose."):
            for i in (0, 1, 0):
                self.play(spot.animate.move_beam_to(q.slot_point(i)), run_time=0.4)
            self.play(Wiggle(cp, scale_value=1.05), Wiggle(cc, scale_value=1.05), run_time=1.0)

        # S06.8
        tag = ep_tag("→ Concurrency", CONC).move_to(P3(2.1, 1.85))
        with self.narrate("This looks like a small annoyance now. Remember it. In the concurrency section, "
                          "it becomes a very big deal."):
            self.play(prof.change("worried"), FadeIn(tag, scale=0.5), run_time=0.8)
            self.wait(2.5)
        self.beat(1.0)

        # transition: everything fades except the two creatures
        self.play(*[FadeOut(m) for m in (cpu, q, whistle, wlab, spot, tag, run1, run2, l1, l2)],
                  cp.animate.scale(0.55 / 0.7).move_to(P3(-4.6, 1.75)),
                  cc.animate.scale(0.55 / 0.7).move_to(P3(-3.3, 1.75)), run_time=0.8)
