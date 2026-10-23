"""Preview sheet for the episode-09 props.

    python -m manim -ql -s ostep_lib/props/p09_preview.py P09PropSheet
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from manim import *  # noqa: E402,F401
from ostep_lib import *  # noqa: E402,F401


def cap(text, mob, direction=DOWN):
    return Text(text, font_size=16, color=DIM).next_to(mob, direction, buff=0.1)


class P09PropSheet(Scene):
    def construct(self):
        apply_style(self)
        cA, cB, cC, cD = PROCESS_COLORS[:4]
        drum = RaffleDrum(1.3).move_to(LEFT * 5.8 + UP * 2.3)
        ball, _ = drum.draw(63, cA)
        ball.move_to(drum.chute_point())
        t = Ticket(cA).scale(1.6).move_to(LEFT * 4.2 + UP * 2.8)
        t2 = Ticket(cB, label=7).scale(1.6).move_to(LEFT * 4.2 + UP * 2.0)
        st = TicketStack(75, cA).move_to(LEFT * 3.0 + UP * 2.4)
        st2 = TicketStack(25, cB).move_to(LEFT * 2.0 + UP * 2.4)
        ss = Seesaw(2.6, "often", "rarely").move_to(LEFT * 0.2 + UP * 2.2)
        ss.set_angle_now(10)
        pie = TargetPie().move_to(RIGHT * 2.4 + UP * 2.4)
        ns = NumberStrip(100, [("A", 75, cA), ("B", 25, cB)], x_range=(3.2, 6.4), y=2.3, ticks=[0, 75, 99])
        mk = ns.marker_at(63)
        self.add(drum, ball, t, t2, st, st2, ss, pie, ns, mk)
        jl = JobList([("A", 100, cA), ("B", 50, cB), ("C", 250, cC)], at=(-4.0, 0.2), gap=1.9)
        self.add(jl, jl.pointer(1))
        lanes = VGroup(*[PassLane(n, c, s, 0.6 - 0.45 * i, x0=0.4, scale=0.02) for i, (n, c, s) in
                         enumerate([("A", cA, 100), ("B", cB, 200), ("C", cC, 40)])])
        self.add(lanes, *[l.stride_bar for l in lanes])
        pt = PassTable(top_left=(5.2, 1.2), col_w=0.0 + 0.5, row_h=0.28, font_size=14)
        pt.add_row((0, 0, 0), "A"); pt.add_row((100, 0, 0), "B")
        self.add(pt)
        ms = VGroup(*[VruntimeMeter(c, 1.0, level=l) for c, l in ((cA, 0.7), (cB, 0.3), (cC, 0.0))]).arrange(RIGHT, buff=0.3)
        ms.move_to(LEFT * 5.0 + DOWN * 1.8)
        self.add(ms, ms[0].gap_to(ms[1]))
        tree = RBTree(at=(-0.8, -1.2), dx=0.52, dy=0.65, radius=0.22)
        self.add(tree)
        fp = FairnessPlot(3.2, 1.4, at=(4.5, -1.8))
        self.add(fp, fp.curve())
        icons = VGroup(cloud_icon(1.2), vm_window("Linux", cA, 1.0, 0.7, "75%"), coin_icon(), die_icon(), handshake_icon(),
                       sched_chip("MLFQ"), text_editor_icon(), bad_luck_cloud(width=1.0)).arrange(RIGHT, buff=0.35)
        icons.move_to(DOWN * 3.3).scale(0.8)
        self.add(icons)
