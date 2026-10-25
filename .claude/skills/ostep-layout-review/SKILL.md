---
name: ostep-layout-review
description: Find and fix components drawn on top of each other in an OSTEP episode's rendered scenes (labels hidden under props, cards overlapping cards or the crux strip, things touching the Student/Professor, text on lines), using the shape-aware layout check, a contact sheet for ambiguous cases, and allow_overlap for deliberate ones. Use when the user reports overlapping/clipped/blocked elements, or asks to review or clean up an episode's layout, e.g. "/ostep-layout-review 05", "check overlaps in episode 06 S03-S07".
---

# OSTEP layout review: overlapping components

You make an episode's scenes free of **unintended** overlaps, and you change nothing else. The
check finds candidates; you decide, fix, and re-check. Only real problems are changed; deliberate
overlaps get an explicit `allow_overlap` so they are never reported again.

## Arguments
- Episode (number, slug or path), resolved in `Ostep/Manim/`.
- Optional scene selection: `S05`, `S05-S07`, `S03,S09`. The default is all scenes.

## Read first
1. `ostep_lib/layout.py` (module docstring): what each finding kind means, what is ignored on
   purpose, and the roles (chrome, host, panel, actor, prop, background, ignore).
2. `Ostep/README.md` §5 "Screen zones" (the reserved zones) and the bible's layout rules.
3. The scene files you will touch, and the episode's `common.py` (state builders: a fix to a
   scene's end state must also go into the builder the next scene starts from).

## Step 1: run the check (no video, no images)
Before anything else, record the starting point: `python tools/continuity.py <NN>` (so later you
can tell your regressions from old sub-pixel jumps), and `python -m py_compile` the scene files
(one syntax error stops the run and the remaining scenes go unchecked).
```
python tools/render.py <NN> --check-only --scenes S03,S04,S05
```
Run it **in the foreground with a long timeout** (up to 10 min per call), **a few scenes per
call**: a scene can take 1–3 min and nothing is printed until the call ends, and background jobs
you wait on can stall you. Read the printed lines, not the files: a scene with no findings leaves
no `.jsonl`. `[bounds]` lines are a different check (things crossing the frame edge); ignore them
unless something is cut off by mistake.
This runs every scene as a Manim dry run with the layout check on and writes the findings to
`Ostep/Renders/<ep>/480p15/layout/<stem>.jsonl`. Each printed line is
`[overlap:<kind>] t=<s> <A> x <B> box=(x0,y0)-(x1,y1)`, where A is drawn below B:

| kind | meaning | almost always |
|---|---|---|
| `cover` | a text is partly hidden by B (card, CPU pins, a box border, an arrow, a dot) | real |
| `text` | two different texts on top of each other | real |
| `line` | a text sits on a line or border | real |
| `edge` | a text straddles the edge of a filled shape | real |
| `chrome` | something touches the crux strip/card, badge or docked term | real |
| `host` | something touches the Student or Professor | real |
| `panel` | two panels partly overlap, or a creature/CPU partly overlaps a panel | real |
| `spill` | a card's own text (title, label) sticks out past the card's edge | real: shrink/wrap the text or widen the card |
| `zone:chrome`, `zone:host` | content inside the thin reserved margin around them | real (crowding) |

Also printed: `[ghost] t=<s> FadeOut(X) re-shows something that is not on screen`. A FadeOut,
`.animate` or other remover targets a mobject that already left, so Manim adds it back and it
flashes on screen for the length of that animation. Always real: drop that animation (or, to reuse
the mobject, place it and `FadeIn` it on purpose).

Labels name the objects: texts by their content (spaces removed), others by class, role and
center, e.g. `CPU[prop]@(-2.0,0.6)`.

## Step 2: triage, cheaply
- Group findings by root cause (one misplaced label often produces 2–3 lines).
- **Decide from the code when you can**: read the scene at that moment (the `t` and the box tell
  you where). A label placed with `move_to` onto a prop, a card positioned over the strip's
  y-range, a creature landing on a label: those are clear. No image needed.
- **Ambiguous ones only** (could be a deliberate composition: a plug landing in its slot, an icon
  laid on a card on purpose): make one contact sheet and look at it:
  ```
  python tools/overlap_sheet.py <NN> --scenes S06,S10 --kinds cover,edge
  ```
  It prints a numbered list and writes `layout/sheet_<n>.png` (crops with the overlap outlined in
  red, 12 per sheet). Read at most **2 sheets** per episode. Delegate the viewing to a Sonnet
  subagent if the user asks for frugality: it returns "real / deliberate" per number.

## Step 3: fix the real ones
Edit scene files with the Edit tool (they have CRLF line endings; scripted `str.replace` edits
easily turn `
` escapes into real newlines).

Prefer the smallest change that removes the overlap without touching anything else:
- **Labels**: put them on a free side with `next_to(target, direction, buff=0.1–0.15)`; never
  `move_to` a label onto something. Labels of creatures that sit on a CPU go to the side or
  above, not between the creature and the CPU.
- **Creature labels** (`Process(label=...)`) are part of the creature: they sit under its feet
  and are rebuilt by every `change()` / `set_expression`. To keep one off a CPU, a rail or a
  queue tube, drop the built-in label for that stretch and show a separate `Text` beside the
  creature (bring the label back once it's on free ground). `z_index` set on a creature is lost
  when it rebuilds: set layers on the static prop instead. When a pool/spotlight hides a label,
  move the pool; reordering layers just turns `cover` into `line`.
- **Panels / cards**: move or shrink them into free space, or fade the old one out before the new
  one comes in. Never let content enter the crux strip's area or a host's area (the reserved
  zones): move the content, or fade the strip out (`FadeOut(strip)`) for that stretch and back in.
- **Bubbles / overlays that cover content**: place them where nothing is, or dim the content
  first on purpose (then `allow_overlap`).
- **Highlights**: size and place a highlight box from its target (`SurroundingRectangle(target,
  buff=0.06)`), not from a separately computed shape.
- Keep continuity: if you move something that persists across a cut, update the `common.py`
  builder the next scene starts from, so both sides still match.
- **Deliberate overlaps**: keep them and declare them in the scene, right where they are built:
  `self.allow_overlap(a, b, "plug lands in its slot")` (`b=None`: `a` with anything). Use it
  only for compositions that are clearly intended; say which in your report.

## Step 4: verify
1. `python tools/render.py <NN> --check-only --scenes <changed scenes>`: the fixed findings are
   gone and no new ones appeared. At most 2 fix rounds per scene; report what is left.
2. Re-render the changed scenes for real (`python tools/render.py <NN> --scenes ...`), then
   re-assemble the episode (`python tools/render.py <NN> --no-render`).
3. `python tools/continuity.py <NN>`: your moves didn't create jumps at cuts.
4. Optionally one contact sheet of the changed spots (`overlap_sheet.py` with the new findings
   file, or frames you pick) to confirm visually.

## Report
- Findings before → after, per scene (counts by kind).
- Each fix in one line (scene, what moved where), and each `allow_overlap` with its reason.
- Anything left unfixed and why (e.g. a library animation: suggest the library change).
- Commit only the episode's files (and library files you changed on purpose) with the commit
  trailer from the session's instructions.
