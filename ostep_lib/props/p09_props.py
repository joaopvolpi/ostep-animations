"""Proportional-share props (episode 09): TargetPie, NumberStrip, JobList, PassLane, PassTable,
VruntimeMeter, RBTree, FairnessPlot.

Each is a VGroup built from primitives and the series colors.  Quick reference:

    pie = TargetPie((0.75, 0.25), radius=0.45, label="target")      pie.pulse()  pie.set_shares(...)
    ns = NumberStrip(100, [("A", 75, coral), ("B", 25, mint)], x_range=(-5, 5), y=-1.6)
        ns.marker_at(63) -> pointer mobject; ns.reorder(["B", "A"]) -> animation; ns.x_of(n)
    jl = JobList([("A", 100, coral), ("B", 50, mint), ("C", 250, gold)], at=(0.8, 1.2), gap=1.9)
        jl.node(i), jl.pointer(i), jl.reorder([2, 0, 1]), jl.total_tag
    lane = PassLane("A", coral, stride=100, y=1.4, x0=-5.0, scale=0.025)   lane.flag, lane.stride_bar, lane.step()
    table = PassTable(top_left=(2.4, 2.4)); table.add_row((0, 0, 0), "A") -> animation
    m = VruntimeMeter(coral, height=1.0); m.set_level(0.5) / m.add_runtime(12, weight=1024) -> animations; m.gap_to(other)
    tree = RBTree(); tree.node(14); tree.highlight_min(); tree.insert_path(20) -> list of node values
    fp = FairnessPlot(); fp.curve()
"""
from __future__ import annotations

import numpy as np
from manim import (
    Arrow, Axes, AnimationGroup, Circle, CurvedArrow, DashedLine, Dot, FadeIn, FadeOut, Indicate, Line, Polygon,
    Rectangle, RoundedRectangle, Sector, Succession, Text, Transform, UpdateFromAlphaFunc, VGroup, VMobject,
    DEGREES, DOWN, LEFT, ORIGIN, RIGHT, TAU, UP, rate_functions, Brace,
)

from ..style import BG, DIM, TEXT, CPU_COLOR, KERNEL_COLOR, PROCESS_COLORS, MONO_FONT
from .core import INK, outline_of

__all__ = ["TargetPie", "NumberStrip", "JobList", "PassLane", "PassTable", "VruntimeMeter", "RBTree",
           "FairnessPlot", "RB_SPEC"]

OKG = "#8BE07A"


def _P(x, y=0.0):
    return np.array([float(x), float(y), 0.0])


# ---------------------------------------------------------------------------
class TargetPie(VGroup):
    """Pie of shares (default 75/25 coral/mint), optional ``label`` under it.

    ``TargetPie(shares=(0.75, 0.25), colors=None, radius=0.45, label="target", font_size=18,
    stroke=DIM)``.  Parts: ``sectors``, ``label``.  ``set_shares(shares)`` animates;
    ``pulse()`` is an Indicate."""

    def __init__(self, shares=(0.75, 0.25), colors=None, radius=0.45, label="target", font_size=18,
                 stroke=DIM, **kwargs):
        super().__init__(**kwargs)
        self.radius, self.stroke = radius, stroke
        self.colors = list(colors) if colors else [PROCESS_COLORS[i] for i in range(len(shares))]
        self.shares = tuple(shares)
        self.sectors = self._sectors(self.shares)
        self.add(self.sectors)
        self.label = Text(label, font_size=font_size, color=DIM).next_to(self.sectors, DOWN, buff=0.08) if label else VGroup()
        self.add(self.label)

    def _sectors(self, shares):
        out, a = VGroup(), 90 * DEGREES
        for s, c in zip(shares, self.colors):
            out.add(Sector(radius=self.radius, start_angle=a, angle=-TAU * s).set_fill(c, 1)
                    .set_stroke(self.stroke, 2))
            a -= TAU * s
        return out

    def set_shares(self, shares, run_time=0.8):
        new = self._sectors(shares).move_to(self.sectors.get_center())
        self.shares = tuple(shares)
        return Transform(self.sectors, new, run_time=run_time)

    def pulse(self, **kw):
        return Indicate(self.sectors, **kw)


