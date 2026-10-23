"""Episode 10 props: CacheCPU, ScheduleGrid and the Bus pulse helper.

CacheCPU -- a CPU chip with a cache strip hanging under it (3 mini cells)::

    c = CacheCPU("CPU 0", size=1.2)
    self.play(c.store("7", color=A_COLOR))       # next free cell fills and shows "7"
    self.play(c.set_value(0, "9"))               # Transform the text of a cell
    self.play(c.invalidate(0))                   # strike-through, then the cell empties
    self.play(c.warmth(2, A_COLOR))              # exactly 2 cells filled with the job color
    self.play(c.clear())
    c.slot_point()  (top of the chip)   c.cache_point()  (center of the strip)
    c.cache_bottom() (where data leaves toward memory)   c.cell_point(i)

ScheduleGrid -- the book's "CPU n x time slice" tables, colored per job letter::

    g = ScheduleGrid(rows=4, columns=5, cell_w=0.8, cell_h=0.5, colors={"A": ..., "B": ...})
    self.add(g)                                   # frame + row labels
    self.play(g.fill(0, 0, "A"))                  # 0-based row, col
    self.play(g.fill_column(0, "ABCD"))           # whole column, lagged
    self.play(g.fill_row(1, "BAEDC"))
    g.set(row, col, job)  (instant)    self.play(g.hatch(0, 3))  (idle cell)
    self.play(g.highlight_job("A"))   self.play(g.unhighlight())
    self.play(g.clear())

bus_pulse(bus, a, b, color) -- a bright dot (with halo) travels along ``bus.path(a, b)``.
"""
from __future__ import annotations

import numpy as np
from manim import (
    Animation, AnimationGroup, Circle, Create, Dot, FadeIn, FadeOut, GrowFromEdge, Line, LaggedStart,
    MoveAlongPath, Rectangle, RoundedRectangle, Succession, Text, Transform, UpdateFromAlphaFunc,
    VGroup, DOWN, UP, LEFT, RIGHT, ORIGIN, smooth, linear, there_and_back,
)

from ..style import TEXT, DIM, BG, MEM_COLOR, CPU_COLOR, KERNEL_COLOR, MONO_FONT, FONT, PROCESS_COLORS
from .core import CPU, outline_of, INK
from .p04_icons import hatch_rect, mix, IDLE_GREY

__all__ = ["CacheCPU", "ScheduleGrid", "bus_pulse"]


def _P(x, y=0.0):
    return np.array([float(x), float(y), 0.0])


