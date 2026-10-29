import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


class S03NoSubstitute(Ep11Scene):
    def construct(self):
        self.world(stu="curious", prof="happy", mode="corner", term="mechanisms")
        stu, prof = self.stu, self.prof
        panels = build_panels_end()
        self.add(panels)

        # S03.1
        q = question_mark(0.4).next_to(stu, UP, buff=0.05)
        self.say("It all seems a little complicated, though. How can I learn more?",
                 stu.change("confused"), FadeIn(q),
                 panels.animate(run_time=0.8).scale(0.5).move_to(P3(0, 1.85)), min_time=4.0)

        # S03.2
        term = Terminal(width=5.2, height=2.6, font_size=18, prompt="$").move_to(P3(0, -0.5))
        self.say("There's no substitute for doing.", prof.change("explaining"), FadeOut(q), FadeIn(term),
                 min_time=2.0)
        self.play(term.type("make test"))

        # S03.3
        with self.narrate("Do the class projects, and I bet by the end it will all make sense.", min_time=7.0):
            for name, part in (("trap handler ... ok", panels.left), ("timer ... ok", panels.mid),
                               ("switch ... ok", panels.right)):
                self.play(term.print(name), run_time=0.5)
                tick = tick_mark(0.18, GREEN_OK, 5)
                last = term.last_line()
                tick.next_to(last, RIGHT, buff=0.15)
                self.play(FadeIn(tick), Indicate(part, scale_factor=1.15, color=GREEN_OK), run_time=0.7)
                term.add(tick)
            self.play(stu.change("curious"), run_time=0.7)
            self.play(stu.animate.shift(DOWN * 0.15), run_time=0.4)
            self.play(stu.animate.shift(UP * 0.15), run_time=0.4)
