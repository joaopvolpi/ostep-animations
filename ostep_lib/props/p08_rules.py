"""RuleBoard: an accumulating rulebook panel (tag chips "R1", "R2" ... plus one short line each).

    rb = RuleBoard()                       # right-hand panel, x 3.25..6.6, y 2.5 down
    rb.skeleton(5)                         # dim empty slots R1..R5 (placeholders)
    self.play(*rb.add("R1", "Higher priority runs."))
    self.play(rb.glow("R1"))                # flash the rule when it fires
    self.play(rb.merge(["R4a", "R4b"], "R4", "..."))   # the two lines slide together into one
    self.play(rb.warn())                    # red outline + cracks; rb.ok() = green outline
    rb.place_now([("R1", "..."), ...])      # instant build for a scene's "starts with" state

Rows are laid out by order (``row_h`` apart).  New rows are folded into the board group when
the animation ends, so ``FadeOut(rb)`` removes everything.
"""
from __future__ import annotations

import numpy as np
from manim import (
    Animation, AnimationGroup, FadeIn, FadeOut, Line, RoundedRectangle, Succession, Text, Transform,
    VGroup, Write, Wait, Indicate, Create, SurroundingRectangle, UP, DOWN, LEFT, RIGHT, ORIGIN,
)

from ..style import TEXT, DIM, VIRT, KERNEL_COLOR, PERS
from .core import CARD_FILL, wrap_text

OK_GREEN = "#8BE07A"


def _P(x, y=0.0):
    return np.array([float(x), float(y), 0.0])


class _Fold(AnimationGroup):
    """AnimationGroup that folds newly written mobjects into the board when it ends."""

    def __init__(self, board, row, fresh, *anims, old=None, **kw):
        super().__init__(*anims, **kw)
        self._board, self._row, self._fresh, self._old = board, row, fresh, old

    def clean_up_from_scene(self, scene):
        super().clean_up_from_scene(scene)
        for m in self._fresh:
            scene.remove(m)
        if self._old is not None and self._old in self._row.submobjects:
            self._row.remove(self._old)
        for m in self._fresh:
            if m not in self._row.submobjects:
                self._row.add(m)
        if self._row not in self._board.submobjects:
            self._board.add(self._row)


