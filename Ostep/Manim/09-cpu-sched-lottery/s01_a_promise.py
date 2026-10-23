import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403

PIE_AT = P3(3.4, 1.0)


class S01APromise(Ep09Scene):
    def construct(self):
        # S01.1
        rack = server_rack_icon(1.0, 1.8).scale(1.1).move_to(P3(0, 0.9))
        chip = CPU(size=0.42, label="", pins=3).move_to(rack.get_center() + UP * 0.1)
        self.say("Picture a cloud server.", FadeIn(rack), FadeIn(chip, scale=0.6),
                 Succession(Wait(0.6), Indicate(chip, color=CPU_COLOR, scale_factor=1.3)))

        # S01.2
        a, b = proc("A", scale=0.6), proc("B", scale=0.6)
        for p in (a, b):
            p.move_to(rack.get_center())
        apos, bpos = P3(-3.4, 2.1), P3(-3.4, 0.5)
        pie = TargetPie((0.75, 0.25), radius=1.0, label=None).move_to(PIE_AT)
        l75 = Text("75%", font_size=26, color=INK_DARK).move_to(PIE_AT + P3(-0.35, -0.2))
        l25 = Text("25%", font_size=26, color=INK_DARK).move_to(PIE_AT + P3(0.42, 0.45))
        sect = pie.sectors
        self.add(a, b)
        self.say("Two customers share one CPU. One of them paid for three quarters of the machine. "
                 "The other paid for one quarter.",
                 hop_bottom(a, apos - P3(0, 0.45), run_time=1.0), hop_bottom(b, bpos - P3(0, 0.45), run_time=1.0),
                 Succession(Wait(2.5), LaggedStart(*[Create(s) for s in sect], lag_ratio=0.5, run_time=1.5),
                            AnimationGroup(FadeIn(l75), FadeIn(l25))))

        # S01.3
        stu = Student("neutral").move_to(STU_DIALOGUE + DOWN * 0.1)
        prof = Professor("neutral").flip().move_to(PROF_DIALOGUE + DOWN * 0.1)
        self.add(stu, prof)
        stu.set_opacity(0)
        prof.set_opacity(0)
        self.say("Easy. Round robin, with a twist.", stu.animate.set_opacity(1).shift(UP * 0.1), run_time=0.8)
        self.play(stu.change("curious"), run_time=0.5)

        def chip_try(name, y_x, extra, ex_pos):
            c = sched_chip(name, 0.9, 0.46).move_to(P3(y_x, -3.0))
            return c

        chips = {n: sched_chip(n, 0.95, 0.46).move_to(P3(x, -3.0)) for n, x in (("RR", -1.2), ("SJF", 0.0), ("MLFQ", 1.25))}
        for c in chips.values():
            self.add(c)
            c.set_opacity(0)

        # S01.4
        rr = chips["RR"]
        half = TargetPie((0.5, 0.5), radius=0.28, label=None).move_to(P3(0.2, -1.4))
        neq = MathTex(r"\neq", color=KERNEL_COLOR, font_size=48).next_to(half, RIGHT, buff=0.15)
        up_pt = P3(0.0, -1.0)
        self.say("Round robin gives everyone the same share.",
                 prof.animate.set_opacity(1),
                 Succession(rr.animate(run_time=0.4).set_opacity(1),
                            rr.animate(run_time=0.8).move_to(up_pt),
                            FadeIn(half, scale=0.5), FadeIn(neq, scale=1.4),
                            Wait(0.3),
                            AnimationGroup(FadeOut(half), FadeOut(neq), rr.animate.move_to(P3(-1.2, -3.0)).rotate(0.0))))
        self.play(prof.change("thinking"), run_time=0.5)

        # S01.5
        sjf = chips["SJF"]
        q = question_mark(0.5)
        self.say("Shortest-job-first promises nothing about shares.",
                 Succession(sjf.animate(run_time=0.4).set_opacity(1), sjf.animate(run_time=0.8).move_to(up_pt),
                            FadeIn(q.next_to(sjf, UP, buff=0.05).move_to(up_pt + UP * 0.6), scale=0.4), Wait(0.5),
                            AnimationGroup(FadeOut(q), sjf.animate.move_to(P3(0.0, -3.0)))))

        # S01.6
        mlfq = chips["MLFQ"]
        fuzzy = Circle(radius=0.55).set_stroke(DIM, 2).set_fill(opacity=0).move_to(up_pt + UP * 0.9)
        cloud = bad_luck_cloud("guess", 1.0).scale(0.6).move_to(up_pt + RIGHT * 0.9 + UP * 0.5)
        self.say("And the multi-level feedback queue guesses from behavior and hopes for the best.",
                 Succession(mlfq.animate(run_time=0.4).set_opacity(1), mlfq.animate(run_time=0.8).move_to(up_pt + RIGHT * 0.2),
                            AnimationGroup(FadeIn(cloud), Create(fuzzy)),
                            Wobble_(fuzzy), Wait(0.3),
                            AnimationGroup(FadeOut(cloud), FadeOut(fuzzy), mlfq.animate.move_to(P3(1.25, -3.0)))))

        # S01.7
        names = {"RR": "turnaround", "SJF": "response", "MLFQ": "guess"}
        tags = VGroup(*[Text(names[n], font_size=18, color=DIM).next_to(chips[n], UP, buff=0.08) for n in chips])
        self.say("All of them chase a number: turnaround time, response time.",
                 FadeIn(tags),
                 Succession(*[Indicate(chips[n], color=CPU_COLOR, scale_factor=1.2, run_time=0.9) for n in chips]))

        # S01.8
        self.say("None lets you say, on purpose, \"you get seventy-five percent.\"",
                 pie.pulse(), *[chips[n].animate.set_opacity(0.3) for n in chips],
                 tags.animate.set_opacity(0.3))

        # S01.9
        self.say("So what would a scheduler that keeps that promise even look like?", stu.change("confused"))

        # S01.10
        drum = RaffleDrum(1.4).move_to(P3(8.0, -0.6))
        self.add(drum)
        self.say("Surprisingly, like a raffle.", prof.change("happy"),
                 drum.animate(run_time=1.6).move_to(P3(5.6, -0.6)),
                 Succession(Wait(0.4), drum.spin(1, run_time=2.0)))
        self.play(drum.spin(1, run_time=1.5))


def Wobble_(m):
    return Succession(m.animate(run_time=0.25).shift(RIGHT * 0.08), m.animate(run_time=0.25).shift(LEFT * 0.16),
                      m.animate(run_time=0.25).shift(RIGHT * 0.08))
