import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403

# NOTE: users are neutral cards (DIM frame, white text) so they don't clash with processes A and B;
# only the job chips use coral / mint.
A2_COLOR = "#F2A58C"


def user_card(name, tix, at):
    r = card_rect(2.6, 1.0)
    t = Text(name, font_size=24, color=TEXT).move_to(r.get_center() + UP * 0.2)
    n = Text(f"{tix} tickets", font_size=22, color=DIM).move_to(r.get_center() + DOWN * 0.2)
    return VGroup(r, t, n).move_to(at)


def tag_row(lit):
    g = VGroup()
    for i, n in enumerate(("currency", "transfer", "inflation")):
        t = token(n, VIRT if i == lit else DIM, size=20)
        g.add(t.move_to(P3(-2.6 + 2.6 * i, 2.35)))
        if i != lit:
            t.set_opacity(0.6)
    return g


class S06TicketCurrency(Ep09Scene):
    def construct(self):
        self.world(stu="frustrated", prof="happy")
        # S06.1
        tags = tag_row(0)
        tags_dim = tag_row(-1)
        self.say("The ticket is a flexible tool. The book gives three tricks.",
                 LaggedStart(*[FadeIn(t, shift=DOWN * 0.15) for t in tags_dim], lag_ratio=0.3),
                 Succession(Wait(1.8), Transform(tags_dim[0], tags[0])))

        # S06.2
        ca = user_card("User A", 100, P3(-4.6, 1.0))
        a1 = proc("A", scale=0.45, label="A1").move_to(P3(-0.6, 1.4))
        a2 = proc("A", scale=0.45, color=A2_COLOR, label="A2").move_to(P3(-0.6, 0.2))
        self.say("Ticket currency. User A has a hundred tickets and two jobs, A1 and A2.",
                 self.term("ticket currency"),
                 FadeIn(ca, shift=RIGHT * 0.3), FadeIn(a1, shift=LEFT * 0.3), FadeIn(a2, shift=LEFT * 0.3))

        # S06.3
        ba1 = token("500 A-tickets", COL["A"], size=20).move_to(P3(1.7, 1.4))
        ba2 = token("500 A-tickets", COL["A"], size=20).move_to(P3(1.7, 0.2))
        cur = Text("A's currency", font_size=20, color=DIM).next_to(ca, DOWN, buff=0.12)
        self.say("She gives each five hundred tickets in her own currency.",
                 FadeIn(ba1, shift=RIGHT * 0.2), FadeIn(ba2, shift=RIGHT * 0.2), FadeIn(cur))

        # S06.4
        cb = user_card("User B", 100, P3(-4.6, -1.3))
        b1 = proc("B", scale=0.45, label="B1").move_to(P3(-0.6, -1.3))
        bb1 = token("10 B-tickets", COL["B"], size=20).move_to(P3(1.7, -1.3))
        self.say("User B has a hundred tickets and one job, B1, with ten of his.",
                 FadeOut(cur), FadeIn(cb, shift=RIGHT * 0.3), FadeIn(b1, shift=LEFT * 0.3), FadeIn(bb1))

        # S06.5
        glob_t = Text("global", font_size=22, color=DIM).move_to(P3(4.9, 2.0))
        n1 = token("50", COL["A"], size=22).move_to(P3(4.4, 1.4))
        n2 = token("50", A2_COLOR, size=22).move_to(P3(4.4, 0.2))
        n3 = token("100", COL["B"], size=22).move_to(P3(4.4, -1.3))
        arrows = VGroup(*[Arrow(s.get_right(), d.get_left(), buff=0.1, stroke_width=3, color=DIM,
                                max_tip_length_to_length_ratio=0.2)
                          for s, d in ((ba1, n1), (ba2, n2), (bb1, n3))])
        conv = Text("→ global", font_size=18, color=DIM).next_to(arrows[0], UP, buff=0.05)
        self.say("The system converts: A1 and A2 become fifty global tickets each, B1 becomes a hundred.",
                 FadeIn(glob_t), LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.3), FadeIn(conv),
                 Succession(Wait(1.5), AnimationGroup(FadeIn(n1), FadeIn(n2), FadeIn(n3))))

        # S06.6
        tot = Text("total: 200", font_size=24, color=CPU_COLOR).move_to(P3(4.4, -0.55))
        drum = RaffleDrum(0.8).move_to(P3(2.6, -2.35))
        ball, anim = drum.draw(137, CPU_COLOR, run_time=0.8)
        ball[0].scale(1.5)   # three digits fit inside the small ball
        ball[1].scale(0.85)
        self.add(drum)
        drum.set_opacity(0)
        with self.narrate("Two hundred in total, and the lottery runs on those."):
            self.play(drum.animate.set_opacity(1), FadeIn(tot), drum.spin(1, run_time=1.2))
            self.play(anim)
            self.play(glide(ball, n3.get_left() + LEFT * 0.4, 0.7))
            self.play(Indicate(n3, color=CPU_COLOR), FadeOut(ball))
        self.beat(0.4)
        self.fade_stage()
