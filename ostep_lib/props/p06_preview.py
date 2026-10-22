"""Prop sheet for episode 06.

    python -m manim -ql -s ostep_lib/props/p06_preview.py P06PropSheet
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2].parent))

from manim import *  # noqa: E402
from ostep_lib import *  # noqa: E402


class P06PropSheet(Scene):
    def construct(self):
        apply_style(self)
        title = Text("episode 06 props", font_size=26, color=DIM).to_corner(UL, buff=0.3)

        chip = CPU(1.12, label=None, pins=3)
        tok = KernelToken().next_to(chip, UP, buff=0.02)
        k1 = VGroup(chip, tok).move_to([-5.2, 2.3, 0])
        pk = RegPacket(PROCESS_COLORS[0], labels=["PC", "flags", "..."]).move_to([-3.4, 2.7, 0])
        pk2 = RegPacket(KERNEL_COLOR).move_to([-3.4, 1.9, 0])
        ks = KernelStack("k-stack(A)").move_to([-1.6, 2.1, 0])
        p_in = RegPacket(PROCESS_COLORS[0]).move_to(ks.slot_point(0)).scale(1.3)
        ks.items.append(p_in)
        tt = TrapTable(filled=3).move_to([2.2, 2.0, 0])
        tt.highlight_row(1)
        clock = AlarmClock(0.4).move_to([5.3, 2.1, 0])

        gate = ShieldGate().move_to([-5.4, -0.2, 0])
        cab = cabinet_lock(1.0).move_to([-4.0, -0.2, 0])
        soc = socket_cover(1.0).move_to([-2.8, -0.2, 0])
        fen = fence_glyph().move_to([-1.6, -0.2, 0])
        mag = magnifier_icon().move_to([-0.4, -0.2, 0])
        door = door_in_line().move_to([0.7, -0.2, 0])
        booth = booth_gate().move_to([2.0, -0.2, 0])
        ring = bench_ring(PROCESS_COLORS[1]).move_to([3.6, -0.5, 0])
        proc = Process("ready", color=PROCESS_COLORS[1], label="B").scale(0.6)
        proc.shift(ring.get_center() + UP * 0.2 - proc.get_bottom())

        chart = ProtocolChart(["OS (kernel mode)", "Hardware", "Program (user mode)"],
                              colors=[KERNEL_COLOR, CPU_COLOR, USER_COLOR], top=-1.1, bottom=-3.6,
                              col_width=3.6, col_x=[-4.0, 0.0, 4.0], font_size=18, row_h=0.36)
        chart.add(*[]) 
        self.add(title, k1, pk, pk2, ks, p_in, tt, clock, gate, cab, soc, fen, mag, door, booth, ring, proc, chart)
        self.play(chart.draw(run_time=0.1))
        self.play(chart.write_row(0, "initialize trap table", bold=True, run_time=0.1),
                  )
        self.play(chart.write_row(1, "remember address of syscall handler", run_time=0.1))
        self.play(chart.write_row(2, "Run main()", run_time=0.1))
        self.wait(0.1)
