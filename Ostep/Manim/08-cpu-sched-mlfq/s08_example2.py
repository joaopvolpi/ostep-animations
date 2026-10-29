import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


class S08Example2(Ep08Scene):
    def construct(self):
        A = s07_end(self)
        lad, cpu, board, tl = self.ladder, self.cpu, self.board, self.tl
        lad.register(A, 0, 0)
        lad.release(A)
        spot = Spotlight(height=0.6, spread=0.3)
        spot.move_beam_to(lad.lane_point(0, 3))
        self.add(spot)
        gA = self.attach_gauge(A, 1.0, 1.0)

        # S08.1
        ex2 = ex_tag("Example 2: a short job arrives")
        now = tl.boundary_marker(10, "now", color=CPU_COLOR, font_size=20, extra=0.0)
        self.say("Now a more interesting one. A is still running in the lowest queue.",
                 Transform(self.ex_tag, ex2), tl.unfill_ticks(list(range(11, 21)), run_time=0.8), FadeIn(now), FadeOut(gA) if False else Wait(0.1))
        tl.purge()
        self.remove(gA)
        gA = None

        # S08.2
        B = job("B", lad.job_scale)
        B.move_to(P3(-3.0, 3.05))
        lad.register(B, 2, 0)
        need = VGroup(label("needs 20 ms", 16, TEXT), *[Rectangle(width=0.3, height=0.2).set_fill(COL["B"], 1).set_stroke(TEXT, 1) for _ in range(2)])
        need[1:].arrange(RIGHT, buff=0.02)
        need.arrange(DOWN, buff=0.05).next_to(P3(-3.0, 2.05), RIGHT, buff=0.55)
        self.say("At time one hundred milliseconds, B arrives. B is an interactive job, and it only needs twenty milliseconds of CPU.",
                 FadeIn(B, shift=DOWN * 0.1), FadeIn(need))

        # S08.3
        self.say("Rule three puts B in the top queue.",
                 B.animate.move_to(lad.lane_point(2, 0)), board.glow("R3"), spot.animate.move_beam_to(lad.lane_point(2, 3)), run_time=1.0)
        need.next_to(B, RIGHT, buff=0.15)

        # S08.4
        self.remove(spot)
        spot = Spotlight(height=0.6, spread=0.3)
        spot.move_beam_to(lad.lane_point(2, 3))
        self.add(spot)
        self.say("By Rule one, B beats A, so B runs.",
                 board.glow("R1"), Succession(self.to_lane(A, 0, 0, "ready"), self.to_cpu(B)), cell_run(tl, "Q2", 11, "B", 1.5),
                 FadeOut(need[0]), spot.animate.move_beam_to(lad.lane_point(2, 3)))
        gB = self.attach_gauge(B, 1.0, 1.0)
        self.add(gB)

        # S08.5
        self.say("Ten milliseconds later, B has used its allotment, and it moves down to Q1.",
                 gB.drain(1.0, run_time=1.5), cell_run(tl, "Q2", 11, "B", 0.1) if False else Wait(0.1),
                 after(1.6, AnimationGroup(self.to_lane(B, 1, 0, "ready"), board.glow("R4a", run_time=1.0), gB.reset(0.4), cell_run(tl, "Q1", 12, "B", 1.0))),
                 spot.animate.move_beam_to(lad.lane_point(1, 3)))

        # S08.6
        with self.narrate("Ten more, and B is finished, before it ever reaches the bottom."):
            self.play(self.to_cpu(B), cell_run(tl, "Q1", 13, "B", 0.01) if False else Wait(0.1), run_time=0.7)
            self.play(gB.drain(0.5, run_time=1.2), Indicate(lad.lane_rect(1), color=CPU_COLOR, run_time=1.2))
            self.play(B.change("done"), run_time=0.6)
            self.play(FadeOut(VGroup(B, gB, need[1:])), run_time=0.7)

        # S08.7
        runs = [cell_run(tl, "Q0", t, "A", 0.3) for t in range(13, 21)]
        self.say("Now A resumes where it left off.", Succession(self.to_cpu(A), *runs), FadeOut(now), spot.animate.move_beam_to(lad.lane_point(0, 3)))

        # S08.8
        callout = label("never told it!", 22, KERNEL_COLOR).move_to(P3(-3.0, 1.15 + 1.3))
        callout.move_to(P3(-2.4, 2.65 - 0.5))
        self.say("Wait. We never told the scheduler B was short!", self.stu.change("excited"), FadeIn(callout, scale=1.3))

        # S08.9
        self.say("Right. That's the beauty of it.", self.prof.change("proud"), FadeOut(callout))

        # S08.10
        bub = label("probably short?", 22, TEXT)
        bub = VGroup(RoundedRectangle(width=bub.width + 0.4, height=0.5, corner_radius=0.2).set_fill(CARD_FILL, 1).set_stroke(DIM, 2), bub)
        bub[1].move_to(bub[0])
        bub.move_to(P3(-2.4, 1.1))
        B2 = job("B", lad.job_scale)
        lad.register(B2, 2, 0)
        B2.move_to(lad.lane_point(2, 0))
        self.say("Since MLFQ can't know whether a job is short or long, it first assumes it might be short, and gives it high priority.",
                 FadeIn(B2, scale=1.3), FadeIn(bub), spot.animate.move_beam_to(lad.lane_point(2, 3)))

        # S08.11
        a1 = VGroup(job("B", 0.3), tick_mark(0.25)).arrange(RIGHT, buff=0.1)
        a2 = VGroup(job("A", 0.3), Arrow(UP * 0.2, DOWN * 0.2, buff=0, color=KERNEL_COLOR, stroke_width=4, tip_length=0.1)).arrange(RIGHT, buff=0.1)
        t1 = label("runs quickly, completes", 16, PERS)
        t2 = label("sinks, proves itself long", 16, KERNEL_COLOR)
        m1 = VGroup(a1, t1).arrange(RIGHT, buff=0.15).move_to(P3(-3.0, 2.05))
        m2 = VGroup(a2, t2).arrange(RIGHT, buff=0.15).move_to(P3(-3.0, 1.1))
        self.say("If it really is short, it runs quickly and completes. If it isn't, it sinks down the queues and proves itself a long, batch-like job.",
                 FadeOut(bub), FadeOut(B2), FadeOut(spot), FadeIn(m1), after(2.5, FadeIn(m2)), self.prof.change("explaining"))

        # S08.12
        approx = approx_tag()
        self.say("In this way MLFQ approximates SJF.", FadeOut(VGroup(m1, m2)), FadeIn(approx, scale=1.2), min_time=2.5)
        self.beat(1.5)
