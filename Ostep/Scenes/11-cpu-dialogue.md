# 11 — Summary Dialogue on CPU Virtualization · Scene breakdown
> Script: Ostep/Scripts/11-cpu-dialogue.md · Scenes: 10 · Est. duration: ~4:05

## Visual overview
- **Core visual idea: a victory lap through the "world" of 04–10.** This is a dialogue episode, so
  the characters carry the story and the props are *quick visual callbacks* (a few seconds each)
  that appear above them as the Student mentions each idea: the CPU with a process on it, the
  User/Kernel boundary with a trap crossing it, the timer clock, the save slot, the ready Queue,
  the MLFQ stack, the spotlight, and finally the Illusion split pointing at memory.
- **Spoken lines are dialogue, not narration.** The full text of every line appears in the
  subtitles (`.srt`). On screen, a speech bubble is used only for a short punchline (a few words);
  otherwise the speaking character just changes expression and looks toward the other.
- Every callback prop is a **miniature of the version in the earlier episode** (same colors, same
  look), at about 60% scale, so the viewer recognizes it at a glance. Nothing new is taught.
- Props used (from the bible and `ostep_lib`): Section badge, CPU, Process, User/Kernel boundary
  (`UserKernelBoundary`), Privilege gauge, Clock icon, Save slot, Terminal, Queue, Timeline,
  Spotlight, System stack, Tip card, Illusion split, Memory, Term highlight, hand icon, name_tag,
  x_mark / tick_mark, seesaw (built from primitives, see New assets). Characters: Professor, Student,
  Process (and a Computer cameo is *not* used).

### Persistent assignments
| Thing | Look | Notes |
|---|---|---|
| Process **A** | `Process(label="A", color=PROCESS_COLORS[0])` (coral) | Same as 04. Plays the long job in the gum gag. |
| Process **B** | `PROCESS_COLORS[1]` (mint) | The short job. |
| Process **C** | `PROCESS_COLORS[2]` (gold) | Third process in MLFQ and Queue callbacks. |
| Process **D** | `PROCESS_COLORS[3]` (sky) | Only the "gullible neighbor" in S08. |
| CPU home | `CPU_COLOR` chip at **(0, 0.8)** in callback scenes (scale 0.8) | A running process stands on top of it, as in 04. |
| Characters (dialogue mode) | Student at **(−2.6, −1.2)**, Professor at **(2.6, −1.2)**, scale 1 (Professor `flip()`ped to face left) | S01 and S10 only. |
| Characters (corner mode) | Student at **(−5.8, −2.8)**, scale 0.75, facing right. Professor at **(5.8, −2.8)**, scale 0.75, `flip()` | S02–S09. Props own the center stage (x −4.5..4.5, y −2.0..3.0). |
| Section badge | Top-left (−6.6, 3.6): `VIRT` dot + "11 · Summary Dialogue", font 22, `DIM` | Appears in S01, stays until S09. |
| Term highlight | As in 04: (0, 2.9), font 54, `VIRT` underline, then docks top-right (6.6, 3.6) at font 26 | Used for: *mechanisms*, *limited direct execution*, *resource manager*. |
| Speech/thought bubbles | `says()` / `thinks()`, font 30, only for punchlines of ≤ 6 words | Never for full lines. |

Timeline state encoding is the series standard (running solid, ready outline, blocked `DIM` + clock,
idle hatched). Mini timelines here follow it exactly.

## Scenes

### S01 — A loaded question   (beats: B01) · ~0:15
**Purpose:** set the tone: a relaxed wrap-up between Professor and Student, and the one question the episode answers.
**Starts with:** empty (BG).
**Layout:** characters in dialogue mode. Nothing else on screen except the section badge.

| # | Narration (exact words the action lands on) | On screen / animation |
|---|---|---|
| 1 | (before the first line) | Student and Professor `FadeIn` at dialogue positions, facing each other (`look_at` each other). Both neutral. Section badge `Write`s in top-left: `VIRT` dot + "11 · Summary Dialogue". |
| 2 | "So, Student. Did you learn anything?" | Professor stays neutral, looks at Student. A small floating "?" glyph pops above the Student's head. |
| 3 | "That's a loaded question. I think you only want me to say 'yes.'" | Student → bored. Thought bubble above Student: **"yes?"** (`thinks`), with a tiny roll of the pupils (`look(UP)` then back). |
| 4 | "True. But it's still an honest question. Give a professor a break, will you?" | Professor → happy. Thought bubble fades. A tiny shrug: Professor bobs up 0.1 and back. |
| 5 | "Okay, okay. I did learn a few things." | Student → neutral, then a short nod (0.2 down and back). Pause 0.5 s. |

