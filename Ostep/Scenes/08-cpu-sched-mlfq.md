# 08 — Scheduling: The Multi-Level Feedback Queue · Scene breakdown
> Script: Ostep/Scripts/08-cpu-sched-mlfq.md · Scenes: 18 · Est. duration: ~14:00

## Visual overview
- **Core metaphor: a ladder of queues.** The ready `Queue` from 04/07 grows into a stack of horizontal
  lanes: the top lane is the highest priority, the bottom lane the lowest. The CPU sits to the right of the
  ladder and always serves the highest non-empty lane. Process creatures *climb and sink* between lanes, which
  makes "priority changes with behavior" physical. A small **allotment gauge** (a fuel bar on the running
  process) drains while it runs and decides when it sinks.
- **Second visual: the level-versus-time chart** (the book's Figures 8.2–8.6). A `Timeline` whose *rows are
  the queue levels* (Q2, Q1, Q0) and whose blocks are colored by *job*. The audience sees the ladder (what the
  scheduler knows right now) above, and the chart (what happened) below, filling in sync.
- **Third visual: the rulebook.** A panel on the right that starts empty at the crux and *accumulates*
  Rules 1 → 5. Rules that get replaced (4a/4b → 4) visibly `Transform`. When a rule fires in an animation, its
  line glows. This is the spine of the episode: every new rule enters as the fix to a flaw.
- **Signature recurring prop: Spotlight** (policy, from 04) picks the job on the highest lane. **Stopwatch**
  icon = time period `S`. **Padlock** = the security tip.
- Props used (from the bible): Crux card, Tip/Aside card, Term highlight, Section badge, CPU, Queue, Timeline,
  Spotlight, Process, stopwatch, padlock, keyboard, ClockIcon, tick_mark/x_mark, Terminal (for `nice`), `ep_tag`.
  Characters: Professor, Student, Process (no Computer in this episode, except as an optional cameo in S01).

### Persistent assignments
| Thing | Look | Notes |
|---|---|---|
| Job **A** | `Process(label="A", color=PROCESS_COLORS[0])` (coral) | The **long, CPU-bound** job in every example (matches A in 04/07). In Figure 8.1 it is simply "a job at the top". |
| Job **B** | `PROCESS_COLORS[1]` (mint) | The **short / interactive** job; also the **gamer** in S13 (it plays at being interactive). |
| Job **C** | `PROCESS_COLORS[2]` (gold) | Second interactive job (S11), and the middle job in Figure 8.1. |
| Job **D** | `PROCESS_COLORS[3]` (sky) | Only in Figure 8.1 (S03–S04), at the bottom. |
| CPU | `CPU_COLOR` chip 1.2 × 1.2 at **(2.0, 1.3)** in "ladder" mode; the running job stands on its top edge | |
| Ladder lanes | 8-lane mode (S03–S04): y = 2.8 − 0.6·i, x −6.0..0.2, jobs at scale 0.35. 3-lane mode (S06 onward): **Q2 y = 2.3, Q1 y = 1.3, Q0 y = 0.3**, jobs at scale 0.6. Lane label at x = −6.4 ("Q2", "Q1", "Q0"), "high priority ↑" / "low priority ↓" in `DIM` at the left edge. Lane = thin rounded rectangle, `DIM` stroke 1; the lane being served has `CPU_COLOR` stroke. | Same job colors; lanes stay neutral so job colors pop. |
| Timeline | `Timeline(rows=["Q2","Q1","Q0"], ticks=20, x_range=(-4.4, 3.4), top=-0.9, row_height=0.45)`; one tick = 10 ms; tick labels in ms (0, 50, 100, …); block color = job color via `fill(row, tick, "running", color=job_color)` | Figures 8.2–8.4 span 200 ms; 8.5 and 8.6 span 300 ms (`ticks=30`, same x-range). |
| Rulebook | Right panel x 3.4..6.7, y 3.1..−0.8; header "MLFQ rules" (font 24, `VIRT`), one line per rule (font 20, ≤ 9 words), tag "R1", "R2"… in `VIRT` at the left | Appears in S02 (empty), fills across the episode. |
| Characters (corner mode) | Student at **(−6.1, −2.8)**, scale 0.75, facing right. Professor at **(6.1, −2.8)**, scale 0.75, `flip()` | Default. "Dialogue mode" (S01, S18): Student (−2.6, −1.2), Professor (2.6, −1.2), scale 1. |
| Section badge | Top-left (−6.6, 3.6): `VIRT` dot + "08 · MLFQ", font 22, `DIM` | Appears in S02, stays to S17. |
| Term highlight | As in 04: font 54 at (0, 2.9), `VIRT` underline, then shrinks to the top-right (6.6, 3.6) | Every bolded term's first appearance. |

The **Timeline state encoding** is the series standard from the bible. Here only "running" is used for
blocks (colored by job); blocked jobs show the clock glyph next to their lane position instead of timeline cells.

## Scenes

### S01 — Two jobs, no labels   (beats: B01) · ~0:50
**Purpose:** feel the problem: two jobs that look identical but are very different, and neither of the two known
policies is good without knowing which is which.
**Starts with:** empty.
**Layout:** two wrapped "mystery boxes" at center, left (−2, 1.8), right (2, 1.8); the box at the right is 3× bigger. Characters in dialogue mode (enter at the start). A small SJF/RR scoreboard in the upper-right later.

| # | Narration (exact words the action lands on) | On screen / animation |
|---|---|---|
| 1 | "Two jobs just arrived at the scheduler." | Two identical grey boxes with a "?" slide in from the top into a spotlight cone (`Spotlight`, pointing at the gap between them). |
| 2 | "One of them is tiny: a keystroke, an echo on the screen, done in a blink." | The left box pulses; a small keyboard icon flashes next to it with a tiny "1 ms" tag, then the tag is covered by a "?". |
| 3 | "The other will grind through numbers for an hour." | The right box, drawn larger, gets a stopwatch whose hand spins, tag "1 hour", then it too is covered by a "?". |
| 4 | "From the outside, they look exactly the same." | Both tags show "?" and the boxes are pulled to the same size and look. Hold 1 s. |
| 5 | "Easy. Shortest job first, like last time." | Student enters (curious) and speaks. A mini SJF icon (the "SJF" tag from 07) appears above the left box. |
| 6 | "If we knew which one was which. SJF and STCF need each job's length *in advance*, and the OS almost never has it." | Professor enters (thinking). The SJF tag gets a red X (`x_mark`) and a small caption "needs job length?". |
| 7 | "Fine. Round robin, then." | Student (frustrated). A round-robin ring (two arrows in a circle) replaces the SJF tag. |
| 8 | "Round robin keeps **response time** low: the keyboard feels snappy." | Professor (explaining). A small response-time arrow from "arrive" to "first run" shrinks to short under the ring; a green tick. |
| 9 | "But it drags every job out, so **turnaround time** is awful." | The turnaround arrow ("arrive" to "done") stretches long; a red cross. |
| 10 | "So we're stuck." | Student (confused). The two tags (SJF: X, RR: half-check) sit side by side. |
| 11 | "Not stuck. We can't see the future. But we *can* watch the past." | Professor (happy). The "?" boxes fade; a rewind clock arrow (counterclockwise) draws between them. Pause 1 s. |

**Characters:** Student (curious → frustrated → confused), Professor (thinking → explaining → happy).
**Ends with:** the rewind arrow in the middle, both characters in dialogue mode. Next scene wipes it.
**Implementation notes:** reuse the SJF / RR icons from 07 if they exist, or simple text tags ("SJF", "Round Robin"). Don't spend effort on the boxes: rounded squares with a `?` glyph (`question_mark`).

### S02 — The Crux   (beats: B02) · ~0:30
**Purpose:** pose the question; announce the build: five rules, each fixing the last.
**Starts with:** S01 end state.
**Layout:** Crux card centered (0, 0.8), 9 × 3. Rulebook skeleton lower-right.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | (transition) | The rewind arrow and the boxes fade. Characters glide to corner mode. Crux card `Write`s in the `VIRT` frame: header "THE CRUX", question in bold: **"How to schedule without perfect knowledge?"** Subtitle (`DIM`, smaller): "Low response time for interactive jobs, low turnaround time, and no a priori knowledge of job length." |
| 2 | "Today's answer is one of the most famous ideas in scheduling: the **Multi-Level Feedback Queue**, or **MLFQ**." | Term highlight "MLFQ" (full name below it in `DIM`). |
| 3 | "It was first described in 1962, in the Compatible Time-Sharing System…" | A small era tag "1962 · CTSS" slides in under the card (an `EraRibbon` marker could be reused, but a plain tag is enough). |
| 4 | "…and it helped earn its creator, Fernando Corbato, the Turing Award." | The tag gains a small gold medal glyph and "F. Corbato · Turing Award". |
| 5 | "We'll build it in five rules." | The card shrinks to a one-line strip at the top-center (0, 3.2); the Section badge "08 · MLFQ" appears. The **rulebook** panel draws on the right with five empty numbered slots "R1 … R5". |
| 6 | "Each one is the answer to a problem with the one before." | A tiny arrow chain between the slots (R1 → R2 → … → R5) draws, with the label "each fixes the last" in `DIM`. Hold 1 s. |

**Characters:** corner mode; Student looks at the card (`look_at`), Professor neutral.
**Ends with:** section badge, the crux strip on top, an empty rulebook panel at right.

### S03 — The ladder of queues   (beats: B03) · ~0:50
**Purpose:** MLFQ = several queues at different priority levels; a ready job sits on one; the scheduler serves the highest non-empty one. Adapt **Figure 8.1**.
**Starts with:** S02 end state. The crux strip fades out at the start of this scene; the rulebook stays (empty).
**Layout:** 8 lanes (Q8 at the top, Q1 at the bottom, y = 2.8 − 0.6·i), x −6.0..0.2. "high priority" and "low priority" labels at the left. The CPU at (2.0, 1.3). Tip card later covers the lower-right.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "MLFQ doesn't have one ready queue." | A single ready `Queue` (the one from 04/07: A, B, C, D standing in a row, labeled "Ready") appears at the center-left. |
| 2 | "It has several, each at a different **priority level**." | The queue splits into eight horizontal lanes stacked vertically (the row is stretched/`Transform`ed into lane rectangles); labels Q8 … Q1 `Write` down the left. Term highlight "priority level". |
| 3 | "A job that's ready to run sits on exactly one of them…" | The jobs A, B, C, D (scale 0.35) hop one at a time into lanes: A and B into Q8, C into Q4, D into Q1 (**Figure 8.1**). |
| 4 | "…and the scheduler picks from the highest queue that has anything in it." | A **Spotlight** from above slides down the ladder and stops on the Q8 lane; the CPU chip `GrowFromCenter` at (2.0, 1.3) and a bright arrow runs from the Q8 lane to it. |
| 5 | "Picture a ladder. In the book's first figure there are eight queues." | Arrows "high priority ↑ / low priority ↓" draw at the left. The whole ladder gets a slight wobble (`Indicate`) as if a ladder. |
| 6 | "Jobs A and B sit at the top, C in the middle, D at the bottom." | `Indicate` A and B, then C, then D in turn (0.5 s each). |
| 7 | "And the big idea: the scheduler will *learn* from history." | Student (curious). A history clock arrow (counterclockwise) draws beside the CPU; Term "learn from history" is written in `TEXT` at (0, 3.3). |
| 8 | "What a job did a moment ago tells us what it will probably do next." | A small trace strip (a few colored blocks) slides left-to-right out of a job, with an arrow "→ next?" at its end. |
| 9 | "Branch predictors and caches do this too." | Tip card ("TIP: LEARN FROM HISTORY", `DIM` frame) slides in from the right over the lower-right area (x 1.8..6.6, y −2.4..0.2) with two tiny icons: a fork glyph (branch predictor) and a small cache grid. |
| 10 | "But careful: when the past is a bad guide, such a system can decide worse than one with no knowledge at all." | Professor (worried). On the tip card, the history trace is followed by a "wrong guess" red X over its arrow. Pause 1 s. Student → neutral. |

**Characters:** Student (curious), Professor (explaining → worried).
**Ends with:** the 8-lane ladder with A, B (Q8), C (Q4), D (Q1) and the CPU; the Tip card still visible, to be slid out at the start of S04.
**Implementation notes:** build the ladder as eight `Queue` instances (labeled Q8…Q1). Adapt Figure 8.1 literally: jobs shown as circles in the book; we use process creatures at scale 0.35 with only the face visible; labels A–D beneath each.

### S04 — Rules 1 and 2   (beats: B04) · ~0:45
**Purpose:** Rule 1 (priority wins) and Rule 2 (equal priority → round robin); the cost: lower queues starve.
**Starts with:** S03 end state; the Tip card slides out at the start.
**Layout:** same ladder. A short `Timeline` (single row "CPU") appears at the bottom y = −2.0, x −4.4..3.4, 8 ticks.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Rule one: if the priority of A is greater than the priority of B, A runs, and B doesn't." | Rulebook line **R1: If Priority(A) > Priority(B), A runs (B doesn't).** `Write`s. In the ladder, A hops on the CPU (→ running); a second job (C, from Q4) shakes its head and stays (a small "✕ not now" puff). The Q8 lane glows in `CPU_COLOR`. |
| 2 | "Rule two: if A and B have the *same* priority, they take turns, round robin." | R2 writes: **If Priority(A) = Priority(B), A and B run in RR.** A is swapped for B on the CPU (hop), then back; a circular arrow appears between A and B in the Q8 lane. |
| 3 | "That's the same time-slice rotation we already know." | A one-second callback chip "RR · time slice (Ep. 07)" `ep_tag("← Ep. 07")` at the lane. |
| 4 | "So with this picture, A and B alternate forever." | The CPU timeline row fills A, B, A, B, A, B, A, B (coral, mint alternating, 0.3 s each). The `Spotlight` stays at the Q8 lane. |
| 5 | "And C and D?" | The camera of attention moves down: `Indicate` C (Q4), then D (Q1). Their faces droop (ready → still ready; add "zZ" over them). |
| 6 | "They never run! That's an outrage." | Student (frustrated). A big "starved?" text pops over C/D and disappears. |
| 7 | "It is, and we'll come back to it." | Professor (worried). A tiny bookmark glyph appears on the rulebook, next to R1/R2, labeled "starvation → later". |
| 8 | "But first: with priorities this rigid, everything depends on where each job sits. So who decides that?" | A question mark appears over the ladder as a whole, with the lane arrows (up/down) pulsing. Pause 1 s. |

