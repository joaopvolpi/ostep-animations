"""Core props shared by every episode (CPU, Memory, Disk, cards, term highlight...).

Everything is built from Manim primitives in the series palette, with the same
flat-fill + darker-outline look as the characters.  See ``CORE_API.md``.
"""
from __future__ import annotations

import numpy as np
from manim import (
    Animation, AnimationGroup, Arc, ArcBetweenPoints, Circle, Create, DashedLine,
    DashedVMobject, Dot, Ellipse, FadeIn, FadeOut, Line, Polygon, Rectangle,
    Rotate, RoundedRectangle, Square, Succession, Text, Transform, VGroup, VMobject,
    Wait, Write, ReplacementTransform, GrowFromCenter,
    DOWN, LEFT, ORIGIN, RIGHT, UP, DL, DR, UL, UR, PI, TAU, BOLD, config, linear, smooth,
)

from ..style import (
    BG, CPU_COLOR, DIM, DISK_COLOR, FONT, MEM_COLOR, MONO_FONT, PERS, TEXT, VIRT,
)
from ..characters.base import Character, darker, lighter, mix

INK = "#1E1A1E"          # same ink as the characters' outlines
CARD_FILL = "#242424"    # card background (slightly lighter than BG)
PEACH_COLOR = "#FFB07A"
PEACH_CREASE = "#F88017"

# Screen zones (see the bible, "Screen zones").  The top band belongs to the chrome:
# section badge (top-left) and docked term (top-right) on row y=3.6, the docked crux
# strip centered at y=3.0.  Scene content (diagrams, labels, titles) stays below CONTENT_TOP.
CONTENT_TOP = 2.55
CHROME_ROW_Y = 3.6
CRUX_STRIP_Y = 3.0
SCRIM_Z = 40

# Canonical host positions (Student left, Professor right, facing each other).  Characters are
# placed by their design-frame anchor (see Character.get_critical_point), so these are exact
# whatever the expression: use them, or `host_pair`, in every scene so cuts never jump.
HOST_SCALE = 0.75
STU_CORNER = np.array([-5.8, -2.8, 0.0])
PROF_CORNER = np.array([5.8, -2.8, 0.0])
STU_DIALOGUE = np.array([-2.6, -1.2, 0.0])
PROF_DIALOGUE = np.array([2.6, -1.2, 0.0])


def tag_role(mob, role):
    """Give ``mob`` and every part of it a layout role for the overlap check ("chrome", "host",
    "panel", "actor", "prop", "background" or "ignore"; see ``ostep_lib/layout.py``).  Parts are
    tagged too because animations often add them to the scene one by one."""
    for m in mob.get_family():
        m.ostep_role = role
    return mob


def late(delay, anim):
    """Start ``anim`` after ``delay`` seconds inside a larger play WITHOUT the t=0 flash that
    ``Succession(Wait(delay), anim)`` causes (a Succession adds its non-first members' mobjects
    to the scene at full opacity at t=0, so a veil or a big term would pop up early)."""
    return AnimationGroup(Wait(delay), anim, lag_ratio=1)


def finish_now(anim):
    """Run an animation to its end state instantly: builds a scene's "starts with" state."""
    anim.scene = None
    anim.begin()
    anim.finish()
    return anim


def host_pair(mode="corner", stu_expr="neutral", prof_expr="neutral"):
    """Student (facing right) and Professor (flipped, facing left) in ``"corner"`` or
    ``"dialogue"`` mode, looking at each other.  ``host_mode_anims`` moves them between modes."""
    from ..characters.humanoid import Professor, Student
    stu, prof = Student(stu_expr), Professor(prof_expr).flip()
    stu.mode_scale = prof.mode_scale = 1.0
    if mode == "corner":
        stu.scale(HOST_SCALE).move_to(STU_CORNER)
        prof.scale(HOST_SCALE).move_to(PROF_CORNER)
        stu.mode_scale = prof.mode_scale = HOST_SCALE
    else:
        stu.move_to(STU_DIALOGUE)
        prof.move_to(PROF_DIALOGUE)
    stu.set_look(prof)
    prof.set_look(stu)
    return stu, prof


def host_mode_anims(stu, prof, mode, run_time=1.0):
    """List of animations gliding both hosts to ``"corner"`` or ``"dialogue"`` mode."""
    s = HOST_SCALE if mode == "corner" else 1.0
    out = []
    for ch, pos in ((stu, STU_CORNER if mode == "corner" else STU_DIALOGUE),
                    (prof, PROF_CORNER if mode == "corner" else PROF_DIALOGUE)):
        f = s / getattr(ch, "mode_scale", 1.0)
        ch.mode_scale = s
        out.append(ch.animate(run_time=run_time).scale(f).move_to(pos))
    return out


__all__ = [
    "INK", "CARD_FILL", "PEACH_COLOR", "CONTENT_TOP", "CHROME_ROW_Y", "CRUX_STRIP_Y", "scrim",
    "HOST_SCALE", "STU_CORNER", "PROF_CORNER", "tag_role", "STU_DIALOGUE", "PROF_DIALOGUE",
    "host_pair", "host_mode_anims", "late", "finish_now",
    "outline_of", "label_text", "mono_text", "wrap_text", "centered_text", "make_translucent",
    "base_point", "place_on", "hop_to", "HopTo",
    "CPU", "Memory", "Disk", "DiskSpin",
    "CruxCard", "TipCard", "AsideCard", "TermHighlight", "SectionBadge", "IllusionSplit",
    "Peach", "FileIcon", "ClockIcon", "Spotlight", "GearPair", "PauseGlyph", "PlayGlyph",
    "Laptop",
]


# ---------------------------------------------------------------------------
# small helpers
# ---------------------------------------------------------------------------
def outline_of(color, amount=0.55):
    """The darker outline color the characters use for a given fill."""
    return darker(color, amount)


def label_text(s, font_size=24, color=TEXT, weight="NORMAL", **kw):
    """Text in the series font (CMU Serif)."""
    return Text(str(s), font=FONT, font_size=font_size, color=color, weight=weight, **kw)


def mono_text(s, font_size=24, color=TEXT, weight="NORMAL", **kw):
    """Text in the series monospace font (CMU Typewriter Text)."""
    return Text(str(s), font=MONO_FONT, font_size=font_size, color=color, weight=weight, **kw)


def wrap_text(s, max_width, font_size=30, font=FONT, weight="NORMAL"):
    """Greedy word wrap: returns ``s`` with newlines so each line fits ``max_width``."""
    words = str(s).split()
    lines, cur = [], ""
    for w in words:
        cand = (cur + " " + w).strip()
        if cur and Text(cand, font=font, font_size=font_size, weight=weight).width > max_width:
            lines.append(cur)
            cur = w
        else:
            cur = cand
    if cur:
        lines.append(cur)
    return "\n".join(lines)


