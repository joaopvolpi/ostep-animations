import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


class S13Accounting(Ep08Scene):
    def construct(self):
        self.build(lanes=None, cpu=False, rules=("R1", "R2", "R3", "R4a", "R4b", "R5"), stu="neutral", prof="neutral",
                   term="voodoo constants")
        board = self.board

        # S13.1
        self.say("Now gaming.", board.glow("R4a", KERNEL_COLOR, 1.0), Succession(Wait(0.4), board.glow("R4b", KERNEL_COLOR, 1.0)))

        # S13.2 (close-up)
        B = job("B", 1.2, "running").move_to(P3(-1.6, 0.7))
        sh = put_shades(B, 1.0)
        g = AllotmentGauge(2.4, 1.0)
        g.attach_to(B)
        spot = P3(-1.6 + 2.2, 0.0)
        poof = puff(0.35)
        poof.move_to(g.get_center())
        self.say("The culprits are Rules four A and four B: the scheduler forgets how much CPU a job already used whenever it does I/O.",
                 FadeIn(B), FadeIn(sh), FadeIn(g))
        # shades follow B
        sh.add_updater(lambda m: m.move_to(B.get_center() + UP * 0.12 * B.get_height()))
        with self.narrate(""):
            self.play(g.drain(0.9, run_time=1.4))
            self.play(SetExpr(B, "blocked"), run_time=0.3)
            self.play(hop_to(B, P3(-1.6, 0.7), run_time=0.5))
            self.play(g.reset(0.5), FadeIn(poof, scale=1.6), run_time=0.6)
            self.play(FadeOut(poof), SetExpr(B, "running"), run_time=0.4)

        # S13.3
        pad = Notepad("ledger", lines=3, width=2.4, font_size=18)
        lines = [pad.line_text(i, t) for i, t in enumerate(("3 ms", "3 ms", "4 ms"))]
        d = P3(2.0, 0.6) - pad.get_center()
        pad.shift(d)
        for l in lines:
            l.shift(d)
        self.say("The fix is better accounting.", self.note("accounting"), FadeIn(pad, shift=LEFT * 0.4))

        # S13.4
        seq = []
        for amt, w in ((0.3, lines[0]), (0.3, lines[1]), (0.4, lines[2])):
            seq.append(AnimationGroup(g.chunk(amt, run_time=0.8), Write(w, run_time=0.8)))
        self.say("At each level, the scheduler keeps track of the allotment used, even across I/Os.", Succession(*seq))

        # S13.5
        qlab = label("Q2", 28, TEXT).next_to(B, RIGHT, buff=0.3)
        qlab1 = label("Q1", 28, TEXT).move_to(qlab.get_center() + DOWN * 0.8)
        self.say("Once it's spent, the job is demoted.", FadeIn(qlab), Succession(Wait(0.8), AnimationGroup(Transform(qlab, qlab1), B.animate.shift(DOWN * 0.5))))
        self.play(FadeOut(VGroup(B, sh, g, pad, qlab, *lines)), run_time=0.5)

        # S13.6
        one = Rectangle(width=2.6, height=0.35).set_fill(COL["B"], 1).set_stroke(TEXT, 1).move_to(P3(-2.0, 1.0))
        tens = VGroup(*[Rectangle(width=0.26, height=0.35).set_fill(COL["B"], 1).set_stroke(TEXT, 1) for _ in range(10)]).arrange(RIGHT, buff=0.0)
        tens.move_to(P3(-2.0, 0.2))
        eq = VGroup(MathTex("=", color=TEXT), label("10 ms used", 22, TEXT)).arrange(RIGHT, buff=0.15).next_to(one, RIGHT, buff=0.25)
        eq2 = VGroup(MathTex("=", color=TEXT), label("10 ms used", 22, TEXT)).arrange(RIGHT, buff=0.15).next_to(tens, RIGHT, buff=0.25)
        self.say("One long burst or many small ones: it doesn't matter.",
                 GrowFromEdge(one, LEFT), LaggedStart(*[FadeIn(t, shift=UP * 0.1) for t in tens], lag_ratio=0.1),
                 Succession(Wait(1.2), FadeIn(eq), FadeIn(eq2)))
        self.play(FadeOut(VGroup(one, tens, eq, eq2)), run_time=0.4)

        # S13.7
        self.say("So we merge four A and four B into one rule: once a job uses up its allotment at a given level, regardless of how many times it has given up the CPU, its priority is reduced.",
                 board.merge(["R4a", "R4b"], "R4", RULES["R4"]), Succession(Wait(2.0), board.glow("R4", GREEN_OK, 1.2)))

        # S13.8
        tl_l, tl_r = make_half(LEFT_X, 30), make_half(RIGHT_X, 30)
        set_cells(tl_l, FIG82[:2]); tl_l.set_span("Q0", 2, 10, "running", COL["A"])
        set_cells(tl_r, FIG82[:2]); tl_r.set_span("Q0", 2, 10, "running", COL["A"])
        ttl = label("old rules", 22, DIM).move_to(P3(-3.4, -0.45))
        ttr = label("Rule 4", 22, DIM).move_to(P3(1.0, -0.45))
        U = 0.3
        left = []
        for k, b in enumerate(range(10, 26)):
            left.append(tl_l.fill_span("Q2", b, b + U, "running", COL["B"], run_time=0.12))
            if k % 4 == 3:
                left.append(tl_l.fill_span("Q0", b + U, b + 1, "running", COL["A"], run_time=0.1))
        self.say("On the left, the gamer B issues an I/O before every allotment ends, stays on top, and dominates the CPU.",
                 FadeIn(tl_l), FadeIn(tl_r), FadeIn(ttl), FadeIn(ttr), Succession(Wait(1.5), *left))

        # S13.9
        right = []
        for b in (10, 11, 12):
            right.append(tl_r.fill_span("Q2", b, b + U, "running", COL["B"], run_time=0.12))
        for b in (13, 14, 15):
            right.append(tl_r.fill_span("Q1", b, b + U, "running", COL["B"], run_time=0.12))
        a0 = 10.0
        spans = [("A", 16, 18), ("B", 18, 19), ("A", 19, 21), ("B", 21, 22), ("A", 22, 24), ("B", 24, 25), ("A", 25, 30)]
        for n, s0, s1 in spans:
            right.append(tl_r.fill_span("Q0", s0, s1, "running", COL[n], run_time=0.2))
        self.say("On the right, with the new rule, it slowly sinks.", Succession(*right))

        # S13.10
        ok = tick_mark(0.4).move_to(P3(2.0, -0.45))
        bad = x_mark(0.35).move_to(P3(-2.4, -0.45))
        self.say("No unfair share.", self.stu.change("excited"), FadeIn(ok, scale=1.4), FadeIn(bad, scale=1.4))
        self.beat(1.0)
