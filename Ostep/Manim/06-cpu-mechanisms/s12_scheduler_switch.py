import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403
from s11_timer_interrupt import build_end as s11_end  # noqa: E402


def slot_with_label(text, color):
    return VGroup(save_slot(0.6, color), Text(text, font_size=18, color=TEXT)).arrange(DOWN, buff=0.08)


def build_end():
    """S12 end: S11 end + save slots for A and B and a dotted return arrow aimed at B."""
    d = s11_end()
    sA = slot_with_label("save slot (A)", COL["A"]).move_to(P3(-1.9, -2.95))
    sB = slot_with_label("save slot (B)", COL["B"]).move_to(P3(1.9, -2.95))
    ret = DashedLine(P3(0, -0.7), P3(3.4, 0.8), dash_length=0.12).add_tip(tip_length=0.2)
    d.update(sA=sA, sB=sB, ret=ret)
    return d


class S12SchedulerSwitch(Ep06Scene):
    def construct(self):
        self.add_badge()
        self.add_docked_term("non-cooperative")
        stu, prof = corner_chars(True, "neutral", "neutral")
        d = s11_end()
        w, a, b, tt, ks, pk, timer, st, rib = (d[k] for k in ("w", "a", "b", "tt", "ks", "pk", "timer", "strip", "ribbon"))
        self.add(w.boundary, w.gauge, w.chip, *w.rings.values(), a, b, tt, ks, pk, timer, w.token, st, stu, prof)
        self.add(rib)

        # S12.1
        door = door_in_line().move_to(P3(-2.4, BY)).set_z_index(1)
        a1 = Arrow(P3(-2.4, -0.55), w.token.get_left() + LEFT * 0.05, buff=0, color=CPU_COLOR, stroke_width=5)
        bl = bolt(0.25)
        a2 = CurvedArrow(timer.get_bottom() + DOWN * 0.7, w.token.get_right() + RIGHT * 0.05, angle=-0.7, color=CPU_COLOR)
        bl.move_to(a2.point_from_proportion(0.5))
        self.say("Now the OS is back in control, by a system call or a timer interrupt.",
                 AnimationGroup(FadeOut(st), FadeOut(rib)),
                 Succession(Wait(1.0), AnimationGroup(FadeIn(door), GrowArrow(a1)), AnimationGroup(Create(a2), FadeIn(bl))))

        # S12.2
        spot = Spotlight(height=1.0, spread=0.5).move_beam_to(P3(0, 1.6))
        self.say("It must decide: keep running this process, or switch?",
                 Succession(AnimationGroup(FadeOut(VGroup(a1, a2, bl, door)), FadeIn(spot)),
                            spot.animate(run_time=1.0).move_beam_to(P3(-3.4, 1.7)),
                            spot.animate(run_time=1.0).move_beam_to(P3(3.4, 1.7)),
                            spot.animate(run_time=0.8).move_beam_to(P3(0, 1.6))))

        # S12.3
        tg = ep_tag("→ Ep. 07-10").next_to(spot.lamp, RIGHT, buff=0.2)
        self.say("That's the job of the scheduler, and its policies fill the next episodes.",
                 Succession(self.note("scheduler"), FadeIn(tg, scale=1.3)))

        # S12.4
        gears = GearPair(0.2).next_to(w.token, UP, buff=0.05)
        self.say("If the decision is to switch, the OS runs a low-level piece of code: the context switch.",
                 AnimationGroup(spot.animate(run_time=1.2).move_beam_to(P3(3.4, 1.7)), FadeOut(tg)),
                 Succession(Wait(1.0), FadeIn(gears), gears.spin(TAU, 1.5)), late(1.0, self.term("context switch")))

        # S12.5
        big = save_slot(0.9).move_to(P3(0, 1.2))
        ghost_r = RegisterBank([("PC", "0x400"), ("SP", "0xff8"), ("eax", "42"), ("ebx", "7")], cols=2, box_width=1.2,
                               box_height=0.38, font_size=16).move_to(P3(-2.6, 1.3))
        ghost_m = Memory(cells=5, width=0.8, height=1.8, font_size=14).move_to(P3(2.6, 1.0))
        make_translucent(ghost_r, 0.4, 0.4)
        make_translucent(ghost_m, 0.4, 0.4)
        self.say("Remember the save slot from episode four?",
                 AnimationGroup(FadeOut(spot), FadeOut(gears)),
                 Succession(Wait(0.5), AnimationGroup(FadeIn(big, scale=1.6), FadeIn(ghost_r), FadeIn(ghost_m)),
                            Indicate(big, scale_factor=1.2)))

        # S12.6
        bad = save_slot(0.35, COL["A"]).next_to(a, UP, buff=0.05)
        load = VGroup(Arrow(P3(3.4, 2.85), P3(3.4, 2.35), buff=0, color=COL["B"], stroke_width=5),
                      Text("load", font_size=20, color=COL["B"]).move_to(P3(2.8, 2.65)))
        self.say("The video-game save! Pause one, load the other!", stu.change("excited"),
                 AnimationGroup(FadeOut(ghost_r), FadeOut(ghost_m), FadeIn(bad, scale=1.5), FadeIn(load, shift=UP * 0.2)))

        # S12.7
        sA = slot_with_label("save slot (A)", COL["A"]).move_to(P3(-1.9, -2.95))
        sB = slot_with_label("save slot (B)", COL["B"]).move_to(P3(1.9, -2.95))
        to_a = Arrow(w.chip.get_bottom() + LEFT * 0.3 + DOWN * 0.1, sA.get_top() + UP * 0.05, buff=0.03, color=COL["A"], stroke_width=4)
        from_b = Arrow(sB.get_top() + UP * 0.05, w.chip.get_bottom() + RIGHT * 0.3 + DOWN * 0.1, buff=0.03, color=COL["B"], stroke_width=4)
        self.say("Exactly. Save a few registers of the running process, restore a few of the next one.", prof.change("proud"),
                 AnimationGroup(FadeOut(big), FadeOut(bad), FadeOut(load)),
                 Succession(Wait(0.8), AnimationGroup(FadeIn(sA), FadeIn(sB)), GrowArrow(to_a), GrowArrow(from_b)))

        # S12.8
        ret = DashedLine(P3(0, -0.7), P3(-3.4, 0.8), dash_length=0.12).add_tip(tip_length=0.2)
        ret2 = DashedLine(P3(0, -0.7), P3(3.4, 0.8), dash_length=0.12).add_tip(tip_length=0.2)
        self.say("Then return-from-trap doesn't go back to the process that was interrupted. It goes into the other one.",
                 Succession(Create(ret), ReplacementTransform(ret, ret2)))
        self.beat(1.0)
