import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


class S09Example3(Ep08Scene):
    def construct(self):
        A = s08_end(self, stu="excited", prof="proud")
        lad, cpu, board = self.ladder, self.cpu, self.board
        # starts with: timeline cleared, tag swapped, A on the CPU (ticks 1-2 prefilled as in Example 1)
        self.remove(self.tl, self.approx, self.ex_tag)
        tl = self.tl = make_tl(20)
        set_cells(tl, FIG82[:2])
        ex = ex_tag("Example 3: interactive job with I/O")
        self.add(tl, ex)
        lad.register(A, 0, 0); lad.release(A)
        self.stu.set_expression("neutral"); self.prof.set_expression("neutral")
        U = 0.1

        # S09.1
        self.say("Third example: I/O.", self.stu.change("neutral", look_at=tl), self.prof.change("neutral"))

        # S09.2
        B = job("B", lad.job_scale)
        B.move_to(lad.lane_point(2, 0))
        lad.register(B, 2, 0)
        kb = keyboard_icon(0.45).next_to(B, RIGHT, buff=0.15)
        tag = label("1 ms of CPU, then input", 18, TEXT).next_to(kb, RIGHT, buff=0.15)
        self.say("Suppose B, the interactive job, only needs one millisecond of CPU before it asks for input, and it's competing with the long job A.",
                 FadeIn(B, shift=DOWN * 0.4), FadeIn(kb), FadeIn(tag))
        gB = self.attach_gauge(B, 1.0, 1.0)

        # S09.3
        clk = ClockIcon(0.3, color=TEXT).move_to(BLOCK_AT)
        self.say("B runs for one millisecond and then blocks.",
                 Succession(AnimationGroup(self.to_lane(A, 0, 0, "ready"), FadeOut(tag), FadeOut(kb)), self.to_cpu(B), FadeIn(gB),
                            AnimationGroup(gB.drain(0.1, run_time=0.4), tl.fill_span("Q2", 2, 2 + U, "running", COL["B"], run_time=0.4)),
                            Succession(SetExpr(B, "blocked"), hop_to(B, BLOCK_SPOT, run_time=0.5), FadeIn(clk))))

        # S09.4
        used = label("used 1 of 10 ms", 18, CPU_COLOR).move_to(P3(1.7, -0.15))
        self.say("That is giving up the CPU before the allotment is used up.",
                 Indicate(gB, color=CPU_COLOR, scale_factor=1.3), FadeIn(used))

        # S09.5
        self.say("So Rule four B applies: B stays at the same priority level.",
                 board.glow("R4b"), Succession(clk.spin(1, run_time=1.2), FadeOut(clk), gB.reset(0.4), self.to_lane(B, 2, 0, "ready")),
                 FadeOut(used))

        # S09.6
        loops = []
        a_end = 2 + U
        for k, b0 in enumerate((6, 10, 14)):
            loops.append(Succession(
                self.to_cpu(A),
                tl.fill_span("Q0", a_end, b0, "running", COL["A"], run_time=0.9 if k == 0 else 0.6),
                self.to_lane(A, 0, 0, "ready", t=0.4),
                self.to_cpu(B),
                AnimationGroup(gB.drain(0.1, run_time=0.3), tl.fill_span("Q2", b0, b0 + U, "running", COL["B"], run_time=0.3)),
                Succession(SetExpr(B, "blocked"), hop_to(B, BLOCK_SPOT, run_time=0.4)),
                gB.reset(0.3), self.to_lane(B, 2, 0, "ready", t=0.4)))
            a_end = b0 + U
        self.say("Each time B comes back from its I/O, it's still at the top, still ahead of A.", *[], Succession(*loops), min_time=1.0)
        # (the loops run in the narration of S09.6 below)

        # S09.7
        rest = [("Q0", a_end, 18.0, "A"), ("Q2", 18.0, 18.0 + U, "B"), ("Q0", 18.0 + U, 20.0, "A")]
        fin = [tl.fill_span(r, b0, b1, "running", COL[n], run_time=0.5) for r, b0, b1, n in rest]
        tick = tick_mark(0.35).next_to(B, RIGHT, buff=0.15)
        rt = label("response time: low", 20, DIM).move_to(P3(1.7, -0.15))
        self.say("The interactive job stays snappy, which is exactly the goal.",
                 self.to_cpu(A), Succession(*fin), Succession(Wait(0.8), FadeIn(tick, scale=1.4), FadeIn(rt)))
        self.beat(1.0)
