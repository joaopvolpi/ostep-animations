import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common_more import *  # noqa: E402,F401,F403


class S16MigrationEasy(Ep10Scene):
    def construct(self):
        self.world(strip=2, term="load imbalance", stu="frustrated", prof="worried")
        stu, prof = self.stu, self.prof
        st = mq_stage("", "BD")
        c0, c1, q0, q1, grid = st["c0"], st["c1"], st["q0"], st["q1"], st["grid"]
        pB, pD = st["p1"]
        set_cpu_power(c0, False)
        null = mono("NULL", 18, DIM).move_to(P3(MQ_X[0], MQ_Q_Y + 0.25))
        self.add(c0, c1, q0, q1, pB, pD, grid, null)

        # S16.1
        suit = suitcase_icon(0.5, color=DIM).move_to(P3(0, 0.3))
        self.say("The obvious answer: move jobs around. We've seen this word before. Migration.",
                 self.note("migration"), FadeIn(suit, scale=0.6), stu.change("neutral"), prof.change("neutral"))

        # S16.2
        arc = CurvedArrow(P3(1.6, -0.2), P3(-1.6, -0.2), angle=TAU / 8, color=DIM, stroke_width=4)
        self.say("Take a job from a busy CPU, and give it to an idle one.",
                 Create(arc), Indicate(arc, color=CPU_COLOR, scale_factor=1.05))

        # S16.3
        self.say("The easy case first. Queue zero is empty, queue one holds B and D.",
                 Indicate(q0.tray, color=CPU_COLOR), Indicate(q1.tray, color=CPU_COLOR), FadeOut(arc), FadeOut(null))

        # S16.4
        suit2 = suitcase_icon(0.3).next_to(pB, UP, buff=0.0)
        with self.narrate("Just move one of them, say B, over to CPU zero."):
            self.play(FadeIn(suit2, scale=0.5), run_time=0.4)
            _, repack = q1.pop(0)
            q0.items.append(pB)
            self.play(hop_to(pB, q0.slot_point(0), run_time=1.0, height=1.0), suit2.animate.shift(P3(-6.0, 0.0)),
                      repack, run_time=1.0)
            self.play(FadeOut(suit2), cpu_power(c0, True), hop_to(pB, c0.slot_point(), run_time=0.7), run_time=0.8)
            q0.items.remove(pB)
            self.play(pB.change("running"), c0.warmth(3, COL["B"], run_time=1.2), run_time=1.2)

        # S16.5
        okt = tick_mark(0.5).move_to(P3(0, 0.3))
        with self.narrate("One migration, balanced load, everybody's happy."):
            self.play(FadeOut(suit), FadeIn(okt, scale=1.5), stu.change("excited"), run_time=0.6)
            self.play(LaggedStart(*[AnimationGroup(grid.fill(0, c, "B", run_time=0.25), grid.fill(1, c, "D", run_time=0.25))
                                    for c in range(12)], lag_ratio=0.2), run_time=2.0)
        self.beat(0.4)
