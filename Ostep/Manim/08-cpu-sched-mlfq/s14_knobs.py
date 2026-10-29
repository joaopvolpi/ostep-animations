import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


class S14Knobs(Ep08Scene):
    def construct(self):
        self.build(lanes=3, cpu=True, ticks=30, rules=None, board=False, stu="neutral", prof="neutral", term="accounting")
        lad, cpu, tl = self.ladder, self.cpu, self.tl
        panel = SliderPanel(["number of queues", "time slice / queue", "allotment", "boost period"], width=2.5, font_size=18)
        panel.move_to(P3(4.9, 0.85))

        # S14.1
        lad5 = MLFQLadder(levels=5, arrows=False)
        with self.narrate("Plenty of questions remain. How many queues?"):
            self.play(self.note("parameterize"), FadeIn(panel, shift=LEFT * 0.5), run_time=0.8)
            self.play(panel.move_knob(0, 0.9, 0.6), FadeOut(lad), run_time=0.6)
            self.play(FadeIn(lad5), run_time=0.5)
            self.beat(0.4)
            self.play(panel.move_knob(0, 0.5, 0.6), FadeOut(lad5), run_time=0.6)
            self.play(FadeIn(lad), run_time=0.5)

        # S14.2
        ring_a = progress_ring(0.95, color=VIRT, value=0.4, width=6).move_to(cpu)
        ring_b = progress_ring(0.95, color=VIRT, value=0.85, width=6).move_to(cpu)
        self.say("How long a time slice at each level?",
                 panel.move_knob(1, 0.2, 0.6), FadeIn(ring_a), after(0.6, Transform(ring_a, ring_b, run_time=1.0)))
        self.play(panel.move_knob(1, 0.5, 0.5), FadeOut(ring_a), run_time=0.5)

        # S14.3
        g1 = AllotmentGauge(0.8, 1.0).move_to(P3(2.0, 2.2))
        g2 = AllotmentGauge(1.6, 1.0).move_to(P3(2.0, 2.2))
        self.say("How big an allotment?", panel.move_knob(2, 0.85, 0.6), FadeIn(g1), after(0.6, Transform(g1, g2, run_time=0.9)))
        self.play(panel.move_knob(2, 0.5, 0.5), FadeOut(g1), run_time=0.5)

        # S14.4
        sw = stopwatch_icon(0.3).move_to(P3(0.85, 0.0))
        self.say("How often to boost?", panel.move_knob(3, 0.15, 0.6), FadeIn(sw),
                 after(0.6, Rotate(sw.hand, angle=-TAU, about_point=sw[0].get_center(), run_time=1.0),
                            Rotate(sw.hand, angle=-TAU * 3, about_point=sw[0].get_center(), run_time=1.0)))
        self.play(panel.move_knob(3, 0.5, 0.5), FadeOut(sw), run_time=0.5)

        # S14.5
        sparks = VGroup(*[label("?", 26, CPU_COLOR).move_to(P3(3.1, panel.knobs[i].get_center()[1])) for i in range(4)])
        jit = []
        for i in range(4):
            jit.append(Succession(*[panel.move_knob(i, f, 0.2) for f in (0.35, 0.65, 0.4, 0.6, 0.5)]))
        self.say("There are no easy answers, only experience with real workloads.",
                 self.stu.change("confused"), *jit, FadeIn(sparks), self.prof.change("explaining"))
        self.play(FadeOut(sparks), run_time=0.4)

        # S14.6
        A, B = self.put("A", 2, 0), self.put("B", 2, 1)
        t2 = label("10 ms", 22, CPU_COLOR).move_to(lad.lane_point(2, 4.3))
        hops = []
        for j in (A, B, A, B):
            hops += [self.to_cpu(j, 0.3), self.to_lane(j, 2, 0 if j is A else 1, "ready", t=0.3)]
        self.say("One common idea: high-priority queues get short slices, ten milliseconds or less, because interactive jobs alternate quickly.",
                 FadeIn(t2), Succession(*hops))

        # S14.7
        t0 = label("40 ms", 22, CPU_COLOR).move_to(lad.lane_point(0, 4.3))
        t1 = label("20 ms", 22, CPU_COLOR).move_to(lad.lane_point(1, 4.3))
        self.say("Low-priority queues hold CPU-bound jobs, so they get long slices, hundreds of milliseconds.",
                 Succession(FadeIn(t0, shift=UP * 0.2), FadeIn(t1, shift=UP * 0.2)), self.prof.change("explaining"), self.stu.change("neutral"))

        # S14.8
        self.say("In this example, the top queue has a ten-millisecond slice, the middle one twenty, the bottom one forty.",
                 Indicate(t2, color=CPU_COLOR), after(1.5, Indicate(t1, color=CPU_COLOR)), after(3.0, Indicate(t0, color=CPU_COLOR)))

        # S14.9
        spans = [("Q2", "A", 0, 1), ("Q2", "B", 1, 2), ("Q1", "A", 2, 4), ("Q1", "B", 4, 6)]
        s0 = 6
        n = "A"
        while s0 < 30:
            spans.append(("Q0", n, s0, min(s0 + 4, 30)))
            s0 += 4
            n = "B" if n == "A" else "A"
        fills = [tl.fill_span(r, b0, b1, "running", COL[j], run_time=0.35) for r, j, b0, b1 in spans]
        self.say("Two jobs run through the top, then the middle, then settle into long, uninterrupted runs at the bottom.",
                 Succession(*fills), FadeOut(panel))
        self.beat(1.5)
