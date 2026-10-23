import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common_more import *  # noqa: E402,F401,F403


class S03Crux(Ep10Scene):
    def construct(self):
        w = build_s02_end()
        lap, chips, threads, cores, sw, others, stu, prof = (
            w[k] for k in ("lap", "chips", "threads", "cores", "sw", "others", "stu", "prof"))
        self.add(lap, chips, *threads, cores, sw, *others, stu, prof)

        # S03.1 (transition): everything fades, the badge forms
        badge = make_badge()
        self.play(FadeOut(VGroup(lap, cores, sw, *others)),
                  *[t.animate.scale(0.2).move_to(badge.dot) for t in threads],
                  *[c.animate.scale(0.2).move_to(badge.dot).set_opacity(0) for c in chips],
                  FadeIn(badge.dot), FadeIn(badge.text, shift=RIGHT * 0.2), run_time=1.4)
        self.remove(*threads, chips)
        self.add(badge)

        # S03.2
        card = CruxCard(CRUX_Q, CRUX_SUB, accent=VIRT, question_size=32, subtitle_size=22).move_to(P3(0, 0.3))
        self.say_crux(card, stu.look_at(card), prof.look_at(card), hold=0.4)
        self.say("So that's the question. Do the old techniques work, or do we need new ideas?")

        # S03.3
        t1 = VGroup(label("old techniques", 26), tick_mark(0.3)).arrange(RIGHT, buff=0.2)
        t2 = VGroup(label("new ideas", 26), tick_mark(0.3)).arrange(RIGHT, buff=0.2)
        tags = VGroup(t1, t2).arrange(RIGHT, buff=1.2).move_to(P3(0, -1.8))
        self.say("Spoiler: a bit of both.", FadeIn(t1, shift=UP * 0.2),
                 Succession(Wait(0.8), FadeIn(t2, shift=UP * 0.2)))

        # S03.4
        self.say("But to see why, we first have to look at what changed in the hardware.",
                 FadeOut(tags), card.dock(run_time=1.2), stu.change("curious"))
        self.beat(0.3)
