"""Props for episode 06 (limited direct execution): the OS token, register packets,
kernel stacks, the trap table, the CPU "ride" across the User/Kernel boundary.

* ``KernelToken``  the red "OS" badge that stands on the CPU chip (the OS running).
* ``RegPacket``    three tiny cells in the owner's color = a process's saved registers.
* ``PacketFly``    animation: move (along an arc), scale and optionally fade a mobject.
* ``KernelStack``  narrow tray ``k-stack(A)`` that register packets are pushed onto.
* ``TrapTable``    card with rows ``syscall -> handler`` that fill in one by one.
* ``cpu_ride``     the signature motion: the chip slides across the boundary; the line
                   flashes and the privilege gauge flips at the crossing.
"""
from __future__ import annotations

import numpy as np
from manim import (
    Animation, AnimationGroup, Arrow, Create, FadeIn, FadeOut, Line, Rectangle, RoundedRectangle,
    Square, Succession, Text, VGroup, VMobject, Wait, Write, smooth, linear, WHITE,
    LEFT, RIGHT, UP, DOWN, ORIGIN, BOLD, UL, UR,
)

from ..characters.base import mix
from ..style import (TEXT, DIM, BG, FONT, MONO_FONT, KERNEL_COLOR, CPU_COLOR, MEM_COLOR)
from .core import CARD_FILL, INK, outline_of, base_point
from .ov_icons import padlock_icon, OK_GREEN

__all__ = ["KernelToken", "RegPacket", "PacketFly", "ShiftBy", "KernelStack", "TrapTable", "cpu_ride"]


def _P(x, y=0.0):
    return np.array([float(x), float(y), 0.0])


class PacketFly(Animation):
    """Move ``mob`` (its center) to ``end`` along an arc, scaling it by ``end_scale`` and
    optionally fading it out.  ``arc`` is the height of the bump (0 = straight)."""

    def __init__(self, mob, end, arc=0.4, end_scale=1.0, fade=False, **kwargs):
        kwargs.setdefault("run_time", 0.8)
        kwargs.setdefault("rate_func", smooth)
        self.end = np.array(end, dtype=float)
        self.arc = arc
        self.end_scale = end_scale
        self.fade = fade
        super().__init__(mob, **kwargs)

    def begin(self):
        self._fam = [sm for sm in self.mobject.get_family() if isinstance(sm, VMobject) and len(sm.points)]
        self._pts = [sm.points.copy() for sm in self._fam]
        self._fo = [sm.get_fill_opacity() for sm in self._fam]
        self._so = [sm.get_stroke_opacity() for sm in self._fam]
        self._c0 = self.mobject.get_center().copy()
        super().begin()

    def interpolate_mobject(self, alpha):
        a = self.rate_func(alpha)
        c = self._c0 + (self.end - self._c0) * a + UP * self.arc * 4 * a * (1 - a)
        s = 1 + (self.end_scale - 1) * a
        for sm, p, fo, so in zip(self._fam, self._pts, self._fo, self._so):
            sm.points = (p - self._c0) * s + c
            if self.fade:
                sm.set_fill(opacity=fo * (1 - a), family=False)
                sm.set_stroke(opacity=so * (1 - a), family=False)


class ShiftBy(Animation):
    """Shift ``mob`` by ``delta`` relative to where it is when the animation *begins*
    (unlike ``.animate.shift``, safe inside a Succession after other moves)."""

    def __init__(self, mob, delta, **kwargs):
        kwargs.setdefault("run_time", 0.8)
        kwargs.setdefault("rate_func", smooth)
        self.delta = np.array(delta, dtype=float)
        super().__init__(mob, **kwargs)

    def begin(self):
        self._fam = [sm for sm in self.mobject.get_family() if len(sm.points)]
        self._pts = [sm.points.copy() for sm in self._fam]
        super().begin()

    def interpolate_mobject(self, alpha):
        a = self.rate_func(alpha)
        for sm, p in zip(self._fam, self._pts):
            sm.points = p + self.delta * a


