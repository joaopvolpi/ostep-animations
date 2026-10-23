import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


def mini_card(text, w=1.5, color=DIM):
    r = RoundedRectangle(width=w, height=0.34, corner_radius=0.06).set_fill(CARD_FILL, 1).set_stroke(color, 1.5)
    t = Text(text, font_size=14, color=TEXT, font=MONO_FONT).move_to(r)
    return VGroup(r, t)


class S05UseRandomness(Ep09Scene):
    def construct(self):
        self.world(stu="neutral", prof="neutral")
        stu, prof = self.stu, self.prof

        # S05.1
        coin = coin_icon(0.6).move_to(P3(4.0, 0.8))
        sloppy = Text("sloppy?", font_size=24, color=DIM).next_to(coin, UP, buff=0.3)
        cpu = CPU(size=0.9, label="CPU").move_to(P3(4.0, -0.7))
        flip = Succession(*[Rotate(coin, angle=PI, axis=RIGHT, run_time=0.35) for _ in range(4)])
        self.say("Hold on. We're letting the OS flip coins? Isn't that sloppy?",
                 stu.change("frustrated"), FadeIn(coin), FadeIn(cpu), Succession(Wait(0.6), flip), FadeIn(sloppy))

        # S05.2
        card = TipCard("", title="TIP: Use randomness", width=6.6, height=4.7, accent=DIM)
        card.move_to(P3(-1.0, 0.0))
        self.say("It's the most beautiful part. Random buys you three things.",
                 prof.change("happy"), FadeOut(VGroup(coin, sloppy, cpu)), card.slide_in(LEFT))

        def badge(n, y):
            c = Circle(radius=0.2).set_fill(VIRT, 1).set_stroke(outline_of(VIRT), 2).move_to(P3(-3.8, y))
            return VGroup(c, Text(str(n), font_size=22, color=INK_DARK).move_to(c))

        ys = [1.05, -0.2, -1.4]
        b1, b2, b3 = badge(1, ys[0]), badge(2, ys[1]), badge(3, ys[2])

        # S05.3
        gear = GearPair(0.22).move_to(P3(-2.9, ys[0]))
        t1 = Text("clever algorithm", font_size=20, color=TEXT).move_to(P3(-1.5, ys[0]))
        jag = VMobject().set_points_as_corners([P3(-0.1 + 0.12 * k, ys[0] + (0.15 if k % 2 else -0.15)) for k in range(8)])
        jag.set_stroke(KERNEL_COLOR, 3)
        cross = x_mark(0.3).move_to(P3(1.4, ys[0]))
        lru = ep_tag("LRU → Ep. 22", color=DIM, font_size=16).move_to(P3(-1.5, ys[0] - 0.45))
        self.say("One: no nasty corner cases. Some clever algorithms have a workload that makes them fall apart, "
                 "like the LRU policy we'll meet in the memory episodes.",
                 FadeIn(b1), FadeIn(gear), FadeIn(t1), Succession(Wait(2.5), Create(jag), FadeIn(cross), FadeIn(lru)),
                 gear.spin(angle=TAU, run_time=3))

        # S05.4
        die = die_icon(0.5).move_to(P3(-2.9, ys[0]))
        t1b = Text("random: no bad workload", font_size=20, color=TEXT).move_to(P3(-1.0, ys[0]))
        tick = tick_mark(0.3).move_to(P3(1.4, ys[0]))
        self.say("Random has no such workload.",
                 FadeOut(gear), FadeOut(t1), FadeOut(cross), FadeOut(lru), FadeIn(die), FadeIn(t1b),
                 Succession(Wait(0.6), FadeIn(tick)))

        # S05.5
        left = VGroup(*[mini_card("cpu used: 12.4 ms") for _ in range(2)]).arrange(DOWN, buff=0.1).move_to(P3(-2.3, ys[1]))
        right = VGroup(*[mini_card("tickets: 100") for _ in range(2)]).arrange(DOWN, buff=0.1).move_to(P3(0.2, ys[1]))
        strike = Line(left.get_corner(DL), left.get_corner(UR)).set_stroke(KERNEL_COLOR, 4)
        self.say("Two: almost no state. A counting scheduler must track every process's CPU use; random only needs each "
                 "process's tickets.",
                 FadeIn(b2), FadeIn(left), Succession(Wait(2.0), FadeIn(right), Create(strike)))

        # S05.6
        sw = stopwatch_icon(0.28).move_to(P3(-2.7, ys[2]))
        drum = RaffleDrum(0.7).move_to(P3(-0.2, ys[2] - 0.2))
        t3 = Text("fast", font_size=22, color=TEXT).move_to(P3(-1.5, ys[2]))
        ball, anim = drum.draw(7, COL["A"], run_time=0.6)
        self.say("Three: speed, as long as the random number is quick.",
                 FadeIn(b3), FadeIn(sw), FadeIn(t3), FadeIn(drum), Succession(Wait(1.0), anim))
        self.beat(0.5)
        # transition: the card slides out
        self.play(card.slide_out(LEFT), FadeOut(VGroup(b1, b2, b3, die, t1b, jag, tick, left, right, strike, sw, t3, drum, ball)),
                  run_time=0.8)
