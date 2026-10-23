# ostep_lib.props.core: API summary

`from ostep_lib import *` exports everything below, plus `NarratedScene` and `INTRO`.
Modules `ostep_lib/props/ov_*.py` and `ostep_lib/props/p<NN>_*.py` are **auto-imported** by
`props/__init__.py`, and their `__all__` is re-exported. Episode 04: put your props in
`p04_*.py` with an `__all__`, and they show up in `from ostep_lib import *`. A module that
fails to import only raises a warning.

Preview: `python -m manim -ql -s ostep_lib/props/preview.py PropSheet`, plus `PropDemo` (animated).

## Scene base: `ostep_lib/narration.py`
- `NarratedScene(Scene)`: `setup()` applies the style.
- `say(text, *anims, min_time=None, stretch=False)`: plays the anims together and adds a subcaption.
  The call lasts max(words/2.5, min_time, anim time). If the anims are shorter, it pads with a wait,
  or stretches them when `stretch=True`. With no anims, it just waits.
- `with self.narrate(text, min_time=None): ...`: one subcaption around several `play` calls (padded).
- `beat(seconds=1.0)`.
- `speech_time(text, min_time=None)`.

## Helpers
- `outline_of(color, amount=0.55)`: the darker outline color the characters use.
- `label_text(s, font_size=24, color=TEXT, weight)` (CMU Serif), `mono_text(...)` (CMU Typewriter).
- `wrap_text(s, max_width, font_size, font, weight)` returns a string with `\n`.
  `centered_text(s, max_width, font_size, color, ...)` returns a VGroup of centered lines.
- `make_translucent(mob, fill_opacity=0.25, stroke_opacity=0.6)`: the "virtual copy" look (in place, multiplies opacities).
- `base_point(mob)`: the feet of a Process (local y = -1.05, so the label hangs below), the body bottom of other
  characters, or `get_bottom()` for anything else.
- `place_on(mob, point)`: instantly puts `base_point` on `point`.
- `hop_to(mob, point, height=None, anchor="base"|"center", squash=0.18, run_time=0.5)`: arc hop
  with squash and stretch; the base point lands on `point`. Don't combine it with `change`/`look_at` of the
  same character in one `play`.

## Hardware
- `CPU(size=1.4, label="CPU", color=CPU_COLOR, pins=4, font_size=None)`. Parts: `body, die, pins, label, mark`.
  `slot_point()` = top-center of the body (where a running process stands). `seat(process)` places it there.
  `virtual_copy(fill_opacity=0.25, stroke_opacity=0.6)`.
- `Memory(cells=8, regions=None, contents=None, width=1.4, height=4.4, color=MEM_COLOR, font_size=18,
  mono=True, addresses=True|list[str], title=None, cell_fill_opacity=0.18)`.
  `regions=["code", "static data", ("heap", 1.5), ("free", 2), "stack"]` gives named regions (weight = relative
  height; the region name is the cell text, in serif). With `cells=n`, `contents=[...]` sets the texts, in mono.
  Parts: `cells` (Rectangles, top to bottom), `texts`, `addresses` (left, DIM mono; default "0", "1", ...), `title`.
  Access: `cell(i_or_name)`, `region(name)`, `index_of(name)`, `cell_center(i)`.
  Animations: `set_content(i, text)`, `fill_cell(i_or_name, color, opacity=0.6)`, `clear_cell(i)`.
- `Disk(width=1.6, height=1.3, color=DISK_COLOR, label=None, font_size=22)`. Parts: `body, top, hub, arm, band, label`.
  `top_point()` = center of the top surface. `spin(turns=1, run_time=1)` returns an animation (`DiskSpin`).

## Cards and overlays
- `CruxCard(question, subtitle=None, accent=VIRT, width=9, header="THE CRUX", question_size=34, subtitle_size=24)`.
  Parts: `frame, header, question, subtitle`. `write(run_time=1.6)`. `dock(point=(0, 3.0), font_size=24)`
  transforms the card into a one-line strip with the question (afterwards `self` *is* the strip).
  `strip(point, font_size)` builds the strip without animating.
- `TipCard(body="", title="TIP", width=5, height=None, accent=DIM, font_size=26, icon=None)` and
  `AsideCard(...)` (header "ASIDE"). `body` is a str (wrapped, centered) or a Mobject. Parts: `frame, rule,
  header, icon, body`. `content_center()`, `slide_in(direction=RIGHT)`, `slide_out(direction=RIGHT)`.
