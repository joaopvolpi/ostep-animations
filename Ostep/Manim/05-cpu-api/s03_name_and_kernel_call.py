import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


class S03NameAndKernelCall(Ep05Scene):
    def construct(self):
        d = build_s02_end()
        self.add(d["badge"], d["strip"], d["stu"], d["prof"])
        stu, prof = d["stu"], d["prof"]

        cpu = CPU(1.4).move_to(CPU_S3)
        par = proc(PAR, "ready", label=f"PID {PID_P}").move_to(P3(-4.3, 1.0))

        # S03.1
        tag = name_tag("29146", font_size=18).scale(0.6).move_to(P3(-3.9, 2.45))
        with self.narrate("First, a name. Every process has an ID, a number the OS uses to refer to it."):
            self.play(GrowFromCenter(cpu), FadeIn(par), run_time=0.7)
            self.play(par.change("running"), run_time=0.4)
            self.play(hop_seat(par, cpu), run_time=0.6)
            self.play(FadeIn(tag, scale=0.6), stu.change("curious", look_at=tag), run_time=0.5)
            self.play(Indicate(tag, scale_factor=1.15), Indicate(par.label if False else tag, color=CPU_COLOR),
                      run_time=0.8)

        # S03.2
        self.say("It's the process identifier, or PID.", self.terms.note("process identifier (PID)"))

        # S03.3
        code = card_code(1).move_to(CODE_CARD_AT)
        mt = mk_term(4.6, 1, 18).move_to(MINI_TERM_AT)
        with self.narrate("Our program starts with PID 29146."):
            self.play(FadeOut(tag), FadeIn(code, shift=LEFT * 0.3), FadeIn(mt), run_time=0.7)
            self.play(mt.print("hello (pid:29146)"))

        # S03.4
        stop = stop_sign_tag("stop 29146").move_to(P3(-4.5, 1.7))
        arr = Arrow(stop.get_right(), par.get_left() + LEFT * 0.0 + UP * 0.2, buff=0.1, stroke_width=4, color=KERNEL_COLOR)
        with self.narrate("In UNIX, if you want to do something to a process, like stop it, the PID is how you name it."):
            self.play(FadeIn(stop, shift=RIGHT * 0.2), Create(arr), run_time=0.8)
            self.wait(2.2)
            self.play(FadeOut(stop), FadeOut(arr), run_time=0.5)

        # S03.5
        code2 = card_code(2).move_to(CODE_CARD_AT)
        code2.shift(code.get_top() - code2.get_top())
        with self.narrate("Now the interesting part."):
            self.play(ReplacementTransform(code, code2), run_time=0.6)
            bar = code2.add_bar(TEXT, 2)
            self.play(FadeIn(bar), run_time=0.4)
            self.beat(0.5)
        code = code2

        # S03.6
        bd = UserKernelBoundary(y=BOUNDARY_Y)
        gauge = PrivilegeGauge(height=1.6, level="user").move_to(GAUGE_S3)
        packet = program_chip("fork()", CPU_COLOR, 18).move_to(P3(-1.0, 1.5))
        with self.narrate("The program calls fork(). It's a system call: a request to the OS, "
                          "so it crosses into the kernel."):
            self.play(self.terms.show("fork()"), prof.change("explaining", look_at=packet))
            self.play(bd.draw(1.5), FadeIn(gauge), run_time=1.5)
            self.play(FadeIn(packet, scale=0.5), run_time=0.4)
            self.play(bd.cross(packet, P3(-0.8, -1.7), run_time=1.2), gauge.set_level("kernel"))
            self.play(Indicate(bd.kernel_zone, color=KERNEL_COLOR, scale_factor=1.0), run_time=0.6)
        self.beat(0.5)
