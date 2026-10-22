import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403

CARD_X = -1.2
CARD_YS = [1.8, 0.9, 0.0, -0.9, -1.8]
CARD_TEXT = ["1 · Every job runs the same time", "2 · All jobs arrive together", "3 · Run to completion",
             "4 · CPU only, no I/O", "5 · Run-time is known"]
BAR_Y = [1.15, 0.6, 0.05]
BAR_X0 = [3.0, 3.6, 3.3]


class S03FiveLies(Ep07Scene):
    def construct(self):
        self.world(stu="neutral", prof="happy", strip=False)
        stu, prof = self.stu, self.prof
        strip = make_strip()
        crux = crux_strip_mobs()
        self.add(crux)

        cards = VGroup()
        locks = []
        for y, t in zip(CARD_YS, CARD_TEXT):
            fr = RoundedRectangle(width=6.4, height=0.7, corner_radius=0.12).set_fill(CARD_FILL, 1).set_stroke(DIM, 2.5)
            fr.move_to(P3(CARD_X, y))
            tx = Text(t, font_size=28, color=TEXT).move_to(fr.get_left() + RIGHT * 0.75, aligned_edge=LEFT)
            lk = Padlock(0.3).move_to(fr.get_left() + RIGHT * 0.4)
            cards.add(VGroup(fr, tx, lk))
            locks.append(lk)
        self.play(FadeOut(crux), run_time=0.4)

        # S03.1
        cluster = VGroup(*[proc(n, scale=0.5) for n in "ABC"]).arrange(RIGHT, buff=0.15).move_to(P3(4.4, 0.5))
        wl = Text("workload", font_size=26, color=DIM).next_to(cluster, UP, buff=0.2)
        self.say("To think clearly, let's first simplify. The processes running in the system are the workload…",
                 Succession(Wait(3.0), self.term("workload", hold=0.5)), FadeIn(cluster, shift=LEFT * 0.4), FadeIn(wl))

        # S03.2
        bars = VGroup(*[sj_bar(l, 1.0, COL[n], n, x, y) for n, l, x, y in
                        zip("ABC", (2.4, 1.0, 1.7), BAR_X0, BAR_Y)])
        self.say("…and we'll call each one a job.",
                 self.term("job", hold=0.4, size=48),
                 Succession(Wait(1.0), AnimationGroup(*[ReplacementTransform(c, b) for c, b in zip(cluster, bars)],
                                                      FadeOut(wl))))

        # S03.3
        self.say("We'll assume five things about the workload.",
                 LaggedStart(*[Create(c[0]) for c in cards], lag_ratio=0.4, run_time=2.0))

        # S03.4
        eq = VGroup(*[sj_bar(1.6, 1.0, COL[n], n, x, y) for n, x, y in zip("ABC", BAR_X0, BAR_Y)])
        self.say("One: every job runs for the same amount of time.",
                 Write(cards[0][1]), Succession(Wait(0.8), GrowFromCenter(locks[0])),
                 Succession(Wait(1.2), AnimationGroup(*[Transform(b, e) for b, e in zip(bars, eq)]),
                            AnimationGroup(*[Indicate(b, scale_factor=1.1) for b in bars])))

        # S03.5
        line = DashedLine(P3(3.2, 1.5), P3(3.2, -0.3), dash_length=0.12).set_stroke(DIM, 2)
        aligned = VGroup(*[sj_bar(1.6, 1.0, COL[n], n, 3.2, y) for n, y in zip("ABC", BAR_Y)])
        self.say("Two: all jobs arrive at the same moment.",
                 Write(cards[1][1]), Succession(Wait(0.8), GrowFromCenter(locks[1])),
                 Succession(Wait(1.0), Create(line), AnimationGroup(*[Transform(b, e) for b, e in zip(bars, aligned)])))

        # S03.6
        self.say("Three: once started, a job runs to completion.",
                 Write(cards[2][1]), Succession(Wait(0.8), GrowFromCenter(locks[2])))

        # S03.7
        disk = Disk(0.8, 0.65).move_to(P3(4.0, -1.1))
        cross = x_mark(0.5).move_to(disk)
        self.say("Four: jobs only use the CPU. They never do I/O.",
                 Write(cards[3][1]), Succession(Wait(0.8), GrowFromCenter(locks[3])),
                 Succession(Wait(1.5), FadeIn(disk, scale=0.6), Create(cross)))

        # S03.8
        ball = CrystalBall(0.4, color=DIM).move_to(P3(5.5, -1.3))
        self.say("Five: the run-time of each job is known in advance.",
                 Write(cards[4][1]), Succession(Wait(0.8), GrowFromCenter(locks[4])),
                 Succession(Wait(1.5), FadeIn(ball, scale=0.6)))

        # S03.9
        self.say("Known in advance? How would the OS ever know that?",
                 stu.change("confused"), locks[4].wobble(run_time=1.2))

        # S03.10
        tint = cards[4][0].copy().set_fill(KERNEL_COLOR, 0.25).set_stroke(KERNEL_COLOR, 3)
        self.say("It wouldn't. That's the least realistic one, and it makes our scheduler all-knowing.",
                 prof.change("explaining"), Transform(cards[4][0], tint), ball.glow_up(run_time=1.0))

        # S03.11
        nums = [strip.locks[i].num.copy() for i in range(5)]
        anims = []
        for i, card in enumerate(cards):
            anims.append(AnimationGroup(
                FadeOut(VGroup(card[0], card[1]), scale=0.2, target_position=card[2]),
                card[2].animate.scale(0.28 / 0.3).move_to(strip.locks[i].lock.get_center()),
                FadeIn(nums[i])))
        self.say("But these assumptions are scaffolding. We'll take them down, one at a time…",
                 LaggedStart(*anims, lag_ratio=0.15, run_time=3.0),
                 FadeOut(VGroup(bars, line, disk, cross, ball)))
        # swap the moved card locks for the real strip (identical look)
        self.remove(*locks, *nums)
        self.add(strip)
        self.strip = strip

        # S03.12
        tagt = Text("scheduling discipline", font_size=20, color=DIM).next_to(strip, RIGHT, buff=0.3)
        self.say("…until we have a fully-operational scheduling discipline. Like a Death Star, but for CPUs.",
                 prof.change("happy"), FadeIn(tagt))
        self.beat(0.8)
