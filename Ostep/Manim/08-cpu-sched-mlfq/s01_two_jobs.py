import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


class S01TwoJobs(Ep08Scene):
    def construct(self):
        box_l = mystery_box(1.0).move_to(P3(-3.2, 1.7))
        box_r = mystery_box(1.0).move_to(P3(3.2, 1.7))
        spot = Spotlight(height=1.2, spread=0.6)
        spot.move_beam_to(P3(0, 1.2))

        # S01.1
        self.say("Two jobs just arrived at the scheduler.",
                 FadeIn(box_l, shift=DOWN * 1.2), FadeIn(box_r, shift=DOWN * 1.2), FadeIn(spot))

        # S01.2
        kb = keyboard_icon(0.7).move_to(P3(-3.7, 0.5))
        t_l = label("1 ms", 24, CPU_COLOR).move_to(P3(-2.85, 0.5))
        self.say("One of them is tiny: a keystroke, an echo on the screen, done in a blink.",
                 Indicate(box_l, scale_factor=1.2), Succession(Wait(0.8), FadeIn(kb, scale=1.3), FadeIn(t_l)))
        self.play(Transform(t_l, label("?", 28, CPU_COLOR).move_to(t_l)), run_time=0.5)

        # S01.3
        sw = stopwatch_icon(0.3).move_to(P3(2.55, 0.5))
        t_r = label("1 hour", 24, CPU_COLOR).move_to(P3(3.55, 0.5))
        self.say("The other will grind through numbers for an hour.",
                 box_r.animate.scale(1.6).move_to(P3(3.2, 1.8)),
                 Succession(Wait(0.8), FadeIn(sw, scale=1.3), FadeIn(t_r), Rotate(sw.hand, angle=-TAU, about_point=sw[0].get_center(), run_time=1.5)))
        self.play(Transform(t_r, label("?", 28, CPU_COLOR).move_to(t_r)), run_time=0.5)

        # S01.4
        self.say("From the outside, they look exactly the same.",
                 box_r.animate.scale(1 / 1.6).move_to(P3(3.2, 1.7)), FadeOut(spot))
        self.beat(1.0)

        # S01.5
        stu, prof = student_dlg("curious"), prof_dlg("thinking")
        sjf = tag_chip("SJF", TEXT, 26).move_to(P3(0, 1.9))
        self.say("Easy. Shortest job first, like last time.",
                 FadeIn(stu, shift=UP * 0.4), FadeIn(sjf, shift=DOWN * 0.2))

        # S01.6
        xm = x_mark(0.3).next_to(sjf, RIGHT, buff=0.15)
        need = label("needs job length?", 20, DIM).next_to(sjf, DOWN, buff=0.15)
        self.say("If we knew which one was which. SJF and STCF need each job's length in advance, and the OS almost never has it.",
                 FadeIn(prof, shift=UP * 0.4), FadeIn(xm, scale=1.4), FadeIn(need))

        # S01.7
        ring = rr_ring(0.3).move_to(P3(-0.9, 1.9))
        rrt = label("Round Robin", 26, TEXT).next_to(ring, RIGHT, buff=0.15)
        self.say("Fine. Round robin, then.",
                 FadeOut(VGroup(sjf, xm, need)), FadeIn(ring, scale=1.3), FadeIn(rrt), stu.change("frustrated"))

        # S01.8
        r_lab = label("response", 22, DIM).move_to(P3(-1.7, 0.85))
        r_arr = Arrow(P3(-0.6, 0.85), P3(1.6, 0.85), buff=0, color=PERS, stroke_width=4, max_tip_length_to_length_ratio=0.2)
        r_end = Arrow(P3(-0.6, 0.85), P3(-0.1, 0.85), buff=0, color=PERS, stroke_width=4, max_tip_length_to_length_ratio=0.4)
        tk = tick_mark(0.3).move_to(P3(0.3, 0.85))
        self.say("Round robin keeps response time low: the keyboard feels snappy.",
                 FadeIn(r_lab), Succession(Create(r_arr), Transform(r_arr, r_end)), Succession(Wait(1.2), FadeIn(tk, scale=1.3)),
                 prof.change("explaining"))

        # S01.9
        t_lab = label("turnaround", 22, DIM).move_to(P3(-1.7, 0.3))
        t_arr = Arrow(P3(-0.6, 0.3), P3(-0.2, 0.3), buff=0, color=KERNEL_COLOR, stroke_width=4, max_tip_length_to_length_ratio=0.5)
        t_long = Arrow(P3(-0.6, 0.3), P3(2.0, 0.3), buff=0, color=KERNEL_COLOR, stroke_width=4, max_tip_length_to_length_ratio=0.15)
        xm2 = x_mark(0.28).move_to(P3(2.4, 0.3))
        self.say("But it drags every job out, so turnaround time is awful.",
                 FadeIn(t_lab), FadeIn(t_arr), Succession(Wait(0.6), Transform(t_arr, t_long, run_time=1.6)),
                 Succession(Wait(2.4), FadeIn(xm2, scale=1.3)))

        # S01.10
        self.play(FadeOut(VGroup(r_lab, r_arr, tk, t_lab, t_arr, xm2, ring, rrt)), run_time=0.5)
        sjf2 = tag_chip("SJF", TEXT, 24).move_to(P3(-1.5, 1.9))
        xs = x_mark(0.28).next_to(sjf2, RIGHT, buff=0.12)
        rr2 = tag_chip("RR", TEXT, 24).move_to(P3(1.2, 1.9))
        half = VGroup(tick_mark(0.24), x_mark(0.22)).arrange(RIGHT, buff=0.08).next_to(rr2, RIGHT, buff=0.12)
        self.say("So we're stuck.",
                 FadeIn(sjf2), FadeIn(xs), FadeIn(rr2), FadeIn(half), stu.change("confused"))

        # S01.11
        hist = history_clock(0.5).scale(1.3).move_to(P3(0, 1.5))
        self.say("Not stuck. We can't see the future. But we can watch the past.",
                 FadeOut(VGroup(box_l, box_r, kb, sw, t_l, t_r, sjf2, xs, rr2, half)),
                 Succession(Wait(0.8), Create(hist[1]), FadeIn(hist[0])), prof.change("happy"))
        self.beat(1.0)
