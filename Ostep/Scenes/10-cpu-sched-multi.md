# 10 — Multiprocessor Scheduling (Advanced) · Scene breakdown
> Script: Ostep/Scripts/10-cpu-sched-multi.md · Scenes: 22 · Est. duration: ~16:00

## Visual overview
- **Core metaphor: the single-CPU world of 04/07 "gets a second, third, fourth CPU", and each CPU
  keeps a small private "desk" (its cache).** Everything in the episode is about what that desk
  changes. Part 1 (S04–S10) is hardware: one CPU with a cache, then two CPUs with caches on a
  shared Bus and Memory (adapting Figures 10.1 and 10.2). Part 2 (S11–S19) is scheduling: the
  same CPUs now take jobs from either **one shared Queue (SQMS)** or **one Queue each (MQMS)**,
  and a **ScheduleGrid** (the book's CPU 0..3 × time-slice tables) records who ran where.
- **Second metaphor: cache warmth.** A small "warmth" meter on every cache fills with the color of
  the job that has been running there. A job that hops to another CPU starts that CPU's meter at
  zero. Affinity is "meter stays full"; migration is "meter resets". It pays off in S12, S13, S14, S17 and S18.
- **Third: the padlock.** One padlock icon (the existing `padlock`) is the lock. It sits on the
  shared list (S08–S09) and on the shared queue (S11), and is absent in MQMS (S14). The viewer
  should feel "lock = queue of CPUs waiting".
- Props reused (from the bible): Crux card (twice), Aside/Tip card, Term highlight, Section badge,
  CPU (several), Memory, Bus, Queue, Timeline (only for hatched idle look), Code block, padlock,
  stopwatch, mechanism/policy gears (not used), Process creatures, Computer, Professor, Student.
- Characters: Professor and Student in corner mode by default.

### Persistent assignments
| Thing | Look | Notes |
|---|---|---|
| Job **A** | `Process(label="A", color=PROCESS_COLORS[0])` (coral) | Same as 04. Letters are used everywhere in the book figures. |
| Job **B** | `PROCESS_COLORS[1]` (mint) | |
| Job **C** | `PROCESS_COLORS[2]` (gold) | Gold sits close to `CPU_COLOR` yellow; always give C a `TEXT` outline when it is *on* a CPU chip so it stays readable. |
| Job **D** | `PROCESS_COLORS[3]` (sky) | |
| Job **E** | `PROCESS_COLORS[4]` | Only in SQMS and work-stealing scenes. |
| **CPU n** | `CPU(label="CPU n", size=1.2)` chip with a **cache strip** attached to its bottom edge (see New assets: `CacheCPU`) | Positions per scene. Four-CPU scenes use x = −4.5, −1.5, 1.5, 4.5 (spacing 3). Two-CPU scenes use x = −2, 2. |
| **Cache** | Small rounded strip 1.2 × 0.45, `MEM_COLOR` outline, fill 0.15, label "cache" font 16, 3 mini cells inside | Warmth meter = the fill of those cells in the *job color*; empty = `DIM` outline. |
| **Main memory** | `Memory` prop used as a small column (1.2 × 1.6, 4 cells), at bottom-center | Cells hold values as text. |
| **Bus** | `Bus` horizontal line at y = −0.4 with taps down from each cache and one tap down to Memory | Same line style as 04's Figure 4.1 bus. |
| **Padlock** | `padlock` icon, `KERNEL_COLOR` when locked, `DIM` when free, 0.45 units | |
| **ScheduleGrid** | New prop: rows "CPU 0..3" (or 0..1), cells 0.7 × 0.5, each cell filled in the job's color with its letter (`BG`-coloured text on bright fills); idle = hatched grey; "… (repeat) …" label to the right | Adapts the book's black/grey/white tables to the series colors. |
| Characters (corner mode) | Student bottom-left (−5.8, −2.8) scale 0.75 facing right; Professor bottom-right (5.8, −2.8) scale 0.75, flipped | Same as 04. Dialogue mode is Student (−2.6, −1.2), Professor (2.6, −1.2) at scale 1. |
| Section badge | Top-left (−6.6, 3.6): `VIRT` dot + "10 · Multi-CPU Scheduling", font 22, `DIM` | Appears in S03, stays until S21. |
| Term highlight | Same as 04: written at (0, 2.9) font 54 with `VIRT` underline, then docks top-right (6.6, 3.6) at font 26 | Every bold term's first appearance. |

## Scenes

### S01 — Eight cores, one slow program   (beats: B01, first half) · ~0:40
**Purpose:** feel the paradox: more CPUs do not make an ordinary program faster.
**Starts with:** empty (BG).
**Layout:** laptop outline (reuse `Laptop`) at center (0, 0.3), 5 wide, made translucent; inside, a row of eight small `CPU` chips (0.4 each) at y = 0.3, x from −2.1 to 2.1. Characters in dialogue mode, entering later.

| # | Narration (exact words the action lands on) | On screen / animation |
|---|---|---|
| 1 | "My new laptop has eight cores!" | Student slides in (excited). The `Laptop` outline draws; the eight chips `GrowFromCenter` inside, 0.1 s apart. Label "8 cores" pops above. |
| 2 | "So now every program I write runs eight times faster, right?" | A speech bubble from the Student: "8× faster?" (MathTex "8\times"). |
| 3 | "Let's test that. Take a normal C program…" | Professor enters (thinking). A small Code-like card "a.c" (a file icon with `main(){…}`) floats in under the laptop. |
| 4 | "Run it on this machine." | The file hops onto the laptop. Chip 1 lights `CPU_COLOR`; the other seven stay `DIM`. A single Process creature (coral, running) sits on chip 1. |
| 5 | "One core lights up. Seven sit idle." | A bracket under the seven dim chips with "idle ×7". The Computer pops up bottom-center (0, −2.6), scale 0.6, idle. |
| 6 | "A typical program only uses a single CPU. Adding CPUs does not make it run faster." | A stopwatch next to the laptop reads "1× speed" in `TEXT`; the Student's "8× faster?" bubble gets a red ✗ (`x_mark`) and the text crossfades to "1×". Student → sad. |

**Characters:** Student (excited → sad), Professor (thinking), Computer (idle).
**Ends with:** laptop with eight chips (one lit, with coral A on it), stopwatch "1×", Student (sad), Professor, Computer.
**Implementation notes:** keep the chips as simple `CPU` instances scaled to 0.4; the "idle ×7" bracket is a `Brace`.

### S02 — Parallel programs need threads   (beats: B01, second half) · ~0:55
**Purpose:** a program must be rewritten to run in parallel, with threads. And once it is, the OS must decide who goes where, assuming only one CPU was the old scheduler's world.
**Starts with:** S01 end state.
**Layout:** laptop moves to the upper center (0, 1.0) at scale 0.8. Below it, the thread-split area.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "To use eight cores, you'd have to rewrite it to run in **parallel**, perhaps using **threads**." | Term highlight "parallel". The coral process on chip 1 splits (mitosis squash) into eight small thread-processes (`make_thread`, coral), one hops to each chip; every chip lights `CPU_COLOR`. The stopwatch counts up "8×". Term highlight "threads". |
| 2 | "Remember the threads from the first episodes, the ones that fought over the shared counter?" | A small `MemoryStrip` thumbnail with a counter cell appears at the bottom (callback to 01–03): two thread-copies `+1` arrows hit it; the cell flickers 5 → 6 (lost update), then fades. |
| 3 | "Okay, so that's the programmer's problem. What does it have to do with the OS?" | Student (confused) with "?". |
| 4 | "Everything. Because the moment you *do* have eight busy threads, plus every other process…" | Professor (explaining). Around the laptop, other process creatures (mint, gold, sky) arrive at the edges and queue up toward the chips. |
| 5 | "…someone has to decide who runs on which core." | A spotlight (policy icon) sweeps across chips and processes, with "?" over each chip. |
| 6 | "And everything we learned about scheduling assumed exactly one CPU." | The spotlight narrows to chip 1 and stays; the other seven chips dim to 50%. Hold 1 s. |
| 7 | "Quick note. The book calls this an *advanced* chapter…" | An Aside card slides in from the right: "ASIDE · advanced chapter: leans on concurrency (later in the series)". |
| 8 | "So we'll sketch those parts, and promise to come back to them later." | Tag "→ Ep. 26–28" on the aside. The card slides out. |

**Characters:** Student (confused), Professor (explaining).
**Ends with:** laptop (translucent) with 8 chips, queue of processes outside; characters corner mode.
**Implementation notes:** the thread glyphs reuse `make_thread`. The counter thumbnail is a quick cameo, keep ≤ 3 s.

### S03 — The Crux   (beats: B02) · ~0:20
**Purpose:** pose the episode's question.
**Starts with:** S02 end state.
**Layout:** Crux card centered (0, 0.3), 9 × 3, `VIRT` frame.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | (transition) | Laptop and processes fade; chips shrink into the forming Section badge "10 · Multi-CPU Scheduling". |
| 2 | "Which brings us to the question behind this whole episode: {question}" (then the subtitle, then "So that's the question.") | Crux card `Write`s: **"How should the OS schedule jobs on multiple CPUs?"** Subtitle (DIM): "What new problems arise? Do the same old techniques work, or are new ideas required?" |
| 3 | "Spoiler: a bit of both." | Two small word tags beneath: "old techniques" ✓ and "new ideas" ✓. |
| 4 | "But to see why, we first have to look at what changed in the hardware." | Card shrinks to a one-line strip at the top (0, 3.2), kept through S18. |

**Characters:** corner mode; Student looks at the card.
**Ends with:** section badge, crux strip, characters.

### S04 — Caches: a fast shelf   (beats: B03) · ~0:45
**Purpose:** a cache makes slow memory look fast. Adapts **Figure 10.1**.
**Starts with:** S03 end state (crux strip, badge).
**Layout:** `CacheCPU` at (−1.5, 1.4) with its cache strip; `Memory` column at (−1.5, −1.7), 1.2 wide, 4 cells; a vertical line between cache and Memory (the memory path). Right side (3.5, 0.2) free for a stopwatch readout.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Here is the single CPU we've been using all along." | The CPU chip `GrowFromCenter` at (−1.5, 1.4) with an A process on it (running). |
| 2 | "And now, a detail we've been hiding: the **cache**." | The cache strip slides out from under the chip. Term highlight "hardware cache". |
| 3 | "Main memory holds *all* the data, but it's slow. Tens of nanoseconds, maybe hundreds." | Memory column `FadeIn` at the bottom, all four cells filled `MEM_COLOR`. A long trail line to it with a stopwatch icon "~100 ns" (`MONO_FONT`, font 26) on the right. |
| 4 | "So the CPU keeps a small, fast memory right next to it… It holds copies of popular data." | The cache strip pulses; a tiny label "small · fast". |
| 5 | "Think of the books on your desk versus the ones in the library across town." | A small desk icon (rectangle with three books) pops beside the cache strip, and a library (bigger building made of rectangles) beside the Memory column; each `FadeIn`/`FadeOut` within 2 s. |
| 6 | "The first time the program loads a value, the CPU has to go all the way to memory." | A request dot leaves the chip, passes the cache (miss: tiny "✗" flash) and travels down to Memory; the stopwatch ticks "~100 ns". |
| 7 | "It copies the value into the cache on the way back." | A copy of the value (a small square, "7") travels back up and lands in the cache's first mini cell. |
| 8 | "The next time, it finds the value in the cache, and gets it in just a few nanoseconds." | Second request dot: stops at the cache (green `tick_mark`); stopwatch "~few ns" flashes in `CPU_COLOR`. |
| 9 | "The large slow memory suddenly looks like a fast one." | Hold 1 s. Both stopwatch readouts stay for comparison: "memory ≈ 100 ns" / "cache ≈ a few ns" (use `MathTex(r"\approx")`, not ≈). |

**Characters:** none new; Student curious (look_at the cache).
**Ends with:** CPU + cache (one value cached) + Memory + two stopwatch readouts; crux strip and badge.
**Implementation notes:** the CPU hosts a "load" mini code line "x = *p;" optional.

### S05 — Locality   (beats: B04) · ~0:35
**Purpose:** the cache works because programs have temporal and spatial locality.
**Starts with:** S04 end state, but the stopwatch readouts shrink to the top-right.
**Layout:** two panels side by side: left "temporal" (x −3.3), right "spatial" (x 3.3), each with a row of Memory cells (horizontal strip, 8 cells, y = 0.4) via `MemoryStrip`. CPU and cache slide to the top-center (0, 2.0) at scale 0.6.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "But the cache is tiny. How does it know what to keep?" | Student (curious). A "?" over the cache. |
| 2 | "It guesses, and the guess works because of **locality**." | Term highlight "locality". The two panels draw. |
| 3 | "**Temporal locality**: data you just used is likely to be used again soon…" | Term highlight "temporal locality". Left strip: a small loop arrow circling over a code box `for(i…)`; one cell (the loop counter) lights, then lights again and again at 0.4 s intervals. A small copy of it sits in the cache. |
| 4 | "…like a loop counter, or the instructions of the loop itself." | A second lit cell labeled "loop code" joins. |
| 5 | "**Spatial locality**: if you touch address x, you will probably touch the neighbors soon…" | Term highlight "spatial locality". Right strip: cell 3 lights, then the cache grabs cells 3–4–5 as a block (a bracket around three cells slides up into the cache). |
| 6 | "…like a program walking through an array." | A cursor steps across cells 3, 4, 5, 6: cached ones show a green flash (hits); only cell 6 (outside the bracket) flashes red then is pulled in. |
| 7 | "Programs show both kinds all the time, so caches work well." | Both panels pulse in sync. |
| 8 | "Keep this in mind. It is the whole reason the rest of the episode matters." | A pin icon lands on the cache. Hold 1 s. |

**Characters:** Student (curious → neutral), Professor neutral.
**Ends with:** both locality panels dimmed; CPU + cache at top-center.
**Implementation notes:** reuse `MemoryStrip.pulse()` and `.color_cell()`. The "hits" can use `tick_mark()`.

### S06 — Two CPUs, two caches: stale data   (beats: B05) · ~1:20
**Purpose:** show cache incoherence concretely. Adapts **Figure 10.2**.
**Starts with:** S05 end state, panels fade.
**Layout:** `CacheCPU` 1 at (−2.8, 1.8), `CacheCPU` 2 at (2.8, 1.8); `Bus` horizontal at y = −0.2 from x −3.5 to 3.5 with the label "Bus" at its right end; Memory column at (0, −2.0) tapped from the bus. One memory cell labeled `addr 0x40` holds "7".

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Now the tricky part. Add a second CPU." | The single CPU slides left and a second `CacheCPU` `GrowFromCenter`s at right. |
| 2 | "Each CPU has its own cache, and both share one main memory, connected by a **bus**." | Memory column at the bottom; the Bus draws and taps connect each cache and the memory. Term highlight "bus" (small). Caches are empty (`DIM`). |
| 3 | "Memory holds a value at some address." | Memory cell `0x40` highlights; it reads "7". |
| 4 | "The program, on CPU one, reads it." | Process A (coral, running) is on CPU 1. A request dot goes down the bus to memory. |
| 5 | "It's not in CPU one's cache, so it's fetched from memory: the value is seven." | A "7" copy travels along the bus, up into cache 1's cell; cache 1 shows "0x40: 7" in coral. |
| 6 | "The program then changes it to nine." | A's value changes inside cache 1 ("7" → "9", `Transform`, a pencil-stroke glow). Memory still says 7: show a red dashed "stale!" outline on the memory cell. |
| 7 | "But writing all the way back to slow main memory takes a while, so the system, usually, just updates the cache and does the write to memory *later*." | A small "write-back later" tag with a clock icon on the memory path; a dotted arrow from cache 1 to memory, not yet traveled. |
| 8 | "Now the OS stops the program and moves it to CPU two." | Process A hops from CPU 1 to CPU 2 (`hop_to`, expression ready → running). Cache 1 stays with its "9". |
| 9 | "(The book's example calls the old value D and the new one D-prime.)" | A tiny `DIM` caption under memory: "book: D → D′". |
| 10 | "The program reads the same address again. CPU two's cache has nothing." | A's request dot goes to cache 2: a red ✗ miss. |
| 11 | "So it fetches from main memory, which still holds the *old* value. Seven. Not nine." | The dot goes down the bus; the "7" comes back and lands in cache 2; A stays `running` and gets a small floating "7?" bubble (Process has no "confused" expression). A red cross appears next to a ghost "9" in cache 1: a big "7 ≠ 9" in `KERNEL_COLOR` between the caches. |
| 12 | "The program just read stale data. The wrong answer, from the right address!" | Student (surprised); the Computer pops up bottom-center (0, −2.9) at scale 0.6 → error. |
| 13 | "This is the problem of **cache coherence**." | Professor (worried). Term highlight "cache coherence". |
| 14 | "Research on it fills libraries. We'll skip the nuance, and take a computer architecture course for that." | A short "→ computer architecture course" tag next to the term; a stack of three books appears and fades. |

**Characters:** Student (surprised), Professor (worried), Computer (error).
**Ends with:** two CacheCPUs (cache 1: "9", cache 2: "7"), Bus, Memory "7"; red "7 ≠ 9" mismatch; term strip shows "cache coherence".
**Implementation notes:** the key is a clean left-to-right causal story, no more than ~3 active elements at once (the value dot, the cache cell, the memory cell). `hop_to` for the process move. Values in `MONO_FONT`.

### S07 — Bus snooping   (beats: B06) · ~0:50
**Purpose:** hardware fixes coherence by every cache watching the bus; invalidate or update.
**Starts with:** S06 end state.
**Layout:** same as S06. Each cache gets a small eye icon (new tiny glyph, simple circle + dot) at its top-right.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "The fix is the hardware's job." | The mismatch fades; the stale "7" in cache 2 and memory dim. Rewind (reverse) the last step: A back to CPU 1; cache 1 "9" and cache 2 empty. |
| 2 | "Every cache watches the bus, the wire connecting everything to memory. This is **bus snooping**." | Term highlight "bus snooping". Eyes open on both caches (tiny pupils look at the Bus). |
| 3 | "When a cache sees an update for data it holds…" | Cache 2 is given a copy of 0x40 = 7 (it also holds it); cache 1 updates to "9" and the update travels along the Bus as a bright pulse. Cache 2's eye follows the pulse. |
| 4 | "…it reacts in one of two ways. It can **invalidate**: throw its own copy away, so the next read has to fetch the fresh value." | Term highlight "invalidate". Cache 2's "7" gets a red strike-through and fades. A small label "invalidate". |
| 5 | "Or it can **update**: put the new value into its own cache too." | Rewind to the pulse; this time cache 2's "7" `Transform`s to "9". Label "update". Term highlight "update". |
| 6 | "Either way, the one shared memory stays one shared memory." | Both caches and memory show consistent "9" (memory updates lazily: a faint arrow). A tick `tick_mark()` between the caches. |
| 7 | "Write-back caches, like our example, make this trickier, because the write to memory isn't visible until later. But you can imagine how the basic scheme works." | A small Aside card "write-back caches: trickier" slides in and out (1.5 s). |
| 8 | "So the hardware makes sure the program sees the right value, no matter which CPU it's on. Then we're done!" | Student (excited). The tick grows. |
| 9 | "Hold that thought." | Professor (happy); a small hand-up icon pauses the tick; the screen dims ~20% (a transition toward S08). |

**Characters:** Student (excited), Professor (happy).
**Ends with:** two caches consistent at "9", eyes visible, Bus, Memory; screen dimmed slightly.
**Implementation notes:** the bright "pulse" is a `MoveAlongPath` of a dot along the Bus, with `ShowPassingFlash`.

### S08 — Coherence isn't enough: the race   (beats: B07, first half) · ~0:55
**Purpose:** two CPUs executing the same list-pop at once can both remove the same node, even with coherent caches. Adapts **Figure 10.3**.
**Starts with:** S07 end state; Bus/Memory/caches fade to the bottom at 30%.
**Layout:** Code block of `List_Pop` (monokai, font 20, ~9 lines) at left (−3.8, 0.9). A linked list at the right: nodes `head → 5 → 3 → 8 → NULL` at y = 1.2, x from 0.5 to 5.5. Two CPU chips at the bottom (−1.5, −1.7) and (1.5, −1.7) with a thread-process each (coral and sky). Two `tmp` pointer chips float above.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Coherent caches guarantee that every CPU sees the *same* memory." | A tick over the caches, the Bus (a small "same view" label). |
| 2 | "They don't guarantee that two CPUs will modify it in a sensible *order*." | The tick is replaced by "?" over an "order" label. |
| 3 | "Here is a shared linked list, and the routine that removes the head from it." | The list nodes `Create`; the Code block fades in (`List_Pop`). |
| 4 | "Read the head into a temporary variable. Remember its value." | Highlight bar on line 7–8: a pointer chip `tmp` jumps from the thread on CPU 1 to the head node; the value "5" copies into a "value" box. |
| 5 | "Move the head forward. Free the old head. Return the value." | Highlight bars on lines 9, 10, 11 (the head arrow moves to node 3; node 5 puffs away; "5" exits). |
| 6 | "Now imagine threads on two CPUs both run the first line at the same time." | Rewind. Both threads get a bar on line 7 simultaneously; the list is the same. |
| 7 | "Each has its own private temporary, because that lives on its own stack." | Two `tmp` chips (coral, sky), each with a small "stack" tab, both point at the same head node. |
| 8 | "So both remove the same element, both free it, and the program frees memory twice." | Both threads run lines 9–10: node 5 puffs away, then the second `free` hits an empty spot: a big red "double free!" (`KERNEL_COLOR`) with error flash. The Computer pops up (error). |
| 9 | "Even with perfect cache coherence." | The tick from step 1 gets a crossed circle. Hold 1 s. |

**Characters:** Computer (error), Student (frustrated) reacting to the double free.
**Ends with:** Code block, broken list with "double free!" label, two threads on two CPUs.
**Implementation notes:** reuse the xv6-style highlight bar from 04's Code block. Keep line text from Figure 10.3 exactly.

### S09 — The lock fix   (beats: B07, second half) · ~0:30
**Purpose:** mutual exclusion; locks cost more as CPUs grow; lock-free exists but is rare.
**Starts with:** S08 end state.
**Layout:** same stage.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "The solution, as you may remember from the first episodes, is **mutual exclusion**: wrap the routine in a **lock**." | Rewind the race. The "double free" label fades. Term highlight "lock". A `padlock` icon (open) appears beside the Code block; two new lines `lock(&m);` and `unlock(&m);` are inserted at the top and bottom of `List_Pop`. |
| 2 | "Lock at the top, unlock at the end, and only one CPU at a time is inside." | Thread 1 enters: padlock closes (`KERNEL_COLOR`), the code block glows around the routine. Thread 2 waits outside with a small clock. After thread 1 exits (padlock opens), thread 2 enters; list shows 5 gone, then 3 gone. A tick. |
| 3 | "We won't get into the details here. They're the subject of the whole concurrency section." | Tag "→ Ep. 26–28" next to the padlock. |
| 4 | "But hold on to one fact: locks have a cost." | The padlock and a stopwatch pair up. |
| 5 | "As the number of CPUs grows, accessing a shared, locked data structure gets *slow*." | Four more CPU chips (with waiting threads) join in a line outside the door, each with a clock; the line grows to 8; a stopwatch next to the padlock counts "waiting…" . |
| 6 | "There are also **lock-free** structures that avoid locks, but they are complicated, and used only on occasion." | A small Aside card "lock-free structures: complex, rare" slides in then out. |

**Characters:** Student (frustrated → neutral), Professor (explaining).
**Ends with:** padlock with a growing line of waiting CPUs; Code block. Transition: all fades but the padlock, which shrinks to the top-right corner.

### S10 — Cache affinity   (beats: B08) · ~0:45
**Purpose:** running on the same CPU is faster because its cache is warm. Adapts the idea of the book's section 10.3.
**Starts with:** the padlock docked top-right.
**Layout:** two `CacheCPU`s at (−2.5, 1.2) and (2.5, 1.2). Each cache has a warmth meter (the 3 mini cells). Memory at the bottom (0, −2.0) with a Bus. Process A starts on CPU 1.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "When a process runs on a CPU, it gradually fills that CPU's caches…" | A (coral) running on CPU 1. Cache 1's three mini cells fill with coral one by one (0.6 s each). |
| 2 | "…and its TLBs, which we'll meet in the memory episodes…" | A tiny `DIM` tag "TLB → Ep. 19" attached to the cache. |
| 3 | "It builds up *state*. This is called **cache affinity**: the CPU is warm for that process." | Term highlight "cache affinity". The cache glows coral and a small warmth label "warm" with a flame/thermometer. |
| 4 | "The next time that process runs, it runs faster on the same CPU…" | A hops off (ready) and back on to CPU 1; a stopwatch beside shows "fast" with a short arc. |
| 5 | "Put it on a different CPU, and it must reload everything, slowly." | A hops to CPU 2. Cache 2 is empty. Request dots go down the Bus to Memory one by one; cache 2's cells fill coral slowly (2 s), the stopwatch shows "slow". |
| 6 | "It still runs correctly, thanks to coherence, just slower." | A small tick at the CPU 2 ("correct") plus a turtle-slow gauge (`SpeedGauge` low). |
| 7 | "So a multiprocessor scheduler should consider cache affinity. When possible, keep a process on the same CPU." | Professor (explaining). A glowing "pin" ties A to CPU 1 (a small pushpin icon on the chip). |

**Characters:** Professor (explaining), Student (curious).
**Ends with:** A with a pin on CPU 1, cache 1 warm; cache 2 cold; the term strip shows "cache affinity".
**Implementation notes:** the warmth meter is just mini cells with animated fill. Reuse `SpeedGauge`.

### S11 — Attempt 1: one shared queue   (beats: B09, first part) · ~0:45
**Purpose:** SQMS is the simplest approach, but its shared queue needs a lock, which doesn't scale.
**Starts with:** S10 end state, cleared.
**Layout:** four `CacheCPU`s along the top (x = −4.5, −1.5, 1.5, 4.5, y = 1.5), labeled "CPU 0..3". A single `Queue` along the bottom (y = −1.0) with jobs A–E, label "the queue", with the book's `NULL` end marker. A padlock on the queue's left end.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Fine. So what's the simplest scheduler? Take the one we already have and share it?" | Student (curious). The Queue with A–E appears (left-aligned) with four idle CPUs above. |
| 2 | "Put all jobs into a single queue. Each CPU, whenever it needs work, grabs the next job from it." | Term highlight "SQMS" (with subtitle "single-queue multiprocessor scheduling", small). CPU 0 pulls A (hop up), CPU 1 pulls B, CPU 2 pulls C, CPU 3 pulls D; E remains. Jobs `running`. |
| 3 | "It needs almost no new work. Take any single-CPU policy, and let it pick the best job to run…" | A spotlight (the policy icon from 04/07) hovers over the queue head: "any existing policy". |
| 4 | "But there are two problems. The first: **scalability**." | Term highlight "scalability". |
| 5 | "The queue is shared, so the scheduler must lock it." | The padlock closes on the queue (`KERNEL_COLOR`). Each CPU shows a thin line to the queue. |
| 6 | "And as we just saw, locks hurt more and more as CPUs grow." | Four CPUs finish their slice at the same moment and all reach for the queue: three of them stop at the padlock, each with a small clock, in a line. A bar "waiting for the lock" grows. |
| 7 | "More time is spent waiting for the lock, less time doing the work the system is supposed to do." | A split time-bar under the chips: yellow "work" shrinks as red "lock" grows (4 chips → 8 chips quickly doubling, via copies). |
| 8 | "(The book wishes it had a real measurement here…)" | A small `DIM` note "real measurement: left as an exercise" with a dotted chart outline. |

**Characters:** Student (curious), Professor (explaining).
**Ends with:** four CPUs holding A–D, queue holding E, padlock and queueing line, work/lock bar.
**Implementation notes:** keep exactly four CPUs (the book's). The 8-chip doubling is a brief flourish.

### S12 — SQMS and affinity   (beats: B09, second part) · ~0:40
**Purpose:** with a shared queue, jobs bounce between CPUs (the book's 4-CPU table).
**Starts with:** S11 end state; the lock bar fades.
**Layout:** the CPUs stay; below them the **ScheduleGrid** (rows CPU 0..3, 5 columns) at (0, −1.2), cell 0.8 × 0.5. Warmth meters on each cache above the chips.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "The second problem is cache affinity. Take five jobs, A through E, and four CPUs." | The queue is reset to A–E (five jobs). Caption "5 jobs · 4 CPUs". |
| 2 | "Each CPU simply takes the next job from the shared queue…" | Slice 1 fills in the grid: column 1 = A, B, C, D. (CPU 0 A, CPU 1 B, CPU 2 C, CPU 3 D.) E is waiting. |
| 3 | "…so over time the jobs bounce around." | Columns 2–5 fill one by one at 0.8 s each, matching the book's table: CPU 0 = A E D C B, CPU 1 = B A E D C, CPU 2 = C B A E D, CPU 3 = D C B A E. Each job's cells make a diagonal; the matching colored cells are connected by faint lines (job A's path highlighted). |
| 4 | "A on CPU zero, then CPU one, then CPU two. Each time it lands on a cold cache." | A's path highlights; the three CPUs' caches flash "cold" on each hop (meters stay near empty). |
| 5 | "This is exactly the opposite of what affinity wants." | A red ✗ on the grid; the caches show low warmth. Professor (worried). |

**Characters:** Professor (worried).
**Ends with:** the 4×5 ScheduleGrid (book table), A's path highlighted, cold meters.
**Implementation notes:** the book's table has job A in CPU0 slice 1, CPU1 slice 2, CPU2 slice 3, CPU3 slice 4 (a rotating schedule; E fits in at slice 2 on CPU 0). Use the page-6 figure as the source, with the series' colors in place of the book's greys.

### S13 — Patching SQMS with affinity   (beats: B10) · ~0:40
**Purpose:** most SQMS schedulers add an affinity mechanism: some jobs stay, one migrates. Complex.
**Starts with:** S12 end state.
**Layout:** same stage. The ScheduleGrid is rebuilt.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Real SQMS schedulers add an affinity mechanism." | The grid cells fade; a pin icon appears next to each CPU. |
| 2 | "Let some jobs stay put, and move others around to balance the load." | Jobs A–D pin to CPU 0–3 (pins click on). |
| 3 | "For our five jobs: A, B, C and D each stay on their own CPU." | The grid refills (page 7): CPU 0 = A in every slice but slice 2, CPU 1 = B, CPU 2 = C, CPU 3 = D, and E in the remaining cells; the four stay-put rows are mostly one color. Warmth meters stay full. |
| 4 | "Only job E *migrates*, from CPU to CPU, so the load stays fair." | E's cells highlight; arrows E: CPU 0 → CPU 1 → CPU 2 → CPU 3 as slices progress (a suitcase glyph on E). Term highlight "migration" (small, first mention only). |
| 5 | "A different job could take the migrating role the next time round, if you want fairness among the others too." | The suitcase hops from E to the next job in a later "repeat" lane (small). |
| 6 | "It works. But it's complex to build." | Professor (explaining). A gear-cluster icon (mechanism) with a "complex" tag. |
| 7 | "So SQMS is easy to write, and doesn't scale or preserve affinity well." | A short verdict row: "simple ✓ · scales ✗ · affinity ✗ (patchable)" with `tick_mark`/`x_mark`. |

**Characters:** Professor (explaining).
**Ends with:** the pinned schedule grid; verdict strip. Transition: all fades except the section badge and crux strip.
**Implementation notes:** the book's figure for this scene: CPU 0: A E A A A; CPU 1: B B E B B; CPU 2: C C C E C; CPU 3: D D D D E.

### S14 — Attempt 2: one queue per CPU   (beats: B11) · ~1:00
**Purpose:** MQMS: each CPU gets its own queue; scalable and affinity-friendly.
**Starts with:** S13 end state, cleared.
**Layout:** two CPUs: CPU 0 at (−3, 1.6) and CPU 1 at (3, 1.6), `CacheCPU` each. **Queue** Q0 below CPU 0 at (−3, −0.2), **Queue** Q1 below CPU 1 at (3, −0.2). ScheduleGrid (2 rows × 8) at the bottom (0, −2.2). The padlock from S09 is shown crossed out at top-center.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "So some systems flip the design around. Give every CPU its own queue." | Two CPUs; two empty Queues "Q0", "Q1" slide in below. The padlock from S11 appears in the middle, then is cut by a diagonal line. |
| 2 | "This is **multi-queue multiprocessor scheduling**, or **MQMS**." | Term highlight "MQMS". |
| 3 | "Each queue runs its own policy, say round robin." | A small tag "round robin" under each queue. |
| 4 | "A new job gets placed on exactly one queue, by some heuristic: pick randomly, or the one with fewer jobs." | A, B, C, D arrive from the top-left (hop in). A → Q0, B → Q1, C → Q0, D → Q1 (each with a tiny heuristic tag "fewer jobs"). |
| 5 | "After that, each CPU schedules *independently*. No shared structure, no shared lock." | The two halves get a dashed divider; no lines between the CPUs. |
| 6 | "CPU zero alternates between A and C, CPU one between B and D." | The ScheduleGrid fills (page 8): CPU 0 = A A C C A A C C…, CPU 1 = B B D D B B D D…. Jobs hop on/off in sync. |
| 7 | "The payoff is real. MQMS is naturally scalable: more CPUs, more queues, and the locks are never in contention." | A third and fourth CPU+Queue pair slide in at the sides (scale to fit); no waiting lines appear. A work/lock bar stays all yellow. |
| 8 | "And a job stays on its CPU, so affinity comes for free." | Warmth meters of the caches fill and stay full. |
| 9 | "That sounds perfect." | Student (excited). |
| 10 | "That is what I would say, if I hadn't been paying attention to the title of the next section." | Professor (worried) with a faint sweat drop. A small label "next: load imbalance" glimmers in the corner. |

**Characters:** Student (excited), Professor (worried).
**Ends with:** two CPUs (the extra pair fades out) with Q0 = A, C, Q1 = B, D; grid with the round-robin pattern.
**Implementation notes:** the extra two CPUs are a flourish; remove them before the next scene so the exact book setup is restored.

### S15 — The trouble: load imbalance   (beats: B12) · ~1:15
**Purpose:** when a job finishes, queues become unbalanced: unfair shares, then an idle CPU. Adapts the book's page 8 figures. Pose the second Crux.
**Starts with:** S14 end state.
**Layout:** same as S14 (two CPUs, two Queues, 2 × 12 ScheduleGrid). The Computer at bottom-center (0, −2.9), scale 0.6, busy.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Suppose job C finishes." | C (gold) does a check (done) in Q0 and fades. Q0 now holds only A. |
| 2 | "Queue zero now holds only A. Queue one still holds B and D." | Highlight the queues. |
| 3 | "Run round robin on each queue independently, and what happens?" | The grid continues: CPU 0 fills with A A A A A A…, CPU 1 continues B B D D B B D D. |
| 4 | "CPU zero runs A, and only A, all the time. CPU one still splits its time between B and D." | The grid fills at 0.5 s per column for ~11 columns. |
| 5 | "So A gets *twice* as much CPU as B or D. That's not the fair share the scheduler wanted." | A brace over CPU 0's row labeled "A: 100%"; one over CPU 1's row labeled "B: 50%, D: 50%". `MathTex("2\\times")` flash. Student (confused). |
| 6 | "It gets worse. Suppose A finishes too." | A does a check and fades out of Q0. |
| 7 | "Queue zero is now empty. CPU zero has nothing to do." | CPU 0's chip drains its color to dark; grid row CPU 0 fills with hatched idle cells; Q0 shows only the label with a tiny "NULL". |
| 8 | "It sits idle, while CPU one is juggling two jobs. How terrible." | The Computer → sleeping (zZz); CPU 0 gets a "zzz" tag, a clock; CPU 1 on its own flickers between B and D. Dramatic: the lower-third gets a thin "(dramatic and sinister music)" caption in `DIM` italics. |
| 9 | "This is **load imbalance**, the fundamental problem of multi-queue scheduling." | Term highlight "load imbalance". The hatched row pulses. |
| 10 | "And that leaves us with a second crux: {question}" | A second small Crux card slides in: **"How to deal with load imbalance?"** subtitle (DIM): "How should a multi-queue multiprocessor scheduler handle load imbalance, so as to better achieve its desired scheduling goals?" It replaces the crux strip at the top. |

**Characters:** Student (confused → frustrated), Professor (worried), Computer (busy → sleeping).
**Ends with:** CPU 0 idle (hatched row), CPU 1 alternating B and D; Q0 empty, Q1 = B, D; crux strip for load imbalance at the top.
**Implementation notes:** the book gives three figures: (1) Q0 = A, Q1 = B, D; (2) CPU 0 all A, CPU 1 BBDD…; (3) Q0 empty and CPU 0 blank. Use the hatched idle encoding from the bible.

### S16 — Migration: the easy case   (beats: B13, first part) · ~0:35
**Purpose:** fix an idle CPU by moving a job to it.
**Starts with:** S15 end state.
**Layout:** same stage; grid cleared; CPU 0 at (−3, 1.6), CPU 1 at (3, 1.6), Q0 empty, Q1 = B, D.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "The obvious answer: move jobs around. We've seen this word before. **Migration**." | Term highlight "migration". A suitcase glyph (`DIM`) appears. |
| 2 | "Take a job from a busy CPU, and give it to an idle one." | A dotted arrow from Q1 to Q0 pulses. |
| 3 | "The easy case first. Queue zero is empty, queue one holds B and D." | Hold; both queues highlight. |
| 4 | "Just move one of them, say B, over to CPU zero." | B (mint) hops from Q1 to Q0 (suitcase attached); CPU 0 wakes up (color returns). B's warmth: cache 0 meter fills, starts from empty. |
| 5 | "One migration, balanced load, everybody's happy." | The grid: CPU 0 = B B B B…, CPU 1 = D D D D…. Both rows full. Tick. Student (excited). |

**Characters:** Student (curious → excited).
**Ends with:** Q0 = B, Q1 = D; both CPUs busy; grid two full rows.
**Implementation notes:** the migrate hop must use `hop_to` with the suitcase glyph attached.

### S17 — Migration: the tricky case   (beats: B13, second part) · ~0:50
**Purpose:** when one migration isn't enough: three jobs on two CPUs need continuous migration. Adapts the page-9 figure.
**Starts with:** S16 end state, rewound to the state "A alone on CPU 0, B and D on CPU 1".
**Layout:** same stage. Q0 = A; Q1 = B, D. Grid (2 × 12), cell 0.6 × 0.5.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "And the harder case?" | Student (curious). The stage rewinds to Q0 = A, Q1 = B, D (A comes back in). |
| 2 | "Here's a trickier one. A is alone on CPU zero. B and D share CPU one." | Highlight. |
| 3 | "One migration doesn't fix this: moving B just flips the problem." | B hops to Q0 (A and B now share CPU 0) and D is alone on CPU 1, a "↔" flip: then reversed. A red "same problem, flipped" tag. (Use `MathTex(r"\leftrightarrow")` for the arrow.) |
| 4 | "The load is three jobs on two CPUs. Nobody can give a whole CPU's worth to everyone, so the answer is *continuous* migration." | A fraction "3 jobs / 2 CPUs = 1.5" (`MathTex`) appears; a loop arrow around the suitcase. |
| 5 | "First A alone on CPU zero, and B and D alternate on CPU one." | Grid: CPU 0 = A A A A…, CPU 1 = B D B D…. (The book's first four columns: A A A A on CPU 0 and B D B D on CPU 1.) |
| 6 | "After a few time slices, B moves to CPU zero to compete with A…" | B hops over; CPU 0 columns 5–8 alternate A and B (B A B A); the cache meters flash "cold" for B on CPU 0. |
| 7 | "…while D enjoys a few slices alone on CPU one." | CPU 1 columns 5–8: D D D D. |
| 8 | "And the load stays balanced, over time." | Later columns: A and D swap roles (A hops to CPU 1, the book's columns 9–12 with A D A D … and B B B B on CPU 0). The "everyone gets 2/3 of a CPU" tag with a brace over each job's share. |
| 9 | "There are many other migration patterns. But the real question is the decision: *how* should the system decide to migrate?" | Professor (explaining). A "?" over the suitcase. Hold 1 s. |

**Characters:** Student (curious), Professor (explaining).
**Ends with:** the filled schedule (page 9 figure), suitcase glyph, "?" over it.
**Implementation notes:** book's final timeline for reference: CPU 0 = A A A A B A B A B B B B; CPU 1 = B D B D D D D A D A D … (Verify against the PDF when coding: it is the page-9 figure; copy it exactly.) Make sure the grid letters line up with the migrations being narrated, with B and A changing places.

### S18 — Work stealing   (beats: B14) · ~1:00
**Purpose:** work stealing is a decentralized way to decide when to migrate. The tension: peeking too often vs. too rarely.
**Starts with:** S17 end state, cleared.
**Layout:** two CPUs with Queues: Q0 (low on jobs) at left (−3, −0.2), Q1 (full: B, D, E) at right (3, −0.2). A small eye glyph above Q0 (the "source" queue) and a dotted arc to Q1. A small tag row at the bottom.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "One basic approach is **work stealing**." | Term highlight "work stealing". Q0 holds just A (running), Q1 holds B, D, E. |
| 2 | "A queue that's running low on jobs occasionally *peeks* at another queue to see how full it is." | The eye glyph hops from Q0 to Q1 and a small level gauge pops up over Q1 ("3 jobs"), then the eye returns. |
| 3 | "If the other queue is notably fuller, the low queue **steals** one or more jobs to balance the load." | A job (E) slides from Q1's tail to Q0 (the suitcase is replaced by a small "stolen" hand icon). Q0 = A, E; Q1 = B, D. The two gauges now match. |
| 4 | "How often should it peek?" | Student (confused). |
| 5 | "There's the catch. If CPUs peek too often, they take locks on each other's queues…" | A "peek" frequency dial turns to MAX: eyes rapidly hop back and forth; a padlock appears on Q1 with an increasing line of waiting eyes. |
| 6 | "…the overhead goes up, and we've rebuilt SQMS, the thing we were trying to escape." | The two queues merge visually into one shared queue with the padlock (a quick `Transform` into the S11 picture); the label "SQMS again!" appears. |
| 7 | "If they peek too rarely, we're back to severe load imbalance." | Dial back to MIN: the eye barely moves; CPU 0's row hatches idle again; Q1 stays full. |
| 8 | "Finding the right threshold is, as is common in system policy design, a black art." | The dial is set between the two extremes (a small "sweet spot?" with a wobbling needle); a small cauldron icon (black art, simple pot made of a semicircle) briefly bubbles. |
| 9 | "That's the honest answer. And here's another tension: every steal throws away a bit of cache affinity." | Professor (happy → neutral). The stolen job's cache meter flashes empty on the new CPU. |

**Characters:** Student (confused), Professor (happy).
**Ends with:** the dial at "?", Q0 = A, E and Q1 = B, D; affinity flash fading.
**Implementation notes:** the dial can be `SpeedGauge` repurposed with labels "rarely"/"often". The cauldron is optional.

### S19 — What Linux did   (beats: B15) · ~0:50
**Purpose:** real systems chose different answers: O(1) and CFS multi-queue, BFS single-queue.
**Starts with:** S18 end state, cleared.
**Layout:** three cards across the center, each 3.4 × 3.2: x = −4, 0, 4; y = 0.3. Each has a title, a mini queue picture and a tag at its bottom.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "So what does a real system do? Interestingly, in the Linux community no single solution won." | A penguin-free generic "Linux" tag (a plain text "Linux" in `MONO_FONT`) appears at the top. |
| 2 | "Three different multiprocessor schedulers arose over time." | Three cards slide in, empty. |
| 3 | "The **O(1) scheduler**, the **Completely Fair Scheduler**, or **CFS**, and the **BF Scheduler**, or **BFS**." | Titles write in, one per card: "O(1)", "CFS", "BFS". |
| 4 | "O(1) and CFS use *multiple* queues. BFS uses a *single* queue." | Under O(1) and CFS: a mini picture of 2 small queues feeding 2 CPUs; under BFS a mini picture of one queue feeding 2 CPUs (re-uses the SQMS/MQMS pictures). |
| 5 | "So, both approaches can work, in practice." | A green tick between the single and multi pictures. |
| 6 | "O(1) is a priority-based scheduler, a bit like the MLFQ we saw before." | The O(1) card's tag: "priority-based (MLFQ-like) · interactivity". A mini staircase of priority levels. |
| 7 | "CFS, in contrast, is deterministic and proportional-share, like the stride scheduling from last time." | The CFS card's tag: "proportional share (stride-like)". A mini pie/share bar. |
| 8 | "BFS is also proportional-share, but built on a more complicated scheme called Earliest Eligible Virtual Deadline First, EEVDF." | The BFS card's tag: "proportional share · EEVDF". |
| 9 | "And about that 'BF' in BFS: the book says you should look it up yourself." | A small sticker on BFS: "(look it up!)" with a cheeky magnifier. Student (curious → surprised). |
| 10 | "Read more about them on your own." | An Aside card at the bottom: "Meehan's dissertation, linked below". |

**Characters:** Student (curious → surprised), Professor (happy).
**Ends with:** the three cards.
**Implementation notes:** no logos or penguin images. Pure shapes and text. The cards are plain rounded rectangles in `DIM` frames.

### S20 — The big picture   (beats: B16) · ~0:50
**Purpose:** compare SQMS vs MQMS and close the loop: no simple answer.
**Starts with:** S19 end state.
**Layout:** a comparison table at center (0, 0.3), 10 × 3.6: header row with a tiny SQMS picture (one queue, padlock) and MQMS picture (two queues). Rows: "simple", "scales", "keeps affinity", "balances load". The characters are in corner mode.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Let's put it all in one place." | The three cards morph to the two headers (SQMS, MQMS). |
| 2 | "The single-queue approach is simple to build and balances load well…" | SQMS column: "simple" ✓, "balances load" ✓ (green). |
| 3 | "…but struggles to scale to many processors, and loses cache affinity." | "scales" ✗, "keeps affinity" ✗ (red) with the padlock and the bouncing-job icon. |
| 4 | "The multi-queue approach scales better and handles affinity well…" | MQMS column: "scales" ✓, "keeps affinity" ✓. |
| 5 | "…but has trouble with load imbalance, and is more complicated." | "balances load" ✗, "simple" ✗ (with a hatched idle CPU icon). |
| 6 | "Whichever approach you choose, there is no simple answer." | The two columns pulse equally; a balance scale glyph tilts both ways. |
| 7 | "Building a general-purpose scheduler remains a daunting task, because small code changes can lead to large behavioral differences." | A small `Code`-edit icon (1 line changed) causes the schedule grid thumbnail to reshuffle. |
| 8 | "Only try it if you know exactly what you are doing, or, at least, if you are getting paid a large amount of money to do so." | A money-meter glyph (`money_meter` icon) rises. Professor (proud, with a wry look). |

**Characters:** Professor (proud), Student (neutral).
**Ends with:** the comparison table.

### S21 — Recap   (beats: B17) · ~0:35
**Purpose:** five takeaways.
**Starts with:** S20 end state.
**Layout:** numbered list at left (−5.6 .. 1), font 28; icons at x = 4.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "So, today:" | Table fades; header "Recap" in `VIRT`. |
| 2 | "Programs that use one CPU don't speed up on many…" | Line 1; icon: a row of CPU chips, one lit. |
| 3 | "**Caches** use locality to speed things up; with several CPUs, hardware keeps them **coherent** by **bus snooping**." | Line 2; icon: two caches and the bus with an eye. |
| 4 | "Shared data still needs **locks**, which slow down as CPUs grow." | Line 3; icon: padlock with waiting line. |
| 5 | "**Cache affinity**: keep a job on the same CPU when you can." | Line 4; icon: warmth meter + pin. |
| 6 | "**SQMS** is simple but doesn't scale or keep affinity. **MQMS** scales, but suffers **load imbalance**, fixed by **migration** and **work stealing**." | Line 5; icon: the two queue pictures with the suitcase. Hold 1.5 s. |

**Ends with:** the full list. Section badge fades out.

### S22 — Teaser   (beats: B18) · ~0:30
**Purpose:** hook for 11 and for the concurrency section.
**Starts with:** S21 end state.
**Layout:** dialogue mode.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "So after all this, we know how to schedule on one CPU, and on many. What's left?" | The list fades; characters move to dialogue positions. Student (curious). |
| 2 | "One more short conversation, to pull the whole virtualization of the CPU together." | Professor (happy). A small CPU icon with a ribbon ("CPU virtualized ✓") appears between them. |
| 3 | "And then we leave the CPU behind, and virtualize memory." | A Memory column slides in next to the CPU icon. |
| 4 | "But we will meet those locks again. Much of this chapter said 'we'll see later'." | The padlock and a thread glyph hop onto a "Part 2" tag in the corner. |
| 5 | "Later is the concurrency section: threads, locks, and what they cost. Next: the CPU virtualization dialogue." | Cut to black. Then "Next: 11 · Summary Dialogue" in `TEXT` with a `VIRT` dot. Hold 2 s. |

**Characters:** Student (curious), Professor (happy).
**Ends with:** black end card.

## New assets needed
- **`CacheCPU(label, size)`** (`CPU` plus a cache strip attached below it): a cache strip with 3 mini cells, `MEM_COLOR` outline; methods: `.store(value, color)` (fills the next cell), `.invalidate(cell)` (strike-through and fade), `.set_value(cell, text)`, `.warmth(level, color)` (fills 0–3 cells in a job color), `.clear()`, `.slot_point()` (delegates to the CPU), `.cache_point()` (where data enters/leaves). Used in S04–S18.
- **Cache-hit / miss glyphs:** reuse `tick_mark` / `x_mark`; no new glyph needed.
- **`ScheduleGrid(rows, columns, cell_size)`**: the book's CPU × time-slice table. Rows "CPU 0..n"; cells show a job letter on a job-colored fill; `.fill(row, col, job)` returns an animation; `.fill_row(row, jobs)`, `.hatch(row, col)` for idle (bible's hatched-grey), `.highlight_job(job)`, `.clear()`, "… (repeat) …" label. (A thin wrapper over `Timeline` would do: `Timeline` colors blocks by row, but here color is per job.)
- **Eye glyph** (`eye_icon`): simple circle with a pupil that can look toward a point; used for bus snooping (S07) and peeking (S18).
- **Suitcase glyph** (`suitcase_icon`): small rounded rectangle with a handle, for migration (S13, S16–S18).
- **Pushpin glyph** (`pin_icon`): for affinity (S10, S13, S20).
- **`Bus` extension:** `Bus.pulse(a, b)` helper returning a passing-flash + a dot along the path (the core `Bus.path` exists). Taps from several caches.
- **Warmth meter:** covered by `CacheCPU.warmth`, no separate prop.
- **Existing items used as-is:** `CPU`, `Memory`, `Bus`, `Queue`, `Timeline` (hatch), `padlock`, `stopwatch`, `money_meter`, `SpeedGauge`, `MemoryStrip`, `make_thread`, `Laptop`, `Code`, `CruxCard`, `AsideCard`, `TermHighlight`, `SectionBadge`, `hop_to`.
- **Library note:** a Process "confused" isn't an available expression (only ready/running/blocked/done/zombie), so S06 step 11 uses a speech bubble from the Process instead.

## Open questions
- **Length (~16 min).** This episode is over the bible's 8–15 min. Split into two episodes (hardware / scheduling), or trim S05, S10, S13? I recommend keeping it as one for now, and recording first to measure.
- **Cache coherence level.** I follow the book: only invalidate/update and bus snooping, no MESI. OK?
- **Fake data values.** I use 7 and 9 instead of the book's D and D′ (so as not to clash with job D). A caption mentions the book's names once.
- **Process expression gap.** S06 wants a "confused" Process; there is none. I used a "7?" bubble. Alternatively add a `confused` expression to `Process`. Your call.
- **S19 visual:** three plain cards (no logos). OK, or would you prefer a timeline of dates? The book gives none, so I avoided inventing any.
- **S12/S13/S17 grids.** The ScheduleGrid copies the book's tables (page 6, 7, 8, 9). When implementing, the letters should be rechecked against the PDF (I read them from the rendered pages).
- **Callbacks to 07–09** (round robin, MLFQ, stride/CFS): confirm those episodes cover them as assumed.
