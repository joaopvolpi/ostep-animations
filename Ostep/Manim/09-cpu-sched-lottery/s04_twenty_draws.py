import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


def owner_of(n):
    return "A" if n < 75 else "B"


class S04TwentyDraws(Ep09Scene):
    def construct(self):
        self.world(term="lottery scheduling", pie=True)
        stu, prof, pie = self.stu, self.prof, self.pie
        W = build_s03_world()
        cpu, drum, a, b, sa, sb, strip = (W[k] for k in ("cpu", "drum", "a", "b", "sa", "sb", "strip"))
        labs = strip_labels(strip)
        total = Text("total: 100", font_size=20, color=DIM).move_to(P3(5.75, STRIP3_Y - 0.42))
        mk = strip.marker_at(63)
        cap = caption_at("tickets = share", y=-2.45, size=26)
        stu.set_expression("excited")
        hop_to(a, cpu.slot_point()).begin()
        a.move_to(cpu.slot_point() + (a.get_center() - base_point(a)))
        self.add(cpu, drum, a, b, sa, sb, strip, labs, total, mk)

        # S04.1
        tl = Timeline(["CPU"], ticks=20, x_range=(-3.8, 5.0), top=-2.0, row_height=0.42, row_kinds=["cpu"],
                      tick_labels=False, label_font=20)
        tally = Text("A: 0 · B: 0", font_size=24, color=TEXT, font=MONO_FONT).move_to(P3(-3.4, -1.4))
        self.say("Let's draw twenty.", FadeOut(cap), FadeOut(total), Create(tl), FadeIn(tally),
                 FadeOut(mk), stu.change("neutral"))
        # tally helper
        counts = {"A": 0, "B": 0}

        def tally_to(newtxt):
            return Transform(tally, Text(newtxt, font_size=24, color=TEXT, font=MONO_FONT).move_to(tally))

        # S04.2
        def one(i, num, who, rt):
            m = strip.marker_at(num).set_opacity(1)
            counts[who] += 1
            return Succession(
                AnimationGroup(FadeIn(m, scale=0.5), Flash(strip.segs[who], color=COL[who], flash_radius=0.3, run_time=rt)
                               if False else Indicate(strip.segs[who], color=COL[who], scale_factor=1.03, run_time=rt)),
                tl.fill("CPU", i, "running", color=COL[who], run_time=rt * 0.6),
                FadeOut(m, run_time=rt * 0.3))

        with self.narrate("Sixty-three: A. Eighty-five: B. Seventy: A. Thirty-nine: A. Seventy-six: B."):
            for i, (n, who) in enumerate(DRAWS, 1):
                ball, anim = drum.draw(n, COL[who], run_time=0.5)
                self.play(anim, run_time=0.5)
                self.play(FadeOut(ball), one(i, n, who, 0.4), run_time=0.8)

        # S04.3
        with self.narrate("And so on."):
            for k, (n, who) in enumerate(zip(REST_NUMS, REST), 6):
                self.play(one(k, n, who, 0.2), run_time=0.25)

        # S04.4
        brace_row = VGroup(*[tl.block_at[(0, t)] for t in range(1, 21) if RUN20[t - 1] == "B"])
        br = Brace(tl, DOWN, buff=0.08, color=COL["B"])
        brl = Text("4 / 20 = 20%", font_size=22, color=COL["B"]).next_to(br, DOWN, buff=0.08)
        self.say("After twenty slices, A has run sixteen times and B four.",
                 tally_to("A: 16 · B: 4"), FadeIn(br), FadeIn(brl), Indicate(brace_row, color=COL["B"]))

        # S04.5
        neq = Text("20% ≠ 25%", font_size=22, color=KERNEL_COLOR).move_to(P3(6.0, 0.9))
        neq = VGroup(Text("20%", font_size=22, color=COL["B"]), MathTex(r"\neq", font_size=30, color=KERNEL_COLOR),
                     Text("25%", font_size=22, color=DIM)).arrange(RIGHT, buff=0.1).move_to(P3(5.9, 0.75))
        self.say("Four out of twenty. That's twenty percent, not twenty-five.",
                 stu.change("confused"), pie.pulse(), FadeIn(neq))

        # S04.6
        note = Text("probabilistic, not guaranteed", font_size=22, color=TEXT).move_to(P3(0, -3.3))
        self.say("Right. Lottery scheduling is probabilistically correct, not guaranteed.",
                 prof.change("explaining"), FadeOut(brl), Write(note.move_to(br.get_bottom() + DOWN * 0.3)))

        # S04.7
        bar_bg = Rectangle(width=3.6, height=0.2).set_fill(COL["B"], 0.9).set_stroke(TEXT, 1).move_to(P3(1.8, -1.4))
        bar_a = Rectangle(width=3.6 * 0.8, height=0.2).set_fill(COL["A"], 0.9).set_stroke(TEXT, 1)
        bar_a.align_to(bar_bg, LEFT).match_y(bar_bg)
        dotted = DashedLine(bar_bg.get_top() + LEFT * 3.6 * (0.5 - 0.75) + UP * 0.12,
                            bar_bg.get_bottom() + LEFT * 3.6 * (0.5 - 0.75) + DOWN * 0.12, color=TEXT, dash_length=0.05)
        dotted.shift(UP * 0.0)
        rng = np.random.default_rng(3)
        more = rng.random(40) < 0.75
        self.say("The longer the two jobs compete, the closer they get to seventy-five and twenty-five.",
                 FadeOut(br), FadeOut(note), FadeOut(neq),
                 FadeIn(bar_bg), FadeIn(bar_a), Create(dotted),
                 Succession(tl.extend(60, run_time=0.8)))
        a_ct = 16
        with self.narrate(""):
            for k in range(21, 61):
                who = "A" if more[k - 21] else "B"
                a_ct += who == "A"
                frac = a_ct / k
                self.play(tl.fill("CPU", k, "running", color=COL[who], run_time=0.08),
                          bar_a.animate.stretch_to_fit_width(3.6 * frac, about_edge=LEFT), run_time=0.1)
        self.beat(1.0)
