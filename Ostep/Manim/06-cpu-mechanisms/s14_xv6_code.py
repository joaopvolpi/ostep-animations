import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403
from s13_watching_a_switch import build_end as s13_end  # noqa: E402


def stage_mobs(d):
    w = d["w"]
    return [w.boundary, w.gauge, w.chip, *w.rings.values(), d["a"], d["b"], d["ksA"], d["ksB"], d["pA"], d["pB"],
            d["timer"], d["tl"], d["pkA"], w.token]


class S14Xv6Code(Ep06Scene):
    def construct(self):
        self.add_badge()
        self.add_docked_term("context switch")
        stu, prof = corner_chars(True, "neutral", "neutral")
        d = s13_end()
        mobs = stage_mobs(d)
        d["w"].boundary.set_z_index(-5)
        self.add(*mobs, stu, prof)

        # S14.1
        code = swtch_code(18).move_to(P3(-2.4, 0.3))
        cap = Text("xv6 (Figure 6.4, trimmed)", font_size=18, color=DIM).next_to(code, UP, buff=0.15)
        old_slot = VGroup(save_slot(0.7, COL["A"]), Text("old", font_size=20, color=TEXT)).arrange(DOWN, buff=0.08).move_to(P3(3.6, 2.2))
        new_slot = VGroup(save_slot(0.7, COL["B"]), Text("new", font_size=20, color=TEXT)).arrange(DOWN, buff=0.08).move_to(P3(5.2, 2.2))
        cpu_g = CPU(0.8, label=None, pins=3).move_to(P3(4.4, 0.4))
        t1 = KernelStack("old stack", width=1.3, height=1.0, slots=2).move_to(P3(2.3, -2.0))
        t2 = KernelStack("new stack", width=1.3, height=1.0, slots=2).move_to(P3(3.8, -2.0))
        ptr = Arrow(cpu_g.get_bottom() + DOWN * 0.05, t1.get_top() + UP * 0.35, buff=0, color=CPU_COLOR, stroke_width=4)
        overlay = Rectangle(width=16, height=9).set_fill(BG, 0.8).set_stroke(width=0).set_z_index(8)
        for m in (code, cap, old_slot, new_slot, cpu_g, t1, t2, ptr):
            m.set_z_index(12)
        bg = VGroup(*mobs, stu, prof)
        self.allow_overlap(VGroup(code, cap, old_slot, new_slot, cpu_g, t1, t2, ptr), bg,
                           "the code card and its helpers sit on top of the dimmed stage")
        self.say("In xv6, that's a few lines of x86 assembly:",
                 FadeIn(overlay, run_time=1.0),
                 Succession(Wait(0.8), AnimationGroup(FadeIn(code), FadeIn(cap), FadeIn(old_slot), FadeIn(new_slot),
                                                      FadeIn(cpu_g), FadeIn(t1), FadeIn(t2), FadeIn(ptr))))

        # S14.2
        bar = code_line_bar(code, 1, 5, KERNEL_COLOR).set_z_index(12)
        pk = RegPacket(KERNEL_COLOR).move_to(cpu_g.get_center()).set_z_index(12)
        self.allow_overlap(VGroup(bar, pk), bg, "on top of the dimmed stage")
        self.say("store the registers into the old context…",
                 Succession(FadeIn(bar), AnimationGroup(FadeIn(pk, scale=0.5)),
                            PacketFly(pk, old_slot[0].get_center(), arc=0.4, end_scale=0.6, fade=True, run_time=1.2)))

        # S14.3
        bar2 = code_line_bar(code, 6, 8, COL["B"])
        pk2 = RegPacket(COL["B"]).move_to(new_slot[0].get_center()).set_z_index(12)
        self.allow_overlap(VGroup(bar2, pk2), bg, "on top of the dimmed stage")
        self.say("…load them from the new one…",
                 Succession(ReplacementTransform(bar, bar2), FadeIn(pk2, scale=0.5),
                            PacketFly(pk2, cpu_g.get_center(), arc=0.4, end_scale=0.6, fade=True, run_time=1.2)))

        # S14.4
        bar3 = code_line_bar(code, 9, 9, CPU_COLOR, 0.35)
        ptr2 = Arrow(cpu_g.get_bottom() + DOWN * 0.05, t2.get_top() + UP * 0.35, buff=0, color=CPU_COLOR, stroke_width=4).set_z_index(12)
        self.allow_overlap(VGroup(bar3, ptr2), bg, "on top of the dimmed stage")
        self.say("…switch the stack…",
                 Succession(ReplacementTransform(bar2, bar3), ReplacementTransform(ptr, ptr2)))

        # S14.5
        bar4 = code_line_bar(code, 11, 11, CPU_COLOR, 0.35)
        rt = tag("returns into the new process", COL["B"], 20).move_to(P3(-2.4, -2.55)).set_z_index(12)
        self.allow_overlap(VGroup(bar4, rt), bg, "on top of the dimmed stage")
        self.say("…and ret.",
                 Succession(ReplacementTransform(bar3, bar4), FadeIn(rt, shift=UP * 0.2)), min_time=2.0)
        self.beat(1.2)

        # S14 end: the stage returns at full brightness
        self.play(FadeOut(VGroup(code, cap, old_slot, new_slot, cpu_g, t1, t2, ptr2, bar4, rt)), FadeOut(overlay),
                  run_time=1.0)