class KernelToken(VGroup):
    """The OS "running": a red rounded badge with a white "OS", 0.9 x 0.55.

    ``KernelToken(label="OS", scale=1.0)``.  Parts: ``badge``, ``text``, ``arm``.
    ``place(cpu)`` stands it on a chip instantly; ``hop_onto(cpu)`` animation;
    ``dim_to(o=0.3)`` / ``wake()``; ``reach(point)`` shoots the arm out and ``retract()``
    pulls it back.  Keep the arm retracted while hopping the token.
    """

    def __init__(self, label="OS", scale=1.0, **kwargs):
        super().__init__(**kwargs)
        self.badge = RoundedRectangle(width=0.9, height=0.55, corner_radius=0.14)
        self.badge.set_fill(KERNEL_COLOR, 1).set_stroke(outline_of(KERNEL_COLOR), 3)
        self.text = Text(label, font=FONT, font_size=28, color=WHITE, weight=BOLD).move_to(self.badge)
        self.arm = Line(ORIGIN, ORIGIN + RIGHT * 0.01).set_stroke(KERNEL_COLOR, 7, opacity=0)
        self.arm.move_to(self.badge.get_center())
        self.add(self.arm, self.badge, self.text)
        if scale != 1.0:
            self.scale(scale)

    def place(self, cpu, dy=0.02):
        self.shift(cpu.slot_point() + UP * dy - self.badge.get_bottom())
        return self

    def hop_onto(self, cpu, run_time=0.5, dy=0.02):
        from .core import hop_to
        return hop_to(self, cpu.slot_point() + UP * dy, run_time=run_time)

    def dim_to(self, opacity=0.3, run_time=0.5):
        return AnimationGroup(self.badge.animate.set_fill(opacity=opacity).set_stroke(opacity=opacity),
                              self.text.animate.set_opacity(opacity), run_time=run_time)

    def wake(self, run_time=0.5):
        return self.dim_to(1.0, run_time)

    def reach(self, point, run_time=0.6):
        c = self.badge.get_center()
        tgt = Line(c, np.array(point, dtype=float)).set_stroke(KERNEL_COLOR, 7, opacity=1)
        return _Retarget(self.arm, tgt, run_time=run_time)

    def retract(self, run_time=0.4):
        c = self.badge.get_center()
        tgt = Line(c, c + RIGHT * 0.01).set_stroke(KERNEL_COLOR, 7, opacity=0)
        return _Retarget(self.arm, tgt, run_time=run_time)


class _Retarget(Animation):
    """Transform wrapper that tolerates degenerate lines (straight interpolation of points)."""

    def __init__(self, mob, target, **kwargs):
        kwargs.setdefault("run_time", 0.6)
        self.target = target
        super().__init__(mob, **kwargs)

    def begin(self):
        self._p0 = self.mobject.points.copy()
        self._o0 = self.mobject.get_stroke_opacity()
        super().begin()

    def interpolate_mobject(self, alpha):
        a = self.rate_func(alpha)
        n = min(len(self._p0), len(self.target.points))
        self.mobject.points = self._p0[:n] * (1 - a) + self.target.points[:n] * a
        self.mobject.set_stroke(opacity=self._o0 * (1 - a) + self.target.get_stroke_opacity() * a)


class RegPacket(VGroup):
    """A process's registers in transit: ``n`` tiny cells in a row filled with the owner's
    color (kernel registers = ``KERNEL_COLOR``).

    ``RegPacket(color, labels=None, cell=0.18, n=3)``.  ``labels`` (e.g. ``["PC", "flags", "..."]``)
    adds tiny captions under the cells.  ``fly_to(point)`` / ``fly_into(mob)`` return animations.
    """

    def __init__(self, color, labels=None, cell=0.18, n=3, **kwargs):
        super().__init__(**kwargs)
        self.color = color
        cw = 0.38 if labels else cell
        self.cells = VGroup(*[Rectangle(width=cw, height=cell).set_fill(color, 1).set_stroke(outline_of(color), 2)
                              for _ in range(n)]).arrange(RIGHT, buff=0.03)
        self.add(self.cells)
        self.labels = VGroup()
        if labels:
            for c, l in zip(self.cells, labels):
                t = Text(l, font=MONO_FONT, font_size=13, color=TEXT)
                t.next_to(c, DOWN, buff=0.04)
                self.labels.add(t)
            self.add(self.labels)

    def fly_to(self, point, run_time=0.8, arc=0.4, end_scale=1.0):
        return PacketFly(self, point, arc=arc, end_scale=end_scale, run_time=run_time)

    def fly_into(self, mob, run_time=0.8, arc=0.4, end_scale=0.4, vanish=False):
        """Fly to the center of ``mob``, shrinking; with ``vanish`` it fades on arrival."""
        return PacketFly(self, mob.get_center(), arc=arc, end_scale=end_scale, fade=vanish, run_time=run_time)


