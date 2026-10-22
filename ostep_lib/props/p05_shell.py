"""Shell-related props (episode 05): FdTable, ShellLoop, KernelPipe, MenuCardRows."""
from __future__ import annotations

import numpy as np
from manim import (
    AnimationGroup, Arrow, Create, CubicBezier, DashedVMobject, FadeIn, FadeOut, Flash, Line, RoundedRectangle,
    Succession, Text, VGroup, VMobject, Wait, Rectangle, Triangle, DashedLine, ArcBetweenPoints, Transform,
    DOWN, LEFT, RIGHT, UP, PI, linear,
)

from ..style import (
    BG, TEXT, DIM, CPU_COLOR, KERNEL_COLOR, USER_COLOR, DISK_COLOR, MONO_FONT, VIRT, PROCESS_COLORS,
)
from .core import CARD_FILL, GearPair
from .ov_icons import desktop_icon, tick_mark, x_mark
from .p04_icons import MenuCard, plug_glyph, keyboard_icon
from .p05_icons import wrench_glyph, program_chip

__all__ = ["FdTable", "ShellLoop", "KernelPipe", "MenuCardRows"]


def _P(x, y=0.0):
    return np.array([float(x), float(y), 0.0])


# ---------------------------------------------------------------------------
# FdTable
# ---------------------------------------------------------------------------
class FdTable(VGroup):
    """Three file-descriptor plugs (0 stdin, 1 stdout, 2 stderr) hanging from a panel, each with
    a cable to a device (keyboard, screen, screen).  The creature stands on ``panel``.

    ``FdTable(center=(0, -0.2), spacing=1.3)``.  Parts: ``panel``, ``sockets`` (dashed outlines),
    ``plugs``, ``names``, ``cables``, ``devices``.  Everything is in the group.

    * ``slot_point(i)``: the plug position.
    * ``cut(i)``: spark, cable gone, plug pops out (the dashed socket remains).
    * ``scan_free(taken=(0,), free=1)``: ``(animation, marks)``: a pointer ticks the slots with
      x / tick marks (``marks`` stay in the scene: fade them yourself).
    * ``plug_into(i, device, below=0.85)``: ``(animation, plug, cable)``: ``device`` flies to just
      below slot ``i``, a new plug fills the socket and a cable joins them.
    """

    SLOT_COLORS = (USER_COLOR, CPU_COLOR, KERNEL_COLOR)

    def __init__(self, center=(0.0, -0.2), spacing=1.3, **kwargs):
        super().__init__(**kwargs)
        cx, cy = center[0], center[1]
        self.spacing = spacing
        self.slots = [_P(cx + (i - 1) * spacing, cy) for i in range(3)]
        self.panel = RoundedRectangle(width=3 * spacing + 0.5, height=0.26, corner_radius=0.1)
        self.panel.set_fill(CARD_FILL, 1).set_stroke(DIM, 2.5).move_to(_P(cx, cy + 0.72))
        self.sockets, self.plugs, self.names, self.cables = VGroup(), VGroup(), VGroup(), VGroup()
        labels = ("stdin", "stdout", "stderr")
        for i, s in enumerate(self.slots):
            sock = DashedVMobject(RoundedRectangle(width=0.62, height=0.4, corner_radius=0.07), num_dashes=16)
            sock.set_stroke(DIM, 2).move_to(s)
            plug = plug_glyph(str(i), self.SLOT_COLORS[i], 16).move_to(s)
            name = Text(labels[i], font=MONO_FONT, font_size=14, color=DIM).move_to(s + UP * 0.38)
            self.sockets.add(sock)
            self.plugs.add(plug)
            self.names.add(name)
        dev_pos = [_P(cx - spacing - 1.5, cy - 1.45), _P(cx, cy - 1.6), _P(cx + spacing + 0.6, cy - 1.6)]
        self.devices = VGroup(keyboard_icon(0.9), desktop_icon(0.95), desktop_icon(0.95))
        for d, p in zip(self.devices, dev_pos):
            d.move_to(p)
        for i, (s, d) in enumerate(zip(self.slots, self.devices)):
            self.cables.add(self._cable(i, s, d))
        self.add(self.panel, self.sockets, self.cables, self.plugs, self.names, self.devices)

    def _cable(self, i, slot, dev):
        start = slot + DOWN * 0.18
        end = dev.get_top() + UP * 0.02
        c = CubicBezier(start, start + DOWN * 0.5, end + UP * 0.5, end)
        return c.set_stroke(self.SLOT_COLORS[i], 4)

    def slot_point(self, i):
        return self.slots[i].copy()

    def cut(self, i, run_time=0.9):
        mid = self.cables[i].point_from_proportion(0.5)
        return AnimationGroup(
            Flash(mid, color=CPU_COLOR, line_length=0.2, flash_radius=0.2, num_lines=8, run_time=0.5),
            FadeOut(self.cables[i]),
            FadeOut(self.plugs[i], shift=UP * 0.5),
            run_time=run_time)

    def scan_free(self, taken=(0,), free=1, step=0.7):
        ptr = Triangle().rotate(PI).scale(0.12).set_fill(CPU_COLOR, 1).set_stroke(width=0)
        ptr.move_to(self.slots[0] + UP * 0.62)
        marks = VGroup()
        steps = [FadeIn(ptr, run_time=0.2)]
        for i in list(taken) + [free]:
            m = (x_mark(0.22) if i in taken else tick_mark(0.22)).move_to(self.slots[i] + RIGHT * 0.52)
            marks.add(m)
            steps.append(ptr.animate(run_time=0.3).move_to(self.slots[i] + UP * 0.62))
            steps.append(FadeIn(m, run_time=step * 0.5))
        steps.append(FadeOut(ptr, run_time=0.2))
        return Succession(*steps), marks

    def plug_into(self, i, device, below=0.85, color=None):
        s = self.slots[i]
        color = color or self.SLOT_COLORS[i]
        target = s + DOWN * below
        plug = plug_glyph(str(i), color, 16).move_to(s)
        cable = Line(s + DOWN * 0.18, target + UP * 0.28).set_stroke(color, 4)
        anim = Succession(
            device.animate(run_time=0.9).move_to(target),
            AnimationGroup(FadeIn(plug, shift=DOWN * 0.3), Create(cable), run_time=0.5))
        return anim, plug, cable


