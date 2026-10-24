---
name: ostep-render
description: Implement an OSTEP episode's scene breakdown (Ostep/Scenes/*.md) as ManimCE code using ostep_lib, render it with tools/render.py into Ostep/Renders, and assemble the episode video with burned-in single-line captions (default on, --no-captions to disable) from the script's narration. Use when the user asks to code, animate, implement, render or build the video for a chapter or for specific scenes, e.g. "render episode 04", "/ostep-render 04 S05-S07", "/ostep-render 04 --final".
---

# OSTEP scenes → Manim code → rendered video

You implement the scene breakdown **faithfully**: what's on screen, where, in which order, landing
on which words. Then you render it and *look at* the result before calling it done. The scene file
is the spec, the script is the narration, and the bible is the style law.

## Arguments
- Episode (number, slug or path), resolved in `Ostep/Scenes/`. If there is no scene file, stop and
  suggest `/ostep-scenes` first.
- Optional scene selection: `S05`, `S05-S07`, `S03,S09`. The default is all scenes.
- Optional `--final`: high-quality render (`-qh`, 1080p60) plus episode assembly. The default is a
  draft (`-ql`, 480p15) of the selected scenes only, with no assembly.
- Optional `--no-captions`: render without the caption band. **Captions are on by default.**

## Captions (default: on)
- Captions are the script's narration, burned into the video by `tools/render.py`. It scales the
  animation to 90%, keeps it at the top of the frame, and adds a caption band below it, so the
  output stays 16:9.
- Rules: **one line at most** (long narration is split and timed proportionally), the **series font**
  (CMU Serif, `TEXT` color on `BG`), and **never overlapping the animation** (they live only in the
  band).
- The band is outside the animation's frame, so scene layouts need no changes and no frame checks
  for it. Just keep everything inside the normal safe area as usual.
- The caption text comes from `NarratedScene.say(...)` subcaptions. So every spoken line must go
  through `say`, using the script's exact words, or it won't be captioned.
- `--no-captions` gives the clean video (full-size animation, no band).

## Read first
1. `Ostep/README.md`: palette, layout, props, motion rules.
2. `ostep_lib/README.md`, plus the source of anything you'll use (`ostep_lib/style.py`,
   `ostep_lib/characters/*`, `ostep_lib/props/*` if it exists). Use the real API; don't guess.
3. `Ostep/Scenes/<NN-slug>.md`: the whole file, especially "Visual overview" (persistent
   assignments), the selected scenes, and "New assets needed". Also check any
   `Ostep/Scenes/_shared-assets-*.md` covering this episode: it gives the **canonical name and spec**
   for assets several episodes share. Build those under that name, once.
4. `Ostep/Scripts/<NN-slug>.md`: the narration for the beats the selected scenes cover.
5. Existing code in `Ostep/Manim/<NN-slug>/`, if any. Extend it; never silently overwrite a
   scene file that already exists. Ask first, unless the user asked to redo it.

