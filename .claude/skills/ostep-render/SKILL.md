---
name: ostep-render
description: Implement an OSTEP episode's scene breakdown (Ostep/Scenes/*.md) as ManimCE code using ostep_lib, render it, visually verify the frames, and assemble the episode video with subtitles from the script's narration. Use when the user asks to code, animate, implement, render or build the video for a chapter or for specific scenes, e.g. "render episode 04", "/ostep-render 04 S05-S07", "/ostep-render 04 --final".
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

## Read first
1. `Ostep/README.md`: palette, layout, props, motion rules.
2. `ostep_lib/README.md`, plus the source of anything you'll use (`ostep_lib/style.py`,
   `ostep_lib/characters/*`, `ostep_lib/props/*` if it exists). Use the real API; don't guess.
3. `Ostep/Scenes/<NN-slug>.md`: the whole file, especially "Visual overview" (persistent
   assignments), the selected scenes, and "New assets needed".
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
Ostep/Renders/<NN-slug>/
  <NN-slug>.mp4         # assembled episode (--final only)
  <NN-slug>.srt         # subtitles from the narration
```
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

### `ostep_lib/narration.py` (create once if missing)
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
- Keep it simple and robust: prefer `Transform`, `FadeIn/Out`, `Create`, `Write`, `MoveAlongPath`,
  updaters only where needed. No external images or SVGs.
- If the spec is ambiguous or physically impossible (things overlap, don't fit, contradict each
  other), choose the closest sensible version and log it under **Deviations** in your report.

## Step 3: render and verify (token-frugal)
Images are expensive, so frame inspection is the exception, not the rule.
1. Draft render every scene: `python -m manim -ql Ostep/Manim/<NN-slug>/sXX_<slug>.py SXX<Title>`.
   It must run without errors. **Don't Read frames by default.**
2. **Catch layout problems in code.** Use `next_to`/`arrange` with buffers. Assert, or print, that
   key mobjects stay inside the safe area (x ∈ [−6.6, 6.6], y ∈ [−3.6, 3.6]). Check bounding boxes
   for overlaps between the main elements.
3. **Inspect visually only the critical scenes:** crowded ones with many components on screen,
   where overlaps or cut-offs are likely. Pick a few per episode. For each, Read at most **1–2
   frames** (the busiest moment, or the end state via `-s`). Check: nothing cut off, no unintended
   overlaps, text legible at 480p, "Ends with" state as specified. At most 2 fix rounds.
4. Prop preview sheets: one look at the final version.
5. Check the duration against the scene's estimate (±30%). A big mismatch usually means
   narration text is missing, or the pauses are wrong.

## Step 4: assemble (`--final` only)
1. Render every scene with `-qh`.
2. Concatenate in scene order with ffmpeg's concat demuxer into `Ostep/Renders/<NN-slug>/<NN-slug>.mp4`
   (re-encode, `-c:v libx264 -pix_fmt yuv420p`, if the inputs' parameters differ).
3. Merge the per-scene `.srt` files into `<NN-slug>.srt`, offsetting each by the cumulative
   durations (read them with `ffprobe`).
4. Extract ~4 frames spread over the episode and Read them as a final sanity check.

Clean up stray `media/` folders and `__pycache__` outside `Ostep/Renders/` when done. Use
`--media_dir` pointing into the scratchpad for drafts, so the project stays clean.

## Report
- The files created or changed (code, props, docs).
- For each scene: status (✅ rendered and verified / ⚠️ issues), the duration vs. the estimate, and the path to the draft video.
- **Deviations** from the scene spec, and why.
- New props and expressions added to the library.
- For `--final`: the episode path, its total length, and the subtitle file.
- Open questions or suggested spec changes (e.g. "S05's chip grid reads as busy; suggest 6 chips + counter").
