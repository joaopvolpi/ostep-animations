import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


class S04ParanoidOs(Ep11Scene):
    def construct(self):
        self.world(stu="curious", prof="explaining", mode="corner", term="mechanisms")
        stu, prof = self.stu, self.prof
        panels, term = build_s03_end(self)
        self.add(panels)

        bd = make_boundary()
        gauge = PrivilegeGauge(height=1.3, level="user").move_to(GAUGE_AT)
        cpu = CPU(size=0.9).move_to(CPU_AT)
        pa = proc("A", "running", scale=0.6, label=None)
        feet_to(pa, cpu.slot_point())
        eye = EyeIcon(width=0.9, iris=KERNEL_COLOR).move_to(P3(-0.8, -1.2))

        # S04.1
        self.say("Did you get a sense of the philosophy of the OS?",
                 FadeOut(term), FadeOut(panels), bd.draw(1.4),
                 Succession(Wait(0.6), AnimationGroup(FadeIn(cpu), FadeIn(pa), FadeIn(gauge))),
                 prof.change("thinking"))

        # S04.2
        self.say("I think so. The OS is fairly paranoid.", stu.change("neutral"), FadeIn(eye),
                 Succession(Wait(1.2), eye.look_at(P3(-3.0, -1.2)), eye.look_at(P3(2.5, -1.2)), eye.look_at(P3(-0.8, -1.2))))

        # S04.3
        ring = Circle(radius=0.85, color=KERNEL_COLOR).set_stroke(KERNEL_COLOR, 5).move_to(cpu)
        self.say("It wants to stay in charge.", eye.look_at(cpu),
                 Succession(Wait(0.4), Create(ring), Indicate(ring, scale_factor=1.15, color=KERNEL_COLOR), FadeOut(ring)))

        # S04.4
        speed = SpeedGauge(value=0.2, width=1.4, color=CPU_COLOR).move_to(P3(-0.2, 1.25))
        self.say("It wants a program to run as efficiently as possible, and hence limited direct execution.",
                 Succession(self.term("limited direct execution"), FadeIn(speed),
                            AnimationGroup(*[Transform(a, b) for a, b in zip((speed.bar, speed.label), speed.value_targets(1.0))],
                                           run_time=1.2)))

        # S04.5
        D = proc("D", "running", scale=0.6, label=None)
        rect = SurroundingRectangle(D, color=RED, buff=0.04, corner_radius=0.1)
        rogue = VGroup(D, rect)
        feet_to(D, P3(1.7, BOUND_Y + 0.1))
        rect.move_to(D)
        clock = AlarmClock(radius=0.3, boxed=False, label="").move_to(P3(3.2, 1.4))
        hand = hand_icon(0.7).rotate(-PI / 2).move_to(P3(2.6, -0.2))
        self.say("But it also wants to say \"Ah! Not so fast, my friend\" to an errant or malicious process.",
                 FadeOut(speed), FadeIn(rogue),
                 Succession(Wait(1.0), hop_to(rogue, P3(1.7, BOUND_Y - 0.6), anchor="center", run_time=0.6),
                            AnimationGroup(FadeIn(clock), clock.ring(), FadeIn(hand, shift=LEFT * 0.4), run_time=0.9),
                            hop_to(rogue, P3(0.6, BOUND_Y + 0.9), anchor="center", run_time=0.6)),
                 Succession(Wait(3.8), stu.says("Not so fast!", expression="excited")),
                 min_time=7.0)

        # S04.6
        with self.narrate("Paranoia rules the day.", min_time=2.0):
            self.play(stu.remove_bubble(), Indicate(eye, scale_factor=1.3), gauge.set_level("kernel", run_time=0.4))
            self.wait(0.4)
            self.play(gauge.set_level("user", run_time=0.4))

        # S04.7
        stack, procs = make_stack()
        self.play(FadeOut(rogue), FadeOut(clock), FadeOut(hand), FadeOut(eye), FadeOut(cpu), FadeOut(pa),
                  bd.animate.set_opacity(0.3), run_time=0.6)
        self.say("Perhaps that's why we think of the OS as a resource manager.",
                 Succession(self.terms.note("resource manager"), FadeIn(stack), FadeIn(procs),
                            Indicate(stack.band, scale_factor=1.03, color=KERNEL_COLOR)),
                 stu.change("curious"))

        # S04.8
        puzzle = puzzle_piece(0.5).move_to(P3(4.2, -0.9))
        self.say("Yes indeed. You're starting to put it together.", prof.change("proud"), GrowFromCenter(puzzle))
        self.beat(1.0)
