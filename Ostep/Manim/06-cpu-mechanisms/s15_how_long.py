import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403
from s13_watching_a_switch import build_end as s13_end  # noqa: E402
from s14_xv6_code import stage_mobs  # noqa: E402


class S15HowLong(Ep06Scene):
    def construct(self):
        self.add_badge()
        self.add_docked_term("context switch")
        stu, prof = corner_chars(True, "neutral", "neutral")
        d = s13_end()
        w, b, pA = d["w"], d["b"], d["pA"]
        w.boundary.set_z_index(-5)
        self.add(*stage_mobs(d), stu, prof)
        timer = d["timer"]

        # S15.1
        card = AsideCard(Text("How long do context switches take?", font_size=20, color=TEXT), width=4.8, height=3.6)
        card.move_to(P3(3.0, 0.5))
        overlay = Rectangle(width=16, height=9).set_fill(BG, 0.75).set_stroke(width=0).set_z_index(8)
        stage_all = VGroup(*stage_mobs(d), stu, prof)
        front = []

        def up_front(*ms):
            for m_ in ms:
                m_.set_z_index(12)
                self.allow_overlap(m_, stage_all, "the aside card sits on top of the dimmed stage")
                front.append(m_)
        up_front(card)
        card.body.move_to(P3(3.0, card.frame.get_top()[1] - 0.95))
        sw = stopwatch_icon(0.7).move_to(P3(-5.0, 1.4))
        up_front(sw)
        self.say("How long does all this take?",
                 AnimationGroup(card.slide_in(), FadeIn(sw), FadeIn(overlay)), Succession(Wait(0.5), Indicate(sw, scale_factor=1.25)))

        left = card.frame.get_left()[0] + 0.3
        cy = card.frame.get_center()[1]

        def row(label, units, y, text_tex):
            lab = Text(label, font_size=18, color=TEXT).move_to(P3(left, y + 0.3), aligned_edge=LEFT)
            bar = Rectangle(width=max(units * 0.3, 0.05), height=0.2).set_fill(COL["A"], 1).set_stroke(TEXT, 1)
            bar.move_to(P3(left, y), aligned_edge=LEFT)
            val = MathTex(text_tex, font_size=28, color=TEXT).next_to(bar, RIGHT, buff=0.15)
            up_front(lab, bar, val)
            return lab, bar, val

        l1, b1, v1 = row("system call", 4, cy + 0.15, r"\approx 4\,\mu\mathrm{s}")
        l2, b2, v2 = row("context switch", 6, cy - 0.5, r"\approx 6\,\mu\mathrm{s}")
        src = Text("Linux 1.3.37 · 200 MHz", font_size=16, color=DIM).move_to(P3(left, cy - 1.1), aligned_edge=LEFT)

        up_front(src)
        # S15.2
        self.say("In 1996, on a 200-megahertz machine, a system call took about four microseconds, and a context "
                 "switch about six.",
                 Succession(AnimationGroup(FadeIn(l1), FadeIn(l2), FadeIn(src)),
                            AnimationGroup(GrowFromEdge(b1, LEFT), FadeIn(v1)), AnimationGroup(GrowFromEdge(b2, LEFT), FadeIn(v2))))

        # S15.3
        nb1 = Rectangle(width=0.12, height=0.2).set_fill(COL["A"], 1).set_stroke(TEXT, 1).move_to(b1.get_left(), aligned_edge=LEFT)
        nb2 = Rectangle(width=0.18, height=0.2).set_fill(COL["A"], 1).set_stroke(TEXT, 1).move_to(b2.get_left(), aligned_edge=LEFT)
        nv1 = MathTex(r"< 1\,\mu\mathrm{s}", font_size=28, color=TEXT).next_to(nb1, RIGHT, buff=0.15)
        nv2 = MathTex(r"< 1\,\mu\mathrm{s}", font_size=28, color=TEXT).next_to(nb2, RIGHT, buff=0.15)
        up_front(nb1, nb2, nv1, nv2)
        self.say("Modern systems do almost ten times better.",
                 AnimationGroup(Transform(b1, nb1), Transform(b2, nb2), ReplacementTransform(v1, nv1), ReplacementTransform(v2, nv2)))

        # S15.4
        base = cy - 1.15
        cb = Rectangle(width=0.5, height=0.2).set_fill(CPU_COLOR, 1).set_stroke(TEXT, 1).move_to(P3(left + 0.7, base), aligned_edge=DOWN)
        mb = Rectangle(width=0.5, height=0.1).set_fill(DIM, 1).set_stroke(TEXT, 1).move_to(P3(left + 2.4, base), aligned_edge=DOWN)
        cl = Text("CPU speed", font_size=14, color=CPU_COLOR).next_to(cb, UP, buff=0.8)
        ml = Text("memory bandwidth", font_size=14, color=DIM).next_to(mb, UP, buff=0.35)
        cb2 = Rectangle(width=0.5, height=1.0).set_fill(CPU_COLOR, 1).set_stroke(TEXT, 1).move_to(cb.get_bottom(), aligned_edge=DOWN)
        mb2 = Rectangle(width=0.5, height=0.3).set_fill(DIM, 1).set_stroke(TEXT, 1).move_to(mb.get_bottom(), aligned_edge=DOWN)
        cl.next_to(cb2, UP, buff=0.05)
        ml.next_to(mb2, UP, buff=0.05)
        up_front(cb, mb, cl, ml, cb2, mb2)
        self.say("Not everything speeds up with the CPU, though: many OS operations are bound by memory bandwidth.",
                 Succession(AnimationGroup(FadeOut(VGroup(l1, l2, b1, b2, nv1, nv2, src)), FadeIn(cb), FadeIn(mb)), AnimationGroup(Transform(cb, cb2), Transform(mb, mb2),
                                                                                    FadeIn(cl), FadeIn(ml))))

        # S15.5
        prog_bg = Rectangle(width=0.9, height=0.1).set_fill(CARD_FILL, 1).set_stroke(DIM, 1)
        prog = Rectangle(width=0.05, height=0.1).set_fill(GREEN_OK, 1).set_stroke(width=0)
        bang = Text("!", font_size=48, color=RED_BAD, weight=BOLD)
        bl = bolt(0.3).move_to(timer.get_center())
        self.say("What if a timer interrupt fires during a system call?", stu.change("confused"),
                 Succession(AnimationGroup(card.slide_out(), FadeOut(VGroup(cb, mb, cl, ml)), FadeOut(sw), FadeOut(overlay)),
                            w.down("B"),
                            AnimationGroup(FadeIn(prog_bg.move_to(P3(0, -0.15))), FadeIn(prog.move_to(prog_bg.get_left(), aligned_edge=LEFT))),
                            prog.animate(run_time=1.0).stretch_to_fit_width(0.5, about_edge=LEFT),
                            timer.ring(0.6),
                            PacketFly(bl, P3(0, -1.0), arc=0.4, fade=True, run_time=0.9),
                            AnimationGroup(FadeIn(bang.move_to(P3(0.9, 0.0)), scale=1.8), Flash(P3(0.9, 0.0), color=RED_BAD, flash_radius=0.45))))

        # S15.6
        tg = ep_tag("→ Concurrency · Part II").move_to(P3(-2.3, 0.45))
        self.say("Good question, and the answer belongs to the whole second piece of this series.", prof.change("happy"),
                 FadeIn(tg, scale=1.3))

        # S15.7
        gate = ShieldGate(1.0).move_to(P3(2.6, 0.2))
        bolts = [bolt(0.22).move_to(timer.get_center()) for _ in range(3)]
        clk = ClockIcon(0.3).move_to(P3(4.7, 0.1))
        too = Text("too long?", font_size=18, color=DIM).next_to(clk, UP, buff=0.1)
        self.say("One simple trick is to disable interrupts while handling one, but not for long, or you lose some.",
                 Succession(self.note("disable interrupts"), FadeOut(bang), FadeIn(gate, shift=DOWN * 0.8),
                            AnimationGroup(*[Succession(Wait(0.3 * k), PacketFly(bolts[k], P3(3.3 + 0.35 * k, 0.6 + 0.1 * k), arc=0.3, run_time=0.8))
                                             for k in range(3)]),
                            AnimationGroup(FadeIn(clk), FadeIn(too)), clk.spin(1.0, 1.5),
                            AnimationGroup(*[FadeOut(bl_, shift=UP * 0.3) for bl_ in bolts])))

        # S15.8
        lock = padlock_icon(0.35, KERNEL_COLOR).move_to(pA.get_corner(UR) + P3(0.0, 0.1))
        self.say("Real kernels also use locking to protect their data structures.",
                 Succession(AnimationGroup(FadeOut(VGroup(clk, too)), FadeIn(lock, scale=1.6)), self.note("locking")))

        # S15.9
        pt = ep_tag("→ Part II").move_to(P3(0, 1.8))
        self.say("Concurrency, later.",
                 Succession(AnimationGroup(FadeOut(lock), FadeOut(gate), FadeOut(tg), FadeOut(prog_bg), FadeOut(prog)),
                            FadeIn(pt), Wait(0.6), FadeOut(pt)))
        self.play(w.up("B"))