def centered_text(s, max_width, font_size=30, color=TEXT, font=FONT, weight="NORMAL",
                  line_buff=0.12):
    """Word-wrapped text with each line centered (Text alone left-aligns lines).
    Returns a VGroup of one Text per line."""
    lines = wrap_text(s, max_width, font_size, font, weight).split("\n")
    g = VGroup(*[Text(l, font=font, font_size=font_size, color=color, weight=weight) for l in lines])
    return g.arrange(DOWN, buff=line_buff)


def make_translucent(mob, fill_opacity=0.25, stroke_opacity=0.6):
    """Series 'virtual copy' look: fill 0.25, stroke 0.6 (in place, returns mob).
    Opacities are multiplied, so parts that were invisible stay invisible."""
    for sm in mob.get_family():
        if isinstance(sm, VMobject) and len(sm.points):
            sm.set_fill(opacity=sm.get_fill_opacity() * fill_opacity, family=False)
            sm.set_stroke(opacity=sm.get_stroke_opacity() * stroke_opacity, family=False)
    return mob


def base_point(mob):
    """The point a mobject 'stands' on: the feet of a Process, the bottom of the
    body of other characters, the bottom-center of anything else."""
    if isinstance(mob, Character):
        from ..characters.process import Process
        if isinstance(mob, Process):
            return mob.to_global(np.array([0.0, -1.05, 0.0]))
        b = mob.core.get_bottom()
        return np.array([mob.to_global(np.zeros(3))[0], b[1], 0.0])
    return mob.get_bottom()


def place_on(mob, point):
    """Move ``mob`` so that its base point (see :func:`base_point`) is at ``point``."""
    mob.shift(np.array(point, dtype=float) - base_point(mob))
    return mob


class HopTo(Animation):
    """Arc hop with squash and stretch.  Use :func:`hop_to`."""

    def __init__(self, mobject, point, height=None, anchor="base", squash=0.18, **kwargs):
        kwargs.setdefault("run_time", 0.5)
        kwargs.setdefault("rate_func", linear)
        self.target_point = np.array(point, dtype=float)
        self.hop_height = height
        self.anchor = anchor
        self.squash = squash
        super().__init__(mobject, **kwargs)

    def _anchor(self):
        if self.anchor == "center":
            return self.mobject.get_center()
        return base_point(self.mobject)

    def begin(self):
        self._fam = [sm for sm in self.mobject.get_family() if len(sm.points)]
        self._start = [sm.points.copy() for sm in self._fam]
        self._p0 = self._anchor().copy()
        d = self.target_point - self._p0
        if self.hop_height is None:
            self.hop_height = 0.35 + 0.18 * np.linalg.norm(d[:2])
        # base of the mobject for squash (bottom-center for 'center' anchors too)
        self._base = base_point(self.mobject).copy()
        super().begin()

    def interpolate_mobject(self, alpha):
        a = self.rate_func(alpha)
        t0, t1 = 0.12, 0.85
        s = self.squash
        if a < t0:                      # take-off squash
            k = np.sin(PI * a / t0)
            t, sy, sx = 0.0, 1 - s * k, 1 + 0.7 * s * k
        elif a < t1:                    # flight: stretched
            t = smooth((a - t0) / (t1 - t0))
            k = np.sin(PI * (a - t0) / (t1 - t0))
            t_lin = (a - t0) / (t1 - t0)
            sy, sx = 1 + 0.6 * s * k, 1 - 0.35 * s * k
        else:                           # landing squash
            k = np.sin(PI * (a - t1) / (1 - t1))
            t, sy, sx = 1.0, 1 - s * k, 1 + 0.7 * s * k
        d = self.target_point - self._p0
        if t0 <= a < t1:
            off = d * t_lin + UP * self.hop_height * 4 * t_lin * (1 - t_lin)
        else:
            off = d * t
        base = self._base
        for sm, p in zip(self._fam, self._start):
            q = p - base
            q = q * np.array([sx, sy, 1.0])
            sm.points = q + base + off


def hop_to(mobject, point, height=None, anchor="base", squash=0.18, **kwargs):
    """Animation: ``mobject`` hops along an arc so that its base point (feet of a
    Process / bottom of anything else, or its center with ``anchor="center"``)
    lands on ``point``.  Squashes on take-off and landing, stretches in flight.

    Don't combine with ``change``/``look_at`` of the same character in one play
    (use a ``Succession`` or separate plays)."""
    return HopTo(mobject, point, height=height, anchor=anchor, squash=squash, **kwargs)


# ---------------------------------------------------------------------------
# CPU
# ---------------------------------------------------------------------------
class CPU(VGroup):
    """Yellow chip with pins on four sides.

    ``CPU(size=1.4, label="CPU", color=CPU_COLOR, pins=4, font_size=None)``.
    Parts: ``body``, ``die`` (inner square, put content on ``die.get_center()``),
    ``pins``, ``label``.  ``slot_point()`` is where a running process stands
    (top-center of the body); ``seat(process)`` moves a process there.
    """

    def __init__(self, size=1.4, label="CPU", color=CPU_COLOR, pins=4, font_size=None, **kwargs):
        super().__init__(**kwargs)
        self.size = size
        out = outline_of(color)
        pin_len, pin_w = size * 0.11, size * 0.07
        n_pins = pins
        pins = VGroup()
        offs = np.linspace(-0.3, 0.3, n_pins) * size if n_pins > 1 else [0.0]
        for o in offs:
            for d in (UP, DOWN, LEFT, RIGHT):
                horiz = abs(d[0]) > 0
                r = Rectangle(width=pin_len if horiz else pin_w, height=pin_w if horiz else pin_len)
                perp = np.array([d[1], d[0], 0])
                r.move_to(d * (size / 2 + pin_len / 2 - 0.01) + perp * o)
                pins.add(r)
        pins.set_fill(mix(color, "#9A9A9A", 0.75), 1).set_stroke(out, 2)
        body = RoundedRectangle(width=size, height=size, corner_radius=size * 0.1)
        body.set_fill(color, 1).set_stroke(out, 4)
        die = RoundedRectangle(width=size * 0.62, height=size * 0.62, corner_radius=size * 0.06)
        die.set_fill(darker(color, 0.18), 1).set_stroke(out, 2)
        dot = Circle(radius=size * 0.035).move_to(body.get_corner(DL) + (UR * size * 0.11))
        dot.set_fill(out, 1).set_stroke(width=0)
        self.pins, self.body, self.die, self.mark = pins, body, die, dot
        self.add(pins, body, die, dot)
        if label:
            fs = font_size or max(14, int(26 * size / 1.4))
            self.label = Text(label, font=FONT, font_size=fs, color=INK, weight=BOLD)
            if self.label.width > die.width * 0.9:
                self.label.scale_to_fit_width(die.width * 0.9)
            self.label.move_to(die)
            self.add(self.label)
        else:
            self.label = VGroup()

    def slot_point(self):
        """Point where a running process stands: top-center of the body."""
        return self.body.get_top()

    def seat(self, process):
        """Instantly place ``process`` so it stands on the chip. Returns process."""
        return place_on(process, self.slot_point())

    def virtual_copy(self, fill_opacity=0.25, stroke_opacity=0.6):
        """Translucent copy (the series' 'virtual CPU' look)."""
        return make_translucent(self.copy(), fill_opacity, stroke_opacity)


