"""Shape-aware overlap check for rendered scenes (``NarratedScene`` runs it when OSTEP_CHECK=1).

It rasterizes what is actually drawn (opaque fills, strokes and text glyphs, in draw order) on a
coarse grid and reports the overlaps that are almost always mistakes:

* ``cover``   a text is partly hidden by something drawn on top of it (a card, a CPU's pins,
              a highlight box's border, an arrow...).
* ``text``    two texts on top of each other.
* ``line``    a text sits on a line or border (an arrow, a box edge, a dashed boundary).
* ``edge``    a text straddles the edge of a filled shape (half on a card, half off it).
* ``chrome``  something touches the chrome (crux strip / card, section badge, docked term).
* ``host``    something touches the Student or the Professor.
* ``panel``   two panels (cards, code blocks, terminals, filled boxes) partly overlap, or an
              actor / prop partly overlaps a panel.
* ``spill``   a card's own text (its title, a label) sticks out past the card's outer edge.
* ``zone:chrome`` / ``zone:host``  content inside the reserved zone around the chrome or a host:
              a thin margin (``ZONE_MARGIN``) around their actual drawn shape, only while they are
              on screen (for hosts: panels, creatures and props only; a "?" over the head is fine).
              Touching them is reported as ``chrome`` / ``host`` instead.

Ignored on purpose: parts of the same unit (a character, a CPU, a card, a text), an object
sitting entirely on a panel drawn below it (a creature on a card, a card on a big background
band), semi-transparent fills (highlight bars), anything under an opaque scrim, and overlaps that
last less than ``HOLD`` seconds (things passing each other in motion).

A deliberate overlap is declared in the scene with ``self.allow_overlap(a, b, why)``.

Units and roles: a unit is a mobject whose parts are never checked against each other.  Text
mobjects are units; so is any mobject with a role.  Roles come from classes (``Student`` /
``Professor`` = host, ``CruxCard`` / ``SectionBadge`` = chrome, ``Character`` = actor, ``CPU`` /
``Disk`` / ``Memory`` = prop, ``Code`` / ``Terminal`` / cards = panel) or from an ``ostep_role``
attribute ("chrome", "host", "panel", "actor", "prop", "background", "ignore").  Everything else
is split into its leaves.  Texts inside a unit are still checked against other units.
"""
from __future__ import annotations

import json
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from manim import DecimalNumber, MarkupText, MathTex, Paragraph, SingleStringMathTex, Text, VMobject, config
from manim.utils.family import extract_mobject_family_members

RES = 0.025                 # grid cell, in frame units
HOLD = 0.25                 # an overlap must last this long (2 samples at 4 Hz) to count
OPAQUE = 0.5                # fill / stroke opacity that hides what's below
BACKGROUND_AREA = 40.0      # a filled shape bigger than this (units^2) is a background band
PANEL_AREA = 0.6            # a filled box at least this big is a panel
TEXT_FRAC = 0.04            # share of a text's pixels that must be hit
SHAPE_FRAC = 0.03           # share of the smaller shape's pixels that must be hit
CONTAIN = 0.97              # "entirely on top of" threshold
ZONE_MARGIN = 0.1           # reserved margin around chrome and hosts (units)
ZONE_PX = 4                 # pixels of content inside a zone that count

TEXT_TYPES = (Text, MarkupText, SingleStringMathTex, MathTex, DecimalNumber, Paragraph)
ROLE_CLASSES = (
    ({"Student", "Professor"}, "host"),
    ({"CruxCard", "SectionBadge"}, "chrome"),
    ({"Bubble"}, "bubble"),
    ({"Character"}, "actor"),
    ({"CPU", "Disk", "Memory"}, "prop"),
    ({"Code", "Terminal", "MenuCard", "TipCard", "PCBCard"}, "panel"),
)


def _role_of(m):
    r = getattr(m, "ostep_role", None)
    if r:
        return r
    if getattr(m, "is_scrim", False):
        return "ignore"
    names = {c.__name__ for c in type(m).__mro__}
    for classes, role in ROLE_CLASSES:
        if names & classes:
            return role
    return None


