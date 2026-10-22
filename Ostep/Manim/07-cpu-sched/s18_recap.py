import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403

LINES = [
    "A policy picks which process runs next, and metrics let us compare policies.",
    "Turnaround time measures completion; response time measures how soon a job first runs.",
    "FIFO, SJF and STCF are good for turnaround; SJF and STCF fix the convoy.",
    "Round Robin is good for response time and bad for turnaround: a fundamental trade-off.",
    "Overlapping I/O with computation raises utilization, but the OS can't see the future.",
]
NARR = [
    "A policy decides which process runs next, and we compare policies using metrics.",
    "Turnaround time measures completion; response time measures how soon a job first runs.",
    "FIFO, SJF and STCF are good for turnaround; SJF and STCF fix the convoy.",
    "Round Robin is good for response time and bad for turnaround. That's a fundamental trade-off.",
    "Overlapping I/O with computation raises utilization, but the OS can't see the future.",
]


def icon(k):
    if k == 0:
        sp = Spotlight(height=0.6, spread=0.25)
        tray = Line(LEFT * 0.7, RIGHT * 0.7).set_stroke(DIM, 3)
        ps = VGroup(*[proc(n, scale=0.2) for n in "ABC"]).arrange(RIGHT, buff=0.12)
        ps.next_to(tray, UP, buff=0.02)
        sp.move_beam_to(ps[0].get_bottom())
        return VGroup(tray, ps, sp)
    if k == 1:
        a = Line(LEFT * 0.8, RIGHT * 0.8).set_stroke(TEXT, 3)
        ca = VGroup(*[Line(UP * 0.07, DOWN * 0.07).move_to(a.get_end() if s else a.get_start()) for s in (0, 1)]).set_stroke(TEXT, 3)
        b = DashedLine(LEFT * 0.8, LEFT * 0.1, dash_length=0.07).set_stroke(INTRO, 3).shift(DOWN * 0.3)
        return VGroup(a, ca, b)
    if k == 2:
        return VGroup(Rectangle(width=0.9, height=0.25).set_fill(COL["A"], 1).set_stroke(TEXT, 1),
                      Rectangle(width=0.25, height=0.25).set_fill(COL["B"], 1).set_stroke(TEXT, 1),
                      Rectangle(width=0.25, height=0.25).set_fill(COL["C"], 1).set_stroke(TEXT, 1)).arrange(RIGHT, buff=0.05)
    if k == 3:
        beam = Line(LEFT * 0.8, RIGHT * 0.8).set_stroke(TEXT, 5).rotate(0.2)
        return VGroup(beam, Triangle().scale(0.15).set_fill(DIM, 1).set_stroke(width=0).next_to(beam, DOWN, buff=0.0))
    ball = CrystalBall(0.22)
    ball.crack_mob.set_stroke(TEXT, 3, opacity=1).pointwise_become_partial(ball.crack_full, 0, 1)
    lanes = VGroup(*[Line(LEFT * 0.7, RIGHT * 0.7).set_stroke(c, 5) for c in (CPU_COLOR, DISK_COLOR)]).arrange(DOWN, buff=0.15)
    return VGroup(lanes, ball.next_to(lanes, RIGHT, buff=0.3))


class S18Recap(Ep07Scene):
    def construct(self):
        self.world(opened=(0, 1, 2, 3), stu="neutral", prof="explaining", strip=False)
        stu, prof = self.stu, self.prof
        head = Text("Recap", font_size=44, color=VIRT, weight=BOLD).move_to(P3(-6.2, 2.85), aligned_edge=LEFT)
        lines = VGroup(*[Text(wrap_text(s, 7.8, 26), font_size=26, color=TEXT, line_spacing=0.75) for s in LINES])
        lines.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(P3(-6.2, 2.25), aligned_edge=UL)
        if lines.get_bottom()[1] < -2.0:
            lines.scale_to_fit_height(4.2).move_to(P3(-6.2, 2.25), aligned_edge=UL)
        icons = [icon(k).move_to(P3(4.9, lines[k].get_center()[1])) for k in range(5)]

        # S18.1
        self.say("So, today:", Write(head), prof.change("happy"))
        # S18.2 - S18.6
        for k in range(5):
            extra = []
            if k == 4:
                extra = [prof.change("proud")]
            self.say(NARR[k], Write(lines[k]), FadeIn(icons[k], shift=LEFT * 0.3), *extra)
        self.beat(1.5)
        self.play(FadeOut(self.badge), run_time=0.5)
