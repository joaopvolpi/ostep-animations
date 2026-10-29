import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


class S02TheCrux(Ep08Scene):
    def construct(self):
        # starts with S01's end state
        stu, prof = student_dlg("confused"), prof_dlg("happy")
        hist = history_clock(0.5).scale(1.3).move_to(P3(0, 1.5))
        self.add(stu, prof, hist)
        self.stu, self.prof = stu, prof

        # S02.1 (transition + card)
        card = CruxCard(CRUX_Q, CRUX_SUB, accent=VIRT, question_size=32)
        card.move_to(P3(0, 0.9))
        badge = SectionBadge(BADGE_TEXT, accent=VIRT)
        self.play(FadeOut(hist), stu.animate.scale(CHAR_SCALE).move_to(STUDENT_CORNER),
                  prof.animate.scale(CHAR_SCALE).move_to(PROF_CORNER), run_time=1.2)
        self.say_crux(card, stu.change("curious", look_at=card), prof.change("neutral"), hold=0.6,
                      lead="Which brings us to the crux: {q}")

        # S02.2
        self.say("Today's answer is one of the most famous ideas in scheduling: the Multi-Level Feedback Queue, or MLFQ.",
                 self.term("MLFQ", at=P3(0, -1.7)))

        # S02.3
        tag = tag_chip("1962 · CTSS", TEXT, 24).move_to(P3(0, -1.6))
        self.say("It was first described in 1962, in the Compatible Time-Sharing System…",
                 FadeIn(tag, shift=UP * 0.4))

        # S02.4
        medal = medal_glyph(0.6).next_to(tag, LEFT, buff=0.25)
        name = label("F. Corbato · Turing Award", 22, DIM).next_to(tag, DOWN, buff=0.2)
        self.say("…and it helped earn its creator, Fernando Corbato, the Turing Award.",
                 FadeIn(medal, scale=1.4), FadeIn(name))

        # S02.5
        board = RuleBoard(row_h=0.58)
        sk = board.skeleton(5)
        self.say("We'll build it in five rules.",
                 FadeOut(VGroup(tag, medal, name)), card.dock(), FadeIn(badge.dot), FadeIn(badge.text, shift=RIGHT * 0.2),
                 FadeIn(board.frame), FadeIn(board.header), FadeIn(sk))
        self.add(badge, board)

        # S02.6
        chips = VGroup(*[tag_chip(f"R{i}", VIRT, 20) for i in range(1, 6)])
        chain = VGroup()
        for i, c in enumerate(chips):
            chain.add(c)
            if i < 4:
                chain.add(Arrow(ORIGIN, RIGHT * 0.4, buff=0, color=DIM, stroke_width=3, tip_length=0.12))
        chain.arrange(RIGHT, buff=0.1).move_to(P3(-0.3, 0.3))
        lab = label("each fixes the last", 24, DIM).next_to(chain, DOWN, buff=0.25)
        self.say("Each one is the answer to a problem with the one before.",
                 LaggedStart(*[FadeIn(m, shift=RIGHT * 0.2) for m in chain], lag_ratio=0.15), FadeIn(lab))
        self.beat(1.0)
