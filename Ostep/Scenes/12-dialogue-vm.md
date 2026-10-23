# 12 — A Dialogue on Memory Virtualization · Scene breakdown
> Script: Ostep/Scripts/12-dialogue-vm.md · Scenes: 10 · Est. duration: ~3:55

## Visual overview
- **Core visual idea: the monster in the closet, then the first rule.** The episode is a dialogue, so
  the characters carry the story and a single prop world sits between them. It opens with a closet
  door and a looming blue Memory column (the "monster"), becomes a staircase roadmap
  (base/bounds, TLBs, page tables, modern VM), then settles on the series' signature motif, the
  **Illusion split**, now with memory: three processes that each see "their own" big memory
  (translucent) against one real Memory column (blue). The same split resolves into the two reasons
  for the illusion: a roomy address space (ease of use) and walls between processes (isolation).
- **Spoken lines are dialogue, not narration.** Full text lives in the subtitles (`.srt`). On screen a
  speech or thought bubble appears only for a punchline of at most 6 words. Otherwise the speaker
  changes expression and the other looks at them.
- Callbacks: the illusion split and virtual copies (04, 01–03), the Memory column (05+), the OS
  token and "kill the offending process" (06), the padlock (07), the recap layout (11).
- **No full unveils in this dialogue:** its terms are unveiled in 13, where they are taught (a term is unveiled once in the series). *Virtual address*, *address space*, *physical address* and *isolation* are Term notes. Episode 13's AS16 column (code, heap, free, stack) is the same region order as ours.
- Props used: Section badge, Memory, IllusionSplit, MappingArrows, GearPair, Process, Padlock,
  KernelToken, EyeIcon, TermHighlight, `book`, `x_mark`, `question_mark`, `ep_tag`, `make_translucent`.
  Characters: Professor, Student, Process. (No Computer cameo.)

### Persistent assignments
| Thing | Look | Notes |
|---|---|---|
| Process **A** | `Process(label="A", color=PROCESS_COLORS[0])` (coral) | Same as 04–11. In S08 A is the errant program. |
| Process **B** | `PROCESS_COLORS[1]` (mint) | The innocent neighbor in S08. |
| Process **C** | `PROCESS_COLORS[2]` (gold) | Third process in S06. |
| Memory (real) | `Memory(..., color=MEM_COLOR)`, solid | The one physical memory. Always solid. |
| Virtual memory | Translucent copy (`make_translucent`), dashed outline, same blue tint | Always the "pretend" look. |
| Characters (dialogue mode) | Student at **(−2.6, −1.2)**, Professor at **(2.6, −1.2)**, scale 1 (Professor `flip()`ped to face left) | S01–S03, S10. |
| Characters (corner mode) | Student at **(−5.8, −2.8)**, scale 0.75, facing right. Professor at **(5.8, −2.8)**, scale 0.75, `flip()` | S04–S09. Props own x ∈ [−4.8, 4.8], y ∈ [−2.0, 2.5]. |
| Section badge | Top-left (−6.6, 3.6): `VIRT` dot + "12 · Memory Dialogue", font 22, `DIM` | In S01, stays until S09. |
| Term unveil / note | Unveil (`terms.show`): veil, center, then dock top-right. Note (`terms.note`): slides into the dock (6.6, 3.6), no veil. | **No unveils** (13 unveils *virtual address* and *address space*). **Notes:** *virtual address* (S05), *physical address* (S06), *address space* (S07), *isolation* (S08). |

**Zones:** nothing but the badge and docked terms in y > 2.55. Scene labels sit at y ≤ 2.35. The
Illusion split uses the prop's own titles (now at y = 2.25, below the top band): "What each program sees" / "What really happens".

## Scenes

### S01 — Are we done?   (beats: B01) · ~0:15
**Purpose:** set the tone and the question that opens the part: virtualization is not over.
**Starts with:** empty (BG).
**Layout:** dialogue mode. Only the section badge besides the characters. A "NO!" glyph pops at (0, 0.9).

