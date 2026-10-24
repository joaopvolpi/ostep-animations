import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from manim import *  # noqa: E402,F403
from ostep_lib import *  # noqa: E402,F403
from common import *  # noqa: E402,F403
from s20_system_call import s20_world, s20_end_extras  # noqa: E402

MINI_POS = np.array([-5.4, 0.35, 0])
L_CPU = np.array([-3.0, 0.55, 0])
L_XS = (-3.9, -3.0, -2.1)
L_BASE_Y = -1.25
L_DISK = np.array([-1.0, -1.0, 0])


def s21_left():
    mini = minicomputer_icon(1.3, 1.7).move_to(MINI_POS)
    cpu = CPU(size=0.8).move_to(L_CPU)
    procs = VGroup()
    for i, x in enumerate(L_XS):
        p = Process(color=ABCD_COLORS[i], label="ABC"[i]).scale(0.5)
        place_on(p, [x, L_BASE_Y, 0])
        procs.add(p)
    disk = Disk(width=0.9, height=0.8).move_to(L_DISK)
    mems = VGroup(*[Rectangle(width=0.7, height=0.2).set_fill(ABCD_COLORS[i], 0.7).set_stroke(width=0)
                    .move_to([x, L_BASE_Y - 0.55, 0]) for i, x in enumerate(L_XS)])
    walls = VGroup(*[Rectangle(width=0.06, height=0.38).set_fill(TEXT, 1).set_stroke(width=0)
                     .move_to([(L_XS[k] + L_XS[k + 1]) / 2, L_BASE_Y - 0.55, 0]) for k in range(2)])
    return mini, cpu, procs, disk, mems, walls


def s21_right():
    unix = Text("UNIX", font=MONO_FONT, font_size=64, color=TEXT, weight=BOLD).move_to([3.2, 1.0, 0])
    sub = Text("Thompson & Ritchie · Bell Labs", font_size=20, color=DIM).next_to(unix, DOWN, buff=0.15)
    def box(t):
        tx = Text(t, font=MONO_FONT, font_size=18, color=TEXT)
        r = RoundedRectangle(width=tx.width + 0.3, height=0.5, corner_radius=0.08).set_fill(CARD_FILL, 1).set_stroke(DIM, 2)
        return VGroup(r, tx.move_to(r))
    grep = box("grep foo file.txt")
    pipe = pipe_glyph(0.7)
    wc = box("wc -l")
    pipeline = VGroup(grep, pipe, wc).arrange(RIGHT, buff=0.12).move_to([3.0, -0.75, 0])
    return unix, sub, pipeline


def s21_end_world():
    """Exact S21 end state (S22's start): returns the left/right groups plus the late extras."""
    mini, cpu, procs, disk, mems, walls = s21_left()
    unix, sub, pipeline = s21_right()
    procs[0].set_expression("blocked")
    procs[1].shift(cpu.slot_point() - base_point(procs[1]))
    procs[1].set_expression("running")
    grep, pipe, wc = pipeline
    out = Text("3", font=MONO_FONT, font_size=28, color=GOOD, weight=BOLD).next_to(wc, RIGHT, buff=0.3)
    cb = VGroup(Circle(radius=0.28).set_fill(USER_COLOR, 1).set_stroke(outline_of(USER_COLOR), 3),
                Text("C", font=FONT, font_size=30, color=INK, weight=BOLD))
    cb[1].move_to(cb[0])
    cb.next_to(unix, RIGHT, buff=0.15).shift(UP * 0.25)
    return mini, cpu, procs, disk, mems, walls, unix, sub, pipeline, VGroup(out, cb)