# ---------------------------------------------------------------------------
# Memory (vertical column)
# ---------------------------------------------------------------------------
class Memory(VGroup):
    """Tall blue column of stacked cells, addresses on the left (0 at the top).

    Two ways to build it:

    * ``Memory(cells=8, contents=[...])``: equal cells, optional text per cell.
    * ``Memory(regions=["code", "static data", ("heap", 1.5), ("free", 2), "stack"])``:
      named regions (``name`` or ``(name, weight)``); the label is the content.

    Args: ``width=1.4, height=4.4, color=MEM_COLOR, font_size=18, mono=True``
    (cell contents in MONO_FONT; regions use the serif font), ``addresses=True``
    (or a list of strings, one per cell top; default "0", "1", ...),
    ``title=None`` (shown above the column).

    Access: ``cells`` (rects), ``texts`` (one Text per cell, empty if none),
    ``addresses``, ``cell(i)``, ``region(name)`` (rect), ``index_of(name)``.
    Animations: ``set_content(i, text)``, ``fill_cell(i_or_name, color, opacity)``,
    ``clear_cell(i)``.
    """

    def __init__(self, cells=8, regions=None, contents=None, width=1.4, height=4.4,
                 color=MEM_COLOR, font_size=18, mono=True, addresses=True, title=None,
                 cell_fill_opacity=0.18, **kwargs):
        super().__init__(**kwargs)
        self.color = color
        self.font_size = font_size
        self.mono = mono if regions is None else False
        if regions is not None:
            names, weights = [], []
            for r in regions:
                if isinstance(r, (tuple, list)):
                    names.append(r[0]); weights.append(float(r[1]))
                else:
                    names.append(r); weights.append(1.0)
            contents = names
            self.names = names
        else:
            weights = [1.0] * cells
            self.names = [None] * cells
            contents = list(contents or []) + [""] * (cells - len(contents or []))
        tot = sum(weights)
        self.cells = VGroup()
        self.texts = VGroup()
        y = height / 2
        self._fill_opacity = cell_fill_opacity
        for w, c in zip(weights, contents):
            h = height * w / tot
            r = Rectangle(width=width, height=h).move_to(UP * (y - h / 2))
            # opaque fill that looks like `color` at cell_fill_opacity over BG
            r.set_fill(mix(color, BG, 1 - cell_fill_opacity), 1).set_stroke(color, 3)
            self.cells.add(r)
            self.texts.add(self._make_text(c, r))
            y -= h
        self.add(self.cells, self.texts)
        self.addresses = VGroup()
        if addresses:
            labels = addresses if isinstance(addresses, (list, tuple)) else None
            if labels is None:
                labels = [str(i) for i in range(len(self.cells))]
            for r, s in zip(self.cells, labels):
                if s is None or s == "":
                    self.addresses.add(VGroup())
                    continue
                t = Text(str(s), font=MONO_FONT, font_size=max(12, font_size - 4), color=DIM)
                t.next_to(r.get_corner(UL), LEFT, buff=0.1).align_to(r, UP).shift(DOWN * 0.04)
                self.addresses.add(t)
            self.add(self.addresses)
        self.title = VGroup()
        if title:
            self.title = Text(title, font=FONT, font_size=font_size + 6, color=color)
            self.title.next_to(self.cells, UP, buff=0.15)
            self.add(self.title)

    def _make_text(self, s, rect):
        if not s:
            return VGroup().move_to(rect)
        f = MONO_FONT if self.mono else FONT
        t = Text(str(s), font=f, font_size=self.font_size, color=TEXT)
        if t.width > rect.width * 0.9:
            t.scale_to_fit_width(rect.width * 0.9)
        if t.height > rect.height * 0.8:
            t.scale_to_fit_height(rect.height * 0.8)
        return t.move_to(rect)

    def cell(self, i):
        return self.cells[self.index_of(i)]

    def index_of(self, key):
        if isinstance(key, str):
            return self.names.index(key)
        return key

    def region(self, name):
        return self.cells[self.index_of(name)]

    def cell_center(self, i):
        return self.cell(i).get_center()

    def set_content(self, i, s, **kw):
        """Animation: replace cell ``i``'s text with ``s`` ("" empties it)."""
        i = self.index_of(i)
        old = self.texts[i]
        new = self._make_text(s, self.cells[i])
        if not s:
            new = Text(".", font=FONT, font_size=self.font_size).set_opacity(0).move_to(self.cells[i])
        self.texts.submobjects[i] = new
        kw.setdefault("run_time", 0.5)
        if len(old.points) == 0 and not old.submobjects:
            return AnimationGroup(FadeIn(new, scale=0.6), **kw)
        return AnimationGroup(FadeOut(old, scale=0.6), FadeIn(new, scale=1.4), **kw)

    def fill_cell(self, i, color, opacity=0.6, **kw):
        """Animation: fill a cell or region with ``color``."""
        kw.setdefault("run_time", 0.5)
        return self.cell(i).animate(**kw).set_fill(color, opacity)

    def clear_cell(self, i, **kw):
        return self.fill_cell(i, mix(self.color, BG, 1 - self._fill_opacity), 1, **kw)


