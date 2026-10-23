import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common_more import *  # noqa: E402,F401,F403
from ostep_lib.props.ov_icons import money_meter  # noqa: E402

COLX = {"label": -3.2, "sqms": 0.8, "mqms": 3.8}
ROWS = [("simple", True, False), ("scales", False, True), ("keeps affinity", False, True), ("balances load", True, False)]
ROW_Y = [0.55, -0.1, -0.75, -1.4]


def mini_q(cx, cy, n=1, pad=False):
    g = VGroup()
    for i in range(n):
        y = cy - 0.25 * (n - 1) + 0.5 * i - 0.0
        t = RoundedRectangle(width=0.8, height=0.08, corner_radius=0.04).set_fill(DIM, 0.6).set_stroke(DIM, 1.5)
        dots = VGroup(*[Dot(radius=0.07, color=PROCESS_COLORS[k % 5]).shift(P3(-0.25 + 0.25 * k, 0.12)) for k in range(3 if n == 1 else 2)])
        g.add(VGroup(t, dots).move_to(P3(cx, y)))
    if pad:
        g.add(Padlock(0.28).move_to(P3(cx - 0.75, cy)))
    return g


class S20BigPicture(Ep10Scene):
    def construct(self):
        self.world(strip=0, stu="neutral", prof="neutral")
        stu, prof = self.stu, self.prof
        cards = [RoundedRectangle(width=3.4, height=3.2, corner_radius=0.2).set_fill(CARD_FILL, 1).set_stroke(DIM, 2).move_to(P3(x, 0.3))
                 for x in (-4, 0, 4)]
        lin = mono("Linux", 30, TEXT).move_to(P3(0, 2.3))
        self.add(*cards, lin)

        # S20.1
        frame = RoundedRectangle(width=9.6, height=3.9, corner_radius=0.2).set_fill(CARD_FILL, 1).set_stroke(DIM, 2).move_to(P3(0, 0.15))
        h_s = VGroup(label("SQMS", 28, VIRT), mini_q(0, 0, 1, pad=True)).arrange(DOWN, buff=0.12).move_to(P3(COLX["sqms"], 1.55))
        h_m = VGroup(label("MQMS", 28, VIRT), mini_q(0, 0, 2)).arrange(DOWN, buff=0.12).move_to(P3(COLX["mqms"], 1.55))
        labels = [label(r[0], 24).move_to(P3(COLX["label"], y)) for r, y in zip(ROWS, ROW_Y)]
        for lb in labels:
            lb.align_to(P3(-4.5, 0), LEFT)
        self.say("Let's put it all in one place.",
                 FadeOut(lin), ReplacementTransform(VGroup(*cards), frame),
                 Succession(Wait(0.6), AnimationGroup(FadeIn(h_s), FadeIn(h_m), *[FadeIn(l) for l in labels])),
                 stu.change("neutral"))

        def mark(ok, col, row):
            m = tick_mark(0.28) if ok else x_mark(0.28)
            return m.move_to(P3(COLX[col], ROW_Y[row]))
        # S20.2
        self.say("The single-queue approach is simple to build and balances load well…",
                 FadeIn(mark(True, "sqms", 0), scale=1.5), Succession(Wait(1.6), FadeIn(mark(True, "sqms", 3), scale=1.5)))
        # S20.3
        bounce = VGroup(Dot(radius=0.07, color=COL["A"]), CurvedArrow(P3(-0.15, 0), P3(0.15, 0), angle=-TAU / 4, color=DIM, tip_length=0.12))
        bounce.scale(1.0).move_to(P3(COLX["sqms"] + 0.6, ROW_Y[2]))
        self.say("…but struggles to scale to many processors, and loses cache affinity.",
                 FadeIn(mark(False, "sqms", 1), scale=1.5), Succession(Wait(1.8), FadeIn(mark(False, "sqms", 2), scale=1.5)),
                 FadeIn(bounce))
        # S20.4
        self.say("The multi-queue approach scales better and handles affinity well…",
                 FadeIn(mark(True, "mqms", 1), scale=1.5), Succession(Wait(1.8), FadeIn(mark(True, "mqms", 2), scale=1.5)))
        # S20.5
        idle = hatch_rect(0.4, 0.28).move_to(P3(COLX["mqms"] + 0.6, ROW_Y[3]))
        self.say("…but has trouble with load imbalance, and is more complicated.",
                 FadeIn(mark(False, "mqms", 3), scale=1.5), Succession(Wait(1.6), FadeIn(mark(False, "mqms", 0), scale=1.5)),
                 FadeIn(idle))

        # S20.6 balance scale
        beam = Line(P3(-0.6, 0), P3(0.6, 0)).set_stroke(TEXT, 4)
        post = Triangle().scale(0.15).set_fill(TEXT, 1).set_stroke(width=0).next_to(beam, DOWN, buff=0)
        pans = VGroup(*[Line(P3(x, 0), P3(x, -0.25)).set_stroke(TEXT, 2) for x in (-0.6, 0.6)])
        bal = VGroup(beam, pans, post).move_to(P3(0, -2.55))
        with self.narrate("Whichever approach you choose, there is no simple answer."):
            self.play(Indicate(h_s, color=CPU_COLOR), Indicate(h_m, color=CPU_COLOR), FadeIn(bal), run_time=1.0)
            self.play(Rotate(bal, angle=0.2, about_point=bal.get_center()), run_time=0.7)
            self.play(Rotate(bal, angle=-0.4, about_point=bal.get_center()), run_time=0.9)

        # S20.7
        code = VGroup(RoundedRectangle(width=1.2, height=0.7, corner_radius=0.08).set_fill("#272822", 1).set_stroke(DIM, 2),
                      *[Line(P3(-0.45, 0.2 - 0.18 * i), P3(0.45 - 0.3 * i, 0.2 - 0.18 * i)).set_stroke(DIM, 3) for i in range(3)])
        code[2].set_stroke(CPU_COLOR, 4)
        code.move_to(P3(-2.2, -2.7))
        thumb_a = ScheduleGrid(2, 6, 0.3, 0.25, colors=grid_colors(), row_labels=["", ""]).move_to(P3(0.6, -2.7))
        thumb_a.set_row(0, "AABBAA"); thumb_a.set_row(1, "BBAABB")
        thumb_b = ScheduleGrid(2, 6, 0.3, 0.25, colors=grid_colors(), row_labels=["", ""]).move_to(P3(0.6, -2.7))
        thumb_b.set_row(0, "ABABAB"); thumb_b.set_row(1, "BBBAAA")
        arr = Arrow(P3(-1.5, -2.7), P3(-0.5, -2.7), buff=0, color=DIM, stroke_width=3, tip_length=0.15)
        self.say("Building a general-purpose scheduler remains a daunting task, because small code changes can lead "
                 "to large behavioral differences.",
                 FadeOut(bal), FadeIn(code), Create(arr), FadeIn(thumb_a),
                 Succession(Wait(3.0), Indicate(code[2], color=KERNEL_COLOR), Transform(thumb_a, thumb_b)))

        # S20.8
        money = money_meter("$$$ / hour", 1.6).move_to(P3(3.6, -2.7))
        self.say("Only try it if you know exactly what you are doing, or, at least, if you are getting paid "
                 "a large amount of money to do so.",
                 FadeIn(money, shift=UP * 0.2), prof.change("proud"))
        self.beat(0.5)