# ---------------------------------------------------------------------------
# CacheCPU
# ---------------------------------------------------------------------------
class CacheCPU(VGroup):
    """``CacheCPU(label="CPU 0", size=1.2, n_cells=3)``.  Parts: ``cpu``, ``strip`` (rounded
    rectangle), ``cache_label``, ``cells`` (list of Rectangles), ``texts`` (list of Text, empty
    at first), ``link`` (the short wire between chip and cache)."""

    def __init__(self, label="CPU 0", size=1.2, n_cells=3, **kwargs):
        super().__init__(**kwargs)
        k = size / 1.2
        self.k = k
        self.cpu = CPU(size=size, label=label, font_size=max(12, int(22 * k)))
        sw, sh = 1.85 * k, 0.46 * k
        self.strip = RoundedRectangle(width=sw, height=sh, corner_radius=0.08 * k)
        self.strip.set_fill(mix(MEM_COLOR, BG, 0.85), 1).set_stroke(MEM_COLOR, 2.5)
        self.strip.next_to(self.cpu.body, DOWN, buff=0.27 * k)
        self.link = Line(self.cpu.body.get_bottom(), self.strip.get_top()).set_stroke(DIM, 3)
        self.cache_label = Text("cache", font_size=max(11, int(15 * k)), color=DIM)
        self.cache_label.move_to(self.strip.get_left() + RIGHT * 0.45 * k)
        self.cells = []
        self.texts = []
        self.fills = [None] * n_cells
        cw, ch, gap = 0.3 * k, 0.3 * k, 0.04 * k
        total = n_cells * cw + (n_cells - 1) * gap
        x0 = self.strip.get_right()[0] - 0.08 * k - total
        cy = self.strip.get_center()[1]
        for i in range(n_cells):
            r = Rectangle(width=cw, height=ch).set_fill(BG, 1).set_stroke(DIM, 1.5)
            r.move_to(_P(x0 + cw / 2 + i * (cw + gap), cy))
            self.cells.append(r)
            t = Text("", font=MONO_FONT, font_size=max(10, int(17 * k)), color=TEXT)
            t.move_to(r)
            self.texts.append(t)
        self.add(self.link, self.cpu, self.strip, self.cache_label, *self.cells, *self.texts)
        self.n_cells = n_cells
        self.used = 0

    # ------------------------------------------------------------ points
    def slot_point(self):
        return self.cpu.slot_point()

    def cache_point(self):
        return self.strip.get_center()

    def cache_top(self):
        return self.strip.get_top()

    def cache_bottom(self):
        return self.strip.get_bottom()

    def cell_point(self, i):
        return self.cells[i].get_center()

    def bottom_point(self):
        return self.strip.get_bottom()

    # --------------------------------------------------------- internals
    def _text_like(self, i, s, color=TEXT):
        t = Text(s, font=MONO_FONT, font_size=max(10, int(17 * self.k)), color=color)
        t.move_to(self.cells[i])
        return t

    def _fill_target(self, i, color, opacity=0.75):
        r = self.cells[i].copy()
        r.set_fill(color, opacity).set_stroke(outline_of(color), 2)
        return r

    def _empty_target(self, i):
        r = self.cells[i].copy()
        r.set_fill(BG, 1).set_stroke(DIM, 1.5)
        return r

    # --------------------------------------------------------- animations
    def store(self, value, color=TEXT, cell=None, run_time=0.5, text_color=None):
        """The next free cell (or ``cell``) fills with ``color`` and shows ``value``."""
        i = self.used if cell is None else cell
        if cell is None:
            self.used = min(self.used + 1, self.n_cells)
        tgt = self._fill_target(i, color)
        new_t = self._text_like(i, str(value), text_color or INK)
        self.fills[i] = color
        # the persistent text object of the cell is morphed into the new text
        return AnimationGroup(Transform(self.cells[i], tgt), Transform(self.texts[i], new_t), run_time=run_time)

    def set_value(self, i, value, color=None, run_time=0.5):
        new_t = self._text_like(i, str(value), color or INK)
        old = self.texts[i]
        anims = [Transform(old, new_t)]
        if color is not None:
            anims.append(Transform(self.cells[i], self._fill_target(i, color)))
            self.fills[i] = color
        return AnimationGroup(*anims, run_time=run_time)

    def invalidate(self, i=0, run_time=0.9):
        """Strike the cell's value through, then empty the cell."""
        c = self.cells[i]
        strike = Line(c.get_left() + LEFT * 0.04, c.get_right() + RIGHT * 0.04).set_stroke(KERNEL_COLOR, 4)
        strike.rotate(0.35)
        empty = self._empty_target(i)
        old_t = self.texts[i]
        self.fills[i] = None
        return Succession(
            Create(strike, run_time=run_time * 0.35),
            AnimationGroup(FadeOut(strike), Transform(c, empty), Transform(old_t, self._text_like(i, "")),
                           run_time=run_time * 0.65),
        )

    def warmth(self, level, color, run_time=None):
        """Exactly ``level`` cells (from the left) are filled with ``color``; the rest empty."""
        anims = []
        for i in range(self.n_cells):
            if i < level:
                anims.append(Transform(self.cells[i], self._fill_target(i, color, 0.8)))
                self.fills[i] = color
            else:
                anims.append(Transform(self.cells[i], self._empty_target(i)))
                self.fills[i] = None
        return LaggedStart(*anims, lag_ratio=0.35, run_time=run_time or 0.25 * self.n_cells + 0.3)

    def clear(self, run_time=0.5):
        anims = []
        for i in range(self.n_cells):
            anims.append(Transform(self.cells[i], self._empty_target(i)))
            empty = self._text_like(i, "")
            anims.append(Transform(self.texts[i], empty))
            self.fills[i] = None
        self.used = 0
        return AnimationGroup(*anims, run_time=run_time)

    def pulse(self, color=MEM_COLOR, run_time=0.8):
        from manim import Indicate
        return Indicate(self.strip, color=color, scale_factor=1.12, run_time=run_time)