# ---------------------------------------------------------------------------
class NumberStrip(VGroup):
    """A horizontal ruler 0..``total`` with colored segments per owner.

    ``NumberStrip(total, segments, x_range=(-5, 5), y=0, height=0.4, ticks=None, show_labels=True,
    font_size=18)``; ``segments`` = [(name, size, color)] laid end to end.  Parts: ``line``, ``segs``
    (dict name -> Rectangle), ``seg_labels`` (name -> Text), ``tick_labels``.
    ``x_of(n)`` -> x of ticket number n boundary; ``marker_at(n)`` -> a pointer triangle + number
    above the strip (a VGroup, not added); ``reorder(order)`` -> animation that swaps the segments
    to the given name order."""

    def __init__(self, total, segments, x_range=(-5.0, 5.0), y=0.0, height=0.4, ticks=None,
                 show_labels=True, font_size=18, seg_label_size=20, **kwargs):
        super().__init__(**kwargs)
        self.total, self.x0, self.x1, self.y, self.h = total, float(x_range[0]), float(x_range[1]), float(y), height
        self.sizes = {n: s for n, s, _ in segments}
        self.colors = {n: c for n, _, c in segments}
        self.order = [n for n, _, _ in segments]
        self.font_size = font_size
        self.segs, self.seg_labels = {}, {}
        for n in self.order:
            r = Rectangle(width=1, height=height).set_fill(self.colors[n], 0.9).set_stroke(outline_of(self.colors[n]), 2)
            t = Text(n, font_size=seg_label_size, color=INK)
            self.segs[n], self.seg_labels[n] = r, t
        self.tick_labels = VGroup()
        self.line = Line(_P(self.x0, y - height / 2), _P(self.x1, y - height / 2)).set_stroke(DIM, 2)
        self._layout(self.order)
        self.add(self.line, *self.segs.values(), *self.seg_labels.values())
        self.ticks_at = ticks
        if ticks is not None:
            self.tick_labels = VGroup()
            for v in ticks:
                x = self.x_of(v)
                tk = Line(_P(x, y - height / 2), _P(x, y - height / 2 - 0.1)).set_stroke(DIM, 2)
                lab = Text(str(v), font_size=font_size, color=DIM, ) .next_to(tk, DOWN, buff=0.05)
                self.tick_labels.add(VGroup(tk, lab))
            self.add(self.tick_labels)

    def x_of(self, n):
        return self.x0 + (self.x1 - self.x0) * n / self.total

    def _layout(self, order):
        pos = 0
        w_all = self.x1 - self.x0
        self._targets = {}
        for n in order:
            w = w_all * self.sizes[n] / self.total
            cx = self.x0 + w_all * (pos + self.sizes[n] / 2) / self.total
            self._targets[n] = (w, cx)
            r, t = self.segs[n], self.seg_labels[n]
            r.stretch_to_fit_width(w).move_to(_P(cx, self.y))
            t.move_to(r)
            if t.width > w - 0.05:
                t.set_opacity(0)
            else:
                t.set_opacity(1)
            pos += self.sizes[n]

    def marker_at(self, n, color=CPU_COLOR, label=None, above=True):
        x = self.x_of(n)
        tri = Polygon(_P(0, -0.11), _P(-0.13, 0.11), _P(0.13, 0.11)).set_fill(color, 1).set_stroke(INK, 1.5)
        txt = Text(str(n if label is None else label), font_size=22, color=color)
        g = VGroup(tri, txt)
        # triangle tip touches the top of the strip; label above the triangle
        tri.move_to(_P(x, self.y + self.h / 2 + 0.11))
        txt.next_to(tri, UP, buff=0.04)
        g.tri, g.txt = tri, txt
        return g

    def reorder(self, order, run_time=1.0):
        """Animation: segments (and labels) glide to the new order."""
        w_all = self.x1 - self.x0
        anims, pos = [], 0
        for n in order:
            w = w_all * self.sizes[n] / self.total
            cx = self.x0 + w_all * (pos + self.sizes[n] / 2) / self.total
            anims.append(self.segs[n].animate.move_to(_P(cx, self.y)))
            anims.append(self.seg_labels[n].animate.move_to(_P(cx, self.y)))
            pos += self.sizes[n]
        self.order = list(order)
        return AnimationGroup(*anims, run_time=run_time)