**Characters:** Student (neutral → bored → neutral), Professor (neutral → happy).
**Ends with:** badge + both characters in dialogue mode.
**Implementation notes:** no crux card on purpose (a dialogue chapter has no CRUX box). The "?" is `question_mark()` at 0.4 units.

### S02 — The machinery   (beats: B02, first part) · ~0:25
**Purpose:** recall the three mechanisms of limited direct execution by *showing* them, one per phrase.
**Starts with:** S01 end state.
**Layout:** characters glide to corner mode (0.8 s). Center stage is a 3-panel strip: left panel at (−3.2, 0.8) the **User/Kernel boundary** (mini, y = 0.8 with a small process above), middle panel at (0, 0.8) the **CPU + clock**, right panel at (3.2, 0.8) the **save slot** with two processes. Panels are unframed, ~2.6 wide each, revealed one by one.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "First, how the OS virtualizes the CPU." | Characters glide to corners. Student → curious, looks up at the stage. The CPU chip (scale 0.8) `GrowFromCenter`s at center (0, 0.8) with Process A standing on it (running). |
| 2 | "There were a bunch of important **mechanisms**:" | Term highlight "mechanisms". The gear icon (`GearPair`, scale 0.5) appears next to the CPU and spins once. The CPU fades to 30% and slides to the middle panel. |
| 3 | "traps and trap handlers," | Left panel: dashed User/Kernel boundary draws (`USER_COLOR` above, `KERNEL_COLOR` below). A small process above `cross`es down through it, a flash on the line, then the label "trap handler" appears in the kernel half and the process returns up. |
| 4 | "timer interrupts," | Middle panel: the CPU returns to full opacity with Process A running. A `ClockIcon` ticks beside it; the ring flashes `KERNEL_COLOR`; A hops off the CPU. |
| 5 | "and how the OS and the hardware carefully save and restore state when switching between processes." | Right panel: a save slot icon. A's colored registers stream into the slot (0.6 s), then B's stream out of a second slot onto the CPU; B hops on. A mini "save / restore" double arrow appears. |
| 6 | "Good, good!" | Professor → happy. Panels pulse once together (`Indicate`). Pause 0.5 s. |

**Characters:** Student (neutral → curious), Professor (happy at the end).
**Ends with:** three mini panels (boundary, CPU+clock, save slot) across the stage, the term strip "mechanisms" top-right, characters in corners.
**Implementation notes:** reuse the real props at scale ~0.6 (`UserKernelBoundary(y=0.8)` constrained to the left third, `CPU`, `ClockIcon`, `save_slot`). The three panels are a single `VGroup` so S03 can fade them as one.

### S03 — No substitute for doing   (beats: B02, second part) · ~0:15
**Purpose:** the Professor's advice: learning this takes hands-on work, not just reading.
**Starts with:** S02 end state.
**Layout:** the three panels shrink toward the top (y = 2.2, scale 0.5). A **Terminal** at center (0, 0.1), 5.2 × 2.2.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "It all seems a little complicated, though. How can I learn more?" | Student → confused, "?" above. The three panels shrink and rise (0.8 s) to make room. |
| 2 | "There's no substitute for doing." | Professor → explaining. The Terminal `FadeIn`s; prompt `$ make test` types in (`Terminal.type`). |
| 3 | "Do the class projects, and I bet by the end it will all make sense." | Test lines print one by one, each with a green `tick_mark`: "trap ... ok", "timer ... ok", "switch ... ok". The three mini panels above light up in turn as their tests pass. Student → curious, then a slow nod. |

**Characters:** Student (confused → curious), Professor (explaining).
**Ends with:** Terminal (3 green ticks) center; panels docked small at the top; characters in corners.
**Implementation notes:** keep terminal text ≤ 5 short lines. The script's "Sounds good." line was cut, so the Student's nod carries it.