class Unit:
    def __init__(self, root, role, is_text, group=None):
        self.root, self.role, self.is_text = root, role, is_text
        self.group = group        # the role unit a text belongs to (its parts aren't checked against it)
        self.leaves = []          # (leaf, is_text)
        self.order = 10 ** 9


def _units(scene, veil_z):
    """Split what's on screen into units.  Every text is its own unit (so a highlight box over
    one row of a card is judged against that row); a text inside a role unit keeps that unit as
    its ``group``.  Other leaves belong to their role unit, or are units of their own."""
    owner = {}

    def walk(m, unit):
        if id(m) in owner:
            return
        role = _role_of(m)
        if role == "ignore":
            owner[id(m)] = None
            return
        if isinstance(m, TEXT_TYPES):
            group = unit.group or unit if unit is not None else None
            if unit is None or not unit.is_text:
                unit = Unit(m, group.role if group else role, True, group)
        elif unit is None and role is not None:
            unit = Unit(m, role, False)
        owner[id(m)] = unit
        for sm in m.submobjects:
            walk(sm, unit)
        if unit is None and not m.submobjects and isinstance(m, VMobject):
            owner[id(m)] = Unit(m, None, False)

    for m in scene.mobjects:
        walk(m, None)
    order = extract_mobject_family_members(scene.mobjects, use_z_index=True, only_those_with_points=True)
    units = {}
    for i, leaf in enumerate(order):
        u = owner.get(id(leaf))
        if u is None or not isinstance(leaf, VMobject):
            continue
        if veil_z is not None and leaf.z_index <= veil_z:
            continue
        u.leaves.append((leaf, u.is_text))
        u.order = min(u.order, i)
        units[id(u)] = u
    return list(units.values())


# ---------------------------------------------------------------------------
# rasterizing (cached per leaf: most leaves don't change between samples)
# ---------------------------------------------------------------------------
_CACHE = {}


def _px(p):
    fw, fh = config.frame_width, config.frame_height
    return np.column_stack(((p[:, 0] + fw / 2) / RES, (fh / 2 - p[:, 1]) / RES))


def _curves(sm):
    """Polylines (pixel coordinates) approximating each subpath: Beziers sampled at t = 0, 1/2."""
    pts = sm.points
    n = len(pts) // 4 * 4
    if n == 0:
        return []
    b = pts[:n].reshape(-1, 4, 3)
    mid = (b[:, 0] + 3 * b[:, 1] + 3 * b[:, 2] + b[:, 3]) / 8
    # a new subpath starts where a curve doesn't begin at the previous curve's end
    breaks = np.where(np.linalg.norm(b[1:, 0] - b[:-1, 3], axis=1) > 1e-6)[0] + 1
    out = []
    for seg in np.split(np.arange(len(b)), breaks):
        p = np.empty((len(seg) * 2 + 1, 2))
        p[0:-1:2], p[1:-1:2], p[-1] = b[seg, 0, :2], mid[seg, :2], b[seg[-1], 3, :2]
        out.append(_px(np.column_stack((p, np.zeros(len(p))))))
    return out


