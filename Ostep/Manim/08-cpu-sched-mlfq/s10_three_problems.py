import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403

CARD_Y = -0.7
CX = (-4.7, -1.5, 1.7)


def make_card1():
    c = card_frame("starvation", 3.0, 2.3)
    x0, y0 = c.frame.get_center()[0], c.frame.get_center()[1]
    top = Rectangle(width=2.0, height=0.4).set_fill(DIM, 0.1).set_stroke(DIM, 1.5).move_to(P3(x0 - 0.35, y0 + 0.2))
    bot = Rectangle(width=2.0, height=0.4).set_fill(DIM, 0.1).set_stroke(DIM, 1.5).move_to(P3(x0 - 0.35, y0 - 0.45))
    wall = VGroup(*[job(n, 0.2) for n in "BCBC"]).arrange(RIGHT, buff=0.12).move_to(top)
    a = job("A", 0.2).move_to(bot.get_left() + RIGHT * 0.3)
    zz = zz_glyph(0.15).next_to(a, RIGHT, buff=0.02)
    cpu = CPU(size=0.5, font_size=12).move_to(P3(x0 + 1.2, y0 + 0.2))
    cnt = label("0 ms of CPU", 18, KERNEL_COLOR).move_to(P3(x0, y0 - 0.95))
    c.add(top, bot, wall, a, zz, cpu, cnt)
    c.wall, c.zz, c.cnt = wall, zz, cnt
    return c


def make_card2():
    c = card_frame("gaming", 3.0, 2.3)
    x0, y0 = c.frame.get_center()[0], c.frame.get_center()[1]
    b = job("B", 0.55, "running").move_to(P3(x0 - 0.7, y0 - 0.1))
    sh = put_shades(b, 1.0)
    g = AllotmentGauge(0.9, 1.0)
    g.attach_to(b)
    io = io_button(0.45).move_to(P3(x0 + 0.3, y0 - 0.75))
    pie = mini_pie([(0.34, COL["B"]), (0.66, DIM)], 0.4).move_to(P3(x0 + 0.9, y0 + 0.05))
    c.add(b, sh, g, io, pie)
    c.b, c.g, c.io, c.pie, c.sh = b, g, io, pie, sh
    return c


def make_card3():
    c = card_frame("behavior changes", 3.0, 2.3)
    x0, y0 = c.frame.get_center()[0], c.frame.get_center()[1]
    bot = Rectangle(width=2.4, height=0.45).set_fill(DIM, 0.1).set_stroke(DIM, 1.5).move_to(P3(x0, y0 - 0.55))
    a = job("A", 0.25).move_to(bot.get_left() + RIGHT * 0.4)
    ph = label("Phase 1: compute", 18, COL["A"]).move_to(P3(x0, y0 + 0.4))
    c.add(bot, a, ph)
    c.a, c.ph, c.bot = a, ph, bot
    return c


