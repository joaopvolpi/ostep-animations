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
- Set `OSTEP_CHECK=1` to print a `[bounds]` warning whenever a mobject crosses the frame edge, and an
  `[overlap]` warning whenever two visible texts overlap. The overlap check also samples ~4×/s during
  animations, must hold for two samples in a row, and ignores text under a scrim. `tools/render.py`
  always sets it, prints only these lines, and ends with a "layout check: N warning(s)" summary. It renders with
  `--disable_caching`, because cached animations skip their frames and so skip the mid-animation samples. If you run
  manim yourself, pass that flag too, or the check under-reports.

## Props (`ostep_lib.props`)
`props/__init__.py` auto-imports `core.py` plus every `ov_*.py` and `p<NN>_*.py` module and
re-exports their `__all__`. Full core API: `props/CORE_API.md`. Previews:
`python -m manim -ql -s ostep_lib/props/preview.py PropSheet` (core), `OverviewSheet` (01–03),
and `ostep_lib/props/p04_preview.py` with `P04PropSheet` / `P04IconSheet` (04).

**Core (`core.py`)**
- `CPU(size, label, pins)`: `.slot_point()`, `.seat(p)`, `.virtual_copy()`.
- `Memory(cells|regions, contents, addresses, title)`: `.cell()`, `.region()`, `.set_content()`, `.fill_cell()`, `.clear_cell()`.
- `Disk(width, height, label)`: `.top_point()`, `.spin()`.
- `CruxCard(question, subtitle, accent)`: `.write_head()`, `.write_sub()`, `.dock()` (and the silent `.write()`: avoid it). A crux is
  always read aloud: `self.say_crux(card, *extra_anims, sub_anims=(), dock=False, hold=0.8, **dock_kwargs)` on a `NarratedScene`
  narrates "The crux: <question>" while the card writes, reads the subtitle as it fades in, then optionally docks. It speaks exactly
  the card's text. A crux that only appears as a strip swap: `self.say("The crux: <q>", ReplacementTransform(old, new))`.
- Hosts: `host_pair(mode, stu_expr, prof_expr)` and `host_mode_anims(stu, prof, mode, run_time)` with `STU_CORNER`, `PROF_CORNER`,
  `STU_DIALOGUE`, `PROF_DIALOGUE`, `HOST_SCALE` (corner = 0.75 at (±5.8, −2.8); dialogue = 1.0 at (±2.6, −1.2)).
  **A character's `get_center()` / `move_to` / `scale` use a fixed design anchor** (the default-expression body center in its design frame),
  not the bounding box, so placing a character gives the same position whatever its expression. Edges (`get_top()`, `get_left()`…) still use the real bounding box.
