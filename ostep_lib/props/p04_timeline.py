"""Timeline: a Gantt-style grid of process states over time ticks.

State encoding (series standard, from episode 04):

=========  ===========================================================
running    solid fill in the row color, TEXT stroke 1
ready      row-color outline only (fill opacity 0.15)
blocked    DIM fill at 0.35 opacity + a tiny clock glyph
idle       dark grey #333333 with diagonal hatching (CPU row / idle CPU)
busy       CPU_COLOR solid (CPU-utilization row)
done/None  empty (no block)
=========  ===========================================================

Usage::

    tl = Timeline(["P0", "P1"], ticks=8, colors=[c0, c1], x_range=(-4.5, 3.5),
                  top=-1.2, row_step=0.6, cpu_row=True)
    self.play(Create(tl))
    self.play(tl.fill("P0", 1, "running"), tl.fill("P1", 1, "ready"))
    self.play(tl.fill_cpu(1, "busy"))
    self.play(tl.extend(10))            # rescale to 10 ticks within the same x range
    self.play(tl.unfill("P0", 4))       # rewind a block

Blocks live in ``tl.blocks`` (a VGroup inside the timeline) and are indexed by
``(row, tick)`` in ``tl.block_at``.  Ticks are 1-based.
"""
from __future__ import annotations

import numpy as np
from manim import (
    Animation, AnimationGroup, Create, FadeIn, FadeOut, GrowFromEdge, Line, Rectangle,
    Text, Transform, VGroup, ORIGIN, LEFT, RIGHT, UP, DOWN, smooth, linear,
)

from ..style import TEXT, DIM, CPU_COLOR, PROCESS_COLORS, BG
from .p04_icons import hatch_rect, mini_clock, IDLE_GREY

STATES = ("running", "ready", "blocked", "idle", "busy")


def _P(x, y=0.0):
    return np.array([float(x), float(y), 0.0])


