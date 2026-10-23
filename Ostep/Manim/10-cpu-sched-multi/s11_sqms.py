import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common_more import *  # noqa: E402,F401,F403


class S11Sqms(Ep10Scene):
    def construct(self):
        self.world(strip=1, term="cache affinity", stu="neutral", prof="neutral")
        stu, prof = self.stu, self.prof
        cpus = four_cpus()
        q, ps = job_queue("ABCDE")
        null = mono("NULL", 18, DIM).move_to(P3(3.3, -1.0))
        pad = Padlock(0.45, opened=True).move_to(P3(-3.2, -1.0))
        self.add(*cpus)

        # S11.1
        self.say("Fine. So what's the simplest scheduler? Take the one we already have and share it?",
                 stu.change("curious"), FadeIn(q), FadeIn(null), LaggedStart(*[FadeIn(p, shift=UP * 0.3) for p in ps], lag_ratio=0.15))

        # S11.2
        with self.narrate("Put all jobs into a single queue. Each CPU, whenever it needs work, grabs the next job from it."):
            self.play(self.note("SQMS"), FadeIn(pad), run_time=0.8)
            for i in range(4):
                p, repack = q.pop(0)
                self.play(hop_to(p, cpus[i].slot_point(), run_time=0.8), repack, run_time=0.8)
                p.set_expression("running")
        # S11.3
        spot = Spotlight(height=0.9, spread=0.4).move_beam_to(q.slot_point(0) + DOWN * 0.1)
        pol = label("any existing policy", 22, CPU_COLOR).next_to(q, RIGHT, buff=0.25).shift(UP * 0.5)
        pol.move_to(P3(3.2, -1.75))
        self.say("It needs almost no new work. Take any single-CPU policy, and let it pick the best job to run, "
                 "and then the second best for the second CPU, and so on.",
                 FadeIn(spot), FadeIn(pol, shift=UP * 0.1), prof.change("explaining"))

        # S11.4
        self.say("But there are two problems. The first: scalability.", self.note("scalability"),
                 FadeOut(spot), FadeOut(pol), prof.change("neutral"))

        # S11.5
        lines = VGroup(*[DashedLine(c.cache_bottom(), q.slot_point(0) + UP * 0.1 + RIGHT * 0.25 * i, dash_length=0.1)
                         .set_stroke(DIM, 2, opacity=0.6) for i, c in enumerate(cpus)])
        self.say("The queue is shared, so the scheduler must lock it.",
                 pad.close(), Create(lines))

        # S11.6
        waiters = []
        for i in range(3):
            w = Process("ready", color=PROCESS_COLORS[5], label=None).scale(0.3)
            place_on(w, P3(-2.4 + 0.5 * i, -1.9))
            ck = mini_clock(0.1).move_to(w.get_top() + UP * 0.12)
            waiters.append(VGroup(w, ck))
        lockbar = Rectangle(width=1.8, height=0.2).set_fill(KERNEL_COLOR, 1).set_stroke(width=0)
        lockbar.move_to(P3(-3.7, -2.55))
        lb_lab = label("waiting for the lock", 18, KERNEL_COLOR).move_to(P3(-3.7, -3.0))
        self.say("And as we just saw, locks hurt more and more as CPUs grow.",
                 LaggedStart(*[FadeIn(w, shift=UP * 0.2) for w in waiters], lag_ratio=0.4), FadeIn(lb_lab),
                 GrowFromEdge(lockbar, LEFT),
                 stu.change("sad"))

        # S11.7
        bx, by, bw = -0.6, -2.55, 3.0
        work = Rectangle(width=bw * 0.75, height=0.3).set_fill(CPU_COLOR, 1).set_stroke(width=0)
        lock = Rectangle(width=bw * 0.25, height=0.3).set_fill(KERNEL_COLOR, 1).set_stroke(width=0)
        bar = VGroup(work, lock).arrange(RIGHT, buff=0).move_to(P3(bx + 1.0, by))
        n_lab = label("4 CPUs", 20, TEXT).next_to(bar, UP, buff=0.12)
        wl = label("work", 18, CPU_COLOR).next_to(bar, DOWN, buff=0.08).align_to(bar, LEFT)
        ll = label("lock", 18, KERNEL_COLOR).next_to(bar, DOWN, buff=0.08).align_to(bar, RIGHT)
        w2 = Rectangle(width=bw * 0.3, height=0.3).set_fill(CPU_COLOR, 1).set_stroke(width=0)
        l2 = Rectangle(width=bw * 0.7, height=0.3).set_fill(KERNEL_COLOR, 1).set_stroke(width=0)
        bar2 = VGroup(w2, l2).arrange(RIGHT, buff=0).move_to(bar)
        bar2[0].align_to(bar, LEFT)
        bar2[1].next_to(bar2[0], RIGHT, buff=0)
        with self.narrate("More time is spent waiting for the lock, less time doing the work the system is supposed to do."):
            self.play(FadeIn(bar), FadeIn(n_lab), FadeIn(wl), FadeIn(ll), run_time=0.8)
            self.play(Transform(bar, bar2), Transform(n_lab, label("8 CPUs", 20, TEXT).move_to(n_lab)), run_time=2.0)

        # S11.8
        chart = DashedVMobject(Rectangle(width=1.9, height=0.9).set_stroke(DIM, 2), num_dashes=40).move_to(P3(3.9, -2.45))
        note = label("real measurement:\nleft as an exercise", 16, DIM).move_to(chart)
        self.say("The book wishes it had a real measurement here. Take our word for it, for now.",
                 Create(chart), FadeIn(note), stu.change("neutral"))
        self.beat(0.4)