**Characters:** Student (frustrated), Professor (worried).
**Ends with:** ladder with A, B (Q8), C, D; rulebook with R1, R2; CPU timeline of 8 alternating ticks (to be removed in S05).
**Implementation notes:** Timeline here has one row ("CPU"), not the 3-row level chart. A throwaway `Timeline(rows=["CPU"], ticks=8)`.

### S05 — Priorities that change   (beats: B05) · ~0:45
**Purpose:** the central idea: priority is not fixed; it varies by observed behavior. Interactive vs. CPU-bound.
**Starts with:** S04 end state; the CPU timeline fades at the start. The ladder shrinks into 3-lane mode, i.e. C, D and the lanes between merge (Q8..Q1 collapse via `Transform` into Q2, Q1, Q0; A and B jump into Q2, C into Q1, D into Q0) while the Student asks.
**Layout:** the 3-lane ladder (Q2 y = 2.3, Q1 y = 1.3, Q0 y = 0.3). Below it two "behavior strips" at y = −0.8 (job B) and y = −1.8 (job A), x −5..3.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "So who sets the priorities?" | Student (curious). |
| 2 | "Nobody sets them once and for all." | Professor (explaining). The numbers "Priority = 7" etc. that floated near each job crumble and fade (they were static labels). |
| 3 | "The key to MLFQ is that it *varies* a job's priority based on what it does, its **observed behavior**." | Term highlight "observed behavior". The up and down arrows beside the ladder start pulsing. |
| 4 | "A job that keeps giving up the CPU to wait for the keyboard smells interactive…" | Strip for **B** (mint): short colored bursts, then a keyboard icon and a gap, repeating. Label "gives up the CPU often". |
| 5 | "…so MLFQ keeps its priority high." | B glides to the top lane (Q2) with a small up-arrow. Label "interactive". |
| 6 | "A job that burns the CPU for long stretches smells like a batch job…" | Strip for **A** (coral): one long unbroken bar growing. Label "uses the CPU for long stretches". |
| 7 | "…so MLFQ lowers its priority." | A sinks to the bottom lane (Q0), down-arrow. Label "CPU-bound". |
| 8 | "The scheduler *infers* which is which, from history." | The history clock arrow from S03 reappears between the two strips and "infers" is written in `TEXT` with an arrow pointing to the lane. Hold 1 s. |

