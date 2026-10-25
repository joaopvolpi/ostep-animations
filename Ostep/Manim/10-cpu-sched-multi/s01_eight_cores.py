import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


class S01EightCores(Ep10Scene):
    def construct(self):
        lap, chips = build_laptop()
        stu = Student("excited").scale(CHAR_SCALE).move_to(STUDENT_CORNER)
        prof = Professor("thinking").scale(CHAR_SCALE).flip().move_to(PROF_CORNER)

        # S01.1
        cores = label("8 cores", 26).next_to(lap, UP, buff=0.15)
        self.say("My new laptop has eight cores!",
                 FadeIn(stu, shift=RIGHT * 0.8), Create(lap),
                 Succession(Wait(0.6), LaggedStart(*[GrowFromCenter(c) for c in chips], lag_ratio=0.3)),
                 Succession(Wait(1.6), FadeIn(cores, shift=UP * 0.2)))

        # S01.2
        self.say("So now every program I write runs eight times faster, right?",
                 stu.says(MathTex(r"8\times\ \text{faster?}", color=INK).scale(0.9), max_width=3.2, font_size=28))

        # S01.3
        a_c = FileIcon("a.c", color=TEXT, width=0.7, lines=3, font_size=22).move_to(P3(0, -1.9))
        self.say("Let's test that. Take a normal C program, the kind you've written all semester.",
                 FadeIn(prof, shift=LEFT * 0.8), FadeIn(a_c, shift=UP * 0.6))
        # S01.4
        a = proc("A", "running", 0.3)
        chip1 = chips[0]
        self.allow_overlap(a, chip1, "process A stands on its chip")
        lit = mini_chip(True).move_to(chip1)
        self.say("Run it on this machine.",
                 a_c.animate.move_to(chip1.get_center() + DOWN * 0.1).scale(0.3).set_opacity(0),
                 Succession(Wait(0.7), AnimationGroup(Transform(chip1, lit), FadeIn(a.move_to(chip1.get_top() + UP * 0.15)))))
        place_on(a, chip1.get_top() + DOWN * 0.05)
        self.allow_overlap(a, chip1, "process A stands on its chip")
        self.remove(a_c)

        # S01.5
        idle = VGroup(*chips[1:])
        br = Brace(idle, DOWN, buff=0.08)
        idle_t = label("idle ×7", 22, DIM).next_to(br, DOWN, buff=0.08)
        comp = Computer("idle").scale(0.35).move_to(P3(0, -2.6))
        self.say("One core lights up. Seven sit idle.",
                 GrowFromCenter(br), FadeIn(idle_t, shift=UP * 0.1), FadeIn(comp, scale=0.7), prof.change("neutral"))

        # S01.6
        sw = stopwatch("1× speed", 24).move_to(P3(4.3, 0.3))
        xm = x_mark(0.45).move_to(stu.get_top() + UP * 0.9 + RIGHT * 0.2)
        self.say("A typical program only uses a single CPU. Adding CPUs does not make it run faster.",
                 FadeIn(sw, shift=LEFT * 0.4), FadeIn(xm, scale=1.4),
                 stu.change("sad"))
        self.beat(0.6)
        self.play(stu.says(MathTex(r"1\times", color=INK), max_width=2, font_size=28), FadeOut(xm), run_time=0.8)
        self.beat(0.6)
