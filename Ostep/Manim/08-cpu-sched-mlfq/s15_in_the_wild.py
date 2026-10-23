import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403

CARDS_X = -3.8
CARD_YS = (1.7, 0.15, -1.4)


def info_card(title, y):
    fr = RoundedRectangle(width=3.8, height=1.4, corner_radius=0.15).set_fill(CARD_FILL, 1).set_stroke(DIM, 2.5)
    fr.move_to(P3(CARDS_X, y))
    t = Text(title, font_size=22, color=VIRT, weight=BOLD).move_to(fr.get_top() + DOWN * 0.28)
    t.align_to(fr, LEFT).shift(RIGHT * 0.25)
    return VGroup(fr, t), fr, t


def mini_ladder(n, x, y, tinted=(), w=1.4, step=0.16):
    g = VGroup()
    for i in range(n):
        col = KERNEL_COLOR if i in tinted else DIM
        r = Rectangle(width=w, height=step - 0.03).set_fill(col, 0.4 if i in tinted else 0.1).set_stroke(col, 1.2)
        r.move_to(P3(x, y + (n / 2 - i - 0.5) * step))
        g.add(r)
    return g


class S15InTheWild(Ep08Scene):
    def construct(self):
        self.build(lanes=3, cpu=True, ticks=30, board=False, stu="neutral", prof="neutral", term="parameterize")
        A, B = self.put("A", 2, 0), self.put("B", 2, 1)
        dim = VGroup(self.ladder, self.cpu, self.tl, A, B)
        # start: world faded to 15%
        dim.set_opacity(0.15)
        c1, f1, t1 = info_card("Solaris TS", CARD_YS[0])
        c2, f2, t2 = info_card("FreeBSD", CARD_YS[1])
        c3, f3, t3 = info_card("Reserved + nice", CARD_YS[2])

        # S15.1
        self.say("Real systems tune these knobs differently.", Create(f1), Succession(Wait(0.4), Create(f2)), Succession(Wait(0.8), Create(f3)))
        for f in (f1, f2, f3):
            f.set_fill(CARD_FILL, 1)

        # S15.2
        rows = VGroup(*[label(s, 16, DIM) for s in ("queue      slice", "Q59      20 ms", "...      more")]).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        rows.move_to(f1.get_center() + DOWN * 0.2).align_to(f1, LEFT).shift(RIGHT * 0.3)
        self.say("The Solaris Time-Sharing class is an editable table.", Write(t1), FadeIn(rows))

        # S15.3
        chips = VGroup(tag_chip("60 queues", TEXT, 20), tag_chip("20 ms to hundreds of ms", TEXT, 20), tag_chip("boost about once a second", TEXT, 20))
        chips.arrange(DOWN, buff=0.15, aligned_edge=LEFT).move_to(P3(0.7, 1.7))
        ml = mini_ladder(20, 3.2, 1.7, w=1.2, step=0.13)
        self.say("By default: sixty queues, slices growing from twenty milliseconds at the top to a few hundred at the bottom, and a boost about once a second.",
                 LaggedStart(*[FadeIn(c, shift=RIGHT * 0.3) for c in chips], lag_ratio=0.5), Succession(Wait(2.0), LaggedStart(*[FadeIn(r) for r in ml], lag_ratio=0.05)))

        # S15.4
        strike = Line(f1.get_corner(DL) + RIGHT * 0.1, f1.get_corner(UR) + LEFT * 0.1).set_stroke(KERNEL_COLOR, 4)
        self.say("FreeBSD skips the table.", FadeIn(c2), Succession(Wait(0.6), Create(strike)))
        self.play(FadeOut(VGroup(chips, ml)), run_time=0.5)

        # S15.5
        formula = MathTex(r"\text{priority} = f(\text{CPU used})", color=TEXT).scale(0.7).move_to(P3(0.6, 0.5))
        ax = Axes(x_range=[0, 4], y_range=[0, 1], x_length=2.0, y_length=0.7, tips=False, axis_config={"color": DIM, "stroke_width": 2})
        ax.move_to(P3(3.0, 0.35))
        curve = ax.plot(lambda x: np.exp(-x), x_range=[0, 4], color=PERS)
        dl = label("usage decays", 16, DIM).next_to(ax, UP, buff=0.05).shift(UP * 0.0)
        self.say("It computes priority from CPU used, and that usage decays over time, which plays the role of the boost.",
                 self.note("decay-usage"), Write(formula), Succession(Wait(1.5), Create(ax), Create(curve, run_time=1.5), FadeIn(dl)))

        # S15.6
        ml3 = mini_ladder(4, 1.0, -1.2, tinted=(0, 1), w=1.6, step=0.28)
        osl = label("OS only", 16, KERNEL_COLOR).next_to(ml3, RIGHT, buff=0.15).align_to(ml3, UP)
        self.say("Some schedulers reserve the top levels for the OS itself.", FadeIn(c3), FadeIn(ml3), FadeIn(osl))

        # S15.7
        term = Terminal(width=3.6, height=1.2, font_size=16, prompt="$").move_to(P3(4.6, -1.3))
        jb = job("A", 0.2).move_to(ml3[2].get_left() + RIGHT * 0.3)
        self.say("And many accept advice: the UNIX nice command raises or lowers a job's priority, a little.",
                 self.note("advice"), FadeIn(term), FadeIn(jb), Succession(Wait(1.0), term.type("nice -n 10 ./job")),
                 Succession(Wait(3.5), jb.animate.move_to(ml3[3].get_left() + RIGHT * 0.3)))

        # S15.8
        tip = TipCard(body=VGroup(label("Use advice where", 18, TEXT), label("possible", 18, TEXT)).arrange(DOWN, buff=0.05),
                      title="TIP", width=3.0, height=1.2, accent=DIM)
        tip.move_to(P3(5.0, 1.5))
        self.say("The OS rarely knows what's best, so it takes hints.", self.prof.change("explaining"), tip.slide_in(RIGHT))

        # S15.9
        hand = hand_icon(0.4).move_to(P3(2.7, -0.35))
        maybe = label("maybe", 18, DIM).next_to(hand, RIGHT, buff=0.1)
        self.say("It isn't obliged to obey.", FadeIn(hand), FadeIn(maybe), Wiggle(jb, scale_value=1.4, run_time=1.2))
        self.beat(1.0)