**Characters:** Student (curious), Professor (explaining).
**Ends with:** 3-lane ladder with B on Q2 and A on Q0 (C and D fade out when the ladder collapses); rulebook R1, R2; the behavior strips fade at the end of the scene.
**Implementation notes:** the book (Fig 8.1) only shows static queues. This scene is original; it is the visual core of "feedback".

### S06 — Attempt #1: allotment, Rules 3 and 4   (beats: B06) · ~0:55
**Purpose:** introduce **allotment** and the first version of the priority-change rules: Rule 3, 4a, 4b.
**Starts with:** S05 end state, with the ladder cleared of jobs (all jobs exit via `FadeOut`) and the level-time `Timeline` drawn at the bottom (rows Q2, Q1, Q0; 20 ticks).
**Layout:** ladder at the top, CPU at (2.0, 1.3), `Timeline` bottom (top = −0.9), rulebook right.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "To turn this into rules, we need one new concept: the **allotment**." | Term highlight "allotment". The Timeline slides up from the bottom and the 3-lane labels Q2, Q1, Q0 appear on both ladder and timeline. |
| 2 | "It's the amount of time a job can spend at a given priority level before the scheduler lowers its priority." | A job A (coral) appears on the CPU with an **allotment gauge**: a small horizontal bar (width 1.2, `TEXT` outline) above its head, full (`CPU_COLOR` fill). Label "allotment". The gauge drains in 1.5 s; a down-arrow forms when empty. |
| 3 | "To keep things simple, we'll say for now that the allotment is exactly one time slice." | A small tag "allotment = 1 time slice = 10 ms" next to the gauge; a ruler brace spans the first timeline cell, labeled "10 ms". |
| 4 | "Rule three: when a job enters the system, it starts at the highest priority, the topmost queue." | R3 writes in the rulebook: **A new job enters at the top queue.** A new job (B, mint) drops from the top of the screen into Q2. |
| 5 | "Rule four, part A: if a job uses up its allotment while running, it moves down one queue." | R4a: **Used its allotment? Move down one queue.** B on the CPU, its gauge drains, B slides from Q2 to Q1 (arrow). |
| 6 | "Rule four, part B: if a job gives up the CPU, for example for an I/O, *before* its allotment is up, it stays where it is, and its allotment is reset." | R4b: **Gave up the CPU early? Stay put; allotment resets.** B on the CPU, gauge half drained; B hops off to a clock icon (blocked, ClockIcon) and back; the gauge snaps to full, B stays in the same lane. |
| 7 | "So a job that keeps the CPU too long gets punished, and a job that's polite gets to stay?" | Student (curious). R4a gets a down-arrow glyph, R4b a "reset" circular arrow. |
| 8 | "Exactly. Let's watch it work." | Professor (happy). Jobs clear; the Timeline is empty and ready. |
| 9 | "From now on we use three queues, which the book calls Q2, Q1 and Q0, and a ten-millisecond time slice." | The labels Q2, Q1, Q0 `Indicate`; a tag "slice = 10 ms" docks next to the CPU. |

**Characters:** Student (curious), Professor (happy).
**Ends with:** empty 3-lane ladder, CPU at (2.0, 1.3), empty level-time `Timeline` (20 ticks = 200 ms), rulebook R1–R4b, slice tag.
**Implementation notes:** the allotment gauge is a new prop (see New assets): a `Rectangle` outline plus an inner fill whose width is a `ValueTracker`. The rulebook is a new prop. Keep the rule text short: the narration says the full wording.