| # | Narration (exact words the action lands on) | On screen / animation |
|---|---|---|
| 1 | (before the first line) | Student and Professor `FadeIn` at dialogue positions, facing each other. Both neutral. Section badge `Write`s in top-left. |
| 2 | "So, are we done with virtualization?" | Student → curious, a small `question_mark` (0.4) above his head. Professor stays neutral. |
| 3 | "No!" | Professor → surprised. "NO!" (`Text`, bold, 60, `VIRT`) pops at (0, 0.9) (`GrowFromCenter` with a quick overshoot). Student jolts back (`shift` left 0.15 and back) and the "?" vanishes. |
| 4 | "Hey, no reason to get so excited." | "NO!" fades. Student → frustrated, looks at Professor. |
| 5 | "I was just asking a question. Students are supposed to do that, right?" | Student → neutral, shrugging bob (up 0.1 and back). Pause 0.5 s. |

**Characters:** Student (curious → frustrated → neutral), Professor (neutral → surprised).
**Ends with:** badge + both characters in dialogue mode.
**Implementation notes:** no crux card on purpose. Professor and Student `look_at` each other from the start.

### S02 — Good questions   (beats: B02) · ~0:20
**Purpose:** the Professor's gentle rule: a good question has some thought behind it. Student deflates.
**Starts with:** S01 end state.
**Layout:** dialogue mode. A small sailboat glyph floats above the Student at (−2.6, 0.9).

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Well, professors always say that." | Professor → explaining. A tiny sailboat (sail full, wind lines) fades in over the Student, bobbing. |
| 2 | "But what they really mean is: ask questions, if they are good questions, and you have actually put a little thought into them." | Professor stays explaining. Two small tick-boxes appear at the Professor's side, one by one: "good" then "some thought", each with a `tick_mark` (≤ 3 words each, at (0.4, 0.9) and (0.4, 0.3), font 24). |
| 3 | "Well, that sure takes the wind out of my sails." | Student → sad. The sail deflates (`Transform` to a limp shape) and the boat sinks a little. The tick-boxes fade. |
| 4 | "Mission accomplished." | Professor → happy, a small proud bob. The sailboat fades out. Pause 0.5 s. |

**Characters:** Professor (explaining → happy), Student (neutral → sad).
**Ends with:** both characters in dialogue mode, badge, nothing else.
**Implementation notes:** the sailboat is a local helper: `Polygon` sail + hull + two curved wind lines (`Arc`). Remove tick-boxes before the sail deflates so only one gag is on screen.

### S03 — The monster in the closet   (beats: B03, first part) · ~0:15
**Purpose:** "we're not done: memory is the monster".
**Starts with:** S02 end state.
**Layout:** dialogue mode. A **closet** at (0, 0.9): a `RoundedRectangle` doorframe 1.8 × 2.6 (`DIM`), a dark interior, a door panel hinged on its left edge. Inside: a mini `Memory(cells=4, width=0.9, height=1.8)` with two `EyeIcon`s on its top cell.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "In any case, we are not nearly done." | Professor → explaining. The closet (door closed) `FadeIn`s at center. |
| 2 | "You have just seen how to virtualize the CPU." | A small CPU chip (scale 0.5, `CPU_COLOR`) with a green tick floats beside the closet at (−1.9, 2.0); it docks on the left side and dims. Student → neutral. |
| 3 | "But there is a big monster waiting in the closet:" | The door creaks open (the door panel squashes toward its hinge over 1 s). Two eyes blink inside. Student → surprised; a small "!" glyph. |
| 4 | "memory." | The Memory column grows out of the dark (`scale` 1 → 1.4, slight overshoot), eyes track the Student (`look_at`). Blue light spills out. Pause 0.5 s. |

**Characters:** Professor (explaining), Student (neutral → surprised).
**Ends with:** the open closet with the Memory monster, the dimmed CPU chip at its left, characters in dialogue mode.
**Implementation notes:** the closet is a local group. The door animation is `door.animate.stretch_to_fit_width(0.25).move_to(hinge, LEFT)`. Use `EyeIcon` with `.look_at(student)`. The eyes may be plain `Circle`s if `EyeIcon` is not ready.

