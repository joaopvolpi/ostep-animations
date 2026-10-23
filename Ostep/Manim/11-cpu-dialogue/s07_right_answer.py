import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403

FIFO = ["rr....", "wwrr..", "wwwwrr"]
RR = ["rwwrww", "wrwwrw", "wwrwwr"]
SEE_AT = P3(-1.6, 1.1)


class S07RightAnswer(Ep11Scene):
    def construct(self):
        self.world(stu="excited", prof="neutral", mode="corner")
        stu, prof = self.stu, self.prof
        old = build_s06_end()
        thumb = hand_icon(0.45, COMPUTER_COLOR).move_to(stu.get_top() + UP * 0.5)
        self.add(old, thumb)

        see = Seesaw(width=3.2, left="turnaround", right="response").move_to(SEE_AT)
        see.left_pan.label.set_color(COL["A"]) if hasattr(see.left_pan, "label") else None
        see.right_pan.label.set_color(COL["B"]) if hasattr(see.right_pan, "label") else None
        q = question_mark(1.2, CPU_COLOR).move_to(P3(0, 0.8))
        left_strip = sched_strip(FIFO, -4.0, -0.2)
        right_strip = sched_strip(FIFO, -1.2, -0.2)

        # S07.1
        self.say("These policy battles could rage forever. Is there really a right answer?",
                 FadeOut(old), FadeOut(thumb), FadeIn(q), stu.change("confused"), min_time=4.0)

        # S07.2
        self.say("Probably not.", q.animate.scale(0.3).move_to(SEE_AT + DOWN * 0.3), prof.change("thinking"), min_time=2.0)

        # S07.3
        self.say("Even our own metrics are at odds.", FadeOut(q), FadeIn(see), min_time=2.5)

        # S07.4
        tick = tick_mark(0.3, GREEN_OK, 6)
        xm = x_mark(0.3)
        tick.move_to(see.left_pan[0].get_center() + UP * 0.55 + LEFT * 0.8)
        with self.narrate("A scheduler that's good at turnaround time is bad at response time, and vice versa.", min_time=9.0):
            self.play(see.tilt(12), FadeIn(left_strip), FadeIn(right_strip), run_time=1.0)
            xm.move_to(right_strip.get_right() + RIGHT * 0.35)
            self.play(FadeIn(tick), FadeIn(xm), run_time=0.5)
            self.wait(1.2)
            self.play(see.tilt(-12), FadeOut(tick), FadeOut(xm), run_time=0.9)
            self.play(Transform(left_strip[1], sched_strip(RR, -4.0, -0.2)[1]),
                      Transform(right_strip[1], sched_strip(RR, -1.2, -0.2)[1]), run_time=1.0)
            tick2 = tick_mark(0.3, GREEN_OK, 6).move_to(right_strip.get_right() + RIGHT * 0.35)
            xm2 = x_mark(0.3).move_to(left_strip.get_right() + RIGHT * 0.3)
            self.play(FadeIn(tick2), FadeIn(xm2), run_time=0.5)
            self.wait(0.8)
            self.play(FadeOut(tick2), FadeOut(xm2), run_time=0.4)

        # S07.5
        card = TipCard(body="Don't find the best. Avoid disaster.", title="LAMPSON", width=3.4, font_size=24,
                       accent=VIRT).move_to(P3(4.2, 0.9))
        ring = Circle(radius=0.4, color=GREEN_OK).set_stroke(GREEN_OK, 4).move_to(see.pivot.get_center() + DOWN * 0.2)
        self.say("As Lampson said, perhaps the goal isn't to find the best solution, but to avoid disaster.",
                 card.slide_in(), Succession(Wait(1.0), see.tilt(0), Create(ring)), min_time=6.0)

        # S07.6
        self.say("That's a little depressing.", stu.change("sad"), see.tilt(-5), min_time=2.2)

        # S07.7
        l_pt, r_pt = see.left_pan[0].get_center(), see.right_pan[0].get_center()
        self.say("Good engineering can be that way. It can also be uplifting.", prof.change("happy"),
                 Succession(see.tilt(8), see.tilt(-8), see.tilt(0),
                            AnimationGroup(Flash(see.left_pan[0].get_center() + UP * 0.3, color=CPU_COLOR, run_time=0.5),
                                           Flash(see.right_pan[0].get_center() + UP * 0.3, color=CPU_COLOR, run_time=0.5))),
                 min_time=4.5)

        # S07.8
        self.say("I think being pragmatic is a good thing: not every problem has a clean, easy solution.",
                 prof.change("explaining"), stu.change("neutral"), min_time=5.5)
        self.beat(1.0)
