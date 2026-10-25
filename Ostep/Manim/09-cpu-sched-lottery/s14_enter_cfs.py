import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403

PX = {"A": -3.6, "B": -1.2, "C": 1.2, "D": 3.6}
PY = -0.9


class S14EnterCFS(Ep09Scene):
    def construct(self):
        self.world(stu="excited", prof="happy")
        stu, prof = self.stu, self.prof
        cpu = CPU(size=1.2, label="CPU").move_to(P3(0, 1.0))

        # S14.1
        linux = Text("Linux", font_size=24, color=DIM, font=MONO_FONT).move_to(P3(-5.6, 2.2))
        self.say("Now for the real world. For years, Linux used a scheduler with a similar goal, reached in a very different "
                 "way: the Completely Fair Scheduler, or CFS.",
                 FadeIn(linux), self.term("Completely Fair Scheduler (CFS)"))

        # S14.2
        coin = coin_icon(0.4).move_to(P3(2.4, 1.0))
        sliver = Rectangle(width=0.7, height=0.08).set_fill(CPU_COLOR, 1).set_stroke(width=0).move_to(cpu.get_top() + UP * 0.08)
        self.say("Its other goal is efficiency. Scheduling steals CPU time from the programs it schedules.",
                 FadeIn(cpu), FadeIn(coin),
                 Succession(Wait(1.0), FadeIn(sliver), glide(sliver, P3(2.4, 1.0), 1.2), FadeOut(sliver)))

        # S14.3
        bar = Rectangle(width=2.0, height=0.3).set_fill(CPU_COLOR, 0.8).set_stroke(TEXT, 1)
        tax = Rectangle(width=0.1, height=0.3).set_fill(KERNEL_COLOR, 1).set_stroke(width=0).align_to(bar, RIGHT).match_y(bar)
        tag5 = MathTex(r"\approx 5\%", font_size=34, color=KERNEL_COLOR)
        study = Text("datacenter study", font_size=18, color=DIM)
        chip = VGroup(bar, tax, tag5.next_to(bar, RIGHT, buff=0.15), study.next_to(bar, DOWN, buff=0.1)).move_to(P3(-3.6, 1.0))
        self.say("In a study of Google's data centers, even after heavy optimization, about five percent of all CPU time "
                 "went to scheduling.", FadeOut(coin), FadeIn(chip))

        # S14.4
        sw = stopwatch_icon(0.35).move_to(P3(2.6, 1.0))
        self.say("So CFS must decide fast.", FadeIn(sw),
                 Succession(*[Indicate(sw, scale_factor=1.25, run_time=0.3) for _ in range(4)]))

        # S14.5
        procs = {n: proc(n, scale=0.6).move_to(P3(PX[n], PY)) for n in "ABCD"}
        meters = {n: VruntimeMeter(COL[n], height=0.9, max_value=20.0).next_to(procs[n], RIGHT, buff=0.15) for n in "ABCD"}
        self.say("Its counter is virtual runtime, or vruntime.",
                 FadeOut(chip), FadeOut(sw), self.term("vruntime"),
                 *[FadeIn(procs[n]) for n in "ABCD"], *[FadeIn(meters[n]) for n in "ABCD"])

        # S14.6
        clk = ClockIcon(0.25, color=CPU_COLOR).move_to(P3(3.2, 1.7))
        txt0 = Text("vruntime: 0 ms", font_size=22, color=TEXT).move_to(P3(3.2, 1.2))
        txt1 = Text("vruntime: 12 ms", font_size=22, color=TEXT).move_to(txt0)
        home = {n: procs[n].get_center().copy() for n in "ABCD"}
        self.say("A running process accumulates vruntime, at the same rate as real time.",
                 hop_to(procs["A"], cpu.slot_point(), run_time=0.9), FadeIn(clk), FadeIn(txt0),
                 Succession(Wait(1.0), AnimationGroup(meters["A"].add_runtime(12, run_time=3.0),
                                                      Transform(txt0, txt1, run_time=3.0), clk.spin(1, run_time=3.0))))

        # S14.7
        spot = Spotlight(height=0.9, spread=0.35)
        spot.move_beam_to(meters["A"].get_center() + RIGHT * 0.0 + DOWN * 0.7)
        self.say("When it's time to choose, CFS picks the process with the lowest vruntime.",
                 FadeOut(VGroup(clk, txt0)), hop_bottom(procs["A"], home["A"] + DOWN * 0.45, run_time=0.8),
                 Succession(Wait(1.0), FadeIn(spot), glide(spot, procs["B"].get_center() + DOWN * 0.1 + UP * 0.5, 0.9),
                            hop_to(procs["B"], cpu.slot_point(), run_time=0.9)))

        # S14.8
        ghost = VGroup(*[Line(P3(-5.0, 2.0 - 0.35 * k), P3(5.0, 2.0 - 0.35 * k)).set_stroke(DIM, 1.5, opacity=0.5)
                         for k in range(3)])
        self.say("Like stride's pass value?", stu.change("curious"),
                 Succession(FadeIn(ghost), Wait(0.8), FadeOut(ghost)))

        # S14.9
        self.say("Same flavor: whoever has had the least goes next.", prof.change("happy"))
        self.beat(0.8)
        self.fade_stage()
