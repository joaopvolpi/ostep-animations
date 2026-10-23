import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


def strip_pattern(color, y, x0=-5.0, kind="B"):
    """Behavior trace: B = short bursts, keyboard, gap; A = one long bar (built empty)."""
    g = VGroup()
    if kind == "B":
        x = x0
        for _ in range(3):
            r = Rectangle(width=0.35, height=0.3).set_fill(color, 1).set_stroke(TEXT, 1).move_to(P3(x + 0.175, y))
            kb = keyboard_icon(0.45).move_to(P3(x + 0.35 + 0.4, y))
            g.add(r, kb)
            x += 0.35 + 1.0
    return g


class S05Changing(Ep08Scene):
    def construct(self):
        s04_end(self, stu="neutral", prof="worried")
        lad = self.ladder
        A, B, C, D = (self.jobs[n] for n in "ABCD")

        # S05.1
        lad.collapse_to  # noqa
        col = lad.collapse_to(3)
        pts = {A: lad.register(A, 2, 0), B: lad.register(B, 2, 1), C: lad.register(C, 1, 0), D: lad.register(D, 0, 0)}
        moves = [j.animate.scale(2).move_to(p) for j, p in pts.items()]
        self.say("So who sets the priorities?", col, *moves, self.stu.change("curious"))

        # S05.2
        pl = [label(t, 20, DIM).move_to(P3(-1.7, y)) for t, y in (("Priority = 7", 2.05), ("Priority = 4", 1.1), ("Priority = 1", 0.15))]
        self.play(*[FadeIn(p) for p in pl], run_time=0.5)
        self.say("Nobody sets them once and for all.", self.prof.change("explaining"),
                 *[FadeOut(p, shift=DOWN * 0.5 + RIGHT * 0.2 * i, scale=0.5, run_time=1.4) for i, p in enumerate(pl)])

        # S05.3
        self.say("The key to MLFQ is that it varies a job's priority based on what it does, its observed behavior.",
                 self.note("observed behavior"), FadeOut(VGroup(C, D)),
                 Indicate(lad.arrows.up, color=CPU_COLOR), Succession(Wait(0.6), Indicate(lad.arrows.down, color=CPU_COLOR)))

        # S05.4
        trB = strip_pattern(COL["B"], -1.05)
        lbB = label("gives up the CPU often", 20, COL["B"]).move_to(P3(-3.2, -0.65))
        self.say("A job that keeps giving up the CPU to wait for the keyboard smells interactive…",
                 LaggedStart(*[FadeIn(m, shift=RIGHT * 0.2) for m in trB], lag_ratio=0.2), FadeIn(lbB))

        # S05.5
        up = Arrow(P3(-2.6, 1.7), P3(-2.6, 2.4), buff=0, color=PERS, stroke_width=5)
        inter = label("interactive", 22, PERS).move_to(P3(-1.4, 2.05))
        self.say("…so MLFQ keeps its priority high.", Indicate(B, scale_factor=1.5), FadeIn(up), FadeIn(inter))

        # S05.6
        bar = Rectangle(width=7.0, height=0.3).set_fill(COL["A"], 1).set_stroke(TEXT, 1).move_to(P3(-1.5, -2.0))
        lbA = label("uses the CPU for long stretches", 20, COL["A"]).move_to(P3(-2.8, -1.6))
        self.say("A job that burns the CPU for long stretches smells like a batch job…",
                 FadeIn(lbA), GrowFromEdge(bar, LEFT, run_time=3.5))

        # S05.7
        dn = Arrow(P3(-2.6, 0.9), P3(-2.6, 0.3), buff=0, color=KERNEL_COLOR, stroke_width=5)
        cb = label("CPU-bound", 22, KERNEL_COLOR).move_to(P3(-1.4, 0.15))
        self.say("…so MLFQ lowers its priority.", lad.promote(A, 0, 0, run_time=1.0), FadeIn(dn), FadeIn(cb),
                 FadeOut(up), FadeOut(inter))

        # S05.8
        hist = history_clock(0.3).move_to(P3(2.6, -1.0))
        inf = label("infers", 24, TEXT).next_to(hist, DOWN, buff=0.3)
        arr = CurvedArrow(P3(2.1, -0.9), P3(0.5, 0.0), angle=-0.5, color=DIM, stroke_width=3, tip_length=0.15)
        self.say("The scheduler infers which is which, from history.", FadeIn(hist), Write(inf), Create(arr))
        self.beat(1.0)
        self.play(FadeOut(VGroup(trB, lbB, bar, lbA, dn, cb, hist, inf, arr)), run_time=0.8)
