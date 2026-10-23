import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


def lad_icon():
    g = VGroup(*[Rectangle(width=1.2, height=0.2).set_fill(DIM, 0.15).set_stroke(DIM, 1.5).shift(DOWN * 0.26 * i) for i in range(3)])
    g[0].set_stroke(CPU_COLOR, 3).set_fill(CPU_COLOR, 0.2)
    return g.move_to(ORIGIN)


class S17Recap(Ep08Scene):
    def construct(self):
        self.build(lanes=3, cpu=True, ticks=20, rules=("R1", "R2", "R3", "R4", "R5"), stu="neutral", prof="proud", term="advice")
        lad, cpu = self.ladder, self.cpu
        tags = VGroup(tag_chip("BSD UNIX", TEXT, 20).move_to(P3(0.9, 2.3)), tag_chip("Solaris", TEXT, 20).move_to(P3(2.45, 2.3)),
                      tag_chip("Windows NT", TEXT, 20).move_to(P3(1.7, -0.25)))
        self.add(tags)
        world = VGroup(lad, cpu, self.tl, self.board, tags, self.terms.docked)

        # S17.1
        hdr = label("Recap", 34, VIRT, weight=BOLD).move_to(P3(-5.6, 2.3), aligned_edge=LEFT)
        self.say("So, today:", FadeOut(world), self.prof.change("neutral"), Succession(Wait(0.6), Write(hdr)))

        ys = (1.5, 0.7, -0.1, -0.9, -1.7)
        texts = ["Several queues, highest first", "Learn from history", "Quick to give up the CPU = stays high",
                 "Boost + accounting = fair and safe", "Knobs need tuning"]
        lines = [label(f"{i + 1}. {t}", 28, TEXT).move_to(P3(-5.6, y), aligned_edge=LEFT) for i, (t, y) in enumerate(zip(texts, ys))]
        # icons
        i1 = lad_icon()
        i2 = VGroup(history_clock(0.28), job("A", 0.3).shift(RIGHT * 0.9 + DOWN * 0.1)).arrange(RIGHT, buff=0.3)
        i3 = VGroup(job("B", 0.4), keyboard_icon(0.5)).arrange(RIGHT, buff=0.2)
        i4 = VGroup(Arrow(DOWN * 0.3, UP * 0.3, buff=0, color=PERS, stroke_width=5), Padlock(0.4)).arrange(RIGHT, buff=0.3)
        i5 = Dial(0.4, "S", 0.6)
        icons = [i1, i2, i3, i4, i5]
        for ic, y in zip(icons, ys):
            if ic is i5:
                ic.shift(P3(4.0, y + 0.1) - ic.hub.get_center())
            else:
                ic.move_to(P3(4.0, y))
        scripts = [
            "MLFQ uses several queues at different priority levels, and the CPU goes to the highest one.",
            "It doesn't know job lengths, so it learns from history: new jobs start at the top and sink as they use their allotment.",
            "Jobs that give up the CPU quickly keep a high priority, so interactive jobs stay snappy, and the scheduler approximates SJF.",
            "A priority boost stops starvation, and better accounting stops gaming.",
            "Every knob, the number of queues, the slice lengths, S, takes tuning, and none has an obvious best value.",
        ]
        for k in range(5):
            self.say(scripts[k], Write(lines[k]), FadeIn(icons[k], shift=LEFT * 0.3), min_time=2.0)
        self.beat(1.2)
        self.play(FadeOut(self.badge), run_time=0.5)