def _leaf_raster(sm, as_text):
    """(x0, y0, mask, kind) or None; kind is 'fill', 'text' or 'stroke' (a leaf may give two)."""
    fo = float(sm.get_fill_opacity()) if len(sm.get_fill_opacities()) else 0.0
    so = float(sm.get_stroke_opacity()) if len(sm.get_stroke_opacities()) else 0.0
    sw = float(sm.get_stroke_width() or 0)
    want_fill, want_stroke = fo >= OPAQUE, so >= OPAQUE and sw > 0
    if not (want_fill or want_stroke) or not len(sm.points):
        return []
    key = (id(sm), hash(sm.points.tobytes()), want_fill, want_stroke, round(sw, 2), as_text)
    hit = _CACHE.get(key)
    if hit is not None:
        return hit
    curves = _curves(sm)
    out = []
    if curves:
        allp = np.vstack(curves)
        width = max(1, int(round(sw * 0.01 / RES)))
        pad = width + 2
        x0, y0 = np.floor(allp.min(axis=0)).astype(int) - pad
        x1, y1 = np.ceil(allp.max(axis=0)).astype(int) + pad
        w, h = int(x1 - x0), int(y1 - y0)
        if 0 < w < 4000 and 0 < h < 4000:
            off = np.array([x0, y0])
            if want_fill:
                img = Image.new("1", (w, h), 0)
                d = ImageDraw.Draw(img)
                for c in curves:
                    if len(c) >= 3:
                        d.polygon([tuple(p) for p in c - off], fill=1)
                out.append((int(x0), int(y0), np.asarray(img, dtype=bool), "text" if as_text else "fill"))
            if want_stroke:
                img = Image.new("1", (w, h), 0)
                d = ImageDraw.Draw(img)
                for c in curves:
                    d.line([tuple(p) for p in c - off], fill=1, width=width)
                out.append((int(x0), int(y0), np.asarray(img, dtype=bool), "text" if as_text else "stroke"))
    if len(_CACHE) > 20000:
        _CACHE.clear()
    _CACHE[key] = out
    return out


def _rasterize(u):
    parts = [r for leaf, txt in u.leaves for r in _leaf_raster(leaf, txt)]
    if not parts:
        return False
    x0 = min(p[0] for p in parts)
    y0 = min(p[1] for p in parts)
    x1 = max(p[0] + p[2].shape[1] for p in parts)
    y1 = max(p[1] + p[2].shape[0] for p in parts)
    u.box = (x0, y0, x1, y1)
    masks = {k: np.zeros((y1 - y0, x1 - x0), dtype=bool) for k in ("fill", "stroke", "text")}
    for px, py, m, kind in parts:
        masks[kind][py - y0: py - y0 + m.shape[0], px - x0: px - x0 + m.shape[1]] |= m
    u.fill, u.stroke, u.text = masks["fill"], masks["stroke"], masks["text"]
    u.shape = u.fill | u.stroke
    u.all = u.shape | u.text
    u.n_text, u.n_all = int(u.text.sum()), int(u.all.sum())
    return u.n_all > 0


def _effective_role(u):
    if u.role in ("chrome", "host", "panel", "actor", "prop", "background", "bubble"):
        return u.role
    if u.is_text:
        return "chrome" if u.role == "chrome" else "text"
    area = u.fill.sum() * RES * RES
    if area >= BACKGROUND_AREA:
        return "background"
    if area >= PANEL_AREA:
        return "panel"
    return "other"


# ---------------------------------------------------------------------------
# the rules
# ---------------------------------------------------------------------------
def _judge(a, b, ra, rb, cut):
    """Kind of the problem between a (drawn below) and b (drawn above), or None."""
    if "background" in (ra, rb):
        return None
    at, bt = cut(a, a.text), cut(b, b.text)
    if a.n_text and b.n_text:
        ov = (at & bt).sum()
        if ov > TEXT_FRAC * min(a.n_text, b.n_text):
            # the same text drawn twice in the same place looks like one text: not a problem
            if _text_of(a) == _text_of(b) and ov > 0.85 * max(a.n_text, b.n_text):
                return None
            return "text"
    if a.n_text and (at & cut(b, b.shape)).sum() > TEXT_FRAC * a.n_text:
        return "cover"
    if b.n_text and (bt & cut(a, a.stroke)).sum() > TEXT_FRAC * b.n_text:
        return "line"
    if b.n_text and a.fill.any():
        # a text half on a filled shape, half off it (straddling its edge)
        on = (bt & cut(a, a.fill)).sum() / b.n_text
        if TEXT_FRAC < on < 1 - TEXT_FRAC:
            return "edge"
    pair = {ra, rb}
    ov = (cut(a, a.all) & cut(b, b.all)).sum()
    small = min(a.n_all, b.n_all)
    if not small:
        return None
    # touching the chrome or a host shows even when small next to the other shape: an absolute floor
    if ov >= ZONE_PX:
        if "chrome" in pair and pair != {"chrome"}:
            return "chrome"
        if "host" in pair and pair != {"host"} and "bubble" not in pair:
            return "host"
    if ov <= SHAPE_FRAC * small:
        return None
    contained = b.n_all <= a.n_all and ov >= CONTAIN * b.n_all      # b sits entirely on a
    if pair in ({"panel"}, {"panel", "actor"}, {"panel", "prop"}) and not contained:
        return "panel"
    return None


