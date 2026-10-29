import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


class S11Boost(Ep08Scene):
    def construct(self):
        # starts with the 3-lane layout (card 1 shrunk back into the ladder + timeline)
        self.build(lanes=3, cpu=True, ticks=20, rules=("R1", "R2", "R3", "R4a", "R4b"), holders=("R5",),
                   stu="frustrated", prof="worried", term="starvation")
        lad, cpu, board, tl = self.ladder, self.cpu, self.board, self.tl
        A = self.put("A", 0, 0)
        B = self.put("B", 1, 0)
        C = self.put("C", 1, 1)
        sw = stopwatch_icon(0.3).move_to(cpu.get_center() + UP * 0.0 + LEFT * 0.0)
        sw.move_to(P3(0.9, 0.0))

        # S11.1
        self.say("Let's fix starvation first.", self.prof.change("explaining"), self.stu.change("neutral"))

        # S11.2
        bar = Rectangle(width=2.0, height=0.25).set_fill(DIM, 0.2).set_stroke(TEXT, 2).move_to(P3(-1.0, -0.2))
        fill = Rectangle(width=0.2, height=0.25).set_fill(COL["A"], 1).set_stroke(width=0).align_to(bar, LEFT).match_y(bar)
        fill2 = Rectangle(width=0.5, height=0.25).set_fill(COL["A"], 1).set_stroke(width=0).align_to(bar, LEFT).match_y(bar)
        self.say("What if we guarantee that every job makes some progress?",
                 FadeIn(bar), FadeIn(fill), after(1.0, Transform(fill, fill2, run_time=1.0)))
        self.play(FadeOut(VGroup(bar, fill)), run_time=0.4)

        # S11.3
        self.say("Simple idea: every so often, throw everybody back in the top queue.",
                 FadeIn(sw), Rotate(sw.hand, angle=-TAU, about_point=sw[0].get_center(), run_time=2.0),
                 after(2.2, lad.boost_all()))

        # S11.4
        s_hi = label("S", 26, VIRT, weight=BOLD).next_to(sw, RIGHT, buff=0.1)
        self.say("That's Rule five: after some time period S, move all the jobs in the system to the topmost queue.",
                 board.add_rule("R5", RULES["R5"]), FadeIn(s_hi), after(3.5, self.term("priority boost")))

        # S11.5
        t1 = VGroup(tick_mark(0.25), label("no starvation", 16, PERS)).arrange(RIGHT, buff=0.08).move_to(P3(5.0, -1.45))
        t2 = VGroup(tick_mark(0.25), label("behavior changes", 16, PERS)).arrange(RIGHT, buff=0.08).move_to(P3(5.0, -1.45))
        t1.move_to(P3(4.9, -1.15)); t2.move_to(P3(4.9, -1.5))
        self.say("It solves two problems at once.", FadeIn(t1[0], scale=1.4), after(1.0, FadeIn(t2[0], scale=1.4)))

        # S11.6
        self.say("A job in the top queue shares the CPU round robin, so it can't starve.",
                 FadeIn(t1[1]), Succession(self.to_cpu(A), self.to_lane(A, 2, 2, "ready", t=0.4), self.to_cpu(B), self.to_lane(B, 2, 0, "ready", t=0.4)))

        # S11.7
        kb = keyboard_icon(0.4).next_to(A, UP, buff=0.05)
        self.say("And a CPU-bound job that turned interactive gets treated properly once it's boosted.",
                 FadeIn(t2[1]), self.student_look(), FadeIn(kb, scale=1.3))

        # S11.8
        self.play(FadeOut(VGroup(kb, sw, s_hi, t1, t2)), lad.animate.set_opacity(0.2), cpu.animate.set_opacity(0.2),
                  FadeOut(VGroup(A, B, C)), FadeOut(tl), run_time=0.8)
        tl_l, tl_r = make_half(LEFT_X), make_half(RIGHT_X)
        set_cells(tl_l, FIG82[:2]); tl_l.set_span("Q0", 2, 10, "running", COL["A"])
        set_cells(tl_r, FIG84_RIGHT[:10]); tl_r.set_span("Q0", 2, 10, "running", COL["A"])
        ttl = label("without boost", 22, DIM).move_to(P3(-3.4, -0.45))
        ttr = label("with boost", 22, DIM).move_to(P3(1.0, -0.45))
        self.say("Here's the long job A, competing with two short interactive jobs, B and C.",
                 FadeIn(tl_l), FadeIn(tl_r), FadeIn(ttl), FadeIn(ttr))

        # S11.9
        starved = label("starved", 22, KERNEL_COLOR, weight=BOLD).move_to(P3(-1.0 - 1.5, -1.95))
        starved.move_to(tl_l.cell_center("Q0", 16))
        fills = [tl_l.fill("Q2", t, "running", color=COL["B"] if t % 2 else COL["C"], run_time=0.3) for t in range(11, 21)]
        self.say("On the left, no boost: once B and C arrive, A is starved.", Succession(*fills), after(3.6, FadeIn(starved)))

        # S11.10
        mk = [tl_r.boundary_marker(10, None, color=VIRT), tl_r.boundary_marker(20, None, color=VIRT)]
        swr = VGroup(stopwatch_icon(0.2), label("S = 100 ms", 18, VIRT)).arrange(RIGHT, buff=0.1).move_to(P3(0.9, -2.9))
        rfills = []
        for row, t, n in FIG84_RIGHT[10:]:
            rfills.append(tl_r.fill(row, t, "running", color=COL[n], run_time=0.3))
        self.say("On the right, we boost every hundred milliseconds.", FadeIn(mk[0]), FadeIn(swr), Succession(*rfills), after(4.0, FadeIn(mk[1])))

        # S11.11
        cap = label("S = 100 ms (too small, but good for a picture)", 18, DIM).move_to(P3(0.2, -3.2))
        self.say("That's too small for a real system, but fine for a picture.", FadeIn(cap))

        # S11.12
        self.say("Now A runs periodically.", self.stu.change("curious"), Indicate(tl_r.blocks_in("Q2", ticks=[11]), color=COL["A"], scale_factor=1.6))
        self.beat(1.0)

    def student_look(self):
        return self.stu.change("curious")
