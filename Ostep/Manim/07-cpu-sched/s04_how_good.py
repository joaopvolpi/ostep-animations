import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


def tx(*parts, size=38):
    m = MathTex(*parts, font_size=size)
    return m


class S04HowGood(Ep07Scene):
    def construct(self):
        self.world(stu="neutral", prof="happy")
        stu, prof, strip = self.stu, self.prof, self.strip
        tl = make_gantt(12, 10)

        # S04.1
        sample = Rectangle(width=2.2, height=0.5).set_fill(COL["A"], 1).set_stroke(TEXT, 1).move_to(P3(0, 0.3))
        ruler = ruler_glyph(2.4).move_to(P3(-2.2, -0.35))
        self.say("To compare policies, we need a scheduling metric: a number that measures how well a schedule does.",
                 self.term("scheduling metric", hold=0.8), FadeIn(sample),
                 after(1.0, FadeIn(ruler), ruler.animate(run_time=2.0).move_to(P3(0.6, -0.35))))
        self.play(FadeOut(VGroup(sample, ruler)), run_time=0.4)

        # S04.2
        self.say("For now, we'll use exactly one. Turnaround time.",
                 self.term("turnaround time", hold=0.6),
                 after(0.8, AnimationGroup(Create(tl.grid), FadeIn(tl.row_labels), FadeIn(tl.tick_labels))))

        # S04.3
        arr = tl.arrival_marker("A", 0, "arrives")
        blk = Rectangle(width=6 * CELL10, height=G_RH).set_fill(COL["A"], 1).set_stroke(TEXT, 1)
        blk.move_to(P3(GX[0] + 3 * CELL10, tl.row_y("A")))
        comp = tl.arrival_marker("A", 6, "completes")
        br = tl.bracket("A", 0, 6, "turnaround", gap=0.4)
        sw = stopwatch_icon(0.22).move_to(P3(-6.2, 1.9))
        self.say("It's the time at which a job completes, minus the time at which it arrived.",
                 Succession(FadeIn(arr, shift=DOWN * 0.2), Wait(0.3), GrowFromEdge(blk, LEFT, run_time=1.2),
                            FadeIn(comp, shift=DOWN * 0.2)),
                 after(2.2, Create(br.line), FadeIn(br.caps), FadeIn(br.label)),
                 FadeIn(sw),
                 after(1.5, Rotate(sw.hand, -TAU * 0.9, about_point=sw[0].get_center(), run_time=2.0)))

        # S04.4
        f = tx(r"T_{turnaround}", "=", r"T_{completion}", "-", r"T_{arrival}")
        f[2].set_color(PERS)
        f[4].set_color(INTRO)
        f.move_to(P3(0, -2.4))
        self.play(Write(f), run_time=1.6)
        self.beat(0.5)

        # S04.5
        f_red = tx(r"T_{turnaround}", "=", r"T_{completion}").move_to(P3(0, -2.4))
        f_red[2].set_color(PERS)
        zero = tx("0").move_to(f[4])
        with self.narrate("Since we've assumed every job arrives at time zero, turnaround is just completion time."):
            self.play(Transform(f[4], zero), run_time=1.0)
            self.play(FadeOut(VGroup(f[3], f[4])), Transform(VGroup(f[0], f[1], f[2]), f_red), run_time=1.0)
            self.play(strip.locks[1].pulse(), run_time=1.0)

        # S04.6
        f_full = tx(r"T_{turnaround}", "=", r"T_{completion}", "-", r"T_{arrival}").move_to(P3(0, -2.4))
        f_full[2].set_color(PERS)
        f_full[4].set_color(INTRO)
        with self.narrate("That fact will change when we relax the assumptions."):
            self.play(FadeOut(VGroup(f[0], f[1], f[2])), FadeIn(f_full), run_time=0.6)
            self.wait(0.6)
            self.play(FadeOut(f_full), FadeOut(VGroup(blk, arr, comp, br, sw)), run_time=0.8)

        # S04.7
        dim = dimmer(VGroup(tl), 0.9, 0.85)
        perf = VGroup(RoundedRectangle(width=2.8, height=2.0, corner_radius=0.15).set_fill(CARD_FILL, 1).set_stroke(CONC, 3),
                      gauge_glyph(1.1), Text("performance", font_size=24, color=TEXT))
        perf[1].move_to(perf[0].get_center() + UP * 0.15)
        perf[2].move_to(perf[0].get_bottom() + UP * 0.35)
        fair = VGroup(RoundedRectangle(width=2.8, height=2.0, corner_radius=0.15).set_fill(CARD_FILL, 1).set_stroke(VIRT, 3),
                      scale_glyph(1.2), Text("fairness", font_size=24, color=TEXT))
        fair[1].move_to(fair[0].get_center() + UP * 0.15)
        fair[2].move_to(fair[0].get_bottom() + UP * 0.35)
        perf.move_to(P3(-2.2, 0.4))
        fair.move_to(P3(2.2, 0.4))
        for m in (perf, fair):
            m.set_z_index(30)
        self.allow_overlap(VGroup(perf, fair), tl, "cards fade in over the dimmed chart")
        self.say("Turnaround is a performance metric. The other big family is fairness.",
                 prof.change("explaining"), FadeIn(dim, run_time=0.6), late(0.6, FadeIn(perf)),
                 late(0.6, FadeIn(fair, shift=LEFT * 0.3)),
                 self.term("fairness", hold=0.6))

        # S04.8
        beam = Line(P3(-2.2, -1.1), P3(2.2, -1.1)).set_stroke(TEXT, 5)
        pivot = Triangle().scale(0.18).set_fill(DIM, 1).set_stroke(width=0).move_to(P3(0, -1.28))
        starved = proc("C", "blocked", scale=0.5).move_to(P3(4.9, -0.9))
        stag = Text("starved?", font_size=22, color=DIM).next_to(starved, UP, buff=0.05)
        self.say("And the two tend to fight: a scheduler can maximize performance by starving a few jobs, "
                 "which isn't fair at all.",
                 stu.change("curious"), FadeIn(pivot), Create(beam),
                 after(2.0, AnimationGroup(Rotate(beam, 0.18, about_point=P3(0, -1.1)),
                                                      perf.animate.shift(UP * 0.15), fair.animate.shift(DOWN * 0.15),
                                                      FadeIn(starved), FadeIn(stag))))
        self.play(FadeOut(VGroup(perf, fair, beam, pivot, starved, stag, dim)), run_time=0.8)
