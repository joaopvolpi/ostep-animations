import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403

TICK_MS = 6          # one timeline tick = 6 ms; 42 ticks = 252 ms


def make_timeline():
    return Timeline(["CPU"], ticks=42, x_range=(-5.2, 5.2), top=-0.9, row_height=0.5, row_kinds=["cpu"],
                    label_mode="boundary", unit_per_tick=TICK_MS, label_every=8, unit="ms", tick_font=16,
                    tick_label_y=-1.4, label_font=20)


class S15SchedLatency(Ep09Scene):
    def construct(self):
        self.world(term="Completely Fair Scheduler (CFS)", stu="neutral", prof="neutral")
        stu, prof = self.stu, self.prof
        cpu = CPU(size=0.8, label="CPU").move_to(P3(-5.2, 1.5))
        tl = make_timeline()
        meters = {n: VruntimeMeter(COL[n], height=0.7, width=0.26, max_value=48.0) for n in "ABCD"}
        procs = {n: proc(n, scale=0.4) for n in "ABCD"}
        for i, n in enumerate("ABCD"):
            procs[n].move_to(P3(-1.8 + 1.2 * i, -2.55))
            meters[n].next_to(procs[n], RIGHT, buff=0.1)
        spot = Spotlight(height=0.7, spread=0.3)
        spot.move_beam_to(meters["A"].get_center() + DOWN * 0.45)
        self.add(cpu, tl)
        self.add(*procs.values(), *meters.values())

        # S15.1
        sw = Text("switch?", font_size=22, color=CPU_COLOR).move_to(P3(-3.6, 1.5))
        self.say("But when does CFS stop the running process? Every millisecond?",
                 stu.change("confused"), Succession(*[Indicate(cpu, color=CPU_COLOR, scale_factor=1.15, run_time=0.25)
                                                       for _ in range(6)]), FadeIn(sw))

        # S15.2
        ss = Seesaw(3.6, "switch often", "switch rarely").move_to(P3(0, 1.4))
        ss.set_angle_now(0)
        fair = VGroup(Text("fair", font_size=20, color=TEXT), tick_mark(0.25),
                      Text("cost", font_size=20, color=TEXT), x_mark(0.25)).arrange(RIGHT, buff=0.12).move_to(P3(-2.6, 0.2))
        many = [tl.fill("CPU", t, "running", color=COL["AB"[t % 2]], run_time=0.15) for t in range(1, 13)]
        self.say("That's the tension. Switch often, and you're fair even over tiny windows, but you pay for every "
                 "context switch.",
                 FadeOut(sw), FadeIn(ss), Succession(Wait(0.8), ss.tilt(14, run_time=0.8)), FadeIn(fair),
                 Succession(Wait(3.0), *many))

        # S15.3
        eff = VGroup(Text("efficient", font_size=20, color=TEXT), tick_mark(0.25),
                     Text("unfair", font_size=20, color=TEXT), x_mark(0.25)).arrange(RIGHT, buff=0.12).move_to(P3(2.6, 0.2))
        self.play(tl.clear_blocks(0.5), run_time=0.5)
        tl.purge()
        self.say("Switch rarely, and you're efficient, but unfair in the short run.",
                 FadeOut(fair), ss.tilt(-14, run_time=1.0), FadeIn(eff),
                 Succession(Wait(1.0), tl.fill_span("CPU", 0, 20, "running", color=COL["A"], run_time=0.8),
                            tl.fill_span("CPU", 20, 40, "running", color=COL["B"], run_time=0.8)))

        # S15.4
        eq = MathTex(r"\text{48 ms} \div n", font_size=36, color=TEXT).move_to(P3(0, 0.15))
        br = tl.bracket("CPU", 0, 8, "48 ms")
        self.play(tl.clear_blocks(0.5), FadeOut(eff), ss.tilt(0, run_time=0.6), run_time=0.6)
        tl.purge()
        self.say("CFS uses two knobs. First, sched_latency, typically forty-eight milliseconds, divided by the number of "
                 "runnable processes.",
                 self.term("sched_latency"), FadeOut(ss), FadeIn(eq), Create(br.line if hasattr(br, "line") else br)
                 if False else FadeIn(br))

        # S15.5
        eq2 = MathTex(r"48 \div 4 = 12\ \text{ms}", font_size=36, color=TEXT).move_to(eq)
        blocks = [tl.fill_span("CPU", 2 * k, 2 * k + 2, "running", color=COL["ABCD"[k]], run_time=0.4) for k in range(4)]
        self.say("Four processes: twelve milliseconds each.", Transform(eq, eq2), Succession(*blocks))

        # S15.6
        lbls = VGroup(*[Text("12", font_size=18, color=INK_DARK).move_to(tl.cell_center("CPU", 2 * k + 1) + RIGHT * 0.0)
                        for k in range(4)])
        anims = [FadeIn(lbls), FadeIn(spot)]
        seq2 = [tl.fill_span("CPU", 8 + 2 * k, 10 + 2 * k, "running", color=COL["ABCD"[k]], run_time=0.4) for k in range(4)]
        for n in "ABCD":
            anims.append(meters[n].set_level(0.25, run_time=2.0))
        self.say("CFS runs one for twelve, then switches to a process with lower vruntime.",
                 *anims[:2], Succession(Wait(1.0), AnimationGroup(meters["A"].set_level(0.25, run_time=0.8)),
                                        spot.animate(run_time=0.8).move_beam_to(meters["B"].get_center() + DOWN * 0.45),
                                        *seq2))

        # S15.7
        pairs = []
        for k in range(6):
            n = "AB"[k % 2]
            b0 = 16 + 4 * k
            pairs.append(tl.fill_span("CPU", b0, b0 + 4, "running", color=COL[n], run_time=0.4))
        marks = [tick_mark(0.3).next_to(procs[n], UP, buff=0.05) for n in "CD"]
        self.say("Our four take turns. Then two finish, and the other two get twenty-four each.",
                 *[FadeIn(m) for m in marks],
                 Succession(Wait(1.0), AnimationGroup(*[FadeOut(procs[n]) for n in "CD"], *[FadeOut(meters[n]) for n in "CD"],
                                                      *[FadeOut(m) for m in marks]),
                            *pairs))
        self.beat(0.8)
