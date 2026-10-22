"""StateDiagram: the three-state process model (OSTEP Figure 4.2).

Three circular zones -- Running (left), Ready (right), Blocked (bottom) -- and
four curved, labeled arrows:

* Running -> Ready  (top)     "descheduled"
* Ready -> Running  (bottom)  "scheduled"
* Running -> Blocked          "I/O: initiate"
* Blocked -> Ready            "I/O: done"

Zones can hold a decoration (``running_icon``: e.g. a CPU chip, drawn in the
lower half of the Running zone; the Ready zone has a small tray; the Blocked
zone a clock).  All geometry queries read the live circles, so the diagram can
be moved and scaled freely.

    sd = StateDiagram(running_icon=CPU(size=0.7))
    self.play(sd.create_zones())           # circles + zone labels
    self.play(sd.write_arrow("scheduled"))
    pts = sd.zone_points("ready", 2)       # standing points (bottom-centers)
    self.play(sd.to_legend((4.4, 2.0), 0.45))
    dot = sd.make_dot(color); sd.place_dot(dot, "running")
    self.play(sd.move_dot(dot, "blocked"))
"""
from __future__ import annotations

import numpy as np
from manim import (
    AnimationGroup, Animation, ArcBetweenPoints, Circle, Create, Dot, FadeIn, FadeOut,
    LaggedStart, RoundedRectangle, Text, VGroup, Write, CurvedArrow, StealthTip,
    UP, DOWN, LEFT, RIGHT, ORIGIN, PI,
)

from ..style import TEXT, DIM, CPU_COLOR, VIRT
from .p04_icons import mini_clock

ZONES = ("running", "ready", "blocked")
ARROWS = ("descheduled", "scheduled", "io_initiate", "io_done")
ARROW_TEXT = {"descheduled": "descheduled", "scheduled": "scheduled",
              "io_initiate": "I/O: initiate", "io_done": "I/O: done"}
ZONE_TEXT = {"running": "Running", "ready": "Ready", "blocked": "Blocked"}


def _P(x, y=0.0):
    return np.array([float(x), float(y), 0.0])


def _unit(a):
    return _P(np.cos(a), np.sin(a))


