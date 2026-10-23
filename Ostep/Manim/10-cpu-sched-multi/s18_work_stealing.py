import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common_more import *  # noqa: E402,F401,F403


class S18WorkStealing(Ep10Scene):
    def construct(self):
        self.world(strip=2, stu="neutral", prof="neutral")
        stu, prof = self.stu, self.prof
        st = mq_stage("A", "BDE")
        c0, c1, q0, q1 = st["c0"], st["c1"], st["q0"], st["q1"]
        pA = st["p0"][0]
        pB, pD, pE = st["p1"]
        pA.set_expression("running")
        eye = EyeIcon(0.6).move_to(P3(-3.0, -1.55))
        g0 = tag("1 job", 18, TEXT).move_to(P3(-5.2, -0.6))
        self.add(c0, c1, q0, q1, pA, pB, pD, pE, eye)

        # S18.1 key term
        with self.narrate("One basic approach is work stealing."):
            self.play(self.term("work stealing"))
            self.play(FadeIn(g0), run_time=0.4)

        # S18.2
        g1 = tag("3 jobs", 18, TEXT).move_to(P3(5.2, -0.6))
        with self.narrate("A queue that's running low on jobs occasionally peeks at another queue to see how full it is."):
            self.play(hop_to(eye, P3(3.0, -1.55), anchor="center", run_time=1.0, height=0.6), run_time=1.0)
            self.play(eye.look_at(P3(3.0, -0.4)), FadeIn(g1, scale=0.7), run_time=0.6)
            self.play(hop_to(eye, P3(-3.0, -1.55), anchor="center", run_time=1.0, height=0.6), run_time=1.0)

        # S18.3
        hand = hand_icon(0.45).next_to(pE, UP, buff=0.05)
        g0b, g1b = tag("2 jobs", 18, TEXT).move_to(g0), tag("2 jobs", 18, TEXT).move_to(g1)
        with self.narrate("If the other queue is notably fuller, the low queue steals one or more jobs to balance the load."):
            _, rep = q1.pop(2)
            self.play(FadeIn(hand, scale=0.6), run_time=0.4)
            self.play(q0.push(pE), rep, hand.animate.shift(P3(-6.0, 0.0)), run_time=1.4)
            self.play(Transform(g0, g0b), Transform(g1, g1b), FadeOut(hand), run_time=0.6)

        # S18.4
        self.say("How often should it peek?", stu.change("confused"))

        # S18.5 peek too often
        dial = SpeedGauge(0.5, width=2.4, color=CPU_COLOR, font_size=18).move_to(P3(0, -2.9))
        rare = label("rarely", 20, DIM).next_to(dial.track, LEFT, buff=0.25)
        often = label("often", 20, DIM).next_to(dial.track, RIGHT, buff=0.25)
        pad = Padlock(0.45).move_to(P3(1.1, -0.85))
        waiting = VGroup(*[EyeIcon(0.4).move_to(P3(2.0 + 0.6 * i, -1.7)) for i in range(4)])
        b_, l_ = dial.value_targets(1.0, text="")
        with self.narrate("There's the catch. If CPUs peek too often, they take locks on each other's queues…"):
            self.play(FadeIn(dial), FadeIn(rare), FadeIn(often), stu.change("neutral"), run_time=0.5)
            self.play(Transform(dial.bar, b_), Transform(dial.label, l_), FadeIn(pad, scale=0.6), run_time=0.8)
            for i in range(4):
                self.play(hop_to(eye, P3(3.0, -1.55), anchor="center", run_time=0.35, height=0.3),
                          FadeIn(waiting[i], scale=0.5), run_time=0.4)
                self.play(hop_to(eye, P3(-3.0, -1.55), anchor="center", run_time=0.35, height=0.3), run_time=0.4)

        # S18.6 SQMS again
        merged, mps = job_queue("AEBD", center=(0, -0.9), label_text="the queue", spacing=0.9, scale=0.4)
        mpad = Padlock(0.45).move_to(P3(-2.6, -0.9))
        again = label("SQMS again!", 30, KERNEL_COLOR).move_to(P3(0, -2.1))
        old = VGroup(q0, q1, pA, pE, pB, pD, g0, g1, pad, waiting, eye)
        self.say("…the overhead goes up, and we've rebuilt SQMS, the thing we were trying to escape.",
                 FadeOut(old), FadeIn(merged), LaggedStart(*[FadeIn(p) for p in mps], lag_ratio=0.1), FadeIn(mpad),
                 Succession(Wait(1.5), FadeIn(again, scale=0.7)), prof.change("worried"))

        # S18.7 peek too rarely
        q0b = Queue(label="Q0", center=(MQ_X[0], MQ_Q_Y), slots=3, spacing=0.9, mover=hop_mover)
        q1b = Queue(label="Q1", center=(MQ_X[1], MQ_Q_Y), slots=3, spacing=0.9, mover=hop_mover)
        qs = [proc(j, "ready", 0.4) for j in "BDEA"]
        q1b.place(*qs)
        eye2 = EyeIcon(0.6).move_to(P3(-3.0, -1.55))
        b2, l2 = dial.value_targets(0.0, text="")
        zz = zz_glyph(0.4).move_to(c0.cpu.get_corner(UR) + UR * 0.2)
        with self.narrate("If they peek too rarely, we're back to severe load imbalance."):
            self.play(FadeOut(VGroup(merged, *mps, mpad, again)), FadeIn(q0b), FadeIn(q1b), *[FadeIn(p) for p in qs],
                      FadeIn(eye2), Transform(dial.bar, b2), Transform(dial.label, l2), run_time=1.0)
            self.play(cpu_power(c0, False), FadeIn(zz), eye2.look_at(P3(3.0, -0.4)), run_time=1.0)

        # S18.8
        b3, l3 = dial.value_targets(0.5, text="")
        sweet = label("sweet spot?", 22, CPU_COLOR).next_to(dial.track, UP, buff=0.2)
        pot = VGroup(Arc(radius=0.3, start_angle=PI, angle=PI).rotate(PI).set_stroke(TEXT, 3).set_fill("#444444", 1),
                     Line(P3(-0.3, 0), P3(0.3, 0)).set_stroke(TEXT, 3)).move_to(P3(4.6, -2.7))
        bub = VGroup(*[Circle(radius=0.07).set_stroke(GREEN_OK, 2).move_to(pot.get_top() + P3(-0.12 + 0.12 * i, 0.15 + 0.08 * i))
                       for i in range(3)])
        self.say("Finding the right threshold is, as is common in system policy design, a black art.",
                 Transform(dial.bar, b3), FadeIn(sweet), FadeIn(pot), LaggedStart(*[FadeIn(b, shift=UP * 0.2) for b in bub], lag_ratio=0.4),
                 Wiggle(sweet, scale_value=1.15, rotation_angle=0.03 * TAU), cpu_power(c0, True), FadeOut(zz))

        # S18.9
        flash = Indicate(c0.strip, color=KERNEL_COLOR, scale_factor=1.15)
        self.say("That's the honest answer. And here's another tension: every steal throws away a bit of cache affinity.",
                 prof.change("happy"), flash, c0.warmth(0, COL["E"]),
                 FadeOut(bub), FadeOut(pot), FadeOut(sweet))
        self.beat(0.4)