class S10ThreeProblems(Ep08Scene):
    def construct(self):
        A, B = s09_end(self, stu="neutral", prof="neutral")
        board = self.board
        thumb = VGroup(self.ladder, self.cpu, self.tl, A, B, self.ex_tag)
        self.allow_overlap(VGroup(A, B), self.ladder, "tiny job labels touch lane borders while the ladder shrinks to a thumbnail")

        # S10.1
        self.play(thumb.animate.scale(0.32).move_to(P3(-4.6, 1.55)), run_time=1.0)
        self.say("So we have a basic MLFQ. Short and interactive jobs fly, and long ones share what's left.",
                 self.stu.change("excited"), board.ok())

        # S10.2
        self.say("But it has serious flaws.", self.prof.change("worried"), board.warn())

        # S10.3
        ring = progress_ring(0.45, color=CPU_COLOR, value=0.999).move_to(P3(0.2, 1.5))
        sw = stopwatch_icon(0.2).move_to(ring)
        self.say("Can you spot them? Pause the video, and think as deviously as you can.",
                 self.prof.change("thinking"), FadeIn(sw), Create(ring[1], run_time=3.0), self.stu.change("confused", look_at=ring))

        # S10.4
        c1 = make_card1().move_to(P3(CX[0], CARD_Y))
        self.play(FadeOut(VGroup(ring, sw)), run_time=0.4)
        self.say("First: starvation.", self.term("starvation"))
        self.play(FadeIn(c1, shift=UP * 0.5), run_time=0.8)

        # S10.5
        self.say("With too many interactive jobs, they consume all the CPU, and long jobs never get any.",
                 LaggedStart(*[Indicate(m, scale_factor=1.4) for m in c1.wall], lag_ratio=0.4), Indicate(c1.cnt, color=KERNEL_COLOR),
                 after(2.0, Indicate(c1.zz, scale_factor=1.5)), self.stu.change("neutral"))

        # S10.6
        c2 = make_card2().move_to(P3(CX[1], CARD_Y))
        self.say("Second: a smart user can game the scheduler, tricking it into giving them more than their fair share.",
                 self.note("game the scheduler"), FadeIn(c2, shift=UP * 0.5))

        # S10.7
        g = c2.g
        gk = board.hold_glow("R4b", KERNEL_COLOR)
        self.say("Rule four B is the hole. Just before the allotment is used up, issue an I/O, and you keep your priority.",
                 FadeIn(gk), g.drain(0.99, run_time=2.0),
                 after(2.4, Indicate(c2.io, scale_factor=1.3), g.reset(0.5)))

        # S10.8
        pies = [mini_pie([(f, COL["B"]), (1 - f, DIM)], 0.4).move_to(c2.pie) for f in (0.6, 0.85, 0.99)]
        loop = []
        for p in pies:
            loop.append(Succession(g.drain(0.99, run_time=0.8), Indicate(c2.io, scale_factor=1.3, run_time=0.4),
                                   AnimationGroup(g.reset(0.3), Transform(c2.pie, p, run_time=0.6))))
        self.say("Do that at ninety-nine percent of the allotment, every time, and one job can nearly monopolize the CPU.",
                 Succession(*loop))
        self.play(FadeOut(gk), run_time=0.3)

        # S10.9
        pl = Padlock(0.4, opened=True)
        tip = TipCard(body=VGroup(label("Scheduling must be secure", 16, TEXT), label("from attack", 16, TEXT)).arrange(DOWN, buff=0.05),
                      title="TIP", width=3.0, height=1.2, accent=DIM, icon=pl)
        tip.move_to(P3(CX[1], -2.75))
        self.say("On a shared server, that's a security problem.", self.prof.change("worried"), tip.slide_in(DOWN))

        # S10.10
        self.say("Scheduling policy has to resist attack.", pl.close())

        # S10.11
        c3 = make_card3().move_to(P3(CX[2], CARD_Y))
        self.say("Third: programs change.", FadeIn(c3, shift=UP * 0.5))

        # S10.12
        kb = keyboard_icon(0.45).next_to(c3.a, UP, buff=0.05)
        sliv = VGroup(*[Rectangle(width=0.04, height=0.2).set_fill(COL["A"], 1).set_stroke(width=0) for _ in range(6)]).arrange(RIGHT, buff=0.12).next_to(c3.a, RIGHT, buff=0.3)
        upa = Arrow(c3.a.get_top() + RIGHT * 0.5 + UP * 0.2, c3.a.get_top() + RIGHT * 0.5 + UP * 0.8, buff=0, color=PERS, stroke_width=4)
        xm = x_mark(0.3).move_to(upa.get_center() + RIGHT * 0.1)
        self.say("A CPU-bound job may become interactive, but with our rules it's stuck at the bottom.",
                 self.stu.change("frustrated"), FadeIn(kb, scale=1.3), FadeIn(sliv), after(1.5, FadeIn(upa), FadeIn(xm, scale=1.4)))
        self.beat(1.0)
