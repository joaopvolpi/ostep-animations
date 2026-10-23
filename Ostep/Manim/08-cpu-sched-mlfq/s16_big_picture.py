import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


class S16BigPicture(Ep08Scene):
    def construct(self):
        self.build(lanes=3, cpu=True, ticks=20, board=False, stu="neutral", prof="explaining", term="advice")
        lad, cpu, tl = self.ladder, self.cpu, self.tl
        board = RuleBoard()
        board.place_now([(t, RULES[t]) for t in ("R1", "R2", "R3", "R4", "R5")])
        B = self.put("B", 2, 0)
        A = self.put("A", 1, 0)
        C = job("C", lad.job_scale)
        spot = Spotlight(height=0.6, spread=0.3)
        spot.move_beam_to(lad.lane_point(2, 3))

        # S16.1
        self.say("Let's put it all together. Here are the five rules, as refined.", FadeIn(board, shift=LEFT * 0.4), FadeIn(spot))
        self.beat(0.5)

        # S16.2
        self.say("One: higher priority runs.", board.glow("R1"), self.to_cpu(B), lad.serve(2))
        # S16.3
        lad.register(C, 2, 1)
        C.move_to(lad.lane_point(2, 1))
        self.say("Two: equal priority takes turns, round robin, using the time slice of that queue.",
                 board.glow("R2"), FadeIn(C), Succession(self.to_lane(B, 2, 0, "ready"), self.to_cpu(C), self.to_lane(C, 2, 1, "ready"), self.to_cpu(B)))
        # S16.4
        D = job("D", lad.job_scale)
        lad.register(D, 2, 2)
        D.move_to(lad.lane_point(2, 2))
        self.say("Three: new jobs start at the top.", board.glow("R3"), FadeIn(D, shift=DOWN * 0.8), self.to_lane(B, 2, 0, "ready"))
        # S16.5
        g = self.attach_gauge(A, 1.0, 1.0)
        self.say("Four: a job that uses up its allotment at a level moves down, however many times it gave up the CPU.",
                 board.glow("R4", run_time=1.5),
                 Succession(self.to_cpu(A), FadeIn(g), g.chunk(0.3, 0.5), g.chunk(0.3, 0.5), g.chunk(0.4, 0.5), self.to_lane(A, 0, 0, "ready"), g.reset(0.3)))
        self.play(FadeOut(g), run_time=0.3)
        # S16.6
        sw = stopwatch_icon(0.3).move_to(P3(0.85, 0.0))
        self.say("Five: every so often, everybody goes back to the top.",
                 board.glow("R5"), FadeIn(sw), Rotate(sw.hand, angle=-TAU, about_point=sw[0].get_center(), run_time=1.5),
                 Succession(Wait(1.6), lad.boost_all()))
        self.play(FadeOut(sw), run_time=0.3)

        # S16.7
        br = Brace(VGroup(lad.lanes[2], lad.lanes[0]), RIGHT, buff=0.08).set_color(VIRT)
        lev = label("levels", 20, VIRT).next_to(br, RIGHT, buff=0.05)
        loop = CurvedArrow(cpu.get_bottom() + DOWN * 0.1, lad.right_point(1) + RIGHT * 0.05 + DOWN * 0.3, angle=-1.2, color=VIRT, stroke_width=5)
        self.say("That's why it's called a Multi-Level Feedback Queue.", self.note("feedback"), FadeIn(br), FadeIn(lev), Succession(Wait(1.5), Create(loop)))
        # S16.8
        fb = label("feedback", 22, VIRT).next_to(loop, DOWN, buff=0.1).shift(LEFT * 0.4)
        hist = history_clock(0.28).move_to(P3(1.1, -0.65))
        self.say("It has multiple levels of queues, and it uses feedback to decide a job's priority. History is its guide.",
                 FadeIn(fb), Succession(Wait(3.0), FadeIn(hist)))
        # S16.9
        self.say("It doesn't demand to know a job in advance. It watches.",
                 Succession(spot.animate(run_time=0.6).move_beam_to(lad.lane_point(2, 0)), spot.animate(run_time=0.6).move_beam_to(lad.lane_point(2, 4)),
                            spot.animate(run_time=0.6).move_beam_to(lad.lane_point(2, 1))), FadeOut(VGroup(br, lev, loop, fb, hist)))
        # S16.10
        ck1, ck2 = tick_mark(0.25).next_to(B, RIGHT, buff=0.05), tick_mark(0.25).next_to(C, RIGHT, buff=0.05)
        fills = [cell_run(tl, "Q2", 1, "B", 0.25), cell_run(tl, "Q2", 2, "C", 0.25), cell_run(tl, "Q1", 3, "A", 0.25),
                 cell_run(tl, "Q0", 4, "A", 0.25), cell_run(tl, "Q0", 5, "A", 0.25), cell_run(tl, "Q2", 11, "A", 0.25), cell_run(tl, "Q2", 12, "A", 0.25)]
        self.say("Short jobs get excellent response, close to SJF or STCF, and long jobs still make fair progress.",
                 Succession(*fills), Succession(Wait(0.6), FadeIn(ck1, scale=1.4), FadeIn(ck2, scale=1.4)))
        # S16.11
        tags = [tag_chip("BSD UNIX", TEXT, 20).move_to(P3(0.9, 2.3)), tag_chip("Solaris", TEXT, 20).move_to(P3(2.45, 2.3)),
                tag_chip("Windows NT", TEXT, 20).move_to(P3(1.7, -0.25))]
        self.say("BSD UNIX derivatives, Solaris, and Windows NT and its successors all use a form of MLFQ as their base scheduler.",
                 LaggedStart(*[GrowFromCenter(t) for t in tags], lag_ratio=0.5), self.prof.change("proud"))
        self.beat(1.5)