# ---------------------------------------------------------------------------
# Disk
# ---------------------------------------------------------------------------
class Disk(VGroup):
    """Green cylinder (platter seen at an angle).

    ``Disk(width=1.6, height=1.3, color=DISK_COLOR, label=None)``.
    Parts: ``body``, ``top`` (ellipse), ``arm`` (stripe on the top surface).
    ``top_point()`` = center of the top surface (to stack files on it).
    ``spin(turns=1, run_time=1)`` returns an animation turning the stripe.
    """

    def __init__(self, width=1.6, height=1.3, color=DISK_COLOR, label=None, font_size=22, **kwargs):
        super().__init__(**kwargs)
        out = outline_of(color)
        ry = width * 0.17
        self.rx, self.ry = width / 2, ry
        h = height - 2 * ry
        # body = rect + bottom half ellipse
        body = VMobject()
        bot = Ellipse(width=width, height=2 * ry).shift(DOWN * h / 2)
        arc_pts = [np.array([width / 2 * np.cos(t), -h / 2 + ry * np.sin(t), 0])
                   for t in np.linspace(0, -PI, 25)]
        pts = [np.array([width / 2, h / 2, 0])] + arc_pts + [np.array([-width / 2, h / 2, 0])]
        body.set_points_as_corners(pts + [pts[0]])
        body.set_fill(darker(color, 0.12), 1).set_stroke(out, 4)
        band = Arc(radius=1, start_angle=PI, angle=PI).stretch(width / 2 * 0.98, 0).stretch(ry, 1)
        band.shift(DOWN * (h / 2 - h * 0.35)).set_stroke(darker(color, 0.35), 2.5).set_fill(opacity=0)
        top = Ellipse(width=width, height=2 * ry).shift(UP * h / 2)
        top.set_fill(lighter(color, 0.25), 1).set_stroke(out, 4)
        hub = Ellipse(width=width * 0.16, height=2 * ry * 0.16).move_to(top)
        hub.set_fill(darker(color, 0.3), 1).set_stroke(out, 2)
        self._top_c = top.get_center()
        arm = Line(top.get_center(), top.get_center() + RIGHT * width / 2 * 0.8)
        arm.set_stroke(darker(color, 0.45), 4)
        self.body, self.top, self.hub, self.arm, self.band = body, top, hub, arm, band
        self.add(body, top, arm, hub)
        self.label = VGroup()
        if label:
            self.label = Text(label, font=FONT, font_size=font_size, color=INK, weight=BOLD)
            self.label.move_to(body.get_center() + DOWN * ry * 0.6)
            if self.label.width > width * 0.85:
                self.label.scale_to_fit_width(width * 0.85)
            self.add(self.label)

    def top_point(self):
        return self.top.get_center()

    def spin(self, turns=1.0, run_time=1.0, **kw):
        return DiskSpin(self, turns=turns, run_time=run_time, **kw)


class DiskSpin(Animation):
    """Turns a Disk's stripe around its (elliptical) top surface."""

    def __init__(self, disk, turns=1.0, **kwargs):
        self.turns = turns
        kwargs.setdefault("rate_func", linear)
        super().__init__(disk.arm, **kwargs)
        self.disk = disk

    def interpolate_mobject(self, alpha):
        d = self.disk
        c = d.top.get_center()
        rx = d.top.width / 2 * 0.8
        ry = d.top.height / 2 * 0.8
        th = TAU * self.turns * alpha
        end = c + np.array([rx * np.cos(th), ry * np.sin(th), 0])
        self.mobject.put_start_and_end_on(c, end)


# ---------------------------------------------------------------------------
# Cards
# ---------------------------------------------------------------------------
class CruxCard(VGroup):
    """The book's crux box: accent frame, "THE CRUX" header, bold question,
    optional DIM subtitle.

    ``CruxCard(question, subtitle=None, accent=VIRT, width=9, header="THE CRUX",
    question_size=34, subtitle_size=24)``.  Parts: ``frame``, ``header``,
    ``question``, ``subtitle``.
    ``write()`` animation: frame grows, texts write.
    ``dock(point=(0, 3.2), font_size=24)`` animation: becomes a one-line strip
    with just the question (the strip mobject is ``self`` afterwards).
    """

    def __init__(self, question, subtitle=None, accent=VIRT, width=9.0, header="THE CRUX",
                 question_size=34, subtitle_size=24, **kwargs):
        super().__init__(**kwargs)
        self.accent = accent
        self.question_str = question
        self.subtitle_str = subtitle or ""
        inner = width - 0.8
        self.header = Text(header, font=FONT, font_size=22, color=accent, weight=BOLD)
        self.question = centered_text(question, inner, question_size, TEXT, weight=BOLD)
        parts = [self.header, self.question]
        self.subtitle = VGroup()
        if subtitle:
            self.subtitle = centered_text(subtitle, inner, subtitle_size, DIM, line_buff=0.08)
            parts.append(self.subtitle)
        body = VGroup(*parts).arrange(DOWN, buff=0.28)
        h = body.height + 0.7
        self.frame = RoundedRectangle(width=width, height=h, corner_radius=0.25)
        self.frame.set_fill(CARD_FILL, 1).set_stroke(accent, 5)
        body.move_to(self.frame)
        self.add(self.frame, self.header, self.question, self.subtitle)
        tag_role(self, "chrome")

    def write(self, run_time=1.6):
        """Silent write of the whole card. Prefer ``NarratedScene.say_crux``: a crux on screen
        is always read aloud (and so captioned)."""
        anims = [FadeIn(self.frame, scale=0.92), Write(self.header), Write(self.question)]
        if len(self.subtitle):
            anims.append(FadeIn(self.subtitle, shift=UP * 0.1))
        return Succession(AnimationGroup(*anims[:2]), *anims[2:], run_time=run_time)

    def write_head(self, run_time=1.4):
        """Frame + header + question (the subtitle stays hidden: it is not in the scene yet)."""
        return Succession(AnimationGroup(FadeIn(self.frame, scale=0.92), Write(self.header)),
                          Write(self.question), run_time=run_time)

    def write_sub(self, run_time=0.8):
        """The subtitle fades in (only valid after ``write_head``)."""
        return FadeIn(self.subtitle, shift=UP * 0.1, run_time=run_time)

    def strip(self, point=(0, 3.0, 0), font_size=24, max_width=7.6):
        q = Text(self.question_str, font=FONT, font_size=font_size, color=TEXT, weight=BOLD)
        if q.width > max_width:
            q.scale_to_fit_width(max_width)
        fr = RoundedRectangle(width=q.width + 0.6, height=q.height + 0.3, corner_radius=0.12)
        fr.set_fill(CARD_FILL, 1).set_stroke(self.accent, 3)
        g = VGroup(fr, q).move_to(np.array(point, dtype=float))
        # match the submobject layout of the card: frame, header, question, subtitle
        def ghost():
            return Dot(fr.get_center(), radius=0.001).set_opacity(0)
        return tag_role(VGroup(fr, ghost(), q, ghost()), "chrome")

    def dock(self, point=(0, 3.0, 0), font_size=24, run_time=1.0):
        """Frame and question morph into the strip; header and subtitle fade out and are
        dropped from the card afterwards (no leftover ghost points)."""
        fr, _, q, _ = self.strip(point, font_size)
        card = self
        fades = [FadeOut(m) for m in (self.header, self.subtitle) if len(m.get_family()) > 1 or m.has_points()]

        class _Dock(AnimationGroup):
            def clean_up_from_scene(self, scene):
                super().clean_up_from_scene(scene)
                for m in (card.header, card.subtitle):
                    card.remove(m)
                    scene.remove(m)
                card.header, card.subtitle = VGroup(), VGroup()

        return _Dock(Transform(self.frame, fr), Transform(self.question, q), *fades, run_time=run_time)