### S07 — Example 1: a single long job   (beats: B07) · ~0:45
**Purpose:** a long job drifts to the bottom queue and stays. **Figure 8.2**.
**Starts with:** S06 end state.
**Layout:** unchanged.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "First example. One long-running job, A, alone in the system." | Example tag "Example 1: one long job" (top-center, `DIM`). A (coral, expression ready) waits above the ladder. |
| 2 | "It arrives in the top queue, Q2." | A drops into Q2 (R3 glows). The Spotlight points at the Q2 lane. |
| 3 | "After ten milliseconds, it has used its allotment, so it moves down to Q1." | A hops onto the CPU (→ running), the gauge drains; the Timeline fills tick 1 in row Q2 (coral). A slides to Q1 (R4a glows). |
| 4 | "Another ten milliseconds, and it moves down again, to Q0." | Tick 2 fills in row Q1; A slides to Q0. |
| 5 | "And there it stays, running in the lowest queue until it's done." | A stays on the CPU; ticks 3–20 fill quickly in row Q0 (0.1 s each, accelerating), the bottom row becoming a long solid coral bar. No more drain animation: the gauge is hidden once in Q0. |
| 6 | "Pretty simple." | Hold 1 s. The Timeline matches Figure 8.2: coral blocks at ticks 1 (Q2), 2 (Q1), 3–20 (Q0). |

**Characters:** corner mode; both neutral. (No reaction needed.)
**Ends with:** the finished Figure 8.2 on the Timeline, A on the CPU in Q0. Example tag stays.
**Implementation notes:** for fidelity the book's graph shows only the three levels in black; our version colors the blocks coral. Tick labels read 0, 50, 100, 150, 200 (ms).

### S08 — Example 2: along came a short job   (beats: B08) · ~1:00
**Purpose:** MLFQ approximates SJF without knowing job lengths. **Figure 8.3 (left)**.
**Starts with:** S07 end state, with the Timeline rewound to the state at 100 ms: ticks 1 (Q2), 2 (Q1) and 3–10 (Q0) are coral; the rest is empty.
**Layout:** unchanged; a "now" marker on the Timeline at 100 ms.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Now a more interesting one. A is still running in the lowest queue." | Example tag "Example 2: a short job arrives". The Timeline's blocks from ticks 11–20 disappear (rewind, 0.8 s). A is on the CPU in Q0. A "now" marker sits at 100 ms. |
| 2 | "At time one hundred milliseconds, B arrives. B is an interactive job, and it only needs twenty milliseconds of CPU." | B (mint) drops from the top of the screen toward the ladder. A tag "needs 20 ms" with a 2-cell work bar (▮▮) appears on B. |
| 3 | "Rule three puts B in the top queue." | B lands in Q2; R3 glows. |
| 4 | "By Rule one, B beats A, so B runs." | R1 glows. A hops off the CPU, back to Q0 (→ ready); B hops on (→ running). The Spotlight moves from Q0 to Q2. Timeline: tick 11 fills in row Q2 (mint). |
| 5 | "Ten milliseconds later, B has used its allotment, and it moves down to Q1." | B's gauge drains; B slides to Q1 (R4a glows). Tick 12 fills in row Q1 (mint). |
| 6 | "Ten more, and B is *finished*, before it ever reaches the bottom." | Second work cell empties; B → done (check mark) and fades; the Q1 lane flashes. |
| 7 | "Now A resumes where it left off." | A hops back onto the CPU. Ticks 13–20 fill in row Q0 (coral). |
| 8 | "Wait. We never told the scheduler B was short!" | Student (excited). A callout "never told it!" with an arrow at B's tag; the "needs 20 ms" tag is crossed out to show the scheduler never saw it. |
| 9 | "Right. That's the beauty of it." | Professor (proud). |
| 10 | "Since MLFQ can't know whether a job is short or long, it first *assumes* it might be short, and gives it high priority." | A thought bubble over the Spotlight, text "probably short?". B at the top, spotlighted. |
| 11 | "If it really is short, it runs quickly and completes. If it isn't, it sinks down the queues and proves itself a long, batch-like job." | Two small branching mini-diagrams above the ladder: a job finishing at the top (check) vs. a job sinking from Q2 to Q0 (down arrow). |
| 12 | "In this way MLFQ approximates SJF." | A tag "≈ SJF" built as `MathTex(r"\approx")` + "SJF" appears under the ladder in `TEXT`. Hold 1.5 s. |

**Characters:** Student (excited), Professor (proud).
**Ends with:** Figure 8.3 (left) on the Timeline: A Q2/Q1/Q0 up to 100, B at ticks 11–12 (Q2, Q1), A continuing in Q0 ticks 13–20; A on CPU in Q0; the "≈ SJF" tag.
**Implementation notes:** the book colors A black and B gray; we use coral and mint. Reuse the Timeline's `unfill_ticks` for the rewind.

### S09 — Example 3: what about I/O?   (beats: B09) · ~0:45
**Purpose:** a job that does I/O stays at the top (Rule 4b), and the interactive job stays snappy. **Figure 8.3 (right)**.
**Starts with:** S08 end state; the Timeline cleared (`clear_blocks`), the example tag swapped; A is in Q0 on the CPU for the time being.
**Layout:** unchanged. The Timeline now needs ~1 ms slivers: it has the same 200 ms span, with thin rectangles (width ≈ 0.04 tick) in row Q2.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Third example: I/O." | Example tag "Example 3: interactive job with I/O". A in Q0 (it already sank at the start; ticks 1–2 pre-filled as in Example 1 for realism). |
| 2 | "Suppose B, the interactive job, only needs one millisecond of CPU before it asks for input, and it's competing with the long job A." | B (mint) enters at Q2 with a keyboard icon beside it and a tag "1 ms of CPU, then input". |
| 3 | "B runs for one millisecond and then blocks." | B hops on the CPU (A steps off). A sliver fills in row Q2. B hops off to a ClockIcon waiting spot ("blocked", expression blocked); the gauge shows only a sliver drained. |
| 4 | "That is giving up the CPU before the allotment is used up." | The gauge glows with 90% still full; a small bracket labeled "used 1 of 10 ms". |
| 5 | "So Rule four B applies: B stays at the same priority level." | R4b glows. B returns to Q2 (not lower) once the clock icon spins down. |
| 6 | "Each time B comes back from its I/O, it's still at the top, still ahead of A." | Loop three times: A runs in Q0 (a long bar grows in row Q0), B comes back, takes the CPU, a sliver in Q2, clock, back. The pattern fills the Timeline to 200 ms: a comb of slivers in Q2 and long bars in Q0 (match Figure 8.3 right). |
| 7 | "The interactive job stays snappy, which is exactly the goal." | A tick mark (`tick_mark`) appears at B; a tag "response time: low" in `DIM` under the Q2 row. Hold 1 s. |

