"""Preview sheet for the episode-08 props.

    python -m manim -ql -s ostep_lib/props/p08_preview.py P08PropSheet
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from manim import *  # noqa: E402,F401
from ostep_lib import *  # noqa: E402,F401


class P08PropSheet(Scene):
    def construct(self):
        apply_style(self)
        lad = MLFQLadder(levels=3)
        a = Process("ready", color=PROCESS_COLORS[0], label="A").scale(lad.job_scale)
        b = Process("ready", color=PROCESS_COLORS[1], label="B").scale(lad.job_scale)
        lad.place(a, 0); lad.place(b, 2); lad.place(Process("ready", color=PROCESS_COLORS[2], label="C").scale(lad.job_scale), 2)
        lad.serve(2)
        lad.lanes[2].set_stroke(CPU_COLOR, 3.5)
        self.add(lad, *[j for lv in lad.items.values() for _, j in lv])
        rb = RuleBoard()
        rb.place_now([("R1", "If Priority(A) > Priority(B), A runs."), ("R2", "Equal priority: round robin."),
                      ("R3", "A new job enters at the top queue."), ("R4a", "Used its allotment? Move down one queue."),
                      ("R4b", "Quit early? Stay put; allotment resets.")])
        self.add(rb)
        g = AllotmentGauge(1.2, 0.6).move_to([0.9, -0.6, 0])
        g2 = AllotmentGauge(1.2, 0.7).move_to([0.9, -1.0, 0])
        g2.chunk(0.0)
        self.add(g, g2, Text("allotment", font_size=16, color=DIM).next_to(g, RIGHT, buff=0.1))
        s = Process("running", color=PROCESS_COLORS[1], label="B").scale(1.0).move_to([-5.5, -2.0, 0])
        self.add(s, put_shades(s))
        d = Dial(0.8, "S", 0.7).move_to([-3.2, -2.0, 0])
        sp = SliderPanel(["queues", "time slice", "allotment", "boost"], width=2.4).move_to([-0.6, -2.2, 0]).scale(0.7)
        row = VGroup(voodoo_glyph(0.5), medal_glyph(0.6), mini_pie([(0.75, PROCESS_COLORS[0]), (0.25, PROCESS_COLORS[1])], 0.4),
                     neural_glyph(0.7), fork_glyph(), cache_grid(), history_clock(), rr_ring(), mystery_box(0.7), io_button(), bookmark_glyph(),
                     tag_chip("SJF")).arrange(RIGHT, buff=0.3).move_to([0, -3.4, 0]).scale(0.8)
        self.add(d, sp, row)
