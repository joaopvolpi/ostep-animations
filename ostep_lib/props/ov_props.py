"""Props introduced in episode 01-03 (Overview), reusable in later episodes.

Terminal, MemoryStrip, MappingArrows, SystemStack, InterleavingDemo,
UserKernelBoundary, PrivilegeGauge, EraRibbon.
"""
from __future__ import annotations

import numpy as np
from manim import (
    AddTextLetterByLetter, Animation, AnimationGroup, Circle, Create, CurvedArrow, DashedLine,
    Dot, FadeIn, FadeOut, Flash, Indicate, Line, Polygon, Rectangle, RoundedRectangle,
    Succession, Text, Transform, VGroup, VMobject, Wait, Write, ReplacementTransform,
    DOWN, LEFT, ORIGIN, RIGHT, UP, UL, UR, DL, DR, PI, BOLD, there_and_back, linear, smooth,
)

from ..style import (
    BG, CPU_COLOR, DIM, DISK_COLOR, FONT, KERNEL_COLOR, MEM_COLOR, MONO_FONT,
    PROCESS_COLORS, TEXT, USER_COLOR,
)
from ..characters import Process
from .core import CPU, Disk, Memory, CARD_FILL, INK, outline_of, place_on, base_point

TERM_FILL = "#111111"

__all__ = [
    "TERM_FILL", "Terminal", "MemoryStrip", "MappingArrows", "SystemStack", "InterleavingDemo",
    "UserKernelBoundary", "PrivilegeGauge", "EraRibbon", "make_thread",
]


