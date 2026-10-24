import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from manim import *  # noqa: E402,F403
from ostep_lib import *  # noqa: E402,F403
from common import *  # noqa: E402,F403
from s06_crux_api_manager import s06_end_state  # noqa: E402


class S07ThePeach(NarratedScene):
    def construct(self):
        stu, prof = make_hosts("corner", stu_expr="excited", prof_expr="explaining")
        stack, procs, strip = s06_end_state()
        th = terms(INTRO)
        bdg = badge(INTRO)
        self.add(stu, prof, bdg, stack, procs, strip, set_docked(th, "resource manager"))
        th.set_accent(VIRT)

        # S07.1
        f = PEACH_HOST_SCALE / CORNER_SCALE
        stu.mode_scale = prof.mode_scale = PEACH_HOST_SCALE
        self.say("But what is virtualization, oh noble Professor?",
                 FadeOut(VGroup(stack, procs, strip)), bdg.recolor(VIRT),
                 stu.animate.scale(f).move_to(STU_PEACH), prof.animate.scale(f).move_to(PROF_PEACH))
        self.play(stu.change("curious", look_at=prof), prof.look_at(stu), run_time=0.5)

        # S07.2
        table = table_line()
        peach = peach_on_table(Peach())
        self.say("Imagine we have a peach.",
                 prof.change("explaining"), Create(table, run_time=0.6),
                 Succession(Wait(0.3), hop_to(peach.shift(UP * 3).set_opacity(1), peach_on_table(peach.copy()).get_bottom(),
                                              height=0.3, run_time=0.7)), min_time=1.8)

        # S07.3
        self.say("A peach?", stu.change("confused"), min_time=1.2)

        # S07.4
        phys = Text("physical", font_size=22, color=TEXT).next_to(table, DOWN, buff=0.12).set_x(0)
        with self.narrate("A peach. Call it the physical peach."):
            self.play(prof.change("explaining"), FadeIn(phys, shift=UP * 0.1), run_time=0.6)
            self.play(th.note("physical"))

        # S07.5 eaters hop in
        eaters = make_eaters()
        homes = [base_point(e).copy() for e in eaters]
        for e, x in zip(eaters, EATER_XS):
            e.shift(RIGHT * (6 if x > 0 else -6))
        with self.narrate("Now, many eaters would like to eat this peach."):
            self.add(eaters)
            self.play(*[hop_to(e, h, height=0.6, run_time=0.9) for e, h in zip(eaters, homes)])
            self.play(*[e.look_at(peach) for e in eaters], stu.change("curious"), run_time=0.4)

        # S07.6 virtual copies
        vps = VGroup(*[vpeach_above(e) for e in eaters])
        with self.narrate("What we'd like is to give each of them their own peach, so they're all happy."):
            self.play(LaggedStart(*[TransformFromCopy(peach, v) for v in vps], lag_ratio=0.25), run_time=1.4)
            self.play(*[e.change("ready", look_at=v) for e, v in zip(eaters, vps)], run_time=0.5)
            for e in eaters:
                self.play(hop_to(e, base_point(e), height=0.2, run_time=0.25))

        # S07.7
        vtags = VGroup(*[Text("virtual", font_size=18, color=VIRT).next_to(v, UP, buff=0.08) for v in vps])
        with self.narrate("These are virtual peaches. We create many virtual peaches out of the one physical peach."):
            self.play(LaggedStart(*[FadeIn(t, shift=DOWN * 0.1) for t in vtags], lag_ratio=0.2), run_time=0.8)
            self.play(th.note("virtual"))

        # S07.8
        cones = VGroup(*[view_cone(e, v) for e, v in zip(eaters, vps)])
        self.say("The important part is the illusion: to each eater, it looks like they have a real peach "
                 "of their own.",
                 LaggedStart(*[FadeIn(c) for c in cones], lag_ratio=0.2, run_time=1.2),
                 peach.animate(run_time=1.0).set_opacity(0.5))
        self.beat(0.6)