# ---------------------------------------------------------------------------
# ShellLoop
# ---------------------------------------------------------------------------
class ShellLoop(VGroup):
    """The shell's loop: prompt -> fork -> (child: exec | parent: wait) -> prompt.

    ``ShellLoop(cx=3.4)``.  Node names: ``"prompt", "fork", "exec", "wait"``.  Parts: ``nodes``
    (dict of VGroup box+text), ``arrows`` (dict: ``p_f, f_e, f_w, e_p, w_p``), ``edge_x``.
    Nodes start dim; the group holds nodes and arrows (arrows are drawn with ``draw_arrow``).

    * ``node_point(name)``, ``stand_point(name)`` (a spot to the left for a creature's feet).
    * ``light(name, color)`` / ``unlight(name)``: node glow animations.
    * ``draw_arrow(key)``: ``Create``.
    * ``highlight_gap()``: ``(animation, label)``: the fork->exec arrow turns yellow with a
      "still shell code" label (add the label via the animation).
    * ``workshop()``: ``(group, animation)``: dashed box around the gap with gears and a wrench.
    """

    def __init__(self, cx=3.4, ys=(2.4, 1.2, -0.3), dx=1.3, **kwargs):
        super().__init__(**kwargs)
        self.cx = cx
        self.edge_x = cx + 2.5
        names = {"prompt": ("prompt", (cx, ys[0])), "fork": ("fork()", (cx, ys[1])),
                 "exec": ("child: exec", (cx - dx, ys[2])), "wait": ("parent: wait", (cx + dx, ys[2]))}
        self.nodes = {}
        for key, (text, (x, y)) in names.items():
            t = Text(text, font=MONO_FONT, font_size=18, color=TEXT)
            box = RoundedRectangle(width=max(1.3, t.width + 0.3), height=0.55, corner_radius=0.12)
            box.set_fill(CARD_FILL, 1).set_stroke(DIM, 2.5).move_to(_P(x, y))
            t.move_to(box)
            g = VGroup(box, t)
            g.box = box
            self.nodes[key] = g
        N = self.nodes
        a_pf = Arrow(N["prompt"].box.get_bottom(), N["fork"].box.get_top(), buff=0.05, stroke_width=4, color=DIM)
        a_fe = ArcBetweenPoints(N["fork"].box.get_bottom() + LEFT * 0.35, N["exec"].box.get_top(), angle=PI / 3)
        a_fe.add_tip(tip_length=0.18).set_stroke(DIM, 4)
        a_fw = ArcBetweenPoints(N["fork"].box.get_bottom() + RIGHT * 0.35, N["wait"].box.get_top(), angle=-PI / 3)
        a_fw.add_tip(tip_length=0.18).set_stroke(DIM, 4)
        pr = N["prompt"].box.get_right()
        yb_c, yb_w = ys[2] - 0.85, ys[2] - 0.62
        ex_b, wa_b = N["exec"].box.get_bottom(), N["wait"].box.get_bottom()
        e_p = VGroup(Line(ex_b, _P(ex_b[0], yb_c)), Line(_P(ex_b[0], yb_c), _P(self.edge_x, yb_c)),
                     Line(_P(self.edge_x, yb_c), _P(self.edge_x, pr[1])),
                     Arrow(_P(self.edge_x, pr[1]), pr, buff=0.05, stroke_width=4, color=DIM))
        w_p = VGroup(Line(wa_b, _P(wa_b[0], yb_w)), Line(_P(wa_b[0], yb_w), _P(self.edge_x, yb_w)))
        for m in list(e_p[:3]) + list(w_p):
            m.set_stroke(DIM, 4)
        e_p[3].set_stroke(DIM, 4)
        self.arrows = {"p_f": a_pf, "f_e": a_fe, "f_w": a_fw, "e_p": e_p, "w_p": w_p}
        self.add(*self.nodes.values(), *self.arrows.values())
        self.gap_label = None

    def node_point(self, name):
        return self.nodes[name].box.get_center()

    def stand_point(self, name, dx=0.55):
        """Where a creature's feet go to stand just left of a node."""
        b = self.nodes[name].box
        return b.get_left() + LEFT * dx + DOWN * 0.28

    def light(self, name, color=CPU_COLOR, run_time=0.4):
        b = self.nodes[name].box
        return b.animate(run_time=run_time).set_fill(color, 0.3).set_stroke(color, 3.5)

    def unlight(self, name, run_time=0.4):
        b = self.nodes[name].box
        return b.animate(run_time=run_time).set_fill(CARD_FILL, 1).set_stroke(DIM, 2.5)

    def draw_arrow(self, key, run_time=0.5):
        return Create(self.arrows[key], run_time=run_time)

    def highlight_gap(self, run_time=0.8):
        a = self.arrows["f_e"]
        mid = a.point_from_proportion(0.5)
        lab = Text("still shell\ncode", font_size=18, color=CPU_COLOR, line_spacing=0.8)
        lab.move_to(_P(self.cx + 0.4, mid[1] - 0.1))
        self.gap_label = lab
        tip = a.tip
        return AnimationGroup(a.animate.set_stroke(CPU_COLOR, 6, family=False), tip.animate.set_fill(CPU_COLOR).set_stroke(CPU_COLOR),
                              FadeIn(lab), run_time=run_time), lab

    def workshop(self, run_time=1.0):
        a = self.arrows["f_e"]
        c = a.get_center()
        box = DashedVMobject(RoundedRectangle(width=1.95, height=1.05, corner_radius=0.15), num_dashes=40)
        box.set_stroke(CPU_COLOR, 3).move_to(c + LEFT * 0.35)
        gears = GearPair(0.2).move_to(box.get_left() + RIGHT * 0.5)
        wr = wrench_glyph(0.3, DIM).move_to(box.get_left() + RIGHT * 0.5 + DOWN * 0.35)
        grp = VGroup(box, gears, wr)
        return grp, AnimationGroup(Create(box), FadeIn(gears), FadeIn(wr), run_time=run_time)


