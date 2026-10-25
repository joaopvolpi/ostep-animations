import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403

K = 0.094      # units per ms


def block_row(ms, y, colors):
    row = VGroup(*[Rectangle(width=ms * K, height=0.5).set_fill(c, 1).set_stroke(TEXT, 1) for c in colors])
    row.arrange(RIGHT, buff=0).move_to(P3(0, y))
    return row


class S16MinGranularity(Ep09Scene):
    def construct(self):
        self.world(term="sched_latency", stu="confused", prof="happy")
        cols = [PROCESS_COLORS[i % 6] for i in range(10)]
        dots = VGroup(*[Dot(radius=0.14, color=c) for c in cols]).arrange(RIGHT, buff=0.25).move_to(P3(0, 1.3))
        eq = MathTex(r"48 \div 10 = 4.8\ \text{ms}", font_size=40, color=TEXT).move_to(P3(0, 2.2))
        row1 = block_row(4.8, -0.2, cols)
        flashes = VGroup(*[Line(row1[i].get_right() + UP * 0.35, row1[i].get_right() + DOWN * 0.35).set_stroke(KERNEL_COLOR, 3)
                           for i in range(9)])
        sc = Text("switch cost", font_size=20, color=KERNEL_COLOR).next_to(row1, UP, buff=0.45)

        # S16.1
        self.say("Ten processes? Forty-eight over ten is four point eight milliseconds: too small.",
                 LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.1), Write(eq),
                 Succession(Wait(2.0), FadeIn(row1), LaggedStart(*[FadeIn(f) for f in flashes], lag_ratio=0.1), FadeIn(sc)))

        # S16.2
        floor = DashedLine(row1.get_left() + RIGHT * 6 * K + UP * 0.6, row1.get_left() + RIGHT * 6 * K + DOWN * 0.6,
                           color=CPU_COLOR, dash_length=0.08)
        fl = Text("6 ms", font_size=22, color=CPU_COLOR).next_to(floor, DOWN, buff=0.08)
        crosses = VGroup(*[Line(b.get_corner(DL), b.get_corner(UR)).set_stroke(KERNEL_COLOR, 2) for b in row1])
        self.say("So the second knob, min_granularity, typically six milliseconds, says never go below this.",
                 self.term("min_granularity"), FadeIn(floor), FadeIn(fl), Succession(Wait(2.5), Create(crosses)))

        # S16.3
        row2 = block_row(6, -0.2, cols)
        eq2 = MathTex(r"\max(4.8,\,6) = 6\ \text{ms}", font_size=40, color=TEXT).move_to(eq)
        self.say("Ten processes get six each.",
                 FadeOut(crosses), FadeOut(flashes), FadeOut(sc), FadeOut(floor), FadeOut(fl),
                 Transform(row1, row2), Transform(eq, eq2))

        # S16.4
        x0 = row2.get_left()[0]
        brace = Brace(Line(P3(x0, -0.6, ), P3(x0 + 48 * K, -0.6)), DOWN, color=TEXT)
        bl = Text("48 ms", font_size=22, color=TEXT).next_to(brace, DOWN, buff=0.08)
        late = Text("round of 60 ms", font_size=22, color=DIM).next_to(row2, UP, buff=0.4)
        ok = tick_mark(0.3).next_to(late, RIGHT, buff=0.2)
        self.say("Not perfectly fair over forty-eight, but close, and cheap.",
                 FadeIn(brace), FadeIn(bl), Succession(Wait(1.0), FadeIn(late), FadeIn(ok)))
        self.beat(0.8)
        self.play(FadeOut(VGroup(dots, eq, row1, brace, bl, late, ok)), run_time=0.8)
