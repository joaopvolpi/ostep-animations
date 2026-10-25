import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403

COLX = {"name": -4.3, "thumb": -2.3, "turn": 1.5, "resp": 3.3}
ROW_YS = [1.1, 0.4, -0.3, -1.0]


class S17BigPicture(Ep07Scene):
    def construct(self):
        self.world(opened=(0, 1, 2, 3), stu="confused", prof="thinking", strip=False)
        stu, prof = self.stu, self.prof
        strip = make_strip((0, 1, 2, 3))
        lock5 = strip.locks[4]
        lock5.scale(3.2).move_to(P3(0, 0.8))
        ball = CrystalBall(0.55).move_to(P3(0, 2.4))
        ball.crack_mob.set_stroke(TEXT, 4, opacity=1).pointwise_become_partial(ball.crack_full, 0, 1)
        ball.ball.set_fill(DIM, 0.6)
        kr = Text("known run-time", font_size=26, color=DIM).move_to(P3(0, -0.2))
        self.add(lock5, ball, kr)

        frame = RoundedRectangle(width=9.2, height=3.7, corner_radius=0.2).set_fill(CARD_FILL, 1).set_stroke(DIM, 2.5)
        frame.move_to(P3(0, 0.15))
        heads = VGroup(Text("Policy", font_size=22, color=DIM).move_to(P3(COLX["name"] + 0.5, 1.8)),
                       Text("Turnaround", font_size=22, color=DIM).move_to(P3(COLX["turn"], 1.8)),
                       Text("Response", font_size=22, color=DIM).move_to(P3(COLX["resp"], 1.8)))
        seps = VGroup(*[Line(P3(-4.6, y), P3(4.6, y)).set_stroke(DIM, 1, opacity=0.5) for y in (1.5, 0.75, 0.05, -0.65)])
        # tiny supermarket queue as the first row marker
        mq = VGroup(*[proc(n, scale=0.22) for n in "ABC"]).arrange(LEFT, buff=0.08).move_to(P3(-5.3, 2.55))
        mtray = Line(mq.get_left() + LEFT * 0.1 + DOWN * 0.22, mq.get_right() + RIGHT * 0.1 + DOWN * 0.22).set_stroke(DIM, 3)
        mlab = Text("supermarket line", font_size=18, color=DIM).next_to(mtray, DOWN, buff=0.05)

        # S17.1
        self.say("Let's step back. We started with a supermarket line and built four policies.",
                 FadeOut(VGroup(lock5, ball, kr)), after(1.0, AnimationGroup(
                     FadeIn(frame, scale=0.95), Create(seps), FadeIn(heads), FadeIn(mq), Create(mtray), FadeIn(mlab))),
                 stu.change("neutral"), prof.change("explaining"))

        def row(k, name, key, tv, tcol, rok, extra=None, note=None):
            y = ROW_YS[k]
            nm = Text(name, font_size=28, color=VIRT, weight=BOLD).move_to(P3(COLX["name"], y), aligned_edge=LEFT)
            th = thumb(key, 1.9).move_to(P3(COLX["thumb"] + 0.3, y))
            val = Text(tv, font_size=32, color=tcol, weight=BOLD).move_to(P3(COLX["turn"], y))
            mark = (tick_mark(0.3) if rok else x_mark(0.26)).move_to(P3(COLX["resp"], y))
            g = VGroup(nm, th, val, mark)
            if note:
                n = Text(note, font_size=18, color=DIM).next_to(val, RIGHT, buff=0.15)
                g.add(n)
            if extra is not None:
                g.add(extra.move_to(P3(5.4, y)))
            return g

        convoy = VGroup(Rectangle(width=0.8, height=0.22).set_fill(COL["A"], 1).set_stroke(TEXT, 1),
                        Rectangle(width=0.2, height=0.22).set_fill(COL["B"], 1).set_stroke(TEXT, 1),
                        Rectangle(width=0.2, height=0.22).set_fill(COL["C"], 1).set_stroke(TEXT, 1)).arrange(RIGHT, buff=0.04)
        rows = [
            row(0, "FIFO", "convoy", "110", KERNEL_COLOR, False, extra=convoy),
            row(1, "SJF", "sjf", "50", PERS, False),
            row(2, "STCF", "stcf", "50", PERS, False, extra=PauseGlyph(0.3)),
            row(3, "RR", "rr", "14", KERNEL_COLOR, True, note="(SJF: 10)"),
        ]
        rr_resp = Text("1", font_size=26, color=PERS, weight=BOLD).next_to(rows[3][3], RIGHT, buff=0.12)
        rows[3].add(rr_resp)

        # S17.2 - S17.5
        self.say("FIFO is simple but suffers from the convoy effect.", FadeIn(rows[0], shift=UP * 0.2), min_time=4.0)
        self.say("SJF fixes that for jobs that arrive together.", FadeIn(rows[1], shift=UP * 0.2), min_time=4.0)
        self.say("STCF fixes it when they don't, using preemption.", FadeIn(rows[2], shift=UP * 0.2), min_time=4.0)
        self.say("And Round Robin gives up turnaround to win on response time.", FadeIn(rows[3], shift=UP * 0.2), min_time=4.5)

        # S17.6
        c1 = Ellipse(width=2.2, height=0.7).set_stroke(VIRT, 3).move_to(heads[1])
        c2 = Ellipse(width=2.0, height=0.7).set_stroke(VIRT, 3).move_to(heads[2])
        self.say("Two metrics, and no policy wins both.",
                 Create(c1), Create(c2), prof.change("explaining"),
                 after(0.8, LaggedStart(*[Indicate(r[2], scale_factor=1.3) for r in rows], lag_ratio=0.3, run_time=1.5)))
        self.beat(0.6)
        self.fade_stage(self.badge, stu, prof, run_time=0.8)