### S04 — The paranoid OS   (beats: B03) · ~0:35
**Purpose:** show the philosophy: run programs *fast*, but stay in charge, which is why the OS is a resource manager.
**Starts with:** S03 end state.
**Layout:** Terminal and panels fade. Center stage: the **User/Kernel boundary** across the screen at y = 0.4 (privilege gauge at the right, x = 5.0). CPU chip at (−2.2, 1.6) *in user space*; a **System stack** slice (a `KERNEL_COLOR` band) below the boundary at y = −1.4.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Did you get a sense of the philosophy of the OS?" | Terminal and panels `FadeOut`. The boundary draws full width (`UserKernelBoundary.draw()`), user half in `USER_COLOR` tint, kernel half in `KERNEL_COLOR` tint. Professor → thinking. |
| 2 | "I think so. The OS is fairly paranoid." | Student → neutral. A kernel-colored eye glyph (two circles + pupil, primitives) appears in the kernel band and **looks around** (pupil sweeps left, right). |
| 3 | "It wants to stay in charge." | The eye's pupil locks on the CPU chip. A thin `KERNEL_COLOR` crown/ring pulses around the chip. |
| 4 | "It wants a program to run as efficiently as possible, and hence **limited direct execution**." | Term highlight "limited direct execution". Process A (coral) runs directly on the CPU. The boundary stays quiet, no OS arrows. A speed-gauge needle goes to full. |
| 5 | "But it also wants to say 'Ah! Not so fast, my friend' to an errant or malicious process." | A rogue process (Process D, sky, with a red outline, running) tries to leave the CPU's lane for the kernel band. The timer ring flashes and a `hand` icon slams down in front of it; it bounces back (`hop_to` backwards, squash). Student's bubble: **"Not so fast!"**. |
| 6 | "Paranoia rules the day." | The eye glows brighter; the privilege gauge reads KERNEL for 0.5 s then back to USER. |
| 7 | "Perhaps that's why we think of the OS as a **resource manager**." | Term highlight "resource manager". The System stack slice expands: Hardware row (CPU, Memory, Disk) at the bottom, the `KERNEL_COLOR` OS band above, the processes on top; the band glows. Student → curious. |
| 8 | "Yes indeed. You're starting to put it together." | Professor → proud. A small "puzzle piece" snaps in between the hardware and process rows (`GrowFromCenter`). Pause 1 s. |

**Characters:** Professor (thinking → proud), Student (neutral → curious).
**Ends with:** the System stack (hardware row, OS band, processes), the boundary dimmed, term strip "resource manager".
**Implementation notes:** `hop_to` reversed for the bounce. The puzzle piece is a simple `Polygon` with a notch. The eye glyph is built from `Circle`s. The rogue process reuses `Process("running")` with a red `outline_of` overlay.

### S05 — Short jobs first   (beats: B04, first part) · ~0:25
**Purpose:** land the SJF lesson through the Student's joke: the short job should go first.
**Starts with:** S04 end state.
**Layout:** the System stack shrinks away. A **Queue** at center (0, 0.2) labeled "Checkout", with a **cashier counter** (a small rectangle + tiny card terminal) at the left end (−3.8, 0.2). The mini **Timeline** at (0, −1.8), x −3..3, rows A and B.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "And the policies on top of those mechanisms? Any lessons there?" | System stack fades. A `Spotlight` icon appears above the center, with a small "which?" tag. Professor → explaining. |
| 2 | "Bumping short jobs to the front of the queue." | The Queue draws with A (coral, tall/wide, "long") first and B (mint, small, "short") behind it. B hops over A to the front of the queue (`Queue.insert` at slot 0). The spotlight tracks B. |
| 3 | "I knew that was a good idea the day I was buying gum…" | Student's thought bubble: a stick of gum + a tiny cashier. The Queue relabels: B = "gum". |
| 4 | "…and the guy ahead of me had a credit card that wouldn't work." | The Queue reverts (B behind A). A sits at the counter; a red `x_mark` flashes above the card terminal; A's expression → blocked; a tiny clock spins. The timeline shows A's wide `blocked`/running block while B's `ready` outline waits. |
| 5 | "He was no short job, let me tell you." | A's block on the timeline keeps growing; "B waits ..." hatch; Student → frustrated. Beat. |
| 6 | "That sounds oddly rude to that poor fellow. What else?" | Professor → worried. A gets a small apologetic sweat-drop (the Process `blocked` look). Pause 0.5 s. |

