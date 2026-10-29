import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


class S01LoadedQuestion(Ep11Scene):
    def construct(self):
        stu, prof = student_dlg("neutral"), prof_dlg("neutral")
        badge = make_badge()
        self.stu, self.prof = stu, prof

        # S01.1
        self.play(FadeIn(stu), FadeIn(prof), run_time=0.7)
        self.play(stu.look_at(prof), prof.look_at(stu), Write(badge), run_time=0.8)

        # S01.2
        q = question_mark(0.4).next_to(stu, UP, buff=0.1).shift(UP * 0.1)
        self.say("So, Student. Did you learn anything?", GrowFromCenter(q))

        # S01.3
        self.say("That's a loaded question. I think you only want me to say \"yes.\"",
                 FadeOut(q), stu.thinks("yes?", expression="bored"), min_time=4.0)
        self.play(stu.look(UP), run_time=0.4)
        self.play(stu.look(ORIGIN), run_time=0.4)

        # S01.4
        self.say("True. But it's still an honest question. Give a professor a break, will you?",
                 stu.remove_bubble(), prof.change("happy"), min_time=4.5)
        self.play(prof.animate.shift(UP * 0.1), run_time=0.25)
        self.play(prof.animate.shift(DOWN * 0.1), run_time=0.25)

        # S01.5
        self.say("Okay, okay. I did learn a few things.", stu.change("neutral"))
        self.play(stu.animate.shift(DOWN * 0.2), run_time=0.2)
        self.play(stu.animate.shift(UP * 0.2), run_time=0.2)
        self.beat(0.5)
