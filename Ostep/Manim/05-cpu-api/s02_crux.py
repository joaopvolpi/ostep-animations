import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


class S02Crux(Ep05Scene):
    def construct(self):
        w = build_s01_end()
        walker, term, stu, prof = w["walker"], w["term"], w["stu"], w["prof"]
        stu.set_expression("curious")
        prof.set_expression("neutral")
        self.add(walker, term, stu, prof)

        # S02.1 (transition)
        badge = make_badge()
        card = CruxCard(CRUX_Q, CRUX_SUB, accent=VIRT)
        card.move_to(P3(0, 1.1))
        self.play(FadeOut(walker), FadeOut(term), FadeIn(badge, shift=RIGHT * 0.2), run_time=0.8)
        self.say_crux(card, stu.look_at(card), hold=0.6)

        # S02.2
        aside = AsideCard("Practical things. Real code. Type it in.", title="INTERLUDES", width=3.6, font_size=22)
        aside.move_to(P3(3.0, -1.9))
        with self.narrate("This is an interlude. A short, practical episode about a real interface, "
                          "with real code you can type in yourself."):
            self.play(aside.slide_in(RIGHT))
            self.wait(2.0)
            self.play(aside.slide_out(RIGHT))

        # S02.3
        menu = MenuCard("Process API", ["Create", "Destroy", "Wait", "Misc. control", "Status"],
                        width=4.0, height=4.4, font_size=28)
        menu.scale(0.6).move_to(P3(-3.6, -1.5))
        hl = [None]

        def pick(i):
            new = menu.row_highlight(i)
            new.scale(0.6).move_to(P3(menu.card.get_x(), menu.rows[i].get_y()))
            if hl[0] is None:
                hl[0] = new
                return FadeIn(new, run_time=0.3)
            return Transform(hl[0], new, run_time=0.3)

        with self.narrate("In episode four, we listed what any OS must offer: create, destroy, wait, "
                          "miscellaneous control, status."):
            self.play(FadeIn(menu, shift=RIGHT * 0.3), run_time=0.7)
            for i in range(5):
                self.play(pick(i))
                self.wait(0.1)

        # S02.4
        strip = card.strip()
        with self.narrate("Now we order from that menu, the UNIX way."):
            self.play(FadeOut(menu), FadeOut(hl[0]),
                      ReplacementTransform(card.frame, strip[0], run_time=1.2),
                      ReplacementTransform(card.question, strip[2], run_time=1.2),
                      FadeOut(card.header, run_time=0.5), FadeOut(card.subtitle, run_time=0.6),
                      stu.look_at(P3(0, 3.2)))
