"""MLFQLadder: a stack of priority lanes (the ready queue grown into a ladder).

    lad = MLFQLadder(levels=3)                  # Q2 / Q1 / Q0, or levels=8 for Figure 8.1 (Q8..Q1)
    job.scale(lad.job_scale); lad.place(job, 2)  # instant
    self.play(lad.promote(job, 2))               # hop to another lane (also used to demote)
    self.play(lad.demote(job))                   # one lane down
    self.play(lad.boost_all())                   # everyone hops to the top lane (LaggedStart)
    self.play(lad.serve(2))                      # the lane being served gets a CPU_COLOR stroke
    self.play(lad.collapse_to(3))                # 8 lanes -> Q2/Q1/Q0 (jobs must be re-placed)

Jobs are *not* children of the ladder; the ladder tracks them in ``items[level]``.
A job's center sits on the lane's center line (``lane_point``).  ``job_scale`` is the
Process scale that fits the lane (0.3 in 8-lane mode, 0.6 in 3-lane mode).
"""
from __future__ import annotations

import numpy as np
from manim import (
    AnimationGroup, Arrow, LaggedStart, RoundedRectangle, Text, VGroup, FadeIn, UP, DOWN, LEFT, RIGHT, PI,
    Succession, Wait,
)

from ..style import TEXT, DIM, CPU_COLOR
from .core import hop_to


def _P(x, y=0.0):
    return np.array([float(x), float(y), 0.0])


def _geom(levels):
    if levels == 8:
        return dict(ids=list(range(8, 0, -1)), top=2.3, step=0.5, scale=0.3, spacing=0.62, font=18)
    if levels == 3:
        return dict(ids=[2, 1, 0], top=2.05, step=0.95, scale=0.6, spacing=0.85, font=24)
    ids = list(range(levels - 1, -1, -1))
    return dict(ids=ids, top=2.3, step=min(0.95, 3.0 / max(levels - 1, 1)), scale=0.5, spacing=0.75, font=20)


