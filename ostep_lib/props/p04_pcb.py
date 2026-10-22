"""PCBCard: a Process Control Block shown as a small card.

A colored header strip on the left (the process color + its name) and a grid of
``key: value`` fields.  Fields can be updated and highlighted.

    card = PCBCard("A", PROCESS_COLORS[0],
                   [("pid", "1"), ("state", "running"), ("memory", "…"), ("files", "…")])
    self.play(card.set_field("state", "ready"))
    self.play(card.indicate_field("state"))
"""
from __future__ import annotations

import numpy as np
from manim import (
    AnimationGroup, Indicate, Rectangle, RoundedRectangle, Text, Transform, VGroup,
    DOWN, LEFT, RIGHT, UP,
)

from ..style import TEXT, DIM, BG, CPU_COLOR
from .p04_icons import CARD_FILL

STATE_COLORS = {"running": CPU_COLOR, "ready": TEXT, "blocked": DIM}


def _P(x, y=0.0):
    return np.array([float(x), float(y), 0.0])


class PCBCard(VGroup):
    """Parameters: ``title`` (process name), ``color`` (header color),
    ``fields`` list of (key, value) pairs, ``width``/``height``, ``cols``
    (fields per row, default 2), ``col_widths`` (relative column widths),
    ``font_size``, ``header_width``."""

    def __init__(self, title, color, fields, width=3.6, height=1.0, cols=2, font_size=18,
                 header_width=0.55, title_font=28, col_widths=None, **kwargs):
        super().__init__(**kwargs)
        self.color = color
        self.font_size = font_size
        self._w0 = width
        self.body = RoundedRectangle(width=width, height=height, corner_radius=0.1)
        self.body.set_fill(CARD_FILL, 1).set_stroke(color, 2.5)
        self.header = RoundedRectangle(width=header_width, height=height, corner_radius=0.1)
        self.header.align_to(self.body, LEFT).set_fill(color, 1).set_stroke(color, 2.5)
        cover = Rectangle(width=header_width / 2, height=height).set_fill(color, 1).set_stroke(width=0)
        cover.align_to(self.header, RIGHT)
        self.title = Text(str(title), font_size=title_font, color=BG, weight="BOLD")
        if self.title.width > header_width - 0.08:
            self.title.scale_to_fit_width(header_width - 0.08)
        self.title.move_to(self.header)
        self.add(self.body, self.header, cover, self.title)

        self.keys = {}
        self.values = {}
        self._cells = {}
        rows = int(np.ceil(len(fields) / cols))
        x_left = self.header.get_right()[0] + 0.15
        avail_w = self.body.get_right()[0] - 0.1 - x_left
        fr = list(col_widths) if col_widths else [1.0 / cols] * cols
        fr = [f / sum(fr) for f in fr]
        col_x = [x_left + avail_w * sum(fr[:i]) for i in range(cols)]
        top = self.body.get_top()[1]
        row_h = height / rows
        for k, (key, val) in enumerate(fields):
            r, c = divmod(k, cols)
            col_w = avail_w * fr[c]
            anchor = _P(col_x[c], top - (r + 0.5) * row_h)
            kt = Text(f"{key}:", font_size=font_size, color=DIM)
            kt.move_to(anchor, aligned_edge=LEFT)
            vt = self._value_text(key, val)
            vt.next_to(kt, RIGHT, buff=0.08)
            self._fit(vt, anchor[0] + col_w - 0.05)
            self.keys[key] = kt
            self.values[key] = vt
            self._cells[key] = (kt, col_w, anchor)
            self.add(kt, vt)

    def _value_text(self, key, val):
        col = STATE_COLORS.get(str(val), TEXT) if key == "state" else TEXT
        return Text(str(val), font_size=self.font_size, color=col, weight="BOLD" if key == "state" else "NORMAL")

    @staticmethod
    def _fit(vt, max_x):
        if vt.get_right()[0] > max_x:
            left = vt.get_left()
            vt.scale_to_fit_width(max(max_x - left[0], 0.2))
            vt.move_to(left, aligned_edge=LEFT)

    def field(self, key):
        return self.values[key]

    def field_group(self, key):
        return VGroup(self.keys[key], self.values[key])

    def make_value(self, key, value):
        kt, col_w, _ = self._cells[key]
        k = self.body.width / self._w0          # current scale of the card
        vt = self._value_text(key, value).scale(k)
        vt.next_to(kt, RIGHT, buff=0.08 * k)
        self._fit(vt, kt.get_left()[0] + (col_w - 0.05) * k)
        return vt

    def set_field(self, key, value, run_time=0.6):
        """Animation transforming a field's value text."""
        new = self.make_value(key, value)
        return Transform(self.values[key], new, run_time=run_time)

    def set_field_now(self, key, value):
        self.values[key].become(self.make_value(key, value))
        return self

    def indicate_field(self, key, color=CPU_COLOR, run_time=0.7):
        return Indicate(self.field_group(key), color=color, scale_factor=1.15, run_time=run_time)


__all__ = ["PCBCard"]
