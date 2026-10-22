"""CodeWalker: a Code block with several colored highlight bars (episode 05, reusable)."""
from __future__ import annotations

from manim import (
    Circumscribe, Code, FadeIn, Indicate, LaggedStart, Rectangle, Text, VGroup, Write, DOWN, LEFT, RIGHT,
)
import numpy as np

from ..style import DIM, CPU_COLOR, TEXT, MONO_FONT

__all__ = ["CodeWalker", "make_code"]


def make_code(src, font_size=20, line_numbers=False, language="c"):
    """A monokai ``Code`` block in the series font (the 04 recipe)."""
    return Code(code_string=src, language=language, formatter_style="monokai", add_line_numbers=line_numbers,
                background="rectangle",
                background_config={"fill_color": "#272822", "stroke_color": DIM, "stroke_width": 2,
                                   "corner_radius": 0.15, "buff": 0.25},
                paragraph_config={"font": MONO_FONT, "font_size": font_size, "line_spacing": 0.6})


class CodeWalker(VGroup):
    """``Code`` + any number of colored highlight bars.  Lines are numbered from 1.

    ``CodeWalker(src, font_size=20, caption=None, line_numbers=False)``.  The VGroup holds the
    code (``.code``) and the optional caption; **the bars are not children** (so FadeIn/FadeOut
    of a bar never fights the group): ``.bars`` is the list and ``.everything()`` gives
    ``VGroup(self, *bars)`` for moves and fades.

    * ``add_bar(color, line=1, opacity=0.25)`` -> the new bar (not added to the scene: use
      ``FadeIn(bar)``).  Bars on the same line are nested (later ones thinner) so both stay visible.
    * ``move_bar(i, line, run_time=0.5)`` -> animation.
    * ``bar_line(i)``; ``line_point(line, side)``; ``line_mob(line)``.
    * ``indicate(line, color)``; ``circumscribe(line, color)``.
    * ``write_in(run_time)`` -> the lines write in one after another.
    """

    def __init__(self, src, font_size=20, caption=None, line_numbers=False, **kwargs):
        super().__init__(**kwargs)
        self.code = make_code(src, font_size, line_numbers)
        self.add(self.code)
        self.caption = None
        if caption:
            self.caption = Text(caption, font_size=18, color=DIM).next_to(self.code, DOWN, buff=0.15)
            self.add(self.caption)
        self.bars = []
        self._lines = []

    def line_mob(self, line):
        return self.code.code_lines[line - 1]

    def _bar_for(self, i, line, color, opacity):
        ln = self.line_mob(line)
        bg = self.code.background
        h = max(ln.height, 0.22) + 0.1
        h *= max(0.35, 1 - 0.28 * i)
        bar = Rectangle(width=bg.width - 0.15 - 0.12 * i, height=h)
        bar.move_to(np.array([bg.get_x(), ln.get_y(), 0.0]))
        bar.set_fill(color, opacity).set_stroke(color, 1.5, opacity=0.8)
        return bar

    def add_bar(self, color=TEXT, line=1, opacity=0.25):
        i = len(self.bars)
        bar = self._bar_for(i, line, color, opacity)
        self.bars.append(bar)
        self._lines.append(line)
        return bar

    def bar_line(self, i):
        return self._lines[i]

    def move_bar(self, i, line, run_time=0.5):
        tgt = self._bar_for(i, line, self.bars[i].get_fill_color(), self.bars[i].get_fill_opacity())
        dy = tgt.get_y() - self.bars[i].get_y()
        self._lines[i] = line
        return self.bars[i].animate(run_time=run_time).shift(np.array([0, dy, 0.0]))

    def line_point(self, line, side="right"):
        ln = self.line_mob(line)
        x = self.code.background.get_right()[0] if side == "right" else self.code.background.get_left()[0]
        return np.array([x, ln.get_y(), 0.0])

    def indicate(self, line, color=CPU_COLOR):
        return Indicate(self.line_mob(line), color=color, scale_factor=1.08)

    def circumscribe(self, line, color=CPU_COLOR):
        return Circumscribe(self.line_mob(line), color=color, buff=0.08, fade_out=True)

    def write_in(self, run_time=2.0):
        n = len(self.code.code_lines)
        return LaggedStart(FadeIn(self.code.background, run_time=0.4),
                           *[Write(l) for l in self.code.code_lines], lag_ratio=0.18,
                           run_time=run_time) if n else FadeIn(self.code)

    def everything(self):
        return VGroup(self, *self.bars)
