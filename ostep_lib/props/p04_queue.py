"""Queue: processes standing in a row on a tray, with a label underneath.

The tray and label are the mobject; the processes are *tracked* in
``queue.items`` but are not submobjects (they hop in and out, and keep their
own place in the scene).

    q = Queue(label="Ready", center=(0, -1.2), slots=3)
    q.place(a, b, c)                       # instant
    self.play(q.push(d))                   # d walks to the next slot
    p, anim = q.pop(0)                     # first item leaves; others shuffle
    self.play(anim, hop_to(p, cpu.slot_point()))

``mover(mob, point)`` (default: a straight ``animate.move_to``) lets scenes pass
a hop animation such as the core ``hop_to``.  Points passed to the mover are the
*bottom-center* of the target slot; the default mover aligns the mobject's
bottom to it.
"""
from __future__ import annotations

import numpy as np
from manim import (
    AnimationGroup, Animation, Line, RoundedRectangle, Text, VGroup, DOWN, UP, LEFT, RIGHT,
)

from ..style import TEXT, DIM


def _P(x, y=0.0):
    return np.array([float(x), float(y), 0.0])


def default_mover(mob, bottom_point, run_time=0.5):
    target = np.array(bottom_point) + (mob.get_center() - mob.get_bottom())
    return mob.animate(run_time=run_time).move_to(target)


class Queue(VGroup):
    """A tray with ``slots`` places and a label.

    Parameters: ``label`` (str or None), ``center`` (tray center), ``slots``
    (number of places, sets the tray width), ``spacing`` (distance between
    places), ``color``, ``font_size``, ``mover``.
    """

    def __init__(self, label="Ready", center=(0, 0, 0), slots=3, spacing=1.1, color=DIM,
                 font_size=24, mover=None, label_color=None, **kwargs):
        super().__init__(**kwargs)
        self.spacing = spacing
        self.n_slots = slots
        self.mover = mover or default_mover
        c = np.array(list(center) + [0] * (3 - len(center)), dtype=float)
        w = slots * spacing + 0.2
        self.tray = RoundedRectangle(width=w, height=0.12, corner_radius=0.06).move_to(c)
        self.tray.set_fill(color, 0.5).set_stroke(color, 2)
        self.add(self.tray)
        if label:
            self.label = Text(label, font_size=font_size, color=label_color or DIM)
            self.label.next_to(self.tray, DOWN, buff=0.12)
            self.add(self.label)
        else:
            self.label = None
        self.items = []

    # ------------------------------------------------------------ geometry
    def slot_point(self, i, n=None):
        """Bottom-center point of slot ``i`` (items are left-aligned from the
        front of the queue at the left end)."""
        n = self.n_slots if n is None else n
        left = self.tray.get_left()[0] + 0.1 + self.spacing / 2
        return _P(left + i * self.spacing, self.tray.get_top()[1] + 0.04)

    def front_point(self):
        return self.slot_point(0)

    # ------------------------------------------------------------- actions
    def _snap(self, mob, i):
        p = self.slot_point(i)
        mob.move_to(p + (mob.get_center() - mob.get_bottom()))

    def place(self, *mobs):
        """Instantly put mobjects into the next free slots."""
        for m in mobs:
            self._snap(m, len(self.items))
            self.items.append(m)
        return self

    def push(self, mob, mover=None, **kw):
        """Animation: ``mob`` moves to the back of the queue."""
        i = len(self.items)
        self.items.append(mob)
        return (mover or self.mover)(mob, self.slot_point(i), **kw)

    def pop(self, index=0, mover=None, **kw):
        """Remove item ``index``; returns (mob, animation re-packing the rest)."""
        mob = self.items.pop(index)
        return mob, self.pack(mover=mover, **kw)

    def remove_item(self, mob):
        if mob in self.items:
            self.items.remove(mob)
        return self

    def insert(self, index, mob, mover=None, **kw):
        self.items.insert(index, mob)
        return self.pack(mover=mover, **kw)

    def pack(self, mover=None, **kw):
        """Animation sliding every item to its slot."""
        anims = []
        for i, m in enumerate(self.items):
            p = self.slot_point(i)
            if np.linalg.norm(m.get_bottom() - p) > 1e-3:
                anims.append((mover or self.mover)(m, p, **kw))
        return AnimationGroup(*anims) if anims else Animation(VGroup(), run_time=0.01)

    def with_items(self):
        """VGroup of the tray/label plus the items (handy for FadeOut)."""
        return VGroup(self, *self.items)


__all__ = ["Queue", "default_mover"]