class Timeline(VGroup):
    """Gantt grid with row labels, tick separators and tick labels.

    Parameters
    ----------
    rows : list of row names (also used as row labels).
    ticks : number of time slots.
    colors : list of colors (one per row); defaults to PROCESS_COLORS.
    x_range : (x_left, x_right) of the grid itself (labels sit outside it).
    top : y of the first row's center.
    row_height, row_step : height of a row and distance between row centers.
    tick_labels : show 1..N under the grid (``tick_label_y`` overrides their y).
    unit : optional text placed after the last tick label (e.g. "ms").
    cpu_row : add a "CPU" utilization row under the process rows.
    label_font, tick_font : font sizes.
    grid : draw the faint track and separators.
    """

    def __init__(self, rows, ticks=8, colors=None, x_range=(-5.0, 5.0), top=-2.2,
                 row_height=0.45, row_step=None, tick_labels=True, tick_label_y=None,
                 unit=None, cpu_row=False, cpu_label="CPU", label_font=24, tick_font=20,
                 grid=True, **kwargs):
        super().__init__(**kwargs)
        self.rows = list(rows)
        self.n_ticks = ticks
        self.colors = list(colors) if colors else [PROCESS_COLORS[i % 6] for i in range(len(rows))]
        self.x0, self.x1 = map(float, x_range)
        self.top_y = float(top)
        self.row_h = float(row_height)
        self.row_step = float(row_step) if row_step else row_height + 0.15
        self.has_cpu_row = cpu_row
        self.cpu_label = cpu_label
        self.label_font, self.tick_font = label_font, tick_font
        self.show_ticks = tick_labels
        self.tick_label_y = tick_label_y
        self.unit = unit
        self.show_grid = grid
        self.block_at = {}
        self.grid = self._build_grid(ticks)
        self.row_labels = self._build_row_labels()
        self.tick_labels = self._build_tick_labels(ticks)
        self.blocks = VGroup()
        self.add(self.grid, self.row_labels, self.tick_labels, self.blocks)

    # ------------------------------------------------------------- geometry
    @property
    def all_rows(self):
        return self.rows + ([self.cpu_label] if self.has_cpu_row else [])

    def row_index(self, row):
        if isinstance(row, int):
            return row
        return self.all_rows.index(row)

    def row_y(self, row):
        i = self.row_index(row)
        y = self.top_y - i * self.row_step
        if self.has_cpu_row and i == len(self.rows):
            y -= self.row_step * 0.25          # small gap above the CPU row
        return y

    def tick_width(self, ticks=None):
        return (self.x1 - self.x0) / (ticks or self.n_ticks)

    def cell_center(self, row, tick, ticks=None):
        w = self.tick_width(ticks)
        return _P(self.x0 + (tick - 0.5) * w, self.row_y(row))

    def tick_x(self, boundary, ticks=None):
        """x of the boundary *after* tick ``boundary`` (0 = left edge)."""
        return self.x0 + boundary * self.tick_width(ticks)

    def bottom_y(self):
        return self.row_y(len(self.all_rows) - 1) - self.row_h / 2

    # ------------------------------------------------------------- building
    def _build_grid(self, ticks):
        g = VGroup()
        if not self.show_grid:
            return g
        w = self.tick_width(ticks)
        for i, _ in enumerate(self.all_rows):
            y = self.row_y(i)
            track = Rectangle(width=self.x1 - self.x0, height=self.row_h)
            track.move_to(_P((self.x0 + self.x1) / 2, y)).set_fill(BG, 0).set_stroke(DIM, 1, opacity=0.5)
            seps = VGroup(*[Line(_P(self.x0 + k * w, y - self.row_h / 2), _P(self.x0 + k * w, y + self.row_h / 2))
                            for k in range(1, ticks)]).set_stroke(DIM, 1, opacity=0.35)
            g.add(VGroup(track, seps))
        return g

    def _build_row_labels(self):
        g = VGroup()
        for i, name in enumerate(self.all_rows):
            col = CPU_COLOR if (self.has_cpu_row and i == len(self.rows)) else self.colors[i]
            t = Text(str(name), font_size=self.label_font, color=col, weight="BOLD")
            t.next_to(_P(self.x0, self.row_y(i)), LEFT, buff=0.2)
            g.add(t)
        return g

    def _build_tick_labels(self, ticks):
        g = VGroup()
        if not self.show_ticks:
            return g
        y = self.tick_label_y if self.tick_label_y is not None else self.bottom_y() - 0.25
        for k in range(1, ticks + 1):
            t = Text(str(k), font_size=self.tick_font, color=DIM)
            t.move_to(_P(self.cell_center(0, k, ticks)[0], y))
            g.add(t)
        if self.unit:
            u = Text(self.unit, font_size=self.tick_font, color=DIM)
            u.next_to(_P(self.x1, y), RIGHT, buff=0.2)
            g.add(u)
        return g

    # --------------------------------------------------------------- blocks
    def make_block(self, row, tick, state, color=None, ticks=None, span=1):
        """Build (without adding) the block for ``state`` at (row, tick)."""
        i = self.row_index(row)
        if color is None:
            if self.has_cpu_row and i == len(self.rows):
                color = CPU_COLOR
            else:
                color = self.colors[i]
        w = self.tick_width(ticks) * span
        h = self.row_h
        inset = 0.03
        bw, bh = w - 2 * inset, h - 2 * inset
        c = self.cell_center(row, tick, ticks) + RIGHT * (span - 1) * self.tick_width(ticks) / 2
        if state in ("running", "busy"):
            r = Rectangle(width=bw, height=bh).set_fill(color, 1).set_stroke(TEXT, 1)
            b = VGroup(r)
        elif state == "ready":
            r = Rectangle(width=bw, height=bh).set_fill(color, 0.15).set_stroke(color, 2.5)
            b = VGroup(r)
        elif state == "blocked":
            r = Rectangle(width=bw, height=bh).set_fill(DIM, 0.35).set_stroke(DIM, 1)
            clk = mini_clock(radius=min(bh * 0.3, bw * 0.3), stroke_width=1.5)
            b = VGroup(r, clk)
        elif state == "idle":
            b = hatch_rect(bw, bh, spacing=max(bh / 3.5, 0.06))
        else:
            raise ValueError(f"unknown state {state!r}; use one of {STATES}")
        b.move_to(c)
        b.state = state
        return b

    def fill(self, row, tick, state, color=None, run_time=0.35, span=1):
        """Animation that grows a block for ``state`` into (row, tick).

        ``state`` None/"done" returns a no-op.  An existing block at that cell is
        replaced (cross-fade)."""
        i = self.row_index(row)
        if state in (None, "done", "empty"):
            return Animation(VGroup(), run_time=run_time)
        b = self.make_block(i, tick, state, color, span=span)
        old = self.block_at.get((i, tick))
        self.blocks.add(b)
        self.block_at[(i, tick)] = b
        grow = GrowFromEdge(b, LEFT, run_time=run_time, rate_func=linear)
        if old is not None:
            return AnimationGroup(grow, old.animate(run_time=run_time).set_opacity(0))
        return grow

    def set_block(self, row, tick, state, color=None):
        """Instantly place a block (no animation). Returns the block."""
        i = self.row_index(row)
        b = self.make_block(i, tick, state, color)
        old = self.block_at.get((i, tick))
        if old is not None:
            self.blocks.remove(old)
        self.blocks.add(b)
        self.block_at[(i, tick)] = b
        return b

    def fill_cpu(self, tick, state="busy", run_time=0.35):
        if not self.has_cpu_row:
            raise ValueError("Timeline was built without cpu_row=True")
        return self.fill(len(self.rows), tick, state, run_time=run_time)

    def fill_column(self, tick, states, run_time=0.35, cpu=None):
        """Fill one tick for several rows at once.

        ``states`` is a dict {row: state} or a list aligned with ``rows``.
        ``cpu`` optionally fills the CPU row ("busy"/"idle")."""
        if not isinstance(states, dict):
            states = dict(zip(self.rows, states))
        anims = [self.fill(r, tick, s, run_time=run_time) for r, s in states.items()
                 if s not in (None, "done", "empty")]
        if cpu is not None:
            anims.append(self.fill_cpu(tick, cpu, run_time=run_time))
        return AnimationGroup(*anims) if anims else Animation(VGroup(), run_time=run_time)

    def unfill(self, row, tick, run_time=0.3):
        """Animation that shrinks a block away to the left (rewind)."""
        i = self.row_index(row)
        b = self.block_at.pop((i, tick), None)
        if b is None:
            return Animation(VGroup(), run_time=run_time)
        target = b.copy().stretch(0.01, 0, about_edge=LEFT).set_opacity(0)
        return Transform(b, target, run_time=run_time)

    def unfill_ticks(self, ticks, run_time=0.8):
        """Rewind several ticks right-to-left (all rows), as one Succession-like
        LaggedStart. Returns an AnimationGroup."""
        from manim import LaggedStart
        groups = []
        for t in sorted(ticks, reverse=True):
            col = [self.unfill(i, t, run_time=run_time / max(len(ticks), 1))
                   for i in range(len(self.all_rows)) if (i, t) in self.block_at]
            if col:
                groups.append(AnimationGroup(*col))
        if not groups:
            return Animation(VGroup(), run_time=run_time)
        return LaggedStart(*groups, lag_ratio=1.0, run_time=run_time)

    def clear_blocks(self, run_time=0.6):
        """Fade every block out (they stay as invisible members until
        :meth:`purge` is called)."""
        bs = list(self.block_at.values())
        self.block_at = {}
        if not bs:
            return Animation(VGroup(), run_time=run_time)
        return AnimationGroup(*[b.animate(run_time=run_time).set_opacity(0) for b in bs])

    def purge(self):
        """Drop invisible (rewound/cleared) blocks. Call between plays."""
        live = set(id(b) for b in self.block_at.values())
        for b in list(self.blocks.submobjects):
            if id(b) not in live:
                self.blocks.remove(b)
        return self

    def blocks_in(self, row=None, ticks=None):
        """VGroup of the live blocks of a row (or all rows) and tick subset."""
        out = VGroup()
        for (i, t), b in sorted(self.block_at.items(), key=lambda kv: (kv[0][1], kv[0][0])):
            if row is not None and i != self.row_index(row):
                continue
            if ticks is not None and t not in ticks:
                continue
            out.add(b)
        return out

    # --------------------------------------------------------------- extend
    def extend(self, ticks, x_range=None, run_time=1.0):
        """Rescale the grid to ``ticks`` slots (inside the same x range, or a new
        ``x_range``)."""
        if x_range is not None:
            self.x0, self.x1 = map(float, x_range)
            self.row_labels.generate_target()
        new_grid = self._build_grid(ticks)
        new_labels = self._build_tick_labels(ticks)
        anims = [Transform(self.grid, new_grid), Transform(self.tick_labels, new_labels)]
        for (i, t), b in self.block_at.items():
            nb = self.make_block(i, t, b.state, ticks=ticks)
            # keep the original color of the block
            anims.append(Transform(b, nb))
        self.n_ticks = ticks
        return AnimationGroup(*anims, run_time=run_time)

    # -------------------------------------------------------------- markers
    def boundary_marker(self, boundary, label=None, color=TEXT, font_size=24, extra=0.25):
        """A vertical line at the boundary after tick ``boundary`` spanning all
        rows, with an optional label above. Not added."""
        x = self.tick_x(boundary)
        top = self.row_y(0) + self.row_h / 2 + extra
        bot = self.bottom_y() - 0.05
        ln = Line(_P(x, bot), _P(x, top)).set_stroke(color, 3)
        g = VGroup(ln)
        if label is not None:
            t = Text(label, font_size=font_size, color=color)
            t.next_to(ln, UP, buff=0.08)
            g.add(t)
        return g

    def ghost_blocks(self, spec, opacity=0.45):
        """Translucent blocks (not added, not tracked) for a what-if overlay.
        ``spec`` is a list of (row, tick, state)."""
        g = VGroup()
        for row, tick, state in spec:
            b = self.make_block(row, tick, state)
            b.set_opacity(opacity)
            g.add(b)
        return g


TIMELINE_STATES = STATES

__all__ = ["Timeline", "TIMELINE_STATES"]