- `TermHighlight(accent=VIRT, at=(0, 0.3), size=54, dock_at=(6.6, 3.6), dock_size=26, dock_max_width=2.6)` is a manager, not a mobject.
  `show(term, hold=1.2, dock=True, size=None, at=None, accent=None, scrim=True)` returns one Succession: veil the
  scene (`scrim()`), write big + underline at the center above it, hold, then lift the veil while the term docks
  top-right (right-aligned, replacing the previous docked term) or fades (`dock=False`). `scrim=False` is only for an empty screen.
  `show` is the **unveil**, for 3–4 key terms per episode. `note(term, accent=None)` is the light variant for every other term:
  it fades the term straight into the dock, replacing the previous docked term.
- Screen zones: `CONTENT_TOP=2.55`, `CHROME_ROW_Y=3.6`, `CRUX_STRIP_Y=3.0`. `scrim(opacity=0.88, z_index=40)`
  returns a full-frame BG veil (`is_scrim=True`; the overlap check ignores text below it).
  Lower level: `write(term)`, `dock_anim()`, `fade_anim()`. Also `clear()`, `set_accent(c)`, attributes `big`, `docked`.
- `SectionBadge(text, accent=VIRT, font_size=22, corner=(-6.6, 3.6))`: left-aligned at `corner`.
  Parts: `dot, text`. `recolor(accent)` returns an animation.
- `IllusionSplit(left_title="What each program sees", right_title="What really happens",
  orientation="vertical"|"horizontal", at=0, title_size=28, color=DIM, top_y=CONTENT_TOP, bottom_y=-3.6,
  left_x=-6.6, right_x=6.6, title_y=None)`. Vertical: a dashed divider at x=`at`, with titles centered over each half
  at `title_y` (default `top_y - 0.3` = 2.25, below the top band).
  Horizontal: the divider is at y=`at`; `left_title` is the TOP title (top-left) and `right_title` the BOTTOM title (just under the divider, left).
  Parts: `divider, left_title, right_title`. `draw()`, `left_center()`, `right_center()`, and `merge()` (fades the divider
  and titles; the caller moves the contents).

## Icons and misc
- `Peach(radius=0.55)`. Parts: `body, crease, leaf, stem`. `virtual_copy(opacity=0.35)` gives a translucent copy with a dashed outline.
- `FileIcon(name=None, color=DIM, width=0.6, lines=3, font_size=18, mono=True)`. Parts: `page, fold, lines, label` (name under the page).
- `ClockIcon(radius=0.3, color=TEXT)`. `spin(turns=1, run_time=1)` turns the minute hand.
- `Spotlight(height=2.5, spread=0.7, color="#FFF3B0")`. Parts: `lamp, beam, pool`. `move_beam_to(point)` returns self,
  so `spot.animate.move_beam_to(p)` works. `pool_center()`.
- `GearPair(radius=0.6, color="#B8B8B8")`. Parts: `big, small`. `spin(angle=TAU, run_time=2)`.
- `PauseGlyph(size=0.6, color=TEXT)`, `PlayGlyph(size=0.6, color=TEXT)`.
- `Laptop(width=5, color=TEXT, stroke_width=3, fill_opacity=0.0)`. Parts: `lid, screen, base`. `screen_center()`.
- Constants: `INK` (character outline ink), `CARD_FILL`, `PEACH_COLOR`.

## Episode 01-03 props (not core, but stable and usable)
See `ov_*.py`: `Terminal` (console with `.type(cmd)` / `.print(line)`), `MemoryStrip`, `SystemStack`,
`UserKernelBoundary`, `PrivilegeGauge`, `EraRibbon`, `InterleavingDemo`, `MappingArrows`, plus icons.
They are added as they get built. Check the module docstrings.

## Changelog
- v1 (CORE_READY): initial API.
- v1.1 (non-breaking fixes):
  - `Memory` cells now use an opaque fill that looks the same (`mix(color, BG, 1 - cell_fill_opacity)`,
    opacity 1), so lines drawn behind a column are hidden. `clear_cell` restores that fill.
  - `CruxCard.dock()` (rewritten after episodes 04–07 still saw a stray dot with subtitles): the frame and
    question morph into the strip; the header and subtitle fade out and are removed from the card when the
    animation ends. The ghost-dot workaround (`strip()` + `ReplacementTransform`) is no longer needed.
  - `Disk`: the decorative side band was removed (`disk.band` still exists but isn't drawn).
- `NarratedScene`: with env var `OSTEP_CHECK=1`, every `play` prints `[bounds]` warnings for visible mobjects
  that cross the frame edge (debug aid, off by default).
- Note: the CMU fonts have no glyphs for ✓ ★ ≈. Use `tick_mark()`, `Star`, and `MathTex(r"\approx")` instead.
  For crosses use `x_mark()`; for ≠ use `MathTex(r"\neq")`.
