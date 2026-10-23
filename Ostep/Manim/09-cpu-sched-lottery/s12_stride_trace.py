import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403
from s11_stride_basics import LANE_Y, STRIDE  # noqa: E402

X0, SC = -4.6, 0.033     # pass 0..200 fits x in [-4.6, 2.0]


class S12StrideTrace(Ep09Scene):
    def construct(self):
        self.world(stu="neutral", prof="neutral")
        stu, prof = self.stu, self.prof
        lanes = {n: PassLane(n, COL[n], STRIDE[n], LANE_Y[n], x0=X0, scale=SC, length=200) for n in "ABC"}
        procs = {n: proc(n, scale=0.5).move_to(P3(X0 - 0.7, LANE_Y[n] - 0.1)) for n in "ABC"}
        bars = {n: lanes[n].stride_bar for n in "ABC"}
        for n in "ABC":
            bars[n].stretch_to_fit_width(STRIDE[n] * SC).move_to(P3(X0 + STRIDE[n] * SC / 2, LANE_Y[n] - 0.2))
        table = PassTable(top_left=(2.4, 2.3))
        tl = Timeline(["CPU"], ticks=8, x_range=(-4.0, 2.0), top=-2.4, row_height=0.4, row_kinds=["cpu"],
                      tick_labels=False, label_font=20)
        spot = Spotlight(height=0.9, spread=0.35)
        spot.move_beam_to(P3(X0, LANE_Y["A"]))
        axis = Line(P3(X0, 2.15), P3(X0 + 200 * SC, 2.15)).set_stroke(DIM, 2)
        axl = VGroup(*[Text(str(v), font_size=18, color=DIM).move_to(P3(X0 + v * SC, 1.9)) for v in (0, 100, 200)])
        self.add(*lanes.values(), *procs.values(), *bars.values(), axis, axl)
        self.play(FadeIn(table), FadeIn(tl), FadeIn(spot), run_time=0.8)

        tick = {"n": 0}

        def step(who, row_vals, new_pass, rt=0.6, spot_to=True):
            tick["n"] += 1
            anims = [table.add_row(row_vals, who, run_time=rt * 0.6)]
            if spot_to:
                anims.append(spot.animate(run_time=rt * 0.8).move_beam_to(P3(X0 + row_vals["ABC".index(who)] * SC, LANE_Y[who])))
            return AnimationGroup(*anims), AnimationGroup(
                tl.fill("CPU", tick["n"], "running", color=COL[who], run_time=rt * 0.6),
                lanes[who].flag_to(new_pass, run_time=rt), procs[who].animate(run_time=rt).scale(1.0))

        # S12.1
        tie = Text("tie → pick A", font_size=20, color=DIM).move_to(P3(-1.0, 2.45))
        a1, a2 = step("A", (0, 0, 0), 100)
        self.say("Everyone starts at zero, so pick A.", a1, FadeIn(tie), a2)
        self.play(FadeOut(tie), run_time=0.3)

        # S12.2
        self.say("After its slice, A's pass is a hundred.", Indicate(lanes["A"].flag, color=COL["A"]))

        # S12.3
        a1, a2 = step("B", (100, 0, 0), 200)
        self.say("B and C are lower, so B runs next.", a1, Succession(Wait(0.8), a2))

        # S12.4
        a1, a2 = step("C", (100, 200, 0), 40)
        self.say("B's pass becomes two hundred. Now C is lowest, runs, and goes to forty.", a1, Succession(Wait(1.5), a2))

        # S12.5
        with self.narrate("C is still lowest. It runs again: eighty. Again: a hundred and twenty."):
            for vals, newp in (((100, 200, 40), 80), ((100, 200, 80), 120)):
                a1, a2 = step("C", vals, newp)
                self.play(a1, a2, run_time=0.9)
                self.beat(0.4)

        # S12.6
        a1, a2 = step("A", (100, 200, 120), 200)
        self.say("Now A, at a hundred, runs.", a1, Succession(Wait(0.6), a2))

        # S12.7
        cyc = Line(P3(X0 + 200 * SC, 2.0), P3(X0 + 200 * SC, -1.2)).set_stroke(CPU_COLOR, 3)
        cyc_l = Text("cycle complete", font_size=20, color=CPU_COLOR).move_to(P3(X0 + 200 * SC - 0.2, -1.45))
        with self.narrate("And so on."):
            for vals, newp in (((200, 200, 120), 160), ((200, 200, 160), 200)):
                a1, a2 = step("C", vals, newp, rt=0.4)
                self.play(a1, a2, run_time=0.5)
            self.play(table.add_row((200, 200, 200), "A", run_time=0.3) if False else FadeIn(cyc), FadeIn(cyc_l), run_time=0.5)
        self.play(FadeOut(spot), run_time=0.3)

        # S12.8
        counts = {"C": 5, "A": 2, "B": 1}
        tally = VGroup()
        x = -3.9
        for n in "CAB":
            r = Rectangle(width=0.5 * counts[n], height=0.3).set_fill(COL[n], 1).set_stroke(TEXT, 1)
            t = Text(f"{n} ×{counts[n]}", font_size=20, color=COL[n])
            tally.add(VGroup(r, t.next_to(r, DOWN, buff=0.05)))
        tally.arrange(RIGHT, buff=0.25, aligned_edge=UP).move_to(P3(-1.0, -3.2))
        self.say("Follow it to the end of the cycle, when all three passes meet at two hundred. "
                 "C ran five times, A twice, B once.",
                 FadeOut(VGroup(cyc, cyc_l)), FadeIn(tally))

        # S12.9
        ratio = MathTex(r"250:100:50=5:2:1", font_size=32, color=TEXT).move_to(P3(4.2, -2.4))
        ok = tick_mark(0.35).next_to(ratio, RIGHT, buff=0.15)
        self.say("Five, two, one: exactly the ratio of their tickets, two hundred and fifty, a hundred, and fifty.",
                 Write(ratio), Succession(Wait(2.5), FadeIn(ok)))

        # S12.10
        self.say("Exactly. Not \"probably\". Every time.", stu.change("surprised"))

        # S12.11
        self.say("Every time. Small stride, large share: the busy ones barely advance on the number line.",
                 prof.change("proud"), Indicate(bars["C"], color=COL["C"], scale_factor=1.3))
        self.beat(0.6)
        self.play(FadeOut(VGroup(*lanes.values(), *procs.values(), *bars.values(), axis, axl, table, tl, tally, ratio, ok)),
                  run_time=0.8)