class KernelStack(VGroup):
    """The per-process kernel stack tray (1.6 x 1.4) with a label such as ``k-stack(A)``.

    ``KernelStack(label, color=MEM_COLOR, width=1.6, height=1.4, slots=3)``.
    Parts: ``frame``, ``label``.  ``slot_point(k)`` (k = 0 at the bottom).
    ``push(packet)`` / ``pop(to=None)`` return animations (packets live in ``items``;
    add them to the scene yourself).  ``glow()`` / ``dim_down()`` / ``plain()`` emphasis.
    """

    def __init__(self, label="k-stack(A)", color=MEM_COLOR, width=1.6, height=1.4, slots=3, **kwargs):
        super().__init__(**kwargs)
        self.color, self.w, self.h, self.n_slots = color, width, height, slots
        self.frame = Rectangle(width=width, height=height).set_fill(mix(color, BG, 0.86), 1).set_stroke(color, 3)
        self.label = Text(label, font=MONO_FONT, font_size=18, color=color).next_to(self.frame, UP, buff=0.08)
        self.add(self.frame, self.label)
        self.items = []
        self.slot_h = (height - 0.2) / slots

    def slot_point(self, k):
        return self.frame.get_bottom() + UP * (0.1 + self.slot_h * (k + 0.5))

    def push(self, packet, run_time=0.8, end_scale=1.3):
        k = len(self.items)
        self.items.append(packet)
        return PacketFly(packet, self.slot_point(k), arc=0.3, end_scale=end_scale, run_time=run_time)

    def pop(self, to=None, run_time=0.8, end_scale=1 / 1.3, fade=False):
        p = self.items.pop()
        dest = self.frame.get_top() + UP * 1.2 if to is None else to
        return PacketFly(p, dest, arc=0.3, end_scale=end_scale, fade=fade, run_time=run_time)

    def glow(self, run_time=0.4):
        return AnimationGroup(self.frame.animate.set_stroke(CPU_COLOR, 5).set_fill(CPU_COLOR, 0.18),
                              self.label.animate.set_color(CPU_COLOR), run_time=run_time)

    def plain(self, run_time=0.4):
        return AnimationGroup(self.frame.animate.set_stroke(self.color, 3, opacity=1).set_fill(mix(self.color, BG, 0.86), 1),
                              self.label.animate.set_color(self.color).set_opacity(1), run_time=run_time)

    def dim_down(self, run_time=0.4, opacity=0.35):
        return AnimationGroup(self.frame.animate.set_stroke(opacity=opacity).set_fill(opacity=opacity),
                              self.label.animate.set_opacity(opacity), run_time=run_time)


