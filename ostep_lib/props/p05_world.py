"""Process "worlds" and cell division (episode 05).

* ``clone_process(proc, ...)``: the mitosis split of a Process creature.
* ``ProcessWorld(color, pid)``: creature + address space + registers + PCB + open-file plugs.
"""
from __future__ import annotations

import numpy as np
from manim import (
    AnimationGroup, Succession, FadeIn, FadeOut, GrowFromCenter, LaggedStart, ReplacementTransform,
    Transform, Triangle, VGroup, Text, Wait, Indicate, DOWN, LEFT, RIGHT, UP, PI,
)

from ..style import TEXT, DIM, CPU_COLOR, MEM_COLOR, MONO_FONT, PROCESS_COLORS
from ..characters import Process
from .core import Memory, base_point, place_on, make_translucent
from .p04_icons import plug_glyph
from .p04_pcb import PCBCard
from .p04_registers import RegisterBank
from .p05_icons import mem_icon_small

__all__ = ["clone_process", "ProcessWorld"]


def clone_process(proc, to=None, color=None, label=None, spread=0.9, squash_time=0.4, move_time=0.7):
    """Mitosis: ``proc`` squashes, stretches and splits in two.

    Returns ``(clone, animation)``.  **Add ``clone`` to the scene before playing** (it starts
    exactly on top of ``proc``).  ``to``: where the clone's center ends up (``proc`` stays);
    without it the two separate by ``spread`` each way.  ``color`` / ``label`` make the clone a
    differently colored / labeled copy (default: identical)."""
    if color is None and label is None:
        clone = proc.copy()
    else:
        clone = Process(proc.expression, color=color or proc.base_color,
                        label=proc.label_text if label is None else label)
        clone.scale(proc._scale_factor() / clone._scale_factor())
        if proc.is_flipped:
            clone.flip()
        place_on(clone, base_point(proc))
    sq = lambda m: m.animate(run_time=squash_time).stretch(1.3, 0).stretch(0.82, 1)
    step1 = AnimationGroup(sq(proc), sq(clone))
    if to is None:
        mv = [proc.animate(run_time=move_time).shift(LEFT * spread),
              clone.animate(run_time=move_time).shift(RIGHT * spread)]
    else:
        mv = [clone.animate(run_time=move_time).shift(np.array(to, dtype=float) - clone.get_center())]
    return clone, Succession(step1, AnimationGroup(*mv))


