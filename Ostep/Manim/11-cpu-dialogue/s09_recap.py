import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403

LINES = ["1. Mechanisms: control, at full speed", "2. The OS is paranoid on purpose",
         "3. Policies trade goals off", "4. Aim to avoid disaster"]
NARR = ["One: mechanisms give the OS control while programs run at full speed.",
        "Two: the OS is paranoid on purpose.",
        "Three: policies trade one goal against another.",
        "Four: sometimes the aim is just to avoid disaster."]
YS = [1.4, 0.5, -0.4, -1.3]
ICON_X = 4.0


def icon(k):
    if k == 0:
        line = DashedLine(LEFT * 0.7, RIGHT * 0.7, dash_length=0.1).set_stroke(TEXT, 3)
        p = proc("A", "running", scale=0.3, label=None)
        place_on(p, line.get_center() + UP * 0.12 + LEFT * 0.2)
        ar = Arrow(UP * 0.35, DOWN * 0.35, buff=0, stroke_width=4, color=KERNEL_COLOR, tip_length=0.15).move_to(line.get_center() + RIGHT * 0.3)
        return VGroup(line, p, ar)
    if k == 1:
        return hand_icon(0.6, COMPUTER_COLOR)
    if k == 2:
        s = Seesaw(width=1.2)
        s.set_angle_now(10)
        return s
    s = Seesaw(width=1.2)
    ring = Circle(radius=0.25, color=GREEN_OK).set_stroke(GREEN_OK, 3).move_to(s.pivot.get_center() + DOWN * 0.1)
    return VGroup(s, ring)


def build_recap():
    head = Text("The CPU arc", font_size=34, color=VIRT, weight=BOLD).move_to(P3(-5.4, 2.25), aligned_edge=LEFT)
    lines = VGroup(*[Text(s, font_size=30, color=TEXT).move_to(P3(-5.4, y), aligned_edge=LEFT) for s, y in zip(LINES, YS)])
    icons = VGroup(*[icon(k).move_to(P3(ICON_X, YS[k])) for k in range(4)])
    return head, lines, icons


class S09Recap(Ep11Scene):
    def construct(self):
        self.world(stu="curious", prof="happy", mode="corner")
        stu, prof = self.stu, self.prof
        ladder = make_ladder()
        rack = VGroup(server_rack_icon(0.7, 1.1), label("EC2", 22, TEXT)).arrange(DOWN, buff=0.1).move_to(P3(4.6, 1.5))
        flame = Flame(0.8).move_to(stu.get_top() + UP * 0.55)
        flame.flicker()
        self.add(ladder, rack, flame)
        head, lines, icons = build_recap()

        # S09.1
        self.say("What do we carry out of the CPU section?", FadeOut(ladder), FadeOut(rack), FadeOut(flame),
                 Write(head), stu.change("neutral"), min_time=3.0)
        self.play(prof.change("neutral"), run_time=0.5)
        # S09.2-5
        for k in range(4):
            extra = [prof.change("proud")] if k == 3 else []
            self.say(NARR[k], Write(lines[k]), FadeIn(icons[k], shift=LEFT * 0.3), *extra, min_time=3.0)
        self.beat(1.5)
        self.play(FadeOut(self.badge), run_time=0.5)
