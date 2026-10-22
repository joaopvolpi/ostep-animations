"""Speech and thought bubbles."""
from __future__ import annotations

import numpy as np
from manim import (
    Circle, Ellipse, Mobject, Polygon, RoundedRectangle, Text, VGroup,
    RIGHT, config, smooth,
)
from manim.mobject.geometry.boolean_ops import Union

from ..style import TEXT
from .base import FONT, _Morph, P

BUBBLE_FILL = "#262626"


class Bubble(VGroup):
    """A speech (``kind="speech"``) or thought (``kind="thought"``) bubble.

    ``bubble.shape`` is the outline, ``bubble.content`` the text/mobject.
    The tail tip is at ``tip``; the body sits above it on the ``side``
    (RIGHT or LEFT) and is nudged to stay inside the frame.
    """

    def __init__(self, content, kind="speech", tip=np.zeros(3), side=RIGHT,
                 font_size=30, font=FONT, text_color=TEXT, fill_color=BUBBLE_FILL,
                 stroke_color=TEXT, stroke_width=3, padding=0.28,
                 max_width=5.0, lift=None, margin=0.15, **kwargs):
        super().__init__(**kwargs)
        if kind not in ("speech", "thought"):
            raise ValueError("Bubble kind must be 'speech' or 'thought'")
        if isinstance(content, str):
            content = Text(content, font=font, font_size=font_size, color=text_color,
                           line_spacing=0.8)
        if not isinstance(content, Mobject):
            raise TypeError("Bubble content must be a str or a Mobject")
        if content.width > max_width:
            content.scale_to_fit_width(max_width)
        tip = np.array(tip, dtype=float)
        s = 1.0 if np.array(side)[0] >= 0 else -1.0
        w = content.width + 2 * padding
        h = content.height + 2 * padding
        if kind == "speech":
            bw, bh = w, h
            lift = 0.45 if lift is None else lift
        else:
            a, b = w / 2 * 1.42, h / 2 * 1.42
            bw, bh = 2 * a + 0.3, 2 * b + 0.3
            lift = 0.75 if lift is None else lift
        center = tip + P(s * (bw / 2 - 0.15), bh / 2 + lift)
        fw, fh = config.frame_width, config.frame_height
        center[0] = np.clip(center[0], -fw / 2 + margin + bw / 2, fw / 2 - margin - bw / 2)
        center[1] = np.clip(center[1], -fh / 2 + margin + bh / 2, fh / 2 - margin - bh / 2)
        content.move_to(center)

        if kind == "speech":
            body = RoundedRectangle(width=w, height=h, corner_radius=min(0.25, h / 2.5)).move_to(center)
            bottom = center[1] - h / 2
            left, right = center[0] - w / 2, center[0] + w / 2
            bx = np.clip(tip[0] + s * 0.35, left + 0.35, right - 0.35)
            tail = Polygon(P(bx - 0.13, bottom + 0.08), P(bx + 0.13, bottom + 0.08), tip)
            shape = Union(body, tail)
            shape.set_fill(fill_color, 1).set_stroke(stroke_color, stroke_width)
        else:
            parts = [Ellipse(width=2 * a, height=2 * b).move_to(center)]
            per = 2 * np.pi * np.sqrt((a * a + b * b) / 2)
            n = max(9, int(per / 0.42))
            r = 0.26
            for i in range(n):
                t = 2 * np.pi * (i + 0.5) / n
                parts.append(Circle(radius=r).move_to(center + P(a * 0.93 * np.cos(t), b * 0.93 * np.sin(t))))
            cloud = Union(*parts)
            end = center + P(-s * a * 0.45, -b * 0.95)
            puffs = [Circle(radius=rr).move_to(tip + (end - tip) * k)
                     for k, rr in ((0.12, 0.05), (0.42, 0.085), (0.72, 0.12))]
            shape = VGroup(*puffs, cloud)
            shape.set_fill(fill_color, 1).set_stroke(stroke_color, stroke_width)
        self.kind = kind
        self.tip = tip
        self.shape = shape
        self.content = content
        self.add(shape, content)


class BubbleIn(_Morph):
    """Grow a bubble's shape from its tip, then fade in its content."""

    def __init__(self, bubble, **kwargs):
        kwargs.setdefault("run_time", 0.8)
        kwargs.setdefault("rate_func", smooth)
        super().__init__(bubble, **kwargs)

    def _setup(self):
        b = self.mobject
        s_end = b.shape.copy()
        s_start = b.shape.copy().scale(0.02, about_point=b.tip)
        c_end = b.content.copy()
        c_start = b.content.copy().set_opacity(0)
        return [(b.shape, s_start, s_end, 0, 0.6), (b.content, c_start, c_end, 0.35, 1)]
