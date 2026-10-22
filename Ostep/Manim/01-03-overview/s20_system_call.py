import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from manim import *  # noqa: E402,F403
from ostep_lib import *  # noqa: E402,F403
from common import *  # noqa: E402,F403

UK_Y = -0.3
A_POS = np.array([-3.0, 0.85, 0])       # center of process A
F_POS = np.array([-0.9, 0.85, 0])
HANDLER_POS = np.array([1.6, -1.8, 0])
DISK_POS = np.array([4.1, -2.2, 0])     # spec (5, -2.6) collides with the Professor
GAUGE_POS = np.array([6.05, 0.15, 0])


def s20_world():
    uk = UserKernelBoundary(y=UK_Y)
    a = Process(color=A_COLOR, label="A").scale(0.65).move_to(A_POS)
    handler = RoundedRectangle(width=2.3, height=0.8, corner_radius=0.1).set_fill(CARD_FILL, 1).set_stroke(KERNEL_COLOR, 3)
    handler.move_to(HANDLER_POS)
    h_lab = Text("trap handler", font_size=22, color=TEXT).move_to(handler)
    disk = Disk(width=1.3, height=1.1).move_to(DISK_POS)
    gauge = PrivilegeGauge(height=1.8).move_to(GAUGE_POS)
    return uk, a, VGroup(handler, h_lab), disk, gauge