# ---------------------------------------------------------------------------
class JobList(VGroup):
    """A linked list of job nodes ("Job:A Tix:100") with arrows, ``head`` and ``NULL``.

    ``JobList(nodes, at=(0.8, 1.2), gap=1.9, radius=0.34, font_size=18, tag=None)``;
    ``nodes`` = [(name, tickets, color)].  Parts: ``nodes`` (list of VGroup disc+letter),
    ``captions`` (list of Text under each node), ``arrows``, ``head``, ``null``.
    ``node(i)``, ``node_center(i)``, ``pointer(i, label="current")`` -> arrow+label above a node
    (a VGroup, not added), ``reorder(order)`` -> animation (``order`` = list of current indices in new
    order; arrows stay)."""

    def __init__(self, nodes, at=(0.8, 1.2), gap=1.9, radius=0.34, font_size=18, **kwargs):
        super().__init__(**kwargs)
        self.spec = list(nodes)
        self.gap, self.at, self.r = gap, np.array([float(at[0]), float(at[1]), 0.0]), radius
        self.nodes, self.captions, self.arrows = [], [], VGroup()
        for i, (name, tix, c) in enumerate(self.spec):
            d = Circle(radius=radius).set_fill("#3A3A3A", 1).set_stroke(c, 4)
            t = Text(name, font_size=24, color=c, weight="BOLD")
            n = VGroup(d, t)
            n.move_to(self.at + RIGHT * gap * i)
            cap = Text(f"{name} · {tix}", font_size=font_size, color=TEXT, font=MONO_FONT).next_to(n, DOWN, buff=0.1)
            self.nodes.append(n)
            self.captions.append(cap)
        self.head = Text("head", font_size=font_size, color=DIM).next_to(self.nodes[0], LEFT, buff=0.55)
        self.null = Text("NULL", font_size=font_size, color=DIM, font=MONO_FONT).next_to(self.nodes[-1], RIGHT, buff=0.55)
        self.head_arrow = Arrow(self.head.get_right(), self.nodes[0].get_left(), buff=0.06, stroke_width=3,
                                max_tip_length_to_length_ratio=0.3, color=DIM)
        for i in range(len(self.nodes)):
            nxt = self.nodes[i + 1] if i + 1 < len(self.nodes) else self.null
            self.arrows.add(Arrow(self.nodes[i].get_right(), nxt.get_left(), buff=0.06, stroke_width=3,
                                  max_tip_length_to_length_ratio=0.25, color=DIM))
        self.add(self.head, self.head_arrow, *self.nodes, *self.captions, self.arrows, self.null)

    def node(self, i):
        return self.nodes[i]

    def node_center(self, i):
        return self.nodes[i][0].get_center()

    def pointer(self, i, label="current"):
        c = self.node_center(i)
        a = Arrow(c + UP * (self.r + 0.55), c + UP * (self.r + 0.06), buff=0, stroke_width=4,
                  max_tip_length_to_length_ratio=0.35, color=CPU_COLOR)
        t = Text(label, font_size=18, color=CPU_COLOR, font=MONO_FONT).next_to(a, UP, buff=0.04)
        g = VGroup(a, t)
        return g

    def pointer_at(self, i):
        """Position (center) where a pointer built by ``pointer(0)`` should sit for node ``i``."""
        return self.node_center(i) + UP * (self.r + 0.3)

    def reorder(self, order, run_time=1.0):
        anims = []
        for new_i, old_i in enumerate(order):
            tgt = self.at + RIGHT * self.gap * new_i
            dx = tgt - self.nodes[old_i].get_center()
            anims.append(self.nodes[old_i].animate.shift(dx))
            anims.append(self.captions[old_i].animate.shift(dx))
        self.nodes = [self.nodes[o] for o in order]
        self.captions = [self.captions[o] for o in order]
        self.spec = [self.spec[o] for o in order]
        return AnimationGroup(*anims, run_time=run_time)