# ---------------------------------------------------------------------------
# KernelPipe
# ---------------------------------------------------------------------------
class KernelPipe(VGroup):
    """A tube with queue slots inside a thin red kernel band labeled "kernel".

    ``KernelPipe(center=(0, 1), width=3.2, slots=5)``.  Parts: ``band``, ``band_label``, ``tube``,
    ``dividers``.  ``left_end()`` / ``right_end()``; ``send(text, color, run_time)`` returns an
    animation of a token traveling from one end to the other (it fades at the end unless
    ``keep=True``); ``band_group()`` = band + label (to fade it in separately).
    """

    def __init__(self, center=(0.0, 1.0), width=3.2, slots=5, **kwargs):
        super().__init__(**kwargs)
        cx, cy = center
        self.w, self.slots = width, slots
        self.band = RoundedRectangle(width=width + 1.0, height=1.5, corner_radius=0.2)
        self.band.set_fill(KERNEL_COLOR, 0.1).set_stroke(KERNEL_COLOR, 2.5).move_to(_P(cx, cy))
        self.band_label = Text("kernel", font_size=20, color=KERNEL_COLOR).move_to(self.band.get_top() + DOWN * 0.2)
        self.tube = RoundedRectangle(width=width, height=0.6, corner_radius=0.3)
        self.tube.set_fill(CARD_FILL, 1).set_stroke(DIM, 3).move_to(_P(cx, cy - 0.15))
        xs = np.linspace(-width / 2 + 0.3, width / 2 - 0.3, slots + 1)
        self.dividers = VGroup(*[Line(_P(cx + x, cy - 0.15 - 0.2), _P(cx + x, cy - 0.15 + 0.2)).set_stroke(DIM, 1.5)
                                 for x in xs[1:-1]])
        self.add(self.band, self.band_label, self.tube, self.dividers)

    def left_end(self):
        return self.tube.get_left()

    def right_end(self):
        return self.tube.get_right()

    def band_group(self):
        return VGroup(self.band, self.band_label)

    def send(self, text="foo", color=TEXT, run_time=1.4, keep=False):
        tok = program_chip(text, color, 16)
        tok.scale(0.8).move_to(self.left_end() + RIGHT * 0.3)
        steps = [FadeIn(tok, run_time=0.15),
                 tok.animate(run_time=run_time, rate_func=linear).move_to(self.right_end() + LEFT * 0.3)]
        if not keep:
            steps.append(FadeOut(tok, run_time=0.15))
        return Succession(*steps)