class ProcessWorld(VGroup):
    """A process with its "world": creature (top), memory column (code / static data / heap /
    stack), three registers (PC highlighted), a PCB card with the pid, and plugs 0 1 2.

    ``ProcessWorld(color, pid=29146, pcb_pid=None, label=None)``; ``pcb_pid`` is what the PCB
    card shows at first (the child's copy starts with the parent's pid, then ``set_pid`` flips
    it).  The group is about 3.1 wide and 4.4 tall, centered where the memory column is.
    Parts (also lists the pieces for animating one at a time): ``creature, memory, regs, pcb,
    plugs``; ``panels`` = VGroup(memory, regs, pcb, plugs); ``parts()`` = all five.

    Methods
    * ``assemble(run_time)``: animation, panels cascade in, creature grows.
    * ``place(point)``: puts the panels' center at ``point``.
    * ``clone_stages(point, color, new_pid)``: ``(other, peel, cascade)`` (two animations to play in order).
    * ``clone_to(point, color, new_pid)``: ``(other, animation)``; a ghost of the panels peels
      off to ``point``, fills in with ``color`` in a cascade (the new world's parts become scene
      members; add nothing yourself), then the creature grows.  The new PCB still shows the old
      pid: call ``other.set_pid(new_pid)`` next.
    * ``set_pid(pid)``: animation flipping the PCB pid field.
    * ``pc_marker(color)``: a small arrow in the code region (not added); ``code_point()``.
    * ``collapse(creature_point)``: ``(icon, animation)``: panels shrink into a memory icon under
      the creature, which moves to ``creature_point``.
    * ``set_program(color)``: animation recoloring the code and static data regions.
    """

    def __init__(self, color=PROCESS_COLORS[0], pid=29146, pcb_pid=None, label=None, creature_scale=0.7,
                 mem_height=2.6, **kwargs):
        super().__init__(**kwargs)
        self.world_color, self.pid = color, pid
        self.creature = Process("ready", color=color, label=label if label is not None else f"PID {pid}")
        self.creature.scale(creature_scale)
        mem = Memory(regions=["code", "static data", "heap", "stack"], width=1.15, height=mem_height,
                     addresses=False, font_size=14)
        for name in ("code", "static data", "heap", "stack"):
            mem.region(name).set_fill(color, 0.35).set_stroke(color, 3)
        regs = RegisterBank([("PC", "0x400"), ("SP", "0xff8"), ("eax", "42")], cols=1, box_width=1.25,
                            box_height=0.32, font_size=15, buff=0.07)
        regs.boxes["PC"].set_stroke(CPU_COLOR, 3).set_fill(CPU_COLOR, 0.25)
        regs.name_texts["PC"].set_color(CPU_COLOR)
        pcb = PCBCard("PCB", color, [("pid", str(pid if pcb_pid is None else pcb_pid))], width=1.6,
                      height=0.42, cols=1, font_size=16, header_width=0.55, title_font=14)
        plugs = VGroup(*[plug_glyph(str(i), TEXT, 14) for i in range(3)]).arrange(RIGHT, buff=0.1)
        plugs.scale(0.8)
        mem.move_to([-0.85, 0.0, 0.0])
        regs.move_to([0.8, 0.82, 0.0])
        pcb.move_to([0.8, 0.0, 0.0])
        plugs.move_to([0.8, -0.72, 0.0])
        self.creature.move_to([0.0, 2.25, 0.0])
        self.memory, self.regs, self.pcb, self.plugs = mem, regs, pcb, plugs
        self.panels = VGroup(mem, regs, pcb, plugs)
        self.add(self.creature, self.panels)

    # ------------------------------------------------------------------
    def parts(self):
        return [self.creature, self.memory, self.regs, self.pcb, self.plugs]

    def code_point(self):
        return self.memory.region("code").get_center()

    def pc_marker(self, color=None):
        r = self.memory.region("code")
        tri = Triangle().rotate(-PI / 2).scale(0.1).set_fill(color or self.world_color, 1).set_stroke(TEXT, 1.5)
        tri.move_to(r.get_right() + LEFT * 0.14)
        return tri

    def assemble(self, run_time=1.4):
        return AnimationGroup(
            LaggedStart(*[FadeIn(p, shift=UP * 0.15) for p in self.panels], lag_ratio=0.25),
            GrowFromCenter(self.creature), run_time=run_time)

    def set_pid(self, pid, run_time=0.6):
        self.pid = pid
        return self.pcb.set_field("pid", str(pid), run_time=run_time)

    def place(self, point):
        """Move the whole world so that the center of its panels is at ``point``."""
        self.shift(np.array(point, dtype=float) - self.panels.get_center())
        return self

    def clone_stages(self, point, color, new_pid):
        """``(other, peel, cascade)``: ``peel`` = a translucent ghost of the panels leaves the
        original and drifts to ``point``; ``cascade`` = the ghost parts turn into the new world's
        (``color``) parts one by one, then its creature grows.  Play them in order."""
        other = ProcessWorld(color, pid=new_pid, pcb_pid=self.pid, creature_scale=self.creature_scale_())
        other.place(point)
        ghosts = [p.copy() for p in self.panels]
        for g in ghosts:
            make_translucent(g, 0.45, 0.6)
        delta = other.panels.get_center() - self.panels.get_center()
        peel = Succession(AnimationGroup(*[FadeIn(g) for g in ghosts], run_time=0.3),
                          AnimationGroup(*[g.animate.shift(delta) for g in ghosts], run_time=0.9))
        cascade = Succession(
            LaggedStart(*[ReplacementTransform(g, o) for g, o in zip(ghosts, other.panels)],
                        lag_ratio=0.45, run_time=1.6),
            GrowFromCenter(other.creature, run_time=0.5))
        return other, peel, cascade

    def clone_to(self, point, color, new_pid):
        """``(other, animation)``: peel + cascade in one go (see ``clone_stages``)."""
        other, peel, cascade = self.clone_stages(point, color, new_pid)
        return other, Succession(peel, cascade)

    def creature_scale_(self):
        return self.creature._scale_factor() / Process("ready", label="x")._scale_factor()

    def collapse(self, creature_point, icon_dy=-1.05, run_time=1.0):
        icon = mem_icon_small(self.world_color)
        icon.move_to(np.array(creature_point, dtype=float) + DOWN * (0.35 - icon_dy))
        anims = [p.animate.scale(0.15).move_to(icon.get_center()).set_opacity(0) for p in self.panels]
        anims.append(self.creature.animate.move_to(np.array(creature_point, dtype=float)))
        anims.append(FadeIn(icon))
        return icon, AnimationGroup(*anims, run_time=run_time)

    def set_program(self, color, run_time=0.8):
        a = []
        for n in ("code", "static data"):
            a.append(self.memory.region(n).animate.set_fill(color, 0.5).set_stroke(color, 3))
        return AnimationGroup(*a, run_time=run_time)
