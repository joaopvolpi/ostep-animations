import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from manim import *  # noqa: E402,F403
from ostep_lib import *  # noqa: E402,F403
from common import *  # noqa: E402,F403


class S01Welcome(NarratedScene):
    def construct(self):
        stu, prof = make_hosts("dialog")
        prof.set_expression("neutral")
        prof.shift(RIGHT * 6.5)
        stu.shift(LEFT * 6.5)
        self.add(prof, stu)

        # S01.1
        self.say("Welcome! This is a series about operating systems,",
                 Succession(prof.animate(run_time=1.2).move_to(PROF_DIALOG),
                            prof.change("happy", run_time=0.5),
                            Wiggle(prof, scale_value=1.04, rotation_angle=0.07, n_wiggles=4, run_time=1.0)))

        # S01.2
        title, credit = make_title()
        self.say("based on a book called Operating Systems: Three Easy Pieces.",
                 Succession(Write(title, run_time=1.6), FadeIn(credit, shift=UP * 0.1, run_time=0.6)))

        # S01.3
        tag = name_tag("Professor", 15)
        tag.move_to([prof.get_center()[0], prof.get_bottom()[1] - tag.height / 2 - 0.1, 0])
        with self.narrate("I'm here to teach you what you need to know. I'm called \"Professor\". Who are you?"):
            self.wait(1.2)
            self.play(FadeIn(tag, scale=0.5), run_time=0.4)
            self.wait(1.5)
            self.play(FadeOut(tag), prof.look_at(LEFT * 7 + DOWN * 0.8), run_time=0.5)

        # S01.4
        stag = name_tag("Student", 15)
        with self.narrate("Hi, Professor! I'm called \"Student\", as you might have guessed. And I'm ready to learn!"):
            p1 = center_base(stu, STU_DIALOG + LEFT * 2.2)
            p2 = center_base(stu, STU_DIALOG)
            self.play(hop_to(stu, p1, run_time=0.55))
            self.play(hop_to(stu, p2, run_time=0.55))
            self.play(stu.change("excited"), run_time=0.5)
            stag.move_to([stu.get_center()[0], stu.get_bottom()[1] - stag.height / 2 - 0.1, 0])
            self.play(FadeIn(stag, scale=0.5), run_time=0.4)
            self.wait(1.3)
            self.play(FadeOut(stag), stu.look_at(prof), prof.look_at(stu), run_time=0.5)
        self.beat(0.5)