class TipCard(VGroup):
    """Smaller side card with a DIM frame and a "TIP" header.

    ``TipCard(body="", title="TIP", width=5, height=None, accent=DIM, font_size=26,
    icon=None)``.  ``body`` is a string (wrapped) or any Mobject.
    Parts: ``frame``, ``header``, ``body``, ``icon``.  ``content_center()`` gives the
    middle of the body area for custom content.
    ``slide_in(direction=RIGHT)`` / ``slide_out(direction=RIGHT)`` animations.
    """

    TITLE = "TIP"

    def __init__(self, body="", title=None, width=5.0, height=None, accent=DIM, font_size=26,
                 icon=None, **kwargs):
        super().__init__(**kwargs)
        title = title or self.TITLE
        self.header = Text(title, font=FONT, font_size=22, color=accent if accent != DIM else TEXT,
                           weight=BOLD)
        if isinstance(body, str):
            self.body = centered_text(body, width - 0.7, font_size, TEXT, line_buff=0.08) if body else VGroup()
        else:
            self.body = body
        self.icon = icon if icon is not None else VGroup()
        hb = self.body.height if len(self.body.get_family()) > 1 or len(self.body.points) else 0
        h = height or (0.45 + 0.35 + hb + 0.5)
        self.frame = RoundedRectangle(width=width, height=h, corner_radius=0.2)
        self.frame.set_fill(CARD_FILL, 1).set_stroke(accent, 3)
        self.header.move_to(self.frame.get_corner(UL) + np.array([0.3, -0.32, 0]), aligned_edge=LEFT)
        if icon is not None:
            self.icon.scale_to_fit_height(min(self.icon.height, 0.4))
            self.icon.next_to(self.header, RIGHT, buff=0.15)
        rule = Line(self.frame.get_corner(UL) + np.array([0.25, -0.62, 0]),
                    self.frame.get_corner(UR) + np.array([-0.25, -0.62, 0]))
        rule.set_stroke(accent, 1.5, opacity=0.7)
        self.rule = rule
        self.body.move_to(self.content_center())
        self.add(self.frame, rule, self.header, self.icon, self.body)

    def content_center(self):
        top = self.frame.get_top()[1] - 0.62
        bot = self.frame.get_bottom()[1]
        return np.array([self.frame.get_center()[0], (top + bot) / 2, 0])

    def slide_in(self, direction=RIGHT, run_time=0.8):
        return FadeIn(self, shift=-np.array(direction) * 1.5, run_time=run_time)

    def slide_out(self, direction=RIGHT, run_time=0.6):
        return FadeOut(self, shift=np.array(direction) * 1.5, run_time=run_time)


class AsideCard(TipCard):
    """Same as TipCard with an "ASIDE" header."""
    TITLE = "ASIDE"


# ---------------------------------------------------------------------------
# Term highlight
# ---------------------------------------------------------------------------
def scrim(opacity=0.88, z_index=SCRIM_Z):
    """Full-frame BG veil that dims everything below ``z_index`` (marked ``is_scrim``,
    so the overlap check ignores text underneath it)."""
    s = Rectangle(width=config.frame_width + 1, height=config.frame_height + 1, stroke_width=0)
    s.set_fill(BG, opacity).set_z_index(z_index)
    s.is_scrim = True
    return s


_make_scrim = scrim   # TermHighlight.show has a ``scrim`` flag that shadows the name


