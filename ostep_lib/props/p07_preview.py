"""Preview sheet for the episode-07 props.

    python -m manim -ql -s ostep_lib/props/p07_preview.py P07PropSheet
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from manim import *  # noqa: E402,F401
from ostep_lib import *  # noqa: E402,F401
from ostep_lib.props.p04_timeline import Timeline  # noqa: E402


def cap(text, mob, direction=DOWN):
    return Text(text, font_size=16, color=DIM).next_to(mob, direction, buff=0.1)


class P07PropSheet(Scene):
    def construct(self):
        apply_style(self)
        cA, cB, cC = PROCESS_COLORS[:3]

        # Timeline with the 07 extensions
        tl = Timeline(["A", "B", "C"], ticks=12, colors=[cA, cB, cC], x_range=(-5.2, 3.0), top=2.9,
                      row_height=0.34, row_step=0.62, cpu_row=True, label_mode="boundary",
                      unit_per_tick=10, label_every=1, unit="s", tick_font=14, label_font=20,
                      tick_label_y=0.55)
        run = ["A"] * 3 + ["B", "C"] + [None] * 7
        for t, j in enumerate(run, 1):
            for r in "ABC":
                if j == r:
                    tl.set_block(r, t, "running")
                elif j and r > j:
                    tl.set_block(r, t, "ready")
            if j:
                tl.set_block("CPU", t, "running", color={"A": cA, "B": cB, "C": cC}[j])
        self.add(tl)
        self.add(tl.arrival_marker("B", 0, "arrives"), tl.bracket("A", 0, 3, "T"),
                 tl.bracket("C", 0, 1, "1", style="dashed"), tl.bracket("B", 0, 0, "0", style="dashed"),
                 tl.completion_marker("A", 3), tl.completion_marker("B", 4), tl.completion_marker("C", 5))
        self.add(cap("Timeline: cpu row colored by job, arrival marker, brackets (solid / dashed), completion markers",
                     tl, UP).shift(DOWN * 0.1))

        # two-lane CPU / Disk
        t2 = Timeline(["CPU", "Disk"], ticks=14, x_range=(-5.2, 3.0), top=-1.35, row_height=0.34, row_step=0.5,
                      row_kinds=["cpu", "disk"], label_mode="boundary", unit_per_tick=10, label_every=2,
                      unit="ms", tick_font=14, label_font=18)
        for k in (1, 3, 5, 7, 9):
            t2.set_block("CPU", k, "running", color=cA)
        for k in (2, 4, 6, 8):
            t2.set_block("Disk", k, "running", color=cA)
            t2.set_block("CPU", k, "idle")
        t2.set_span("CPU", 9.5, 10.5, "running", color=cB)
        self.add(t2, cap("kinds cpu / disk, boundary labels, fractional span", t2, DOWN))

        # padlocks
        strip = PadlockStrip(5, size=0.45, at=(-6.4, -3.0, 0), opened=(0, 1))
        self.add(strip, cap("Padlock / PadlockStrip", strip, DOWN))
        # crystal ball
        ball = CrystalBall(0.4).move_to(RIGHT * 4.9 + UP * 2.6)
        ball2 = CrystalBall(0.4).move_to(RIGHT * 6.0 + UP * 2.6)
        ball2.crack_mob.set_stroke(TEXT, 4, opacity=1).pointwise_become_partial(ball2.crack_full, 0, 1)
        ball.glow.set_fill(CPU_COLOR, 0.25)
        self.add(ball, ball2, cap("CrystalBall (glow / cracked)", ball, DOWN).shift(RIGHT * 0.6))
        # cart + checkout
        cart = Cart(1.0, boxes=5).move_to(RIGHT * 4.8 + UP * 0.6)
        desk = Checkout(2.0).move_to(RIGHT * 4.9 + DOWN * 0.7)
        milk = milk_carton(0.6).move_to(RIGHT * 6.1 + UP * 0.9)
        chk = checkbook_icon(0.6).move_to(RIGHT * 6.1 + DOWN * 0.1)
        self.add(cart, desk, milk, chk, cap("Cart, Checkout, milk, checkbook", desk, DOWN))
        # readout
        ro = MetricReadout(["100", "(110-10)", "(120-10)"], 3, "103.33", center=(1.4, -3.1), font_size=34)
        ro.show_all()
        ro.frame_value(good=False)
        self.add(ro.shown)