### S04 — The roadmap   (beats: B03, second part) · ~0:25
**Purpose:** the Professor sets expectations: start simple (base/bounds), add TLBs and multi-level page tables, end with a real VM manager. The Student is excited, not scared.
**Starts with:** S03 end state.
**Layout:** characters glide to corner mode (0.8 s). The closet fades; its Memory column shrinks to a plain column at (−5.0, 0.6). The **staircase**: four treads, each 2.0 wide, tops at y = −0.6, 0.0, 0.6, 1.2, centers x = −2.6, −0.6, 1.4, 3.4. Labels (font 22) sit above each tread.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "That sounds cool. Why is it so hard?" | Characters glide to corner mode. Student → excited. The closet and CPU chip fade; the Memory monster shrinks to a plain Memory column (scale 0.5) at (−5.0, 0.6) and loses its eyes. |
| 2 | "There are a lot of details, and you have to keep them straight in your head." | Professor → explaining. Student's head: a thought bubble with a tiny tangle of lines (a `ParametricFunction` scribble), which fades. |
| 3 | "So we start simple, with a technique called base and bounds," | Step 1 `GrowFromEdge(DOWN)`, `MEM_COLOR` fill, label "base/bounds". Memory column hops onto it (`hop_to`). |
| 4 | "and slowly add complexity." | The column climbs; steps 2, 3, 4 grow one by one (0.4 s apart), unlabeled at first. |
| 5 | "Later come TLBs and multi-level page tables." | Labels "TLBs" (step 2) and "multi-level page tables" (step 3, two lines) write in at `DIM` (opacity 0.6). |
| 6 | "We're only naming them for now." | Steps 2 and 3 dim to 0.4 opacity. A tiny "just names" tag is NOT used: the dimming says it. |
| 7 | "Eventually, we'll describe a fully functional, modern virtual memory manager." | Step 4 lights fully with label "modern VM"; the Memory column rides to the top step. |
| 8 | "Neat!" | Student → excited, a small bounce. Pause 0.5 s. |

**Characters:** Student (surprised → excited), Professor (explaining).
**Ends with:** the staircase with the Memory column on top, characters in corners.
**Implementation notes:** staircase = four `Rectangle`s sharing a baseline, a local helper. Total on-screen text ≤ 8 words. `hop_to` is the stair-climb motion.

### S05 — The first rule   (beats: B04) · ~0:25
**Purpose:** the one rule to start with: every address a program generates is a **virtual address**.
**Starts with:** S04 end state.
**Layout:** corner mode. The staircase and column fade first. Center: Process A (coral, scale 0.9) at (−3.0, 0.0); a real-looking `Memory(cells=6, width=1.2, height=3.2)` at (2.6, 0.3).

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Any tips for a poor, sleep-deprived student?" | Staircase `FadeOut`. Student → bored; three floating "z" letters (`Text`, `DIM`, sizes 20/26/32) rise above his head and fade. |
| 2 | "For the sleep, that's easy: sleep more, and party less." | Professor → happy, a quick wag of a finger (small tilt). Student → sad for a moment, the z's linger once more and fade. |
| 3 | "For virtual memory, start with this." | Professor → explaining. Process A (running) and the Memory column `FadeIn`. |
| 4 | "Every address generated by a user program is a" | A dashed arrow (translucent, `USER_COLOR`) shoots from A toward a cell of the column, with a mono label "0x200" riding on it. The arrow lands on a translucent, dashed-outline cell that is NOT the real cell (a small offset), so it looks pretend. |
| 5 | "**virtual address**." | Term note: *virtual address*. Then the dashed arrow pulses once. Pause 1 s. |

**Characters:** Student (bored → sad), Professor (happy → explaining).
**Ends with:** Process A, the dashed "0x200" arrow into a translucent cell of the Memory column; term "virtual address" docked top-right.
**Implementation notes:** pretend cell = `make_translucent` copy of one `Memory.cell` with dashed stroke. Keep A and the arrow x-range clear of the characters. The z letters are tiny glyphs, not narration text. The term is not shown before the Term note.

