import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403

MS = 0.063   # width of 1 ms in the amortization bars (visual ratio 1:10, 1:100)


def amort_bar(slice_ms, x_left, y, h=0.45):
    sl = Rectangle(width=slice_ms * MS, height=h).set_fill(COL["B"], 1).set_stroke(TEXT, 1)
    sv = Rectangle(width=1 * MS, height=h).set_fill(KERNEL_COLOR, 1).set_stroke(width=0)
    sl.move_to(P3(x_left + slice_ms * MS / 2, y))
    sv.next_to(sl, RIGHT, buff=0)
    g = VGroup(sl, sv)
    g.sl, g.sv = sl, sv
    return g


class S12HowShort(Ep07Scene):
    def construct(self):
        self.world(opened=(0, 1, 2), term="Round Robin", stu="curious", prof="happy")
        stu, prof = self.stu, self.prof
        w = build_rr_end()
        ch, title, sb, clk, clklab, queue, ps = (w[k] for k in ("ch", "title", "sb", "clk", "clklab", "queue", "ps"))
        self.add(ch.group(), title, sb, clk, clklab, queue, *ps)
        tl = ch.tl
        cg = VGroup(tl, *ch.br.values())
        cg.save_state()

        # S12.1
        lab2 = Text("0.1 s", font_size=24, color=CPU_COLOR)
        lab3 = Text("0.01 s", font_size=24, color=CPU_COLOR)
        fade = VGroup(ch.ro.shown, sb, queue, *ps)
        self.play(FadeOut(fade), cg.animate.scale(0.55).move_to(P3(0, 1.8)),
                  clk.animate.move_to(P3(-5.4, 0.8)), clklab.animate.move_to(P3(-4.7, 0.8)), run_time=1.0)
        dim = dimmer(cg, 0.05, 0.8)
        self.add(dim)
        self.allow_overlap(dim, cg, "the chart is dimmed on purpose")
        lab2.move_to(clklab.get_left(), aligned_edge=LEFT)
        lab3.move_to(clklab.get_left(), aligned_edge=LEFT)
        self.say("So make the slice really, really short?",
                 stu.change("curious"), FadeIn(dim),
                 after(0.8, Transform(clklab, lab2), Wait(0.4), Transform(clklab, lab3)))

        # S12.2
        cpu_i = len(tl.rows)
        slivers = VGroup(*[Rectangle(width=0.02, height=tl.block_at[(cpu_i, k)].height)
                           .set_fill(KERNEL_COLOR, 1).set_stroke(width=0)
                           .move_to(tl.block_at[(cpu_i, k)].get_right()) for k in range(1, 15)])
        thick = VGroup(*[Rectangle(width=0.1, height=sv.height).set_fill(KERNEL_COLOR, 1).set_stroke(width=0).move_to(sv)
                         for sv in slivers])
        self.say("Careful. Every switch costs time.",
                 prof.change("worried"), FadeIn(slivers), after(0.8, Transform(slivers, thick)))

        # S12.3
        y0 = -1.2
        axis = Line(P3(-3.5, y0), P3(3.5, y0)).set_stroke(DIM, 3)
        ticks = VGroup(*[Line(P3(-3.5 + k, y0 - 0.1), P3(-3.5 + k, y0 + 0.1)).set_stroke(DIM, 2) for k in range(8)])
        tlabs = VGroup(*[Text(f"{10 * k}", font_size=18, color=DIM).move_to(P3(-3.5 + k, y0 - 0.32)) for k in range(8)])
        msl = Text("ms", font_size=18, color=DIM).next_to(tlabs, RIGHT, buff=0.15)
        timer = ClockIcon(0.25, color=TEXT).move_to(P3(-4.5, y0))
        def slice_box(w, cx0):
            return Rectangle(width=w, height=0.4).set_fill(COL["B"], 1).set_stroke(TEXT, 1).move_to(P3(cx0, y0 + 0.9))
        b10, b20, b30 = slice_box(1.0, -3.0), slice_box(2.0, -1.5), slice_box(3.0, 1.0)
        b15 = Rectangle(width=1.5, height=0.4).set_fill(KERNEL_COLOR, 0.4).set_stroke(KERNEL_COLOR, 2).move_to(P3(3.0, y0 + 0.9))
        cx = x_mark(0.3).move_to(P3(3.4, y0 + 1.1))
        down = lambda m: m.animate(run_time=0.35).shift(DOWN * 0.6)
        snap = Succession(FadeIn(b10, shift=DOWN * 0.3), down(b10), FadeIn(b20, shift=DOWN * 0.3), down(b20),
                          FadeIn(b30, shift=DOWN * 0.3), down(b30), FadeIn(b15), b15.animate(run_time=0.3).shift(DOWN * 0.6),
                          b15.animate(run_time=0.4).shift(UP * 0.8 + RIGHT * 0.4), FadeIn(cx))
        self.say("The time slice has to be a multiple of the timer-interrupt period. If the timer fires every ten "
                 "milliseconds, the slice is ten, twenty, any multiple of ten.",
                 FadeIn(VGroup(axis, ticks, tlabs, msl, timer)), after(1.0, Indicate(timer, run_time=1.0)),
                 after(3.0, snap))
        self.play(FadeOut(VGroup(axis, ticks, tlabs, msl, timer, b10, b20, b30, b15, cx)), run_time=0.5)

        # S12.4
        card = TipCard(Rectangle(width=7.2, height=2.2).set_fill(opacity=0).set_stroke(width=0),
                       title="TIP: Amortization can reduce costs", width=8.0, height=3.5).move_to(P3(0, -1.1))
        cc = card.content_center()
        bar = amort_bar(10, cc[0] - 3.3, cc[1] + 0.3)
        l1 = Text("10 ms slice", font_size=18, color=COL["B"]).next_to(bar.sl, DOWN, buff=0.1)
        l2 = Text("1 ms switch", font_size=18, color=KERNEL_COLOR).next_to(bar.sv, UP, buff=0.1)
        pct = Text("10 %", font_size=54, color=KERNEL_COLOR).move_to(cc + P3(2.6, 0.3))
        self.say("And if a switch costs one millisecond and the slice is ten, then ten percent of the time is wasted.",
                 card.slide_in(UP), FadeIn(VGroup(bar, l1, l2, pct), shift=UP * 0.5))

        # S12.5
        bar100 = amort_bar(100, cc[0] - 3.3, cc[1] + 0.3)
        pct2 = Text("< 1 %", font_size=54, color=PERS).move_to(pct)
        l1b = Text("100 ms slice", font_size=18, color=COL["B"]).next_to(bar100.sl, DOWN, buff=0.1)
        l2b = Text("1 ms switch", font_size=18, color=KERNEL_COLOR).next_to(bar100.sv, UP, buff=0.1)
        pct2.move_to(cc + P3(0, -0.85))
        self.say("Make the slice a hundred, and the waste falls under one percent.",
                 Transform(bar, bar100), Transform(l1, l1b), Transform(l2, l2b), Transform(pct, pct2))

        # S12.6
        chain = VGroup(*[amort_bar(10, 0, 0) for _ in range(10)]).arrange(RIGHT, buff=0).move_to(cc + P3(0, -0.2))
        clab = Text("ten switches", font_size=20, color=KERNEL_COLOR).next_to(chain, DOWN, buff=0.1)
        chain_g = VGroup(chain, clab)
        bar_g = VGroup(bar, l1, l2, pct)
        with self.narrate("That's amortization: if an operation has a fixed cost, do it less often."):
            self.play(self.term("amortization", hold=0.6), after(1.5, FadeOut(bar_g, run_time=0.4)))
            self.play(FadeIn(chain_g), run_time=0.4)
            self.wait(1.0)
            self.play(FadeOut(chain_g), run_time=0.4)
            self.play(FadeIn(bar_g), run_time=0.4)

        # S12.7
        slot = save_slot(0.7).move_to(P3(-4.2, -0.8))
        cpu = CPU(1.2, label=None, pins=3).move_to(P3(0, -0.5))
        cache = VGroup(*[Rectangle(width=0.45, height=0.3).set_fill(CPU_COLOR, 0.8).set_stroke(TEXT, 1) for _ in range(4)])
        cache.arrange(RIGHT, buff=0.1).next_to(cpu, RIGHT, buff=0.3)
        cl = Text("cache", font_size=20, color=DIM).next_to(cache, UP, buff=0.1)
        wu = Text("warm-up", font_size=26, color=CPU_COLOR).next_to(cache, DOWN, buff=0.35)
        refill = Succession(*[cache[k].animate(run_time=0.5).set_fill(CPU_COLOR, 0.8) for k in range(4)])
        self.say("The cost of a switch is also more than saving registers. The caches and other hardware state "
                 "have to be warmed up all over again.",
                 card.slide_out(DOWN), FadeOut(bar_g), FadeIn(slot),
                 after(1.0, Indicate(slot, run_time=1.0),
                            AnimationGroup(FadeIn(cpu), FadeIn(cache), FadeIn(cl)), Wait(0.5),
                            AnimationGroup(*[c.animate.set_fill(DIM, 0.15) for c in cache]),
                            AnimationGroup(FadeIn(wu), refill)))
        lab1 = Text("1 s", font_size=24, color=CPU_COLOR).move_to(CLOCK_AT + RIGHT * 0.45 + RIGHT * 0.3, aligned_edge=LEFT).shift(LEFT * 0.3)
        self.play(FadeOut(VGroup(slot, cpu, cache, cl, wu, dim, slivers)), Restore(cg), FadeIn(fade),
                  clk.animate.move_to(CLOCK_AT), Transform(clklab, lab1), run_time=1.2)
        self.beat(0.4)