class MLFQLadder(VGroup):
    def __init__(self, levels=3, labels=None, x_range=(-5.4, 0.2), arrows=True, **kwargs):
        super().__init__(**kwargs)
        self.levels = levels
        g = _geom(levels)
        self.x0, self.x1 = map(float, x_range)
        self.top_y, self.step = g["top"], g["step"]
        self.job_scale, self.spacing, self.label_font = g["scale"], g["spacing"], g["font"]
        self.ids = list(g["ids"])
        self.names = list(labels) if labels else [f"Q{i}" for i in self.ids]
        self.lanes, self.labels = {}, {}
        self.items = {i: [] for i in self.ids}
        self.lane_of = {}
        for k, lid in enumerate(self.ids):
            lane = RoundedRectangle(width=self.x1 - self.x0, height=self.step - 0.08, corner_radius=0.12)
            lane.set_fill(DIM, 0.06).set_stroke(DIM, 1.5)
            lane.set_z_index(-1)   # lanes stay under the jobs even after .animate re-adds them
            lane.move_to(_P((self.x0 + self.x1) / 2, self.lane_y(lid)))
            lab = Text(self.names[k], font_size=self.label_font, color=TEXT)
            lab.move_to(_P(self.x0 - 0.38, self.lane_y(lid)))
            self.lanes[lid], self.labels[lid] = lane, lab
            self.add(lane, lab)
        self.arrows = VGroup()
        if arrows:
            ytop, ybot = self.lane_y(self.ids[0]), self.lane_y(self.ids[-1])
            mid = (ytop + ybot) / 2
            x = self.x0 - 1.05
            up = Arrow(_P(x, mid + 0.15), _P(x, ytop + self.step / 2 - 0.05), buff=0, stroke_width=3, color=DIM,
                       tip_length=0.15, max_tip_length_to_length_ratio=0.5)
            dn = Arrow(_P(x, mid - 0.15), _P(x, ybot - self.step / 2 + 0.05), buff=0, stroke_width=3, color=DIM,
                       tip_length=0.15, max_tip_length_to_length_ratio=0.5)
            hi = Text("high priority", font_size=16, color=DIM).rotate(PI / 2).move_to(_P(x + 0.28, (ytop + mid) / 2 + 0.2))
            lo = Text("low priority", font_size=16, color=DIM).rotate(PI / 2).move_to(_P(x + 0.28, (ybot + mid) / 2 - 0.2))
            self.arrows = VGroup(up, dn, hi, lo)
            self.arrows.up, self.arrows.down = up, dn
            self.add(self.arrows)

    # ------------------------------------------------------------ geometry
    def lane_y(self, level):
        k = self.ids.index(level)
        return self.top_y - k * self.step

    def slot_x(self, slot):
        return self.x0 + 0.55 + slot * self.spacing

    def lane_point(self, level, slot=0):
        """Center of a job standing in ``slot`` of lane ``level``."""
        return _P(self.slot_x(slot), self.lane_y(level))

    def lane_rect(self, level):
        return self.lanes[level]

    def right_point(self, level):
        return _P(self.x1, self.lane_y(level))

    # ------------------------------------------------------------ jobs
    def _free_slot(self, level):
        used = {s for s, _ in self.items[level]}
        s = 0
        while s in used:
            s += 1
        return s

    def _unseat(self, job):
        lv = self.lane_of.pop(job, None)
        if lv is not None:
            self.items[lv] = [(s, j) for s, j in self.items[lv] if j is not job]

    def place(self, job, level, slot=None):
        """Instantly put ``job`` in a lane."""
        self._unseat(job)
        slot = self._free_slot(level) if slot is None else slot
        job.move_to(self.lane_point(level, slot))
        self.items[level].append((slot, job))
        self.lane_of[job] = level
        return job

    def register(self, job, level, slot=None):
        """Bookkeeping only (no movement); returns the lane point the job should go to."""
        self._unseat(job)
        slot = self._free_slot(level) if slot is None else slot
        self.items[level].append((slot, job))
        self.lane_of[job] = level
        return self.lane_point(level, slot)

    def release(self, job):
        """Forget the job's lane (e.g. when it is on the CPU)."""
        self._unseat(job)
        return job

    def promote(self, job, level, slot=None, **kw):
        """Animation: ``job`` hops to ``level`` (up or down)."""
        self._unseat(job)
        slot = self._free_slot(level) if slot is None else slot
        self.items[level].append((slot, job))
        self.lane_of[job] = level
        kw.setdefault("run_time", 0.6)
        return hop_to(job, self.lane_point(level, slot), anchor="center", **kw)

    def demote(self, job, **kw):
        k = self.ids.index(self.lane_of[job])
        return self.promote(job, self.ids[min(k + 1, len(self.ids) - 1)], **kw)

    def boost_all(self, level=None, lag=0.18, **kw):
        """Every placed job hops to the top lane (LaggedStart)."""
        top = self.ids[0] if level is None else level
        jobs = [j for lv in self.ids for _, j in sorted(self.items[lv], key=lambda t: t[0])]
        anims = []
        for j in jobs:
            if self.lane_of.get(j) != top:
                anims.append(self.promote(j, top, **kw))
        if not anims:
            return Wait(0.1)
        return LaggedStart(*anims, lag_ratio=lag)

    # ------------------------------------------------------------ highlight
    def serve(self, level=None, color=CPU_COLOR):
        """Animation: lane ``level`` gets a ``color`` stroke, the others go back to DIM (None = none)."""
        anims = []
        for lid, lane in self.lanes.items():
            if lane.get_stroke_opacity() == 0:
                continue
            if lid == level:
                anims.append(lane.animate.set_stroke(color, 3.5).set_fill(color, 0.12))
            else:
                anims.append(lane.animate.set_stroke(DIM, 1.5).set_fill(DIM, 0.06))
        return AnimationGroup(*anims)

    glow_lane = serve

    # ------------------------------------------------------------ 8 -> 3
    def collapse_to(self, levels=3, run_time=1.2):
        """Animation turning this 8-lane ladder into the 3-lane Q2/Q1/Q0 one (in place).
        Surplus lanes fade (they stay as invisible members).  Jobs must be re-placed afterwards."""
        tg = _geom(levels)
        keep = [0, 3, 7] if levels == 3 else list(range(levels))
        anims = []
        old_ids = list(self.ids)
        new_lanes, new_labels = {}, {}
        for n, k in enumerate(old_ids):
            lane, lab = self.lanes[k], self.labels[k]
            if n in keep:
                j = keep.index(n)
                ty = tg["top"] - j * tg["step"]
                nid = tg["ids"][j]
                anims.append(lane.animate.stretch_to_fit_height(tg["step"] - 0.08).move_to(_P(lane.get_center()[0], ty)))
                newlab = Text(f"Q{nid}", font_size=tg["font"], color=TEXT).move_to(_P(self.x0 - 0.38, ty))
                anims.append(_swap(lab, newlab))
                new_lanes[nid], new_labels[nid] = lane, lab
            else:
                anims.append(lane.animate.set_opacity(0))
                anims.append(lab.animate.set_opacity(0))
        # priority arrows: re-span the new ladder
        self.lanes, self.labels = new_lanes, new_labels
        self.ids = list(tg["ids"])
        self.top_y, self.step = tg["top"], tg["step"]
        self.job_scale, self.spacing, self.label_font = tg["scale"], tg["spacing"], tg["font"]
        self.levels = levels
        self.names = [f"Q{i}" for i in self.ids]
        self.items = {i: [] for i in self.ids}
        self.lane_of = {}
        if len(self.arrows):
            up, dn, hi, lo = self.arrows
            ytop, ybot = self.lane_y(self.ids[0]), self.lane_y(self.ids[-1])
            mid = (ytop + ybot) / 2
            x = up.get_start()[0]
            anims.append(up.animate.put_start_and_end_on(_P(x, mid + 0.15), _P(x, ytop + self.step / 2 - 0.05)))
            anims.append(dn.animate.put_start_and_end_on(_P(x, mid - 0.15), _P(x, ybot - self.step / 2 + 0.05)))
            anims.append(hi.animate.move_to(_P(hi.get_center()[0], (ytop + mid) / 2 + 0.2)))
            anims.append(lo.animate.move_to(_P(lo.get_center()[0], (ybot + mid) / 2 - 0.2)))
        return AnimationGroup(*anims, run_time=run_time)


def _swap(lab, newlab):
    from manim import Transform
    return Transform(lab, newlab)


__all__ = ["MLFQLadder"]
