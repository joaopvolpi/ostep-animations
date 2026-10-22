import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from manim import *  # noqa: E402,F403
from ostep_lib import *  # noqa: E402,F403
from common import *  # noqa: E402,F403
from s05_enter_os import virtual_copies  # noqa: E402

CRUX_Q = "How to virtualize resources?"
CRUX_SUB = "What mechanisms and policies? How, efficiently? What hardware support?"


def s06_end_state():
    stack = make_stack()
    procs = stack_programs()
    crux = CruxCard(CRUX_Q, CRUX_SUB, accent=INTRO)
    strip = crux.strip((0, 3.2, 0))
    return stack, procs, strip


class S06CruxApiManager(NarratedScene):
    def construct(self):
        stu, prof = make_hosts("corner", stu_expr="bored", prof_expr="thinking")
        stack = make_stack()
        procs = stack_programs()
        vc, vm = virtual_copies(stack, procs)
        th = terms(INTRO)
        bdg = badge(INTRO)
        self.add(stu, prof, bdg, stack, procs, vc, vm, set_docked(th, "virtual machine"))

        # S06.1 crux
        crux = CruxCard(CRUX_Q, CRUX_SUB, accent=INTRO).move_to([0, 0.8, 0])
        self.add_subcaption("THE CRUX: How to virtualize resources? What mechanisms and policies does the OS use "
                            "to virtualize? How does it do so efficiently? What hardware support is needed?",
                            duration=5.6)
        self.play(FadeOut(vc), FadeOut(vm), run_time=0.6)
        self.play(crux.write())
        self.beat(2.4)
        self.play(crux.dock((0, 3.2, 0)))
        th.at = np.array([0, 2.35, 0])

        # S06.2 system calls
        doors = stack.doors(["run", "malloc", "open"], xs=[-3.6, 0.0, 3.6])
        p = procs[0]
        req = Arrow(base_point(p) + DOWN * 0.05 + RIGHT * 0.1, doors[0].get_top() + RIGHT * 0.1 + DOWN * 0.05,
                    buff=0, stroke_width=4, tip_length=0.18).set_color(A_COLOR)
        with self.narrate("To let you tell this virtual machine what to do, like run a program, allocate memory "
                          "or open a file, the OS offers a few hundred system calls."):
            self.play(LaggedStart(*[FadeIn(d, shift=DOWN * 0.15) for d in doors], lag_ratio=0.3), run_time=1.0)
            self.wait(1.5)
            self.play(GrowArrow(req), run_time=0.6)
            self.play(Indicate(doors[0], color=CPU_COLOR), run_time=0.6)
            self.play(th.show("system calls", hold=1.0))
        self.play(FadeOut(req), run_time=0.3)

        # S06.3
        with self.narrate("We sometimes say it provides a standard library to applications."):
            self.play(stack.relabel("a standard library"), run_time=0.6)
            self.play(th.show("standard library", size=42, hold=0.8))
            self.play(stack.relabel("Operating System"), run_time=0.5)

        # S06.4 resource manager: hands pass a CPU token
        token = CPU(size=0.5, label=None, pins=2)
        hand = hand_icon(0.5)
        with self.narrate("And because many programs share the CPU, the memory and the disks, the OS is also a "
                          "resource manager. It hands those resources out efficiently and fairly."):
            self.play(stack.relabel("a resource manager"), run_time=0.6)
            for k, pr in enumerate((procs[0], procs[1], procs[2], procs[0])):
                x = pr.get_center()[0] + 0.55
                hand.move_to([x, stack.band.get_top()[1] - 0.05, 0])
                token.next_to(hand, UP, buff=0.02)
                grp = VGroup(hand, token)
                if k == 0:
                    self.play(FadeIn(grp, shift=UP * 0.4), run_time=0.4)
                else:
                    self.play(FadeIn(grp, shift=UP * 0.4), run_time=0.3)
                self.play(grp.animate.shift(UP * 0.55), run_time=0.35)
                self.play(FadeOut(grp, shift=DOWN * 0.3), run_time=0.3)
            self.play(th.show("resource manager", hold=0.8))

        # S06.5 the gag
        sup = Text("the supervisor", font_size=24, color=TEXT).rotate(0.06)
        sup_box = SurroundingRectangle(sup, buff=0.1, corner_radius=0.06).set_fill(CARD_FILL, 1).set_stroke(DIM, 2)
        sup_tag = VGroup(sup_box, sup).move_to([-3.0, -0.9, 0])
        mcp = Text("MASTER CONTROL PROGRAM", font_size=34, color=KERNEL_COLOR, weight=BOLD)
        mcp_glow = glow_for(mcp, KERNEL_COLOR)
        mcp_g = VGroup(mcp_glow, mcp).move_to([0, -0.9, 0])
        with self.narrate("Fun fact: early names for the OS were \"the supervisor\" and even \"the master control program\"."):
            self.play(prof.change("explaining"), stack.relabel("Operating System"), run_time=0.6)
            self.play(FadeIn(sup_tag, shift=DOWN * 0.8), run_time=0.7)
            self.wait(1.2)
            self.play(FadeOut(stack.band_label), FadeOut(sup_tag), FadeIn(mcp_g, scale=1.4),
                      stack.band.animate.set_fill(KERNEL_COLOR, 0.6).set_stroke(width=6), run_time=0.8)
            self.play(Wiggle(mcp_g, scale_value=1.05, rotation_angle=0.02), run_time=0.8)

        # S06.6
        stamp = x_mark(0.5, BAD, 10).move_to(mcp)
        with self.narrate("The second one sounded a little overzealous, so \"operating system\" won."):
            self.play(Create(stamp), run_time=0.4)
            self.play(VGroup(mcp_g, stamp).animate.shift(DOWN * 4.5).rotate(-0.6),
                      stack.band.animate.set_fill(KERNEL_COLOR, 0.25).set_stroke(width=3), run_time=1.0)
            self.remove(mcp_g, stamp)
            stack.band_label = Text("Operating System", font_size=28, color=TEXT).move_to(stack.band)
            self.play(FadeIn(stack.band_label), FadeOut(doors), stu.change("excited"), run_time=0.6)
        self.beat(0.6)
