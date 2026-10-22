import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


class S01ProgramTalksToItself(Ep05Scene):
    def construct(self):
        # S01.1
        p = proc(PAR).move_to(P3(0, 1.0))
        self.wait(0.1)
        with self.narrate("Last time, we ended with a promise: a process that clones itself."):
            self.play(GrowFromCenter(p), run_time=0.6)
            self.play(p.blink())
            clone, anim = clone_process(p)
            self.add(clone)
            self.play(anim)
            self.play(p.animate.shift(LEFT * 8), clone.animate.shift(RIGHT * 8), run_time=1.0)
        self.remove(p, clone)

        # S01.2
        walker = p1_walker().move_to(P3(-3.6, 0.5))
        stu = student_corner("curious")
        prof = prof_corner("neutral")
        with self.narrate("So let's see it. Here is a tiny C program."):
            self.play(walker.write_in(2.2), FadeIn(stu), FadeIn(prof))
            self.play(FadeIn(walker.caption), run_time=0.4)

        # S01.3
        bar = walker.add_bar(TEXT, 1, opacity=0.2)
        self.say('It prints "hello".', FadeIn(bar), min_time=1.8)

        # S01.4
        with self.narrate('Then it hits an if and an else. If it\'s the child, print "child". '
                          'Otherwise, print "parent".'):
            self.play(walker.move_bar(0, 3, 0.6))
            self.wait(0.6)
            self.play(walker.indicate(4), run_time=0.8)
            self.wait(0.4)
            self.play(walker.indicate(6), run_time=0.8)
            self.wait(0.4)

        # S01.5
        term = mk_term(5.0, 4, 18).move_to(P3(3.2, 0.7))
        with self.narrate("Let's run it."):
            self.play(FadeIn(term), FadeOut(bar), run_time=0.5)
            self.play(term.type("./p1"))
            for line in P1_OUT:
                self.play(term.print(line, run_time=0.3))
                self.wait(0.2)

        # S01.6
        q = question_mark(0.5).next_to(stu, UP, buff=0.05)
        q2 = question_mark(0.45).move_to(P3(-1.0, 0.5) + RIGHT * 0.0)
        with self.narrate('Wait. "Hello" appeared once. But then both "child" and "parent" showed up. '
                          "That's an if and an else. How can both of them run?"):
            self.play(stu.change("confused", look_at=term), FadeIn(q, scale=0.5), run_time=0.8)
            self.play(Indicate(term.lines[2], color=CPU_COLOR), Indicate(term.lines[3], color=CPU_COLOR),
                      run_time=1.0)
            fl4, fl6 = walker.bars, None
            b4 = walker.add_bar(PAR, 4, opacity=0.3)
            b6 = walker.add_bar(CHI, 6, opacity=0.3)
            self.play(FadeIn(b4), FadeIn(b6), FadeIn(q2.move_to(walker.line_point(5, "right") + RIGHT * 0.4)),
                      run_time=0.6)
            self.wait(1.0)
            self.play(FadeOut(b4), FadeOut(b6), FadeOut(q2), run_time=0.4)

        # S01.7
        with self.narrate("Because after one particular line, there are two of the program."):
            self.play(prof.change("happy", look_at=walker), FadeOut(q), run_time=0.6)
            self.play(walker.circumscribe(2), run_time=1.2)
            self.wait(0.5)
        self.play(FadeOut(walker.bars[0]), run_time=0.3)

        # S01.8
        calls = VGroup(*[mono(s, 34) for s in ("fork()", "exec()", "wait()")]).arrange(RIGHT, buff=0.7)
        calls.move_to(P3(0, 3.1))
        with self.narrate("Today we meet the three calls UNIX uses to make and manage processes."):
            self.play(LaggedStart(*[Write(c) for c in calls], lag_ratio=0.3), run_time=1.8)
            self.wait(0.5)
            self.play(FadeOut(calls), run_time=0.5)
