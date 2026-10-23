import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from lottery_world import *  # noqa: E402,F401,F403


class S09TheRulerView(Ep09Scene):
    def construct(self):
        self.world(stu="neutral", prof="neutral")
        stu, prof = self.stu, self.prof
        W = build_s08()
        cw, jl, bars, total, drum, dlab, cpu = (W[k] for k in ("cw", "jl", "bars", "total", "drum", "dlab", "cpu"))
        # S08 end state
        bar = cw.add_bar(CPU_COLOR, line=7)
        cnt, win = counter_text(400), winner_text(300)
        ptr = jl.pointer(2)
        jl.nodes[2][0].set_stroke(CPU_COLOR, 5)
        self.add(cw, bar, jl, bars, total, drum, dlab, cpu, cnt, win, ptr)
        pc = proc("C", scale=0.4, label="")
        pc.move_to(cpu.slot_point() + (pc.get_center() - base_point(pc)))
        self.add(pc)

        # S09.1
        strip = NumberStrip(400, [("A", 100, COL["A"]), ("B", 50, COL["B"]), ("C", 250, COL["C"])],
                            x_range=(-5.5, 5.5), y=0.4, ticks=[0, 100, 150, 400], height=0.5)
        for n in strip.order:
            strip.segs[n].set_opacity(0)
            strip.seg_labels[n].set_opacity(0)
        self.add(strip)
        gone = VGroup(cw, bar, cnt, win, drum, dlab, cpu, pc, total, ptr, bars, jl.head, jl.head_arrow, jl.arrows, jl.null,
                      *jl.captions)
        self.say("It's like laying the tickets end to end on a ruler…",
                 stu.change("excited"), FadeOut(gone),
                 AnimationGroup(*[Transform(jl.nodes[i], strip.segs[n].copy().set_opacity(0.9)) for i, n in enumerate("ABC")]),
                 AnimationGroup(*[strip.seg_labels[n].animate.set_opacity(1) for n in strip.order]),
                 FadeIn(strip.line), FadeIn(strip.tick_labels))
        for n in strip.order:
            strip.segs[n].set_opacity(0.9)
        self.remove(*jl.nodes)

        # S09.2
        mk = strip.marker_at(300)
        mk_hi = mk.copy().shift(UP * 1.5).set_opacity(0)
        self.add(mk_hi)
        self.say("…and seeing whose stretch the winner lands on!",
                 Transform(mk_hi, mk.set_opacity(1)),
                 Succession(Wait(1.5), Indicate(strip.segs["C"], color=CPU_COLOR, scale_factor=1.05)))

        # S09.3
        self.say("That's the picture.", prof.change("happy"))

        # S09.4
        tip = VGroup(card_rect(4.6, 0.55, DIM), Text("TIP: sort by tickets", font_size=22, color=TEXT))
        tip[1].move_to(tip[0])
        tip.move_to(P3(0, -2.55))
        jl2 = JobList(JOBS, at=(-2.0, -1.2), gap=2.0, radius=0.3, font_size=16)
        self.say("A tip: sort the list from most tickets to fewest.",
                 FadeIn(tip, shift=UP * 0.2), FadeIn(jl2),
                 Succession(Wait(1.2), strip.reorder(["C", "A", "B"], run_time=1.2),
                            jl2.reorder([2, 0, 1], run_time=1.2)))

        # S09.5
        hops = Text("unsorted: 3 hops → sorted: 1 hop", font_size=22, color=TEXT).move_to(P3(0, -3.1))
        ok = tick_mark(0.3).next_to(hops, RIGHT, buff=0.2)
        self.say("It doesn't change correctness, but the big holders get found early, so you walk fewer nodes.",
                 FadeIn(hops), Succession(Wait(1.0), FadeIn(ok)))
        self.beat(0.8)
        # transition
        self.play(FadeOut(VGroup(strip, mk_hi, jl2, tip, hops, ok)), run_time=0.8)