class TermHighlight:
    """Manager for the bible's term highlight (not a mobject itself).

    ``terms = TermHighlight(accent=VIRT)`` then, in a scene::

        self.play(terms.show("process"))            # KEY term: veil, write big at center, dock
        self.play(terms.note("PCB"))                # secondary term: just slides into the dock
        self.play(terms.show("easy to use", dock=False))   # write big, then fade
        self.play(terms.show("trap", size=40))      # "(smaller)" variants

    ``show(term, hold=1.2, dock=True, size=54, at=(0, 0.3), scrim=True)`` returns one
    Succession.  By default the term gets its own moment: a scrim veils the whole scene,
    the term is written big at screen center above it, then the scrim lifts while the term
    docks.  So it can never collide with whatever the scene has on screen.  Pass
    ``scrim=False`` only when the area at ``at`` is known to be empty.
    The docked term replaces the previous docked one at top-right ``(6.6, 3.6)``
    (right-aligned, font 26, at most ``dock_max_width`` wide so it never reaches the crux strip).
    Also: ``write(term)``, ``dock_anim()``, ``fade_anim()`` for manual control, ``clear()``
    (fades the docked term), ``set_accent(color)``, attributes ``big`` and ``docked``.
    """

    def __init__(self, accent=VIRT, at=(0, 0.3, 0), size=54, dock_at=(6.6, CHROME_ROW_Y, 0),
                 dock_size=26, dock_max_width=2.6):
        self.accent = accent
        self.at = np.array(at, dtype=float)
        self.size = size
        self.dock_at = np.array(dock_at, dtype=float)
        self.dock_size = dock_size
        self.dock_max_width = dock_max_width
        self.big = None
        self.docked = None

    def set_accent(self, color):
        self.accent = color
        return self

    def _make(self, term, size, accent, at=None, right_aligned=False, max_width=None):
        # the docked (right-aligned) form always obeys dock_max_width, however it is built (the
        # animations, or a scene's "starts with" builder), so the term never changes size at a cut
        if max_width is None:
            max_width = self.dock_max_width if right_aligned else 12
        t = Text(term, font=FONT, font_size=size, color=TEXT)
        if t.width > max_width:
            t.scale_to_fit_width(max_width)
        ul = Line(LEFT, RIGHT).set_width(t.width + size * 0.006)
        ul.next_to(t, DOWN, buff=size * 0.0025 + 0.06).set_stroke(accent, max(2, size / 9))
        g = VGroup(t, ul)
        if right_aligned:
            tag_role(g, "chrome")       # the docked term is chrome (the big one sits on a scrim)
            g.move_to(at, aligned_edge=RIGHT)
        else:
            g.move_to(at)
        return g

    def write(self, term, size=None, at=None, accent=None):
        size = size or self.size
        at = self.at if at is None else np.array(at, dtype=float)
        self.big = self._make(term, size, accent or self.accent, at).set_z_index(SCRIM_Z + 1)
        self._term = term
        self._term_accent = accent or self.accent
        return AnimationGroup(Write(self.big[0]), Create(self.big[1]), run_time=0.8)

    def dock_anim(self):
        target = self._make(self._term, self.dock_size, self._term_accent, self.dock_at,
                            right_aligned=True, max_width=self.dock_max_width)
        anims = [Transform(self.big, target)]
        if self.docked is not None:
            anims.append(FadeOut(self.docked, shift=UP * 0.3))
        self.docked, self.big = self.big, None
        return AnimationGroup(*anims, run_time=0.8)

    def fade_anim(self):
        b, self.big = self.big, None
        return FadeOut(b, shift=UP * 0.2, run_time=0.5)

    def docked_now(self, term, accent=None):
        """The docked term, built instantly (for a scene's "starts with" state; the caller adds
        it).  Identical to what ``show``/``note`` leave behind, so a scene that starts from it
        continues the previous one exactly."""
        self._term, self._term_accent = term, accent or self.accent
        self.docked = self._make(term, self.dock_size, self._term_accent, self.dock_at,
                                 right_aligned=True, max_width=self.dock_max_width)
        return self.docked

    def note(self, term, accent=None, run_time=0.8):
        """Secondary term: slides straight into the docked slot (no veil, no big write).
        Use for every term except the episode's few key terms (those get ``show``)."""
        self._term, self._term_accent = term, accent or self.accent
        target = self._make(term, self.dock_size, self._term_accent, self.dock_at,
                            right_aligned=True, max_width=self.dock_max_width)
        anims = [FadeIn(target, shift=DOWN * 0.2)]
        if self.docked is not None:
            anims.append(FadeOut(self.docked, shift=UP * 0.3))
        self.docked = target
        return AnimationGroup(*anims, run_time=run_time)

    def show(self, term, hold=1.2, dock=True, size=None, at=None, accent=None, scrim=True):
        w = self.write(term, size=size, at=at, accent=accent)
        end = self.dock_anim() if dock else self.fade_anim()
        if not scrim:
            return Succession(w, Wait(hold), end)
        veil = _make_scrim()
        # the veil is fully up before the term is written, and lifts only once the term has
        # docked, so the big term never shares the screen with readable scene text.
        # Veil + write sit in one AnimationGroup (lag_ratio=1 = sequential): a Succession adds
        # all its mobjects at the start but begins Write only later, so the term would flash.
        return Succession(AnimationGroup(FadeIn(veil, run_time=0.4), w, lag_ratio=1),
                          Wait(hold), end, FadeOut(veil, run_time=0.4))

    def clear(self, run_time=0.5):
        d, self.docked = self.docked, None
        if d is None:
            return Wait(0.01)
        return FadeOut(d, run_time=run_time)


# ---------------------------------------------------------------------------
# Section badge
# ---------------------------------------------------------------------------
class SectionBadge(VGroup):
    """Small top-left tag: accent dot + text, e.g. ``SectionBadge("04 · The Process")``.

    ``SectionBadge(text, accent=VIRT, font_size=22, corner=(-6.6, 3.6))``: placed
    left-aligned at ``corner``.  Parts: ``dot``, ``text``.
    ``recolor(accent)`` returns an animation changing the dot color.
    """

    def __init__(self, text, accent=VIRT, font_size=22, corner=(-6.6, 3.6, 0), **kwargs):
        super().__init__(**kwargs)
        self.text = Text(text, font=FONT, font_size=font_size, color=DIM)
        self.dot = Dot(radius=0.08).set_fill(accent, 1).set_stroke(outline_of(accent, 0.4), 1.5)
        self.dot.next_to(self.text, LEFT, buff=0.15)
        self.add(self.dot, self.text)
        self.move_to(np.array(corner, dtype=float), aligned_edge=LEFT)
        self.accent = accent
        tag_role(self, "chrome")

    def recolor(self, accent, run_time=0.6):
        self.accent = accent
        return self.dot.animate(run_time=run_time).set_fill(accent, 1).set_stroke(outline_of(accent, 0.4))


