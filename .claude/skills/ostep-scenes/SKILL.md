---
name: ostep-scenes
description: Turn an OSTEP episode script (Ostep/Scripts/*.md) into a detailed scene breakdown that specifies exactly what is on screen, how it animates and how visuals sync with narration, ready to be implemented in ManimCE. Use when the user asks to define/plan/break down the scenes, storyboard, or visuals for a chapter's script, e.g. "make the scenes for chapter 4" or "/ostep-scenes 04-cpu-intro".
---

# OSTEP script → scene breakdown

You turn an episode script into a **storyboard in words**. It has to be precise enough that someone
(or a later coding step) can implement every scene in ManimCE with `ostep_lib` without
inventing anything. Every concept is **explained visually**: the picture should teach even with
the sound off, and the narration should feel like it's describing what the viewer is watching.

## Inputs

- The argument identifies the episode (number, slug, or script path). Resolve it in
  `Ostep/Scripts/`. If no script exists, stop and suggest running `ostep-script` first.
- Read **all** of these first:
  1. `Ostep/README.md`, the series bible: palette, layout, characters, recurring props. Follow it
     strictly. Reuse props before inventing new ones.
  2. `ostep_lib/README.md`: available characters, expressions and API. Only use expressions
     that exist. If a needed prop or expression doesn't exist yet, specify it in
     "New assets needed" rather than silently assuming it.
  3. The script, fully.
  4. The chapter PDF when you need details: exact figures, code listings, numbers. The book's
     figures are often the best starting point for a diagram; note which figure you adapt.
  5. The previous episode's scene file, if any, for visual continuity.

## Process

1. **Map beats to scenes.** A scene is one continuous visual setup, the unit that becomes one
   Manim `Scene` class or a section of one. Usually 1 beat → 1–3 scenes. Every beat must be covered.
2. **Design the visual explanation first, then the choreography.** For each concept ask: what
   picture makes this obvious? Prefer *showing the mechanism move*: processes walking onto the
   CPU, a trap crossing the user/kernel line, addresses being translated as arrows. Avoid
   *labels describing it*. Use transformations to show that one representation becomes
   another. Keep consistent spatial meaning: the same thing stays in the same place and color.
3. **Choreograph against narration.** Split the narration into chunks and attach each animation
   to the exact words it lands on. Leave pauses after reveals.
4. **Track screen state.** Every scene starts from the previous scene's "state at end". Nothing
   appears or disappears without an animation. Watch clutter: at most ~3 focal elements at once.
   **Remove before you add:** when a label, caption or title has served its beat, fade it out in the
   row where the next text appears, so old text never lingers under new text.
5. **Respect the screen zones** (bible §5, "Screen zones"). The top band (y > 2.55) belongs to the
   chrome: section badge, docked crux strip, docked term. Never place scene titles, captions or
   labels there. Never write a term "at the top" over existing content.
   **Terms come in two strengths.** Use the unveil (scene veils, term written at center, then docks)
   for the episode's **3–4 key terms** only: the ones the crux hinges on. Write it as
   "Term unveil: *X*", and never use two in neighbouring rows. Every other new term gets
   "Term note: *X*": it slides into the top-right dock, with no veil. Minor vocabulary needs neither;
   it is spoken and shows up in the captions. In the Visual overview, list the key terms you chose.
   A term is unveiled **once in the whole series**, in the episode that teaches it. Dialogue and
   recap episodes, and callbacks in later episodes, use notes.
6. **The crux is read aloud.** A crux card or strip on screen always has narration: the Narrator says
   the question inside a natural lead-in ("So, the crux is: <question>"; vary it, don't repeat a
   mechanical "The crux:") while the card writes, then reads the card's follow-up text as it fades
   in. Give those their own table rows (narration column = the spoken lead-in plus the exact question on the card), then dock.
   A crux that only changes in the docked strip (a second crux) is read too.
7. **Scenes talk to each other, and start talking at once.** Row 1 of every scene is narration that
   starts at t = 0 (no silent opening while props are being laid out; animate the setup *under*
   that line). That line must bridge from the last line of the previous scene (recall what was
   just said or left open, then say what this scene is about). Add a **Bridge:** line to each
   scene ("S10 follows S09's 'where do the actions come from?': opens with 'So what can the OS do
   with a process? A short menu…'"). If the script lacks the bridge, add it to the scene's
   narration and report the script change. No scene may begin with a bare topic word.
   **On-screen text discipline:** only the few key concepts get a big center unveil; every
   other label is small and placed where it can't touch another label or arrow (say which side
   each label goes on when elements are close).
8. **Make hand-offs exact.** "Ends with" must list every persistent element with its exact position
   and state: hosts (mode: corner or dialogue, and expression), badge, docked term, crux strip,
   and each prop's place. The next scene's "Starts with" is a verbatim copy of it. A scene that
   deliberately starts from a different screen says so ("cut to empty"). Characters always sit at
   the library's standard host positions (`host_pair` modes) unless a row says they move.
9. **Self-check:** sound-off test (does the visual alone teach?), color/prop consistency with the
   bible, characters only in corners/edges and only reacting to beats, no text walls
   (≤ ~25 words on screen), every term's first appearance uses a Term unveil (3–4 key terms) or a
   Term note (the rest).

## Output

Write `Ostep/Scenes/<NN-slug>.md` (same name as the script). If it exists, ask before
overwriting. Structure:

```markdown
# <NN> — <Chapter title> · Scene breakdown
> Script: Ostep/Scripts/<NN-slug>.md · Scenes: <count> · Est. duration: <mm:ss>

## Visual overview
- Core visual metaphor(s) of the episode and how they evolve.
- Props used (from the bible) and the persistent color/label assignment (e.g. Process A = PROCESS_COLORS[0]).

## Scenes

### S01 — <title>   (beats: B01) · ~0:25
**Purpose:** what the viewer should understand by the end of this scene.
**Starts with:** <screen state, or "empty">
**Layout:** where things are (center diagram, characters in corners, top bar…), with rough
positions (e.g. "CPU at center-left (-3, 0)", "ready queue along the bottom, y = -2.5").

| # | Narration (exact words the action lands on) | On screen / animation |
|---|---|---|
| 1 | "Imagine you're running…" | `FadeIn` laptop outline at center; Student enters bottom-left (curious). |
| 2 | "…a browser, a game, music…" | Three app icons pop out of the laptop one by one (`GrowFromCenter`, 0.3 s apart). |
| 3 | (pause 1 s) | — |

**Characters:** who is on screen, expression changes and when.
**Bridge:** how the first line picks up the previous scene's last line.
**Ends with:** exact screen state handed to the next scene.
**Implementation notes:** Manim hints: mobjects, ordering, tricky animations, which book figure is adapted.

(… more scenes)

## New assets needed
- Props / expressions / helpers that don't exist in `ostep_lib` yet, with a short spec.

## Open questions
- Visual choices you want the user to confirm.
```

When you finish, tell the user the file path, the scene count with one line per scene,
the new assets needed, and the open questions.