# ---------------------------------------------------------------------------
# Terminal
# ---------------------------------------------------------------------------
class Terminal(VGroup):
    """Rounded console: DIM prompt, TEXT output, monospace, auto-scroll.

    ``Terminal(width=5.6, height=3.6, font_size=20, prompt="prompt>", title=None,
    cpus=None)``; ``cpus=1`` adds a small chip glyph "1 CPU" in the title bar.
    Animations (positions are computed when called, so call them in play order):
    ``type(cmd, run_time=None)`` types a prompt line, ``print(text, color=TEXT)``
    prints an output line, ``clear()`` empties the screen.  ``lines`` holds the
    visible lines; ``last_line()``.
    """

    def __init__(self, width=5.6, height=3.6, font_size=20, prompt="prompt>", title=None,
                 cpus=None, **kwargs):
        super().__init__(**kwargs)
        self.w, self.h = width, height
        self.font_size = font_size
        self.prompt = prompt
        self.frame = RoundedRectangle(width=width, height=height, corner_radius=0.18)
        self.frame.set_fill(TERM_FILL, 1).set_stroke(DIM, 2.5)
        bar_y = height / 2 - 0.22
        self.bar = Line([-width / 2 + 0.05, height / 2 - 0.44, 0], [width / 2 - 0.05, height / 2 - 0.44, 0])
        self.bar.set_stroke(DIM, 1.5, opacity=0.6)
        dots = VGroup(*[Dot(radius=0.05).set_fill(DIM, 0.8) for _ in range(3)]).arrange(RIGHT, buff=0.09)
        dots.move_to([-width / 2 + 0.3, bar_y, 0])
        self.add(self.frame, self.bar, dots)
        self.title = VGroup()
        if title:
            self.title = Text(title, font=MONO_FONT, font_size=16, color=DIM).move_to([0, bar_y, 0])
            self.add(self.title)
        self.glyph = VGroup()
        if cpus:
            chip = CPU(size=0.26, label=None, pins=2)
            lab = Text(f"{cpus} CPU" + ("s" if cpus > 1 else ""), font=MONO_FONT, font_size=14, color=CPU_COLOR)
            self.glyph = VGroup(chip, lab).arrange(RIGHT, buff=0.1)
            self.glyph.move_to([width / 2 - 0.2, bar_y, 0], aligned_edge=RIGHT)
            self.add(self.glyph)
        ref = Text("Ag", font=MONO_FONT, font_size=font_size)
        self.line_h = ref.height * 1.55
        self.top_y = height / 2 - 0.44 - 0.12
        self.left_x = -width / 2 + 0.22
        self.capacity = max(1, int((height - 0.44 - 0.2) / self.line_h))
        self.lines = VGroup()
        self.add(self.lines)

    # -------------------------------------------------------------- helpers
    def _origin(self):
        # frame may have been moved/scaled: map local layout through the frame
        return self.frame.get_center(), self.frame.width / self.w

    def _slot(self, k):
        c, s = self._origin()
        return c + s * np.array([self.left_x, self.top_y - self.line_h * (k + 0.5), 0])

    def _make_line(self, prompt_part, text_part, color):
        c, s = self._origin()
        parts = VGroup()
        if prompt_part:
            parts.add(Text(prompt_part, font=MONO_FONT, font_size=self.font_size, color=DIM))
        if text_part:
            parts.add(Text(text_part, font=MONO_FONT, font_size=self.font_size, color=color))
        parts.arrange(RIGHT, buff=0.14, aligned_edge=DOWN)
        parts.scale(s)
        maxw = (self.w - 0.4) * s
        if parts.width > maxw:
            parts.scale_to_fit_width(maxw)
        return parts

    def _place_new(self, line):
        anims = []
        k = len(self.lines)
        if k >= self.capacity:
            old = self.lines[0]
            self.lines.remove(old)
            anims.append(FadeOut(old, shift=UP * self.line_h * 0.6))
            dy = UP * self.line_h * self._origin()[1]
            for ln in list(self.lines):
                anims.append(ln.animate.shift(dy))
            k = self.capacity - 1
        line.move_to(self._slot(k), aligned_edge=LEFT)
        self.lines.add(line)
        return anims

    # ------------------------------------------------------------ animations
    def type(self, cmd, run_time=None):
        line = self._make_line(self.prompt, cmd, TEXT)
        anims = self._place_new(line)
        rt = run_time if run_time is not None else min(1.6, 0.35 + 0.045 * len(cmd))
        typing = [FadeIn(line[0], run_time=0.15)] if self.prompt else []
        body = line[-1]
        typing.append(AddTextLetterByLetter(body, run_time=rt, rate_func=linear))
        if anims:
            return Succession(AnimationGroup(*anims, run_time=0.25), *typing)
        return Succession(*typing)

    def print(self, text, color=TEXT, run_time=0.25):
        line = self._make_line(None, text, color)
        anims = self._place_new(line)
        return AnimationGroup(*anims, FadeIn(line, run_time=run_time), run_time=run_time)

    def prompt_line(self, run_time=0.2):
        """A fresh, empty prompt."""
        line = self._make_line(self.prompt, None, TEXT)
        anims = self._place_new(line)
        return AnimationGroup(*anims, FadeIn(line), run_time=run_time)

    def pop(self, run_time=0.2):
        """Remove the last line (returns its FadeOut)."""
        last = self.lines[-1]
        self.lines.remove(last)
        return FadeOut(last, run_time=run_time)

    def clear(self, run_time=0.3):
        old = self.lines
        self.lines = VGroup()
        self.remove(old)
        self.add(self.lines)
        return FadeOut(old, run_time=run_time)

    def last_line(self):
        return self.lines[-1] if len(self.lines) else self.frame