- `TermHighlight.docked_now(term)`: the docked term built instantly, identical to what `show`/`note` leave behind (for a scene's "starts with" state).
- `tools/continuity.py <NN>` compares the last frame of each scene with the first of the next and lists changed regions (`--dir` for
  any folder of scene clips). Aim for ~0%: a jump means a "starts with" state that isn't the previous "ends with". `TipCard` / `AsideCard(body, title, icon)`: `.slide_in()`, `.slide_out()`.
- `TermHighlight(accent)` (manager): `.note(term)` for secondary terms (slides into the top-right dock, no veil).
  `.show(term, hold, dock, size, at, scrim=True)` is the unveil, for the 3–4 key terms of an episode only. `.clear()`. By default
  it veils the scene, writes the term at center (0, 0.3), and docks it top-right (≤ 2.6 wide) as the veil lifts.
  Don't pass `at=` near the top band. `scrim=False` is only for an empty screen. `SectionBadge(text, accent)`: `.recolor()`.
- Screen zones: `CONTENT_TOP` (2.55; scene content stays below), `CHROME_ROW_Y` (3.6), `CRUX_STRIP_Y` (3.0;
  the default `dock()` point, strip ≤ 8.2 wide). `scrim(opacity=0.88)` is a full-frame BG veil at z 40
  (put anything that must stay on top at z > 40).
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

**Process API props (`p05_*.py`)** (preview: `p05_preview.py` → `P05PropSheet`)
- `clone_process(proc, to=None, color=None, label=None, …)` returns `(clone, anim)`; add the clone to the scene before playing.
- `ProcessWorld(color, pid, pcb_pid, label)`: creature + memory column + registers + PCB + fd plugs. `place`, `assemble`, `clone_to`, `clone_stages`, `set_pid`, `pc_marker`, `code_point`, `collapse`, `set_program`.
- `CodeWalker(src, font_size, caption)` / `make_code`: Code with several colored highlight bars (lines numbered from 1). `add_bar`, `move_bar`, `indicate`, `circumscribe`, `line_point`, `line_mob`, `write_in`. Bars aren't children; use `.everything()` to move or fade them together.
- `FdTable` (`cut`, `scan_free`, `plug_into`, `slot_point`), `ShellLoop(cx)` (`light`, `draw_arrow`, `highlight_gap`, `workshop`, …), `KernelPipe` (`send(text)`, `left_end`, `right_end`), `MenuCardRows` (`row_y`, `highlight_row`, `chip_for`, `bracket`).
- Icons: `bolt_glyph`, `Keycap` (`.press()`), `handler_box`, `shield_arc`, `crown_tag`, `glass_pane`, `wrench_glyph`, `program_chip`, `mem_icon_small`, `zombie_mini`, `stop_sign_tag`.

**Limited-direct-execution props (`p06_*.py`)** (preview: `p06_preview.py` → `P06PropSheet`)
- `KernelToken(label="OS")`: the red OS badge riding the CPU. `place(cpu)`, `hop_onto(cpu)`, `dim_to(o)`, `wake()`, `reach(point)`, `retract()`.
- `cpu_ride(chip, target, boundary, gauge, riders, run_time)`: the chip slides across the user/kernel line, the line flashes, and the gauge flips at the midpoint.
- `RegPacket(color, labels, cell, n)` (`fly_to`, `fly_into`), `PacketFly(mob, end, arc, end_scale, fade)`, `ShiftBy(mob, delta)` (relative shift, safe inside `Succession`).
- `KernelStack(label, color, width, height, slots)`: `push`, `pop`, `slot_point`, `glow`, `plain`, `dim_down`.
- `TrapTable(rows, …)`: `add_row`, `highlight_row`, `unhighlight`, `lock`, `row`.
- `ProtocolChart(columns, col_x, colors, …)` (Figures 6.1/6.2-style listings): `draw`, `write_row`, `section`, `link`, `sweep`, `clear_rows`; older rows dim and the chart scrolls.
- `AlarmClock(radius, boxed, label)` (`ring`, `spin`, `start`, `stop`), `ShieldGate(height)` (`open`, `close`).
- Icons: `cabinet_lock`, `socket_cover`, `fence_glyph`, `magnifier_icon`, `door_in_line`, `booth_gate`, `bench_ring`.

**Scheduling props (`p07_*.py`)** (preview: `p07_preview.py` → `P07PropSheet`)
- `Padlock` (`open`, `close`, `wobble`, `shake`, `pulse`; red when closed, green when open) and `PadlockStrip(n, size, at, opened)` (`open(i)`, `close(i)`). This is the series' padlock; prefer it over `ov_icons.padlock`.
- `MetricReadout(terms, denom, value, center, font_size)`: writes `\frac{a+b+c}{n}=v` piece by piece. `reveal_term`, `reveal_numerator`, `reveal_value`, `frame_value(good)`, `strike(old)`, `count_value`, `show_all`, `fade_out`. `ro.shown` holds what's revealed.
- `CrystalBall` (`glow_up`, `glow_down`, `crack`), `Cart(boxes)`, `Checkout` (`blink`), `milk_carton`, `checkbook_icon`.
- **`Timeline` extensions** (additive): kwargs `row_kinds` (process/cpu/disk/os), `label_mode="boundary"`, `unit_per_tick`, `label_every`; methods `row_top`, `fill_span` / `set_span` (fractional ticks), `move_block`, `arrival_marker`, `completion_marker`, `bracket(style="solid"|"dashed")`.

**MLFQ props (`p08_*.py`)** (preview: `p08_preview.py` -> `P08PropSheet`)
- `MLFQLadder(levels, …)`: stacked priority lanes. `lane_point`, `place`, `promote`, `demote`, `boost_all`, `serve` / `glow_lane`, `collapse_to`, `register`. Positions break under scaling, so build it at its final size (11 uses its native size).
- `RuleBoard`: an accumulating rules panel. `skeleton`, `place_now`, `add(tag, text)`, `glow`, `hold_glow`, `merge`, `warn`, `ok`, `outline`, `set_dim`. Keep its frame at `z_index=-1` when animating it, or it covers the rows.
- `AllotmentGauge`: `drain`, `reset`, `chunk` (ledger mode), `attach_to`.
- Icons (`p08_icons`):
  - `gamer_shades` and `put_shades` are the series' sunglasses for Process B, the scheduler-gamer.
  - Also `tag_chip`, `mystery_box`, `history_clock`, `rr_ring`, `io_button`, `Dial`, `SliderPanel`, `voodoo_glyph`, `mini_pie`, `medal_glyph`, `config_glyph`, `neural_glyph`, `fork_glyph`, `cache_grid`, `bookmark_glyph`.

**Proportional-share props (`p09_*.py`)** (preview: `p09_preview.py` -> `P09PropSheet`)
- `RaffleDrum`, `Ticket`, `TicketStack` (tickets colored by process). `RaffleDrum.draw()` returns `(ball, anim)`. Play the draw in its own `play`, not nested in a `Succession` with other `.animate` calls, or its text is duplicated.
- `Seesaw` (`tilt(angle)`, two pans for labels).
- `TargetPie`, `NumberStrip`, `JobList`, `PassLane`, `PassTable`, `VruntimeMeter` (level is a fraction of `max_value`).
- `RBTree` (generic red/black tree; `RB_SPEC` is Fig 9.5), `FairnessPlot`.
- Icons (`p09_icons`): `cloud_icon`, `vm_window`, `coin_icon`, `die_icon`, `handshake_icon`, `paper_chip`, `bad_luck_cloud`, `sched_chip`, `text_editor_icon`.

**Episode 11 icons (`p11_icons.py`)**: `Flame(height)` (`flicker`, `stop_flicker`), `puzzle_piece`, `censor_bar(width, height)`, `neck_bolts`.

**Multi-CPU props (`p10_*.py`)** (preview: `p10_preview.py` -> `P10PropSheet`)
- `EyeIcon(width, iris, opened)`: `look_at(target)`, `set_look`, `open_lids()`, `close_lids()`, `blink()`; used for snooping and peeking (and by episode 11).
- `CacheCPU(label, size, n_cells=3)`: a `CPU` with a cache strip under it. `store(value, color)`, `set_value(i, text, color)`, `invalidate(i)`, `warmth(level, color)`, `clear()`, `pulse()`; points `slot_point()`, `cache_point()`, `cache_bottom()`, `cell_point(i)`. Parts: `cpu`, `strip`, `cells`, `texts`.
- `ScheduleGrid(rows, columns, cell_w, cell_h, colors, row_labels, repeat_label)`: the book's CPU x time-slice table colored by job letter. `fill(row, col, job)`, `fill_row`, `fill_column`, `hatch(row, col)`, `set` / `set_row` (instant), `highlight_job`, `unhighlight`, `clear`, `cell_center`, `cell_mobs(job)`.
- `bus_pulse(bus, a, b, color, run_time)`: a bright dot travels along `Bus.path(a, b)` (the dot hides inside the bus).
- Icons (`p10_icons`): `suitcase_icon` (migration), `pin_icon` (affinity), `flame_icon` (warmth), `hand_up_icon`.

**Gotchas**
- Don't define a method named `dim` on a `VGroup` subclass; it shadows Manim's `Mobject.dim`.
- `FadeOut` of a block inside a `Timeline` doesn't detach it; call `Timeline.purge()` after clearing.
- `PrivilegeGauge` can't be scaled after creation (`set_level` rebuilds from unscaled geometry). Build it at its final size.
- To build an instant "starts with" state from an animation: `anim.begin(); anim.finish()`.
- **`Succession` flashes later introducers.** It adds every sub-animation's mobject at t=0, but begins
  each one only when its turn comes. So a `Write`/`FadeIn`/`Create` that isn't first shows the finished
  mobject until it starts. Make introducers first in a `Succession`, or group the sequence as
  `AnimationGroup(a, b, lag_ratio=1)`, which begins everything at t=0. Don't put a `Transform` of a
  mobject in the same `AnimationGroup` as its introducer: it would capture the empty start state.
- Scrims and other animated mobjects sit nested inside animation groups in `scene.mobjects`. Search
  `get_family()`, not just the top level.

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
