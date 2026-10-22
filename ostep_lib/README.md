# ostep_lib

Style constants, reusable characters, props and the narrated-scene base for the OSTEP video
series (ManimCE 0.19). Everything is drawn with Manim primitives. No images or SVG files are used.
`from ostep_lib import *` exports all of it.

```python
from manim import *
from ostep_lib import *          # style constants + Professor, Student, Computer, Process

class Intro(Scene):
    def construct(self):
        apply_style(self)                                   # BG background
        prof = Professor().to_edge(LEFT).shift(DOWN)
        stu = Student().flip().to_edge(RIGHT).shift(DOWN)   # flip() makes it face left
        self.play(FadeIn(prof), FadeIn(stu))
        self.play(prof.look_at(stu), stu.look_at(prof))
        self.play(prof.says("What is a process?", expression="explaining"))
        self.play(stu.change("confused"))
        self.play(prof.remove_bubble(), stu.thinks("A running program?"))
        self.play(stu.blink())
```

## Style (`ostep_lib.style`)
`BG, TEXT, DIM`, section accents `VIRT, CONC, PERS, SEC, INTRO`, concept colors
`CPU_COLOR, MEM_COLOR, DISK_COLOR, KERNEL_COLOR, USER_COLOR`, character colors
`PROFESSOR_COLOR, STUDENT_COLOR, COMPUTER_COLOR, PROCESS_COLORS` (6 colors), and
`apply_style(scene)`, which sets the background.

Fonts: `FONT = "CMU Serif"` (the default for `Text`/`MarkupText`/`Paragraph` once ostep_lib is
imported) and `MONO_FONT = "CMU Typewriter Text"` (code, terminals, addresses).
**CMU fonts lack some glyphs**: ✓ ★ ≈ ↔ render as boxes. Use `tick_mark()`, `Star`,
`MathTex(r"\approx")` and `MathTex(r"\leftrightarrow")` instead.

## Narration (`ostep_lib.narration`)
`NarratedScene(Scene)` is the base for every episode scene. `setup()` applies the style.
- `self.say(text, *animations, min_time=None)` adds `text` as a subcaption (exported to `.srt`)
  and plays the animations stretched or padded to the speaking time (`speech_time(text)`,
  about 2.5 words/s).
- `self.beat(seconds=1.0)` is a marked pause.
- Set `OSTEP_CHECK=1` to print a `[bounds]` warning whenever a mobject crosses the frame edge.

## Props (`ostep_lib.props`)
`props/__init__.py` auto-imports `core.py` plus every `ov_*.py` and `p<NN>_*.py` module and
re-exports their `__all__`. Full core API: `props/CORE_API.md`. Previews:
`python -m manim -ql -s ostep_lib/props/preview.py PropSheet` (core), `OverviewSheet` (01–03),
and `ostep_lib/props/p04_preview.py` with `P04PropSheet` / `P04IconSheet` (04).

**Core (`core.py`)**
- `CPU(size, label, pins)`: `.slot_point()`, `.seat(p)`, `.virtual_copy()`.
- `Memory(cells|regions, contents, addresses, title)`: `.cell()`, `.region()`, `.set_content()`, `.fill_cell()`, `.clear_cell()`.
- `Disk(width, height, label)`: `.top_point()`, `.spin()`.
- `CruxCard(question, subtitle, accent)`: `.write()`, `.dock()`. `TipCard` / `AsideCard(body, title, icon)`: `.slide_in()`, `.slide_out()`.
- `TermHighlight(accent)` (manager): `.show(term, hold, dock, size, at)`, `.clear()`. `SectionBadge(text, accent)`: `.recolor()`.
- `IllusionSplit(left, right, orientation="vertical"|"horizontal", at)`: `.draw()`, `.merge()`.
- `Peach(radius)`: `.virtual_copy()`.
- Icons: `FileIcon`, `ClockIcon` (`.spin()`), `Spotlight` (`.move_beam_to()`), `GearPair` (`.spin()`), `PauseGlyph`, `PlayGlyph`, `Laptop`.
- Helpers: `hop_to(mob, point)` (arc with squash and stretch), `base_point`, `place_on`, `make_translucent`, `wrap_text`, `centered_text`, `outline_of`.

**Overview props (`ov_props.py`, `ov_icons.py`)**
- `Terminal(width, height, cpus)`: `.type()`, `.print()`, `.prompt_line()`, `.pop()`, `.clear()` (auto-scroll).
- `MemoryStrip(n, start, step, values)`: `.read()`, `.write()`, `.set_value()`, `.color_cell()`, `.pulse()`, `index_of("0x…")`. `MappingArrows(pairs)`: `.create()`, `.pulse()`.
- `SystemStack(...)`: `.relabel()`, `.route()`, `.doors()`.
- `InterleavingDemo(value, colors)`: `.play_step(k, op)`, `.steps(seq)`, `.reset()`.
- `UserKernelBoundary(y)`: `.draw()`, `.cross(mob, target)`, `.flash_at()`, `.pulse()`. `PrivilegeGauge`: `.set_level("user"|"kernel")`.
- `EraRibbon(eras, y)`: `.draw()`, `.move_marker()`.
- `make_thread(label, color)`: the thread stand-in (a Process at ×0.65).
- Icons: tick_mark, x_mark, next_tag, question_mark, book, editor, punch_cards, mainframe, minicomputer, operator, server_rack, phone, desktop, `PowerSwitch` (`.flip()`), ssd, journal, cow, sticky_note, padlock, leaf, stopwatch, ecg, scroll, pipe_glyph, poster_frame, net_boxes, letter, chair, bookshelf, layers, walls, hand, name_tag, money_meter, loop_arrow.