# ---------------------------------------------------------------------------
# Illusion split
# ---------------------------------------------------------------------------
class IllusionSplit(VGroup):
    """The series' signature split: virtual vs physical.

    ``IllusionSplit(left_title="What each program sees", right_title="What really happens",
    orientation="vertical", at=0, title_size=28, color=DIM)``.

    * vertical: dashed divider at ``x = at`` (y ``top_y`` = CONTENT_TOP .. -3.6), titles
      centered over each half at ``title_y`` (default ``top_y - 0.3`` = 2.25, below the top band).
    * horizontal: divider at ``y = at`` (x -6.6 .. 6.6); ``left_title`` is the TOP
      half's title (left-aligned just under the top margin... placed at the
      top-left), ``right_title`` the BOTTOM half's (left-aligned just below the divider).

    Parts: ``divider``, ``left_title``, ``right_title``.  ``draw()`` animation,
    ``left_center()`` / ``right_center()`` (centers of the halves; top/bottom for
    horizontal), ``merge()`` animation (divider and titles fade, ready for the
    two halves to be merged by the caller).
    """

    def __init__(self, left_title="What each program sees", right_title="What really happens",
                 orientation="vertical", at=0.0, title_size=28, color=DIM,
                 top_y=CONTENT_TOP, bottom_y=-3.6, left_x=-6.6, right_x=6.6, title_y=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = orientation
        self.at = at
        self.bounds = (left_x, right_x, bottom_y, top_y)
        if orientation == "vertical":
            self.divider = DashedLine([at, top_y - 0.1, 0], [at, bottom_y, 0], dash_length=0.15)
        else:
            self.divider = DashedLine([left_x, at, 0], [right_x, at, 0], dash_length=0.15)
        self.divider.set_stroke(color, 3)
        self.left_title = Text(left_title, font=FONT, font_size=title_size, color=TEXT) if left_title else VGroup()
        self.right_title = Text(right_title, font=FONT, font_size=title_size, color=TEXT) if right_title else VGroup()
        title_y = top_y - 0.3 if title_y is None else title_y
        if orientation == "vertical":
            if left_title:
                self.left_title.move_to([(left_x + at) / 2, title_y, 0])
            if right_title:
                self.right_title.move_to([(right_x + at) / 2, title_y, 0])
        else:
            if left_title:
                self.left_title.move_to([left_x, top_y - 0.25, 0], aligned_edge=LEFT)
            if right_title:
                self.right_title.move_to([left_x, at - 0.35, 0], aligned_edge=LEFT)
        for t in (self.left_title, self.right_title):
            if len(t.points) or t.submobjects:
                t.set_color(TEXT)
        self.add(self.divider, self.left_title, self.right_title)

    def draw(self, run_time=1.2):
        return Succession(Create(self.divider, run_time=run_time * 0.6),
                          AnimationGroup(FadeIn(self.left_title, shift=DOWN * 0.15),
                                         FadeIn(self.right_title, shift=DOWN * 0.15),
                                         run_time=run_time * 0.4))

    def left_center(self):
        l, r, b, t = self.bounds
        if self.orientation == "vertical":
            return np.array([(l + self.at) / 2, (t + b) / 2, 0])
        return np.array([(l + r) / 2, (t + self.at) / 2, 0])

    def right_center(self):
        l, r, b, t = self.bounds
        if self.orientation == "vertical":
            return np.array([(r + self.at) / 2, (t + b) / 2, 0])
        return np.array([(l + r) / 2, (b + self.at) / 2, 0])

    def merge(self, run_time=1.0):
        return AnimationGroup(
            self.divider.animate(run_time=run_time).set_stroke(opacity=0).stretch(0.01, 1 if self.orientation == "vertical" else 0),
            FadeOut(self.left_title), FadeOut(self.right_title), run_time=run_time)


# ---------------------------------------------------------------------------
# Peach
# ---------------------------------------------------------------------------
class Peach(VGroup):
    """The physical peach (01-03 S07, 04 S06).  ``Peach(radius=0.55)``.

    Parts: ``body``, ``crease``, ``leaf``, ``stem``.
    ``virtual_copy(opacity=0.35)`` returns a translucent copy with a dashed outline.
    """

    def __init__(self, radius=0.55, **kwargs):
        super().__init__(**kwargs)
        r = radius
        body = Circle(radius=r).set_fill(PEACH_COLOR, 1).set_stroke(outline_of(PEACH_CREASE, 0.35), 4 * r / 0.55)
        blush = Ellipse(width=r * 0.9, height=r * 0.7).move_to([r * 0.25, -r * 0.2, 0])
        blush.set_fill(mix(PEACH_COLOR, "#FF6F61", 0.5), 0.45).set_stroke(width=0)
        shine = Ellipse(width=r * 0.35, height=r * 0.2).rotate(0.6).move_to([-r * 0.45, r * 0.45, 0])
        shine.set_fill("#FFFFFF", 0.4).set_stroke(width=0)
        crease = ArcBetweenPoints([-r * 0.05, r * 0.95, 0], [r * 0.12, -r * 0.6, 0], angle=-0.9)
        crease.set_stroke(PEACH_CREASE, 3.5 * r / 0.55).set_fill(opacity=0)
        stem = Line([0, r * 0.92, 0], [r * 0.06, r * 1.2, 0]).set_stroke("#7A4E2D", 4 * r / 0.55)
        top = np.array([r * 0.06, r * 1.12, 0])
        tip = top + np.array([r * 0.62, r * 0.28, 0])
        a1 = ArcBetweenPoints(top, tip, angle=0.9)
        a2 = ArcBetweenPoints(tip, top, angle=0.9)
        leaf = VMobject()
        leaf.set_points(np.concatenate([a1.points, a2.points]))
        leaf.set_fill(PERS, 1).set_stroke(outline_of(PERS), 2.5 * r / 0.55)
        vein = Line(top, top + (tip - top) * 0.8).set_stroke(outline_of(PERS, 0.3), 1.5)
        self.body, self.crease, self.leaf, self.stem = body, crease, VGroup(leaf, vein), stem
        self.add(body, blush, shine, crease, stem, self.leaf)

    def virtual_copy(self, opacity=0.35):
        c = self.copy()
        for sm in c.get_family():
            if isinstance(sm, VMobject):
                sm.set_fill(opacity=sm.get_fill_opacity() * opacity, family=False)
                sm.set_stroke(opacity=0.5, family=False)
        dashed = DashedVMobject(Circle(radius=self.body.width / 2).move_to(self.body), num_dashes=22)
        dashed.set_stroke(PEACH_COLOR, 3)
        c.submobjects[0].set_stroke(opacity=0)
        c.add(dashed)
        return c


# ---------------------------------------------------------------------------
# Icons
# ---------------------------------------------------------------------------
class FileIcon(VGroup):
    """Page with a folded corner and a few text lines.

    ``FileIcon(name=None, color=DIM, width=0.6, lines=3, font_size=18, mono=True)``.
    The name is shown under the page.  Parts: ``page``, ``fold``, ``lines``, ``label``.
    """

    def __init__(self, name=None, color=DIM, width=0.6, lines=3, font_size=18, mono=True,
                 fill_opacity=1.0, **kwargs):
        super().__init__(**kwargs)
        w, h, f = width, width * 1.3, width * 0.3
        pts = [[-w / 2, h / 2, 0], [w / 2 - f, h / 2, 0], [w / 2, h / 2 - f, 0],
               [w / 2, -h / 2, 0], [-w / 2, -h / 2, 0]]
        page = Polygon(*pts).set_fill(mix(color, BG, 0.55), fill_opacity).set_stroke(color, 3)
        fold = Polygon([w / 2 - f, h / 2, 0], [w / 2 - f, h / 2 - f, 0], [w / 2, h / 2 - f, 0])
        fold.set_fill(mix(color, BG, 0.2), fill_opacity).set_stroke(color, 2)
        ls = VGroup()
        for k in range(lines):
            y = h / 2 - f - 0.12 * w / 0.6 - k * (h - f - 0.25) / max(lines, 1)
            ls.add(Line([-w / 2 + 0.1 * w / 0.6, y, 0], [w / 2 - 0.12 * w / 0.6 - (0.1 if k == lines - 1 else 0), y, 0]))
        ls.set_stroke(color, 2)
        self.page, self.fold, self.lines = page, fold, ls
        self.add(page, fold, ls)
        self.label = VGroup()
        if name:
            self.label = Text(name, font=MONO_FONT if mono else FONT, font_size=font_size, color=TEXT)
            self.label.next_to(page, DOWN, buff=0.08)
            self.add(self.label)


class ClockIcon(VGroup):
    """Small clock face.  ``ClockIcon(radius=0.3, color=TEXT)``.
    ``spin(turns=1, run_time=1)`` returns an animation turning the minute hand."""

    def __init__(self, radius=0.3, color=TEXT, **kwargs):
        super().__init__(**kwargs)
        face = Circle(radius=radius).set_fill("#2A2A2A", 1).set_stroke(color, 3)
        ticks = VGroup(*[Line(radius * 0.78 * np.array([np.cos(a), np.sin(a), 0]),
                              radius * 0.95 * np.array([np.cos(a), np.sin(a), 0]))
                         for a in np.arange(0, TAU, TAU / 4)]).set_stroke(color, 2)
        self.minute = Line(ORIGIN, UP * radius * 0.72).set_stroke(color, 3)
        self.hour = Line(ORIGIN, RIGHT * radius * 0.45).set_stroke(color, 3)
        self.face = face
        self.add(face, ticks, self.hour, self.minute)

    def spin(self, turns=1.0, run_time=1.0, **kw):
        return Rotate(self.minute, -TAU * turns, about_point=self.face.get_center(),
                      run_time=run_time, rate_func=kw.pop("rate_func", linear), **kw)


class Spotlight(VGroup):
    """A lamp with a translucent cone of light and a pool on the floor.

    ``Spotlight(height=2.5, spread=0.7, color="#FFF3B0")``: the lamp sits ``height``
    above the pool.  ``move_beam_to(point)`` moves it so the pool is centered on
    ``point`` (returns self, so ``spot.animate.move_beam_to(p)`` works).
    ``pool_center()``.  Parts: ``lamp``, ``beam``, ``pool``.
    """

    def __init__(self, height=2.5, spread=0.7, color="#FFF3B0", **kwargs):
        super().__init__(**kwargs)
        top = UP * height
        lamp = Polygon(top + LEFT * 0.18 + UP * 0.18, top + RIGHT * 0.18 + UP * 0.18,
                       top + RIGHT * 0.28 + DOWN * 0.08, top + LEFT * 0.28 + DOWN * 0.08)
        lamp.set_fill("#555555", 1).set_stroke(INK, 3)
        beam = Polygon(top + LEFT * 0.24 + DOWN * 0.08, top + RIGHT * 0.24 + DOWN * 0.08,
                       RIGHT * spread, LEFT * spread)
        beam.set_fill(color, 0.22).set_stroke(width=0)
        pool = Ellipse(width=2 * spread, height=0.4 * spread).set_fill(color, 0.35).set_stroke(color, 1.5, 0.6)
        self.lamp, self.beam, self.pool = lamp, beam, pool
        self.add(beam, pool, lamp)

    def pool_center(self):
        return self.pool.get_center()

    def move_beam_to(self, point):
        self.shift(np.array(point, dtype=float) - self.pool_center())
        return self


def _gear(radius, teeth, color):
    pts = []
    n = teeth * 4
    for k in range(n):
        a = TAU * k / n
        r = radius if (k % 4) in (0, 1) else radius * 0.78
        pts.append([r * np.cos(a), r * np.sin(a), 0])
    g = Polygon(*pts).set_fill(color, 1).set_stroke(outline_of(color), 3)
    hole = Circle(radius=radius * 0.25).set_fill(BG, 1).set_stroke(outline_of(color), 3)
    return VGroup(g, hole)


class GearPair(VGroup):
    """Two meshing gears (the 'mechanism' icon).

    ``GearPair(radius=0.6, color="#B8B8B8")``; parts ``big``, ``small``.
    ``spin(angle=TAU, run_time=2)`` returns an animation turning both (in opposite
    directions, at the right ratio)."""

    def __init__(self, radius=0.6, color="#B8B8B8", **kwargs):
        super().__init__(**kwargs)
        self.r1, self.r2 = radius, radius * 0.6
        self.big = _gear(self.r1, 12, color)
        self.small = _gear(self.r2, 8, lighter(color, 0.15))
        self.small.move_to(self.big.get_center() + np.array([1, 0.55, 0]) / np.linalg.norm([1, 0.55]) * (self.r1 + self.r2) * 0.9)
        self.small.rotate(PI / 8)
        self.add(self.big, self.small)

    def spin(self, angle=TAU, run_time=2.0, **kw):
        kw.setdefault("rate_func", linear)
        return AnimationGroup(
            Rotate(self.big, angle, about_point=self.big.get_center()),
            Rotate(self.small, -angle * self.r1 / self.r2, about_point=self.small.get_center()),
            run_time=run_time, **kw)


class PauseGlyph(VGroup):
    """Two rounded bars ⏸.  ``PauseGlyph(size=0.6, color=TEXT)``."""

    def __init__(self, size=0.6, color=TEXT, **kwargs):
        super().__init__(**kwargs)
        for x in (-0.22, 0.22):
            b = RoundedRectangle(width=size * 0.28, height=size, corner_radius=size * 0.08)
            b.move_to(RIGHT * x * size).set_fill(color, 1).set_stroke(outline_of(color, 0.6), 2)
            self.add(b)


class PlayGlyph(VGroup):
    """A right-pointing triangle ▶.  ``PlayGlyph(size=0.6, color=TEXT)``."""

    def __init__(self, size=0.6, color=TEXT, **kwargs):
        super().__init__(**kwargs)
        t = Polygon([-0.4 * size, 0.5 * size, 0], [0.5 * size, 0, 0], [-0.4 * size, -0.5 * size, 0])
        t.set_fill(color, 1).set_stroke(outline_of(color, 0.6), 2)
        self.add(t)


class Laptop(VGroup):
    """Laptop outline: screen + base.  ``Laptop(width=5, color=TEXT, stroke_width=3,
    fill_opacity=0.0, screen_color=BG)``.  Parts: ``lid``, ``screen``, ``base``.
    ``screen_center()``."""

    def __init__(self, width=5.0, color=TEXT, stroke_width=3, fill_opacity=0.0,
                 screen_color="#141414", **kwargs):
        super().__init__(**kwargs)
        w = width
        lid = RoundedRectangle(width=w * 0.8, height=w * 0.52, corner_radius=w * 0.03)
        lid.set_fill(mix(color, BG, 0.75), fill_opacity).set_stroke(color, stroke_width)
        screen = Rectangle(width=w * 0.72, height=w * 0.44).move_to(lid).set_fill(screen_color, fill_opacity)
        screen.set_stroke(color, max(1, stroke_width - 1), opacity=0.7)
        y0 = lid.get_bottom()[1]
        base = Polygon([-w * 0.42, y0, 0], [w * 0.42, y0, 0], [w * 0.5, y0 - w * 0.06, 0],
                       [-w * 0.5, y0 - w * 0.06, 0])
        base.set_fill(mix(color, BG, 0.75), fill_opacity).set_stroke(color, stroke_width)
        notch = Line([-w * 0.06, y0 - 0.005, 0], [w * 0.06, y0 - 0.005, 0]).set_stroke(color, stroke_width)
        self.lid, self.screen, self.base = lid, screen, base
        self.add(lid, screen, base, notch)

    def screen_center(self):
        return self.screen.get_center()