**Characters:** none react. Student looks at the Timeline (`look_at`).
**Ends with:** Figure 8.3 (right) on the Timeline; B in Q2, A in Q0; rulebook R1–R4b.
**Implementation notes:** needs sub-tick slivers on the `Timeline` (see New assets). If that is hard, draw the slivers as plain thin `Rectangle`s at the row's y, x computed from `tick_x`. The "blocked" spot is a small ClockIcon just left of the CPU at (0.9, 2.3).

### S10 — Three problems   (beats: B10) · ~1:05
**Purpose:** reveal three flaws of the current rules: starvation, gaming, and changing behavior; frame them as the next three fixes.
**Starts with:** S09 end state. The Timeline and the ladder shrink (0.6 scale) and move to the upper-left (x −5..−1, y 1.5..3.2) as a "so far" thumbnail; the rulebook stays at the right. Three card slots fill the middle (x −1..3.4).
**Layout:** three cards stacked left to right under the thumbnail: Card 1 (x −4.6), Card 2 (x −0.7), Card 3 (x 3.2); each 3.6 × 3.4, at y = −0.6.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "So we have a basic MLFQ. Short and interactive jobs fly, and long ones share what's left." | Student (excited). The rulebook gets a thin green outline. |
| 2 | "But it has serious flaws." | Professor (worried). The green outline turns red and cracks lines appear across the rulebook. |
| 3 | "Can you spot them? Pause the video, and think as deviously as you can." | Professor (thinking). A stopwatch icon with a 5-second countdown (a ring) — a small `progress_ring`, drawing for 3 s. Student (confused) looks at it. |
| 4 | "First: **starvation**." | Term highlight "starvation". Card 1 slides in: a long coral job at the bottom lane, and a wall of mint and gold interactive jobs crowding the top lane. |
| 5 | "With too many interactive jobs, they consume *all* the CPU, and long jobs never get any." | The CPU on Card 1 is a tiny chip fed by the mint/gold stream; coral A looks at it from below, with a "zZ" and a growing waiting counter "0 ms of CPU". |
| 6 | "Second: a smart user can **game the scheduler**, tricking it into giving them more than their fair share." | Term highlight "game the scheduler". Card 2 slides in: a job with a mask/dark sunglasses glyph (simple) and an allotment gauge. |
| 7 | "Rule four B is the hole. Just before the allotment is used up, issue an I/O, and you keep your priority." | R4b on the rulebook glows red. On Card 2, the gauge reaches 99%; an "I/O" button is pressed; the gauge snaps back to full (R4b reset) and the job stays at the top. |
| 8 | "Do that at ninety-nine percent of the allotment, every time, and one job can nearly monopolize the CPU." | A repeat loop (3×) with a small pie chart appearing at the corner: the gamer's slice of the CPU grows to ~99%, the others shrink. |
| 9 | "On a shared server, that's a **security** problem." | Professor (worried). A Tip card ("TIP: SCHEDULING MUST BE SECURE FROM ATTACK", `DIM` frame, with a padlock icon) slides in under Card 2, with a tiny data-center rack icon (`server_rack`). |
| 10 | "Scheduling policy has to resist attack." | The padlock locks (click). |
| 11 | "Third: programs change." | Card 3 slides in: a coral job on the bottom lane with a "Phase 1: compute" label. |
| 12 | "A CPU-bound job may become interactive, but with our rules it's stuck at the bottom." | The job grows a keyboard icon and starts "wanting" interactive bursts (a thin sliver pattern), but remains on the bottom lane; an up-arrow with a red X. Student (frustrated). Pause 1 s. |

**Characters:** Student (excited → confused → frustrated), Professor (worried → thinking → worried).
**Ends with:** the three cards visible (labels: "starvation", "gaming", "behavior changes"), the Tip card on Card 2, the rulebook with the red outline.
**Implementation notes:** keep the cards flat and cheap: three rounded rectangles with a few primitives. The pie chart is a `Sector`-based mini pie. The countdown ring is an existing icon (`progress_ring`).

### S11 — Attempt #2: the priority boost   (beats: B11) · ~1:00
**Purpose:** Rule 5 fixes starvation (and behavior change). **Figure 8.4**, left (no boost) vs. right (boost every 100 ms).
**Starts with:** S10 end state; cards 2 and 3 fade, Card 1 (starvation) grows to fill the stage and shrinks back into the ladder + Timeline layout from S06 (the ladder returns to its 3-lane position, the Timeline back to the bottom, 20 ticks).
**Layout:** ladder at the top with A (coral) on Q0, B (mint) and C (gold) arriving at 100 ms; Timeline bottom; rulebook right. A stopwatch icon above the CPU for `S`.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Let's fix starvation first." | Professor (explaining). The word "starvation" from S10 shrinks into the top bar. |
| 2 | "What if we guarantee that every job makes *some* progress?" | A "some progress" glyph (a small coral progress bar nudging a few percent). |
| 3 | "Simple idea: every so often, throw everybody back in the top queue." | The stopwatch icon over the CPU spins; at its ring completing, all jobs on the ladder are lifted by a big up-arrow into Q2 (`LaggedStart` hops). |
| 4 | "That's Rule five: after some time period S, move all the jobs in the system to the topmost queue." | R5 writes in the rulebook: **After a period S, move all jobs to the top queue.** The letter S is highlighted in `VIRT`. Term highlight "priority boost". |
| 5 | "It solves two problems at once." | Two check ticks appear next to R5 one at a time, labeled below. |
| 6 | "A job in the top queue shares the CPU round robin, so it can't starve." | Tick 1 "no starvation": A hops on the CPU in Q2 alongside B, with a quick RR alternation. |
| 7 | "And a CPU-bound job that turned interactive gets treated properly once it's boosted." | Tick 2 "behavior changes": A sprouts a keyboard icon and *stays* high now (its bursts are short). |
| 8 | "Here's the long job A, competing with two short interactive jobs, B and C." | Everything resets to the Figure 8.4 setup: A in Q0 from t = 0 (Timeline pre-filled to 100 ms with A at Q2/Q1/Q0); B and C appear at t = 100 ms in Q2 (mint, gold), each with a tiny keyboard icon. The Timeline is split in two halves vertically (left half panel "without boost", right half panel "with boost"), each 10 ticks wide with its own set of rows. |
| 9 | "On the left, no boost: once B and C arrive, A is starved." | The left half runs: Q2 row fills with alternating mint and gold slivers from 100 ms on; A's row (Q0) has no blocks after 100 ms, and a red "starved" tag blinks over it. |
| 10 | "On the right, we boost every hundred milliseconds." | The right half runs: a stopwatch "S = 100 ms" ticks; at 100 ms an up-arrow lifts A; its row shows coral blocks in Q2 at the boost times. Boost markers (thin vertical bars) at 100 ms, 200 ms. |
| 11 | "That's too small for a real system, but fine for a picture." | Caption "S = 100 ms (too small, but good for a picture)" in `DIM`. |
| 12 | "Now A runs periodically." | A's coral blocks pulse (`Indicate`) in the right half. Hold 1 s. |

