import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


class S01ThreeCarts(Ep07Scene):
    def construct(self):
        w = build_s01_end()
        desk, q, family, you, carton = w["desk"], w["q"], w["family"], w["you"], w["carton"]
        carts, checkbook, spot, tag, stu, prof = w["carts"], w["checkbook"], w["spot"], w["tag"], w["stu"], w["prof"]

        # "you" starts at the left edge, holding the carton (the carton follows "you")
        bottom_to(you, P3(-6.0, FLOOR_Y + 0.02))
        carton.move_to(you.get_center() + RIGHT * 0.55 + UP * 0.1)
        off = carton.get_center() - you.get_center()
        carton.add_updater(lambda m: m.move_to(you.get_center() + off))
        stu.shift(LEFT * 3.2)
        prof.shift(RIGHT * 3.2)
        self.add(you, carton, stu, prof)

        # S01.1
        self.say("You're at the supermarket. You've got one carton of milk.",
                 FadeIn(desk, shift=LEFT * 0.4), hop_bottom(you, P3(-4.6, FLOOR_Y + 0.02), run_time=1.6))

        # S01.2
        self.say("You pick the shortest line, and just as you get there…",
                 FadeIn(q), hop_bottom(you, P3(Q_X["back"], FLOOR_Y + 0.02), run_time=1.4))

        # S01.3
        self.say("…the family in front of you starts unloading. Three carts. Piled high.",
                 FadeIn(family, shift=DOWN * 0.2),
                 after(1.2, LaggedStart(*[GrowFromCenter(c) for c in carts], lag_ratio=0.8, run_time=2.4)))

        # S01.4
        self.say("Plus a checkbook.", GrowFromCenter(checkbook), desk.blink(run_time=0.8))

        # S01.5
        sw = stopwatch_icon(0.24).move_to(you.get_top() + UP * 0.35 + RIGHT * 0.1)
        self.say("I'm going to be here all day.",
                 stu.animate.shift(RIGHT * 3.2), FadeIn(sw),
                 after(0.4, Rotate(sw.hand, -3 * TAU, about_point=sw[0].get_center(),
                                              run_time=1.6, rate_func=linear)))

        # S01.6
        wish1 = CurvedArrow(you.get_top() + UP * 0.1, family.get_top() + UP * 0.1 + LEFT * 0.2, angle=-1.2, color=TEXT)
        wish2 = CurvedArrow(family.get_top() + UP * 0.9 + RIGHT * 0.3, you.get_top() + UP * 0.85 + RIGHT * 0.1, angle=1.2, color=DIM)
        for a in (wish1, wish2):
            a.set_stroke(opacity=0.9)
        wish = VGroup(DashedVMobject(wish1, num_dashes=18), DashedVMobject(wish2, num_dashes=18))
        wish.set_stroke(width=3)
        self.play(FadeOut(sw), run_time=0.3)
        self.say("Everyone has felt this. And everyone has an instinct about what the store should do: "
                 "let the milk go first.",
                 prof.animate.shift(LEFT * 3.2),
                 after(3.5, FadeIn(wish, run_time=1.0), Wait(1.5), FadeOut(wish, run_time=0.8)))

        # S01.7
        inout = Text("In… Out…", font_size=24, color=DIM).next_to(stu, UP, buff=0.15)
        self.say("The book's advice, by the way, is to take a long, deep breath. In. Out. It will be okay.",
                 FadeIn(inout),
                 Succession(*[ScaleInPlace(stu, 1.05, rate_func=there_and_back, run_time=1.4) for _ in range(2)]))
        self.play(FadeOut(inout), run_time=0.4)

        # S01.8
        self.say("Now: that line is a scheduler, and the store just made a policy decision. Let's see how good it was.",
                 FadeIn(spot, shift=DOWN * 0.3), FadeIn(tag))
        self.beat(1.0)
        carton.clear_updaters()
