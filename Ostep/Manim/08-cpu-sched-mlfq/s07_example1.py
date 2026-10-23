import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


class S07Example1(Ep08Scene):
    def construct(self):
        s06_end(self, stu="neutral", prof="neutral")
        lad, cpu, board, tl = self.ladder, self.cpu, self.board, self.tl
        # S06 ends with R5 as a placeholder; R4b added
        A = job("A", lad.job_scale)
        A.move_to(lad.lane_point(2, 0).copy() + UP * 0.0)
        A.move_to(P3(-3.0, 2.05))
        spot = Spotlight(height=0.6, spread=0.3)
        spot.move_beam_to(lad.lane_point(0, 3))
        self.add(spot)

        # S07.1
        ex = label("Example 1: one long job", 22, DIM).move_to(P3(-2.0, 2.65 - 0.0))
        ex.move_to(P3(-0.7, -3.05))
        self.say("First example. One long-running job, A, alone in the system.",
                 FadeIn(ex), FadeIn(A, shift=DOWN * 0.3), FadeOut(self.slice_tag))
        self.slice_tag = None

        # S07.2
        g = self.attach_gauge(A, 1.0, 1.0)
        self.say("It arrives in the top queue, Q2.",
                 lad.promote(A, 2, 0, run_time=0.8), spot.animate(run_time=1.0).move_beam_to(lad.lane_point(2, 3)), board.glow("R3"))

        # S07.3
        self.say("After ten milliseconds, it has used its allotment, so it moves down to Q1.",
                 Succession(self.to_cpu(A), FadeIn(g), AnimationGroup(g.drain(1.0, run_time=1.3), cell_run(tl, "Q2", 1, "A", 1.3)),
                            AnimationGroup(self.to_lane(A, 1, 0, "ready"), g.reset(0.4), board.glow("R4a", run_time=1.2))))

        # S07.4
        self.say("Another ten milliseconds, and it moves down again, to Q0.",
                 Succession(self.to_cpu(A), AnimationGroup(g.drain(1.0, run_time=1.2), cell_run(tl, "Q1", 2, "A", 1.2)),
                            AnimationGroup(self.to_lane(A, 0, 0, "ready"), g.reset(0.4), board.glow("R4a", run_time=1.0))))

        # S07.5
        runs = [cell_run(tl, "Q0", t, "A", 0.22 if t < 8 else 0.12) for t in range(3, 21)]
        self.say("And there it stays, running in the lowest queue until it's done.",
                 Succession(self.to_cpu(A), FadeOut(g), *runs))

        # S07.6
        self.say("Pretty simple.", Indicate(tl.blocks_in("Q0"), color=COL["A"], scale_factor=1.05))
        self.beat(1.0)
