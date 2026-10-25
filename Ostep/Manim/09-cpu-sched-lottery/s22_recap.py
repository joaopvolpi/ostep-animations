import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403

LINES = [
    "A proportional-share scheduler promises each job a share, instead of minimizing a time.",
    "Lottery scheduling uses tickets and a random draw. Simple, cheap, and fair in the long run.",
    "Stride scheduling uses strides and pass values to get the shares exactly right.",
    "CFS runs the process with the lowest vruntime, with a time slice from sched_latency, bounded by min_granularity, "
    "and scaled by nice weights.",
    "CFS keeps runnable processes in a red-black tree, so finding the next one is fast even with thousands.",
]
SAY = [
    "A proportional-share scheduler promises each job a share, instead of minimizing a time.",
    "Lottery scheduling uses tickets and a random draw. Simple, cheap, and fair in the long run.",
    "Stride scheduling uses strides and pass values to get the shares exactly right.",
    "CFS runs the process with the lowest vruntime, with a time slice from sched_latency, bounded by min_granularity, "
    "and scaled by nice weights.",
    "CFS keeps runnable processes in a red-black tree, so finding the next one is fast even with thousands.",
]


def icon(i):
    if i == 0:
        return TargetPie((0.75, 0.25), radius=0.35, label=None)
    if i == 1:
        return VGroup(RaffleDrum(0.6), Ticket(COL["A"]).scale(1.2).shift(RIGHT * 0.9 + DOWN * 0.1))
    if i == 2:
        g = VGroup()
        for k, c in enumerate((COL["A"], COL["B"], COL["C"])):
            g.add(Line(P3(-0.6, -0.25 * k), P3(0.6, -0.25 * k)).set_stroke(DIM, 2))
            g.add(Rectangle(width=0.15 + 0.2 * (3 - k), height=0.1).set_fill(c, 1).set_stroke(width=0)
                  .move_to(P3(-0.6 + (0.15 + 0.2 * (3 - k)) / 2, -0.25 * k - 0.1)))
        return g.move_to(ORIGIN)
    if i == 3:
        return VGroup(VruntimeMeter(COL["A"], 0.8, 0.22, level=0.7), VruntimeMeter(COL["B"], 0.8, 0.22, level=0.3)).arrange(RIGHT, buff=0.2)
    t = RBTree(at=(0, 0), dx=0.2, dy=0.28, radius=0.09, font_size=8)
    for nd in t.nodes.values():
        nd.remove(nd[1])      # labels would not fit inside the tiny circles
    return t.scale(1.0)


class S22Recap(Ep09Scene):
    def construct(self):
        self.world(strip=False, chars=False)
        head = Text("Recap", font_size=44, color=VIRT, weight=BOLD).move_to(P3(-6.2, 2.3), aligned_edge=LEFT)
        lines = VGroup(*[Text(wrap_text(s, 8.8, 24), font_size=24, color=TEXT, line_spacing=0.75) for s in LINES])
        lines.arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(P3(-6.2, 1.8), aligned_edge=UL)
        self.say("So, today:", Write(head))
        for i in range(5):
            ic = icon(i)
            ic.move_to(P3(5.0, lines[i].get_center()[1]))
            self.say(SAY[i], FadeIn(lines[i], shift=RIGHT * 0.3), FadeIn(ic, scale=0.8))
        self.beat(1.5)
        self.play(FadeOut(self.badge), run_time=0.6)
