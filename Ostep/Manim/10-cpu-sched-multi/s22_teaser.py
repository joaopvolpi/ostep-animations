import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common_more import *  # noqa: E402,F401,F403
from s21_recap import ITEMS, ITEM_Y, icons  # noqa: E402


class S22Teaser(Ep10Scene):
    def construct(self):
        stu, prof = student_corner("neutral"), prof_corner("proud")
        head = label("Recap", 36, VIRT).move_to(P3(-4.0, 2.25))
        texts = []
        for (s, _), y in zip(ITEMS, ITEM_Y):
            t = Text(s, font_size=24, color=TEXT, line_spacing=0.8)
            t.move_to(P3(-4.6, y), aligned_edge=LEFT)
            texts.append(t)
        icos = icons()
        for ic, y in zip(icos, ITEM_Y):
            ic.move_to(P3(4.2, y))
        listing = VGroup(head, *texts, *icos)
        self.add(listing, stu, prof)

        # S22.1 dialogue mode
        stu_d = Student("curious").move_to(P3(-2.6, -1.2))
        prof_d = Professor("happy").flip().move_to(P3(2.6, -1.2))
        self.say("So after all this, we know how to schedule on one CPU, and on many. What's left?",
                 FadeOut(listing), Transform(stu, stu_d), Transform(prof, prof_d))
        stu.set_expression("curious")

        # S22.2
        chip = CPU(size=0.9, label="CPU").move_to(P3(-0.8, 0.5))
        ribbon = VGroup(tick_mark(0.25), label("CPU virtualized", 20, GREEN_OK)).arrange(RIGHT, buff=0.1).next_to(chip, DOWN, buff=0.25)
        self.say("One more short conversation, to pull the whole virtualization of the CPU together.",
                 prof.change("happy"), FadeIn(chip, scale=0.6), Succession(Wait(1.5), FadeIn(ribbon, shift=UP * 0.1)))

        # S22.3
        mem = Memory(cells=4, width=0.9, height=1.4, addresses=False).move_to(P3(1.3, 0.5))
        self.say("And then we leave the CPU behind, and virtualize memory.", FadeIn(mem, shift=LEFT * 0.6))

        # S22.4
        part2 = tag("Part 2", 22, CONC).move_to(P3(5.4, 2.0))
        pad = Padlock(0.5).move_to(P3(-5.0, 1.2))
        th = make_thread("T", COL["A"], 0.6).move_to(P3(-4.0, 1.0))
        self.say("But we will meet those locks again. Much of this chapter said we'll see later.",
                 FadeOut(VGroup(chip, ribbon, mem)), FadeIn(part2), FadeIn(pad), FadeIn(th))

        # S22.5
        with self.narrate("Later is the concurrency section: threads, locks, and what they cost. "
                          "Next: the CPU virtualization dialogue."):
            self.play(hop_to(pad, part2.get_left() + LEFT * 0.5, anchor="center", run_time=1.2, height=1.0),
                      hop_to(th, part2.get_left() + LEFT * 1.3 + DOWN * 0.3, run_time=1.2, height=1.2), run_time=1.3)
            self.wait(1.5)
        self.play(FadeOut(VGroup(stu, prof, pad, th, part2)), run_time=0.8)
        dot = Dot(radius=0.12, color=VIRT)
        nxt = label("Next: 11 · Summary Dialogue", 36, TEXT)
        card = VGroup(dot, nxt).arrange(RIGHT, buff=0.3).move_to(ORIGIN)
        self.play(FadeIn(card), run_time=0.8)
        self.wait(2.0)
