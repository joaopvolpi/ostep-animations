import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


class S06MlfqWars(Ep11Scene):
    def construct(self):
        self.world(stu="frustrated", prof="worried", mode="corner")
        stu, prof = self.stu, self.prof
        world5 = build_s05_end()
        self.add(world5)

        ladder = make_ladder()
        sjf = VGroup(Spotlight(height=0.7, spread=0.3), label("SJF", 22, DIM)).arrange(DOWN, buff=0.1).move_to(P3(-3.6, 1.0))
        rr = VGroup(loop_arrow(0.3, CPU_COLOR), label("RR", 22, DIM)).arrange(DOWN, buff=0.1).move_to(P3(-0.6, 1.0))

        # S06.1
        with self.narrate("That you can build a smart scheduler that's like SJF and round robin at once.", min_time=4.5):
            self.play(FadeOut(world5), FadeIn(sjf), FadeIn(rr), stu.change("excited"))
            self.wait(1.0)
            self.play(sjf.animate.move_to(P3(-2.4, 0.9)), rr.animate.move_to(P3(-1.4, 0.9)), run_time=0.8)
            self.play(FadeOut(sjf), FadeOut(rr), FadeIn(ladder), run_time=0.8)

        # S06.2
        C = proc("C", "running", scale=0.6, label=None)
        Bj = proc("B", "running", scale=0.6, label=None)
        ladder.place(C, 2)
        ladder.place(Bj, 2, slot=2)
        Bj.move_to(ladder.lane_point(2, 2))
        ladder.release(Bj)
        Bj.shift(RIGHT * 5)
        with self.narrate("MLFQ was pretty neat.", min_time=5.5):
            self.play(FadeIn(C, shift=LEFT * 0.4), run_time=0.5)
            self.play(ladder.demote(C))
            self.play(ladder.demote(C))
            self.play(FadeIn(Bj), run_time=0.3)
            self.play(Bj.animate.move_to(ladder.lane_point(2, 1)), run_time=0.5)
            self.play(Bj.change("done"), run_time=0.5)
            self.play(FadeOut(Bj), run_time=0.4)

        # S06.3
        gears = VGroup(GearPair(0.2), GearPair(0.2)).arrange(DOWN, buff=0.6).move_to(P3(1.0, 0.9))
        sparks = VGroup(*[Line(ORIGIN, UP * 0.15).set_stroke(CPU_COLOR, 3).rotate(a).move_to(gears[i % 2].get_center() + 0.3 * np.array([np.cos(a + PI / 2), np.sin(a + PI / 2), 0]))
                          for i, a in enumerate((0.0, 1.5, 3.0, 4.5))])
        self.say("But a real scheduler seems difficult.", stu.change("confused"),
                 Succession(FadeIn(gears), AnimationGroup(Wiggle(ladder, scale_value=1.03, rotation_angle=0.01 * TAU, run_time=1.0), FadeIn(sparks)), FadeOut(sparks)),
                 min_time=2.8)

        # S06.4
        tags = VGroup(name_tag("CFS", 22), name_tag("BFS", 22), name_tag("O(1)", 22))
        tags[0].move_to(P3(2.7, 1.6)); tags[1].move_to(P3(3.7, 0.5)); tags[2].move_to(P3(4.9, 1.6))
        puffs = VGroup(puff(0.25).move_to(P3(3.2, 1.1)), puff(0.25).move_to(P3(4.3, 1.1)))
        self.say("Indeed. Look at the Linux battles between CFS, BFS and the O(1) scheduler.",
                 prof.change("explaining"), FadeOut(gears), LaggedStart(*[FadeIn(t) for t in tags], lag_ratio=0.3),
                 Succession(Wait(2.5), AnimationGroup(Wiggle(tags[0]), Wiggle(tags[2]), FadeIn(puffs)), FadeOut(puffs)),
                 min_time=5.0)

        # S06.5
        lines = VGroup(*[Line(ORIGIN, RIGHT * w).set_stroke(DIM, 6) for w in (2.0, 1.7, 2.1)]).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        lines.move_to(P3(3.7, -0.5))
        bar = censor_bar(2.4, 0.9).move_to(lines)
        self.say("And no, I will not spell out the full name of BFS.", prof.change("neutral", look_at=P3(5.8, 2.0)),
                 Succession(Create(lines), FadeIn(bar)), min_time=3.5)

        # S06.6
        thumb = hand_icon(0.45, COMPUTER_COLOR).rotate(PI / 2 * 0).move_to(stu.get_top() + UP * 0.5)
        self.say("And I won't ask you to!", stu.change("excited"), FadeIn(thumb, shift=UP * 0.2), min_time=2.0)
        self.beat(0.5)
