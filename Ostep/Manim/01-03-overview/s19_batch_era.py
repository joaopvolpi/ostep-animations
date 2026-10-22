import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from manim import *  # noqa: E402,F403
from ostep_lib import *  # noqa: E402,F403
from common import *  # noqa: E402,F403
from s18_good_os import goal_frame, goal_icons, extras_row  # noqa: E402


class S19BatchEra(NarratedScene):
    def construct(self):
        stu, prof = make_hosts("corner", stu_expr="curious", prof_expr="happy")
        th = hist_terms()
        bdg = badge(INTRO)
        strip = card_strip(piece_cards()).move_to([0, 3.3, 0])
        frames = VGroup(*[goal_frame(i) for i in range(4)])
        icons = VGroup(*goal_icons())
        ex = extras_row()
        self.add(stu, prof, bdg, strip, frames, icons, ex, set_docked(th, "reliability"))

        era = era_ribbon(0)
        mf, shelf, cpu_job, operator = s19_end()

        # S19.1
        self.say("These ideas didn't arrive all at once. Engineers learned them the hard way.",
                 FadeOut(VGroup(strip, frames, icons, ex)), Succession(Wait(0.5), era.draw()))

        # S19.2
        with self.narrate("In the beginning, the OS was just a library of handy routines, like I/O code, so "
                          "programmers didn't have to write it themselves."):
            self.play(FadeIn(mf, shift=UP * 0.3), FadeIn(shelf, shift=RIGHT * 0.3), run_time=0.9)
            self.play(th.show("just a library", size=36, hold=0.8))
            self.play(LaggedStart(*[d.animate.set_opacity(0.3) for d in mf.lights[::3]], lag_ratio=0.05), run_time=0.6)
            self.play(LaggedStart(*[d.animate.set_opacity(1) for d in mf.lights[::3]], lag_ratio=0.05), run_time=0.6)

        # S19.3
        self.say("On the old mainframes, one program ran at a time.", FadeIn(cpu_job, scale=0.6))

        # S19.4
        self.say("A human operator decided the order.", FadeIn(operator, shift=LEFT * 0.4))

        # S19.5 batch of punch-card jobs
        jobs = VGroup(*[punch_cards_icon(1, 0.45) for _ in range(5)]).arrange(RIGHT, buff=0.12)
        jobs.move_to([0.55, -1.75, 0])
        entry = mf.get_right() + DOWN * 1.35
        with self.narrate("Jobs were run in a batch."):
            self.play(FadeIn(jobs, lag_ratio=0.2), run_time=0.5)
            self.play(th.show("batch processing", size=36, hold=0.6))
            for k in range(3):
                j = jobs[k]
                self.play(j.animate.move_to(entry).scale(0.6).set_opacity(0), run_time=0.4)
                self.play(jobs[k + 1:].animate.shift(LEFT * 0.57), Indicate(cpu_job[1], scale_factor=1.15), run_time=0.35)

        # S19.6 no chair; money meter
        chair = chair_icon(0.6).move_to([-0.25, -1.9, 0]).shift(LEFT * 0.0)
        chair.move_to([-0.3, -2.3, 0])
        nox = x_mark(0.3).move_to(chair)
        meter = money_meter().move_to([0.3, 0.9, 0])
        with self.narrate("Nobody sat at the machine interactively. It was simply too expensive to let it sit idle."):
            self.play(FadeOut(jobs[3:]), FadeIn(chair), run_time=0.5)
            self.play(Create(nox), run_time=0.4)
            self.play(FadeIn(meter, shift=DOWN * 0.2), run_time=0.4)
            for _ in range(4):
                self.play(Indicate(meter, color=CPU_COLOR, scale_factor=1.08), run_time=0.45)
        self.play(FadeOut(VGroup(chair, nox, meter)), run_time=0.4)
        self.beat(0.3)
