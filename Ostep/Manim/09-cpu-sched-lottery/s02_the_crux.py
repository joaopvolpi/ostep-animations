import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


class S02TheCrux(Ep09Scene):
    def construct(self):
        w = build_s01_end()
        rack, chip, a, b, pie, l75, l25 = w["rack"], w["chip"], w["a"], w["b"], w["pie"], w["l75"], w["l25"]
        stu, prof, chips, tags, drum = w["stu"], w["prof"], w["chips"], w["tags"], w["drum"]
        self.add(rack, chip, a, b, pie, l75, l25, stu, prof, chips, tags, drum)

        # S02.1 (transition)
        badge = make_badge()
        small = target_pie()
        self.play(FadeOut(VGroup(rack, chip, a, b, chips, tags, drum, l75, l25)),
                  Transform(pie.sectors, small.sectors), FadeIn(small.label, shift=UP * 0.1),
                  FadeIn(badge.dot), FadeIn(badge.text, shift=RIGHT * 0.2),
                  stu.animate.scale(CHAR_SCALE).move_to(STUDENT_CORNER),
                  prof.animate.scale(CHAR_SCALE).move_to(PROF_CORNER),
                  run_time=1.6)
        self.add(badge)

        # S02.2 (card appears)
        card = CruxCard(CRUX_Q, CRUX_SUB, accent=VIRT, question_size=34, subtitle_size=22)
        card.move_to(P3(0, 0.5))
        self.say_crux(card, stu.change("neutral"), sub_anims=(stu.look_at(card),), hold=0.6)

        # S02.3
        self.say("This kind of scheduler is called proportional-share, or sometimes fair-share.",
                 self.term("proportional share", hold=1.0, at=(0, -1.3, 0)))

        # S02.4
        tl = Timeline(["CPU"], ticks=10, x_range=(-3.0, 3.0), top=-1.9, row_height=0.42, row_kinds=["cpu"],
                      tick_labels=False, label_font=20)
        preview = [COL["A"]] * 3 + [COL["B"]] + [COL["A"]] * 4 + [COL["B"], COL["A"]]
        self.add(tl)
        anims = [tl.fill("CPU", t + 1, "running", color=c, run_time=0.3) for t, c in enumerate(preview)]
        self.say("Instead of minimizing a time, it tries to guarantee that each job gets a certain percentage of the CPU.",
                 pie.pulse(), Succession(Wait(1.5), *anims))

        # S02.5
        strip = card.strip((0, 3.0, 0), 24)
        self.say("Let's find out how.",
                 ReplacementTransform(card.frame, strip[0], run_time=1.2),
                 ReplacementTransform(card.question, strip[2], run_time=1.2),
                 FadeOut(card.header, run_time=0.5), FadeOut(card.subtitle, run_time=0.6),
                 FadeOut(tl), prof.change("neutral"))
        self.beat(0.6)
