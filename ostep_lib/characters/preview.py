"""Preview scenes for the character library.

Render from the project root:
    python -m manim -ql -s ostep_lib/characters/preview.py ExpressionSheet
    python -m manim -ql ostep_lib/characters/preview.py CharacterDemo
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from manim import *  # noqa: E402,F403

from ostep_lib.characters.base import FONT  # noqa: E402
from ostep_lib import (  # noqa: E402
    BG, DIM, TEXT, PROCESS_COLORS, apply_style,

    Professor, Student, Computer, Process,
)


class ExpressionSheet(Scene):
    """One still with every character in every expression, labeled."""

    def construct(self):
        apply_style(self)
        rows = [
            ("Professor", [Professor(e) for e in Professor.EXPRESSIONS], 1.0),
            ("Student", [Student(e) for e in Student.EXPRESSIONS], 1.0),
            ("Computer", [Computer(e) for e in Computer.EXPRESSIONS], 1.0),
            ("Process", [Process(e, color=PROCESS_COLORS[i], label=f"PID {i + 1}")
                         for i, e in enumerate(Process.EXPRESSIONS)], 1.7),
        ]
        names = [Professor.EXPRESSIONS, Student.EXPRESSIONS, Computer.EXPRESSIONS,
                 Process.EXPRESSIONS]
        cell_w, row_h = 2.5, 3.5
        sheet = VGroup()
        for r, ((title, chars, scale), exprs) in enumerate(zip(rows, names)):
            base_y = -r * row_h
            for i, (ch, e) in enumerate(zip(chars, exprs)):
                ch.scale(scale)
                x = (i + 0.5) * cell_w
                # place the body's local origin at x and its base on base_y
                o = ch.to_global(ORIGIN)
                bottom = ch.to_global([0, -1.0, 0])[1]
                ch.shift([x - o[0], base_y - bottom, 0])
                lab = Text(e, font=FONT, font_size=30, color=DIM)
                lab.move_to([x, min(base_y - 0.42, ch.get_bottom()[1] - 0.22), 0])
                sheet.add(ch, lab)
            ttl = Text(title, font=FONT, font_size=34, color=TEXT, weight=BOLD)
            ttl.move_to([-0.2, base_y + 1.0, 0], aligned_edge=RIGHT)
            sheet.add(ttl)
            if r:
                sheet.add(Line([-2.4, base_y + row_h - 0.85, 0], [8 * cell_w, base_y + row_h - 0.85, 0],
                               stroke_color="#333333", stroke_width=2))
        sheet.scale_to_fit_height(config.frame_height - 0.3)
        if sheet.width > config.frame_width - 0.3:
            sheet.scale_to_fit_width(config.frame_width - 0.3)
        sheet.move_to(ORIGIN)
        self.add(sheet)


class CharacterDemo(Scene):
    """~15 s tour: enter, blink, look, talk, think, computer works, queue."""

    def construct(self):
        apply_style(self)
        prof = Professor().move_to(LEFT * 4.9 + DOWN * 1.9)
        stu = Student().flip().move_to(RIGHT * 4.9 + DOWN * 2.0)
        self.play(FadeIn(prof, shift=UP * 0.5), FadeIn(stu, shift=UP * 0.5), run_time=0.8)
        self.play(prof.blink(), stu.blink())
        self.play(prof.look_at(stu), stu.look_at(prof), run_time=0.5)
        self.play(prof.says("Let's meet\nthe processes!", expression="explaining"))
        self.wait(0.6)
        self.play(stu.thinks("What's a\nprocess?", expression="curious"))
        self.wait(0.6)
        self.play(prof.remove_bubble(), stu.remove_bubble(), prof.change("neutral"),
                  stu.change("neutral"), run_time=0.5)

        comp = Computer().scale(0.95).move_to(UP * 1.4)
        self.play(FadeIn(comp, shift=DOWN * 0.3), prof.look_at(UP * 1.4),
                  stu.look_at(UP * 1.4), run_time=0.7)
        self.play(comp.blink())

        procs = VGroup(*[Process(label=chr(65 + i)) for i in range(6)])
        procs.arrange(RIGHT, buff=0.3).move_to(DOWN * 2.6)
        self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.3) for p in procs], lag_ratio=0.25),
                  run_time=1.4)
        self.play(*[p.look_at(comp) for p in procs], run_time=0.4)

        first = procs[0]
        self.play(first.animate.move_to(comp.get_bottom() + DOWN * 0.45 + LEFT * 1.6),
                  procs[1:].animate.shift(LEFT * 0.6), run_time=0.7)
        self.play(first.change("running"), comp.change("busy"),
                  procs[1].change("blocked"), stu.change("excited"),
                  prof.change("proud"), run_time=0.7)
        self.wait(0.6)
        self.play(comp.change("overwhelmed"), stu.change("surprised"),
                  prof.change("worried"), *[p.change("ready") for p in procs[2:]])
        self.wait(0.5)
        self.play(comp.change("error"), first.change("zombie"), run_time=0.6)
        self.wait(0.4)
        self.play(comp.change("sleeping"), procs[1].change("done"),
                  first.change("done"), stu.change("bored"), prof.change("thinking"))
        self.play(comp.blink(), stu.blink(), run_time=0.4)
        self.play(FadeOut(first), FadeOut(procs[1]), run_time=0.6)
        self.wait(0.5)
