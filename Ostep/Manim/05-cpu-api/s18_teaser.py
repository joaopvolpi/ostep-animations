import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403

from s17_recap import ITEMS, YS, icons  # noqa: E402


class S18Teaser(Ep05Scene):
    def construct(self):
        # S17 end state (badge faded out): header + list + icons + corner characters
        header = Text("Recap", font_size=44, color=VIRT, weight="BOLD").move_to(P3(-6.0, 2.85), aligned_edge=LEFT)
        lines = VGroup(*[Text(s, font_size=28, color=TEXT) for s in ITEMS])
        for ln, y in zip(lines, YS):
            ln.move_to(P3(-5.8, y), aligned_edge=LEFT)
        ics = icons()
        for ic, y in zip(ics, YS):
            ic.move_to(P3(4.6, y))
        recap = VGroup(header, lines, *ics)
        stu = student_corner("neutral")
        prof = prof_corner("happy")
        self.add(recap, stu, prof)

        # S18.1
        cpu = CPU(1.1).move_to(P3(0, 1.3))
        coral = proc(PAR, "running", scale=0.8)
        seat(coral, cpu)
        band = RoundedRectangle(width=5.0, height=0.55, corner_radius=0.1).set_fill(KERNEL_COLOR, 0.35).set_stroke(KERNEL_COLOR, 3)
        band.move_to(P3(0, 0.0))
        os_lab = Text("OS", font_size=24, color=KERNEL_COLOR, weight="BOLD").move_to(band.get_center() + LEFT * 1.8)
        gears = GearPair(0.2).move_to(band.get_center() + RIGHT * 1.8)
        pane = glass_pane(5.4, 1.0).move_to(band)
        os_group = VGroup(band, os_lab, gears)
        q = question_mark(0.4).next_to(pane, RIGHT, buff=0.2)
        stu2 = student_dialogue("curious")
        prof2 = prof_dialogue("neutral")
        stu2.shift(LEFT * 5)
        prof2.shift(RIGHT * 5)
        with self.narrate('All these calls say "the OS creates this", "the OS stops that". But when my program '
                          "is running on the CPU, the OS isn't. How does it ever get control back?"):
            self.play(FadeOut(recap), FadeOut(stu), FadeOut(prof), run_time=0.8)
            self.add(stu2, prof2)
            self.play(stu2.animate.shift(RIGHT * 5), prof2.animate.shift(LEFT * 5), run_time=1.0)
            self.play(FadeIn(cpu), FadeIn(coral), FadeIn(os_group), FadeIn(pane), run_time=0.8)
            self.play(FadeIn(q, scale=0.5), run_time=0.4)
            self.wait(3.0)

        # S18.2
        gate = VGroup(Line(P3(-1.6, 0.8), P3(-1.6, 2.0)).set_stroke(KERNEL_COLOR, 5),
                      Line(P3(-1.3, 0.8), P3(-1.3, 2.0)).set_stroke(KERNEL_COLOR, 5),
                      Text("checkpoint", font_size=18, color=KERNEL_COLOR).move_to(P3(-1.45, 2.25)))
        gauge = SpeedGauge(1.0, width=1.6).move_to(P3(4.6, 1.5))
        glab = Text("speed", font_size=18, color=DIM).next_to(gauge, UP, buff=0.12)
        ds = VGroup(*[Dot(radius=0.07, color=CPU_COLOR).move_to(P3(-4.2 - 0.5 * k, 1.4)) for k in range(4)])
        bar_t, lab_t = gauge.value_targets(0.2, "20%")
        with self.narrate("Good question. And if the OS watched every instruction, we'd lose all the speed."):
            self.play(prof2.change("thinking"), FadeIn(gate), FadeIn(gauge), FadeIn(glab), FadeIn(ds), run_time=0.8)
            self.play(ds.animate(run_time=2.5, rate_func=linear).shift(RIGHT * 3.0),
                      Transform(gauge.bar, bar_t, run_time=2.5), Transform(gauge.label, lab_t, run_time=2.5))
            self.wait(0.5)

        # S18.3
        bar_f, lab_f = gauge.value_targets(1.0, "100%")
        dl = DashedLine(band.get_top() + UP * 0.05, cpu.get_bottom() + DOWN * 0.05).set_stroke(TEXT, 3)
        q2 = question_mark(0.35).next_to(dl, RIGHT, buff=0.1).shift(UP * 0.1)
        with self.narrate("We want programs to run directly on the CPU, but we want to stay in charge."):
            self.play(FadeOut(gate), FadeOut(ds), Transform(gauge.bar, bar_f), Transform(gauge.label, lab_f), run_time=1.0)
            self.play(Create(dl), FadeIn(q2), FadeOut(q), run_time=0.8)
            self.wait(2.0)

        # S18.4
        nxt = Text("limited direct execution", font_size=34, color=TEXT).move_to(P3(3.5, 2.7))
        card = VGroup(Dot(radius=0.1, color=VIRT), Text("Next: 06 · Direct Execution", font_size=40, color=TEXT)).arrange(RIGHT, buff=0.25)
        with self.narrate("Next time: limited direct execution."):
            self.play(prof2.change("happy"), Write(nxt), run_time=1.5)
            self.wait(0.8)
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)
            self.play(FadeIn(card, shift=UP * 0.2), run_time=0.6)
        self.wait(1.5)
