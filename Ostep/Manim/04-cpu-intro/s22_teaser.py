import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


class S22Teaser(Ep04Scene):
    def construct(self):
        recap = VGroup(recap_header(), recap_lines())   # S21 end state (icons omitted)
        self.add(recap)

        # S22.1
        stu = student_dialogue("curious")
        prof = prof_dialogue("neutral")
        stu.shift(LEFT * 5)
        prof.shift(RIGHT * 5)
        p = proc("A").move_to(P3(0, 1.2))
        with self.narrate("Okay, I'm convinced processes exist. But how do I actually make one? From my own code?"):
            self.play(FadeOut(recap), stu.animate.shift(RIGHT * 5), prof.animate.shift(LEFT * 5), run_time=1.0)
            self.play(GrowFromCenter(p), stu.change("curious", look_at=P3(0, 1.2)), run_time=0.7)

        # S22.2
        calls = VGroup(*[Text(s, font=MONO_FONT, font_size=34, color=TEXT) for s in ("fork()", "exec()", "wait()")])
        calls.arrange(RIGHT, buff=0.7).move_to(P3(0, 2.75))
        with self.narrate("With three of the strangest and most elegant calls in computing: fork(), exec() and wait()."):
            self.play(prof.change("happy", look_at=p), run_time=0.6)
            self.wait(1.6)
            for c in calls:
                self.play(FadeIn(c, shift=DOWN * 0.2), run_time=0.5)

        # S22.3
        left = p.copy()
        right = p.copy()
        with self.narrate("A process that clones itself…"):
            self.play(p.animate.stretch(1.35, 0).stretch(0.85, 1), run_time=0.4)
            self.remove(p)
            self.add(left, right)
            self.play(left.animate.shift(LEFT * 0.9), right.animate.shift(RIGHT * 0.9),
                      stu.change("surprised", look_at=P3(0, 1.2)), run_time=0.7)
            self.play(left.blink(), right.blink())
            self.wait(0.6)
            self.play(left.blink(), right.blink())
        self.wait(0.6)

        # S22.4
        dot = Dot(radius=0.1, color=VIRT)
        nxt = Text("Next: 05 · The Process API", font_size=40, color=TEXT)
        card = VGroup(dot, nxt).arrange(RIGHT, buff=0.25)
        with self.narrate("Next time."):
            self.play(*[FadeOut(m) for m in (stu, prof, left, right, calls)], run_time=0.5)
            self.play(FadeIn(card, shift=UP * 0.2), run_time=0.6)
        self.wait(2.0)