# ---------------------------------------------------------------------------
# MemoryStrip (horizontal)
# ---------------------------------------------------------------------------
class MemoryStrip(VGroup):
    """Horizontal memory array with hex addresses under the cells.

    ``MemoryStrip(n=12, cell_width=0.9, cell_height=0.7, start=0x1FFFFC, step=4,
    addresses=None, values=None, font_size=22, address_size=13, color=MEM_COLOR,
    show_addresses=True)``.  ``addresses`` (list of str) overrides start/step.
    Parts: ``cells``, ``values`` (Text, may be empty), ``addresses``.
    ``index_of(addr)`` accepts an int index, an int address or a "0x..." string.
    Animations: ``set_value(i, v)``, ``read(i, to_point)`` (a copy of the value flies
    out; returns (animation, flying_copy)), ``write(i, v, from_point)``,
    ``color_cell(i, color, opacity=0.55)``, ``pulse(i)``.
    """

    def __init__(self, n=12, cell_width=0.9, cell_height=0.7, start=0x1FFFFC, step=4,
                 addresses=None, values=None, font_size=22, address_size=13, color=MEM_COLOR,
                 show_addresses=True, **kwargs):
        super().__init__(**kwargs)
        self.color = color
        self.font_size = font_size
        if addresses is None:
            addresses = [f"0x{start + step * i:06X}" for i in range(n)]
        self.address_strs = list(addresses)
        values = list(values or []) + [""] * (n - len(values or []))
        self.cells = VGroup()
        for i in range(n):
            r = Rectangle(width=cell_width, height=cell_height)
            r.set_fill(color, 0.15).set_stroke(color, 3)
            self.cells.add(r)
        self.cells.arrange(RIGHT, buff=0)
        self.values = VGroup(*[self._val(v, r) for v, r in zip(values, self.cells)])
        self.addresses = VGroup()
        if show_addresses:
            for a, r in zip(self.address_strs, self.cells):
                t = Text(a, font=MONO_FONT, font_size=address_size, color=DIM)
                if t.width > cell_width * 0.95:
                    t.scale_to_fit_width(cell_width * 0.95)
                t.next_to(r, DOWN, buff=0.1)
                self.addresses.add(t)
        self.add(self.cells, self.values, self.addresses)

    def _val(self, v, r):
        if v == "" or v is None:
            return VGroup().move_to(r)
        t = Text(str(v), font=MONO_FONT, font_size=self.font_size, color=TEXT)
        if t.width > r.width * 0.85:
            t.scale_to_fit_width(r.width * 0.85)
        return t.move_to(r)

    def index_of(self, key):
        if isinstance(key, str):
            k = key.upper().replace("0X", "0x")
            for i, a in enumerate(self.address_strs):
                if a.upper().replace("0X", "0x") == k:
                    return i
            return self.index_of(int(key, 16))
        if key >= len(self.cells):
            for i, a in enumerate(self.address_strs):
                if int(a, 16) == key:
                    return i
            raise KeyError(key)
        return key

    def cell(self, key):
        return self.cells[self.index_of(key)]

    def set_value(self, key, v, run_time=0.4):
        i = self.index_of(key)
        old = self.values[i]
        new = self._val(v, self.cells[i])
        self.values.submobjects[i] = new
        if len(old.points) == 0 and not old.submobjects:
            return FadeIn(new, scale=1.3, run_time=run_time)
        return AnimationGroup(FadeOut(old, shift=UP * 0.2), FadeIn(new, shift=UP * 0.2), run_time=run_time)

    def read(self, key, to_point, run_time=0.8):
        i = self.index_of(key)
        src = self.values[i]
        cp = src.copy()
        return cp.animate(run_time=run_time).move_to(to_point).scale(1.3), cp

    def write(self, key, v, from_point, run_time=0.8):
        """Animation: the new value flies in from ``from_point`` and replaces the old one."""
        i = self.index_of(key)
        old = self.values[i]
        target = self._val(v, self.cells[i])
        fly = target.copy().move_to(from_point).scale(1.3)
        self.values.submobjects[i] = fly
        return AnimationGroup(FadeIn(fly, run_time=0.01),
                              fly.animate(run_time=run_time).move_to(target).scale(1 / 1.3),
                              FadeOut(old, scale=0.5, run_time=run_time))

    def color_cell(self, key, color, opacity=0.55, run_time=0.5):
        return self.cell(key).animate(run_time=run_time).set_fill(color, opacity).set_stroke(color)

    def pulse(self, key, color=CPU_COLOR, run_time=0.4):
        r = self.cell(key)
        flash = r.copy().set_fill(color, 0.5).set_stroke(color, 4)
        return Succession(FadeIn(flash, run_time=run_time / 2), FadeOut(flash, run_time=run_time / 2))