**Characters:** Professor (explaining → worried), Student (curious → frustrated).
**Ends with:** the checkout queue with A at the counter and B waiting, the mini timeline, spotlight dimmed.
**Implementation notes:** adapts the convoy picture from 07 (A long, B and C short). The "gum" label is a `Text` swapped on B. A mini counter is a `RoundedRectangle` + small `Rectangle`. Reuses `Queue.insert`.

### S06 — MLFQ and the scheduler wars   (beats: B04, second part) · ~0:25
**Purpose:** MLFQ as "SJF + RR in one", then the CFS/BFS/O(1) controversy as a squabble.
**Starts with:** S05 end state.
**Layout:** center-left (−1.8, 0.6): a mini **MLFQ stack**, three stacked queue rows (Q2 top, Q0 bottom), 4 wide. Center-right (3.2, 0.6): three name tags in a loose triangle.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "That you can build a smart scheduler that's like SJF and round robin at once." | The checkout fades. Two small labeled icons appear, "SJF" (spotlight) and "RR" (looping arrow, `loop_arrow`), side by side; they slide together and merge (`Transform`) into the MLFQ stack. Student → excited. |
| 2 | "MLFQ was pretty neat." | Process C (gold) enters at the top row, runs, drops one level (`hop_to`), runs, drops again. Process B (short, mint) enters, finishes at the top row. |
| 3 | "But a real scheduler seems difficult." | The stack gets two extra rules (small gears with sparks) and slightly wobbles. Student → confused. |
| 4 | "Indeed. Look at the Linux battles between CFS, BFS and the O(1) scheduler." | Professor → explaining. Three `name_tag`s "CFS", "BFS", "O(1)" fade in on the right; they bump and shove each other (small shakes, little dust puffs from `puff`). |
| 5 | "And no, I will not spell out the full name of BFS." | Under the "BFS" tag, a long grey bar of text writes in, covered at once by a black censor bar with a `x_mark`. Professor looks away with a stubborn face (`neutral`, look UP). |
| 6 | "And I won't ask you to!" | Student → excited; a quick thumbs-up shape (`hand`). Pause 0.5 s. |

**Characters:** Student (excited → confused → excited), Professor (explaining → neutral).
**Ends with:** MLFQ stack at left, three name tags at right, censor bar over BFS.
**Implementation notes:** `Queue` rows reused for MLFQ levels; the same MLFQ visual as ep 08 at ~60%. The censor bar is a `Rectangle` over a `Text` of 6 grey lines.

### S07 — Is there a right answer?   (beats: B05) · ~0:35
**Purpose:** metrics conflict (turnaround vs response), so the goal is to avoid disaster, not find "the best".
**Starts with:** S06 end state.
**Layout:** everything fades. Center (0, 0.6): a **seesaw** (a plank on a triangle fulcrum), labels "turnaround" (left end, `PROCESS_COLORS[0]`) and "response" (right end, `PROCESS_COLORS[1]`). Two mini timeline strips (3 processes each) under the two ends at y = −1.0. The Tip card slides in at the right.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "These policy battles could rage forever. Is there really a right answer?" | Name tags and MLFQ fade. A large "?" glyph appears at center and the Student → confused. |
| 2 | "Probably not." | The "?" shrinks to the seesaw's fulcrum; Professor → thinking. |
| 3 | "Even our own metrics are at odds." | The seesaw `FadeIn`s level. Labels "turnaround" (left) and "response" (right). |
| 4 | "A scheduler that's good at turnaround time is bad at response time, and vice versa." | The plank tips left (turnaround down = good, so a green tick at left); the left mini timeline shows jobs running back to back (FIFO-style) and the right one shows a long first wait (a hatched gap) with a red `x_mark`. Then the plank tips the other way: the right timeline becomes interleaved slices (RR-style), the left shows long stretched finish times. A subtle `DoubleArrow` between the ends pulses. |
| 5 | "As Lampson said, perhaps the goal isn't to find the best solution, but to avoid disaster." | Tip card (`TipCard`, title "LAMPSON") slides in from the right: **"Don't find the best. Avoid disaster."** (6 words). The seesaw settles to level with a small green ring around the fulcrum. |
| 6 | "That's a little depressing." | Student → sad (head droops). Seesaw dips a little. |
| 7 | "Good engineering can be that way. It can also be uplifting." | Professor → happy. The seesaw bobs up and down once like a playground toy, a tiny sparkle at each end. |
| 8 | "I think being pragmatic is a good thing: not every problem has a clean, easy solution." | Professor → explaining. Pause 1 s. The Tip card stays. Student → neutral. |