# ---------------------------------------------------------------------------
class PassLane(VGroup):
    """One runner lane on the pass number line.

    ``PassLane(name, color, stride, y, x0=-5.0, scale=0.025, length=260, font_size=20)``: a thin lane
    starting at x0 (pass 0), world scale ``scale`` units per pass unit.  Parts: ``track``, ``flag``
    (pole + pennant in ``color``), ``stride_bar`` (length = stride, placed under the lane, not added),
    ``pass_value``.  ``x_of(v)``; ``flag_to(v, run_time)`` -> animation."""

    def __init__(self, name, color, stride, y, x0=-5.0, scale=0.025, length=260, **kwargs):
        super().__init__(**kwargs)
        self.name, self.color, self.stride, self.y, self.x0, self.scale_ = name, color, stride, y, x0, scale
        self.pass_value = 0
        self.track = Line(_P(x0, y), _P(x0 + length * scale, y)).set_stroke(DIM, 2, opacity=0.6)
        pole = Line(_P(0, 0), _P(0, 0.5)).set_stroke(TEXT, 2.5)
        pen = Polygon(_P(0, 0.5), _P(0.3, 0.4), _P(0, 0.3)).set_fill(color, 1).set_stroke(outline_of(color), 1.5)
        self.flag = VGroup(pole, pen)
        self.flag.move_to(_P(x0, y), aligned_edge=DOWN)
        self.flag.shift(_P(0, y) - self.flag.get_bottom())
        self.stride_bar = Rectangle(width=stride * scale, height=0.16).set_fill(color, 0.9) \
            .set_stroke(outline_of(color), 1.5)
        self.stride_bar.move_to(_P(x0 + stride * scale / 2, y - 0.2))
        self.add(self.track, self.flag)

    def x_of(self, v):
        return self.x0 + v * self.scale_

    def flag_to(self, v, run_time=0.8):
        self.pass_value = v
        return self.flag.animate(run_time=run_time).shift(_P(self.x_of(v) - self.flag.get_bottom()[0]))


class PassTable(VGroup):
    """Figure 9.3 as a table: header + rows, added one at a time.

    ``PassTable(top_left=(2.4, 2.4), col_w=0.95, row_h=0.36, font_size=20, colors=None)``.
    ``add_row(values, who)`` -> animation (a new row slides in, the ``who`` cell tinted with the
    runner's color); ``rows`` lists the row groups; ``last_row``."""

    HEADER = ("A", "B", "C", "runs")

    def __init__(self, top_left=(2.4, 2.4), col_w=0.9, row_h=0.36, font_size=20, colors=None, **kwargs):
        super().__init__(**kwargs)
        self.tl, self.cw, self.rh, self.fs = np.array([top_left[0], top_left[1], 0.0]), col_w, row_h, font_size
        self.colors = colors or {"A": PROCESS_COLORS[0], "B": PROCESS_COLORS[1], "C": PROCESS_COLORS[2]}
        self.rows = []
        hdr = VGroup()
        for j, h in enumerate(self.HEADER):
            col = self.colors.get(h, DIM)
            t = Text(f"pass {h}" if h != "runs" else "runs", font_size=font_size - 2, color=col)
            t.move_to(self._cell(0, j))
            hdr.add(t)
        self.header = hdr
        self.rule = Line(self.tl + DOWN * row_h * 0.9, self.tl + RIGHT * col_w * 4 + DOWN * row_h * 0.9) \
            .set_stroke(DIM, 1.5)
        self.add(self.header, self.rule)

    def _cell(self, r, j):
        return self.tl + _P(self.cw * (j + 0.5), -self.rh * (r + 0.5) - (0.12 if r > 0 else 0))

    def add_row(self, values, who, run_time=0.5):
        r = len(self.rows) + 1
        row = VGroup()
        for j, v in enumerate(values):
            row.add(Text(str(v), font_size=self.fs, color=TEXT, font=MONO_FONT).move_to(self._cell(r, j)))
        w = Text(who, font_size=self.fs, color=self.colors[who], weight="BOLD").move_to(self._cell(r, 3))
        row.add(w)
        self.rows.append(row)
        self.add(row)
        return FadeIn(row, shift=DOWN * 0.15, run_time=run_time)

    @property
    def last_row(self):
        return self.rows[-1]


