"""MetricReadout: the running-average expression ``\\frac{10+20+30}{3}=20``, built from
separate pieces so it can be written left to right, framed, and have an old value struck out.

    ro = MetricReadout(["10", "20", "30"], 3, "20", center=(0, -2.1))
    self.play(*ro.reveal_term(0))            # "10+" and the bar, the 3 below  -> \\frac{10+}{3}
    self.play(*ro.reveal_term(1))
    self.play(*ro.reveal_term(2))            # numerator complete
    self.play(*ro.reveal_value())            # "= 20"
    self.play(*ro.frame_value(good=True))    # value colored PERS + green box (False: red)
    self.play(*ro.strike(old="110"))         # old value written above, struck out in red
    self.play(ro.count_value(110, run_time=1.2))   # counts 110 -> value (integers)
    self.play(ro.fade_out())

Nothing is in the scene until revealed (``ro`` itself is only a layout holder; ``ro.shown`` is
the group of everything revealed so far).  ``terms`` are LaTeX strings (``"(110-10)"`` ok).
"""
from __future__ import annotations

import numpy as np
from manim import (
    AnimationGroup, Create, DecimalNumber, FadeIn, FadeOut, Line, MathTex, SurroundingRectangle,
    Succession, UpdateFromAlphaFunc, VGroup, Write, ReplacementTransform, RIGHT, LEFT, UP, DOWN,
)

from ..style import TEXT, DIM, PERS, KERNEL_COLOR


class MetricReadout(VGroup):
    """``MetricReadout(terms, denom, value, center=(0, -2.1), font_size=38, joiner="+",
    lead=None)``.  ``lead`` is an optional LaTeX prefix shown with the first reveal (e.g.
    ``r"\\text{avg}"``).  Parts: ``term_mobs``, ``plus_mobs``, ``bar``, ``denom_mob``,
    ``eq``, ``value_mob``, ``shown``."""

    def __init__(self, terms, denom, value, center=(0, -2.1, 0), font_size=38, joiner="+",
                 color=TEXT, **kwargs):
        super().__init__(**kwargs)
        self.font_size = font_size
        self.color = color
        self.value_str = str(value)
        self.terms_str = list(terms)
        self.term_mobs = [MathTex(t, font_size=font_size, color=color) for t in terms]
        self.plus_mobs = [MathTex(joiner, font_size=font_size, color=color) for _ in terms[:-1]]
        row = VGroup()
        for i, t in enumerate(self.term_mobs):
            row.add(t)
            if i < len(self.plus_mobs):
                row.add(self.plus_mobs[i])
        row.arrange(RIGHT, buff=0.08)
        self.bar = Line(LEFT, RIGHT).set_stroke(color, 3)
        self.bar.set_width(row.width + 0.25)
        self.denom_mob = MathTex(str(denom), font_size=font_size, color=color)
        row.move_to(ORIGIN_3)
        self.bar.next_to(row, DOWN, buff=0.07)
        self.denom_mob.next_to(self.bar, DOWN, buff=0.1)
        self.eq = MathTex("=", font_size=font_size, color=color)
        self.eq.next_to(self.bar, RIGHT, buff=0.2)
        self.value_mob = MathTex(self.value_str, font_size=font_size, color=color)
        self.value_mob.next_to(self.eq, RIGHT, buff=0.2)
        self.row = row
        parts = VGroup(row, self.bar, self.denom_mob, self.eq, self.value_mob)
        c3 = np.array(list(center) + [0.0] * (3 - len(center)), dtype=float)
        parts.shift(c3 - parts.get_center())
        self.layout = parts
        self.shown = VGroup()
        self.extras = VGroup()
        self.box = None

    # ----------------------------------------------------------- reveal
    def reveal_term(self, i, run_time=0.6):
        """Animations showing term ``i`` (and its ``+``); the first call also shows the bar and
        the denominator."""
        mobs = [self.term_mobs[i]]
        if i < len(self.plus_mobs):
            mobs.append(self.plus_mobs[i])
        anims = []
        if len(self.shown) == 0:
            mobs += [self.bar, self.denom_mob]
        for m in mobs:
            self.shown.add(m)
            anims.append(Write(m) if m is not self.bar else Create(m))
        return [AnimationGroup(*anims, run_time=run_time)]

    def reveal_numerator(self, run_time=1.0):
        mobs = [self.row, self.bar, self.denom_mob]
        self.shown.add(*self.term_mobs, *self.plus_mobs, self.bar, self.denom_mob)
        return [AnimationGroup(Write(self.row), Create(self.bar), Write(self.denom_mob), run_time=run_time)]

    def reveal_value(self, run_time=0.8):
        self.shown.add(self.eq, self.value_mob)
        return [AnimationGroup(Write(self.eq), Write(self.value_mob), run_time=run_time, lag_ratio=0.4)]

    def show_all(self):
        """Instantly return everything revealed (for scene starts). Returns ``shown``."""
        self.shown.add(*self.term_mobs, *self.plus_mobs, self.bar, self.denom_mob, self.eq, self.value_mob)
        return self.shown

    # ----------------------------------------------------------- emphasis
    def frame_value(self, good=True, run_time=0.6):
        col = PERS if good else KERNEL_COLOR
        self.box = SurroundingRectangle(self.value_mob, color=col, buff=0.14, corner_radius=0.08).set_stroke(col, 4)
        self.shown.add(self.box)
        return [self.value_mob.animate(run_time=run_time).set_color(col), Create(self.box, run_time=run_time)]

    def frame_now(self, good=True):
        """Instant version of ``frame_value`` (for scene start states). Returns the box."""
        col = PERS if good else KERNEL_COLOR
        self.value_mob.set_color(col)
        self.box = SurroundingRectangle(self.value_mob, color=col, buff=0.14, corner_radius=0.08).set_stroke(col, 4)
        self.shown.add(self.box)
        return self.box

    def strike(self, old, color=KERNEL_COLOR, run_time=0.8):
        """Write the old value above the current one and strike it out."""
        o = MathTex(str(old), font_size=self.font_size, color=DIM)
        o.next_to(self.value_mob, UP, buff=0.5)
        ln = Line(o.get_corner(np.array([-1, -1, 0])) + LEFT * 0.08, o.get_corner(np.array([1, 1, 0])) + RIGHT * 0.08)
        ln.set_stroke(color, 4)
        self.old_mob, self.old_strike = o, ln
        self.shown.add(o, ln)
        return [FadeIn(o, shift=UP * 0.2, run_time=run_time * 0.5), Succession(
            FadeIn(VGroup(), run_time=run_time * 0.4), Create(ln, run_time=run_time * 0.6))]

    def count_value(self, start, run_time=1.2, color=None):
        """Animation: the value counts from ``start`` to the final value (integers)."""
        end = float(self.value_str)
        place = self.value_mob.get_center()
        dec = DecimalNumber(start, num_decimal_places=0, font_size=self.font_size, color=color or self.color)
        dec.move_to(place)
        old = self.value_mob
        self.value_mob = dec
        self.shown.remove(old)
        self.shown.add(dec)

        def upd(m, a):
            m.set_value(round(start + (end - start) * a))
            m.move_to(place)
        return Succession(FadeIn(dec, run_time=0.2), UpdateFromAlphaFunc(dec, upd, run_time=run_time, suspend_mobject_updating=False))

    def fade_out(self, run_time=0.6):
        return FadeOut(self.shown, run_time=run_time)


ORIGIN_3 = np.zeros(3)

__all__ = ["MetricReadout"]
