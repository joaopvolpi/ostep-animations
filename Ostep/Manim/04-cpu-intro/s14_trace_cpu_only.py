import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


class S14TraceCPUOnly(Ep04Scene):
    def construct(self):
        self.add_badge()
        self.add_docked_term("descheduled")
        stu, prof = self.add_corner_chars()
        slot = docked_save_slot()
        w = build_s13_end()
        sd = w["sd"]
        self.add(slot, sd, w["disk"], w["a"], w["b"], w["d"])

        t = build_trace_world(8)
        cpu, p0, p1, tl = t["cpu"], t["p0"], t["p1"], t["tl"]
        bar0 = work_bar(["w"] * 4, COL["P0"]).next_to(p0, UP, buff=0.12)
        bar1 = work_bar(["w"] * 4, COL["P1"]).next_to(p1, UP, buff=0.12)
        d0 = sd.make_dot(COL["P0"], label="0", radius=0.13)
        d1 = sd.make_dot(COL["P1"], label="1", radius=0.13)

        # S14.1
        with self.narrate("To see that in action, let's watch two processes, zero and one, each needing just four ticks of CPU and no I/O."):
            self.play(FadeOut(VGroup(w["a"], w["b"], w["d"], w["disk"])), run_time=0.5)
            self.play(sd.to_legend(LEGEND_POS, LEGEND_SCALE, run_time=1.0), FadeIn(cpu), run_time=1.0)
            sd.place_dot(d0, "ready").place_dot(d1, "ready")
            self.play(FadeIn(p0, shift=UP * 0.2), FadeIn(p1, shift=UP * 0.2), FadeIn(bar0), FadeIn(bar1),
                      FadeIn(d0), FadeIn(d1), Create(tl.grid), FadeIn(tl.row_labels), FadeIn(tl.tick_labels),
                      run_time=1.2)
        self.beat(1.2)

        # S14.2
        with self.narrate("Process zero runs for four ticks while process one waits, ready."):
            p0.set_expression("running")
            self.play(hop_seat(p0, cpu, run_time=0.6), bar0.animate.next_to(cpu, LEFT, buff=0.25).shift(UP * 0.9),
                      sd.move_dot(d0, "running"))
            for k in range(1, 5):
                self.play(tl.fill("P0", k, "running", run_time=0.5), tl.fill("P1", k, "ready", run_time=0.5),
                          bar0.cells[4 - k].animate(run_time=0.5).set_fill(opacity=0.1))

        # S14.3
        with self.narrate("At tick four, process zero is done."):
            p0.set_expression("done")
            self.play(hop_bottom(p0, TRACE_P0_SPOT, run_time=0.6), FadeOut(bar0), sd.remove_dot(d0))
            self.play(p0.animate.set_opacity(0.5), run_time=0.4)
        self.beat(0.8)

        # S14.4
        with self.narrate("Process one runs for ticks five to eight."):
            p1.set_expression("running")
            self.play(hop_seat(p1, cpu, run_time=0.6), bar1.animate.next_to(cpu, LEFT, buff=0.25).shift(UP * 0.9),
                      sd.move_dot(d1, "running"))
            for k in range(5, 9):
                self.play(tl.fill("P1", k, "running", run_time=0.5),
                          bar1.cells[8 - k].animate(run_time=0.5).set_fill(opacity=0.1))
            p1.set_expression("done")
            self.play(hop_bottom(p1, TRACE_P1_SPOT, run_time=0.6), FadeOut(bar1), sd.remove_dot(d1))

        # S14.5
        busy = Text("CPU busy: 8 / 8", font_size=26, color=CPU_COLOR).next_to(tl.tick_labels, DOWN, buff=0.12)
        with self.narrate("Eight ticks of work, eight ticks of time. The CPU never idled."):
            self.play(LaggedStart(*[tl.fill_cpu(k, "busy") for k in range(1, 9)], lag_ratio=0.15), run_time=1.6)
            self.play(Write(busy), run_time=0.7)
        self.beat(0.6)

        # transition: blocks clear; P0/P1 reset to ready beside the CPU
        p0.set_opacity(1)
        p0.set_expression("ready")
        p1.set_expression("ready")
        d0b = sd.make_dot(COL["P0"], label="0", radius=0.13)
        d1b = sd.make_dot(COL["P1"], label="1", radius=0.13)
        sd.place_dot(d0b, "ready").place_dot(d1b, "ready")
        self.play(tl.clear_blocks(), FadeOut(busy), FadeIn(d0b), FadeIn(d1b), run_time=0.8)
        tl.purge()
        self.wait(0.3)