# ---------------------------------------------------------------------------
# MappingArrows
# ---------------------------------------------------------------------------
class MappingArrows(VGroup):
    """Curved arrows from virtual cells to physical cells (crossing a split).

    ``MappingArrows([(src_mob, dst_mob, color), ...], angle=-0.5, stroke_width=4)``:
    each arrow goes from the bottom of ``src`` to the top of ``dst``.
    ``create()`` and ``pulse()`` animations.
    """

    def __init__(self, pairs, angle=-0.5, stroke_width=4, **kwargs):
        super().__init__(**kwargs)
        for src, dst, color in pairs:
            a = CurvedArrow(src.get_bottom() + DOWN * 0.05, dst.get_top() + UP * 0.05, angle=angle,
                            tip_length=0.2)
            a.set_stroke(color, stroke_width)
            a.tip.set_fill(color, 1).set_stroke(color)
            self.add(a)

    def create(self, run_time=1.2):
        return AnimationGroup(*[Create(a) for a in self], run_time=run_time)

    def pulse(self, run_time=0.8):
        return AnimationGroup(*[Indicate(a, scale_factor=1.0, color=TEXT) for a in self], run_time=run_time)


# ---------------------------------------------------------------------------
# SystemStack
# ---------------------------------------------------------------------------
class SystemStack(VGroup):
    """Hardware row (CPU, Memory, Disk) + OS band; programs stand above the band.

    ``SystemStack(hw_y=-2.3, band_y=-0.9, programs_y=0.8, hw_x=(-3, 0, 3), band_width=10,
    band_height=0.8, cpu_size=0.84, mem_size=(0.9, 1.6), disk_width=1.0,
    label="Operating System")``.  Parts: ``cpu``, ``memory``, ``disk``, ``hardware``
    (VGroup of the three), ``band`` (rect), ``band_label``.
    ``program_point(i, n=3)`` = where program i stands (base point).
    ``relabel(text)`` animation (crossfades the band label), ``route(start, hw)``
    returns two segments start -> band and band -> hardware, ``doors(names)`` returns a VGroup of
    labeled notches on the band's top edge (not added).
    """

    def __init__(self, hw_y=-2.3, band_y=-0.9, programs_y=0.8, hw_x=(-3, 0, 3), band_width=10.0,
                 band_height=0.8, cpu_size=0.84, mem_size=(0.9, 1.6), disk_width=1.0,
                 label="Operating System", label_size=28, **kwargs):
        super().__init__(**kwargs)
        self.hw_y, self.band_y, self.programs_y, self.hw_x = hw_y, band_y, programs_y, hw_x
        self.cpu = CPU(size=cpu_size).move_to([hw_x[0], hw_y, 0])
        self.memory = Memory(cells=5, width=mem_size[0], height=mem_size[1], addresses=False)
        self.memory.move_to([hw_x[1], hw_y, 0])
        self.disk = Disk(width=disk_width, height=disk_width * 0.85).move_to([hw_x[2], hw_y, 0])
        self.hardware = VGroup(self.cpu, self.memory, self.disk)
        self.band = RoundedRectangle(width=band_width, height=band_height, corner_radius=0.12)
        self.band.set_fill(KERNEL_COLOR, 0.25).set_stroke(KERNEL_COLOR, 3).move_to([0, band_y, 0])
        self.label_size = label_size
        self.band_label = Text(label, font=FONT, font_size=label_size, color=TEXT).move_to(self.band)
        self.add(self.hardware, self.band, self.band_label)

    def program_point(self, i, n=3):
        xs = self.hw_x if n == 3 else np.linspace(-4, 4, n)
        return np.array([xs[i], self.programs_y - 0.5, 0])

    def relabel(self, text, color=TEXT, run_time=0.6):
        new = Text(text, font=FONT, font_size=self.label_size, color=color).move_to(self.band)
        if new.width > self.band.width - 0.3:
            new.scale_to_fit_width(self.band.width - 0.3)
        old = self.band_label
        self.band_label = new
        self.remove(old)
        self.add(new)
        return AnimationGroup(FadeOut(old, shift=UP * 0.15), FadeIn(new, shift=UP * 0.15), run_time=run_time)

    def route(self, start, hw, dashed=True, color=TEXT, width=2.5):
        """Request path through the OS: a segment from ``start`` down to the band's top,
        and a segment from the band's bottom down to ``hw`` (the OS does the routing).
        Returns a VGroup of the two (dashed) lines."""
        start = np.array(start, dtype=float)
        end = hw.get_top() + UP * 0.05
        L = DashedLine if dashed else Line
        kw = dict(dash_length=0.1) if dashed else {}
        a = L(start, np.array([start[0], self.band.get_top()[1], 0]), **kw)
        b = L(np.array([end[0], self.band.get_bottom()[1], 0]), end, **kw)
        return VGroup(a, b).set_stroke(color, width)

    def doors(self, names, xs=None, color=TEXT):
        xs = xs if xs is not None else np.linspace(-3.5, 3.5, len(names))
        g = VGroup()
        top = self.band.get_top()[1]
        for x, n in zip(xs, names):
            door = RoundedRectangle(width=0.7, height=0.34, corner_radius=0.1)
            door.set_fill(BG, 1).set_stroke(KERNEL_COLOR, 2.5).move_to([x, top, 0])
            lab = Text(n, font=MONO_FONT, font_size=16, color=color).move_to(door)
            if lab.width > 0.62:
                lab.scale_to_fit_width(0.62)
            g.add(VGroup(door, lab))
        return g