**Characters:** Student (confused → sad → neutral), Professor (thinking → happy → explaining).
**Ends with:** the seesaw (level) with the two mini timelines, Tip card "Avoid disaster" at right.
**Implementation notes:** the seesaw is `Polygon` (fulcrum) + `Rectangle` (plank) rotated by `Rotate` about the fulcrum. Mini timelines use `Timeline` (3 rows, 6 ticks) at scale 0.5, with the standard state encoding. Keep to ≤ 25 words of text at once.

### S08 — Lighting fires   (beats: B06) · ~0:35
**Purpose:** gaming the scheduler (the MLFQ trick), the Professor's "I created a monster" joke, and the "light a fire" payoff.
**Starts with:** S07 end state.
**Layout:** seesaw, timelines and card fade. Center-left (−2.2, 0.8): the MLFQ stack from S06 at the same scale. Top-right (3.6, 2.4): a **server_rack** icon labeled "EC2".

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Anything else that caught your fancy?" | The seesaw scene fades out; the MLFQ stack returns at the left. Professor → neutral, looks at Student. |
| 2 | "Gaming the scheduler!" | Student → excited. The MLFQ rows glow. Process D (sky, "gullible neighbor") sits in the lower row; Process C (gold, "the gamer") sits at the top row with sunglasses (small `Line`s over the face). |
| 3 | "I might try it next time I run a job on Amazon's EC2." | A cloud-ish rounded rectangle + `server_rack` slides in at top-right with the label "EC2". C's glasses glint. |
| 4 | "Steal some cycles from some unsuspecting, and more importantly OS-ignorant, customer." | C does the MLFQ trick: each time its slice ends, a tiny disk blip (the `Disk.spin()` mini icon) fires, and C stays on the top row, climbing back up (`hop_to`). A tiny coin / cycle token slides from D's row to C. D's row gets a small tear. D → blocked look. |
| 5 | "I might have created a monster." | Professor → surprised. A grey stitched Process (zombie expression, bolts on the neck as two small rectangles) walks in from the right edge (`FadeIn` + shift). |
| 6 | "Professor Frankenstein is not what I'd like to be called." | The monster raises its arms; a small "Prof. Frankenstein" name tag drops above the Professor; Professor → worried. |
| 7 | "But isn't that the idea? To get us excited enough to look into it on our own? Lighting fires and all that?" | The monster fades. Student → curious. A small **flame** icon appears above Student's head (`GrowFromCenter`) and flickers: *light a fire*. |
| 8 | "I guess so. But I didn't think it would work!" | Professor → worried, then a short wry smile (`happy`). The flame flickers. Pause 1 s. |

**Characters:** Professor (neutral → surprised → worried → happy), Student (excited → curious).
**Ends with:** MLFQ stack, "EC2" rack, the flame over the Student; monster gone.
**Implementation notes:** the "gaming" mini-demo reuses the MLFQ rows and `hop_to`; it lasts ~5 s and does not re-teach the trick. The stitched "Frankenstein" is a `Process("zombie")` with two small `Rectangle`s as neck bolts. The flame is two overlapping `Polygon`s with a flicker updater (a new simple icon).