class StateDiagram(VGroup):
    """Parameters: ``positions`` dict zone -> (x, y); ``radius``; ``running_icon``
    (optional mobject placed in the Running zone); ``font_size`` for zone
    labels, ``arrow_font`` for arrow labels; ``zone_color``."""

    def __init__(self, positions=None, radius=1.1, running_icon=None, font_size=30,
                 arrow_font=24, zone_color=TEXT, arrow_color=DIM, **kwargs):
        super().__init__(**kwargs)
        pos = {"running": (-3, 1.2), "ready": (3, 1.2), "blocked": (0, -1.6)}
        pos.update(positions or {})
        self.radius0 = radius
        self.zones = {}
        self.zone_labels = {}
        zone_group = VGroup()
        label_group = VGroup()
        for z in ZONES:
            c = _P(*pos[z])
            circ = Circle(radius=radius).move_to(c).set_stroke(zone_color, 3).set_fill(TEXT, 0.0)
            self.zones[z] = circ
            zone_group.add(circ)
            t = Text(ZONE_TEXT[z], font_size=font_size, color=TEXT, weight="BOLD")
            if z == "blocked":
                t.next_to(circ, DOWN, buff=0.12)
            else:
                t.next_to(circ, UP, buff=0.12)
            self.zone_labels[z] = t
            label_group.add(t)
        # decorations
        deco = VGroup()
        self.running_icon = running_icon
        if running_icon is not None:
            r = self.zones["running"]
            running_icon.move_to(r.get_center() + DOWN * radius * 0.42)
            deco.add(running_icon)
        rz = self.zones["ready"]
        self.tray = RoundedRectangle(width=radius * 1.45, height=0.08, corner_radius=0.04)
        self.tray.move_to(rz.get_center() + DOWN * radius * 0.5).set_fill(DIM, 0.5).set_stroke(DIM, 1.5)
        deco.add(self.tray)
        bz = self.zones["blocked"]
        self.clock = mini_clock(radius=radius * 0.2, stroke_width=2)
        self.clock.move_to(bz.get_center() + _unit(PI / 4) * radius * 0.95)
        deco.add(self.clock)

        # arrows
        self.arrows = {}
        self.arrow_labels = {}
        arrow_group = VGroup()
        arrow_label_group = VGroup()
        R, Rd, B = (self.zones[z].get_center() for z in ZONES)
        specs = {
            "descheduled": (R, PI / 5, Rd, PI - PI / 5, -0.45, UP),
            "scheduled": (Rd, PI + PI / 5, R, -PI / 5, -0.45, DOWN),
            "io_initiate": (R, -PI / 2 + 0.15, B, PI - 0.35, 0.35, LEFT),
            "io_done": (B, 0.35, Rd, -PI / 2 - 0.15, 0.35, RIGHT),
        }
        for name, (c1, a1, c2, a2, ang, side) in specs.items():
            p1 = c1 + _unit(a1) * (radius + 0.08)
            p2 = c2 + _unit(a2) * (radius + 0.08)
            arr = CurvedArrow(p1, p2, angle=ang, tip_length=0.2, stroke_width=3, color=arrow_color)
            self.arrows[name] = arr
            arrow_group.add(arr)
            lab = Text(ARROW_TEXT[name], font_size=arrow_font, color=TEXT)
            mid = arr.point_from_proportion(0.5)
            if name in ("descheduled", "scheduled"):
                lab.next_to(mid, side, buff=0.1)
            else:
                lab.next_to(mid, side, buff=0.3)
            self.arrow_labels[name] = lab
            arrow_label_group.add(lab)

        self.zone_group = zone_group
        self.label_group = label_group
        self.deco = deco
        self.arrow_group = arrow_group
        self.arrow_label_group = arrow_label_group
        self.dots = VGroup()
        self.dot_zone = {}
        self.add(zone_group, label_group, deco, arrow_group, arrow_label_group, self.dots)

    # ------------------------------------------------------------- geometry
    @property
    def radius(self):
        return self.zones["running"].width / 2

    @property
    def scale_factor(self):
        return self.radius / self.radius0

    def zone_center(self, zone):
        return self.zones[zone].get_center()

    def zone_points(self, zone, n=1, spacing=None, y=None):
        """Bottom-center standing points for ``n`` items inside ``zone``.

        Running: on top of the running icon (or the zone's lower third).
        Ready: on the tray.  Blocked: on the zone's lower third."""
        c = self.zone_center(zone)
        r = self.radius
        spacing = spacing if spacing is not None else r * 0.62
        if y is None:
            if zone == "running" and self.running_icon is not None:
                y = self.running_icon.get_top()[1] + 0.02
            elif zone == "ready":
                y = self.tray.get_top()[1] + 0.02
            else:
                y = c[1] - r * 0.5
        xs = [c[0] + (k - (n - 1) / 2) * spacing for k in range(n)]
        return [_P(x, y) for x in xs]

    def arrow_path(self, name):
        return self.arrows[name]

    # ----------------------------------------------------------- animations
    def create_zones(self, run_time=1.5):
        return AnimationGroup(
            LaggedStart(*[Create(self.zones[z]) for z in ZONES], lag_ratio=0.3),
            LaggedStart(*[Write(self.zone_labels[z]) for z in ZONES], lag_ratio=0.3),
            FadeIn(self.deco),
            run_time=run_time,
        )

    def create_arrows(self, run_time=1.0):
        return LaggedStart(*[Create(a) for a in self.arrow_group], lag_ratio=0.2, run_time=run_time)

    def write_arrow(self, name, run_time=0.8):
        return Write(self.arrow_labels[name], run_time=run_time)

    def pulse_arrow(self, name, color=VIRT, run_time=0.8):
        from manim import Indicate
        return Indicate(self.arrows[name], color=color, scale_factor=1.05, run_time=run_time)

    def glow_zone(self, zone, color=CPU_COLOR, run_time=0.6):
        return self.zones[zone].animate(run_time=run_time).set_stroke(color, 5).set_fill(color, 0.08)

    def unglow_zone(self, zone, color=TEXT, run_time=0.6):
        return self.zones[zone].animate(run_time=run_time).set_stroke(color, 3).set_fill(color, 0.0)

    def to_legend(self, point=(4.4, 2.0), scale=0.45, hide_arrow_labels=True, run_time=1.2):
        """Animate into a small 'legend' copy at ``point``. Arrow labels fade
        (they'd be unreadable) unless ``hide_arrow_labels`` is False."""
        target = self.copy()
        if hide_arrow_labels:
            target.arrow_label_group.set_opacity(0)
        target.scale(scale).move_to(_P(*point))
        return self.animate_to(target, run_time)

    def animate_to(self, target, run_time=1.0):
        from manim import Transform
        return Transform(self, target, run_time=run_time)

    def set_legend(self, point=(4.4, 2.0), scale=0.45, hide_arrow_labels=True):
        if hide_arrow_labels:
            self.arrow_label_group.set_opacity(0)
        self.scale(scale).move_to(_P(*point))
        return self

    # ------------------------------------------------------------------ dots
    def make_dot(self, color, radius=None, label=None):
        r = radius if radius is not None else 0.32 * self.radius / 1.1 * 0.55
        d = Dot(radius=r, color=color).set_stroke(TEXT, 1.5)
        if label:
            t = Text(label, font_size=48, color="#1C1C1C", weight="BOLD")
            t.scale_to_fit_height(r * 1.0)
            t.move_to(d)
            d = VGroup(d, t)
        return d

    def _dot_points(self, zone, n):
        c = self.zone_center(zone)
        r = self.radius
        sp = r * 0.5
        dy = {"running": 0.3 if self.running_icon is not None else 0.0,
              "ready": -0.2, "blocked": 0.0}[zone]
        return [c + RIGHT * (k - (n - 1) / 2) * sp + UP * r * dy for k in range(n)]

    def place_dot(self, dot, zone):
        """Instantly put a tracking dot in a zone (and re-pack that zone)."""
        self.dot_zone[dot] = zone
        if dot not in self.dots:
            self.dots.add(dot)
        self._repack(zone, animate=False)
        return self

    def move_dot(self, dot, zone, run_time=0.6):
        """Animation moving a tracking dot to another zone (re-packing both)."""
        old = self.dot_zone.get(dot)
        self.dot_zone[dot] = zone
        if dot not in self.dots:
            self.dots.add(dot)
        anims = self._repack(zone, animate=True, run_time=run_time)
        if old and old != zone:
            anims += self._repack(old, animate=True, run_time=run_time)
        return AnimationGroup(*anims) if anims else Animation(VGroup(), run_time=run_time)

    def remove_dot(self, dot, run_time=0.4):
        zone = self.dot_zone.pop(dot, None)
        anims = [dot.animate(run_time=run_time).set_opacity(0)]
        if zone:
            anims += self._repack(zone, animate=True, run_time=run_time)
        return AnimationGroup(*anims)

    def _repack(self, zone, animate, run_time=0.6):
        members = [d for d in self.dots if self.dot_zone.get(d) == zone]
        pts = self._dot_points(zone, len(members))
        anims = []
        for d, p in zip(members, pts):
            if animate:
                anims.append(d.animate(run_time=run_time).move_to(p))
            else:
                d.move_to(p)
        return anims


STATE_ZONES, STATE_ARROWS = ZONES, ARROWS

__all__ = ["StateDiagram", "STATE_ZONES", "STATE_ARROWS"]