# ---------------------------------------------------------------------------
# MenuCardRows
# ---------------------------------------------------------------------------
class MenuCardRows(MenuCard):
    """``MenuCard`` with per-row helpers for the UNIX-call callback (05 S16).

    * ``row_y(i)``; ``highlight_row(i, color)`` = ``row_highlight``.
    * ``chip_for(i, text, x=None, color=DIM)``: a mono chip at the row's height, right of the
      card (or centered at ``x``); returns the chip (not added).
    * ``bracket(i, j)``: a bracket rectangle spanning rows ``i..j`` on the right edge.
    """

    def row_y(self, i):
        return self.rows[i].get_y()

    def highlight_row(self, i, color=VIRT):
        return self.row_highlight(i, color)

    def chip_for(self, i, text, x=None, color=DIM, font_size=20):
        chip = program_chip(text, color, font_size)
        if x is None:
            chip.move_to(_P(self.card.get_right()[0] + 0.3 + chip.width / 2, self.row_y(i)))
        else:
            chip.move_to(_P(x, self.row_y(i)))
        return chip

    def bracket(self, i, j, color=VIRT, dx=0.2):
        y0, y1 = self.row_y(i), self.row_y(j)
        x = self.card.get_right()[0] + dx
        pts = [_P(x - 0.1, y0 + 0.15), _P(x, y0 + 0.15), _P(x, y1 - 0.15), _P(x - 0.1, y1 - 0.15)]
        return VMobject().set_points_as_corners(pts).set_stroke(color, 4)