# ---------------------------------------------------------------------------
# Threads + InterleavingDemo
# ---------------------------------------------------------------------------
def make_thread(label="T1", color=None, scale=0.65, expression="ready"):
    """Thread stand-in: a Process scaled x0.65 with a T-label."""
    return Process(expression, color=color or PROCESS_COLORS[1], label=label).scale(scale)


class InterleavingDemo(VGroup):
    """Shared counter cell + two threads with register boxes + step lanes.

    ``InterleavingDemo(value=5, cell_label="counter", labels=("T1", "T2"),
    colors=(PROCESS_COLORS[1], PROCESS_COLORS[3]), cell_pos=(0, 2.2),
    thread_pos=((-4, 0.2), (4, 0.2)), lane_x=(-2.5, 2.5), lane_ys=(-0.9, -1.7, -2.5))``.
    Parts: ``cell``, ``cell_value``, ``threads`` (2 Processes), ``regs`` (2 boxes),
    ``reg_values``, ``lanes`` (2 VGroups of 3 op blocks), ``step_label``.
    ``play_step(thread, op)`` with thread 0/1 and op "load"/"add"/"store" returns an
    animation and updates the internal values (create it right before playing it);
    ``steps(list)`` is a generator of them.
    ``reset(value)`` animation.  ``value`` is the current cell value.
    """

    OPS = ("load", "add", "store")
    OP_TEXT = {"load": "load r ← counter", "add": "r = r + 1", "store": "store counter ← r"}

    def __init__(self, value=5, cell_label="counter", labels=("T1", "T2"),
                 colors=(PROCESS_COLORS[1], PROCESS_COLORS[3]), cell_pos=(0, 2.2),
                 thread_pos=((-4.6, 0.0), (4.6, 0.0)), lane_x=(-2.4, 2.4),
                 lane_ys=(-1.0, -1.8, -2.6), **kwargs):
        super().__init__(**kwargs)
        self.value = value
        self.colors = colors
        self.cell = RoundedRectangle(width=1.6, height=1.0, corner_radius=0.1)
        self.cell.set_fill(MEM_COLOR, 0.2).set_stroke(MEM_COLOR, 4).move_to([*cell_pos, 0])
        self.cell_title = Text(cell_label, font=MONO_FONT, font_size=22, color=MEM_COLOR)
        self.cell_title.next_to(self.cell, UP, buff=0.12)
        self.cell_value = self._num(value, 40).move_to(self.cell)
        self.threads = VGroup()
        self.regs = VGroup()
        self.reg_values = [None, None]
        self.reg_texts = [VGroup(), VGroup()]   # live register values (kept out of the group)
        self.lanes = VGroup()
        for k in range(2):
            th = make_thread(labels[k], colors[k])
            place_on(th, [thread_pos[k][0], thread_pos[k][1] - 0.4, 0])
            self.threads.add(th)
            box = RoundedRectangle(width=0.9, height=0.7, corner_radius=0.08)
            box.set_fill(CARD_FILL, 1).set_stroke(colors[k], 3)
            side = RIGHT if k == 0 else LEFT
            box.next_to(th, side, buff=0.35).shift(UP * 0.15)
            rl = Text("r", font=MONO_FONT, font_size=20, color=colors[k]).next_to(box, UP, buff=0.06)
            self.regs.add(VGroup(box, rl))
            lane = VGroup()
            for op, y in zip(self.OPS, lane_ys):
                b = RoundedRectangle(width=3.2, height=0.6, corner_radius=0.08)
                b.set_fill(colors[k], 0.12).set_stroke(colors[k], 2.5).move_to([lane_x[k], y, 0])
                t = Text(self.OP_TEXT[op], font=MONO_FONT, font_size=20, color=TEXT).move_to(b)
                lane.add(VGroup(b, t))
            self.lanes.add(lane)
        self.step_n = 0
        self.step_label = Text("step 0", font=MONO_FONT, font_size=22, color=DIM).move_to([0, 0.3, 0])
        self.add(self.cell, self.cell_title, self.cell_value, self.threads, self.regs, self.lanes)

    def _num(self, v, size=30, color=TEXT):
        return Text(str(v), font=MONO_FONT, font_size=size, color=color, weight=BOLD)

    def play_step(self, k, op, run_time=0.8, show_step=True):
        lane_block = self.lanes[k][self.OPS.index(op)]
        self.step_n += 1
        anims = [Indicate(lane_block[0], color=self.colors[k], scale_factor=1.05)]
        if show_step:
            new_lab = Text(f"step {self.step_n}", font=MONO_FONT, font_size=22, color=DIM).move_to(self.step_label)
            anims.append(Transform(self.step_label, new_lab))
        box = self.regs[k][0]
        old_reg = self.reg_texts[k]
        if op == "load":
            fly = self.cell_value.copy()
            self.reg_texts[k] = fly
            self.reg_values[k] = self.value
            anims += [FadeOut(old_reg), fly.animate.move_to(box).scale(0.75).set_color(self.colors[k])]
        elif op == "add":
            v = self.reg_values[k] + 1
            new = self._num(v, 30, self.colors[k]).move_to(box)
            self.reg_texts[k] = new
            self.reg_values[k] = v
            anims += [FadeOut(old_reg, shift=UP * 0.25), FadeIn(new, shift=UP * 0.25)]
        else:  # store
            fly = old_reg.copy()
            oldv = self.cell_value
            self.remove(oldv)
            self.cell_value = fly
            self.value = self.reg_values[k]
            anims += [fly.animate.move_to(self.cell).scale(4 / 3).set_color(TEXT),
                      FadeOut(oldv, scale=0.6)]
        return AnimationGroup(*anims, run_time=run_time)

    def steps(self, seq, run_time=0.8):
        """Generator: yields each step's animation lazily (build each one right before
        playing it: ``for a in demo.steps(seq): self.play(a)``)."""
        for k, op in seq:
            yield self.play_step(k, op, run_time)

    def reset(self, value, run_time=0.5):
        newv = self._num(value, 40).move_to(self.cell)
        oldv = self.cell_value
        self.remove(oldv)
        self.cell_value = newv
        self.value = value
        anims = [FadeOut(oldv), FadeIn(newv)]
        for k in range(2):
            if self.reg_values[k] is not None:
                anims.append(FadeOut(self.reg_texts[k]))
                self.reg_texts[k] = VGroup()
                self.reg_values[k] = None
        self.step_n = 0
        return AnimationGroup(*anims, run_time=run_time)


