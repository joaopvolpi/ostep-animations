import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from manim import *  # noqa: E402,F403
from ostep_lib import *  # noqa: E402,F403
from common import *  # noqa: E402,F403


class S04FetchDecodeExecute(NarratedScene):
    def construct(self):
        # S03 end state
        stu, prof = make_hosts("dialog", stu_expr="neutral", prof_expr="happy")
        strip = card_strip(piece_cards())
        lines = motto_lines()
        lines[1].set_color(INTRO)
        glow = glow_for(lines[1])
        note = Text("attributed to Confucius; closer to Xunzi", font_size=20, color=DIM)
        note.next_to(lines, DOWN, buff=0.3).shift(LEFT * 0.4)
        self.add(stu, prof, strip, lines, glow, note)

        th = terms(INTRO)
        th.at = np.array([-0.9, 3.0, 0])
        bdg = badge(INTRO)
        cpu = s04_cpu()
        mem = s04_memory()
        ring = fde_ring([-2.8, -1.8, 0])

        # S04.1
        self.say("Let's start at the bottom. What happens when a program runs?",
                 FadeOut(VGroup(strip, lines, glow, note)), *mode_anims(stu, prof, "corner"),
                 Succession(Wait(0.6), AnimationGroup(FadeIn(bdg), Create(cpu), Create(mem), run_time=1.4)))
        self.play(FadeIn(ring), cpu.label.animate.set_opacity(0.0), run_time=0.6)

        # S04.2 fetch
        pc = pc_arrow(mem, 0)
        cur = mem.texts[0].copy()
        with self.narrate("Something very simple. The processor fetches an instruction from memory."):
            self.play(FadeIn(pc, shift=RIGHT * 0.3), run_time=0.5)
            self.play(th.write("fetch"), light(ring, 0), run_time=0.8)
            self.play(cur.animate.move_to(cpu.die).scale_to_fit_width(cpu.die.width * 0.85).set_color(INK),
                      run_time=1.0)
            self.wait(0.6)
            self.play(th.dock_anim())

        # S04.3 decode
        add = Text("ADD", font_size=30, color=INK, weight=BOLD).move_to(cpu.die)
        with self.narrate("It decodes it, figuring out which instruction this is."):
            self.play(ReplacementTransform(cur, add), light(ring, 1), run_time=0.8)
            self.play(th.write("decode"), run_time=0.8)
            self.wait(0.6)
            self.play(th.dock_anim())

        # S04.4 execute
        calc = Text("2 + 3 → 5", font_size=22, color=INK, weight=BOLD).move_to(cpu.die)
        with self.narrate("Then it executes it: add two numbers, access memory, check a condition, jump to a function."):
            self.play(light(ring, 2), FadeOut(add), FadeIn(calc, scale=1.3), run_time=0.7)
            self.play(Indicate(calc, color=VIRT), run_time=0.6)
            self.play(th.write("execute"), FadeOut(calc), run_time=0.8)
            self.wait(0.8)
            self.play(th.dock_anim())

        def cycle(i, rt=0.8):
            """One fetch-decode-execute pass on cell i (PC moves first)."""
            fly = mem.texts[i].copy()
            self.play(pc.animate.next_to(mem.cell(i), LEFT, buff=0.45), run_time=rt * 0.2)
            self.play(light(ring, 0), fly.animate.move_to(cpu.die).scale_to_fit_width(cpu.die.width * 0.85)
                      .set_color(INK), run_time=rt * 0.3)
            self.play(light(ring, 1), fly.animate.scale(1.1), run_time=rt * 0.2)
            self.play(light(ring, 2), FadeOut(fly, scale=0.5), run_time=rt * 0.3)

        # S04.5
        with self.narrate("Then it moves on to the next instruction. And the next."):
            cycle(1)
            cycle(2)

        # S04.6 accelerate
        tr = ValueTracker(0)
        ctr = counter_text(tr, pos=[-2.8, 1.85, 0], font_size=22, color=CPU_COLOR)
        with self.narrate("Millions, these days billions, of times per second,"):
            self.add(ctr)
            rts = [0.6, 0.45, 0.35, 0.35]
            for k, i in enumerate((3, 4, 5, 6)):
                cycle(i, rts[k])
            blur = VGroup(*[b[0].copy().set_fill(CPU_COLOR, 0.25).set_stroke(CPU_COLOR) for b in ring.boxes])
            self.play(tr.animate.set_value(3_000_000_000), FadeIn(blur), pc.animate.set_opacity(0.4),
                      rate_func=rush_into, run_time=1.6)
            self.play(FadeOut(blur), pc.animate.set_opacity(1), run_time=0.3)

        # S04.7
        with self.narrate("until the program finishes."):
            self.play(pc.animate.next_to(mem.cell(7), LEFT, buff=0.45), light(ring, 2), run_time=0.4)
            self.play(Indicate(mem.cells[7], color=CPU_COLOR), run_time=0.6)
            self.play(*[b[0].animate.set_stroke(DIM).set_fill(CARD_FILL, 1) for b in ring.boxes],
                      *[b[1].animate.set_color(DIM) for b in ring.boxes], run_time=0.3)
            self.beat(0.5)

        # S04.8
        self.say("That's the Von Neumann model of computing.",
                 FadeOut(ctr), th.show("Von Neumann model", hold=1.0), min_time=2.6)

        # S04.9 chaos, then the curtain
        die = cpu.die
        dashes = VGroup()
        rng = np.random.default_rng(3)
        for k in range(10):
            d = Line(LEFT * 0.12, RIGHT * 0.12).set_stroke(PROCESS_COLORS[k % 6], 5)
            d.move_to(die.get_center() + np.array([rng.uniform(-0.4, 0.4), rng.uniform(-0.4, 0.4), 0]))
            d.rotate(rng.uniform(0, PI))
            dashes.add(d)
        curtain = RoundedRectangle(width=1.9, height=1.9, corner_radius=0.15).set_fill(CARD_FILL, 1).set_stroke(INTRO, 3)
        curtain.move_to(cpu)
        neat = fde_ring(ORIGIN, w=0.75, gap=0.18, font_size=14)
        ring_lit(neat, 0)
        neat.scale_to_fit_width(1.6).move_to(curtain)
        cap = Text("the appearance: one at a time, in order", font_size=20, color=INTRO)
        cap.next_to(cpu, UP, buff=0.35)
        with self.narrate("Modern processors play some wild tricks under the hood to go faster, but they keep up "
                          "the appearance of exactly this: one instruction at a time, in order."):
            self.play(FadeIn(dashes, lag_ratio=0.1), run_time=0.4)
            for _ in range(3):
                self.play(*[d.animate.move_to(die.get_center() + np.array([rng.uniform(-0.42, 0.42),
                                                                          rng.uniform(-0.42, 0.42), 0]))
                            .rotate(rng.uniform(-1, 1)) for d in dashes], run_time=0.37)
            self.play(FadeIn(curtain, shift=DOWN * 0.8), FadeIn(neat, shift=DOWN * 0.8), run_time=0.8)
            self.remove(dashes)
            self.play(FadeIn(cap), run_time=0.5)
            for j in range(4):
                self.play(light(neat, (j + 1) % 3), run_time=0.4)

        # S04.10
        self.say("Sounds simple.", stu.change("bored"),
                 FadeOut(VGroup(curtain, neat, cap), shift=UP * 0.6), min_time=1.2)

        # S04.11
        p2, p3 = other_program(0), other_program(1)
        p2.move_to([5.2, 1.5, 0])
        p3.move_to([5.2, -0.75, 0])
        for p in (p2, p3):
            for c in p.cells:
                c.set_stroke(DIM)
        aims = VGroup(*[DashedLine(p.get_left(), cpu.get_right() + RIGHT * 0.1, dash_length=0.12)
                        .add_tip(tip_length=0.18).set_color(DIM) for p in (p2, p3)])
        aims.set_z_index(-1)
        self.say("It is. Until you want to run more than one of them.",
                 prof.change("thinking"), FadeIn(p2, shift=LEFT * 0.6), FadeIn(p3, shift=LEFT * 0.6),
                 Succession(Wait(0.6), Create(aims, run_time=0.8)))
        self.beat(0.8)
