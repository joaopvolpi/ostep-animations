import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


class S03Ladder(Ep08Scene):
    def construct(self):
        # starts with S02's end state
        self.build(lanes=None, cpu=False, rules="skeleton", stu="curious", prof="neutral")
        strip = crux_strip()
        self.add(strip)
        lad = MLFQLadder(levels=8)
        cpu = CPU(size=1.2).move_to(CPU_AT)
        self.ladder, self.cpu = lad, cpu
        s = lad.job_scale
        ready = Queue(label="Ready", center=(-2.6, -1.9), slots=4, spacing=0.8, font_size=18)
        jobs = {n: job(n, s) for n in "ABCD"}
        ready.place(*jobs.values())
        self.play(FadeOut(strip), run_time=0.6)

        # S03.1
        self.say("MLFQ doesn't have one ready queue.", FadeIn(ready), *[FadeIn(j, shift=DOWN * 0.2) for j in jobs.values()])

        # S03.2
        lane_parts = [m for lv in lad.ids for m in (lad.lanes[lv], lad.labels[lv])]
        self.say("It has several, each at a different priority level.",
                 FadeOut(VGroup(ready.tray, ready.label)),
                 LaggedStart(*[FadeIn(m, shift=RIGHT * 0.2) for m in lane_parts], lag_ratio=0.08), self.note("priority level"))

        # S03.3
        hops = []
        for n, lv in (("A", 8), ("B", 8), ("C", 4), ("D", 1)):
            hops.append(lad.promote(jobs[n], lv, run_time=0.7))
        self.say("A job that's ready to run sits on exactly one of them…", Succession(*hops))

        # S03.4
        spot = Spotlight(height=0.7, spread=0.3)
        spot.move_beam_to(lad.lane_point(1, 3))
        self.add(spot)
        link = CurvedArrow(P3(0.3, 2.3), P3(1.35, 1.35), angle=-0.6, color=CPU_COLOR, stroke_width=5)
        self.say("…and the scheduler picks from the highest queue that has anything in it.",
                 FadeIn(spot), Succession(Wait(0.4), spot.animate(run_time=1.6).move_beam_to(lad.lane_point(8, 3))),
                 lad.serve(8), Succession(Wait(1.8), GrowFromCenter(cpu), Create(link)))

        # S03.5
        self.say("Picture a ladder. In the book's first figure there are eight queues.",
                 FadeIn(lad.arrows), Indicate(lad.arrows.up, color=CPU_COLOR), Indicate(lad.arrows.down, color=CPU_COLOR))

        # S03.6
        self.say("Jobs A and B sit at the top, C in the middle, D at the bottom.",
                 Succession(Indicate(VGroup(jobs["A"], jobs["B"]), scale_factor=1.5, run_time=0.9),
                            Indicate(jobs["C"], scale_factor=1.5, run_time=0.8), Indicate(jobs["D"], scale_factor=1.5, run_time=0.8)))

        # S03.7
        hist = history_clock(0.3).move_to(P3(0.8, -0.45))
        ltxt = label("learn from history", 20, TEXT).move_to(P3(2.1, -0.95))
        self.say("And the big idea: the scheduler will learn from history.",
                 self.stu.change("curious"), FadeIn(hist), Succession(Wait(0.8), Write(ltxt)))

        # S03.8
        blocks = VGroup(*[Rectangle(width=0.16, height=0.22).set_fill(COL["A"], 1).set_stroke(TEXT, 1) for _ in range(4)]).arrange(RIGHT, buff=0.03)
        blocks.move_to(P3(1.7, -0.45))
        nxt = VGroup(Arrow(ORIGIN, RIGHT * 0.35, buff=0, color=TEXT, stroke_width=3, tip_length=0.12), label("next?", 18, DIM)).arrange(RIGHT, buff=0.05)
        nxt.next_to(blocks, RIGHT, buff=0.08)
        self.say("What a job did a moment ago tells us what it will probably do next.",
                 LaggedStart(*[FadeIn(b, shift=RIGHT * 0.3) for b in blocks], lag_ratio=0.25), Succession(Wait(1.2), FadeIn(nxt)))

        # S03.9
        card = tip_history_card()
        self.say("Branch predictors and caches do this too.", card.slide_in(DOWN), self.prof.change("explaining"))

        # S03.10
        bad = x_mark(0.3).move_to(card.get_right() + LEFT * 0.4 + UP * 0.35)
        self.say("But careful: when the past is a bad guide, such a system can decide worse than one with no knowledge at all.",
                 self.prof.change("worried"), Succession(Wait(1.0), FadeIn(bad, scale=1.5)), self.stu.change("neutral"))
        self.beat(1.0)
