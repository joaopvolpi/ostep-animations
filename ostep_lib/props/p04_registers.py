"""RegisterBank: a grid of labeled CPU register boxes with values.

    regs = RegisterBank([("PC", "0x40"), ("SP", "0xff8"), ("FP", "0xffc"),
                         ("eax", "42"), ("ebx", "7"), ...], cols=2)
    self.play(regs.set_value("eax", "43"))
    self.play(regs.highlight("PC", CPU_COLOR))
    self.play(regs.flicker(rounds=3))        # values change as if being written

Register names and values use the monospace font (``MONO_FONT``).
"""
from __future__ import annotations

import random

import numpy as np
from manim import (
    AnimationGroup, Succession, RoundedRectangle, Text, Transform, VGroup, Wait,
    DOWN, LEFT, RIGHT, UP,
)

from ..style import TEXT, DIM, MONO_FONT, CPU_COLOR
from .p04_icons import CARD_FILL


class RegisterBank(VGroup):
    """Parameters: ``registers`` list of (name, value); ``cols``; ``box_width``,
    ``box_height``; ``font_size``; ``buff`` between boxes; ``title`` (optional
    text above the grid)."""

    def __init__(self, registers, cols=2, box_width=1.35, box_height=0.42, font_size=20,
                 buff=0.12, title=None, title_font=22, **kwargs):
        super().__init__(**kwargs)
        self.font_size = font_size
        self._box_w0 = box_width
        self.names = [n for n, _ in registers]
        self.boxes = {}
        self.name_texts = {}
        self.value_texts = {}
        grid = VGroup()
        for name, val in registers:
            box = RoundedRectangle(width=box_width, height=box_height, corner_radius=0.06)
            box.set_fill(CARD_FILL, 1).set_stroke(DIM, 2)
            nt = Text(name, font=MONO_FONT, font_size=font_size, color=DIM)
            nt.move_to(box.get_left() + RIGHT * 0.1, aligned_edge=LEFT)
            vt = Text(str(val), font=MONO_FONT, font_size=font_size, color=TEXT)
            vt.move_to(box.get_right() + LEFT * 0.1, aligned_edge=RIGHT)
            cell = VGroup(box, nt, vt)
            self.boxes[name], self.name_texts[name], self.value_texts[name] = box, nt, vt
            grid.add(cell)
        grid.arrange_in_grid(cols=cols, buff=buff)
        self.grid = grid
        self.add(grid)
        if title:
            self.title = Text(title, font_size=title_font, color=TEXT)
            self.title.next_to(grid, UP, buff=0.15)
            self.add(self.title)
        else:
            self.title = None

    def cell(self, name):
        return VGroup(self.boxes[name], self.name_texts[name], self.value_texts[name])

    def make_value(self, name, value, color=None):
        box = self.boxes[name]
        k = box.width / self._box_w0          # current scale of the bank
        vt = Text(str(value), font=MONO_FONT, font_size=self.font_size,
                  color=color or self.value_texts[name].get_color())
        vt.scale(k)
        vt.move_to(box.get_right() + LEFT * 0.1 * k, aligned_edge=RIGHT)
        return vt

    def set_value(self, name, value, run_time=0.3):
        return Transform(self.value_texts[name], self.make_value(name, value), run_time=run_time)

    def highlight(self, name, color=CPU_COLOR, run_time=0.5, fill_opacity=0.25):
        box = self.boxes[name]
        return AnimationGroup(
            box.animate(run_time=run_time).set_stroke(color, 3).set_fill(color, fill_opacity),
            self.name_texts[name].animate(run_time=run_time).set_color(color),
        )

    def unhighlight(self, name, run_time=0.5):
        box = self.boxes[name]
        return AnimationGroup(
            box.animate(run_time=run_time).set_stroke(DIM, 2).set_fill(CARD_FILL, 1),
            self.name_texts[name].animate(run_time=run_time).set_color(DIM),
        )

    def flicker(self, rounds=3, names=None, step=0.25, seed=4):
        """Succession of random value changes (as if instructions wrote them)."""
        rng = random.Random(seed)
        names = names or [n for n in self.names if n not in ("PC", "SP", "FP")] or self.names
        steps = []
        for _ in range(rounds):
            picks = rng.sample(names, k=min(3, len(names)))
            steps.append(AnimationGroup(*[self.set_value(n, str(rng.randint(0, 99)), run_time=step)
                                          for n in picks]))
        return Succession(*steps)


__all__ = ["RegisterBank"]
