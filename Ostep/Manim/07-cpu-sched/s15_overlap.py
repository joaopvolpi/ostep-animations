import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


class S15Overlap(Ep07Scene):
    def construct(self):
        self.world(opened=(0, 1, 2, 3), term="blocked", stu="curious", prof="happy", chars=False)
        self.stu = student_corner("curious")
        stu = self.stu
        self.add(stu)
        strip = self.strip
        tl = make_lanes()
        set_lane_blocks(tl, NAIVE_CPU, NAIVE_DISK)
        disk = Disk(0.7, 0.6).move_to(P3(-5.75, 0.2))
        a = proc("A", "blocked", scale=0.5)
        bottom_to(a, P3(-5.55, 1.12))
        barA = lane_bursts(2.3)
        gaps = VGroup(*[Text("I/O", font_size=14, color=COL["A"]).move_to(barA[k]) for k in (1, 3, 5, 7)])
        barB = sj_bar(5, CELL14, COL["B"], "50 ms", LANE_X[0], 1.9)
        la = Text("A", font_size=22, color=COL["A"]).next_to(barA, LEFT, buff=0.12)
        lb = Text("B", font_size=22, color=COL["B"]).next_to(barB, LEFT, buff=0.12)
        poor = Text("Poor use of resources", font_size=34, color=KERNEL_COLOR).move_to(P3(0, -1.3))
        idle = Text("CPU idle: 40 ms", font_size=28, color=CPU_COLOR).move_to(P3(0, -2.0))
        comp = Computer("sleeping").scale(0.6).move_to(PROF_CORNER)
        self.add(tl, disk, a, barA, gaps, barB, la, lb, poor, idle, comp)

        # S15.1
        queue = Queue(label=None, center=(-0.6, 2.05), slots=6, spacing=0.75)
        items = [Rectangle(width=0.5, height=0.3).set_fill(COL["A"], 1).set_stroke(TEXT, 1) for _ in range(5)]
        bq = Rectangle(width=0.5, height=0.3).set_fill(COL["B"], 1).set_stroke(TEXT, 1)
        queue.place(*items, bq)
        alab = Text("A bursts", font_size=18, color=COL["A"]).next_to(queue, DOWN, buff=0.1).shift(LEFT * 1.6)
        blab = Text("B", font_size=18, color=COL["B"]).next_to(bq, DOWN, buff=0.2)
        self.say("The trick: treat each ten-millisecond burst of A as its own little job.",
                 tl.unfill_ticks(range(1, 15), run_time=1.0), FadeOut(VGroup(poor, idle, barA, gaps, barB, la, lb, a)),
                 comp.change("idle"),
                 after(1.2, AnimationGroup(FadeIn(queue), *[FadeIn(i, shift=DOWN * 0.2) for i in items],
                                                      FadeIn(bq), FadeIn(alab), FadeIn(blab))))
        tl.purge()

        # S15.2
        spot = Spotlight(height=0.7, spread=0.25)
        spot.move_beam_to(queue.slot_point(0))
        self.say("When the system starts, the shortest job is A's first burst. It runs.",
                 FadeIn(spot), after(1.5, AnimationGroup(
                     tl.fill("CPU", 1, "running", color=COL["A"]), items[0].animate.set_opacity(0.25))))

        # S15.3
        self.say("Then A goes to the disk and B takes over.",
                 tl.fill("Disk", 2, "ready", color=COL["A"]), tl.fill("CPU", 2, "running", color=COL["B"]),
                 spot.animate.move_beam_to(queue.slot_point(5)))

        # S15.4
        arr = tl.arrival_marker("CPU", 2, "A ready", color=COL["A"])
        pause = PauseGlyph(0.22).move_to(tl.block_at[(0, 2)].get_center())
        self.say("When A's I/O completes, a new short job appears. It preempts B, runs ten milliseconds, then B returns.",
                 FadeIn(arr, shift=DOWN * 0.2),
                 after(1.0, spot.animate(run_time=0.7).move_beam_to(queue.slot_point(1)), FadeIn(pause),
                            AnimationGroup(tl.fill("CPU", 3, "running", color=COL["A"]), items[1].animate.set_opacity(0.25)),
                            AnimationGroup(tl.fill("Disk", 4, "ready", color=COL["A"]), tl.fill("CPU", 4, "running", color=COL["B"]),
                                           FadeOut(pause), FadeOut(arr))))

        # S15.5
        with self.narrate("Back and forth."):
            for t in range(5, 11):
                an = [tl.fill("CPU", t, "running", color=COL["A"] if t % 2 else COL["B"], run_time=0.25)]
                if t in OVERLAP_DISK:
                    an.append(tl.fill("Disk", t, "ready", color=COL["A"], run_time=0.25))
                if t % 2:
                    an.append(items[t // 2].animate.set_opacity(0.25))
                self.play(*an, run_time=0.25)
            self.play(FadeOut(VGroup(spot, queue, *items, bq, alab, blab)), run_time=0.4)

        # S15.6
        bands = VGroup(*[Rectangle(width=CELL14, height=1.0).set_fill(COL["A"], 0.18).set_stroke(COL["A"], 1.5)
                         .move_to(P3(LANE_X[0] + (k - 0.5) * CELL14, 0.5)) for k in OVERLAP_DISK])
        self.say("This is overlap: while A waits on the disk, B uses the CPU.",
                 self.term("overlap", hold=0.8), after(1.5, LaggedStart(*[FadeIn(b) for b in bands],
                                                                                lag_ratio=0.5, run_time=2.0)),
                 comp.change("busy"))

        # S15.7
        ghost14 = tl.completion_marker(None, 14, "140", color=DIM)
        ghost14.set_opacity(0.6)
        m100 = tl.completion_marker(None, 10, "100", color=TEXT)
        saved = Text("−40 ms", font_size=34, color=PERS, weight=BOLD).move_to(P3(3.5, -1.75))
        link = Arrow(tl.tick_x(14) * RIGHT + DOWN * 1.15, tl.tick_x(10) * RIGHT + DOWN * 1.15, buff=0, color=PERS, stroke_width=4)
        self.say("Everyone finishes sooner than if we ran A, waited, ran A, waited, and only then ran B.",
                 FadeIn(ghost14, shift=DOWN * 0.3), after(2.5, FadeIn(m100, shift=DOWN * 0.3)),
                 after(4.0, AnimationGroup(Create(link), FadeIn(saved))))

        # S15.8
        t1 = Text("interactive", font_size=20, color=COL["A"]).move_to(P3(-3.3, 1.45))
        t2 = Text("CPU hog", font_size=20, color=COL["B"]).move_to(P3(-1.9, 1.45))
        self.say("So interactive jobs run often, and the CPU hogs fill the gaps!",
                 stu.change("excited"), FadeIn(t1), FadeIn(t2))
        self.play(FadeOut(VGroup(t1, t2)), run_time=0.3)

        # S15.9 (tip)
        tip = TipCard("start the operation, then switch to other work", title="TIP: Overlap enables higher utilization",
                      width=5.6, height=1.5, font_size=22).move_to(P3(2.9, 2.2))
        self.play(tip.slide_in(RIGHT, run_time=0.5), run_time=0.5)
        self.wait(0.8)
        prof = prof_corner("happy")
        self.play(tip.slide_out(RIGHT, run_time=0.5), FadeOut(VGroup(bands, link, saved)),
                  FadeOut(comp), FadeIn(prof), run_time=0.6)
