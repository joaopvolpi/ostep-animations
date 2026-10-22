import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403
from s18_recap import LINES, icon  # noqa: E402,F401


class S19Teaser(Ep07Scene):
    def construct(self):
        self.world(stu="neutral", prof="proud", strip=False, badge=False)
        stu, prof = self.stu, self.prof
        head = Text("Recap", font_size=44, color=VIRT, weight=BOLD).move_to(P3(-6.2, 2.85), aligned_edge=LEFT)
        lines = VGroup(*[Text(wrap_text(s, 7.8, 26), font_size=26, color=TEXT, line_spacing=0.75) for s in LINES])
        lines.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(P3(-6.2, 2.25), aligned_edge=UL)
        self.add(head, lines)

        # S19.1
        s_pos, p_pos = P3(-2.6, -1.2 - 1.05), P3(2.6, -1.2 - 1.05)
        self.say("So how does a real scheduler decide, if it can't see the future?",
                 FadeOut(VGroup(head, lines)),
                 stu.animate.scale(1 / CHAR_SCALE).move_to(P3(-2.6, -1.2)),
                 prof.animate.scale(1 / CHAR_SCALE).move_to(P3(2.6, -1.2)))
        self.play(stu.change("curious"), run_time=0.5)

        # S19.2
        hist = VGroup(*[Rectangle(width=w, height=0.28).set_fill(COL["A"], 1).set_stroke(TEXT, 1) for w in (0.5, 0.7, 0.45)])
        hist.arrange(RIGHT, buff=0.15).move_to(P3(-1.0, 1.8))
        nxt = Rectangle(width=0.55, height=0.28).set_fill(opacity=0).set_stroke(COL["A"], 2).next_to(hist, RIGHT, buff=1.0)
        arr = DashedLine(hist.get_right() + RIGHT * 0.05, nxt.get_left() + LEFT * 0.05, dash_length=0.1).add_tip(tip_length=0.15)
        arr.set_stroke(DIM, 3)
        hl = Text("recent past", font_size=20, color=DIM).next_to(hist, UP, buff=0.15)
        nl = Text("short again?", font_size=20, color=DIM).next_to(nxt, UP, buff=0.15)
        self.say("By watching the recent past. If a job has been short so far, it's probably short again.",
                 prof.change("happy"), FadeIn(hist, shift=RIGHT * 0.3), FadeIn(hl),
                 Succession(Wait(2.5), Create(arr), FadeIn(nxt), FadeIn(nl)))

        # S19.3
        bars = VGroup(*[Rectangle(width=2.6, height=0.3).set_fill(CARD_FILL, 1).set_stroke(c, 3)
                        for c in (CONC, VIRT, KERNEL_COLOR)])
        for i, b in enumerate(bars):
            b.move_to(P3(-0.8 + 0.8 * i, 2.4 - 0.6 * i))
        hopper = proc("A", scale=0.28, label=None)
        bottom_to(hopper, bars[0].get_top() + RIGHT * 0.5)
        hops = Succession(hop_bottom(hopper, bars[1].get_top() + RIGHT * 0.5, run_time=0.6),
                          hop_bottom(hopper, bars[2].get_top() + RIGHT * 0.5, run_time=0.6),
                          hop_bottom(hopper, bars[1].get_top() + RIGHT * 0.5, run_time=0.6),
                          hop_bottom(hopper, bars[0].get_top() + RIGHT * 0.5, run_time=0.6))
        self.say("That idea has a name: the multi-level feedback queue.",
                 FadeOut(VGroup(hist, hl, arr, nxt, nl)), LaggedStart(*[FadeIn(b) for b in bars], lag_ratio=0.4),
                 FadeIn(hopper), Succession(Wait(1.5), hops), stu.change("excited"))

        # S19.4
        self.play(FadeOut(*self.mobjects), run_time=0.5)
        dot = Dot(radius=0.1, color=VIRT)
        nxt_t = Text("Next: 08 · The Multi-Level Feedback Queue", font_size=40, color=TEXT)
        card = VGroup(dot, nxt_t).arrange(RIGHT, buff=0.3).move_to(ORIGIN)
        self.play(FadeIn(card), run_time=0.8)
        self.wait(2.0)
