# 07 — Scheduling: Introduction · Scene breakdown
> Script: Ostep/Scripts/07-cpu-sched.md · Scenes: 19 · Est. duration: ~13:45

## Visual overview
- **Core visual: the Gantt world.** Every policy is drawn on the same **Timeline**: one row per job
  (A, B, C) using the series state encoding (running = solid, ready = outline), plus a combined
  **CPU lane** below where each block carries the color of the job that ran. Waiting is therefore
  *visible* as a hollow outline getting longer. Turnaround and response time are measured as
  **brackets** along the rows, and a **metric readout** under the chart sums them into an average.
  Because the same chart is reused for FIFO, SJF, STCF and RR, viewers compare policies by watching
  the same jobs *reshuffle* (`Transform` of blocks), not by reading numbers.
- **Second metaphor: the supermarket line.** It opens the episode (S01) as a Queue of shoppers and comes
  back for the convoy (S06) and for SJF's "ten items or less" lane (S07).
- **Third motif: five padlocks.** The five workload assumptions are padlocks in a small strip at the top.
  Each one *opens* when the episode relaxes that assumption (1 in S06, 2 in S08, 3 in S09, 4 in S15).
  The fifth stays locked in S16, which is the cliffhanger.
- **Policy = Spotlight.** Reused from 04: whenever a scheduler decision is made, the Spotlight picks a job.
- Props used (from the bible): Crux card, Tip / Aside card, Term highlight, Section badge, Timeline,
  Queue, Spotlight, GearPair, CPU, Disk, Terminal, ClockIcon,
  Process creatures, `ep_tag`. Characters: Professor, Student, Computer (only briefly), Process.

### Persistent assignments
| Thing | Look | Notes |
|---|---|---|
| Job **A** | `Process(label="A", color=PROCESS_COLORS[0])` (coral) | Same as ep. 04. Always the "long" job in the long-job examples; in the 5 s examples it is the first job. |
| Job **B** | `PROCESS_COLORS[1]` (mint) | |
| Job **C** | `PROCESS_COLORS[2]` (gold) | |
| Timeline home ("Gantt world") | x from −5 to 5; rows A, B, C at y = 1.2, 0.7, 0.2 (row height 0.45); **CPU lane** at y = −0.5; tick labels at y = −1.05 with "Time" at the right end; policy title at (0, 3.1) | Cell size depends on the example: 10 s per cell (12 cells) for the 120 s examples, 1 s per cell (15 cells) for the 15 s examples, 10 ms per cell (14 cells) for I/O. |
| Metric readout | `MathTex` at (0, −2.0), font 38, `TEXT`; the final average in a framed box and color: red (`KERNEL_COLOR`) if bad, `PERS` green if good | e.g. `\frac{10+20+30}{3}=20`. Built from the book's exact expressions. |
| Completion marker | A small downward `Triangle` plus the number, on the tick axis, in the job's color | New value counted into the readout when it lands. |
| Turnaround bracket | Horizontal bracket spanning arrival → completion above the job's row, `TEXT` stroke, label "T" | Appears in S04 and S06–S09. |
| Response bracket | Horizontal bracket arrival → first run in the `INTRO` color (warm off-white), dashed | Appears in S10–S11; clearly different from the turnaround bracket. |
| Section badge | Top-left at (−6.6, 3.6): `VIRT` dot + "07 · Scheduling", font 22, `DIM` | Appears in S02, stays on until S18. |
| Term highlight | As in 04: written at (0, 2.9), font 54, `VIRT` underline, shrinks to top-right (6.6, 3.6) | For every bolded term. |
| Padlock strip | Five padlocks (the `padlock` icon, 0.28 high) in a row at (−6.6..−4.6, 3.1), numbered 1–5 beneath | Visible S03–S16. |
| Characters (corner mode) | Student at (−5.8, −2.8), scale 0.75, facing right; Professor at (5.8, −2.8), scale 0.75, `flip()` | Same as 04. "Dialogue mode" for S01 and S19 as in 04. |
| Policy title | Written at (0, 3.1), font 36, accent `VIRT`: "FIFO", "SJF", "STCF", "RR" | The previous title `Transform`s into the next. |

## Scenes

### S01 — The family with three carts   (beats: B01) · ~0:40
**Purpose:** feel the problem: a short job stuck behind a long one. Everyone already has an instinct about what should happen.
**Starts with:** empty (BG).
**Layout:** a checkout counter (rounded rectangle plus a small register) at right (3.2, −0.4). A **Queue** labeled "Checkout" to its left, slots at x = 0.8, −0.9, −2.6, along y = −0.4. Student at dialogue position (−4.2, −1.2).

| # | Narration (exact words the action lands on) | On screen / animation |
|---|---|---|
| 1 | "You're at the supermarket. You've got one carton of milk." | The counter `FadeIn`. A mint `Process` creature "you" (label "you", color `PROCESS_COLORS[1]`) walks in from the left holding a small milk-carton glyph. |
| 2 | "You pick the shortest line, and just as you get there…" | The Queue label writes. "you" hops into the last slot (x = −2.6). |
| 3 | "…the family in front of you starts unloading. Three carts. Piled high." | A coral `Process` (label "family") is at the front slot. Three cart glyphs (outline, stacked boxes) roll in one by one (`GrowFromCenter`, 0.4 s apart) beside it, overflowing with colored boxes. |
| 4 | "Plus a checkbook." | A small checkbook glyph pops over the family; the register's light blinks. |
| 5 | "I'm going to be here all day." | Student enters from the left (frustrated). A small stopwatch above the milk shopper spins; its hand goes round three times. |
| 6 | "Everyone has felt this. And everyone has an instinct about what the store *should* do: let the milk go first." | Professor enters from the right (thinking). A dotted arrow loops the milk shopper to the front slot and the family to the back; it reads as a wish, then fades. |
| 7 | "The book's advice, by the way, is to take a long, deep breath. In. Out. It will be okay." | The Student inhales: a soft pulse of the Student's scale (1.0 → 1.05 → 1.0) twice, a small "In… Out…" `DIM` text above. |
| 8 | "Now: that line is a **scheduler**, and the store just made a policy decision. Let's see how good it was." | The Queue gets a small `Spotlight` (cone) hovering over the front slot, with the tag "who goes next?" in `DIM`. Pause 1 s. |