def _morphing(scene):
    """ids of mobjects being morphed by a running Transform (their shapes are transient)."""
    from manim import Transform
    ids = set()
    for anim in getattr(scene, "animations", None) or []:
        stack = [anim]
        while stack:
            a = stack.pop()
            stack.extend(getattr(a, "animations", []))
            if isinstance(a, Transform):
                ids.update(id(x) for x in a.mobject.get_family())
    return ids


def _text_of(u):
    return str(getattr(u.root, "text", None) or getattr(u.root, "tex_string", None) or id(u.root))


def find_overlaps(scene, mid_play=False):
    """[(kind, unit_below, unit_above, pixel_box)] for the current frame."""
    veil_z = max((sm.z_index for m in scene.mobjects for sm in m.get_family()
                  if getattr(sm, "is_scrim", False) and sm.get_fill_opacity() >= 0.6), default=None)
    units = _units(scene, veil_z)
    if mid_play:
        busy = _morphing(scene)
        units = [u for u in units if id(u.root) not in busy]
    units = [u for u in units if _rasterize(u)]
    units.sort(key=lambda u: u.order)
    roles = [_effective_role(u) for u in units]
    allowed = getattr(scene, "_allowed_overlaps", [])
    found = []
    for i, a in enumerate(units):
        for j in range(i + 1, len(units)):
            b = units[j]
            x0, y0 = max(a.box[0], b.box[0]), max(a.box[1], b.box[1])
            x1, y1 = min(a.box[2], b.box[2]), min(a.box[3], b.box[3])
            if x1 <= x0 or y1 <= y0:
                continue
            if a.group is b or b.group is a or (a.group is not None and a.group is b.group):
                continue

            def cut(u, arr):
                return arr[y0 - u.box[1]: y1 - u.box[1], x0 - u.box[0]: x1 - u.box[0]]
            kind = _judge(a, b, roles[i], roles[j], cut)
            if kind and not _is_allowed(allowed, a, b):
                found.append((kind, a, b, (x0, y0, x1, y1)))
    # spill: a card's own text that straddles the card's outer edge (a title too long for its frame);
    # the pair loop skips a text and its own card, so check that edge here
    pos = {id(u): k for k, u in enumerate(units)}
    for i, t in enumerate(units):
        g = t.group
        if not t.is_text or g is None or id(g) not in pos or roles[pos[id(g)]] not in ("panel", "chrome"):
            continue
        gb, tb = g.box, t.box
        if (gb[2] - gb[0]) * (gb[3] - gb[1]) * RES * RES < PANEL_AREA:
            continue        # no real frame (a badge's dot, a term's underline)
        iw = min(gb[2], tb[2]) - max(gb[0], tb[0])
        ih = min(gb[3], tb[3]) - max(gb[1], tb[1])
        inside = iw > 0 and ih > 0 and iw * ih >= 0.5 * (tb[2] - tb[0]) * (tb[3] - tb[1])
        out = max(gb[0] - tb[0], tb[2] - gb[2], gb[1] - tb[1], tb[3] - gb[3])
        if inside and out >= 2 and not _is_allowed(allowed, g, t):
            found.append(("spill", g, t, tuple(tb)))
    # reserved zones: a thin margin around the chrome and the hosts
    hit_pairs = {(id(a), id(b)) for _, a, b, _ in found}
    r = max(1, int(round(ZONE_MARGIN / RES)))
    for i, o in enumerate(units):
        if roles[i] not in ("chrome", "host"):
            continue
        zone = None
        for j, u in enumerate(units):
            if roles[j] in ("chrome", "host", "background", "bubble") or i == j:
                continue
            # next to a host, small things (a "?" over the head, a tag it wears) are reactions and
            # props of the host; only panels, creatures and props crowd it
            if roles[i] == "host" and roles[j] not in ("panel", "actor", "prop"):
                continue
            if (id(o), id(u)) in hit_pairs or (id(u), id(o)) in hit_pairs:
                continue
            if u.group is o or o.group is u or (u.group is not None and u.group is o.group):
                continue
            zb = (o.box[0] - r, o.box[1] - r, o.box[2] + r, o.box[3] + r)
            x0, y0 = max(zb[0], u.box[0]), max(zb[1], u.box[1])
            x1, y1 = min(zb[2], u.box[2]), min(zb[3], u.box[3])
            if x1 <= x0 or y1 <= y0:
                continue
            if zone is None:
                img = Image.fromarray(np.pad(o.all, r).astype(np.uint8) * 255)
                zone = np.asarray(img.filter(ImageFilter.MaxFilter(2 * r + 1))) > 0
            z = zone[y0 - zb[1]: y1 - zb[1], x0 - zb[0]: x1 - zb[0]]
            m = u.all[y0 - u.box[1]: y1 - u.box[1], x0 - u.box[0]: x1 - u.box[0]]
            if (z & m).sum() >= ZONE_PX and not _is_allowed(allowed, o, u):
                found.append(("zone:" + roles[i], o, u, (x0, y0, x1, y1)))
    return found