### S09 — Recap   (beats: B07) · ~0:20
**Purpose:** four takeaways of the CPU-virtualization arc, as one clean list.
**Starts with:** S08 end state.
**Layout:** the stage clears. A numbered list at the left (−5.4 .. 1.0), font 30, one line each; one icon per line at x = 4.0 (y = 1.8, 0.6, −0.6, −1.8). Characters stay in corners; the Student and Professor both look at the list.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "What do we carry out of the CPU section?" | Everything `FadeOut`. Header "The CPU arc" in `VIRT`, font 34, `Write` at (−3.4, 2.8). |
| 2 | "One: mechanisms give the OS control while programs run at full speed." | Line 1 `Write`s: "1. Mechanisms: control, at full speed". Icon: the User/Kernel boundary with a process crossing. |
| 3 | "Two: the OS is paranoid on purpose." | Line 2: "2. The OS is paranoid on purpose". Icon: the `hand`. |
| 4 | "Three: policies trade one goal against another." | Line 3: "3. Policies trade goals off". Icon: the seesaw (mini). |
| 5 | "Four: sometimes the aim is just to avoid disaster." | Line 4: "4. Aim to avoid disaster". Icon: the Tip card ring/fulcrum. Hold 1.5 s. |

**Characters:** both neutral, looking at the list.
**Ends with:** the full recap list and four icons; section badge fades out.
**Implementation notes:** the same recap layout as 04's S21. Keep each line ≤ 6 words (total ≈ 22 words with the header).

### S10 — Teaser: next, memory   (beats: B08) · ~0:15
**Purpose:** hook into 12: the same illusion trick, now for memory.
**Starts with:** S09 end state.
**Layout:** characters move to dialogue mode. Center-top (0, 1.6): the **Illusion split** (vertical divider, left "What each program sees", right "What really happens") with three small processes at left, each inside a translucent tall box (its own big memory), and a single **Memory** column at right (MEM_COLOR).

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "So the CPU is sorted out." | The recap fades. Characters glide to dialogue mode. Student → curious. |
| 2 | "What about memory? Does every process get its own, too?" | The Illusion split draws. Left: three processes A, B, C (coral, mint, gold) each with its own translucent memory column; right: one real Memory column (blue). Student's "?" above; the three left columns shimmer (0.4 ↔ 0.8) like the virtual CPUs in 04. |
| 3 | "The same trick, on a different resource." | Professor → happy. The CPU chip from 04's S02 flicks in beside the Memory column for 1 s, then the peach icon (callback to 01–03) briefly sits in the middle. |
| 4 | "Next time." | `FadeOut` everything (0.5 s). The end card: "Next: 12 · Dialogue on Memory Virtualization" in `TEXT` with a `VIRT` dot. Hold 2 s. |

**Characters:** Student (curious), Professor (happy).
**Ends with:** black end card.
**Implementation notes:** the Memory column is `Memory(regions=..., title="memory")`, reused. The "shimmering virtual boxes" are `make_translucent` copies. Use `ep_tag` style for the end card text.

## New assets needed
All of these are small primitives. Nothing else is new.
- **Seesaw(left_label, right_label)**: plank + triangle fulcrum, `.tip(side)`, `.level()` animations. Used in S07 and S09.
- **Flame glyph**: two overlapping polygons (orange/yellow) with a flicker updater. Used in S08.
- **Eye glyph** (paranoid OS): two circles + pupil with a `.look(direction)` animation. Used in S04.
- **Puzzle-piece / censor-bar helpers**: one polygon with a notch, one rectangle overlay. Trivial; can be local to the scene file.
- **Monster accessory:** neck bolts on `Process("zombie")`. Local to S08.
- (Optional) Student "happy" expression: not needed here; used excited/neutral/curious instead.

## Open questions
- **Callback props are miniatures of 06–10.** Their exact look depends on what the parallel agents build (boundary, MLFQ stack, spotlight). If any differ from what I described, S02, S06 and S08 need small touch-ups.
- **Process roles in the gum gag (S05):** A (coral) = long customer, B (mint) = short, to match the usual A/B/C of the scheduling episodes. Fine?
- **Spoken lines and bubbles:** dialogue lines are subtitles only; bubbles are reserved for punchlines (≤ 6 words). Is that the right balance, or do you prefer full-line speech bubbles?
- **Recap and teaser** (S09, S10) are extras to the book's dialogue. Keep, or end on "I didn't think it would work!"?
- **Frankenstein monster (S08)** reuses the zombie Process. Cute, or too much for an already busy scene?
- **The "steal cycles" joke:** kept as in the book, with the Professor visibly worried. OK?
