import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common_more import *  # noqa: E402,F401,F403

ROW0 = "AAAABABABBBB"
ROW1 = "BDBDDDDDADAD"


class S17MigrationHard(Ep10Scene):
    def construct(self):
        self.world(strip=2, term="migration", stu="excited", prof="neutral")
        stu, prof = self.stu, self.prof
        st = mq_stage("B", "D")
        c0, c1, q0, q1, grid = st["c0"], st["c1"], st["q0"], st["q1"], st["grid"]
        pB, = st["p0"]
        pD, = st["p1"]
        self.add(c0, c1, q0, q1, pB, pD, grid)
        self.on_trays([pB, pD], [q0, q1])
        finish_now(c0.warmth(3, COL["B"]))
        for c in range(12):
            grid.set(0, c, "B")
            grid.set(1, c, "D")

        # S17.1 rewind to: Q0 = A, Q1 = B, D
        pA = proc("A", "ready", 0.4)
        place_on(pA, P3(-6.0, 1.8))
        self.say("And the harder case?",
                 stu.change("curious"), grid.clear())
        _, rep = q0.pop(0)
        q0.items.clear()
        self.add(pA)
        self.on_trays([pA], [q0, q1])
        with self.narrate("Here's a trickier one. A is alone on CPU zero. B and D share CPU one."):
            self.play(hop_to(pB, q1.slot_point(0), run_time=0.8, height=0.1), run_time=0.8)
            q1.items.insert(0, pB)
            self.play(q1.pack(), run_time=0.5)
            self.play(q0.push(pA), run_time=0.8)
            self.play(Indicate(pA, color=COL["A"]), Indicate(pB, color=COL["B"]), Indicate(pD, color=COL["D"]), run_time=0.8)

        # S17.3 flip
        flip = MathTex(r"\leftrightarrow", color=KERNEL_COLOR).scale(1.4).move_to(P3(0, -0.3))
        same = tag("same problem, flipped", 18, KERNEL_COLOR).move_to(P3(0, -1.0))
        with self.narrate("One migration doesn't fix this: moving B just flips the problem."):
            _, rep = q1.pop(0)
            q0.items.append(pB)
            self.play(hop_to(pB, q0.slot_point(1), run_time=0.9, height=0.1), rep, FadeIn(flip, scale=0.6), FadeIn(same), run_time=0.9)
            self.wait(0.5)
            _, rep = q0.pop(1)
            q1.items.insert(0, pB)
            self.play(hop_to(pB, q1.slot_point(0), run_time=0.9, height=0.1), q1.pack(), rep, run_time=0.9)
            self.play(FadeOut(flip), FadeOut(same), run_time=0.4)

        # S17.4
        frac = MathTex(r"\frac{3\ \text{jobs}}{2\ \text{CPUs}} = 1.5", color=TEXT).scale(0.9).move_to(P3(0, 0.3))
        suit = suitcase_icon(0.5).move_to(P3(0, -0.6))
        loop = loop_arrow(0.45, color=VIRT).move_to(suit)
        self.say("The load is three jobs on two CPUs. Nobody can give a whole CPU's worth to everyone, "
                 "so the answer is continuous migration.",
                 FadeIn(frac, shift=UP * 0.2), Succession(Wait(2.0), FadeIn(suit, scale=0.6), Create(loop)))

        # S17.5
        self.say("First A alone on CPU zero, and B and D alternate on CPU one.",
                 LaggedStart(*[AnimationGroup(grid.fill(0, c, ROW0[c], run_time=0.25), grid.fill(1, c, ROW1[c], run_time=0.25))
                               for c in range(4)], lag_ratio=0.5), FadeOut(frac), run_time=3.2)

        # S17.6
        cold = label("cold", 18, MEM_COLOR).move_to(c0.cache_bottom() + DOWN * 0.2)
        with self.narrate("After a few time slices, B moves to CPU zero to compete with A…"):
            _, rep = q1.pop(0)
            q0.items.append(pB)
            self.play(hop_to(pB, q0.slot_point(1), run_time=0.9, height=0.1), rep, run_time=0.9)
            self.play(LaggedStart(*[grid.fill(0, c, ROW0[c], run_time=0.25) for c in range(4, 8)], lag_ratio=0.5),
                      FadeIn(cold, scale=1.3), Indicate(c0.strip, color=MEM_COLOR), run_time=1.6)

        # S17.7
        self.say("…while D enjoys a few slices alone on CPU one.",
                 LaggedStart(*[grid.fill(1, c, ROW1[c], run_time=0.25) for c in range(4, 8)], lag_ratio=0.5),
                 FadeOut(cold))

        # S17.8
        share = tag("everyone gets 2/3 of a CPU", 20, CPU_COLOR).move_to(P3(0, -1.45))
        with self.narrate("And the load stays balanced, over time."):
            _, rep = q0.pop(0)
            q1.items.append(pA)
            self.play(hop_to(pA, q1.slot_point(1), run_time=0.9, height=0.1), rep, run_time=0.9)
            self.play(LaggedStart(*[AnimationGroup(grid.fill(0, c, ROW0[c], run_time=0.25), grid.fill(1, c, ROW1[c], run_time=0.25))
                                    for c in range(8, 12)], lag_ratio=0.5), FadeIn(share), run_time=2.0)

        # S17.9
        qm = question_mark(0.6).move_to(suit.get_center() + UP * 0.6)
        self.say("There are many other migration patterns. But the real question is the decision: "
                 "how should the system decide to migrate?",
                 prof.change("explaining"), FadeIn(qm, scale=0.5), Indicate(suit, color=CPU_COLOR))
        self.beat(0.8)
        # hand-off to S18: the bare CPUs and queues
        self.fade_stage(c0, c1, q0, q1, extra=(c0.warmth(0, COL["B"]),))
