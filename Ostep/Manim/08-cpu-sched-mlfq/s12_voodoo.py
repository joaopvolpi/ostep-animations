import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


class S12Voodoo(Ep08Scene):
    def construct(self):
        self.build(lanes=None, cpu=False, rules=("R1", "R2", "R3", "R4a", "R4b", "R5"), stu="curious", prof="explaining",
                   term="priority boost")
        board = self.board
        board.set_opacity(0.3)
        tl_l, tl_r = make_half(LEFT_X), make_half(RIGHT_X)
        set_cells(tl_l, FIG82[:2]); set_cells(tl_r, FIG84_RIGHT)
        pan = VGroup(tl_l, tl_r).set_opacity(0.3)
        self.add(pan)

        # S12.1
        dial = Dial(1.0, "S", 0.5)
        dial.shift(P3(-1.5, 1.2) - dial.hub.get_center())
        self.say("So what should S be?",
                 Create(dial.arc), FadeIn(dial.ticks), FadeIn(dial.needle), FadeIn(dial.hub), Write(dial.label))

        # S12.2
        sparks = VGroup(*[label("?", 24, CPU_COLOR).move_to(dial.hub.get_center() + UP * 0.5 + RIGHT * (i - 1.5) * 0.45) for i in range(4)])
        ends = [LEFT * 1.3 + UP * 0.6, RIGHT * 1.3 + UP * 0.6, LEFT * 0.5 + UP * 1.0, RIGHT * 0.6 + UP * 1.1]
        self.say("Hard question.", dial.wiggle(run_time=1.6),
                 Succession(Wait(0.4), AnimationGroup(*[Succession(FadeIn(s), s.animate(run_time=0.8).shift(e).set_opacity(0)) for s, e in zip(sparks, ends)])))
        self.remove(sparks)

        # S12.3
        vg = voodoo_glyph(0.7).move_to(P3(-3.4, 1.5))
        self.say("John Ousterhout called values like this voodoo constants, because they seem to need black magic to set.",
                 self.note("voodoo constants"), FadeIn(vg, shift=DOWN * 0.3), dial.swing_to(0.5))

        # S12.4
        sad = VGroup(job("A", 0.5), label("starved", 18, KERNEL_COLOR)).arrange(DOWN, buff=0.05).move_to(P3(1.3, 1.2))
        zz = zz_glyph(0.2).next_to(sad[0], UP + RIGHT, buff=0.0)
        self.say("Too high, and long jobs starve.", dial.swing_to(0.92, run_time=1.2), FadeIn(sad), FadeIn(zz), self.stu.change("sad"))

        # S12.5
        shoved = VGroup(job("B", 0.4), job("C", 0.4)).arrange(RIGHT, buff=0.1).move_to(P3(1.3, 1.2))
        boost = Arrow(P3(2.2, 0.6), P3(2.2, 1.6), buff=0, color=COL["A"], stroke_width=5)
        self.say("Too low, and interactive jobs lose their share.", dial.swing_to(0.08, run_time=1.2),
                 FadeOut(sad), FadeOut(zz), FadeIn(shoved), FadeIn(boost), self.stu.change("neutral"))

        # S12.6
        tip = TipCard(body="Avoid voodoo constants (Ousterhout's Law)", title="TIP", width=3.2, font_size=20, accent=DIM)
        tip.move_to(P3(4.9, 0.9))
        self.say("Hence Ousterhout's Law: avoid voodoo constants if you can.",
                 self.note("Ousterhout's Law"), self.prof.change("explaining"), tip.slide_in(RIGHT), FadeOut(VGroup(shoved, boost)))

        # S12.7
        cfg = config_glyph("S = 1000  # default", 3.0, 18).move_to(P3(-1.0, -0.7))
        gear = GearPair(0.3).move_to(P3(1.3, -0.7))
        nn = neural_glyph(0.9).move_to(P3(2.3, -0.7))
        self.say("Often you can't, so you get a config file of defaults an administrator tweaks, or, these days, machine-learned values.",
                 dial.swing_to(0.5), FadeIn(cfg, shift=UP * 0.4), Succession(Wait(2.0), FadeIn(gear), gear.spin(angle=TAU, run_time=2.0)),
                 Succession(Wait(4.0), FadeIn(nn, shift=LEFT * 0.4)))
        self.beat(1.0)