# ---------------------------------------------------------------------------
# User/Kernel boundary + privilege gauge
# ---------------------------------------------------------------------------
class UserKernelBoundary(VGroup):
    """Dashed line, tinted zones (user above, kernel below) and labels.

    ``UserKernelBoundary(y=-0.3, x_range=(-7.2, 7.2), top=4.1, bottom=-4.1,
    label_x=-6.6, user_opacity=0.08, kernel_opacity=0.10)``.
    Parts: ``line``, ``user_zone``, ``kernel_zone``, ``user_label``, ``kernel_label``.
    ``draw()``: line draws, zones fade in.  ``cross(mob, target, run_time=1)``:
    moves ``mob`` (center) to ``target`` and flashes the line where it crosses.
    ``flash_at(x)``, ``pulse(times=2)``.
    """

    def __init__(self, y=-0.3, x_range=(-7.2, 7.2), top=4.1, bottom=-4.1, label_x=-6.6,
                 user_opacity=0.08, kernel_opacity=0.10, label_size=22, **kwargs):
        super().__init__(**kwargs)
        self.y = y
        x0, x1 = x_range
        self.user_zone = Rectangle(width=x1 - x0, height=top - y).move_to([(x0 + x1) / 2, (top + y) / 2, 0])
        self.user_zone.set_fill(USER_COLOR, user_opacity).set_stroke(width=0)
        self.kernel_zone = Rectangle(width=x1 - x0, height=y - bottom).move_to([(x0 + x1) / 2, (y + bottom) / 2, 0])
        self.kernel_zone.set_fill(KERNEL_COLOR, kernel_opacity).set_stroke(width=0)
        self.line = DashedLine([x0, y, 0], [x1, y, 0], dash_length=0.2).set_stroke(TEXT, 3)
        self.user_label = Text("user mode", font=FONT, font_size=label_size, color=USER_COLOR)
        self.user_label.move_to([label_x, y + 0.3, 0], aligned_edge=LEFT)
        self.kernel_label = Text("kernel mode", font=FONT, font_size=label_size, color=KERNEL_COLOR)
        self.kernel_label.move_to([label_x, y - 0.3, 0], aligned_edge=LEFT)
        self.add(self.user_zone, self.kernel_zone, self.line, self.user_label, self.kernel_label)

    def draw(self, run_time=1.5):
        return Succession(Create(self.line, run_time=run_time * 0.6),
                          AnimationGroup(FadeIn(self.user_zone), FadeIn(self.kernel_zone),
                                         FadeIn(self.user_label), FadeIn(self.kernel_label),
                                         run_time=run_time * 0.4))

    def flash_at(self, x, color=CPU_COLOR):
        return Flash(np.array([x, self.y, 0]), color=color, line_length=0.25, flash_radius=0.25,
                     num_lines=10, run_time=0.5)

    def cross(self, mob, target, run_time=1.0, color=CPU_COLOR):
        start = mob.get_center()
        target = np.array(target, dtype=float)
        dy = target[1] - start[1]
        f = 0.5 if abs(dy) < 1e-6 else float(np.clip((self.y - start[1]) / dy, 0, 1))
        x = start[0] + (target[0] - start[0]) * f
        return AnimationGroup(mob.animate(run_time=run_time, rate_func=linear).move_to(target),
                              Succession(Wait(max(0.01, run_time * f - 0.1)), self.flash_at(x, color)))

    def pulse(self, times=2, run_time=1.2):
        return Succession(*[Indicate(self.line, scale_factor=1.0, color=CPU_COLOR,
                                     run_time=run_time / times) for _ in range(times)])


