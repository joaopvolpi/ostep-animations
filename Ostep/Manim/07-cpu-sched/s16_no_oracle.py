import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


class S16NoOracle(Ep07Scene):
    def construct(self):
        self.world(opened=(0, 1, 2, 3), term="overlap", stu="excited", prof="happy")
        stu, prof, strip = self.stu, self.prof, self.strip
        tl = make_lanes()
        set_lane_blocks(tl, OVERLAP_CPU, OVERLAP_DISK)
        m140 = tl.completion_marker(None, 14, "140", color=DIM)
        m100 = tl.completion_marker(None, 10, "100", color=TEXT)
        disk = Disk(0.7, 0.6).move_to(P3(-5.75, 0.2))
        self.add(tl, m140, m100, disk)
        lock5 = strip.locks[4]

        # S16.1
        self.say("One padlock left: the OS knows how long each job will run.",
                 FadeOut(VGroup(tl, m140, m100, disk), shift=RIGHT * 0.5, scale=0.6),
                 *[strip.locks[i].animate.set_opacity(0.3) for i in range(4)],
                 lock5.animate.scale(3.2).move_to(P3(0, 0.8)))

        # S16.2
        ball = CrystalBall(0.55).move_to(P3(0, 2.4))
        kr = Text("known run-time", font_size=26, color=DIM).move_to(P3(0, -0.2))
        self.say("We said this was the worst assumption, and it is.",
                 FadeIn(ball, shift=DOWN * 0.3), ball.glow_up(), FadeIn(kr))

        # S16.3
        t1 = Text("SJF", font_size=34, color=VIRT, weight=BOLD).move_to(P3(-3.6, 2.5))
        t2 = Text("STCF", font_size=34, color=VIRT, weight=BOLD).move_to(P3(3.6, 2.5))
        n1 = Text("needs: run-time", font_size=20, color=DIM).next_to(t1, DOWN, buff=0.12)
        n2 = Text("needs: run-time", font_size=20, color=DIM).next_to(t2, DOWN, buff=0.12)
        qbars = VGroup(*[sj_bar(1, w, COL[n], "?", x, -1.2) for n, w, x in
                         zip("ABC", (1.8, 1.0, 1.4), (-3.4, -0.5, 1.8))])
        self.say("Both SJF and STCF need to know job lengths before running them.",
                 FadeIn(t1), FadeIn(t2), FadeIn(n1), FadeIn(n2), Succession(Wait(0.8), Indicate(t1), Indicate(t2)),
                 Succession(Wait(1.5), LaggedStart(*[FadeIn(b, shift=UP * 0.2) for b in qbars], lag_ratio=0.4)))

        # S16.4
        stage = Rectangle(width=1.8, height=0.12).set_fill(DIM, 1).set_stroke(TEXT, 2).move_to(P3(-4.5, -1.55))
        walker = proc("A", scale=0.55)
        bottom_to(walker, P3(-6.3, -1.45))
        qm = question_mark(0.4, color=CPU_COLOR).move_to(P3(-4.5, -0.45))
        qoutline = Rectangle(width=1.0, height=0.2).set_fill(opacity=0).set_stroke(DIM, 2).next_to(qm, DOWN, buff=0.1)
        self.say("In a general-purpose OS, the system usually knows very little about how long a program will run.",
                 ball.crack(run_time=1.5), FadeOut(VGroup(t1, t2, n1, n2, qbars)),
                 Succession(Wait(1.5), FadeIn(stage), FadeIn(walker),
                            hop_bottom(walker, P3(-4.5, -1.49), run_time=1.0), FadeIn(qm), FadeIn(qoutline)))

        # S16.5
        self.say("So the best schedulers we found can't actually be built?",
                 stu.change("confused"), FadeOut(VGroup(stage, walker, qm, qoutline)))

        # S16.6
        self.say("Not as they stand.", prof.change("thinking"), lock5.shake(run_time=1.0))

        # S16.7
        cards = VGroup()
        for name, key, x in (("behave like SJF", "sjf5", -2.6), ("keep response good", "rr", 2.6)):
            fr = RoundedRectangle(width=4.6, height=1.9, corner_radius=0.15).set_fill(CARD_FILL, 1).set_stroke(DIM, 2.5)
            lab = Text(name, font_size=26, color=TEXT).move_to(fr.get_top() + DOWN * 0.35)
            th = thumb(key, 2.4).move_to(fr.get_center() + DOWN * 0.3 + LEFT * 0.5)
            qm2 = question_mark(0.6, color=CPU_COLOR).move_to(fr.get_center() + DOWN * 0.3 + RIGHT * 1.6)
            cards.add(VGroup(fr, lab, th, qm2).move_to(P3(x, -2.05)))
        self.say("How do we behave like SJF without that knowledge? And how do we keep response time good, "
                 "like Round Robin?",
                 LaggedStart(*[FadeIn(c, shift=UP * 0.3) for c in cards], lag_ratio=0.8, run_time=3.0))

        # S16.8
        self.say("Keep that question.",
                 FadeOut(cards), FadeOut(VGroup(*[strip.locks[i] for i in range(4)])))
        self.beat(1.0)