def _is_allowed(allowed, a, b):
    def hit(u, fam):
        if fam is None:
            return True
        if u is None:
            return False
        return id(u.root) in fam or any(id(x) in fam for x, _ in u.leaves)
    for fa, fb in allowed:
        if (hit(a, fa) and hit(b, fb)) or (hit(b, fa) and hit(a, fb)):
            return True
    return False


# ---------------------------------------------------------------------------
# reporting
# ---------------------------------------------------------------------------
def label(u):
    if u is None:
        return "-"
    if u.is_text:
        s = getattr(u.root, "text", None) or getattr(u.root, "tex_string", None)
        if s is None and isinstance(u.root, DecimalNumber):
            s = str(u.root.get_value())
        return repr(" ".join(str(s or type(u.root).__name__).split())[:32])
    c = u.root.get_center()
    return f"{type(u.root).__name__}{'[' + u.role + ']' if u.role else ''}@({c[0]:.1f},{c[1]:.1f})"


def box_units(box):
    x0, y0, x1, y1 = box
    fw, fh = config.frame_width, config.frame_height
    return [round(x0 * RES - fw / 2, 2), round(fh / 2 - y1 * RES, 2),
            round(x1 * RES - fw / 2, 2), round(fh / 2 - y0 * RES, 2)]


class OverlapTracker:
    """Keeps overlaps that last >= HOLD seconds; reports each pair once."""

    def __init__(self, scene_name):
        self.first, self.reported = {}, set()
        self.scene_name = scene_name
        self.log = os.environ.get("OSTEP_CHECK_LOG")
        self.findings = []

    def sample(self, scene, mid_play=False):
        t = scene.time
        now = {}
        for kind, a, b, box in find_overlaps(scene, mid_play):
            now[(kind, id(a.root), id(b.root) if b else 0)] = (kind, a, b, box)
        for k in [k for k in self.first if k not in now]:
            del self.first[k]
        for k, (kind, a, b, box) in now.items():
            t0 = self.first.setdefault(k, t)
            if t - t0 >= HOLD - 1e-6 and k not in self.reported:
                self.reported.add(k)
                bb = box_units(box)
                rec = {"scene": self.scene_name, "t": round(t0, 2), "kind": kind, "a": label(a),
                       "b": label(b), "box": bb}
                self.findings.append(rec)
                print(f"[overlap:{kind}] t={t0:.1f}s {rec['a']} x {rec['b']} "
                      f"box=({bb[0]:.1f},{bb[1]:.1f})-({bb[2]:.1f},{bb[3]:.1f})")
                if self.log:          # a .jsonl path (tools/render.py sets it per scene)
                    os.makedirs(os.path.dirname(self.log) or ".", exist_ok=True)
                    with open(self.log, "a", encoding="utf-8") as f:
                        f.write(json.dumps(rec) + "\n")
