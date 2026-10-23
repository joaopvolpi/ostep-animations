"""Preview sheet for the episode-10 props.

    python -m manim -ql -s ostep_lib/props/p10_preview.py P10PropSheet
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from manim import *  # noqa: E402,F401
from ostep_lib import *  # noqa: E402,F401


def cap(text, mob, direction=DOWN):
    return Text(text, font_size=16, color=DIM).next_to(mob, direction, buff=0.1)


class P10PropSheet(Scene):
    def construct(self):
        apply_style(self)
        cA, cB, cC, cD = PROCESS_COLORS[:4]
        c1 = CacheCPU("CPU 0").move_to([-4.8, 2.0, 0])
        c1.store("7", cA); c1.store("9", cA)
        c2 = CacheCPU("CPU 1").move_to([-2.0, 2.0, 0])
        self.add(c1, c2, cap("CacheCPU (2 filled / empty)", c1, DOWN).shift(RIGHT * 1.4 + DOWN * 0.3))
        eyes = VGroup(EyeIcon(0.6), EyeIcon(0.6), EyeIcon(0.6, opened=False))
        eyes[0].set_look([3, 0, 0]); eyes[1].set_look([-3, 1, 0])
        eyes.arrange(RIGHT, buff=0.4).move_to([2.0, 2.3, 0])
        self.add(eyes, cap("EyeIcon (right, left-up, closed)", eyes))
        icons = VGroup(suitcase_icon(), pin_icon(), flame_icon(), hand_up_icon()).arrange(RIGHT, buff=0.5)
        icons.move_to([4.8, 0.8, 0]).scale(1.0)
        self.add(icons, cap("suitcase, pin, flame, hand", icons))
        g = ScheduleGrid(4, 5, colors={"A": cA, "B": cB, "C": cC, "D": cD}, repeat_label=True).move_to([-2.4, -1.3, 0])
        for r, row in enumerate(["AEDCB", "BAEDC", "CBAED", "D.BAE"]):
            g.set_row(r, row)
        self.add(g, cap("ScheduleGrid", g, UP))
        bus = Bus(y=-1.0, x_range=(1.5, 6.5))
        self.add(bus, cap("Bus (+ bus_pulse)", bus, UP))