## Layout of the code
```
ostep_lib/
  narration.py          # Narrated scene base (create if missing, see below)
  props/                # reusable props from the bible (CPU, Memory, Disk, Timeline, cards…)
    __init__.py
    preview.py          # PropSheet still showing every prop, like characters/preview.py
Ostep/Manim/<NN-slug>/
  common.py             # episode constants: process colors/labels, home positions, shared builders
  s01_<slug>.py         # one file per scene: class S01<CamelTitle>(NarratedScene)
  s02_<slug>.py
Ostep/Renders/<NN-slug>/<quality>/      # written by tools/render.py, e.g. 480p15 or 1080p60
  scenes/<stem>.mp4 + .srt  # clean scene video + its subcaptions
  captioned/<stem>.mp4      # scene with the caption band (captions on)
  <NN-slug>.mp4             # assembled episode (captioned unless --no-captions)
  <NN-slug>.srt             # single-line captions for the whole episode
```
**Every rendered video goes to `Ostep/Renders/`** through `tools/render.py`. Manim's working
caches go to `.cache/media/` (gitignored). Don't leave videos in the scratchpad or in `media/`
folders.
Each scene file starts by putting the project root on `sys.path`
(`Path(__file__).resolve().parents[3]`), then `from ostep_lib import *` and `from common import *`
(add the scene's own folder to the path too). Always render from the project root.

## Step 1: shared assets first
For every item in "New assets needed" that the selected scenes use and that doesn't exist yet:
- Implement it in `ostep_lib/props/` (or as a character expression/extra in `ostep_lib/characters/`)
  as a **reusable, parameterized** mobject or animation helper, built from primitives and bible colors.
  It must not be specific to this episode.
- Add it to `props/preview.py`'s `PropSheet`, render it
  (`python -m manim -ql -s ostep_lib/props/preview.py PropSheet`), **Read the PNG**, and iterate until it
  looks clean and consistent with the characters' style (`ostep_lib/characters/expression_sheet.png`).
- Document it in `ostep_lib/README.md`. If it's a new recurring visual, add a row to the bible's
  props table (`Ostep/README.md` §6).
- Episode-only pieces (a one-off icon) go in that episode's `common.py` instead.

### `ostep_lib/narration.py` (exists; extend it, don't replace it)
A `NarratedScene(Scene)` base that applies the style and paces animations to the narration:
- `self.say(text, *animations, min_time=None)`: attaches `text` as a subcaption
  (`self.add_subcaption(text, duration=d)`), where `d = max(words / 2.5, min_time or 0)`
  (about 150 wpm). It plays the given animations, stretched or padded with `wait` so the call lasts
  `d` seconds. With no animations, it just waits `d`.
- `self.beat(seconds=1.0)`: the pauses the scene file marks as "(pause …)".
- Characters' lines go through the same `say`, using the exact text from the script.
- `setup()` calls `apply_style(self)`.

Manim writes subcaptions to a `.srt` next to each scene's video. Narration chunks are the scene
table's "Narration" column, expanded to the full sentence from the script so the subtitles are
complete.

## Step 2: implement each scene
- **One table row → one `self.say(...)` (or `self.beat()`).** Put the row number as a comment
  (`# S06.4`) so code and spec can be cross-checked.
- Honor positions, colors, sizes and persistent assignments from the scene file and `common.py`.
  Use style constants only, never raw hex in scene code.
- **Continuity:** each scene must start exactly in its "Starts with" state. Build that state
  instantly with a `common.py` builder (e.g. `build_world_after_s05()`), not by replaying the
  previous scene. End in the "Ends with" state.
- Respect the character API rules: no two of `change`/`look_at`/`blink` on the same character in one
  `play`, and no `change` together with `.animate` on the same character.
- **The crux is read aloud.** Never `card.write()`/`FadeIn(card)` silently. Use
  `self.say_crux(card, *extra_anims, sub_anims=(...), dock=True|False, hold=0.8, **dock_kwargs)`:
  it narrates the question while the card writes, reads the subtitle as it fades in, then
  docks. Pass `lead="..."` with `{q}` for the question, taking the script's wording, e.g.
  `lead="So, the crux is: {q}"`. Don't leave the mechanical default "The crux:"; the lead-in
  must match the script and vary between cruxes. The question itself is the card's text, so
  captions match the screen. A crux shown only as a strip swap gets
  `self.say("<lead-in> <question>", ReplacementTransform(old, new))`. Do this
  even if the scene file's rows don't mention it. Don't hide the subtitle with `set_opacity(0)`.
- **Continuity (no jumps at cuts).** Each scene must begin exactly where the previous one ended:
  - Hosts: `host_pair(mode, stu_expr, prof_expr)` and `host_mode_anims(stu, prof, mode)` with the
    library's `STU_CORNER` / `PROF_CORNER` / `STU_DIALOGUE` / `PROF_DIALOGUE` constants. Never define
    your own corner constants. Characters are placed by their design anchor, so `move_to` is exact
    for any expression, and any expression can be set after placing.
  - Start state == the previous scene's end state, including expressions and gaze. Never snap a face
    with `set_expression` / `set_look` at the start of a scene to anything but the previous end
    state. If the story needs a different expression, animate it in the first `play`
    (`stu.change("curious")`).
  - To start an animation partway through a `play`, use `late(delay, anim)`, not
    `Succession(Wait(delay), anim)` (which flashes the new mobjects at t=0, visible as a pop at the
    first frame of the scene). `finish_now(anim)` builds an end state instantly.
  - Docked term: `terms.docked_now(term)`. Crux strip: `card.strip()` with defaults. Badge:
    `SectionBadge`. Use the same builder at the end of one scene and the start of the next.
  - Any prop that persists across a cut is built by one `common.py` function that both scenes call
    (the end scene's final state == the next scene's start state).
  - After rendering, run `python tools/continuity.py <NN>`. It compares the last frame of each
    scene with the first frame of the next and lists changed regions. Fix every flagged boundary
    unless the cut is deliberate (a cut to an empty screen, a title card), and say which ones
    are deliberate in the report. This check costs no image tokens.
- Keep it simple and robust: prefer `Transform`, `FadeIn/Out`, `Create`, `Write`, `MoveAlongPath`,
  updaters only where needed. No external images or SVGs.
- If the spec is ambiguous or physically impossible (things overlap, don't fit, contradict each
  other), choose the closest sensible version and log it under **Deviations** in your report.

## Step 3: render and verify (token-frugal)
Images are expensive, so frame inspection is the exception, not the rule.
1. Draft render with the tool: `python tools/render.py <NN> --scenes SXX` (or a range). This
   renders at 480p15, writes to `Ostep/Renders/<NN-slug>/480p15/`, and captions by default. Add
   `--no-captions` while iterating, if you only need the clean video. Every scene must run without
   errors. **Don't Read frames by default.**
2. **Catch layout problems in code.** Use `next_to`/`arrange` with buffers, and follow the bible's
   **screen zones**: scene content stays below `CONTENT_TOP`, and the top band is for the badge,
   crux strip and docked term only. Use "Term unveil" → `terms.show(term)` (scrim + center) for
   at most 3–4 key terms per episode, and "Term note" → `terms.note(term)` (slides into the dock) for
   the rest. If an older scene file asks for more unveils, keep the 3–4 most central and demote
   the others to notes. Log this as a deviation. Don't pass `at=` into an occupied area, and don't set `scrim=False` over a busy
   screen. Fade a label out before new text lands where it was.
   `tools/render.py` runs every scene with `OSTEP_CHECK=1` and ends with
   **"layout check: N warning(s)"**. This check is free (text only), so use it instead of frames:
   - **Every `[overlap]` warning must be fixed** (two texts on top of each other), or justified in
     the report (e.g. a deliberate stack).
   - `[bounds]` warnings are fine only for things meant to run past the edge (full-width
     boundaries, slides in/out).
3. **Inspect visually only the critical scenes:** crowded ones with many components on screen,
   where overlaps or cut-offs are likely. Pick a few per episode. For each, Read at most **1–2
   frames** (the busiest moment, or the end state via `-s`). Check: nothing cut off, no unintended
   overlaps, text legible at 480p, "Ends with" state as specified. At most 2 fix rounds.
4. Prop preview sheets: one look at the final version.
5. Run `python tools/continuity.py <NN>` (see "Continuity" above) and fix the jumps it flags.
6. Run `python tools/silence.py <NN>` (text only, no frames). **Every scene must open with narration
   within 1 s** and no gap between captions may exceed 2.5 s; fix flagged scenes by putting the
   scene's first `say(...)` at t = 0 and running the setup animations under it (never a silent
   build-up). The tool also prints each hand-off (last caption of scene N → first caption of N+1):
   read them; if scene N+1 starts on a new subject without a bridge, fix the line (and the script).
   Also make sure labels, arrows and numbers never sit on top of each other or on another label
   (the layout check catches text/text only: for text vs. arrow, place labels with `next_to` on
   the free side), and that a counter's number sits on the same baseline as its label.
7. Check the duration against the scene's estimate (±30%). A big mismatch usually means
   narration text is missing, or the pauses are wrong.

## Step 4: assemble
- Draft episode: `python tools/render.py <NN>` renders all scenes and assembles
  `Ostep/Renders/<NN-slug>/480p15/<NN-slug>.mp4` + `.srt`.
- `--final`: `python tools/render.py <NN> -q h`, which gives 1080p60 in `.../1080p60/`.
- Add `--no-captions` for a clean version. Use `--no-render` to re-caption or re-assemble existing
  renders without re-rendering.
- For `--final`, extract ~4 frames spread over the episode and Read them as a final sanity check.

Clean up stray `media/` folders and `__pycache__` when done.

## Report
- The files created or changed (code, props, docs).
- For each scene: status (✅ rendered and verified / ⚠️ issues), the duration vs. the estimate, and the path to the draft video.
- **Continuity:** the number of boundaries `tools/continuity.py` flags, which ones are deliberate cuts.
- **Deviations** from the scene spec, and why.
- New props and expressions added to the library.
- For `--final`: the episode path, its total length, and the subtitle file.
- Open questions or suggested spec changes (e.g. "S05's chip grid reads as busy; suggest 6 chips + counter").
