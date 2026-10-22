import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


class S14DiskWait(Ep07Scene):
    def construct(self):
        self.world(opened=(0, 1, 2), term="trade-off", stu="confused", prof="proud")
        stu, prof, strip = self.stu, self.prof, self.strip
        tl = make_lanes()
        disk = Disk(0.7, 0.6).move_to(P3(-5.75, 0.2))

        # S14.1
        self.say("Now the fourth assumption. Real jobs do I/O.",
                 strip.locks[3].open(), FadeOut(prof), Succession(Wait(1.0), AnimationGroup(
                     Create(tl.grid), FadeIn(tl.row_labels), FadeIn(tl.tick_labels), FadeIn(disk))))

        # S14.2
        a = proc("A", scale=0.5)
        bottom_to(a, P3(-2.5, 1.12))
        tag = ep_tag("state · Ep. 04", font_size=18).move_to(P3(5.0, 3.15))
        self.play(FadeIn(a), run_time=0.4)
        self.say("When a job asks the disk for data, it's blocked, so the scheduler has to run someone else.",
                 self.term("blocked", hold=0.8), FadeIn(tag),
                 Succession(Wait(3.8), hop_bottom(a, P3(-5.55, 1.12), run_time=0.9)))
        self.play(a.change("blocked"), run_time=0.5)

        # S14.3
        spot = Spotlight(height=0.8, spread=0.3)
        spot.move_beam_to(P3(3.5, 1.2))
        q = question_mark(0.4).next_to(spot.lamp, RIGHT, buff=0.15)
        self.say("And when the I/O completes, there's another decision.",
                 FadeIn(spot), FadeIn(q), Succession(Wait(1.0), q.animate(run_time=0.6).shift(UP * 0.12),
                                                     q.animate(run_time=0.6).shift(DOWN * 0.12)))

        # S14.4
        barA = sj_bar(5, CELL14, COL["A"], "50 ms", LANE_X[0], 2.6)
        barB = sj_bar(5, CELL14, COL["B"], "50 ms", LANE_X[0], 2.15)
        la, lb = Text("A", font_size=22, color=COL["A"]).next_to(barA, LEFT, buff=0.12), \
            Text("B", font_size=22, color=COL["B"]).next_to(barB, LEFT, buff=0.12)
        self.say("Two jobs, A and B, each need fifty milliseconds of CPU.",
                 FadeIn(barA, shift=RIGHT * 0.3), FadeIn(barB, shift=RIGHT * 0.3), FadeIn(la), FadeIn(lb))

        # S14.5
        bursts = lane_bursts(2.6)
        self.say("But A computes for ten, then does a ten-millisecond I/O, over and over.",
                 ReplacementTransform(barA, bursts))
        gaps = VGroup(*[Text("I/O", font_size=14, color=COL["A"]).move_to(bursts[k]) for k in (1, 3, 5, 7)])
        self.play(FadeIn(gaps), run_time=0.4)

        # S14.6
        self.say("B just computes for fifty.", Indicate(barB, scale_factor=1.08))

        # S14.7
        self.say("Using STCF, what should the scheduler do?", stu.change("curious"),
                 Succession(spot.animate(run_time=0.9).move_beam_to(P3(-3.0, 1.2)),
                            spot.animate(run_time=0.9).move_beam_to(P3(-1.5, 1.2)),
                            spot.animate(run_time=0.9).move_beam_to(P3(3.5, 1.2))))

        # S14.8 (what-if)
        banner = VGroup(RoundedRectangle(width=1.6, height=0.5, corner_radius=0.1).set_fill(CARD_FILL, 1).set_stroke(KERNEL_COLOR, 2.5),
                        Text("naive", font_size=26, color=KERNEL_COLOR)).move_to(P3(5.4, 3.0))
        banner[1].move_to(banner[0])
        comp = Computer("sleeping").scale(0.6).move_to(PROF_CORNER)
        with self.narrate("", min_time=0.0):
            self.play(FadeIn(banner), FadeIn(comp), FadeOut(VGroup(spot, q)), run_time=0.6)
            for t in range(1, 15):
                j = NAIVE_CPU[t]
                an = [tl.fill("CPU", t, "idle", run_time=0.3) if j == "." else
                      tl.fill("CPU", t, "running", color=COL[j], run_time=0.3)]
                if t in NAIVE_DISK:
                    an.append(tl.fill("Disk", t, "ready", color=COL["A"], run_time=0.3))
                self.play(*an, run_time=0.3)

        # S14.9
        poor = Text("Poor use of resources", font_size=34, color=KERNEL_COLOR).move_to(P3(0, -1.3))
        idle = Text("CPU idle: 40 ms", font_size=28, color=CPU_COLOR).move_to(P3(0, -2.0))
        self.say("Poor use of resources.", Write(poor), FadeIn(idle, shift=UP * 0.2))
        self.beat(1.0)
