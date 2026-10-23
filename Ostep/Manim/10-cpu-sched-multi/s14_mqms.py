import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common_more import *  # noqa: E402,F401,F403


class S14Mqms(Ep10Scene):
    def construct(self):
        self.world(strip=1, stu="neutral", prof="neutral")
        stu, prof = self.stu, self.prof
        st = mq_stage("", "")
        c0, c1, q0, q1, grid = st["c0"], st["c1"], st["q0"], st["q1"], st["grid"]

        # S14.1
        pad = Padlock(0.5).move_to(P3(0, MQ_CHIP_Y))
        slash = Line(pad.get_corner(UL) + UL * 0.1, pad.get_corner(DR) + DR * 0.1).set_stroke(KERNEL_COLOR, 6)
        self.say("So some systems flip the design around. Give every CPU its own queue.",
                 FadeIn(c0, shift=RIGHT * 0.5), FadeIn(c1, shift=LEFT * 0.5),
                 Succession(Wait(0.8), AnimationGroup(FadeIn(q0, shift=UP * 0.3), FadeIn(q1, shift=UP * 0.3))),
                 Succession(Wait(2.0), FadeIn(pad, scale=0.6), Wait(0.5), Create(slash)))

        # S14.2
        self.say("This is multi-queue multiprocessor scheduling, or MQMS.", self.note("MQMS"))

        # S14.3
        rr = [tag("round robin", 18).move_to(P3(x, -1.5)) for x in MQ_X]
        self.say("Each queue runs its own policy, say round robin.", *[FadeIn(r, shift=UP * 0.1) for r in rr])

        # S14.4
        jobs = {j: proc(j, "ready", 0.4) for j in "ABCD"}
        for k, (j, p) in enumerate(jobs.items()):
            place_on(p, P3(-6.3 + 0.55 * k, 2.0 - 0.0 * k))
        heur = tag("heuristic: fewer jobs", 18, TEXT).move_to(P3(0, -0.85))
        with self.narrate("A new job gets placed on exactly one queue, by some heuristic: pick randomly, "
                          "or the one with fewer jobs."):
            self.play(FadeIn(heur), *[FadeIn(p) for p in jobs.values()], run_time=0.6)
            for j, q in zip("ABCD", (q0, q1, q0, q1)):
                self.play(q.push(jobs[j]), run_time=0.8)

        # S14.5
        div = DashedLine(P3(0, 0.9), P3(0, -1.6), dash_length=0.12).set_stroke(DIM, 3)
        self.say("After that, each CPU schedules independently. No shared structure, no shared lock.",
                 Create(div), FadeOut(heur))

        # S14.6
        with self.narrate("CPU zero alternates between A and C, CPU one between B and D."):
            self.play(FadeIn(grid), run_time=0.5)
            for c in range(8):
                self.play(grid.fill(0, c, "AACCAACC"[c], run_time=0.3), grid.fill(1, c, "BBDDBBDD"[c], run_time=0.3),
                          run_time=0.4)

        # S14.7
        extra = []
        for x in (-5.8, 5.8):
            ec = cpu_at(x, MQ_CHIP_Y + 0.05, "CPU", size=1.2)
            ec.scale(0.5, about_point=ec.cpu.get_center())
            eq = Queue(label=None, center=(x, MQ_Q_Y), slots=2, spacing=0.5)
            extra.append(VGroup(ec, eq))
        bar = VGroup(Rectangle(width=2.2, height=0.22).set_fill(CPU_COLOR, 1).set_stroke(width=0),
                     label("work", 16, CPU_COLOR).shift(DOWN * 0.3)).move_to(P3(0, -0.5))
        self.say("The payoff is real. MQMS is naturally scalable: more CPUs, more queues, and the locks are never in contention.",
                 FadeIn(extra[0], shift=RIGHT * 0.5), Succession(Wait(0.6), FadeIn(extra[1], shift=LEFT * 0.5)),
                 Succession(Wait(1.2), FadeIn(bar)), FadeOut(div))

        # S14.8
        self.say("And a job stays on its CPU, so affinity comes for free.",
                 c0.warmth(3, COL["A"]), c1.warmth(3, COL["B"]))

        # S14.9
        self.say("That sounds perfect.", stu.change("excited"))

        # S14.10
        nxt = label("next: load imbalance", 22, DIM).move_to(P3(4.6, -1.1))
        self.say("That is what I would say, if I hadn't been paying attention to the title of the next section.",
                 prof.change("worried"), FadeOut(extra[0]), FadeOut(extra[1]), FadeOut(bar), FadeOut(pad), FadeOut(slash),
                 Succession(Wait(1.5), FadeIn(nxt), Indicate(nxt, color=KERNEL_COLOR, scale_factor=1.1)))
        self.beat(0.3)
