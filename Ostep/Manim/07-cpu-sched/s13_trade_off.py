import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


class S13TradeOff(Ep07Scene):
    def construct(self):
        self.world(opened=(0, 1, 2), term="amortization", stu="curious", prof="worried")
        stu, prof = self.stu, self.prof
        w = build_rr_end()
        ch, title, sb0, clk, clklab, queue, ps = (w[k] for k in ("ch", "title", "sb", "clk", "clklab", "queue", "ps"))
        self.add(ch.group(), title, sb0, clk, clklab, queue, *ps)
        tl, sp = ch.tl, ch.sp
        turn = turn_brackets(tl, sp)
        mk = comp_markers(tl, sp)
        hidden = VGroup(*turn.values(), *mk.values())
        hidden.set_opacity(0)
        cg = VGroup(tl, *ch.br.values(), hidden)
        self.add(hidden)

        # shrink the chart into the left half (the S12 -> S13 hand-off)
        self.play(FadeOut(VGroup(sb0, clk, clklab, queue, *ps, ch.ro.shown)),
                  cg.animate.scale(0.55).move_to(P3(-3.2, 1.0)), run_time=1.0)

        # S13.1
        self.say("So Round Robin is great at response time. Now check its turnaround, with the same three jobs.",
                 FadeOut(VGroup(*ch.br.values())), *[turn[j].animate.set_opacity(1) for j in "ABC"], stu.change("neutral"))

        # S13.2
        self.say("A finishes at thirteen. B at fourteen. C at fifteen.",
                 LaggedStart(*[mk[j].animate.set_opacity(1) for j in "ABC"], lag_ratio=0.6, run_time=2.0))

        # S13.3
        ro = MetricReadout(["13", "14", "15"], 3, "14", center=(-3.2, -1.4), font_size=32)
        self.say("Average: fourteen seconds.", *ro.reveal_numerator(run_time=1.2))
        self.play(*ro.reveal_value(), run_time=0.6)
        self.play(*ro.frame_value(False), run_time=0.5)

        # S13.4
        ghost_ex = MathTex(r"\frac{5+10+15}{3}=", "10", font_size=30, color=DIM)
        ghost_ex[1].set_color(PERS)
        lab = Text("SJF:", font_size=24, color=DIM)
        gg = VGroup(lab, ghost_ex).arrange(RIGHT, buff=0.2).move_to(P3(-3.0, -2.75))
        self.say("SJF would have given ten (five, ten and fifteen).", FadeIn(gg, shift=UP * 0.2))

        # S13.5
        bad = x_mark(0.35).next_to(ro.box, RIGHT, buff=0.25)
        self.say("RR is one of the worst policies for turnaround, even worse than FIFO in many cases.",
                 Wiggle(ro.value_mob, scale_value=1.25, rotation_angle=0.05 * TAU), after(1.0, Create(bad)))

        # S13.6
        self.say("It stretches every job out as long as it can.",
                 LaggedStart(*[Indicate(turn[j], scale_factor=1.12, color=KERNEL_COLOR) for j in "ABC"], lag_ratio=0.4, run_time=2.0))

        # S13.7
        self.say("So which one is right?", stu.change("confused"))

        # S13.8
        sb = make_scoreboard([("SJF · STCF", True, False), ("RR", False, True)], width=5.0).move_to(P3(3.4, 1.6))
        piv = P3(3.4, -1.1)
        beam = Line(piv + LEFT * 1.8, piv + RIGHT * 1.8).set_stroke(TEXT, 6)
        tri = Triangle().scale(0.22).set_fill(DIM, 1).set_stroke(width=0).move_to(piv + DOWN * 0.22)
        lsj = Text("SJF", font_size=22, color=TEXT).next_to(beam.get_left(), UP, buff=0.12)
        lrr = Text("RR", font_size=22, color=TEXT).next_to(beam.get_right(), UP, buff=0.12)
        seesaw = VGroup(beam, lsj, lrr)
        self.say("Neither. That's a trade-off.",
                 prof.change("happy"), self.term("trade-off", hold=0.6), FadeIn(sb, shift=LEFT * 0.4),
                 after(1.2, FadeIn(tri), FadeIn(seesaw),
                            Rotate(seesaw, 0.2, about_point=piv, run_time=0.6),
                            Rotate(seesaw, -0.4, about_point=piv, run_time=0.9)))

        # S13.9
        hl = SurroundingRectangle(sb.row_groups[1], color=VIRT, buff=0.08)
        fair = Text("fair", font_size=26, color=VIRT).next_to(beam.get_end(), DOWN, buff=0.2).shift(RIGHT * 0.2)
        self.say("A policy that divides the CPU evenly (a fair one) does badly on turnaround.",
                 Create(hl), FadeIn(fair))

        # S13.10
        hl2 = SurroundingRectangle(sb.row_groups[0], color=VIRT, buff=0.08)
        self.say("A policy that runs short jobs to completion does well on turnaround, but makes others wait.",
                 ReplacementTransform(hl, hl2), FadeOut(fair, run_time=0.4), late(0.5, Rotate(seesaw, 0.4, about_point=piv, run_time=0.9)),
                 Indicate(tl.blocks_in("B"), scale_factor=1.1, run_time=1.5))

        # S13.11
        cake = cake_glyph(0.9).move_to(P3(3.4, -2.55))
        bite = Circle(radius=0.28).set_fill(BG, 1).set_stroke(width=0).move_to(cake.get_center() + UP * 0.25 + RIGHT * 0.45)
        self.say("You can't have your cake and eat it too.",
                 FadeIn(cake, shift=UP * 0.3), after(1.0, FadeIn(bite, scale=0.3)), prof.change("proud"))
        self.beat(0.6)
        self.fade_stage(self.badge, self.strip, stu, prof, run_time=0.8)
