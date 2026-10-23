import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common_more import *  # noqa: E402,F401,F403
from ostep_lib.props.p06_icons import magnifier_icon  # noqa: E402


def mini_chip2(x, y):
    return CPU(size=0.3, label=None, pins=2).move_to(P3(x, y))


def mini_tray(x, y, n=2):
    t = RoundedRectangle(width=0.7, height=0.08, corner_radius=0.04).set_fill(DIM, 0.6).set_stroke(DIM, 1.5).move_to(P3(x, y))
    dots = VGroup(*[Dot(radius=0.07, color=PROCESS_COLORS[i % 5]).move_to(P3(x - 0.2 + 0.2 * i, y + 0.12)) for i in range(n)])
    return VGroup(t, dots)


def mini_multi(cx, cy):
    g = VGroup()
    for dx in (-0.55, 0.55):
        g.add(mini_tray(cx + dx, cy - 0.35), mini_chip2(cx + dx, cy + 0.35),
              Line(P3(cx + dx, cy - 0.15), P3(cx + dx, cy + 0.15)).set_stroke(DIM, 2))
    return g


def mini_single(cx, cy):
    g = VGroup(mini_tray(cx, cy - 0.35, 3))
    for dx in (-0.55, 0.55):
        g.add(mini_chip2(cx + dx, cy + 0.35), Line(P3(cx, cy - 0.28), P3(cx + dx, cy + 0.2)).set_stroke(DIM, 2))
    return g


class S19Linux(Ep10Scene):
    def construct(self):
        self.world(strip=2, stu="neutral", prof="neutral")
        stu, prof = self.stu, self.prof

        # S19.1
        lin = mono("Linux", 30, TEXT).move_to(P3(0, 2.3))
        self.say("So what does a real system do? Interestingly, in the Linux community no single solution won.",
                 FadeOut(self.strip), FadeIn(lin, shift=DOWN * 0.2), stu.change("curious"))

        # S19.2
        cards = [RoundedRectangle(width=3.4, height=3.2, corner_radius=0.2).set_fill(CARD_FILL, 1).set_stroke(DIM, 2).move_to(P3(x, 0.3))
                 for x in (-4, 0, 4)]
        self.say("Three different multiprocessor schedulers arose over time.",
                 LaggedStart(*[FadeIn(c, shift=UP * 0.4) for c in cards], lag_ratio=0.3), prof.change("happy"))

        # S19.3
        titles = [label(t, 36, TEXT).move_to(P3(x, 1.45)) for t, x in (("O(1)", -4), ("CFS", 0), ("BFS", 4))]
        with self.narrate("The O(1) scheduler, the Completely Fair Scheduler, or CFS, and the BF Scheduler, or BFS."):
            for t in titles:
                self.play(Write(t), run_time=0.8)
                self.wait(0.4)

        # S19.4
        pics = [mini_multi(-4, 0.55), mini_multi(0, 0.55), mini_single(4, 0.55)]
        self.say("O(1) and CFS use multiple queues. BFS uses a single queue.",
                 LaggedStart(*[FadeIn(p, shift=UP * 0.2) for p in pics], lag_ratio=0.4))

        # S19.5
        okt = tick_mark(0.4).move_to(P3(2.0, 0.55))
        self.say("So, both approaches can work, in practice.", FadeIn(okt, scale=1.4))

        # S19.6
        def blurb(txt, x):
            return centered_text(txt, 3.0, 20, TEXT).move_to(P3(x, -0.85))
        ladder = MLFQLadder(levels=3, labels=["", "", ""], x_range=(-0.5, 0.5), arrows=False)
        ladder.scale(0.28).move_to(P3(-4, -0.2))
        b1 = blurb("priority-based (MLFQ-like), interactivity", -4)
        self.say("O(1) is a priority-based scheduler, a bit like the MLFQ we saw before.",
                 FadeIn(b1, shift=UP * 0.1), FadeIn(ladder), FadeOut(okt))

        # S19.7
        share = VGroup(*[Rectangle(width=w, height=0.22).set_fill(c, 0.9).set_stroke(INK, 1.5) for w, c in
                         ((0.7, COL["A"]), (0.4, COL["B"]), (0.25, COL["D"]))]).arrange(RIGHT, buff=0).move_to(P3(0, -0.2))
        b2 = blurb("proportional share (stride-like)", 0)
        self.say("CFS, in contrast, is deterministic and proportional-share, like the stride scheduling from last time.",
                 FadeIn(b2, shift=UP * 0.1), FadeIn(share))

        # S19.8
        b3 = blurb("proportional share, EEVDF", 4)
        self.say("BFS is also proportional-share, but built on a more complicated scheme called "
                 "Earliest Eligible Virtual Deadline First, EEVDF.",
                 FadeIn(b3, shift=UP * 0.1))

        # S19.9
        sticker = VGroup(tag("(look it up!)", 18, CPU_COLOR), magnifier_icon(0.4)).arrange(RIGHT, buff=0.1).move_to(P3(3.4, -1.75))
        self.say("And about that BF in BFS: the book says you should look it up yourself. It is not for the faint of heart.",
                 FadeIn(sticker, shift=UP * 0.2), stu.change("surprised"))

        # S19.10
        card = aside_card("Meehan's dissertation, linked below", title="ASIDE", width=5.0, font_size=22).move_to(P3(0, -2.55))
        self.say("Read more about them on your own.", card.slide_in(UP))
        self.beat(0.5)