### S06 — An illusion   (beats: B05) · ~0:35
**Purpose:** show the illusion: each process sees its own memory, the real one is shared, and translation connects them (**physical address**).
**Starts with:** S05 end state.
**Layout:** `IllusionSplit(orientation="vertical", at=0)` with its default titles (y = 2.25). Left: three translucent tall boxes (virtual memory) at x = −4.6, −3.0, −1.4, y center 0.5, 0.9 wide × 2.8 tall, each with an "0x200" mono tag at the same height, and Processes A, B, C (scale 0.55, base y = −1.9) under them. Right: one real Memory at (3.4, 0.5), 1.6 × 3.0, six cells. A `GearPair` (scale 0.5) sits on the divider at (0, 0.5).

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "The OS is just providing an illusion." | The split's divider draws (`IllusionSplit.draw()`). Process A and the Memory column slide to their half. The titles write in. |
| 2 | "Each process thinks it has its own large, private memory." | B and C `FadeIn` at the left. Each process gets its own translucent column `GrowFromEdge(DOWN)`. The three columns shimmer (opacity 0.4 ↔ 0.8, like 04's virtual CPUs). The tall left boxes all dwarf the single real column. |
| 3 | "And with some hardware help," | The gears appear on the divider and spin (`GearPair.spin`). Professor → explaining. |
| 4 | "the OS turns those pretend addresses into real" | The three "0x200" tags (one per box) light up in each process's color. |
| 5 | "**physical addresses**," | Term note: *physical address* (slides into the dock, no veil) while three `MappingArrows` run from each "0x200" tag, through the gears, to three *different* real cells (A's coral cell near the top, B's mint in the middle, C's gold near the bottom), each cell filled with its process color (`fill_cell`). |
| 6 | "so it can find the data." | The three real cells pulse in turn (`Indicate`). Pause 0.5 s. |
| 7 | "Every address from a user program is virtual. Every address from a user program is virtual. Every..." | Student → confused, looks away (`look(DL)`), thought bubble (`thinks`): **"Every address is virtual..."** (3 words). |
| 8 | "What are you mumbling about?" | Professor → neutral, looks at Student. |
| 9 | "Oh, nothing." | Student → neutral; the thought bubble pops (`remove_bubble`). Pause 0.5 s. |

**Characters:** Professor (explaining → neutral), Student (neutral → confused → neutral).
**Ends with:** the full Illusion split (three virtual columns, gears, arrows to three real cells), term "physical address" docked, characters in corners.
**Implementation notes:** every tag reads the **same** address "0x200" on purpose, so the viewer sees three identical virtual addresses landing in three different physical places (no table, just arrows). `MappingArrows(pairs)` for the three pairs; draw with `.create()`. Use `make_translucent` on the three left `Memory` copies. The Term note needs no veil, so the arrows can draw as it slides in. The mumble is subtitles plus the 3-word bubble.

### S07 — Why the illusion? Ease of use   (beats: B06) · ~0:35
**Purpose:** the first reason: a big, contiguous **address space** is easy to program in.
**Starts with:** S06 end state.
**Layout:** the split dissolves (`IllusionSplit.merge()`, everything fades except Process A). Two panels: left (−2.8, 0.3) a **roomy** `Memory(regions=["code", "heap", ("free", 6), "stack"], width=1.8, height=3.4, addresses=False)` (translucent, virtual look); right (2.6, 0.3) a **cramped** `Memory(cells=4, width=1.2, height=1.6)` packed with five tiny colored boxes. Labels at y = −1.8, font 22: "room to spare" (left), "no room" (right). Process A is not shown here.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Why does the OS want to provide this illusion again?" | The split fades. Student → curious. A big `question_mark` (0.9) at center (0, 0.4) shrinks away. |
| 2 | "Mostly ease of use." | Professor → explaining. The roomy memory `FadeIn`s at left with its regions, faint. |
| 3 | "The OS gives each program the view that it has a large, contiguous **address space** to put its code and data into." | Term note: *address space*. The four regions glow top to bottom one at a time (code, heap, free, stack), then a thin bracket on the right side of the column labels the whole length "one big block" (3 words, font 20). |
| 4 | "So, as a programmer, you never have to ask, 'Where should I store this variable?'" | A small yellow box "x" (`mono`) drops from above into the free region (`hop_to`), settles. A `tick_mark` appears. No question mark ever shows. |
| 5 | "The space is large, with lots of room." | Pause 0.5 s; the free region softly pulses. |
| 6 | "Life gets much trickier if you have to squeeze everything into a small, crowded memory." | The bracket and label fade. The cramped memory `FadeIn`s at right with five colored boxes crammed in. A second "x" tries to enter: it bounces off (`hop_to` and back, squash), a red `x_mark` flashes. The label "no room" appears. Student → frustrated; a thought bubble: **"Where do I put x?"** (5 words). |

**Characters:** Professor (explaining), Student (curious → frustrated).
**Ends with:** roomy memory (left, "room to spare") and cramped memory (right, "no room", red x), term "address space" docked.
**Implementation notes:** `Memory(regions=...)` reuses 04/05's address-space look; the cramped memory is a tight `Memory(cells=4)` with `Square`s drawn on top. The variable box is `Text("x")` in a small `Square`. Fade the bubble before the next scene.

### S08 — Isolation   (beats: B07) · ~0:40
**Purpose:** the second reason: **isolation** and protection. One errant program must not touch another's memory, and the OS enforces that (even by killing it).
**Starts with:** S07 end state.
**Layout:** fade the two panels. Center stage: two boxes side by side. Left (−2.8, 0.2): Process A's box (coral outline) with a small Memory (mono, 0.9 × 2.0) and A standing at its base. Right (2.8, 0.2): Process B's box (mint outline), same size, with a value "7" in one of its cells.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Why else?" | Both panels fade. Student → curious. |
| 2 | "Well, **isolation** and protection are big deals too." | Term note: *isolation* (no veil). The two boxes `FadeIn` with A and B standing inside, side by side, with a gap between them. |
| 3 | "We don't want one errant program to read," | A's arm (a long coral arrow) stretches across the gap toward B's cell "7", reads it (the "7" appears next to A's box, as a copy). Professor → worried. |
| 4 | "or worse overwrite, some other program's memory, do we?" | The arrow punches the cell: "7" becomes "?!" in red, B's expression → blocked (shaken). Sweat drop at the Professor. |
| 5 | "Probably not." | Student → neutral. The damage reverses (rewind: cell back to "7", arrow retracts). A `dashed` wall `Create`s between the boxes; a `Padlock` (red, closed) clicks onto it. A's arrow bounces off the wall (`hop_to` back with squash). |
| 6 | "Unless it's a program written by someone you don't like." | Student → excited (a sly look): `look_at` A. A's arrow tries again, but harmlessly; the lock flashes. |
| 7 | "Hmm. I think we may need to add a class on morals and ethics to your schedule." | Professor → worried. A small `book` icon (title "Ethics", 1 word) pops over the Student with a "+" sign. |
| 8 | "Maybe we should. But remember, it's not me who taught us that the proper OS response to errant behavior is to kill the offending process!" | Student → excited, then a quick "hands up" bob. A `KernelToken` ("OS") drops onto A, A → `zombie`. A tiny tombstone (rounded `Rectangle` with a cross) rises where A stood. The wall and padlock stay. Professor → surprised. Pause 1 s. |

**Characters:** Student (curious → neutral → excited), Professor (worried → surprised).
**Ends with:** B's box intact on the right, a tombstone where A was, the wall with the padlock between, "isolation" docked.
**Implementation notes:** reuse the p07 `Padlock` (closed = red = protected). The OS token is `KernelToken`, as in 06's trap story ("kill the offending process" callback). The rewind is a reverse of the same animation (`.animate` back). The tombstone is a local polygon: dim `Rectangle` with a rounded top and a small cross. The `book` icon fades before the OS token enters, so only one gag is at the Student.

### S09 — Recap   (beats: B08) · ~0:15
**Purpose:** four takeaways, one clean list.
**Starts with:** S08 end state.
**Layout:** the stage clears. Header "The memory arc" (`VIRT`, font 34) at (−3.4, 2.2). Lines at x = −5.4 (left-aligned, font 30), y = 1.3, 0.4, −0.5, −1.4. One icon per line at x = 4.0. Characters in corners, both looking at the list.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "So, what do we carry into memory?" | Everything `FadeOut` (badge too). Header writes in. |
| 2 | "One: it is the next monster, and we will tame it in small steps." | Line 1 `Write`s: "1. Memory is the next monster". Icon: the closet door, slightly ajar (mini). |
| 3 | "Two: every address a program generates is virtual." | Line 2: "2. Every address is virtual". Icon: a dashed arrow with "0x200". |
| 4 | "Three: the OS, with hardware help, turns it into a real one." | Line 3: "3. OS + hardware translate it". Icon: the gears with an arrow into a Memory cell. |
| 5 | "And the reasons? Ease of use, and protection." | Line 4: "4. Why: ease of use, protection". Icon: `Padlock` (closed). Hold 1.5 s. |

**Characters:** both neutral, looking at the list.
**Ends with:** the full recap list and four icons.
**Implementation notes:** same recap layout as 11's S09, but the header is moved to y = 2.2 (inside the content zone). Total on-screen text ≈ 22 words.

### S10 — Teaser: address spaces   (beats: B09) · ~0:10
**Purpose:** hook into 13: what does a private memory look like?
**Starts with:** S09 end state.
**Layout:** characters glide to dialogue mode. Center (0, 0.6): a translucent address space (`Memory(regions=["code", "heap", ("free", 6), "stack"], width=1.8, height=3.2)`, virtual look) with a large `question_mark` above it at (0, 2.2).

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "So what does one of these private memories actually look like?" | Recap fades. Characters glide to dialogue mode. Student → curious. The translucent address space `FadeIn`s, shimmering (0.4 ↔ 0.8) under the `question_mark`. |
| 2 | "Let's find out. Next time: address spaces." | Professor → happy. Everything `FadeOut` (0.5 s). End card: a `VIRT` dot + "Next: 13 · Address Spaces" (`ep_tag` style, `TEXT`), centered. Hold 2 s. |

**Characters:** Student (curious), Professor (happy).
**Ends with:** the end card.
**Implementation notes:** the address-space regions are the same as in S07, so 13's picture continues from here. The card title matches the next episode ("13-vm-intro, Address Spaces").

## New assets needed
No new shared props. Everything below is a small local helper in the scene files.
- **Sailboat glyph** (S02): sail `Polygon` + hull + two wind arcs; a `deflate()` Transform to a limp sail.
- **Closet** (S03): frame, dark interior, hinged door panel; `.open()` animation. Memory column and `EyeIcon`s sit inside.
- **Staircase** (S04): four `Rectangle`s on one baseline, labels, per-step dim/light.
- **Tombstone** (S08): dim rounded rectangle with a cross.
- **Z glyphs / "!" / "?"**: plain `Text` or `question_mark`.
- Depends on shared assets from 05–11: `EyeIcon` (10/11), `Padlock` (p07), `KernelToken` (p06), `MappingArrows` (ov_props). If `EyeIcon` is missing, use plain `Circle`s.

## Open questions
- **The "NO!" glyph (S01), the sailboat (S02) and "z" gag (S05)** are extra gags. Keep, or trim them if the episode runs over 4 minutes?
- **S08's OS kill gag** uses `KernelToken` plus a tombstone: a visual pun on the book's joke. Is a zombie plus tombstone too dark for a light dialogue?
- **S06 (same address "0x200" in three places)** is my concrete example; the book's dialogue has no numbers. It pre-empts 13 and 15, but only visually.
- **Recap and teaser** (S09, S10) are my additions to the book's dialogue (same as 11). Keep?
- **Duration:** ~3:55 is at the top of the 2–4 min target. S04 and S08 are the candidates to trim.