**Characters:** Professor (explaining), Student (curious, near the end).
**Ends with:** both halves of Figure 8.4 on screen (with the right half highlighted); R5 in the rulebook (R1–R5, with R4a, R4b).
**Implementation notes:** adapt Figure 8.4 (about 200 ms). To save space, show both halves as two `Timeline` instances, each x-range 4 wide (left (−6.2..−2.2), right (−1.8..2.2)), and hide the ladder when the panels are drawn (the ladder fades to 20%). Matches the book's pattern in broad strokes; don't try to replicate every sliver.

### S12 — The voodoo constant   (beats: B12) · ~0:35
**Purpose:** the question "what should S be?" and Ousterhout's Law.
**Starts with:** S11 end state; the panels fade to 30%.
**Layout:** a dial (radius 1.0) at center-left (−1.5, 1.2) labeled `S`; an Aside card slides in from the right.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "So what should S be?" | Student (curious). The dial draws in with a needle and "S" below. |
| 2 | "Hard question." | The needle wiggles randomly; "?" sparks fly off it. |
| 3 | "John Ousterhout called values like this **voodoo constants**, because they seem to need black magic to set." | Term highlight "voodoo constants". A small hand-drawn-style wand/hat glyph (just stars and a swirl) appears above the dial. |
| 4 | "Too high, and long jobs starve." | The needle swings right; on a mini ladder beside the dial, a coral A looks sad (zZ), a "starved" tag. |
| 5 | "Too low, and interactive jobs lose their share." | The needle swings left; mint and gold jobs get shoved aside by constant coral boosts. |
| 6 | "Hence **Ousterhout's Law**: avoid voodoo constants if you can." | Professor (explaining). Aside card slides in: "TIP: AVOID VOO-DOO CONSTANTS (OUSTERHOUT'S LAW)". Term highlight "Ousterhout's Law" (small, inside the card). |
| 7 | "Often you can't, so you get a config file of defaults an administrator tweaks, or, these days, machine-learned values." | A scrolling config file glyph with the line `S = 1000 # default`; a small gear and a small neural-net glyph (three circles with lines) sweep in. Hold 1 s. |

**Characters:** Student (curious), Professor (explaining).
**Ends with:** the dial with the needle in a "reasonable" middle position, the Aside card; Rule R5 visible in the faded rulebook.
**Implementation notes:** dial = `Circle` + `Line` needle with an updater; the neural-net glyph is three small `Dot`s in two columns with lines.

### S13 — Attempt #3: better accounting   (beats: B13) · ~0:55
**Purpose:** fix gaming by merging Rules 4a/4b into a single Rule 4 that tracks the total allotment used at a level. **Figure 8.5**.
**Starts with:** S12 end state; the dial and card fade; ladder + Timeline return (3-lane, 300 ms span: `ticks=30`).
**Layout:** ladder at the top; the Timeline split in two halves again (left = old rules, right = new rule). The rulebook shows R4a, R4b in `DIM` red ("broken").

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Now gaming." | The Rule 4a and 4b lines in the rulebook flash red. |
| 2 | "The culprits are Rules four A and four B: the scheduler *forgets* how much CPU a job already used whenever it does I/O." | The allotment gauge on the running gamer (B, mint, wearing the sunglasses glyph from S10): it drains 90%, B does I/O (clock), and the gauge snaps back to full with a "poof" (the forgetting). |
| 3 | "The fix is better **accounting**." | Term highlight "accounting". A small ledger/notepad icon appears at the gauge. |
| 4 | "At each level, the scheduler keeps track of the allotment used, even across I/Os." | Now the gauge stays drained when B does I/O; tick marks are added on the ledger for each burst (small stacked chunks filling the gauge: 3 ms + 3 ms + 4 ms = 10 ms). |
| 5 | "Once it's spent, the job is demoted." | The gauge empties; B slides down one lane. |
| 6 | "One long burst or many small ones: it doesn't matter." | Two bars drawn side by side: one 10-ms block; ten 1-ms blocks; both labeled "= 10 ms used". `=` as MathTex. |
| 7 | "So we merge four A and four B into one rule: once a job uses up its allotment at a given level, regardless of how many times it has given up the CPU, its priority is reduced." | The R4a and R4b lines slide together and `Transform` into the new **R4: Allotment used up at a level? Move down, however many times it gave up the CPU.** (green flash). |
| 8 | "On the left, the gamer B issues an I/O before every allotment ends, stays on top, and dominates the CPU." | Figure 8.5 left: Timeline half "old rules": A (coral) holds the bottom row for the first 100 ms; B (mint) arrives and shows a dense comb of slivers in Q2, hogging, while A's Q0 row is mostly empty, between 100 and ~250 ms. Caption "old rules". |
| 9 | "On the right, with the new rule, it slowly sinks." | Right half: B's slivers drop to Q1 and then Q0 after its allotment is spent, alternating with A's blocks in Q0. Caption "Rule 4". |
| 10 | "No unfair share." | Student (excited). A tick mark appears on the right half, a red X on the left. Hold 1 s. |

**Characters:** Student (excited).
**Ends with:** the rulebook with R1, R2, R3, R4 (merged) and R5; Figure 8.5's two halves on screen.
**Implementation notes:** the key visual is the gauge staying drained instead of resetting; show it close-up (scale 1.6) in steps 2–6 before the figure. The book's Figure 8.5 spans 300 ms. Keep the sliver pattern approximate.