class S21MultiprogrammingUnix(NarratedScene):
    def construct(self):
        stu, prof = make_hosts("corner", stu_expr="curious", prof_expr="happy")
        th = hist_terms()
        bdg = badge(INTRO)
        era = era_ribbon(1)
        s19_end()   # S20 builds this (a CPU seating a Process) before A; that changes every Process built later (library quirk)
        uk, a, handler, disk0, gauge = s20_world()
        s20_x = s20_end_extras(a, handler)
        self.add(stu, prof, bdg, uk, a, handler, disk0, gauge, era, s20_x, set_docked(th, "return-from-trap"))

        mini, cpu, procs, disk, mems, walls = s21_left()
        homes = [base_point(p).copy() for p in procs]

        # S21.1
        with self.narrate("Next, cheaper minicomputers brought multiprogramming."):
            self.play(FadeOut(VGroup(uk, a, handler, gauge, s20_x)), ReplacementTransform(disk0, disk),
                      era.move_marker("minicomputers / UNIX"), run_time=0.9)
            self.play(FadeIn(mini, shift=RIGHT * 0.3), FadeIn(cpu), run_time=0.6)
            for p, h in zip(procs, homes):
                place_on(p, mini.get_center() + DOWN * 0.3)
            self.play(*[hop_to(p, h, run_time=0.7) for p, h in zip(procs, homes)])
            self.play(th.show("multiprogramming", hold=0.8))

        # S21.2 A blocks on I/O, B runs
        req = letter_icon(0.3).move_to(procs[0].get_center())
        with self.narrate("Load several jobs, and switch between them rapidly, especially while one waits for slow I/O."):
            self.play(hop_to(procs[0], cpu.slot_point(), run_time=0.5))
            self.play(procs[0].change("running"), run_time=0.3)
            self.wait(0.4)
            self.play(FadeIn(req), req.animate.move_to(disk.top_point()), run_time=0.7)
            self.play(hop_to(procs[0], homes[0], run_time=0.5), disk.spin(1, run_time=0.8))
            self.play(procs[0].change("blocked"), run_time=0.3)
            self.play(hop_to(procs[1], cpu.slot_point(), run_time=0.5))
            self.play(procs[1].change("running"), FadeOut(req), run_time=0.3)

        # S21.3 memory protection + concurrency spark
        spark = Flash(np.array([(L_XS[1] + L_XS[2]) / 2, L_BASE_Y + 0.4, 0]), color=CONC, line_length=0.15,
                      flash_radius=0.15, num_lines=8)
        self.say("That made memory protection and concurrency critical.",
                 FadeIn(mems), Succession(Wait(0.4), FadeIn(walls)), Succession(Wait(1.0), spark),
                 late(0.8, th.show("memory protection", size=34, hold=0.7)))

        # S21.4 UNIX
        unix, sub, pipeline = s21_right()
        self.say("This era also gave us UNIX, from Ken Thompson and Dennis Ritchie at Bell Labs.",
                 Write(unix, run_time=1.0), Succession(Wait(0.8), FadeIn(sub)))

        # S21.5 pipes
        grep, pipe, wc = pipeline
        dashes = VGroup(*[Line(LEFT * 0.08, RIGHT * 0.08).set_stroke(TEXT, 3) for _ in range(4)])
        out = Text("3", font=MONO_FONT, font_size=28, color=GOOD, weight=BOLD).next_to(wc, RIGHT, buff=0.3)
        with self.narrate("It was simple and powerful, built from small programs chained with pipes,"):
            self.play(FadeIn(pipeline, lag_ratio=0.3), run_time=0.8)
            for d in dashes:
                d.move_to(grep.get_right() + LEFT * 0.3)
                self.play(FadeIn(d, run_time=0.05), d.animate(run_time=0.35).move_to(wc.get_left() + RIGHT * 0.2))
                self.remove(d)
            self.play(FadeIn(out, shift=RIGHT * 0.2), run_time=0.4)
            self.play(th.show("pipes", hold=0.7))

        # S21.6 C badge
        cb = VGroup(Circle(radius=0.28).set_fill(USER_COLOR, 1).set_stroke(outline_of(USER_COLOR), 3),
                    Text("C", font=FONT, font_size=30, color=INK, weight=BOLD))
        cb[1].move_to(cb[0])
        cb.next_to(unix, RIGHT, buff=0.15).shift(UP * 0.25)
        self.say("and written in the new C language.", FadeIn(cb, scale=0.4))
        self.beat(0.5)