# ---------------------------------------------------------------------------
# ScheduleGrid
# ---------------------------------------------------------------------------
class ScheduleGrid(VGroup):
    """CPU x time-slice table.  ``rows`` is an int (labels "CPU 0..") or a list of labels.
    Cells are addressed 0-based ``(row, col)``.  ``colors`` maps a job letter to a color."""

    def __init__(self, rows=4, columns=5, cell_w=0.8, cell_h=0.5, colors=None, row_labels=None,
                 label_size=20, letter_size=22, repeat_label=False, **kwargs):
        super().__init__(**kwargs)
        self.nrows = rows if isinstance(rows, int) else len(rows)
        self.ncols = columns
        self.cw, self.ch = cell_w, cell_h
        self.colors = dict(colors or {})
        self.letter_size = letter_size
        labels = row_labels or (rows if not isinstance(rows, int) else [f"CPU {i}" for i in range(rows)])
        W, H = columns * cell_w, self.nrows * cell_h
        self.frame = Rectangle(width=W, height=H).set_fill(mix(DIM, BG, 0.9), 1).set_stroke(DIM, 2)
        self.lines = VGroup()
        for c in range(1, columns):
            x = -W / 2 + c * cell_w
            self.lines.add(Line(_P(x, -H / 2), _P(x, H / 2)))
        for r in range(1, self.nrows):
            y = H / 2 - r * cell_h
            self.lines.add(Line(_P(-W / 2, y), _P(W / 2, y)))
        self.lines.set_stroke(DIM, 1, opacity=0.6)
        self.labels = VGroup()
        for r, s in enumerate(labels):
            t = Text(s, font_size=label_size, color=DIM)
            t.move_to(_P(-W / 2 - 0.15 - t.width / 2, H / 2 - (r + 0.5) * cell_h))
            self.labels.add(t)
        self.cells = {}   # (row, col) -> VGroup(rect, letter) or hatch
        self.jobs = {}    # (row, col) -> job letter or None
        self.add(self.frame, self.lines, self.labels)
        self.repeat = None
        if repeat_label:
            self.repeat = Text("... (repeat) ...", font_size=label_size - 2, color=DIM)
            self.repeat.next_to(self.frame, RIGHT, buff=0.2)
            self.add(self.repeat)
        self._home = self.frame.get_center()

    # -------------------------------------------------------- geometry
    def _unit_center(self, row, col):
        W, H = self.ncols * self.cw, self.nrows * self.ch
        return _P(-W / 2 + (col + 0.5) * self.cw, H / 2 - (row + 0.5) * self.ch)

    def cell_center(self, row, col):
        # follows moves/scales of the whole grid
        u = self._unit_center(row, col) - ORIGIN
        s = self.frame.width / (self.ncols * self.cw)
        return self.frame.get_center() + u * s

    def row_center(self, row):
        return self.cell_center(row, self.ncols // 2) if self.ncols % 2 else \
            (self.cell_center(row, self.ncols // 2 - 1) + self.cell_center(row, self.ncols // 2)) / 2

    def _make_cell(self, row, col, job):
        s = self.frame.width / (self.ncols * self.cw)
        color = self.colors.get(job, PROCESS_COLORS[4])
        rect = Rectangle(width=self.cw * s * 0.94, height=self.ch * s * 0.86)
        rect.set_fill(color, 0.95).set_stroke(outline_of(color), 2)
        txt = Text(job, font_size=self.letter_size * s, color=INK, weight="BOLD")
        g = VGroup(rect, txt).move_to(self.cell_center(row, col))
        g.job = job
        return g

    def _make_hatch(self, row, col):
        s = self.frame.width / (self.ncols * self.cw)
        h = hatch_rect(self.cw * s * 0.94, self.ch * s * 0.86, color=DIM, spacing=0.1 * s)
        h.move_to(self.cell_center(row, col))
        h.job = None
        return h

    def _drop(self, key):
        old = self.cells.pop(key, None)
        if old is not None:
            self.remove(old)
        return old

    def _put(self, key, mob):
        self._drop(key)
        self.cells[key] = mob
        self.add(mob)

    # ---------------------------------------------------------- instant
    def set(self, row, col, job):
        if job in (None, ".", " "):
            self._put((row, col), self._make_hatch(row, col))
            self.jobs[(row, col)] = None
        else:
            self._put((row, col), self._make_cell(row, col, job))
            self.jobs[(row, col)] = job
        return self

    def set_row(self, row, jobs, start=0):
        for i, j in enumerate(jobs):
            self.set(row, start + i, j)
        return self

    # --------------------------------------------------------- animated
    def fill(self, row, col, job, run_time=0.4):
        """Animation: the cell appears (grows from its left edge)."""
        key = (row, col)
        if job in (None, ".", " "):
            return self.hatch(row, col, run_time)
        m = self._make_cell(row, col, job)
        old = self.cells.get(key)
        self._put(key, m)
        self.jobs[key] = job
        if old is not None:
            return Transform(old, m, run_time=run_time) if False else FadeIn(m, run_time=run_time)
        return GrowFromEdge(m, LEFT, run_time=run_time)

    def hatch(self, row, col, run_time=0.4):
        key = (row, col)
        m = self._make_hatch(row, col)
        self._put(key, m)
        self.jobs[key] = None
        return FadeIn(m, run_time=run_time)

    def fill_row(self, row, jobs, start=0, run_time=0.35, lag=0.5):
        return LaggedStart(*[self.fill(row, start + i, j, run_time) for i, j in enumerate(jobs)],
                           lag_ratio=lag)

    def fill_column(self, col, jobs, run_time=0.35, lag=0.3):
        return LaggedStart(*[self.fill(r, col, j, run_time) for r, j in enumerate(jobs)], lag_ratio=lag)

    def highlight_job(self, job, dim_to=0.25, run_time=0.5):
        """Cells of ``job`` get a TEXT outline; everything else fades to ``dim_to``."""
        anims = []
        for key, m in self.cells.items():
            if self.jobs.get(key) == job:
                anims.append(m.animate.set_opacity(1).set_stroke(TEXT, 3))
            else:
                anims.append(m.animate.set_opacity(dim_to))
        return AnimationGroup(*anims, run_time=run_time)

    def unhighlight(self, run_time=0.5):
        anims = []
        for key, m in self.cells.items():
            job = self.jobs.get(key)
            if job is None:
                anims.append(m.animate.set_opacity(1))
            else:
                color = self.colors.get(job, PROCESS_COLORS[4])
                anims.append(m.animate.set_opacity(1).set_stroke(outline_of(color), 2))
        return AnimationGroup(*anims, run_time=run_time)

    def clear(self, run_time=0.5):
        mobs = list(self.cells.values())
        self.cells = {}
        self.jobs = {}
        for m in mobs:
            self.remove(m)
        if not mobs:
            return Animation(VGroup(), run_time=0.01)
        return FadeOut(VGroup(*mobs), run_time=run_time)

    def cell_mobs(self, job=None):
        return VGroup(*[m for k, m in self.cells.items() if job is None or self.jobs.get(k) == job])


# ---------------------------------------------------------------------------
# Bus pulse
# ---------------------------------------------------------------------------
def bus_pulse(bus, a, b, color=CPU_COLOR, run_time=1.0, radius=0.09):
    """A bright dot with a halo travels along ``bus.path(a, b)``.  The dot lives inside ``bus``
    (hidden when idle), so the bus must be in the scene."""
    path = bus.path(a, b)
    dot = Dot(path.get_start(), radius=radius, color=color)
    halo = Circle(radius=radius * 2.2).set_fill(color, 0.35).set_stroke(width=0).move_to(dot)
    pulse = VGroup(halo, dot)
    pulse.set_opacity(0)
    bus.add(pulse)
    holder = pulse

    def vis(m, alpha):
        on = 1.0 if 0.0 < alpha < 1.0 else 0.0
        halo.set_fill(color, 0.35 * on)
        dot.set_fill(color, on)

    return AnimationGroup(
        MoveAlongPath(holder, path, rate_func=linear),
        UpdateFromAlphaFunc(holder, vis, rate_func=linear),
        run_time=run_time,
    )