# ---------------------------------------------------------------------------
class VruntimeMeter(VGroup):
    """A vertical fuel-gauge bar with a process-colored fill.

    ``VruntimeMeter(color, height=1.0, width=0.32, max_value=100.0)``: ``level`` in [0, 1].
    ``set_level(v)`` and ``add_runtime(ms, weight=1024)`` return animations (the latter raises the level by
    ``ms * 1024/weight / max_value``).  ``gap_to(other)`` returns a double-ended bracket between the two
    fill tops; ``top_point()``; parts: ``frame``, ``fill``."""

    def __init__(self, color, height=1.0, width=0.32, max_value=100.0, level=0.0, **kwargs):
        super().__init__(**kwargs)
        self.color, self.h, self.w, self.max_value = color, height, width, max_value
        self.level = level
        self.frame = Rectangle(width=width, height=height).set_fill(BG, 1).set_stroke(DIM, 2.5)
        self.fill = Rectangle(width=width - 0.06, height=0.01).set_fill(color, 0.95).set_stroke(width=0)
        self.frame.set_fill(BG, 0.0)
        self.add(self.frame, self.fill)
        self._draw(level)

    def _draw(self, lv):
        lv = float(np.clip(lv, 0.0, 1.0))
        h = max(0.001, (self.h - 0.06) * lv)
        self.fill.stretch_to_fit_height(h)
        self.fill.move_to(self.frame.get_bottom() + UP * (0.03 + h / 2), aligned_edge=ORIGIN)
        self.fill.set_x(self.frame.get_x())
        self.fill.set_opacity(1.0 if lv > 0 else 0.0)

    def set_level_now(self, lv):
        self.level = float(np.clip(lv, 0, 1))
        self._draw(self.level)
        return self

    def set_level(self, lv, run_time=0.8):
        a0 = self.level
        lv = float(np.clip(lv, 0, 1))
        self.level = lv

        def f(m, alpha):
            m._draw(a0 + (lv - a0) * alpha)

        return UpdateFromAlphaFunc(self, f, run_time=run_time, rate_func=rate_functions.smooth)

    def add_runtime(self, ms, weight=1024, run_time=0.8):
        return self.set_level(self.level + ms * 1024.0 / weight / self.max_value, run_time=run_time)

    def top_point(self):
        return self.frame.get_bottom() + UP * (0.03 + (self.h - 0.06) * self.level)

    def gap_to(self, other, label=None, color=KERNEL_COLOR):
        a, b = self.top_point(), other.top_point()
        x = (self.frame.get_right()[0] + other.frame.get_left()[0]) / 2
        ya, yb = a[1], b[1]
        l1 = Line(_P(self.frame.get_right()[0] + 0.05, ya), _P(other.frame.get_left()[0] - 0.05, ya)).set_stroke(color, 2)
        l2 = Line(_P(self.frame.get_right()[0] + 0.05, yb), _P(other.frame.get_left()[0] - 0.05, yb)).set_stroke(color, 2)
        arr = Arrow(_P(x, min(ya, yb)), _P(x, max(ya, yb)), buff=0, stroke_width=3, color=color,
                    max_tip_length_to_length_ratio=0.25).add_tip(at_start=True)
        g = VGroup(l1, l2, arr)
        if label:
            g.add(Text(label, font_size=20, color=color).next_to(arr, RIGHT, buff=0.08))
        return g


# ---------------------------------------------------------------------------
# Figure 9.5: value -> (left, right, color)
RB_SPEC = {
    14: (9, 18, "black"), 9: (1, 10, "red"), 18: (17, 22, "red"),
    1: (None, 5, "black"), 10: (None, None, "black"), 17: (None, None, "black"),
    22: (21, 24, "black"), 5: (None, None, "red"), 21: (None, None, "red"), 24: (None, None, "red"),
}