class RuleBoard(VGroup):
    def __init__(self, accent=VIRT, x_range=(3.2, 6.6), top=2.5, row_h=0.62, n_rows=6, font=16,
                 title="MLFQ rules", **kwargs):
        super().__init__(**kwargs)
        self.accent = accent
        self.x0, self.x1 = map(float, x_range)
        self.top, self.row_h, self.font = float(top), float(row_h), font
        self.n_rows = n_rows
        h = 0.55 + n_rows * row_h + 0.05
        self.frame = RoundedRectangle(width=self.x1 - self.x0, height=h, corner_radius=0.15)
        self.frame.set_fill(CARD_FILL, 1).set_stroke(DIM, 2).move_to(_P((self.x0 + self.x1) / 2, top - h / 2))
        self.frame.set_z_index(-1)   # stays below the rows even after .animate re-adds it
        self.header = Text(title, font_size=24, color=accent, weight="BOLD")
        self.header.move_to(_P((self.x0 + self.x1) / 2, top - 0.3))
        self.add(self.frame, self.header)
        self.order = []          # tags, top to bottom
        self.rows = {}           # tag -> VGroup(chip, body)   (body may be an empty VGroup)
        self.cracks = VGroup()

    # ------------------------------------------------------------ geometry
    def slot_y(self, k):
        return self.top - 0.55 - (k + 0.5) * self.row_h + 0.02

    def row_y(self, tag):
        return self.slot_y(self.order.index(tag))

    def _chip(self, tag, color):
        t = Text(tag, font_size=16, color=color, weight="BOLD")
        r = RoundedRectangle(width=max(0.5, t.width + 0.2), height=0.3, corner_radius=0.08)
        r.set_fill(CARD_FILL, 1).set_stroke(color, 2)
        g = VGroup(r, t)
        t.move_to(r)
        g.rect, g.txt = r, t
        return g

    def _body(self, text):
        return Text(wrap_text(text, self.x1 - self.x0 - 0.85, self.font), font_size=self.font, color=TEXT,
                    line_spacing=0.75)

    def _row(self, tag, text, k, color=None):
        chip = self._chip(tag, color or self.accent)
        chip.move_to(_P(self.x0 + 0.45, self.slot_y(k)))
        body = self._body(text) if text else VGroup()
        if text:
            body.move_to(_P(self.x0 + 0.88, self.slot_y(k)), aligned_edge=LEFT)
        row = VGroup(chip, body)
        row.chip, row.body = chip, body
        return row

    # ------------------------------------------------------------ building
    def skeleton(self, n=5):
        """Instantly add ``n`` dim placeholder slots R1..Rn (returns the group for animating)."""
        g = VGroup()
        for k in range(n):
            tag = f"R{k + 1}"
            row = self._row(tag, None, k, color=DIM)
            self.order.append(tag)
            self.rows[tag] = row
            self.add(row)
            g.add(row)
        return g

    def place_now(self, rules):
        for tag, text in rules:
            row = self._row(tag, text, len(self.order))
            self.order.append(tag)
            self.rows[tag] = row
            self.add(row)
        return self

    def add(self, *args, **kw):
        # VGroup.add must keep working for Manim internals; rule-adding uses (tag, text) strings.
        if len(args) == 2 and all(isinstance(a, str) for a in args):
            return self.add_rule(*args, **kw)
        return super().add(*args, **kw)

    def add_rule(self, tag, text, run_time=1.2):
        """Animations that write rule ``tag``.  Fills a placeholder if one exists."""
        holder = tag if tag in self.rows else ("R" + tag[1] if tag[:1] == "R" and len(tag) > 2 and ("R" + tag[1]) in self.rows else None)
        anims, fold = [], []
        if holder is not None and holder in self.rows and not len(self.rows[holder].body):
            row = self.rows[holder]
            new_chip = self._chip(tag, self.accent).move_to(row.chip)
            body = self._body(text)
            body.move_to(_P(self.x0 + 0.88, self.slot_y(self.order.index(holder))), aligned_edge=LEFT)
            anims.append(Transform(row.chip, new_chip, run_time=0.5))
            anims.append(Write(body, run_time=run_time))
            old = row.body
            row.body = body
            del self.rows[holder]
            self.order[self.order.index(holder)] = tag
            self.rows[tag] = row
            return _Fold(self, row, [body], *anims, old=old)
        # a new row at the end; if placeholders follow, push them down
        k = len(self.order)
        # insert before trailing empty placeholders
        pos = len(self.order)
        while pos > 0 and not len(self.rows[self.order[pos - 1]].body) and self.order[pos - 1] not in (tag,):
            pos -= 1
        k = pos
        for j in range(pos, len(self.order)):
            r = self.rows[self.order[j]]
            anims.append(r.animate.shift(DOWN * self.row_h))
        row = self._row(tag, text, k)
        self.order.insert(k, tag)
        self.rows[tag] = row
        anims.append(FadeIn(row.chip, run_time=0.4))
        anims.append(Write(row.body, run_time=run_time))
        return _Fold(self, row, [row.chip, row.body], *anims)

    # ------------------------------------------------------------ effects
    def glow(self, tag, color=None, run_time=1.2):
        """Flash the line of rule ``tag``."""
        row = self.rows[tag]
        box = RoundedRectangle(width=self.x1 - self.x0 - 0.2, height=self.row_h - 0.06, corner_radius=0.08)
        box.set_fill(color or self.accent, 0.22).set_stroke(color or self.accent, 2.5)
        box.move_to(_P((self.x0 + self.x1) / 2, row.chip.get_center()[1]))
        return Succession(FadeIn(box, run_time=0.25), Wait(max(run_time - 0.6, 0.1)), FadeOut(box, run_time=0.35))

    def hold_glow(self, tag, color=None):
        """A persistent highlight box (returned unadded); fade it out yourself."""
        row = self.rows[tag]
        box = RoundedRectangle(width=self.x1 - self.x0 - 0.2, height=self.row_h - 0.06, corner_radius=0.08)
        box.set_fill(color or self.accent, 0.2).set_stroke(color or self.accent, 2.5)
        box.move_to(_P((self.x0 + self.x1) / 2, row.chip.get_center()[1]))
        return box

    def set_dim(self, tags=None, opacity=0.35):
        tags = self.order if tags is None else tags
        return AnimationGroup(*[self.rows[t].animate.set_opacity(opacity) for t in tags])

    def outline(self, color, width=3.5):
        return self.frame.animate.set_stroke(color, width)

    def ok(self):
        return self.outline(OK_GREEN)

    def warn(self, run_time=1.0):
        """Red outline and crack lines across the panel."""
        cx = (self.x0 + self.x1) / 2
        cracks = VGroup()
        for (xa, ya, xb, yb) in ((0.3, 0.2, 0.7, -0.6), (-0.9, -0.9, -0.5, -1.6), (0.9, -1.2, 0.5, -2.0)):
            pts = [_P(cx + xa, self.top - 0.9 + ya), _P(cx + (xa + xb) / 2 + 0.12, self.top - 0.9 + (ya + yb) / 2),
                   _P(cx + (xa + xb) / 2 - 0.08, self.top - 0.9 + (ya + yb) / 2 - 0.2), _P(cx + xb, self.top - 0.9 + yb)]
            cracks.add(Line(pts[0], pts[1]), Line(pts[1], pts[2]), Line(pts[2], pts[3]))
        cracks.set_stroke(KERNEL_COLOR, 3)
        self.cracks = cracks
        return AnimationGroup(self.frame.animate.set_stroke(KERNEL_COLOR, 4), Create(cracks), run_time=run_time)

    def merge(self, tags_in, tag_out, text, run_time=1.4):
        """The rows ``tags_in`` (adjacent) slide together into a single row ``tag_out``."""
        a, b = tags_in
        ia, ib = self.order.index(a), self.order.index(b)
        ra, rb = self.rows[a], self.rows[b]
        new_chip = self._chip(tag_out, self.accent).move_to(ra.chip)
        new_body = self._body(text)
        new_body.move_to(_P(self.x0 + 0.88, self.slot_y(ia)), aligned_edge=LEFT)
        up = np.array([0, self.slot_y(ia) - self.slot_y(ib), 0])
        anims = [rb.animate(run_time=run_time * 0.5).shift(up).set_opacity(0.0),
                 Transform(ra.chip, new_chip, run_time=run_time),
                 Transform(ra.body, new_body, run_time=run_time)]
        # rows below move up by one
        for t in self.order[ib + 1:]:
            anims.append(self.rows[t].animate(run_time=run_time).shift(UP * self.row_h))
        self.order.remove(b)
        del self.rows[b]
        self.order[ia] = tag_out
        del self.rows[a]
        self.rows[tag_out] = ra
        return AnimationGroup(*anims)


__all__ = ["RuleBoard"]