**Process-episode props (`p04_*.py`)**
- `Timeline(rows, ticks=8, colors, x_range, top, row_height, cpu_row, …)`: `fill(row, tick, state)`, `fill_cpu`, `fill_column`, `unfill`, `unfill_ticks` (rewind), `clear_blocks`, `extend`, `boundary_marker`, `ghost_blocks`, `cell_center`, `tick_x`. States: running / ready / blocked / idle / busy / done (see the bible's encoding).
- `Queue(label, center, slots, spacing, mover)`: `place`, `push`, `pop`, `insert`, `pack`, `slot_point(i)`; processes are tracked in `items`.
- `StateDiagram(positions, radius, running_icon, …)` (Figure 4.2): `zone_points`, `create_zones`, `create_arrows`, `write_arrow`, `pulse_arrow`, `glow_zone`; legend mode `to_legend` / `set_legend` with tracking dots (`make_dot`, `place_dot`, `move_dot`, `remove_dot`).
- `PCBCard(title, color, fields, …)`: `field`, `set_field` (animation), `set_field_now`, `indicate_field`.
- `RegisterBank(registers, cols, …)`: `set_value`, `highlight`, `unhighlight`, `flicker`, `cell`.
- `Bus(y, x_range, taps)`: `add_tap`, `path(a, b)` for `MoveAlongPath`.
- Icons (`p04_icons`): browser/music/chat/gamepad/envelope icons, sheet_music, `RoboticArm`, `SpeedGauge`, `Notepad`, save_slot, `MenuCard`, cursor, puff, info_tag, progress_ring, keyboard, plug, whistle, exit_tag, mini_clock, hatch_rect, check/cross marks, `ep_tag("→ Ep. 06")`.

Known quirk: a character's `.width` / `.height` are unreliable (empty submobjects count in
Manim's bounding box). Use `get_left()` / `get_right()` / `get_top()` / `get_bottom()`.

## Characters

| Class | Look | `EXPRESSIONS` |
|---|---|---|
| `Professor(expression="neutral", color=None)` | lavender bean, round glasses, grey hair fringe, beard + mustache, bow tie | neutral, explaining, happy, thinking, surprised, worried, proud |
| `Student(expression="neutral", color=None)` | smaller rose bean, slate cap, hoodie with drawstrings, freckles | neutral, curious, confused, excited, sad, frustrated, surprised, bored |
| `Computer(expression="idle", color=None)` | beige retro CRT on a stand, glowing face on the screen, power LED | idle, happy, busy, overwhelmed, sleeping, error, surprised |
| `Process(expression="ready", color=None, label=None)` | small blob with feet; color cycles through `PROCESS_COLORS`; optional label under it ("PID 1", "A") | ready, running, blocked, done, zombie |

Default sizes: Professor and Computer are about 2 units tall, Student about 1.7 and
Process about 1.4 with its label (1 unit wide), so 8 processes fit in a row.
Some expressions add extras such as "?", "!", a light bulb, a tear, an anger mark,
sweat drops, steam, zZz, a clock, a check mark or a glow. These cross-fade when the
expression changes.

## Common API (`Character`, a `VGroup`)
- `change(expression, look_at=None, **anim_kwargs)` returns an Animation that morphs
  to the expression. The default run_time is 0.7.
- `set_expression(expression)` changes the expression instantly and returns self.
- `blink(**anim_kwargs)` returns an Animation (0.3 s).
- `look_at(point_or_mobject)` returns an Animation that moves the pupils (the current gaze is in `char.gaze`).
  `look(direction)` does the same for a direction such as `UP` or `DL`
  (`ORIGIN` resets the gaze). `set_look(target)` changes the gaze instantly.
- `says(content, expression=None, run_time=0.8, **bubble_kwargs)` and
  `thinks(...)` return an Animation that grows a speech or thought bubble from the
  head. `content` is a `str` or any Mobject (for example `MathTex`). The bubble is
  stored in `char.bubble`, and an existing bubble is faded out automatically.
  The bubble kwargs are `font_size=30, max_width=5, padding, fill_color, stroke_color,
  text_color, lift, side`. Bubbles are clamped so they stay inside the frame.
- `remove_bubble(run_time=0.5)` returns a FadeOut of the current bubble.
- `get_bubble(content, kind="speech"|"thought")` builds a `Bubble` mobject without
  showing it. `BubbleIn(bubble)` is its show animation.
- `flip()` mirrors the character in place. Text stays readable, and bubbles and
  gaze follow the new `facing` (`RIGHT`/`LEFT`). `is_flipped` tells you the current
  direction.
- `EXPRESSIONS` lists the valid names. Any other name raises `ValueError` with the
  list of valid names.
- Characters move and scale like normal mobjects. Line widths scale with
  `.scale()`, so proportions are kept.

Notes:
- Do not run two of `change`/`look_at`/`blink` on the same character in one
  `play`. Use `change(expr, look_at=...)` to combine them, or use `Succession`.
- Do not play `char.change(...)` together with `char.animate...` on the same
  character. Movement is fine on other mobjects, or in the previous or next `play`.
- Targets are computed when the animation starts, so chaining with `Succession` works.

## Preview
From the project root:
```
python -m manim -ql -s ostep_lib/characters/preview.py ExpressionSheet   # every expression (still)
python -m manim -ql ostep_lib/characters/preview.py CharacterDemo        # ~14 s demo video
```
`characters/expression_sheet.png` is a reference render of the sheet.