class RBTree(VGroup):
    """A red-black tree (default: Figure 9.5).

    ``RBTree(spec=RB_SPEC, root=14, at=(0, 0), dx=0.62, dy=0.8, radius=0.25)``: nodes are circles with a
    red or black fill (white outline, value inside), small null stubs under leaves.  Layout is by
    in-order position.  Parts: ``nodes`` (value -> VGroup), ``edges`` (VGroup), ``stubs``.
    ``node(v)``, ``highlight_min()`` -> animation (leftmost node glows ``CPU_COLOR``),
    ``insert_path(v)`` -> list of node values visited, ``path_points(v)``, ``remove(v)`` -> animation
    that lifts node ``v`` out (to ``to`` if given)."""

    RED = "#D9423A"
    BLK = "#111111"

    def __init__(self, spec=RB_SPEC, root=14, at=(0.0, 0.0), dx=0.62, dy=0.8, radius=0.25, font_size=20, **kwargs):
        super().__init__(**kwargs)
        self.spec, self.root, self.r = spec, root, radius
        order = []

        def inorder(v, d):
            if v is None:
                return
            l, r, _ = spec[v]
            inorder(l, d + 1)
            order.append((v, d))
            inorder(r, d + 1)
        inorder(root, 0)
        n = len(order)
        pos = {}
        for i, (v, d) in enumerate(order):
            pos[v] = _P((i - (n - 1) / 2) * dx, -d * dy)
        self.pos = pos
        self.nodes, self.edges, self.stubs = {}, VGroup(), VGroup()
        for v, (l, r, col) in spec.items():
            if v not in pos:
                continue
            for ch in (l, r):
                if ch is not None:
                    self.edges.add(Line(pos[v], pos[ch]).set_stroke(DIM, 2.5))
            for k, ch in enumerate((l, r)):
                if ch is None:
                    s = pos[v] + _P((-0.17 if k == 0 else 0.17), -0.42)
                    self.stubs.add(Line(pos[v], s).set_stroke(DIM, 2, opacity=0.5))
                    self.stubs.add(Rectangle(width=0.1, height=0.1).set_fill(self.BLK, 1).set_stroke(DIM, 1).move_to(s + DOWN * 0.05))
        for v, (l, r, col) in spec.items():
            if v not in pos:
                continue
            c = self.RED if col == "red" else self.BLK
            circ = Circle(radius=radius).set_fill(c, 1).set_stroke(TEXT, 2.5)
            t = Text(str(v), font_size=font_size, color=TEXT, font=MONO_FONT).move_to(circ)
            g = VGroup(circ, t).move_to(pos[v])
            self.nodes[v] = g
        self.add(self.edges, self.stubs, *self.nodes.values())
        self.shift(np.array([at[0], at[1], 0.0]) - self.nodes[root].get_center())
        self.pos = {v: self.nodes[v].get_center() for v in self.nodes}

    def node(self, v):
        return self.nodes[v]

    def min_value(self):
        v = self.root
        while self.spec[v][0] is not None:
            v = self.spec[v][0]
        return v

    def highlight_min(self, color=CPU_COLOR):
        m = self.nodes[self.min_value()]
        return AnimationGroup(m[0].animate.set_stroke(color, 5), Indicate(m, color=color, scale_factor=1.25))

    def insert_path(self, value):
        path, v = [], self.root
        while v is not None:
            path.append(v)
            l, r, _ = self.spec[v]
            nxt = l if value < v else r
            if nxt is None:
                break
            v = nxt
        return path

    def path_points(self, value):
        return [self.pos[v] for v in self.insert_path(value)]

    def remove(self, v, to=None, run_time=0.8):
        n = self.nodes[v]
        edge_cut = []
        tgt = to if to is not None else n.get_center() + UP * 0.9
        return n.animate(run_time=run_time).move_to(tgt)


# ---------------------------------------------------------------------------
class FairnessPlot(VGroup):
    """Figure 9.2: fairness (0..1) against job length on a log x axis (1..1000).

    ``FairnessPlot(width=6.5, height=2.4, at=(0, -1.2))``.  Parts: ``axes``, ``labels``;
    ``point(length, f)`` -> scene coordinates; ``curve()`` -> the stylized VMobject (digitized by eye);
    ``ideal_line()`` -> dotted line at 1.0."""

    DATA = [(1, 0.5), (3, 0.7), (10, 0.8), (30, 0.9), (100, 0.96), (300, 0.98), (1000, 1.0)]

    def __init__(self, width=6.5, height=2.4, at=(0.0, -1.2), font_size=20, **kwargs):
        super().__init__(**kwargs)
        self.axes = Axes(x_range=[0, 3, 1], y_range=[0, 1.0, 0.5], x_length=width, y_length=height,
                         axis_config={"color": DIM, "stroke_width": 2.5, "include_ticks": False}, tips=False)
        self.axes.move_to(_P(*at))
        xl = VGroup(*[Text(str(10 ** k), font_size=font_size - 2, color=DIM).next_to(self.axes.c2p(k, 0), DOWN, buff=0.1)
                      for k in range(4)])
        yl = VGroup(*[Text(f"{v:g}", font_size=font_size - 2, color=DIM).next_to(self.axes.c2p(0, v), LEFT, buff=0.1)
                      for v in (0, 0.5, 1.0)])
        self.xtitle = Text("job length (time slices)", font_size=font_size, color=TEXT).next_to(xl, DOWN, buff=0.08)
        self.ytitle = Text("fairness", font_size=font_size, color=TEXT).next_to(self.axes.c2p(0, 1.0), UP, buff=0.12)
        self.labels = VGroup(xl, yl, self.xtitle, self.ytitle)
        self.add(self.axes, self.labels)

    def point(self, length, f):
        return self.axes.c2p(np.log10(length), f)

    def curve(self, color=PROCESS_COLORS[1]):
        pts = [self.point(x, y) for x, y in self.DATA]
        v = VMobject().set_points_smoothly(pts)
        v.set_stroke(color, 5).set_fill(opacity=0)
        return v

    def ideal_line(self):
        return DashedLine(self.axes.c2p(0, 1.0), self.axes.c2p(3, 1.0), color=DIM, dash_length=0.08, stroke_width=2)
