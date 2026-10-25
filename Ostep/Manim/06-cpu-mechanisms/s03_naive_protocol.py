import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


class S03NaiveProtocol(Ep06Scene):
    def construct(self):
        self.add_badge()
        self.add_docked_term("limited direct execution")
        st = strip(CRUX_Q1)
        self.add(st)
        stu, prof = corner_chars(True, "curious", "explaining")
        self.add(stu, prof)
        chart = make_s03_chart()
        self.add(chart)

        # S03.1
        self.say("Here's direct execution as a protocol.", chart.draw(1.2))

        # S03.2
        self.say("The OS creates a process entry, allocates memory, loads the program (that's the work behind "
                 "exec() from last time), sets up the stack, clears the registers…",
                 Succession(*[s03_write(chart, i, run_time=1.4) for i in range(5)]))

        # S03.3
        self.say("…and calls main().",
                 s03_write(chart, 5, 1.0))
        # S03.4
        self.say("The program runs, and returns.",
                 Succession(s03_write(chart, 6, 0.8), chart.link(5, 6, run_time=0.8), s03_write(chart, 7, 0.8)))
        # S03.5
        self.say("The OS frees the memory and removes the entry.",
                 Succession(s03_write(chart, 8, 1.0), chart.link(7, 8, run_time=0.6), s03_write(chart, 9, 1.0)))
        self.beat(1.0)

        # S03.6
        self.say("That's just calling a function.", stu.change("curious"),
                 Succession(Indicate(chart.arrows[0], color=CPU_COLOR), Indicate(chart.arrows[1], color=CPU_COLOR)))

        # S03.7
        fast = tag("FAST", GREEN_OK, 24).move_to(P3(3.2, 1.55))
        self.say("Exactly, which is why it's so fast.", prof.change("explaining"), FadeIn(fast, scale=1.3))

        # S03.8
        n1, n2 = numeral(1).move_to(P3(6.15, 1.5)), numeral(2).move_to(P3(6.15, 0.3))
        icon_a = proc("A", "ready", scale=0.45).move_to(P3(6.1, -1.0))
        bang = Text("!", font_size=44, color=RED_BAD, weight=BOLD).next_to(icon_a, UP, buff=0.0)
        self.say("But it raises two problems. One: how do we stop the program from doing what we don't want, "
                 "while still running it efficiently?",
                 prof.change("worried"),
                 Succession(AnimationGroup(FadeIn(n1, scale=1.4), FadeIn(n2, scale=1.4)),
                            Indicate(n1, color=VIRT), FadeIn(icon_a), FadeIn(bang, scale=1.5)))

        # S03.9
        self.play(FadeOut(icon_a), FadeOut(bang), run_time=0.4)
        icon_cpu = CPU(0.5, label=None, pins=2).move_to(P3(6.1, -0.6))
        wall = Rectangle(width=0.08, height=0.6).set_fill(USER_COLOR, 0.4).set_stroke(USER_COLOR, 2).move_to(P3(6.1, -1.3))
        ib = proc("B", "ready", scale=0.3).next_to(wall, DOWN, buff=0.02)
        self.say("Two: how does the OS stop it, to switch to another process?",
                 AnimationGroup(Indicate(n2, color=VIRT), FadeIn(icon_cpu), FadeIn(wall), FadeIn(ib)))
        self.beat(1.0)
