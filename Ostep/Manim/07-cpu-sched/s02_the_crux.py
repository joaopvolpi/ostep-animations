import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


class S02TheCrux(Ep07Scene):
    def construct(self):
        w = build_s01_end()
        desk, q, family, you, carton = w["desk"], w["q"], w["family"], w["you"], w["carton"]
        carts, checkbook, spot, tag, stu, prof = w["carts"], w["checkbook"], w["spot"], w["tag"], w["stu"], w["prof"]
        self.add(desk, q, family, you, carton, carts, checkbook, spot, tag, stu, prof)

        # S02.1 (transition)
        badge = make_badge()
        spot2 = Spotlight(height=1.1, spread=0.4)
        spot2.move_beam_to(P3(0.0, -2.0))
        self.play(FadeOut(VGroup(desk, q, family, you, carton, carts, checkbook, tag)),
                  Transform(spot, spot2),
                  FadeIn(badge.dot), FadeIn(badge.text, shift=RIGHT * 0.2),
                  stu.animate.scale(CHAR_SCALE / 0.9).move_to(STUDENT_CORNER),
                  prof.animate.scale(CHAR_SCALE / 0.8).move_to(PROF_CORNER),
                  run_time=1.6)
        self.add(badge)

        # S02.2 (card appears)
        card = CruxCard(CRUX_Q, CRUX_SUB, accent=VIRT, question_size=32)
        card.move_to(P3(0, 0.9))
        self.say_crux(card, stu.change("neutral"), prof.change("neutral"), hold=0.6)

        # S02.3
        gears = GearPair(0.5).move_to(P3(-4.2, -1.6))
        ep6 = ep_tag("Ep. 06").next_to(gears, DOWN, buff=0.15)
        self.say("Remember mechanisms versus policies? Last episode we met the mechanism: the context switch.",
                 FadeIn(gears, shift=RIGHT * 0.6), FadeIn(ep6, shift=UP * 0.2), gears.spin(angle=TAU, run_time=3.5),
                 prof.change("explaining"))

        # S02.4
        a = proc("A", scale=0.4).move_to(P3(-2.5, -1.7))
        b = proc("B", scale=0.4).move_to(P3(-1.5, -1.7))
        self.play(FadeIn(a), FadeIn(b), run_time=0.4)
        pa, pb = a.get_bottom().copy(), b.get_bottom().copy()
        self.say("It tells the OS how to stop one process and start another.",
                 hop_bottom(a, pb, run_time=0.9, height=0.5), hop_bottom(b, pa, run_time=0.9, height=0.7),
                 gears.spin(angle=TAU * 0.7, run_time=1.8))

        # S02.5
        qq = Queue(label=None, center=(2.5, -2.05), slots=3, spacing=0.65)
        qa, qb, qc = [proc(n, scale=0.4) for n in "ABC"]
        qq.place(qa, qb, qc)
        spot3 = Spotlight(height=1.1, spread=0.4)
        spot3.move_beam_to(P3(2.5 - 0.65, -2.0))
        self.say("Today is about the which.",
                 VGroup(gears, ep6, a, b).animate.shift(LEFT * 1.0).set_opacity(0.35),
                 FadeIn(qq), FadeIn(qa), FadeIn(qb), FadeIn(qc),
                 Transform(spot, spot3))

        # S02.7
        strip = card.strip()
        self.say("And the answer, as we'll see, is surprisingly full of trade-offs.",
                 ReplacementTransform(card.frame, strip[0], run_time=1.2),
                 ReplacementTransform(card.question, strip[2], run_time=1.2),
                 FadeOut(card.header, run_time=0.5), FadeOut(card.subtitle, run_time=0.6),
                 prof.change("neutral"))
        self.beat(0.8)