class TrapTable(VGroup):
    """The trap table card: ``KERNEL_COLOR`` frame, header "TRAP TABLE", rows
    ``key -> handler`` that appear one by one.

    ``TrapTable(rows=("syscall", "timer", "keyboard"), width=3.6, height=1.9, filled=0, dim_rows=())``.
    Rows are built hidden: ``add_row(i, dim=False)`` returns the animation that shows
    row ``i`` (call it right before playing).  ``filled`` rows start visible.
    ``highlight_row(i)`` / ``unhighlight()`` animations; ``row_point(i)`` (right end of
    the row, where an arrow to a handler can start); ``lock()`` closes a padlock on the card.
    """

    def __init__(self, rows=("syscall", "timer", "keyboard"), width=3.6, height=1.9, filled=0,
                 dim_rows=(), **kwargs):
        super().__init__(**kwargs)
        self.keys = list(rows)
        self.w, self.h = width, height
        self.frame = RoundedRectangle(width=width, height=height, corner_radius=0.15)
        self.frame.set_fill(CARD_FILL, 1).set_stroke(KERNEL_COLOR, 4)
        self.header = Text("TRAP TABLE", font=FONT, font_size=22, color=KERNEL_COLOR, weight=BOLD)
        self.header.move_to(self.frame.get_top() + DOWN * 0.3)
        self.rule = Line(self.frame.get_corner(UL) + _P(0.2, -0.55), self.frame.get_corner(UR) + _P(-0.2, -0.55))
        self.rule.set_stroke(KERNEL_COLOR, 1.5, opacity=0.7)
        self.add(self.frame, self.header, self.rule)
        n = len(rows)
        self.row_h = (height - 0.7) / max(n, 3)
        self.dim_rows = set(dim_rows)
        self.row_mobs = [None] * n
        self.hl = None
        self.padlock = None
        for i in range(filled):
            self.add(self._row(i))

    def _row(self, i):
        """Build (once) row ``i`` at the card's *current* position."""
        if self.row_mobs[i] is not None:
            return self.row_mobs[i]
        k = self.keys[i]
        y = self.frame.get_top()[1] - 0.55 - self.row_h * (i + 0.5)
        cx, lx, rx = self.frame.get_center()[0], self.frame.get_left()[0], self.frame.get_right()[0]
        col = DIM if i in self.dim_rows else TEXT
        kt = Text(k, font=MONO_FONT, font_size=20, color=col)
        kt.move_to(_P(lx + 0.3, y), aligned_edge=LEFT)
        ar = Arrow(_P(cx - 0.28, y), _P(cx + 0.36, y), buff=0, stroke_width=3, tip_length=0.13,
                   max_tip_length_to_length_ratio=0.5, color=col)
        ht = Text("handler", font=MONO_FONT, font_size=20, color=col)
        ht.move_to(_P(rx - 0.3, y), aligned_edge=RIGHT)
        self.row_mobs[i] = VGroup(kt, ar, ht)
        return self.row_mobs[i]

    def add_row(self, i, run_time=0.5):
        row = self._row(i)
        self.add(row)
        return FadeIn(row, shift=RIGHT * 0.2, run_time=run_time)

    def row(self, i):
        return self._row(i)

    def row_point(self, i):
        r = self._row(i)
        return r[2].get_right() + RIGHT * 0.08

    def highlight_row(self, i, color=CPU_COLOR, run_time=0.4):
        r = self._row(i)
        rect = Rectangle(width=self.w - 0.3, height=self.row_h).set_fill(color, 0.25).set_stroke(color, 2)
        rect.move_to(r.get_center())
        rect.set_x(self.frame.get_center()[0])
        if self.hl is not None:
            old = self.hl
            self.hl = rect
            self.add(rect)
            return AnimationGroup(FadeOut(old), FadeIn(rect), run_time=run_time)
        self.hl = rect
        self.add(rect)
        return FadeIn(rect, run_time=run_time)

    def unhighlight(self, run_time=0.3):
        h, self.hl = self.hl, None
        return FadeOut(h, run_time=run_time) if h is not None else Wait(0.01)

    def lock(self, run_time=0.5):
        self.padlock = padlock_icon(0.4, KERNEL_COLOR).move_to(self.frame.get_corner(UR) + _P(-0.05, 0.05))
        self.add(self.padlock)
        return FadeIn(self.padlock, scale=1.6, run_time=run_time)


def cpu_ride(chip, target, boundary, gauge=None, riders=(), run_time=0.8, color=CPU_COLOR):
    """The chip slides to ``target`` (a point for its center), carrying ``riders``.

    The boundary flashes where the chip crosses it and ``gauge`` flips to the new level
    (kernel when the target is below the line) at the midpoint.  Returns one animation.
    """
    target = np.array(target, dtype=float)
    start = chip.get_center()
    shift = target - start
    y = boundary.y
    dy = target[1] - start[1]
    f = 0.5 if abs(dy) < 1e-6 else float(np.clip((y - start[1]) / dy, 0.05, 0.95))
    level = "kernel" if target[1] < y else "user"
    anims = [ShiftBy(m, shift, run_time=run_time) for m in (chip, *riders)]
    anims.append(Succession(Wait(max(0.01, run_time * f - 0.05)), boundary.flash_at(start[0], color)))
    if gauge is not None and gauge.level != level:
        anims.append(Succession(Wait(run_time * 0.5), gauge.set_level(level, run_time=0.5)))
    return AnimationGroup(*anims)
