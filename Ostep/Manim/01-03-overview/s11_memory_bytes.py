import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from manim import *  # noqa: E402,F403
from ostep_lib import *  # noqa: E402,F403
from common import *  # noqa: E402,F403
from s10_four_at_once import s10_world, s10_end_world  # noqa: E402


class S11MemoryBytes(NarratedScene):
    def construct(self):
        stu, prof = make_hosts("corner", stu_expr="neutral", prof_expr="happy")
        w = s10_end_world()
        cpu, procs, tl, term0 = w["cpu"], w["procs"], w["tl"], w["term"]
        stu.set_look(cpu)
        th = terms(VIRT)
        bdg = badge(VIRT)
        self.add(stu, prof, bdg, cpu, procs, tl, w["slots"], w["times"], w["tag"], w["band"], term0,
                 set_docked(th, "policy"))

        # S11.1
        self.say("Now memory.", FadeOut(VGroup(cpu, procs, tl, term0, w["slots"], w["times"], w["tag"], w["band"])),
                 late(0.3, th.note("physical memory")))

        # S11.2
        strip = s11_strip()
        self.say("Physical memory is simple. It's an array of bytes.",
                 LaggedStart(*[AnimationGroup(Create(c), FadeIn(v), FadeIn(a))
                               for c, v, a in zip(strip.cells, strip.values, strip.addresses)],
                             lag_ratio=0.12, run_time=1.8))
        self.add(strip)

        # S11.3 read
        c1 = strip.cell(1)
        r_arrow = Arrow(c1.get_top() + UP * 0.9, c1.get_top() + UP * 0.05, buff=0, stroke_width=4,
                        tip_length=0.18).set_color(CPU_COLOR)
        r_lab = Text("read 0x200000", font=MONO_FONT, font_size=20, color=CPU_COLOR).next_to(r_arrow, LEFT, buff=0.12)
        with self.narrate("To read, you give an address."):
            self.play(GrowArrow(r_arrow), FadeIn(r_lab), run_time=0.6)
            anim, fly = strip.read(1, r_lab.get_left() + LEFT * 0.4)
            self.add(fly)
            self.play(fly.animate.move_to(r_arrow.get_top() + UP * 0.25 + RIGHT * 0.35).scale(1.3), run_time=0.8)
            self.play(FadeOut(fly), run_time=0.3)
        self.play(FadeOut(r_arrow), FadeOut(r_lab), run_time=0.3)

        # S11.4 write
        c2 = strip.cell(2)
        w_arrow = Arrow(c2.get_top() + UP * 0.9, c2.get_top() + UP * 0.05, buff=0, stroke_width=4,
                        tip_length=0.18).set_color(VIRT)
        w_lab = Text("write 0x200004 ← 9", font=MONO_FONT, font_size=20, color=VIRT).next_to(w_arrow, RIGHT, buff=0.12)
        with self.narrate("To write, you give an address and the data."):
            self.play(GrowArrow(w_arrow), FadeIn(w_lab), run_time=0.6)
            self.play(strip.write(2, "9", w_arrow.get_top() + UP * 0.2))
            self.play(FadeOut(w_arrow), FadeOut(w_lab), run_time=0.4)

        # S11.5 pulses
        rng = np.random.default_rng(5)
        with self.narrate("Every running program touches memory constantly, even just to fetch its own instructions."):
            for _ in range(8):
                ks = rng.choice(12, size=3, replace=False)
                self.play(*[strip.pulse(int(k), run_time=0.45) for k in ks], run_time=0.45)

        # S11.6 code
        code, title = s11_code()
        self.say("Here's another tiny program, mem.",
                 FadeIn(code.background), Write(code.code_lines, run_time=1.4), FadeIn(title), min_time=2.0)

        # S11.7 malloc -> lilac cell p
        bar = line_bar(code, 0)
        p_lab = Text("p", font=MONO_FONT, font_size=24, color=PID1_COLOR, weight=BOLD).next_to(strip.cell(1), UP, buff=0.1)

        def bar_to(i, rt=0.3):
            return bar.animate(run_time=rt).move_to([bar.get_x(), code.code_lines[i].get_y(), 0])

        with self.narrate("It asks for a little memory with malloc(), prints the address it got, stores a zero there,"):
            self.play(FadeIn(bar), run_time=0.3)
            self.play(strip.color_cell(1, PID1_COLOR), FadeIn(p_lab, shift=DOWN * 0.1), run_time=0.6)
            self.wait(0.4)
            self.play(bar_to(1))
            self.wait(0.8)
            self.play(bar_to(2))
            self.play(strip.set_value(1, "0"))

        # S11.8 loop
        with self.narrate("and then once a second adds one and prints it."):
            for v in (1, 2):
                self.play(bar_to(4))
                self.play(bar_to(5))
                self.play(strip.set_value(1, str(v)))
                self.play(bar_to(6))
            self.play(FadeOut(bar), run_time=0.3)

        self.say("You might want to pause the video here to read the code.", min_time=3.5)

        # S11.9 PID
        pid = pid_process(2134, PID1_COLOR)
        place_on(pid, S11_PID_POS)
        self.say("Each line starts with the program's process identifier, or PID, a number unique to each "
                 "running program.",
                 FadeIn(pid, shift=UP * 0.3), th.note("process identifier (PID)"))

        # S11.10 terminal run
        term = s11_terminal()
        with self.narrate("Run it once: the memory is at address 0x200000, and the value counts 1, 2, 3, 4."):
            self.play(FadeIn(term), strip.set_value(1, "0"), run_time=0.5)
            self.play(term.type("./mem", run_time=0.5))
            self.play(term.print("(2134) address pointed to by p: 0x200000"), run_time=0.4)
            for v in range(1, 5):
                self.wait(0.35)
                self.play(term.print(f"(2134) p: {v}"), strip.set_value(1, str(v)), run_time=0.4)
        self.beat(0.6)
