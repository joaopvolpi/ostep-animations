import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


class S10HowFair(Ep09Scene):
    def construct(self):
        self.world(stu="excited", prof="happy")
        stu, prof = self.stu, self.prof

        def make_tl():
            return Timeline(["A", "B"], ticks=20, colors=[COL["A"], COL["B"]], x_range=(-4.0, 4.0), top=1.5,
                            row_height=0.36, row_step=0.55, tick_labels=False, label_font=22)

        tl = make_tl()
        sa = TicketStack(100, COL["A"], scale=0.8).move_to(P3(5.3, 1.6))
        sb = TicketStack(100, COL["B"], scale=0.8).move_to(P3(5.3, 0.9))

        # S10.1
        self.say("Let's measure that fairness. Two jobs, same length, a hundred tickets each.",
                 FadeIn(tl), FadeIn(sa), FadeIn(sb))

        # S10.2
        endline = DashedLine(P3(tl.tick_x(20), 1.9), P3(tl.tick_x(20), 0.9), color=TEXT, dash_length=0.08)
        self.say("Ideally they'd finish at the same time.",
                 Succession(tl.fill_span("A", 0, 20, "running", run_time=1.2) if False else Wait(0.1)),
                 AnimationGroup(tl.fill_span("A", 0, 20, "running", run_time=1.6), tl.fill_span("B", 0, 20, "running", run_time=1.6)),
                 Create(endline))

        # S10.3
        eq = MathTex(r"F=\frac{T_1}{T_2}", font_size=44, color=TEXT).move_to(P3(0, 2.1))
        self.say("The book defines a fairness metric: the time the first job finishes, divided by the time the second finishes.",
                 self.term("fairness metric"), Write(eq))

        # S10.4
        eq2 = MathTex(r"F=\frac{10}{20}=0.5", font_size=44, color=TEXT).move_to(eq)
        m1 = DashedLine(P3(tl.tick_x(10), 1.9), P3(tl.tick_x(10), 1.1), color=COL["A"], dash_length=0.08)
        self.play(tl.clear_blocks(0.6), FadeOut(endline), run_time=0.6)
        tl.purge()
        self.say("Ten and twenty give zero point five.",
                 tl.fill_span("A", 0, 10, "running", run_time=1.0), tl.fill_span("B", 0, 20, "running", run_time=1.6),
                 Succession(Wait(1.0), Create(m1), Transform(eq, eq2)))

        # S10.5
        eq3 = MathTex(r"F=1", font_size=44, color=CPU_COLOR).move_to(P3(0, 2.1))
        box = SurroundingRectangle(eq3, color=CPU_COLOR, buff=0.15)
        self.play(tl.clear_blocks(0.6), FadeOut(m1), run_time=0.6)
        tl.purge()
        self.say("Finishing together gives one: perfectly fair.",
                 tl.fill_span("A", 0, 20, "running", run_time=1.2), tl.fill_span("B", 0, 20, "running", run_time=1.2),
                 Succession(Wait(1.0), Transform(eq, eq3), Create(box)))

        # S10.6
        fp = FairnessPlot(6.5, 2.2, at=(-0.4, -1.1))
        ideal = fp.ideal_line()
        self.say("Over thirty trials, with jobs from one to a thousand time slices long, the pattern is clear.",
                 FadeOut(VGroup(tl, eq, box, sa, sb)),
                 Succession(Wait(0.6), AnimationGroup(Create(fp.axes), FadeIn(fp.labels)), Create(ideal)))

        # S10.7
        curve = fp.curve()
        d1 = Dot(fp.point(1, 0.5), radius=0.08, color=COL["B"])
        d2 = Dot(fp.point(1000, 1.0), radius=0.08, color=COL["B"])
        l1 = Text("short jobs: unfair", font_size=20, color=KERNEL_COLOR).move_to(fp.axes.c2p(0.2, 0.15), aligned_edge=LEFT)
        l2 = Text("long jobs: fair", font_size=20, color=GREEN_OK).move_to(fp.axes.c2p(2.0, 0.55), aligned_edge=LEFT)
        self.say("Short jobs: poor fairness. Only long jobs let the lottery converge.",
                 Create(curve, run_time=3.0), FadeIn(d1), Succession(Wait(0.5), FadeIn(l1)),
                 Succession(Wait(3.0), AnimationGroup(FadeIn(d2), FadeIn(l2))))

        # S10.8
        q = VGroup(card_rect(2.4, 1.1, DIM), question_mark(0.5, DIM),
                   Text("how many\ntickets?", font_size=20, color=TEXT, line_spacing=0.7))
        q[1].move_to(q[0].get_center() + LEFT * 0.7)
        q[2].move_to(q[0].get_center() + RIGHT * 0.45)
        q.move_to(P3(5.4, 1.6))
        self.say("So for short jobs it's kind of unfair. And how many tickets does each job get, anyway?",
                 stu.change("sad"), Succession(Wait(2.0), AnimationGroup(FadeIn(q, shift=LEFT * 0.3))))
        self.play(stu.change("curious"), run_time=0.6)

        # S10.9
        stamp = Text("OPEN", font_size=32, color=KERNEL_COLOR, weight=BOLD)
        stamp = VGroup(SurroundingRectangle(stamp, color=KERNEL_COLOR, buff=0.1), stamp).rotate(0.25).move_to(q.get_bottom() + DOWN * 0.45)
        stamp.set_opacity(0)
        self.say("The book is honest about that one. It's the ticket-assignment problem, and it's still open.",
                 prof.change("explaining"), self.term("ticket-assignment problem"),
                 Succession(Wait(3.0), stamp.animate(run_time=0.3).set_opacity(0.95).scale(1.0)))
        self.beat(0.8)
        self.play(FadeOut(VGroup(fp, curve, ideal, d1, d2, l1, l2, q, stamp)), run_time=0.8)