class PrivilegeGauge(VGroup):
    """Small vertical privilege meter reading USER or KERNEL.

    ``PrivilegeGauge(height=2.0, width=0.45, level="user", title="privilege")``.
    ``set_level("user"|"kernel")`` animation (the fill rises/falls, recolors, and
    the reading flips).  Parts: ``tube``, ``fill``, ``reading``, ``title``.
    """

    def __init__(self, height=2.0, width=0.45, level="user", title="privilege", **kwargs):
        super().__init__(**kwargs)
        self.gh, self.gw = height, width
        self.tube = RoundedRectangle(width=width, height=height, corner_radius=width / 2)
        self.tube.set_fill(CARD_FILL, 1).set_stroke(TEXT, 2.5)
        self.level = level
        self.fill = self._fill_for(level)
        self.reading = self._reading_for(level)
        self.title = Text(title, font=FONT, font_size=18, color=DIM).next_to(self.tube, UP, buff=0.12)
        self.add(self.tube, self.fill, self.reading, self.title)

    def _fill_for(self, level):
        h = self.gh * (0.3 if level == "user" else 0.92)
        col = USER_COLOR if level == "user" else KERNEL_COLOR
        r = RoundedRectangle(width=self.gw * 0.7, height=h, corner_radius=self.gw * 0.3)
        r.set_fill(col, 0.9).set_stroke(width=0)
        r.move_to(self.tube.get_bottom() + UP * (h / 2 + self.gw * 0.15))
        return r

    def _reading_for(self, level):
        col = USER_COLOR if level == "user" else KERNEL_COLOR
        t = Text(level.upper(), font=MONO_FONT, font_size=20, color=col, weight=BOLD)
        return t.next_to(self.tube, DOWN, buff=0.12)

    def set_level(self, level, run_time=0.6):
        self.level = level
        nf, nr = self._fill_for(level), self._reading_for(level)
        return AnimationGroup(Transform(self.fill, nf), Transform(self.reading, nr), run_time=run_time)


