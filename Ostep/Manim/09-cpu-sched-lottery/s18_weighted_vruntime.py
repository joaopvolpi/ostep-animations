import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


class S18WeightedVruntime(Ep09Scene):
    def construct(self):
        self.world(term="weight", stu="neutral", prof="neutral")
        stu, prof = self.stu, self.prof
        mA = VruntimeMeter(COL["A"], height=2.2, width=0.5, max_value=40.0).move_to(P3(-2.4, -0.1))
        mB = VruntimeMeter(COL["B"], height=2.2, width=0.5, max_value=40.0).move_to(P3(2.4, -0.1))
        la = proc("A", scale=0.45).next_to(mA, DOWN, buff=0.1)
        lb = proc("B", scale=0.45).next_to(mB, DOWN, buff=0.1)
        cpu = CPU(size=0.9, label="CPU").move_to(P3(0, 1.5))
        tl = Timeline(["CPU"], ticks=8, x_range=(-3.0, 3.0), top=-2.55, row_height=0.34, row_kinds=["cpu"],
                      tick_labels=False, label_font=18)
        self.add(mA, mB, la, lb, cpu, tl)
        spot = Spotlight(height=0.8, spread=0.3)
        spot.move_beam_to(P3(-2.4, -1.35))

        # S18.1
        eq = MathTex(r"\text{vruntime}_i \mathrel{+}= ", r"\frac{\text{weight}_0}{\text{weight}_i}", r"\cdot \text{runtime}_i",
                     font_size=34, color=TEXT).move_to(P3(0, 2.4))
        w0 = Text("weight₀ = 1024", font_size=20, color=CPU_COLOR).move_to(P3(0, 0.35))
        self.say("vruntime is scaled too: it grows by real run time times one thousand twenty-four, over the weight.",
                 Write(eq), Succession(Wait(2.5), Indicate(eq[1], color=CPU_COLOR), FadeIn(w0)))

        # S18.2
        ghost = DashedLine(mA.get_left() + UP * (-1.1 + 0.3 * 2.14 + 0.0), mA.get_right() + UP * (-1.1 + 0.3 * 2.14),
                           color=DIM, dash_length=0.08)
        ghost.move_to(P3(-2.4, mA.top_point()[1] + 0.0))
        ghost_y = mA.frame.get_bottom()[1] + 0.03 + (2.2 - 0.06) * 0.3
        ghost.move_to(P3(-2.4, ghost_y))
        gl = Text("if A were B", font_size=16, color=DIM).next_to(ghost, LEFT, buff=0.08)
        runs = ["A", "A", "A", "B", "A", "A", "A", "B"]
        fills = []
        with self.narrate("A, being heavier, accumulates vruntime at a third of B's rate, so it keeps winning and runs longer."):
            self.play(FadeIn(spot), FadeIn(ghost), FadeIn(gl), run_time=0.6)
            self.play(hop_to(la, cpu.slot_point(), run_time=0.7), mA.add_runtime(12, weight=3121, run_time=1.5),
                      tl.fill("CPU", 1, "running", color=COL["A"], run_time=1.5))
            self.play(la.animate.move_to(la.get_center()), tl.fill("CPU", 2, "running", color=COL["A"], run_time=0.4),
                      tl.fill("CPU", 3, "running", color=COL["A"], run_time=0.4), run_time=0.5)
            self.play(hop_bottom(la, mA.get_bottom() + DOWN * 0.55, run_time=0.6),
                      spot.animate(run_time=0.8).move_beam_to(P3(2.4, -1.35)))
            self.play(hop_to(lb, cpu.slot_point(), run_time=0.7), mB.add_runtime(12, weight=1024, run_time=1.5),
                      tl.fill("CPU", 4, "running", color=COL["B"], run_time=1.5))
            self.play(hop_bottom(lb, mB.get_bottom() + DOWN * 0.55, run_time=0.6),
                      spot.animate(run_time=0.8).move_beam_to(P3(-2.4, -1.35)),
                      *[tl.fill("CPU", t, "running", color=COL[runs[t - 1]], run_time=0.2) for t in (5, 6, 7, 8)])

        # S18.3
        self.say("Heavier means a longer slice and a slower meter!", stu.change("excited"))

        # S18.4
        p1 = token("nice -5 vs 0  →  3 : 1", TEXT, size=22).move_to(P3(0, -0.4))
        p2 = token("nice 5 vs 10  →  3 : 1", TEXT, size=22).move_to(P3(0, -1.1))
        ok = tick_mark(0.3).next_to(p2, RIGHT, buff=0.15)
        self.say("And the table only cares about the difference in nice values. Five and ten behave exactly like minus "
                 "five and zero.",
                 prof.change("proud"), FadeOut(w0), FadeIn(p1), Succession(Wait(2.5), FadeIn(p2), FadeIn(ok)))
        self.beat(0.8)
        self.play(FadeOut(VGroup(mA, mB, la, lb, cpu, tl, eq, spot, ghost, gl, p1, p2, ok)), run_time=0.8)