### S14 — Turning the knobs   (beats: B14) · ~0:55
**Purpose:** parameters of MLFQ (queues, slices, allotment, boost); common design: shorter slices at the top, longer at the bottom. **Figure 8.6**.
**Starts with:** S13 end state; the halves fade, the ladder returns to 3 lanes and the Timeline to the bottom with 30 ticks.
**Layout:** a "control panel" (four sliders) at the upper right replaces the rulebook (the rulebook slides off to the right). Then the lanes' widths are adjusted.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Plenty of questions remain. How many queues?" | Term highlight "parameterize" (smaller). The control panel slides in with 4 sliders; slider 1 "number of queues" moves, and the ladder grows/shrinks lanes (3 → 5 → 3). |
| 2 | "How long a time slice at each level?" | Slider 2 "time slice / queue" moves; the CPU shows a ring that changes its arc length. |
| 3 | "How big an allotment?" | Slider 3: the gauge's width changes. |
| 4 | "How often to boost?" | Slider 4: the stopwatch ticks faster/slower. |
| 5 | "There are no easy answers, only experience with real workloads." | Student (confused): all four sliders jitter with "?" sparks. Professor (explaining). |
| 6 | "One common idea: high-priority queues get *short* slices, ten milliseconds or less, because interactive jobs alternate quickly." | The three lane labels gain slice tags: Q2 "10 ms". The jobs hop at a tight rhythm on the CPU. |
| 7 | "Low-priority queues hold CPU-bound jobs, so they get *long* slices, hundreds of milliseconds." | Q0 label gets "40 ms" (a few hundred in real systems); a wider lane tile. Q1 "20 ms". |
| 8 | "In this example, the top queue has a ten-millisecond slice, the middle one twenty, the bottom one forty." | The Timeline for 300 ms is drawn with the cell widths visualized: thin blocks in Q2 (10 ms), medium in Q1 (20 ms), wide in Q0 (40 ms) (**Figure 8.6**). |
| 9 | "Two jobs run through the top, then the middle, then settle into long, uninterrupted runs at the bottom." | A (coral) and B (mint) both enter Q2 and alternate in 10-ms slices (20 ms total in Q2), move to Q1 alternating in 20-ms slices (40 ms total), then to Q0 where they alternate in 40-ms slices. Hold 1.5 s. |

**Characters:** Student (confused), Professor (explaining).
**Ends with:** Figure 8.6 on the Timeline (two jobs, slice widths 10/20/40), the sliders panel faded.
**Implementation notes:** the Timeline needs *variable block width*: a block is a rectangle in the level's row spanning N ticks; use `span` (the Timeline's `make_block` has a `span` parameter). Ticks are 10 ms.

### S15 — MLFQ in the wild   (beats: B15) · ~0:50
**Purpose:** real systems: Solaris TS table, FreeBSD decay-usage, reserved OS levels, `nice`/advice.
**Starts with:** S14 end state; the Timeline and ladder fade to 15%.
**Layout:** three info cards at the left (x −5.4..−1.6, y = 1.8, 0.2, −1.4): Solaris, FreeBSD, "reserved + nice". An Aside/Tip card at right later.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Real systems tune these knobs differently." | The three cards' frames draw. |
| 2 | "The Solaris Time-Sharing class is an editable table." | Card 1 "Solaris TS" `Write`s with a mini table of 3 rows (queue / slice / ...). |
| 3 | "By default: sixty queues, slices growing from twenty milliseconds at the top to a few hundred at the bottom, and a boost about once a second." | The table's header fills: "60 queues", "20 ms → hundreds of ms", "boost ≈ 1 s" (each as a chip); a mini ladder of many lanes (sixty drawn as thin lines) appears beside it. |
| 4 | "FreeBSD skips the table." | Card 2 "FreeBSD" appears; the table card gets a strike line. |
| 5 | "It computes priority from CPU used, and that usage *decays* over time, which plays the role of the boost." | A formula card `MathTex("priority = f(\\text{CPU used})")` and a decaying curve (exponential, falling) beside it labeled "usage decays". Term highlight "decay-usage" (small). |
| 6 | "Some schedulers reserve the top levels for the OS itself." | Card 3: a mini ladder whose top two lanes are tinted `KERNEL_COLOR` with "OS only". |
| 7 | "And many accept **advice**: the UNIX `nice` command raises or lowers a job's priority, a little." | A **Terminal** at the lower-right types `$ nice -n 10 ./job`; the job on the mini ladder slips down one lane. Term highlight "advice". |
| 8 | "The OS rarely knows what's best, so it takes *hints*." | Professor (explaining). A Tip card "TIP: USE ADVICE WHERE POSSIBLE" slides in (`DIM` frame). |
| 9 | "It isn't obliged to obey." | A small hand-with-palm-up glyph ("hint") and a "maybe" tag next to the nice terminal; the job wobbles (may or may not move). Hold 1 s. |

**Characters:** Professor (explaining).
**Ends with:** the three cards and the Tip card; everything else dimmed.
**Implementation notes:** card contents are simple Text + a few primitives. Use `MONO_FONT` for the terminal text. The book names no more detail; don't invent numbers beyond those in the narration.

### S16 — The big picture: five rules   (beats: B16) · ~0:45
**Purpose:** the complete MLFQ: all five rules, one working picture. Why it works.
**Starts with:** S15 end state; all cards fade. The ladder (3 lanes), CPU, Timeline (200 ms, 20 ticks), rulebook return at full opacity.
**Layout:** as in S06 but the rulebook with the final rules; font a bit bigger (22), with each rule at least 0.55 high.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Let's put it all together. Here are the five rules, as refined." | The rulebook returns to center-right at scale 1.3 with R1 R2 R3 R4 R5 (the final wording from the book). Hold briefly. |
| 2 | "One: higher priority runs." | R1 highlights; on the ladder a job at Q2 hops on the CPU while one at Q1 waits. |
| 3 | "Two: equal priority takes turns, round robin, using the time slice of that queue." | R2 highlights; two jobs in Q2 alternate. |
| 4 | "Three: new jobs start at the top." | R3 highlights; a new job drops into Q2. |
| 5 | "Four: a job that uses up its allotment at a level moves down, however many times it gave up the CPU." | R4 highlights; a job's gauge drains in several chunks and it sinks one lane. |
| 6 | "Five: every so often, everybody goes back to the top." | R5 highlights; the stopwatch fires; all jobs rise to Q2. |
| 7 | "That's why it's called a Multi-Level *Feedback* Queue." | Term highlight "feedback" over "multi-level" (`TEXT`): the *queue stack* (levels) highlights, then an arrow loops from the CPU's output back to a job's priority. |
| 8 | "It has *multiple levels* of queues, and it uses *feedback* to decide a job's priority. History is its guide." | The "levels" bracket + the "feedback" loop arrow stay; the history clock arrow from S03 appears. |
| 9 | "It doesn't demand to know a job in advance. It watches." | The Spotlight glances (left-right) as if watching the jobs. |
| 10 | "Short jobs get excellent response, close to SJF or STCF, and long jobs still make fair progress." | B and C (short) finish quickly at the top with check marks; A makes progress in short blocks in Q2 after the boost; the Timeline shows the pattern. |
| 11 | "BSD UNIX derivatives, Solaris, and Windows NT and its successors all use a form of MLFQ as their base scheduler." | Three name tags ("BSD UNIX", "Solaris", "Windows NT") pop around the CPU one by one (`GrowFromCenter`), 0.3 s apart. Hold 1.5 s. |

**Characters:** corner mode; Professor happy at the end (proud on step 11).
**Ends with:** full ladder + CPU + Timeline + rulebook R1–R5 + name tags; all jobs idle after the loop.
**Implementation notes:** a short loop on the ladder (A, B, C cycling) takes ~8 s total across steps 2–10. Pre-script it with a fixed job sequence; no randomness. The five rules are the book's final wording from Section 8.6 (Rule 2 says "using the time slice (quantum length) of the given queue").