# ---------------------------------------------------------------------------
# EraRibbon
# ---------------------------------------------------------------------------
class EraRibbon(VGroup):
    """History ribbon: a line with era ticks and labels, and a sliding marker.

    ``EraRibbon(eras, y=2.6, x_range=(-6, 6), font_size=18, accent=TEXT)``.
    Parts: ``line``, ``ticks``, ``labels``, ``marker`` (triangle above the line).
    ``era_point(i_or_name)``, ``move_marker(i_or_name)`` animation (also highlights
    that label), ``draw()`` animation.  ``current`` = index.
    """

    def __init__(self, eras, y=2.6, x_range=(-6, 6), font_size=18, accent=TEXT, start=0, **kwargs):
        super().__init__(**kwargs)
        self.eras = list(eras)
        self.y = y
        self.accent = accent
        x0, x1 = x_range
        self.line = Line([x0, y, 0], [x1, y, 0]).set_stroke(DIM, 3)
        n = len(self.eras)
        self.xs = np.linspace(x0 + 0.6, x1 - 0.6, n)
        self.ticks = VGroup(*[Dot([x, y, 0], radius=0.07).set_fill(DIM, 1) for x in self.xs])
        self.labels = VGroup(*[Text(e, font=FONT, font_size=font_size, color=DIM).next_to([x, y, 0], DOWN, buff=0.18)
                               for e, x in zip(self.eras, self.xs)])
        self.current = start
        self.marker = Polygon([-0.14, 0.24, 0], [0.14, 0.24, 0], [0, 0, 0]).set_fill(accent, 1).set_stroke(width=0)
        self.marker.move_to(self.era_point(start) + UP * 0.2)
        self.labels[start].set_color(TEXT)
        self.add(self.line, self.ticks, self.labels, self.marker)

    def _idx(self, key):
        return self.eras.index(key) if isinstance(key, str) else key

    def era_point(self, key):
        return np.array([self.xs[self._idx(key)], self.y, 0])

    def move_marker(self, key, run_time=0.8):
        i = self._idx(key)
        old = self.current
        self.current = i
        anims = [self.marker.animate.move_to(self.era_point(i) + UP * 0.2)]
        if old != i:
            anims += [self.labels[old].animate.set_color(DIM), self.labels[i].animate.set_color(TEXT)]
        return AnimationGroup(*anims, run_time=run_time)

    def draw(self, run_time=1.5):
        return Succession(Create(self.line, run_time=run_time * 0.5),
                          AnimationGroup(FadeIn(self.ticks, lag_ratio=0.2), FadeIn(self.labels, lag_ratio=0.2),
                                         FadeIn(self.marker), run_time=run_time * 0.5))