class S20SystemCall(NarratedScene):
    def construct(self):
        stu, prof = make_hosts("corner", stu_expr="curious", prof_expr="happy")
        th = hist_terms(at=(2.0, 1.7, 0), size=40)
        bdg = badge(INTRO)
        era = era_ribbon(0)
        mf, shelf, cpu_job, operator = s19_end()
        self.add(stu, prof, bdg, era, mf, shelf, cpu_job, operator, set_docked(th, "batch processing"))

        uk, a, handler, disk, gauge = s20_world()

        # S20.1
        self.say("Then came a realization: code that runs on behalf of the OS is special.",
                 FadeOut(VGroup(mf, shelf, cpu_job, operator)), era.move_marker("Atlas"),
                 Succession(Wait(0.6), AnimationGroup(FadeIn(a, shift=UP * 0.2), FadeIn(disk, shift=UP * 0.2))))

        # S20.2 the grab
        arm_end = disk.top_point() + UP * 0.05
        arm = Line(a.get_right() + LEFT * 0.1, a.get_right() + LEFT * 0.05).set_stroke(A_COLOR, 6)
        loot = FileIcon("someone else's", color=BAD, width=0.4, font_size=14).move_to(arm_end + UP * 0.2)
        with self.narrate("If any program could read anywhere on the disk, privacy would be gone."):
            self.play(arm.animate.put_start_and_end_on(a.get_right() + LEFT * 0.1, arm_end), run_time=0.7)
            self.play(FadeIn(loot, scale=0.5), Flash(arm_end, color=BAD), run_time=0.5)
            self.play(loot.animate.move_to(a.get_right() + RIGHT * 0.5 + UP * 0.2),
                      arm.animate.put_start_and_end_on(a.get_right() + LEFT * 0.1, a.get_right() + RIGHT * 0.3),
                      run_time=0.8)
            self.wait(0.6)

        # S20.3 rewind + boundary
        with self.narrate("So the system call was invented, pioneered by the Atlas computer."):
            self.play(loot.animate.move_to(arm_end + UP * 0.2), arm.animate.put_start_and_end_on(a.get_right(), arm_end),
                      run_time=0.5, rate_func=rush_from)
            self.play(FadeOut(loot), FadeOut(arm), run_time=0.3)
            self.add(uk.user_zone, uk.kernel_zone)
            self.bring_to_back(uk.user_zone, uk.kernel_zone)
            self.play(Create(uk.line), FadeIn(uk.user_zone), FadeIn(uk.kernel_zone),
                      FadeIn(uk.user_label), FadeIn(uk.kernel_label), run_time=1.2)
            self.play(th.show("system call", hold=0.8))

        # S20.4 procedure call
        fbox = RoundedRectangle(width=0.9, height=0.55, corner_radius=0.08).set_fill(CARD_FILL, 1).set_stroke(USER_COLOR, 2.5)
        fbox.move_to(F_POS)
        flab = Text("f()", font=MONO_FONT, font_size=22, color=TEXT).move_to(fbox)
        go = CurvedArrow(a.get_right() + UP * 0.1, fbox.get_left() + UP * 0.1, angle=-0.5, tip_length=0.15).set_color(USER_COLOR)
        back = CurvedArrow(fbox.get_left() + DOWN * 0.1, a.get_right() + DOWN * 0.1, angle=-0.5, tip_length=0.15).set_color(USER_COLOR)
        pc_lab = Text("procedure call", font_size=18, color=USER_COLOR).next_to(fbox, DOWN, buff=0.15)
        self.say("It's not a normal procedure call.",
                 FadeIn(VGroup(fbox, flab)), Succession(Create(go, run_time=0.5), Create(back, run_time=0.5)),
                 FadeIn(pc_lab), min_time=2.2)

        # S20.5 gauge
        self.say("It jumps into the OS and raises the hardware privilege level.",
                 FadeOut(VGroup(go, back)), FadeIn(gauge, shift=LEFT * 0.3))

        # S20.6 user mode: denied
        arm2 = Line(a.get_bottom(), a.get_bottom()).set_stroke(A_COLOR, 6)
        hit = np.array([a.get_bottom()[0] + 0.9, UK_Y + 0.02, 0])
        with self.narrate("Applications run in user mode, where the hardware restricts what they can do: no direct "
                          "disk I/O, no touching any memory they like."):
            self.play(th.show("user mode", hold=0.8))
            self.play(arm2.animate.put_start_and_end_on(a.get_bottom(), hit), run_time=0.5)
            self.play(uk.flash_at(hit[0], BAD), Wiggle(a, scale_value=1.05, rotation_angle=0.06), run_time=0.6)
            self.play(arm2.animate.put_start_and_end_on(a.get_bottom(), a.get_bottom() + DOWN * 0.01), run_time=0.4)
            self.remove(arm2)

        # S20.7 trap
        trap = Text("trap", font=MONO_FONT, font_size=20, color=CPU_COLOR, weight=BOLD)
        dot = Dot(a.get_bottom(), radius=0.09).set_fill(CPU_COLOR, 1)
        path = Line(a.get_bottom(), handler[0].get_left() + LEFT * 0.05).set_stroke(CPU_COLOR, 4)
        with self.narrate("A special trap instruction jumps to a trap handler set up by the OS,"):
            self.play(FadeIn(handler, shift=UP * 0.2), run_time=0.5)
            trap.next_to(path.get_center(), LEFT, buff=0.15)
            self.add(dot)
            self.play(Create(path), FadeIn(trap), uk.cross(dot, handler[0].get_left()), run_time=1.0)
            self.play(Indicate(handler, color=KERNEL_COLOR), FadeOut(dot), run_time=0.5)
            self.play(th.show("trap · trap handler", hold=0.8))

        # S20.8 kernel mode: reach disk
        harm = Line(handler[0].get_right(), handler[0].get_right()).set_stroke(KERNEL_COLOR, 6)
        data = FileIcon("A's data", color=TEXT, width=0.38, font_size=13).move_to(disk.top_point() + UP * 0.3)
        with self.narrate("and switches to kernel mode, with full access to the hardware."):
            self.play(gauge.set_level("kernel"), run_time=0.6)
            self.play(harm.animate.put_start_and_end_on(handler[0].get_right(), disk.top_point()), run_time=0.5)
            self.play(FadeIn(data, scale=0.5), run_time=0.3)
            self.play(data.animate.move_to(handler[0].get_top() + UP * 0.3 + RIGHT * 0.6),
                      harm.animate.put_start_and_end_on(handler[0].get_right(), handler[0].get_right() + RIGHT * 0.01),
                      run_time=0.6)
            self.remove(harm)
            self.play(th.show("kernel mode", hold=0.8))

        # S20.9 return-from-trap
        ret_lab = Text("return-from-trap", font=MONO_FONT, font_size=18, color=GOOD)
        ret = Line(handler[0].get_top(), a.get_right() + DOWN * 0.3).set_stroke(GOOD, 4)
        ret_lab.next_to(ret.get_center(), RIGHT, buff=0.15)
        with self.narrate("When the OS is done, a return-from-trap drops back to user mode, right where the "
                          "application left off."):
            self.play(Create(ret), FadeIn(ret_lab), uk.cross(data, a.get_right() + RIGHT * 0.35), run_time=1.1)
            self.play(gauge.set_level("user"), FadeOut(data), run_time=0.6)
            self.play(hop_to(a, base_point(a), height=0.3, run_time=0.4))
            self.play(th.show("return-from-trap", hold=0.8))

        # S20.10-11
        self.say("So programs ask permission, and the OS does the dangerous stuff?", stu.change("curious"))
        tag = next_tag("→ Ep. 06", 18).move_to([-4.6, UK_Y - 0.75, 0])
        self.say("Exactly. Remember that dashed line. We'll cross it a lot.",
                 prof.change("happy"), uk.pulse(2), FadeIn(tag))
        self.beat(0.5)
