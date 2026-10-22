"""ProtocolChart: the book's Figures 6.1 / 6.2 as a multi-column, row-by-row listing.

    chart = ProtocolChart(["OS", "Program"], colors=[KERNEL_COLOR, USER_COLOR])
    self.play(chart.draw())
    self.play(chart.write_row(0, "Create entry for process list"))
    self.play(chart.write_row(1, "Run main()", bold=True))
    self.play(chart.link(a, b))        # arrow from row a to row b

* Time flows downward: each ``write_row`` adds one line, in the given column.
* A highlight cursor follows the newest row and every older row dims to 0.5.
* When the next row would pass ``bottom`` the rows scroll up (rows that leave the
  top fade out), so the newest row is always readable.
* Bold rows = privileged / key instructions.
* Rows (and link arrows) join the chart only when their animation begins, so several
  ``write_row`` calls can be chained in one ``Succession`` ahead of time.
"""
from __future__ import annotations

import numpy as np
from manim import (
    Animation, AnimationGroup, Arrow, Create, FadeIn, FadeOut, Line, Rectangle, Text,
    VGroup, VMobject, LEFT, RIGHT, UP, DOWN, BOLD, linear,
)

from ..style import TEXT, DIM, FONT, MONO_FONT, CPU_COLOR, VIRT

__all__ = ["ProtocolChart"]


def _P(x, y=0.0):
    return np.array([float(x), float(y), 0.0])


class _Reveal(Animation):
    """Adds ``mob`` to ``group`` when it begins and fades it in (keeping its own opacities)."""

    def __init__(self, group, mob, **kwargs):
        kwargs.setdefault("run_time", 0.7)
        kwargs.setdefault("rate_func", linear)
        self.group = group
        super().__init__(mob, **kwargs)

    def begin(self):
        if self.mobject not in self.group.submobjects:
            self.group.add(self.mobject)
        self._fam = [sm for sm in self.mobject.get_family() if isinstance(sm, VMobject) and len(sm.points)]
        self._fo = [sm.get_fill_opacity() for sm in self._fam]
        self._so = [sm.get_stroke_opacity() for sm in self._fam]
        self.mobject._base_ops = list(zip(self._fo, self._so))
        for sm in self._fam:
            sm.set_fill(opacity=0, family=False)
            sm.set_stroke(opacity=0, family=False)
        super().begin()

    def interpolate_mobject(self, alpha):
        a = float(np.clip(alpha, 0, 1))
        for sm, fo, so in zip(self._fam, self._fo, self._so):
            sm.set_fill(opacity=fo * a, family=False)
            sm.set_stroke(opacity=so * a, family=False)


class _ShiftFade(Animation):
    """Shift ``mob`` by ``delta`` and scale its opacity to ``factor`` times its revealed
    opacity (absolute, so repeated dimming never compounds).  Relative to the state at begin."""

    def __init__(self, mob, delta, factor, **kwargs):
        kwargs.setdefault("run_time", 0.7)
        kwargs.setdefault("rate_func", linear)
        self.delta = np.array(delta, dtype=float)
        self.factor = factor
        super().__init__(mob, **kwargs)

    def begin(self):
        self._fam = [sm for sm in self.mobject.get_family() if isinstance(sm, VMobject) and len(sm.points)]
        self._pts = [sm.points.copy() for sm in self._fam]
        base = getattr(self.mobject, "_base_ops", None)
        if base is None or len(base) != len(self._fam):
            base = [(sm.get_fill_opacity(), sm.get_stroke_opacity()) for sm in self._fam]
        self._base = base
        self._cur = [(sm.get_fill_opacity(), sm.get_stroke_opacity()) for sm in self._fam]
        super().begin()

    def interpolate_mobject(self, alpha):
        a = float(np.clip(alpha, 0, 1))
        for sm, p, (bf, bs), (cf, cs) in zip(self._fam, self._pts, self._base, self._cur):
            sm.points = p + self.delta * a
            sm.set_fill(opacity=cf * (1 - a) + bf * self.factor * a, family=False)
            sm.set_stroke(opacity=cs * (1 - a) + bs * self.factor * a, family=False)


