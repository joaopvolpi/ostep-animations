import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


class S07SpaceSharing(Ep04Scene):
    def construct(self):
        self.add_badge()
        self.add_docked_term("time sharing")
        stu, prof = self.add_corner_chars("neutral", "explaining")
        d = build_s06_parts(final=True)
        add_s06_world(self, d)

        dim = Rectangle(width=16, height=9).set_fill(BG, 0.7).set_stroke(width=0)
        card = TipCard(VGroup(), title="TIP", width=5.6, height=4.0)
        card.move_to(P3(3.8, 0.5))
        cc = card.content_center()

        # S07.1
        term_at = cc + UP * 1.05
        with self.narrate("By the way, time sharing has a sibling: space sharing."):
            self.play(FadeIn(dim), card.slide_in(RIGHT), run_time=0.8)
            self.play(self.note("space sharing"))

        # S07.2
        n = 8
        bw = 0.55
        blocks = VGroup(*[Rectangle(width=bw, height=0.5).set_stroke(DISK_COLOR, 2.5).set_fill(DISK_COLOR, 0.05)
                          for _ in range(n)]).arrange(RIGHT, buff=0)
        blocks.move_to(cc + UP * 0.1)
        dlab = Text("disk", font_size=22, color=DISK_COLOR).next_to(blocks, UP, buff=0.1, aligned_edge=LEFT)
        self.say("Instead of taking turns, you split the resource up. Your disk works like this.",
                 Create(blocks, run_time=1.0), FadeIn(dlab))

        # S07.3
        fa = Text("file A", font_size=20, color=COL["A"]).next_to(blocks[0:3], DOWN, buff=0.1)
        fb = Text("file B", font_size=20, color=COL["B"]).next_to(blocks[3:5], DOWN, buff=0.1)
        clock = ClockIcon(0.22).next_to(blocks, UP, buff=0.12).align_to(blocks, RIGHT)
        cmp = VGroup(Text("time sharing: take turns", font_size=20, color=TEXT),
                     Text("space sharing: split it up", font_size=20, color=TEXT)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        cmp.move_to(cc + DOWN * 1.15)
        with self.narrate("A block given to one file stays with that file until the file is deleted."):
            self.play(LaggedStart(*[blocks[i].animate.set_fill(COL["A"], 0.9) for i in range(3)],
                                  *[blocks[i].animate.set_fill(COL["B"], 0.9) for i in (3, 4)], lag_ratio=0.2),
                      FadeIn(fa), FadeIn(fb), FadeIn(clock), run_time=1.2)
            self.play(clock.spin(2, run_time=1.6), FadeIn(cmp, shift=UP * 0.2, run_time=0.8))
        self.beat(0.8)

        # S07.4
        content = VGroup(blocks, dlab, fa, fb, clock, cmp)
        self.play(FadeOut(VGroup(card, content), shift=RIGHT * 1.5), FadeOut(dim), run_time=0.8)
        self.wait(0.3)
