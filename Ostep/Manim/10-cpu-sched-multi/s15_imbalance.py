import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common_more import *  # noqa: E402,F401,F403

PAT0 = "AACCAACC"
PAT1 = "BBDDBBDD"


class S15Imbalance(Ep10Scene):
    def construct(self):
        self.world(strip=1, stu="excited", prof="worried")
        stu, prof = self.stu, self.prof
        st = mq_stage("AC", "BD", fill_grid=[PAT0, PAT1])
        c0, c1, q0, q1, grid = st["c0"], st["c1"], st["q0"], st["q1"], st["grid"]
        pA, pC = st["p0"]
        pB, pD = st["p1"]
        comp = Computer("busy").scale(0.55).move_to(P3(5.7, -0.9))
        self.add(c0, c1, q0, q1, *st["p0"], *st["p1"], grid, comp)

        # S15.1
        pC.set_expression("done")
        with self.narrate("Suppose job C finishes."):
            self.play(pC.change("done"), run_time=0.6)
            _, repack = q0.pop(1)
            self.play(FadeOut(pC, shift=UP * 0.3), repack, run_time=0.8)

        # S15.2
        self.say("Queue zero now holds only A. Queue one still holds B and D.",
                 Indicate(q0.tray, color=CPU_COLOR), Indicate(q1.tray, color=CPU_COLOR), stu.change("neutral"))

        # S15.3
        self.say("Run round robin on each queue independently, and what happens?", grid.clear(), stu.change("curious"))

        # S15.4
        with self.narrate("CPU zero runs A, and only A, all the time. CPU one still splits its time between B and D."):
            for c in range(12):
                self.play(grid.fill(0, c, "A", run_time=0.25), grid.fill(1, c, "BBDD"[c % 4], run_time=0.25), run_time=0.4)

        # S15.5
        ta = tag("A: 100% of CPU 0", 18, COL["A"]).move_to(P3(-3.0, -1.45))
        tbd = tag("B: 50% · D: 50%", 18, COL["B"]).move_to(P3(3.0, -1.45))
        two = MathTex(r"2\times", color=KERNEL_COLOR).scale(1.6).move_to(P3(0, -0.6))
        self.say("So A gets twice as much CPU as B or D. That's not the fair share the scheduler wanted.",
                 FadeIn(ta, shift=UP * 0.1), FadeIn(tbd, shift=UP * 0.1), Succession(Wait(1.0), FadeIn(two, scale=0.5), Wait(0.6), FadeOut(two)),
                 stu.change("confused"))

        # S15.6
        with self.narrate("It gets worse. Suppose A finishes too."):
            self.play(pA.change("done"), FadeOut(ta), FadeOut(tbd), run_time=0.6)
            _, repack = q0.pop(0)
            self.play(FadeOut(pA, shift=UP * 0.3), repack, run_time=0.8)

        # S15.7
        null = mono("NULL", 18, DIM).move_to(P3(MQ_X[0], MQ_Q_Y + 0.25))
        hatch_anims = [grid.hatch(0, c, run_time=0.3) for c in range(12)]
        self.say("Queue zero is now empty. CPU zero has nothing to do.",
                 cpu_power(c0, False), FadeIn(null), LaggedStart(*hatch_anims, lag_ratio=0.1))

        # S15.8
        zz = zz_glyph(0.4).move_to(c0.cpu.get_corner(UR) + UR * 0.2)
        music = Text("(dramatic and sinister music)", font_size=20, color=DIM, slant=ITALIC).move_to(P3(0, -3.3))
        sleeper = Computer("sleeping").scale(0.55).move_to(comp)
        self.say("It sits idle, while CPU one is juggling two jobs. How terrible.",
                 Transform(comp, sleeper), FadeIn(zz), FadeIn(music), stu.change("frustrated"),
                 Succession(Wait(1.0), Indicate(pB, color=COL["B"]), Indicate(pD, color=COL["D"])))

        # S15.9 key term
        with self.narrate("This is load imbalance, the fundamental problem of multi-queue scheduling."):
            self.play(FadeOut(music), self.term("load imbalance"))
            self.play(Indicate(grid.cell_mobs(), color=DIM, scale_factor=1.03), run_time=0.8)

        # S15.10 second crux
        card = CruxCard(CRUX2_Q, CRUX2_SUB, accent=VIRT, question_size=32, subtitle_size=22).move_to(P3(0, 0.3))
        shade = scrim(0.85)
        card.set_z_index(45)
        self.add(shade)
        self.play(FadeIn(card.frame, scale=0.9), Write(card.header), run_time=0.8)
        self.play(Write(card.question), FadeIn(card.subtitle), run_time=1.6)
        self.wait(1.5)
        self.play(card.dock(run_time=1.2), FadeOut(self.strip), FadeOut(shade), run_time=1.2)
        self.beat(0.3)