class ProtocolChart(VGroup):
    """``ProtocolChart(columns, col_x=None, colors=None, top=2.55, bottom=-3.0, row_h=0.4,
    font_size=20, col_width=4.2, header_size=24)``.

    Parts: ``headers``, ``rule``, ``dividers``, ``cursor``, ``rows_group``, ``arrows``.
    ``draw()``; ``write_row(col, text, bold=False, mono=False, icon=None, color=None)``
    (animation; increments the row counter); ``section(text, color)``; ``link(a, b)``
    (animation drawing an arrow between two rows, by index); ``row(i)`` / ``row_text(i)``;
    ``sweep(col)`` (a translucent bar over a whole column, not added); ``clear_rows()``;
    ``n_rows``.
    """

    def __init__(self, columns, col_x=None, colors=None, top=2.55, bottom=-3.0, row_h=0.4,
                 font_size=20, col_width=4.2, header_size=24, **kwargs):
        super().__init__(**kwargs)
        self.columns = list(columns)
        n = len(columns)
        if col_x is None:
            col_x = list(np.linspace(-(n - 1) * col_width / 2, (n - 1) * col_width / 2, n)) if n > 1 else [0]
        self.col_x = [float(x) for x in col_x]
        self.col_width = col_width
        self.colors = list(colors) if colors else [TEXT] * n
        self.top, self.bottom, self.row_h, self.fs = float(top), float(bottom), float(row_h), font_size
        self.headers = VGroup(*[Text(c, font=FONT, font_size=header_size, color=col, weight=BOLD).move_to(_P(x, top))
                                for c, x, col in zip(columns, self.col_x, self.colors)])
        xl, xr = self.col_x[0] - col_width / 2, self.col_x[-1] + col_width / 2
        self.x_left, self.x_right = xl, xr
        self.rule = Line(_P(xl, top - 0.3), _P(xr, top - 0.3)).set_stroke(DIM, 2)
        self.dividers = VGroup(*[
            Line(_P((self.col_x[i] + self.col_x[i + 1]) / 2, top + 0.25),
                 _P((self.col_x[i] + self.col_x[i + 1]) / 2, bottom - 0.15)).set_stroke(DIM, 1, opacity=0.35)
            for i in range(n - 1)])
        self.cursor = Rectangle(width=xr - xl, height=row_h).set_fill(CPU_COLOR, 0).set_stroke(width=0)
        self.cursor.move_to(_P((xl + xr) / 2, top - 0.65))
        self.rows_group = VGroup()
        self.arrows = VGroup()
        self.items = []          # row mobjects in order of writing (visible or pending)
        self._y_of = []          # current center y of each row (tracked through scrolls)
        self.n_rows = 0
        self.first_y = top - 0.65
        self.add(self.dividers, self.rule, self.headers, self.cursor, self.arrows, self.rows_group)

    # ------------------------------------------------------------------ build
    def draw(self, run_time=1.0):
        return AnimationGroup(Create(self.rule), FadeIn(self.headers, shift=DOWN * 0.1),
                              Create(self.dividers), run_time=run_time)

    def _make_text(self, text, bold, mono, color):
        t = Text(text, font=MONO_FONT if mono else FONT, font_size=self.fs,
                 color=color or TEXT, weight=BOLD if bold else "NORMAL")
        if t.width > self.col_width - 0.3:
            t.scale_to_fit_width(self.col_width - 0.3)
        return t

    def _next_y(self):
        return self._y_of[-1] - self.row_h if self._y_of else self.first_y

    def _scroll_and_dim(self, y):
        """Returns (y after scrolling, scroll amount, animations for the existing rows)."""
        scroll = 0.0
        if y - self.row_h / 2 < self.bottom:
            scroll = self.bottom - (y - self.row_h / 2)
            y += scroll
        anims = []
        top_limit = self.top - 0.5
        for m, yy in zip(self.items, self._y_of):
            ny = yy + scroll
            anims.append(_ShiftFade(m, UP * scroll, 0.0 if ny > top_limit else 0.5))
        self._y_of = [yy + scroll for yy in self._y_of] + [y]
        return y, scroll, anims

    def write_row(self, col, text, bold=False, mono=False, icon=None, color=None, run_time=0.7):
        """Animation: write ``text`` in column ``col`` (index or name) on a new line."""
        ci = self.columns.index(col) if isinstance(col, str) else col
        y, scroll, anims = self._scroll_and_dim(self._next_y())
        t = self._make_text(text, bold, mono, color)
        t.move_to(_P(self.col_x[ci], y))
        item = VGroup(t)
        if icon is not None:
            icon = icon.copy()
            icon.scale_to_fit_height(0.3)
            icon.next_to(t, LEFT, buff=0.12)
            item.add(icon)
        self.items.append(item)
        self.n_rows += 1
        anims.append(self.cursor.animate.move_to(_P((self.x_left + self.x_right) / 2, y)).set_fill(CPU_COLOR, 0.16))
        anims.append(_Reveal(self.rows_group, item, run_time=run_time))
        return AnimationGroup(*anims, run_time=run_time)

    def section(self, text, color=VIRT, run_time=0.7):
        """A full-width section label row (e.g. "OS @ boot (kernel mode)")."""
        y, scroll, anims = self._scroll_and_dim(self._next_y())
        t = Text(text, font=FONT, font_size=self.fs + 2, color=color, weight=BOLD)
        t.move_to(_P(self.x_left + 0.1, y), aligned_edge=LEFT)
        item = VGroup(t)
        self.items.append(item)
        self.n_rows += 1
        anims.append(_Reveal(self.rows_group, item, run_time=run_time))
        return AnimationGroup(*anims, run_time=run_time)

    # ------------------------------------------------------------- queries
    def row(self, i):
        return self.items[i]

    def row_text(self, i):
        return self.items[i][0]

    def link(self, a, b, color=CPU_COLOR, run_time=0.8):
        """Animation drawing an arrow from row ``a`` to row ``b`` (indices), between the nearest
        text edges.  The arrow joins ``self.arrows`` (the last one is ``self.arrows[-1]`` after
        the animation has begun)."""
        ta, tb = self.row_text(a), self.row_text(b)
        ca, cb = ta.get_center(), tb.get_center()
        if abs(ca[0] - cb[0]) > 0.5:
            sgn = RIGHT if cb[0] > ca[0] else LEFT
            s = (ta.get_right() if cb[0] > ca[0] else ta.get_left()) + sgn * 0.1
            e = (tb.get_left() if cb[0] > ca[0] else tb.get_right()) - sgn * 0.1
        else:
            s, e = ta.get_bottom() + DOWN * 0.04, tb.get_top() + UP * 0.04
        arr = Arrow(s, e, buff=0, stroke_width=4, tip_length=0.16, max_tip_length_to_length_ratio=0.3, color=color)
        return _Reveal(self.arrows, arr, run_time=run_time)

    def sweep(self, col, color=CPU_COLOR, opacity=0.18):
        """A translucent bar covering a whole column (not added)."""
        ci = self.columns.index(col) if isinstance(col, str) else col
        x = self.col_x[ci]
        h = self.top - 0.45 - self.bottom
        bar = Rectangle(width=self.col_width - 0.2, height=h).set_fill(color, opacity).set_stroke(color, 2)
        return bar.move_to(_P(x, (self.top - 0.45 + self.bottom) / 2))

    def clear_rows(self, run_time=0.5):
        a = AnimationGroup(*[m.animate.set_opacity(0) for m in self.items], *[m.animate.set_opacity(0) for m in self.arrows],
                           self.cursor.animate.set_fill(CPU_COLOR, 0), run_time=run_time)
        self.items, self._y_of, self.n_rows = [], [], 0
        return a
