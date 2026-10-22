import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


class S09STCF(Ep07Scene):
    def construct(self):
        self.world(opened=(0, 1), term="non-preemptive", stu="curious", prof="worried")
        stu, prof, strip = self.stu, self.prof, self.strip
        late = Chart("late")
        bars = bars_labelled()
        title = policy_title("SJF")
        arrs = VGroup(late.tl.arrival_marker("A", 0, "arrives", dx=0.05),
                      late.tl.arrival_marker("B", 1, "[B, C arrive]", label_side=LEFT),
                      late.tl.arrival_marker("C", 1))
        self.add(late.group(), bars, title, arrs)
        tl = late.tl
        st = Chart("stcf")
        run, arr = st.sp["run"], st.sp["arrive"]
        ro = st.ro
        ro.shown = VGroup()

        # S09.1
        dim = dimmer(late.group(), 0.1, 0.8)
        self.say("To fix this, we relax the third assumption: jobs don't have to run to completion.",
                 strip.locks[2].open(), FadeIn(dim), prof.change("explaining"))

        # S09.2
        card = AsideCard(Rectangle(width=6.8, height=2.4).set_fill(opacity=0).set_stroke(width=0),
                         title="ASIDE: Preemptive schedulers", width=7.8, height=4.0).move_to(P3(0, 0.2))
        cc = card.content_center()
        cpu = CPU(1.0, label=None, pins=2).move_to(cc + DOWN * 0.15)
        pa = proc("A", "running", scale=0.45)
        bottom_to(pa, cpu.slot_point() + UP * 0.02)
        pb = proc("B", scale=0.45)
        bottom_to(pb, cc + P3(-2.6, -0.85))
        half = VGroup(Rectangle(width=1.2, height=0.3).set_fill(COL["A"], 0.15).set_stroke(COL["A"], 2),
                      Rectangle(width=0.6, height=0.3).set_fill(COL["A"], 1).set_stroke(COL["A"], 2).shift(LEFT * 0.3))
        half.move_to(cc + P3(2.6, -0.7))
        inside = VGroup(cpu, pa, pb)
        self.say("The scheduler can stop A, run something else, and come back later. That's preemption.",
                 card.slide_in(RIGHT), FadeIn(inside, shift=LEFT * 1.5),
                 Succession(Wait(2.0), hop_bottom(pa, half.get_bottom() + UP * 0.0, run_time=0.8),
                            AnimationGroup(FadeOut(pa), FadeIn(half)),
                            hop_bottom(pb, cpu.slot_point() + UP * 0.02, run_time=0.8)),
                 Succession(Wait(3.0), self.term("preemption", hold=0.6)))

        # S09.3
        l1 = Text("non-preemptive (old batch)", font_size=22, color=DIM).move_to(cc + P3(-2.0, -1.5))
        l2 = Text("preemptive (modern)", font_size=22, color=PERS, weight=BOLD).move_to(cc + P3(2.0, -1.5))
        clock = ClockIcon(0.25).next_to(l2, UP, buff=0.12).shift(LEFT * 0.5)
        gears = GearPair(0.2).next_to(l2, UP, buff=0.12).shift(RIGHT * 0.5)
        e6 = ep_tag("Ep. 06", font_size=16).next_to(gears, RIGHT, buff=0.1)
        glow = SurroundingRectangle(l2, color=PERS, buff=0.1, corner_radius=0.08)
        self.say("Old batch systems were non-preemptive. Virtually every modern scheduler is preemptive, and it "
                 "uses exactly the machinery we built last time: the timer interrupt and the context switch.",
                 FadeIn(l1), FadeIn(l2), Succession(Wait(2.5), Create(glow)),
                 Succession(Wait(4.0), AnimationGroup(FadeIn(clock), FadeIn(gears), FadeIn(e6))),
                 Succession(Wait(1.5), self.term("preemptive", hold=0.6)))
        gone = VGroup(card, inside, half, l1, l2, clock, gears, e6, glow)
        old = VGroup(*late.br.values(), *late.mk.values(), late.ro.shown, arrs)
        self.play(FadeOut(gone, shift=RIGHT * 1.5), FadeOut(dim), tl.clear_blocks(0.8), FadeOut(old), run_time=0.9)
        tl.purge()

        # S09.4
        alias = Text("= PSJF", font_size=22, color=DIM).next_to(title, RIGHT, buff=0.2)
        self.say("Add preemption to SJF and you get Shortest Time-to-Completion First, STCF (also called PSJF).",
                 Transform(title, policy_title("STCF")), self.term("STCF", hold=0.8), Succession(Wait(3.0), FadeIn(alias)))

        # S09.5
        spot = Spotlight(height=0.7, spread=0.3)
        spot.move_beam_to(P3(-3.0, BARS_Y - 0.15))
        tl_lab = Text("time left", font_size=20, color=DIM).move_to(P3(-3.0, 2.85))
        self.say("Whenever a new job arrives, run whichever job has the least time left.",
                 FadeIn(spot), FadeIn(tl_lab))

        # S09.6
        a2 = tl.arrival_marker("B", 1, "[B, C arrive]", label_side=LEFT)
        a3 = tl.arrival_marker("C", 1)
        self.say("B and C arrive at ten. A has ninety seconds left.",
                 *cell_anims(tl, run, arr, 1, run_time=0.8),
                 Succession(Wait(1.0), AnimationGroup(FadeIn(a2, shift=DOWN * 0.2), FadeIn(a3, shift=DOWN * 0.2),
                                                       Transform(bars[0], bar_to(bars[0], 9, CELL10, "90 s")))))

        # S09.7
        pause = PauseGlyph(0.25).move_to(tl.cell_center("A", 1) + UP * 0.0)
        with self.narrate("So A is preempted. B runs, then C, then A finishes."):
            self.play(spot.animate.move_beam_to(bars[1].get_center() + DOWN * 0.15), FadeIn(pause), run_time=0.8)
            self.play(*cell_anims(tl, run, arr, 2, run_time=0.5), FadeOut(bars[1]), FadeOut(pause), run_time=0.5)
            self.play(*cell_anims(tl, run, arr, 3, run_time=0.5), spot.animate.move_beam_to(bars[2].get_center() + DOWN * 0.15),
                      FadeOut(bars[2]), run_time=0.5)
            self.play(spot.animate.move_beam_to(P3(-3.0, BARS_Y - 0.15)), run_time=0.5)
            for t in range(4, 13):
                self.play(*cell_anims(tl, run, arr, t, run_time=0.18), run_time=0.18)
            self.play(FadeOut(VGroup(spot, tl_lab, bars[0])), run_time=0.4)

        # S09.8
        self.say("Completions: one-twenty, twenty, thirty.",
                 LaggedStart(*[FadeIn(st.mk[j], shift=DOWN * 0.4) for j in "ABC"], lag_ratio=0.5, run_time=1.5))

        # S09.9
        anims = []
        for j in "ABC":
            b = st.br[j]
            anims += [Create(b.line), FadeIn(b.caps), FadeIn(b.label)]
        self.say("Turnarounds: one-twenty, ten, and twenty.", *anims)

        # S09.10
        self.say("Average: fifty seconds. And given our assumptions, STCF is provably optimal.",
                 *ro.reveal_numerator(run_time=1.6), stu.change("excited"))
        self.play(*ro.reveal_value(), run_time=0.8)
        self.play(*ro.frame_value(True), run_time=0.6)
        tag = VGroup(Star(5, outer_radius=0.14).set_fill(CPU_COLOR, 1).set_stroke(width=0),
                     Text("optimal", font_size=24, color=PERS)).arrange(RIGHT, buff=0.1).move_to(P3(2.0, 3.1))
        self.play(FadeIn(tag, scale=1.4), run_time=0.6)
        self.beat(0.6)