### S17 — Recap   (beats: B17) · ~0:35
**Purpose:** five takeaways.
**Starts with:** S16 end state.
**Layout:** the world fades; numbered list at the left (−5.6 .. 1), font 28, one line each; an icon for each line at x = 4.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "So, today:" | The world `FadeOut` except the section badge; header "Recap" in `VIRT`. |
| 2 | "MLFQ uses several queues at different priority levels, and the CPU goes to the highest one." | Line 1 writes; icon: mini ladder with a spotlight on the top lane. |
| 3 | "It doesn't know job lengths, so it **learns from history**: new jobs start at the top and sink as they use their allotment." | Line 2; icon: history clock + a job sinking one lane. |
| 4 | "Jobs that give up the CPU quickly keep a high priority, so interactive jobs stay snappy, and the scheduler approximates SJF." | Line 3; icon: mint job at the top + keyboard glyph. |
| 5 | "A **priority boost** stops starvation, and **better accounting** stops gaming." | Line 4; icon: boost up-arrow + a padlock. |
| 6 | "Every knob, the number of queues, the slice lengths, S, takes tuning, and none has an obvious best value." | Line 5; icon: dial/sliders. Hold 1.5 s. |

**Ends with:** the full recap list. Section badge fades out.
**Implementation notes:** keep every line ≤ 10 on-screen words (shorter than the narration). The narration lines are paraphrased on screen: "Several queues, highest first", "Learn from history", "Quick to give up the CPU = stays high", "Boost + accounting = fair and safe", "Knobs need tuning".

### S18 — Teaser: a hat of tickets   (beats: B18) · ~0:25
**Purpose:** hook for 09 (Lottery Scheduling).
**Starts with:** S17 end state.
**Layout:** dialogue mode. A jar or hat at center (0, 1.2); tickets float above it.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "MLFQ is clever. But it has so many knobs, and the rules keep patching each other. Isn't there a simpler way to share the CPU fairly?" | The recap fades. Student and Professor move to dialogue mode. Student (curious). A faint tangle of knobs/dials (from S14) flickers at the center and fades. |
| 2 | "There is. Forget turnaround and response for a moment. What if we just promised each job a *share* of the CPU, and picked the next one by drawing a ticket from a raffle drum?" | Professor (happy). The `RaffleDrum` (from episode 09) appears at center; a pie chart ("shares") forms above it with segments coral 75% and mint 25%, the split 09 opens with. Colored `Ticket`s (three coral, one mint) float into the drum. |
| 3 | "The scheduler gambles?" | Student (surprised). A hand pulls a ticket out of the hat; it flips to show a coral "A" (hint, not a complete draw). |
| 4 | "Next time." | Professor (proud). Cut to black (FadeOut all, 0.5 s). Then "Next: 09 · Lottery Scheduling" in `TEXT` with a `VIRT` dot. Hold 2 s. |

**Characters:** Student (curious → surprised), Professor (happy → proud).
**Ends with:** black end card.
**Implementation notes:** the hat is a `Polygon`/`Ellipse` composite; tickets are small rounded rectangles with a notch. Mention only visually, no probability talk yet.

## New assets needed
Props (none of these exist in `ostep_lib` yet):
- **`RuleBoard(rules, accent)`** (new, p08): a panel of rule lines with tag chips ("R1", "R2", …). Methods: `.add(tag, text)` (animation: `Write`), `.glow(tag)` (animation: highlight/indicate), `.merge(tags_in, tag_out, text)` (animation: 4a and 4b slide together and `Transform` into the single Rule 4), `.strike(tag)`/`.warn()` (red outline/cracks), `.set_dim(tags)`. Used in nearly every scene after S02.
- **`AllotmentGauge(width, value)`** (new, p08): a small horizontal bar with fill driven by a `ValueTracker`; `.drain(amount, run_time)`, `.reset()`, `.attach_to(process)` (sits above a process's head and follows it). Also supports a "ledger" mode (stacked chunks) for S13.
- **`MLFQLadder(levels=8|3, labels, lane_width)`** (new, p08): a stack of lane `Queue`s with a label per lane, the "high / low priority" arrows, `.lane_point(level)`, `.promote(job, level)`, `.demote(job)`, `.boost_all()` (a `LaggedStart` of hops to the top lane), `.glow_lane(level)`, and `.collapse_to(levels)` for the 8 → 3 lane transition. Can be built from the existing `Queue` (lane = one Queue with a `slot_point(i)`).
- **Timeline extensions (small changes to `Timeline`)**: (a) tick labels in milliseconds (multiples of 50 labeled "0, 50, 100…" at ticks of 10 ms); (b) *sub-tick slivers* (blocks of width 0.1 tick or less, in a row, at a fractional tick), used in S09, S11, S13; (c) a vertical "marker with label" (already `boundary_marker`, probably enough) for boost times; (d) the `span` parameter exists in `make_block` and is enough for S14.
- **Small icons / glyphs** (primitives): dial with needle (`Dial`), slider panel (four sliders), wand/stars glyph for "voodoo", ledger/notepad (existing `Notepad` from p04 can be reused), raffle drum and tickets (teaser; reuse 09's `RaffleDrum` / `Ticket`, see `Ostep/Scenes/_shared-assets-05-11.md`), dark sunglasses/mask glyph for the gamer (S10, S13), mini pie (`Sector`), config-file glyph, `nice` terminal line (reuse `Terminal`), era tag "1962 · CTSS" (plain text tag), medal glyph. All are simple Manim primitives.
- **Expressions:** none needed. Only expressions from the bible are used.
- **Process helper:** none; reuse `hop_to`.

## Open questions
- **Length:** 18 scenes, ~14 min, top of the series' 8–15 min range. If you want it shorter: drop S12 (voodoo) or S15 (real systems), or merge them into S11/S14. Preferences?
- **Eight queues vs. three:** S03 uses the book's Figure 8.1 (Q8..Q1), and S05 collapses it into Q2/Q1/Q0 (all other figures). Is the animated collapse good, or should we start directly with three queues?
- **Rulebook on the right side:** it takes 3.3 units of width for the whole episode, which makes the ladder narrower. OK, or should the rules appear one at a time centered, then dock?
- **The gamer is B (mint):** B is the good interactive job in S08–S09 and the gamer in S13 (the book also reuses "B"). Should the gamer be a new color so viewers don't think B is bad?
- **Level-time chart:** the book's figures are only black/gray. We color blocks by job; OK to deviate?
- **"Allotment gauge":** my metaphor for allotment. Keep it as the recurring icon for the word (and add it to the bible's props table)?