**Characters:** Student (frustrated), Professor (thinking). Both in dialogue mode.
**Ends with:** the checkout scene: counter, Queue with the family (coral) at front and "you" (mint) at the back, spotlight cone over the front slot, both characters.
**Implementation notes:** shoppers are plain `Process` creatures with the label changed; the carts are rectangles with a wheel `Circle` on each end. "Scheduler" is the first bold term, so use the Term highlight lightly (no section badge yet) or just a bold word in the narration. `Spotlight` and `Queue` are from the existing props.

### S02 — The Crux   (beats: B02) · ~0:30
**Purpose:** pose the question and link it to 04/06: mechanism is done, now it's the policy.
**Starts with:** S01 end state.
**Layout:** Crux card centered (0, 0.4), 9 × 3.2, `VIRT` frame. Characters move to corner mode.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | (transition) | The checkout scene dims to nothing (`FadeOut`) except the `Spotlight`, which floats up to the center. The Section badge "07 · Scheduling" forms at top-left. Characters glide to corner mode. |
| 2 | "Which brings us to the crux: How to develop scheduling policy?" (then the card's follow-up questions, read aloud) | Crux card: header "THE CRUX", question in bold (font 32): **"How to develop scheduling policy?"** `Write`. |
| 3 | "Remember mechanisms versus policies? Last episode we met the mechanism: the context switch." | A `GearPair` (mechanism) rolls in at left (−4, −1.5), turning; a tag "Ep. 06" attaches. |
| 4 | "It tells the OS *how* to stop one process and start another." | The gears' arm lifts a tiny process and swaps it. |
| 5 | "Today is about the *which*." | The gears slide aside and dim; the `Spotlight` swings and rests over a small Queue of A, B, C at the right (2.5, −1.5). |
| 6 | (subtitle writes) | The card subtitle writes in, `DIM`, font 22: "Key assumptions? What metrics are important? What basic approaches have been tried?" |
| 7 | "And the answer, as we'll see, is surprisingly full of trade-offs." | The card shrinks to a one-line strip at (0, 3.2) ("How to develop scheduling policy?", font 24). Pause 0.8 s. |

**Characters:** corner mode; Student neutral, Professor neutral → explaining at step 3.
**Ends with:** badge, crux strip, gears (dim, left) and the spotlight over a tiny Queue A, B, C (right), characters in corners. The gears and queue fade as S03 starts.
**Implementation notes:** `CruxCard.dock()` for the strip. The gears and spotlight are the same icons used in 04's S08, so reuse them as is.

### S03 — Five convenient lies   (beats: B03) · ~0:50
**Purpose:** set the workload assumptions as five locks that the episode will unlock one by one.
**Starts with:** S02 end state, but the gears, queue and crux strip fade.
**Layout:** five assumption "cards" in a column at the left-center, x = −1.2, y = 1.8, 0.9, 0.0, −0.9, −1.8 (each 6.4 × 0.7, `DIM` frame, text font 28). A padlock sits at the left end of each card.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "To think clearly, let's first simplify. The processes running in the system are the **workload**…" | Term highlight "workload". A small cluster of Process creatures A, B, C appears at the right (4.2, 0.4) with the label "workload". |
| 2 | "…and we'll call each one a **job**." | Term highlight "job" (smaller). The creatures turn into horizontal bars of different lengths labeled A, B, C (job = a chunk of CPU work). |
| 3 | "We'll assume five things about the workload." | The five cards' frames draw top to bottom (empty). |
| 4 | "One: every job runs for the same amount of time." | Card 1 writes "1 · Every job runs the same time". Its padlock closes (`GrowFromCenter`, with a tiny click). Three equal bars at the right pulse. |
| 5 | "Two: all jobs arrive at the same moment." | Card 2 "2 · All jobs arrive together"; the bars line up at a vertical line. |
| 6 | "Three: once started, a job runs to completion." | Card 3 "3 · Run to completion". |
| 7 | "Four: jobs only use the CPU. They never do I/O." | Card 4 "4 · CPU only, no I/O"; a tiny Disk icon appears and gets a red ✕. |
| 8 | "Five: the run-time of each job is known in advance." | Card 5 "5 · Run-time is known". A small crystal-ball glyph (grey) appears. |
| 9 | "Known in advance? How would the OS ever know that?" | Student (confused). Padlock 5 wobbles. |
| 10 | "It wouldn't. That's the least realistic one, and it makes our scheduler all-knowing." | Professor (explaining). Card 5 gets a faint red tint; the crystal ball glows. |
| 11 | "But these assumptions are scaffolding. We'll take them down, one at a time…" | The five cards stack-shrink: each card compresses into its padlock, and the five padlocks slide to the top-left strip (under the badge) with their numbers 1–5. |
| 12 | "…until we have a fully-operational scheduling discipline. Like a Death Star, but for CPUs." | Professor (happy). A tiny `DIM` tag "scheduling discipline" next to the strip. Pause 0.8 s. |

**Characters:** Student (confused), Professor (explaining → happy).
**Ends with:** padlock strip at (−6.6, 3.1) with 5 closed padlocks; badge; empty center; characters in corners.
**Implementation notes:** use the `padlock` icon from the overview props; for "open" use a second state (shackle rotated up), or add a `.open()` animation (see New assets). The term highlights for "workload" and "job" can be quick (hold 0.8 s).

### S04 — How good is a schedule?   (beats: B04) · ~0:50
**Purpose:** introduce a metric (a number to compare schedules), turnaround time, and its formula. Mention fairness as the opposing metric.
**Starts with:** S03 end state.
**Layout:** an empty Gantt world: Timeline with rows A, B, C, a CPU lane, 12 cells (10 s per cell), at the standard position. The formula at (0, −2.0) later.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "To compare policies, we need a **scheduling metric**: a number that *measures* how well a schedule does." | Term highlight "scheduling metric". A ruler glyph slides across a small block sample. |
| 2 | "For now, we'll use exactly one. **Turnaround time**." | Term highlight "turnaround time". The empty Timeline draws. |
| 3 | "It's the time at which a job completes, minus the time at which it arrived." | A job A arrives: a small arrow on row A at t = 0 labeled "arrives". A sample block runs on row A to t = 6 cells; the arrow at its end is labeled "completes". A bracket spans the whole length labeled "turnaround". A stopwatch glyph at the left of the bracket starts at 0 and stops at the end. |
| 4 | (formula writes) | `MathTex` writes at (0, −2.0): `T_{turnaround} = T_{completion} - T_{arrival}`. The two terms are colored: completion in `PERS`, arrival in `INTRO`. |
| 5 | "Since we've assumed every job arrives at time zero, turnaround is just completion time." | The `T_arrival` term fades to `0` (`Transform`), and the formula reduces to `T_{turnaround} = T_{completion}`. Padlock 2 pulses (assumption 2 is being used). |
| 6 | "That fact will change when we relax the assumptions." | The reduced formula flickers back to the full one for a beat, then fades. The sample block and bracket fade. |
| 7 | "Turnaround is a *performance* metric. The other big family is **fairness**." | Professor (explaining). The Timeline fades to 15%. Two small cards: "performance" (a gauge) at left (−2, 0.4), "fairness" (a balance scale) at right (2, 0.4). Term highlight "fairness". |
| 8 | "And the two tend to fight: a scheduler can maximize performance by starving a few jobs, which isn't fair at all." | The gauge and the scale are connected by a see-saw line: when the gauge goes up, the scale tips. A Process creature (gold) near the tipped end looks blocked (clock), with "starved?" in `DIM`. |

**Characters:** Professor (explaining), Student (neutral → curious at step 8).
**Ends with:** the empty Timeline back at full brightness; the two cards fade. Formula faded. Policy title slot empty.
**Implementation notes:** `Timeline` here is empty, so create it with `rows=["A","B","C"]`, `ticks=12`; the CPU lane is `cpu_row=True`. Keep this scene's sample bar as a plain `Rectangle` so the Timeline stays untouched. Fairness is mentioned by name only. No Jain formula.

### S05 — First In, First Out   (beats: B05) · ~0:45
**Purpose:** FIFO on the book's Figure 7.1: A, B, C of 10 s each. Average turnaround = 20.
**Starts with:** S04 end state (empty Timeline, 12 cells of 10 s).
**Layout:** standard Gantt world. A Queue of A, B, C along the top-right is not needed; the jobs' order is shown on the rows.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "The simplest policy imaginable: **First In, First Out**, FIFO, also called First Come, First Served." | Policy title writes at (0, 3.1): "FIFO". Term highlight "FIFO", and a smaller tag "= FCFS". |
| 2 | "Whoever arrives first runs first." | A, B, C appear as a Queue at the top-right (4.0, 2.4) in order A, B, C. A small arrow marks the front. |
| 3 | "It's simple, so it's easy to build, and with our assumptions it works pretty well." | A small `PERS` tick next to "simple". |
| 4 | "Three jobs, A, B and C. They all arrive together, but A arrived a hair before B, and B a hair before C." | The three jobs' arrival arrows stack at t = 0 on rows A, B, C, with tiny offsets. |
| 5 | "Each needs ten seconds." | A bracket "10 s" at the top across one cell. |
| 6 | "A finishes at ten." | A is scheduled: Spotlight on A. Row A: cells 1 fill solid coral, the CPU lane too. Rows B, C: cell 1 shows the ready outline (mint, gold). A completion marker "10" drops at tick 1. A's turnaround bracket (0 → 10) draws. The readout writes `\frac{10}{3}...` partially: `\frac{10+}{3}`. |
| 7 | "B at twenty." | Same for B (cell 2): solid mint; C ready outline; marker "20". Readout `\frac{10+20+}{3}`. |
| 8 | "C at thirty." | Cell 3 solid gold; marker "30". Readout complete: `\frac{10+20+30}{3}=20`. |
| 9 | "Average turnaround time: ten plus twenty plus thirty, over three. Twenty seconds." | The three brackets pulse in turn; the "20" in the readout frames in green. |

**Characters:** Student and Professor neutral, small nods (Student → curious at step 9).
**Ends with:** the finished Figure 7.1 chart, three brackets, readout "20" in `PERS`, title "FIFO". Padlock strip unchanged.
**Implementation notes:** `Timeline.fill(row, tick, "running")` for the running block and `"ready"` for the waiting cells; `fill_cpu` colored by job (see New assets). Source: **Figure 7.1**. Keep the readout built with `MathTex` pieces so it can be written left to right (`\frac{10+20+30}{3}` as separate substrings).

### S06 — The convoy   (beats: B06) · ~0:50
**Purpose:** break assumption 1 (equal run-times): FIFO's convoy effect. Figure 7.2: A = 100 s, B = C = 10 s. Average = 110.
**Starts with:** S05 end state.
**Layout:** standard Gantt world, but 120 s = 12 cells, so A is 10 cells long.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Okay, but I bet there's a catch. What if the jobs aren't all the same length?" | Student (curious). Padlock 1 shakes. |
| 2 | "That's the first assumption going away." | Padlock 1 **opens** (shackle lifts, `ValueTracker` to green). The chart clears (blocks `FadeOut` right to left). The three jobs' work bars appear at the top: A (long, 10 cells coral), B and C (1 cell each, mint, gold). |
| 3 | "Same three jobs, but now A needs a hundred seconds, and B and C need ten each." | Labels "100 s", "10 s", "10 s" write on the bars. |
| 4 | "A is first in line, so A runs for a full hundred seconds." | Row A fills cell by cell, accelerating (cells 1–10, 0.25 s each); B, C show outlines getting longer, the ready outline expanding to the right in step. The CPU lane fills coral. |
| 5 | "Then B finishes at a hundred and ten. C at a hundred and twenty." | B's cell 11, C's cell 12 fill solid. Markers "100", "110", "120" drop. The turnaround brackets draw, A short of the others. |
| 6 | "The average: a hundred and ten seconds. Ouch." | Readout `\frac{100+110+120}{3}=110` writes; the `110` in red (`KERNEL_COLOR`), shaking slightly. Student (surprised). |
| 7 | "This is the **convoy effect**: short consumers of a resource get stuck behind a heavyweight one." | Term highlight "convoy effect". B and C's outlines (the long waits) glow red while A's block pulses. |
| 8 | "It's your supermarket line again." | The chart scales down to the right (0.5) and the S01 checkout Queue slides in at the left: the family (A, coral) at the front, milk shopper "you" and a gold shopper behind. The same three-length picture lines up. The queue then slides out. |
| 9 | "Just let B and C go first!" | Student (excited). |
| 10 | "Hold that thought." | Professor (happy). Pause 0.8 s. |

**Characters:** Student (curious → surprised → excited), Professor (happy).
**Ends with:** the FIFO / A = 100 chart with brackets and the readout "110" in red; padlock 1 open.
**Implementation notes:** **Figure 7.2.** Step 4 uses a decreasing `run_time` loop. Keep the red wait outlines on rows B and C visible because they carry the lesson. Step 8's crossfade can be a scaled `Transform` of the chart into three plain shoppers, then back.

### S07 — Shortest Job First   (beats: B07) · ~0:50
**Purpose:** reorder shortest-first and watch the average halve (Figure 7.3). Link to the "ten items or less" lane.
**Starts with:** S06 end state.
**Layout:** standard Gantt world. The Tip card later slides in from the right over x 1.6..6.6, y −1.8..2.0.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "That's exactly the next policy. **Shortest Job First**, SJF." | Policy title `Transform`s "FIFO" → "SJF". Term highlight "SJF". Student's "go first" wish arrow reappears as the intro. |
| 2 | "Run the shortest job first, then the next shortest, and so on." | The Spotlight appears above the three job bars and sweeps to B (shortest), then C, then A, labeling "1st, 2nd, 3rd". |
| 3 | "Same three jobs. B finishes at ten. C at twenty. A at a hundred and twenty." | The blocks on the CPU lane and rows **Transform** from the FIFO order into the SJF order: B (cell 1), C (cell 2), A (cells 3–12), rows adjusting (B solid at 1, C outline then solid, A outline for 2 cells then solid). Markers "10", "20", "120". |
| 4 | "Average turnaround: fifty seconds." | The readout `\frac{10+20+120}{3}=50` writes; the old "110" is struck out above it and the new 50 frames in green. The number counts down from 110 to 50. |
| 5 | "Same jobs, same work, and we cut the average by more than half just by changing the order." | A brace "× 2.2 better" appears between "110" and "50". |
| 6 | "And if all jobs arrive together, SJF is provably optimal." | Professor (explaining). A crown / "optimal" tag pops on the title "SJF", with a small `DIM` note "assuming all arrive together". |
| 7 | "We're in a systems class, so we'll skip the proof." | A tiny proof sheet glyph appears and is crossed out; Student (bored) shrugs. |
| 8 | "But the supermarket got there first: that's the 'ten items or less' lane." | A Tip card slides in from the right: header "TIP", title "The principle of SJF", a sign "10 ITEMS OR LESS" with a small lane showing a mint shopper (1 item) going ahead of a coral one. |
| 9 | (pause 1 s) | Tip card slides out. |

**Characters:** Professor (explaining), Student (bored at step 7).
**Ends with:** the SJF chart (B, C, A), readout "50" in green, title "SJF", padlock 1 open.
**Implementation notes:** **Figure 7.3.** The Transform from FIFO to SJF is the key image, so animate each block moving to its new cell (not cross-fade), with the ready outlines re-growing.

### S08 — Late arrivals   (beats: B08) · ~0:50
**Purpose:** break assumption 2 (simultaneous arrival). SJF is non-preemptive, so the convoy comes back (Figure 7.4). Average = 103.33.
**Starts with:** S07 end state.
**Layout:** standard Gantt world with 12 cells. Arrival arrows on the time axis.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Right. The second assumption goes next." | Student (curious). Padlock 2 **opens**. The chart clears; the title stays "SJF". |
| 2 | "Now A arrives at time zero and needs a hundred seconds." | An arrival arrow on row A at t = 0, the work bar "100 s". |
| 3 | "B and C arrive at time ten, and each needs ten." | Arrival arrows on rows B and C at t = 10 (tick 1), labeled "[B, C arrive]", work bars "10 s" each (small). |
| 4 | "SJF starts A, the only job it has." | A runs: row A solid from cell 1, CPU lane coral. |
| 5 | "When B and C show up, A is already running, and SJF never interrupts." | At tick 1, B and C appear as outlines; a small Spotlight tries to move to B and bounces off a "no interrupt" padlock-like bar on A (A's block glows). |
| 6 | "So they wait until A finishes at a hundred." | Rows B and C outline stretches right while A runs; A reaches cell 10. |
| 7 | "B finishes at a hundred and ten, and C at a hundred and twenty." | Cells 11 and 12 fill for B and C; markers "110", "120"; A's marker "100". |
| 8 | "But their *turnaround* counts from their arrival at ten." | The turnaround brackets of B and C start at tick 1, not 0: lengths 100 and 110 (labeled "110 − 10" and "120 − 10"). The arrival offset is highlighted. |
| 9 | "So that's a hundred, a hundred, and a hundred and ten." | The labels change to "100", "100", "110". |
| 10 | "Average: a hundred and three point three three seconds. The convoy is back." | Readout `\frac{100+(110-10)+(120-10)}{3}=103.33` writes; the value in red. |
| 11 | "The problem is that SJF is **non-preemptive**: it runs each job to completion before it even considers another." | Professor (worried). Term highlight "non-preemptive". |

**Characters:** Student (curious), Professor (worried).
**Ends with:** the late-arrival SJF chart (Figure 7.4) with readout "103.33" in red; padlocks 1–2 open.
**Implementation notes:** **Figure 7.4.** Arrival markers need a new `arrival_marker(row, tick, label)` (see New assets), or use `Timeline.boundary_marker`. Write the readout with the book's exact numerator `100+(110-10)+(120-10)`.

### S09 — Stopping a job mid-way   (beats: B09) · ~0:55
**Purpose:** relax assumption 3 → preemption, using the timer interrupt and context switch from 06; STCF fixes the late-arrival schedule (Figure 7.5). Average = 50.
**Starts with:** S08 end state.
**Layout:** an Aside card on the right during steps 1–3; then the Gantt world.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "To fix this, we relax the third assumption: jobs don't have to run to completion." | Padlock 3 **opens**. The chart dims to 30%. |
| 2 | "The scheduler can stop A, run something else, and come back later. That's **preemption**." | An Aside card slides in ("ASIDE: Preemptive schedulers"). Inside: a CPU with A on it; A is lifted off (the robotic arm / gears from 04), set aside as a half-filled bar, and B placed on. Term highlight "preemption". |
| 3 | "Old batch systems were non-preemptive. Virtually every modern scheduler is **preemptive**, and it uses exactly the machinery we built last time: the timer interrupt and the context switch." | The card shows two labels "non-preemptive (old batch)" and "preemptive (modern)", the second glowing. A small timer-clock icon and the gears (tags "Ep. 06") attach to the preemptive side. Term highlight "preemptive". Card slides out; the chart un-dims and clears. |
| 4 | "Add preemption to SJF and you get **Shortest Time-to-Completion First**, STCF (also called PSJF)." | Title `Transform`s "SJF" → "STCF". Term highlight "STCF", with `DIM` alias "= PSJF". |
| 5 | "Whenever a new job arrives, run whichever job has the *least time left*." | A "time left" bar appears under each job (width = remaining). The Spotlight is set to follow the shortest bar. |
| 6 | "B and C arrive at ten. A has ninety seconds left." | A has run cell 1 (coral). At tick 1, arrival arrows for B, C drop in. A's remaining bar shrinks to 9 cells; B and C bars are 1 cell each. |
| 7 | "So A is preempted. B runs, then C, then A finishes." | The Spotlight swings from A to B. A's block stops (a pause glyph on it); B runs cell 2, C cell 3 (solid), then A resumes cells 4–12. The rows show ready outlines accordingly. |
| 8 | "Completions: one-twenty, twenty, thirty." | Markers "120", "20", "30" drop. |
| 9 | "Turnarounds: one-twenty, ten, and twenty." | The brackets: A 0 → 120, B 10 → 20, C 10 → 30, with labels "120", "10", "20". |
| 10 | "Average: fifty seconds. And given our assumptions, STCF is provably optimal." | Readout `\frac{(120-0)+(20-10)+(30-10)}{3}=50` writes; the 50 in green; the optimal tag pops on the title. Student (excited). |

**Characters:** Professor (explaining), Student (curious → excited).
**Ends with:** the STCF chart (Figure 7.5), readout 50 in green, title "STCF", padlocks 1–3 open.
**Implementation notes:** **Figure 7.5.** Source of the preemption aside: the book's "Aside: Preemptive Schedulers". Reuse `GearPair` for the context-switch mechanism, `ClockIcon` for the timer. A paused A block is shown with `PauseGlyph`.

### S10 — A new metric: response time   (beats: B10) · ~0:50
**Purpose:** introduce response time; show that SJF is bad for it (Figure 7.6, 5 s jobs).
**Starts with:** S09 end state.
**Layout:** a Terminal at left (−3.4, 1.0), 4.4 × 2; later the Gantt world (15 cells of 1 s).

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "If all we cared about were batch jobs, we'd be done." | The STCF chart shrinks and docks at the right as a thumbnail (scale 0.4). |
| 2 | "But then came time-shared machines, and people sitting at terminals, typing." | The Terminal slides in at left; the Student sits (looks) at it; a cursor blinks. |
| 3 | "Now they care about something else: how long until the computer *responds*." | The Student types a key ("a"); a stopwatch above the terminal starts; no echo yet. |
| 4 | "That's **response time**: the time from when a job arrives to the first time it runs." | Term highlight "response time". The echo "a" finally prints and the stopwatch stops at "10 s". Student (frustrated). |
| 5 | (formula writes) | `MathTex`: `T_{response} = T_{firstrun} - T_{arrival}` at (0, −2.0), with `T_firstrun` in `INTRO` color. The turnaround formula ghost sits beside it, `DIM`, for contrast. |
| 6 | "Look at SJF with three jobs of five seconds each." | Terminal and thumbnail fade. Title "SJF". A fresh Gantt world, 15 cells of 1 s: ticks 0, 5, 10, 15 labeled. Arrival arrows for A, B, C at t = 0. |
| 7 | "A runs first and responds at zero." | A runs 5 cells (solid coral); response bracket on A of length 0 (a tiny tick), labeled "0". |
| 8 | "B waits five. C waits ten." | B's response bracket grows 0 → 5 (dashed `INTRO`), then C's 0 → 10. B and C run (5–10, 10–15). Labels "5", "10". |
| 9 | "Average response time: five seconds." | Readout `\frac{0+5+10}{3}=5` writes; "5" in red. |
| 10 | "Imagine typing a character and waiting ten seconds because other jobs got in front." | The terminal thumbnail with the stopwatch at "10 s" pops again over C's bracket. |
| 11 | "That's a terrible terminal." | Student (sad). |
| 12 | "SJF, STCF, and their relatives are great for turnaround and bad for response. So we need a new policy." | Professor (explaining). A mini scoreboard in the top-right: "SJF / STCF: turnaround ✓ (use `tick_mark()`), response ✗ (`x_mark()`)". |

**Characters:** Student (curious → frustrated → sad), Professor (explaining).
**Ends with:** the 5 s SJF chart (Figure 7.6) with response brackets, readout "5" in red, scoreboard row for SJF/STCF.
**Implementation notes:** **Figure 7.6.** The `Terminal` prop is used for the typing. Each response bracket is the dashed one in `INTRO`, per the persistent table. Use `tick_mark()` / `x_mark()` for ✓ ✗, not Unicode.

### S11 — Round Robin   (beats: B11, first half) · ~0:45
**Purpose:** RR: short time slices, round the queue, response times 0, 1, 2 (Figure 7.7).
**Starts with:** S10 end state.
**Layout:** Gantt world (15 cells, 1 s). A Queue "Run queue" along the top right (3.2, 2.4) with A, B, C and a time-slice clock (`ClockIcon`) at (0.8, 2.4).

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Here's the idea. Instead of running jobs to completion, run one for a short **time slice**…" | The SJF blocks pull apart into one-second slices (each 5-cell block splits into 5 single-cell blocks, `Transform`) and the 5-cell blocks dim to 20%. Title "SJF" → "RR". Term highlight "time slice". The clock icon lights up with the label "1 s". A `DIM` alias "= scheduling quantum". |
| 2 | "…(the book also calls it a **scheduling quantum**)…" | (included above, quick fade-in of the alias). |
| 3 | "…then switch to the next job in the queue, and the next, round and round until every job is done. This is **Round Robin**." | The run queue forms: A, B, C. The Spotlight sweeps A → B → C → A in a circle. A circular arrow wraps the queue. Term highlight "Round Robin". |
| 4 | "Same three five-second jobs, with a one-second slice. A, B, C, A, B, C." | The chart refills with 15 thin slices in order ABCABCABC…; rows show each job running and waiting, the CPU lane striping coral, mint, gold. The slice speed accelerates after the 6th slice. |
| 5 | "A runs first, B second, C third, all within three seconds." | The first three slices flash; response brackets: A 0, B 1, C 2 (dashed `INTRO`). |
| 6 | "Response times: zero, one, and two. Average: one second. Down from five." | Readout `\frac{0+1+2}{3}=1` writes with the "1" in green; the old "5" is struck out above it. The scoreboard row for RR: response ✓. |

**Characters:** Student (curious), Professor (happy).
**Ends with:** the RR chart (Figure 7.7) with 15 slices, response brackets 0, 1, 2, readout "1" in green; Run queue and clock at top.
**Implementation notes:** **Figure 7.7.** The slice-splitting `Transform` should map each SJF block into five thin slices. Keep slice widths constant. RR's queue is the 04 `Queue` prop, with a rotating head via `.pop()` / `.push()`.

### S12 — How short is too short?   (beats: B11, second half) · ~0:40
**Purpose:** the time slice has a cost: must be a multiple of the timer-interrupt period; amortization (book tip).
**Starts with:** S11 end state.
**Layout:** the chart dims to 20% and shifts up; the Tip card slides in at center (0, −0.5), 8 × 3.4.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "So make the slice really, really short?" | Student (curious). The slice clock label ticks 1 s → 0.1 s → 0.01 s. |
| 2 | "Careful. Every switch costs time." | Professor (worried). Between slices on the chart, tiny red slivers (switches) appear and thicken as slices shrink. |
| 3 | "The time slice has to be a multiple of the timer-interrupt period. If the timer fires every ten milliseconds, the slice is ten, twenty, any multiple of ten." | A timer-clock icon pulses at the left of a number line of ticks every 10 ms; slice blocks of 10, 20, 30 ms snap to it (the invalid 15 ms bounces away with a red ✕). |
| 4 | "And if a switch costs one millisecond and the slice is ten, then ten percent of the time is wasted." | Tip card "TIP: Amortization can reduce costs": a bar of one 10 ms slice (mint) with a red 1 ms sliver at its end. A big "10 %" label in red. |
| 5 | "Make the slice a hundred, and the waste falls under one percent." | The bar stretches to 100 ms; the sliver stays at 1 ms and looks tiny. The label becomes "< 1 %" in green. |
| 6 | "That's **amortization**: if an operation has a fixed cost, do it less often." | Term highlight "amortization". The two bars flip between each other to emphasize "fewer switches". |
| 7 | "The cost of a switch is also more than saving registers. The caches and other hardware state have to be warmed up all over again." | The save-slot icon (04) flashes. Then a CPU with a few small "cache" rectangles that flush (go dark), then refill slowly (a 4-step fade-in), labeled "warm-up". |

**Characters:** Student (curious), Professor (worried).
**Ends with:** the Tip card with the 100 ms bar; then the card slides out and the chart returns to full brightness.
**Implementation notes:** the tip numbers are from the book: 10 ms slice with 1 ms switch ≈ 10 %; 100 ms slice < 1 %. Do not draw to scale beyond the visual ratio 1:10 and 1:100.

### S13 — You can't have your cake and eat it   (beats: B12) · ~0:50
**Purpose:** RR's turnaround is awful (13, 14, 15; average 14); the trade-off between fair and unfair policies.
**Starts with:** S12 end state (RR chart, full brightness).
**Layout:** the RR chart on the left half (scale 0.7), a scoreboard on the right half.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "So Round Robin is great at response time. Now check its turnaround, with the same three jobs." | The response brackets fade, replaced by turnaround brackets (solid `TEXT`). |
| 2 | "A finishes at thirteen. B at fourteen. C at fifteen." | Completion markers "13", "14", "15" drop at the right end of the chart. |
| 3 | "Average: fourteen seconds." | Readout `\frac{13+14+15}{3}=14` writes; "14" in red. |
| 4 | "SJF would have given ten (five, ten and fifteen)." | A ghost of the SJF chart with markers 5, 10, 15 and `\frac{5+10+15}{3}=10` appears faintly above; "10" in green. |
| 5 | "RR is one of the *worst* policies for turnaround, even worse than FIFO in many cases." | The RR "14" shakes; a skull / thumbs-down glyph (use `x_mark()`). |
| 6 | "It stretches every job out as long as it can." | The solid brackets of A, B, C, now all long and almost equal, glow. The slices on the chart pull taut like a rubber band along the row. |
| 7 | "So which one is right?" | Student (confused). |
| 8 | "Neither. That's a **trade-off**." | Professor (happy). Term highlight "trade-off". The scoreboard writes on the right: two columns "turnaround" / "response", rows "SJF · STCF" and "RR": ✓ ✗ / ✗ ✓ (marks via `tick_mark()`/`x_mark()`). A see-saw between SJF and RR tips either way. |
| 9 | "A policy that divides the CPU evenly (a *fair* one) does badly on turnaround." | The RR row highlights; a balance scale shows "fair" at the heavy end. |
| 10 | "A policy that runs short jobs to completion does well on turnaround, but makes others wait." | The SJF row highlights; blocked outlines of the waiting jobs pulse. |
| 11 | "You can't have your cake and eat it too." | A cake glyph (peach callback: swap it with the peach icon if the user prefers) is eaten, and a pie-chart bite disappears. Professor (proud). Pause 1 s. |

**Characters:** Student (confused), Professor (happy → proud).
**Ends with:** the scoreboard (SJF/STCF vs RR) at right; chart thumbnail at left. Title "RR".
**Implementation notes:** the SJF ghost uses the 5 s numbers from Figure 7.6 (5, 10, 15 → 10). The "cake" glyph is a circle with a wedge. It's a quick gag, so no new asset is needed (primitive shapes). The scoreboard persists to S17.

### S14 — When a job waits on the disk   (beats: B13, first half) · ~0:40
**Purpose:** relax assumption 4 (no I/O): the naive schedule wastes the CPU (Figure 7.8).
**Starts with:** S13 end state, with the chart and scoreboard fading.
**Layout:** a two-lane Timeline: lanes "CPU" (y = 0.8) and "Disk" (y = 0.2), 14 cells of 10 ms, standard width. A Disk icon at (−5.2, 0.2) next to its lane.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Now the fourth assumption. Real jobs do I/O." | Padlock 4 **opens**. The chart clears; the lanes "CPU" and "Disk" draw; unit "ms" under the ticks. |
| 2 | "When a job asks the disk for data, it's **blocked**, so the scheduler has to run someone else." | Term highlight "blocked" (callback tag "state, Ep. 04"). A coral A process hops off the CPU lane, a clock shows on it (blocked). |
| 3 | "And when the I/O completes, there's another decision." | A "?" appears over the Spotlight; it hovers. |
| 4 | "Two jobs, A and B, each need fifty milliseconds of CPU." | Two work bars: A (5 cells) and B (5 cells), "50 ms" each. |
| 5 | "But A computes for ten, then does a ten-millisecond I/O, over and over." | A's bar is divided into five 10 ms bursts (coral) separated by 10 ms I/O gaps (drawn as disk-lane blocks, coral outline). |
| 6 | "B just computes for fifty." | B's bar is one solid mint 5-cell block. |
| 7 | "Using STCF, what should the scheduler do?" | Student (curious); the Spotlight bobs between the two. |
| 8 | "Naively, the scheduler runs a burst of A, then sits idle while A waits on the disk, again and again, and only then runs B." |  Banner "naive": the lanes fill: CPU: A, idle, A, idle, A, idle, A, idle, A (cells at 0, 20, 40, 60, 80); Disk: A's I/O in the gaps; then B from 90 to 140. The idle gaps are hatched grey. The Computer pops at (5.2, −2.9) scale 0.6 → sleeping each time. |
| 9 | "Poor use of resources." | A label "Poor use of resources" in red; readout "CPU idle: 40 ms" appears. |

**Characters:** Student (curious), Computer (sleeping).
**Ends with:** Figure 7.8 fully drawn (A bursts, idle gaps, B at the end), Computer asleep. Padlocks 1–4 open.
**Implementation notes:** **Figure 7.8.** In this chart each cell is 10 ms and the time axis runs to 140. Idle blocks use the state encoding "idle". The Disk lane blocks use `fill(row, tick, "running", color=coral)` in a lane that stands for "the disk is busy with A's I/O" (see New assets for the lane mode).

### S15 — Overlap   (beats: B13, second half) · ~0:40
**Purpose:** treat each CPU burst as a job, so STCF overlaps I/O with computation (Figure 7.9).
**Starts with:** S14 end state.
**Layout:** the same two lanes; the naive version is rewound.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "The trick: treat each ten-millisecond burst of A as its own little *job*." | The naive blocks are rewound (reverse animation, 0.8 s). A's five bursts split off as five small coral jobs in a Queue, with B (mint, 50 ms) beside them. The Computer wakes (idle). |
| 2 | "When the system starts, the shortest job is A's first burst. It runs." | The Spotlight picks A's first burst; the CPU lane fills coral cell 1. |
| 3 | "Then A goes to the disk and B takes over." | A's I/O appears on the Disk lane (cell 2, coral outline); the CPU lane fills mint cell 2. |
| 4 | "When A's I/O completes, a new short job appears. It preempts B, runs ten milliseconds, then B returns." | A's next burst drops in (an arrival arrow); the Spotlight moves to it; B's block is stopped (pause glyph) at the end of its 10 ms; A runs cell 3 (CPU lane coral); disk lane: A's second I/O at cell 4... B resumes at cell 4. |
| 5 | "Back and forth." | The sequence repeats faster: A B A B A B A B A B across 10 cells; the disk lane alternates coral blocks under B. |
| 6 | "This is **overlap**: while A waits on the disk, B uses the CPU." | Term highlight "overlap". Vertical bands link each coral disk block with the mint CPU block above it. |
| 7 | "Everyone finishes sooner than if we ran A, waited, ran A, waited, and only *then* ran B." | The first (naive) chart's end (140) is compared to this chart's end (100): a ghost marker at 140 and a bright marker at 100; "−40 ms" in green. |
| 8 | "So interactive jobs run often, and the CPU hogs fill the gaps!" | Student (excited). Mint B and coral A labeled "interactive" and "CPU hog" for a moment (small `DIM` tags). |
| 9 | (tip) | Tip card "TIP: Overlap enables higher utilization" slides in from the right, quickly (1.5 s), with the one-liner "start the operation, then switch to other work" and slides out. |

**Characters:** Computer (idle → busy), Student (excited), Professor (happy).
**Ends with:** Figure 7.9 fully drawn: both lanes with no CPU gaps; markers 140 (ghost) and 100; padlocks 1–4 open.
**Implementation notes:** **Figure 7.9.** Both lanes must match the book's pattern: CPU: A B A B A B A B A B; Disk: A-io under B's turns (between A's bursts). STCF's decision can be drawn as the Spotlight moving. Use `Timeline.unfill_ticks` for the rewind.

### S16 — No more oracle   (beats: B14) · ~0:40
**Purpose:** the last assumption is the shakiest: the OS doesn't know job lengths. Hook the next episode.
**Starts with:** S15 end state, with the chart shrinking to the right.
**Layout:** the padlock strip enlarges to the center: five padlocks in a row at y = 0.8, number 5 at the center-right. The STCF chart as a thumbnail at left (scale 0.4).

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "One padlock left: the OS knows how long each job will run." | The four open padlocks fade to 30%; padlock 5 enlarges and moves to the center (0, 0.8). |
| 2 | "We said this was the worst assumption, and it is." | A crystal ball glyph (the oracle) appears over it with "known run-time" below. |
| 3 | "Both SJF and STCF need to know job lengths before running them." | The SJF and STCF titles flash with a small "needs: run-time" tag; the work bars under each job read "?" instead of numbers. |
| 4 | "In a general-purpose OS, the system usually knows very little about how long a program will run." | The crystal ball cracks (a zigzag line draws), and the glow fades. A process creature (coral) walks onto a stage, with a question mark where its length bar should be. |
| 5 | "So the best schedulers we found can't actually be built?" | Student (confused). |
| 6 | "Not as they stand." | Professor (thinking). The padlock stays closed and the shackle shakes. |
| 7 | "How do we behave like SJF without that knowledge? And how do we keep response time good, like Round Robin?" | Two small cards below the padlock, "behave like SJF" with the SJF chart thumbnail and "keep response good" with the RR chart thumbnail, each with a "?" on the knowledge. |
| 8 | "Keep that question." | The cards fade; the padlock remains. Pause 1 s. |

**Characters:** Student (confused), Professor (thinking).
**Ends with:** the closed padlock 5 at center with a cracked crystal ball. Everything else fades.
**Implementation notes:** the crack is a jagged `VMobject` line over a circle. The crystal ball is simple: a circle with highlights and a stand. Reuse the 04 question-mark icon.

### S17 — Big picture   (beats: B15, first half) · ~0:40
**Purpose:** summarize all four policies in one scoreboard and one story.
**Starts with:** S16 end state.
**Layout:** a table, 4 rows × 3 columns, centered (0, 0.4), 9 × 3.4. Columns: "Policy", "Turnaround", "Response". Rows: FIFO, SJF, STCF, RR. Under each row a tiny chart thumbnail.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Let's step back. We started with a supermarket line and built four policies." | The padlock fades; the table frame draws. The tiny supermarket Queue sits at the top-left as the first "row" marker. |
| 2 | "FIFO is simple but suffers from the convoy effect." | Row "FIFO" writes with thumbnail (Fig. 7.2). Turnaround 110 (red). Response: ✗. A small convoy cartoon (long block, two small ones) next to it. |
| 3 | "SJF fixes that for jobs that arrive together." | Row "SJF" with the (Fig. 7.3) thumbnail. Turnaround 50 (green). |
| 4 | "STCF fixes it when they don't, using preemption." | Row "STCF" with the (Fig. 7.5) thumbnail. Turnaround 50 (green). A small pause glyph. |
| 5 | "And Round Robin gives up turnaround to win on response time." | Row "RR" with the (Fig. 7.7) thumbnail. Turnaround 14 (red) vs 10, response 1 (green). |
| 6 | "Two metrics, and no policy wins both." | The columns "turnaround" and "response" are circled; the green/red cells form a diagonal. Professor (explaining). Pause 1 s. |

**Characters:** Professor (explaining), Student (neutral).
**Ends with:** the summary table with four rows, thumbnails and colored values.
**Implementation notes:** thumbnails are shrunken `Timeline` groups (scale ~0.2) from earlier scenes or quick re-builds. Numbers: FIFO 110 (long-job example), SJF 50, STCF 50, RR 14 turnaround and 1 response. The table cells for response in the long-job examples are left as ✗ / ✓ marks, not numbers, since the examples differ.

### S18 — Recap   (beats: B15, second half) · ~0:35
**Purpose:** five takeaways.
**Starts with:** S17 end state.
**Layout:** the table fades; a numbered list at the left (−5.6 .. 1), font 28, one line each; an icon for each line at x = 4. Section badge stays until the end of the scene.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "So, today:" | The table `FadeOut`; header "Recap" in `VIRT`. |
| 2 | "A **policy** decides *which* process runs next, and we compare policies using **metrics**." | Line 1 writes; icon: Spotlight over a Queue. |
| 3 | "**Turnaround time** measures completion; **response time** measures how soon a job first runs." | Line 2; icon: two mini brackets (solid and dashed). |
| 4 | "FIFO, SJF and STCF are good for turnaround; SJF and STCF fix the convoy." | Line 3; icon: the convoy blocks reordering (long block moves behind). |
| 5 | "**Round Robin** is good for response time and bad for turnaround. That's a fundamental trade-off." | Line 4; icon: the see-saw. |
| 6 | "Overlapping I/O with computation raises utilization, but the OS can't see the future." | Line 5; icon: the two-lane chart plus the cracked crystal ball. Hold 1.5 s. |

**Characters:** corner mode; both happy-ish (Professor proud on the last line).
**Ends with:** the full recap list. Section badge fades out.

### S19 — Teaser   (beats: B16) · ~0:25
**Purpose:** hook for 08 (MLFQ): use the recent past to predict the future.
**Starts with:** S18 end state.
**Layout:** characters in dialogue mode (Student (−2.6, −1.2), Professor (2.6, −1.2), scale 1). A staircase of three queues at center (0, 1.6), tiny.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "So how does a real scheduler decide, if it can't see the future?" | The recap list fades. Student and Professor move to dialogue positions. Student (curious). |
| 2 | "By watching the recent past. If a job has been short so far, it's probably short again." | Professor (happy). A job's history (a few short bars) appears with a dashed arrow predicting the next bar, short. |
| 3 | "That idea has a name: the multi-level feedback queue." | The history becomes a staircase of three queues (levels) with a process hopping down and up. Student (excited). |
| 4 | (end) | Cut to black (FadeOut all, 0.5 s). Then "Next: 08 · The Multi-Level Feedback Queue" in `TEXT` with a `VIRT` dot. Hold 2 s. |

**Characters:** Student (curious → excited), Professor (happy).
**Ends with:** black end card.
**Implementation notes:** `ep_tag("→ Ep. 08")` can be used for the end card tag. The staircase is only a hint (3 horizontal bars at different heights).

## New assets needed
- **Timeline single-lane / colored-cell mode (extension of `Timeline`):** `fill_cpu(tick, color=<process color>)`, or a lane where cells take the color of the job that ran (04's `fill_cpu` is yellow "busy"). Also a second lane for the Disk (S14–S15) with the same API. A shortcut: `Timeline(rows=["CPU","Disk"])` plus `fill(row, tick, "running", color=...)`.
- **`arrival_marker(row, tick, label=None)`:** small down-arrow on a row at a tick, with an optional label such as "[B, C arrive]"; if `Timeline.boundary_marker` already does this, reuse it.
- **Completion marker + response/turnaround brackets:** `Timeline.bracket(row, t0, t1, label, style="solid"|"dashed", color)` returning a bracket mobject, and `completion_marker(tick, label, color)`. Needed in almost every scene.
- **`MetricReadout`:** a `MathTex` builder that writes the book's exact expressions (e.g. `\frac{10+20+30}{3}=20`) piece by piece and frames/colors the final value green or red; supports striking out an old value.
- **`Padlock` with open/close:** a `.open()` / `.close()` animation on the overview props' `padlock` icon, plus the numbered strip layout.
- **`CrystalBall`:** a circle on a stand with a glow; `.crack()` animation (jagged line). Used in S03 and S16 only.
- **Checkout props:** `Cart` (outline, wheels) and `Checkout` (counter plus register). Used in S01 and S06 only. Can be built inline from primitives instead of added to the library.
- **Doc/ruler glyphs** (S04 ruler, S07 proof sheet, S13 cake): primitives drawn inline in the scene file. No library asset.
- **No new character expressions.** Everything uses expressions from the bible.

## Open questions
- **Gantt style:** I draw each policy as rows A/B/C (solid = running, outline = ready) *plus* a combined CPU lane, which is richer than the book's single-lane figures. Is that OK, or should the book's single bar be primary and the rows be shown only for waits?
- **Process naming:** jobs A/B/C reuse 04's coral/mint/gold. The shopper in S01 is also coral (family) and mint (milk). Keep this foreshadowing?
- **Time units:** the book uses seconds (10, 100, 120) for the policy examples and milliseconds for I/O. The Timeline's ticks are labeled "s" or "ms" per example. Fine, or unify?
- **Length:** 19 scenes, ~13:45. Option to cut: merge S08 and S09 (late arrivals + STCF), or drop S12's cache warm-up. Which do you prefer?
- **"Death Star" and "cake" jokes:** the first is the book's footnote joke, the second the book's idiom. Keep both in the script, or tone one down?
- **Optimal tags:** SJF is "optimal" only when all jobs arrive together (book), and STCF given our assumptions. The chart tag shows a small caveat. Good enough, or add a narration line?
