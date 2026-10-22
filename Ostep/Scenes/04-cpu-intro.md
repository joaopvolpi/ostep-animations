# 04 — The Abstraction: The Process · Scene breakdown
> Script: Ostep/Scripts/04-cpu-intro.md · Scenes: 22 · Est. duration: ~12:00

## Visual overview
- **Core metaphor: processes are creatures that take turns on a single CPU.** The episode builds
  one "world" step by step. The single **CPU** chip sits at a fixed home position. Process creatures
  hop on and off it. A **Timeline** records who ran when. By the end, the same world also has a
  **Memory** column, a **Disk**, a ready **Queue**, a blocked area, and a **process list** of PCB cards.
  The big-picture scene (S20) shows them all at once.
- **Second metaphor: a process is a snapshot you can freeze and resume** (the "save slot").
  It's introduced in S09 as three panels (memory, registers, open files), and pays off in S18 as
  xv6's `struct context`.
- **Signature motif: Illusion split** (left "what each program sees", right "what really happens")
  in S06. It is resolved in S20 when the two halves merge.
- Props used (from the bible): Crux card, Tip card, Term highlight, Section badge, CPU, Memory,
  Disk, Timeline, Queue, Illusion split, Code block. Characters: Professor, Student, Computer, Process.

### Persistent assignments
| Thing | Look | Notes |
|---|---|---|
| Process **A** | `Process(label="A", color=PROCESS_COLORS[0])` (coral) | Time-sharing scenes (S06–S08). |
| Process **B** | `PROCESS_COLORS[1]` (mint) | |
| Process **C** | `PROCESS_COLORS[2]` (gold) | |
| Process **D** | `PROCESS_COLORS[3]` (sky) | Only in S01/S20 crowds. |
| **P0** / **P1** (traces) | coral / mint (same colors as A / B), labels "P0" and "P1" | The book's Process₀ and Process₁. Narration says "process zero / one". |
| CPU home | `CPU_COLOR` chip, 1.4 × 1.4, at **(0, 0.6)** in "world" scenes | A running process stands *on top* of the chip (bottom edge touching the chip's top). |
| Timeline home | Along the bottom, **y = −2.2**, x from −5 to 5 | One row per process, rows 0.45 tall. |
| Characters (corner mode) | Student at **(−5.8, −2.8)**, scale 0.75, facing right. Professor at **(5.8, −2.8)**, scale 0.75, `flip()` (facing left) | Default. "Dialogue mode" (S01, S22): Student (−2.6, −1.2) and Professor (2.6, −1.2), scale 1. |
| Section badge | Top-left at (−6.6, 3.6), left-aligned: small `VIRT` dot + "04 · The Process", font 22, `DIM` | Appears in S03, stays on until S21. |
| Term highlight | New term written at (0, 2.9), font 54, `TEXT`, with a `VIRT` underline; after ~1.5 s it shrinks to font 26 at top-right (6.6, 3.6, right-aligned), replacing the previous term | Used for every bolded term's first appearance. |

### Timeline state encoding (used in S06, S14–S16, S20)
| State | Block look |
|---|---|
| running | Solid fill in the process color, `TEXT` stroke 1 |
| ready | Process color outline only (fill opacity 0.15) |
| blocked | `DIM` fill at 0.35 opacity + a tiny clock glyph |
| idle CPU | Dark grey `#333333` with diagonal hatching |
| done / not present | Empty |

## Scenes

### S01 — A hundred programs   (beats: B01, first half) · ~0:30
**Purpose:** feel the scale: dozens of programs are running "at once" on an ordinary computer.
**Starts with:** empty (BG).
**Layout:** laptop outline centered at (0, 0.3), 5 wide. A counter at top-right (4.8, 3.0). Characters in dialogue mode, entering later.

| # | Narration (exact words the action lands on) | On screen / animation |
|---|---|---|
| 1 | "Look at your computer right now." | `Create` the laptop outline (screen + base trapezoid), `TEXT` stroke 3. |
| 2 | "A web browser." | Browser icon (rounded rect with tab strip) pops out of the screen and floats to (−3, 2.2). `GrowFromCenter`. |
| 3 | "Music playing." | Music-note icon pops out to (−1, 2.8); small eighth notes drift up from it. |
| 4 | "A chat app, a game in the background, maybe a mail client." | Chat bubble, game pad, envelope icons pop out 0.3 s apart to (1, 2.8), (3, 2.2), (3.8, 0.8). |
| 5 | "Open a task manager…" | A task-manager panel slides up over the laptop screen: a scrolling list of grey rows. |
| 6 | "…tens, maybe hundreds of programs…" | The list scrolls faster. Counter "programs: 12" ticks up to **"programs: 137"** (`ChangingDecimal`, 1.5 s). |
| 7 | "…all running *at the same time*." | All icons pulse (`Indicate` together). Pause 0.5 s. |
| 8 | "Okay, sure. That's just… what computers do." | Student slides in from the left to dialogue position (curious) and shrugs at the laptop. |

**Characters:** Student (curious) enters at step 8.
**Ends with:** laptop + 5 icons + task-manager panel + counter "programs: 137"; Student at (−2.6, −1.2).
**Implementation notes:** icons are simple geometric glyphs (no SVG). Keep them ~0.6 units. The task-manager rows are `Rectangle`s with `DIM` fill, moved with an updater for the scroll effect.

### S02 — Open the case   (beats: B01, second half) · ~0:30
**Purpose:** contrast: 137 programs vs. **one** CPU. Each program acts as if it owns a CPU.
**Starts with:** S01 end state.
**Layout:** laptop zooms out of frame; inside view shows a motherboard rectangle (−4..4, −1.5..2), CPU chip at (0, 0.6). Counters at top-right.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Is it? Let's open the case and count the CPUs." | Professor enters right (thinking). The app icons fade; the camera zooms into the laptop screen (scale the laptop ×4 around center while fading it), revealing a dark-green motherboard rectangle with faint traces. |
| 2 | "One." | The CPU chip `GrowFromCenter` at (0, 0.6). A second counter "CPUs: **1**" appears under "programs: 137". |
| 3 | "Maybe four, or eight. Not a hundred." | Three ghost chips appear briefly at (±2.2, 0.6) and (0, 2), counter flickers 4 → 8, then the ghosts fade and the counter returns to 1. |
| 4 | "Each CPU can only follow one stream of instructions at a time." | A thin bright line (instruction stream) enters the chip from the left; a single dot travels along it. |
| 5 | "And yet every one of those programs behaves as if it had a CPU all to itself." | Five small process-colored copies of the chip appear in a row along y = 2.6, each with a tiny app icon above. They shimmer (opacity 0.4 ↔ 0.8). The real chip stays solid. |
| 6 | "So… the computer is lying to us?" | Student → confused. The **Computer** pops up at bottom-center (0, −2.6), scale 0.7, surprised. |
| 7 | "Beautifully. And today we learn how." | Professor → proud. Pause 1 s. |

**Characters:** Professor (thinking → proud), Student (confused), Computer (surprised).
**Ends with:** motherboard + real CPU at (0, 0.6) + 5 shimmering "virtual CPUs" + counters; all three characters.
**Implementation notes:** the "zoom in" is just scale + fade; no camera movement needed (keep a `Scene`, not a `MovingCameraScene`).

### S03 — The Crux   (beats: B02) · ~0:25
**Purpose:** state the episode's question, and link it to the `cpu` demo from 01–03.
**Starts with:** S02 end state.
**Layout:** Crux card centered (0, 0.3), 9 × 3. Characters move to corner mode.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | (transition) | Motherboard, virtual CPUs and counters `FadeOut`. The real CPU shrinks and moves to the top-left as a tiny icon inside the forming **Section badge** "04 · The Process". The Computer exits down. Characters glide to corner mode. |
| 2 | (card appears) | Crux card: `VIRT` frame, "THE CRUX" header (font 22, `VIRT`), question in bold (font 34): **"How to provide the illusion of many CPUs?"** `Write`. |
| 3 | "Last time, we watched the OS pull off this trick with four copies of a tiny program, printing A, B, C and D." | A small terminal thumbnail slides in under the card (0, −1.8) showing the `./cpu` output "A B D C A B D C" scrolling (callback to 01–03). |
| 4 | "Today we find out what it's actually juggling." | Terminal thumbnail fades. The card's subtitle writes in, smaller and `DIM`: "Although there are only a few physical CPUs available, how can the OS provide the illusion of a nearly-endless supply of said CPUs?" |
| 5 | "…introduces the most fundamental idea the operating system gives us." | The card shrinks to the top-center (0, 3.2) as a one-line strip, "How to provide the illusion of many CPUs?", font 24, kept for S04–S06. |

**Characters:** corner mode; Student looks at the card (`look_at`), Professor neutral.
**Ends with:** section badge, crux strip at the top, characters in corners. Nothing else.

### S04 — Sheet music is not a song   (beats: B03) · ~0:55
**Purpose:** program = static bytes on disk; process = that program running. One program can be many processes.
**Starts with:** S03 end state.
**Layout:** **Disk** at left (−4, −0.3). A file icon sits on the disk. Center stage (1, 0.3) is empty space for the "performance".

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "First, a distinction. A **program** is a lifeless thing." | The crux strip fades out. Disk (`DISK_COLOR` cylinder) `FadeIn` at (−4, −0.3). A grey file icon (page with folded corner, labeled `browser`) sits on top. |
| 2 | "It's a file on your disk, a bunch of instructions and maybe some static data." | The file icon opens briefly to show 4 grey lines of pseudo-instructions and a small "data" block. Everything is `DIM`, no motion. |
| 3 | "It just sits there, waiting to spring into action." | Hold. A tiny "zZ" above the file. |
| 4 | "Think of sheet music. Sheet music is not a song." | Beside the disk, the file icon morphs (`Transform`) into a sheet of music (five staff lines + notes), still grey. |
| 5 | "Nothing happens until someone performs it." | Musical notes lift off the sheet and float toward center stage, gaining color. |
| 6 | "The operating system is the performer. It takes those bytes and brings them to life." | The sheet morphs back into the file icon. The file icon flies to center (1, 0.3) and `Transform`s into a **Process** creature (coral, label "browser", expression ready). Its eyes open (`blink`). |
| 7 | "That living, running program has a name: a **process**." | Term highlight "process" (with `VIRT` underline). |
| 8 | "*A process is a running program.*" | Under the process, the text "process = a running program" writes (font 30). |
| 9 | "So if I open two browser windows…" | Student (curious) points. The same file on the disk glows again. |
| 10 | "One program, two performances. Two processes." | A second copy of the file flies to (3, 0.3) and becomes a mint Process "browser". A brace under both processes is labeled "1 program → 2 processes". Professor → happy. |

**Characters:** Student (curious), Professor (happy).
**Ends with:** disk + file at left, two processes (coral, mint) at center, brace label. The term strip shows "process".
**Implementation notes:** both processes keep the label "browser" here. In S05 they get relabeled A and B (crossfade the label), and C is added.

### S05 — One CPU per process?   (beats: B04, first part) · ~0:25
**Purpose:** the naive solution (more CPUs) doesn't scale.
**Starts with:** S04 end state.
**Layout:** CPU home (0, 0.6).

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "So we have a hundred processes and one CPU. Easy: just buy more CPUs." | Disk, file and brace fade. The two processes relabel to **A**, **B**. A third, **C** (gold), hops in. The real CPU `GrowFromCenter` at (0, 0.6). Student (excited). |
| 2 | "One CPU per process? We'd need a hundred chips…" | A, B and C each get their own chip beneath them (they spread to x = −3, 0, 3). Then more processes spill in from the edges and each spawns a chip; chips tile the screen rapidly (~40 chips in a grid). Professor (worried). |
| 3 | "…then a thousand when you open more tabs. That doesn't scale." | The grid shrinks into a dense swarm, then shatters (`FadeOut` with scale 0.5, shift down). Only A, B, C and the one real CPU remain. Student → sad. |

**Ends with:** CPU at home (0, 0.6); A, B, C standing in a row at y = −0.9 (x = −2, 0, 2), expression ready.

### S06 — Taking turns: the illusion split   (beats: B04, middle) · ~0:55
**Purpose:** time sharing: one CPU, rapid turns, so each process *seems* to have its own CPU. Show the cost (each runs slower).
**Starts with:** S05 end state.
**Layout:** **Illusion split**: a vertical dashed divider at x = 0. Left half title "What each program sees" (−3.5, 3.0); right half "What really happens" (3.5, 3.0). Left: A, B, C, each on its own *virtual* CPU (translucent chips at x = −5.2, −3.5, −1.8, y = 0.6). Right: the real CPU at (3.5, 0.6), with A, B, C queued below it at y = −0.9. Timeline across the bottom of the right half (x 0.5..6.3, y = −2.4).

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Here's what the OS does instead." | The divider draws top to bottom. The real CPU slides to (3.5, 0.6), and A/B/C follow to (2.3, −0.9), (3.5, −0.9), (4.7, −0.9). Translucent copies of A/B/C and three translucent CPUs appear on the left. |
| 2 | "It runs process A for a tiny slice of time." | Right: A hops onto the real CPU (arc path, 0.4 s) → running. The first coral block fills on the timeline (row A). Left: virtual A glows (running). |
| 3 | "Then it stops A and runs B." | A hops back to its spot (→ ready); B hops on (→ running). Mint block on row B. |
| 4 | "Then C. Then back to A." | Same for C, then A. |
| 5 | "Each slice lasts only a few milliseconds." | The tick labels on the timeline read "ms". The hopping speeds up ×4 (8 more slices in 2 s), until the processes blur into a flicker on the CPU. |
| 6 | "To any human, and in a sense to each program, it looks like they're all running at once." | Left side: all three virtual processes are steadily "running" with no flicker. Hold 1 s so the contrast is clear. |
| 7 | "This is **virtualizing the CPU**: turning one physical CPU into what looks like many virtual ones." | Term highlight "virtualizing the CPU". Labels "virtual" (left, under the translucent CPUs) and "physical" (right, under the real CPU). |
| 8 | "It's our peach again: snatch it from whoever isn't using it, and hand it to the next eater." | A small peach icon (callback to 01–03) appears on the real CPU for 1.5 s, then morphs back into the chip. |
| 9 | "The basic technique is called **time sharing**." | Term highlight "time sharing". The timeline's alternating colored slices `Indicate`. |
| 10 | "It's like a juggler! Only one ball in the hand at a time, but they're all in the air." | Student (excited). A small thought-bubble from the Student with three balls (coral, mint, gold) juggled in an arc above one hand (`thinks` with a custom mobject, looped 2 s). |
| 11 | "But notice the price. If three processes share one CPU, each one runs *slower* than it would alone." | Professor (explaining). Left side: a speed gauge under each virtual CPU drops from "100%" to "~33%". On the right timeline, brace row A's blocks: "A gets 1/3 of the time". |
| 12 | "Time sharing trades performance for the illusion." | Hold 1 s. |

**Characters:** Student (excited), Professor (explaining); they react only and stay in the corners.
**Ends with:** full illusion split, timeline with ~12 slices. The term strip shows "time sharing".
**Implementation notes:** write a `hop_to(process, point)` helper (ArcBetweenPoints path + squash/stretch scale). Timeline blocks are `Rectangle`s appended to a VGroup per row. The speed-up uses decreasing `run_time` in a loop.

### S07 — Tip: space sharing   (beats: B04, end) · ~0:20
**Purpose:** contrast time sharing with space sharing.
**Starts with:** S06 end state.
**Layout:** a Tip card slides in from the right and covers the right 45% of the screen (x 1..6.6, y −1.5..2.5).

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "By the way, time sharing has a sibling: **space sharing**." | The illusion split dims to 30%. The Tip card slides in ("TIP" header, `DIM` frame). Term highlight "space sharing", but smaller (inside the card, no move to the top bar). |
| 2 | "Instead of taking turns, you split the resource up. Your disk works like this." | Inside the card: a horizontal disk bar (`DISK_COLOR` outline) divided into 8 blocks. |
| 3 | "A block given to one file stays with that file until the file is deleted." | Blocks fill: 3 coral ("file A"), 2 mint ("file B"); they stay put while a clock icon spins. A small comparison row: "time sharing: take turns ⟳ / space sharing: split up ▦". |
| 4 | (end) | The Tip card slides out; the illusion split un-dims. |

**Ends with:** S06 end state.

### S08 — How vs. which   (beats: B05) · ~1:05
**Purpose:** mechanism = *how* (context switch); policy = *which* (scheduling policy); keep them separate (modularity).
**Starts with:** S06 end state.
**Layout:** the split collapses into the right-side world: CPU at (0, 0.6), and A, B, C as a ready **Queue** at bottom (x −2..2, y −1.2) labeled "Ready". Then the screen splits horizontally into two panels: left "HOW · mechanism" (x −6.6..−0.3), right "WHICH · policy" (x 0.3..6.6), both y −1.8..2.6.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Wait, but somebody has to *do* the switching. And somebody has to decide who's next." | Left half (virtual side) fades; the right world slides to center. A is on the CPU (running), B and C in the queue. Student (confused). Two question marks pop: one over the CPU ("do?"), one over the queue ("who?"). |
| 2 | "Two different jobs. You've just spotted one of the best design ideas in operating systems." | Professor (proud). The screen splits into the two panels. A copy of the CPU + A goes to the left panel; a copy of the queue B, C goes to the right. |
| 3 | "The first job is a **mechanism**." | Term highlight "mechanism". The left panel header "HOW" writes. |
| 4 | "That's low-level machinery that answers a *how* question." | Two meshing gears appear in the left panel and rotate. |
| 5 | "*How* do we stop one program and start another?" | A robotic arm built from simple lines (mechanism) lifts A off the CPU and sets a placeholder process on it. |
| 6 | "That mechanism is called a **context switch**, and it gets its own episode later." | Term highlight "context switch". A small tag "→ Ep. 06" sticks onto the gear. |
| 7 | "The second job is a **policy**." | Term highlight "policy". The right panel header "WHICH" writes. |
| 8 | "*which* one should run now? That's a **scheduling policy**." | A pointing hand (or a spotlight cone from above) sweeps across B and C and stops on C. Term "scheduling policy" (small, in the panel). |
| 9 | "It might look at history (who ran the most in the last minute?)…" | Above the queue, three small chips appear one by one: a mini bar chart "history"… |
| 10 | "…at what kind of programs these are…" | …a tag icon "workload"… |
| 11 | "…or at what we're optimizing for: snappy interaction or total throughput." | …a dial with two ends, "interactive ↔ throughput". |
| 12 | "Keeping the two apart is a form of **modularity**." | Term highlight "modularity". The divider between the panels becomes a clean seam; a Tip card title "Separate policy and mechanism" appears across the top center. |
| 13 | "You can swap in a smarter policy without rebuilding the machinery underneath." | The right panel's spotlight is replaced by a different one (it slides out, a new one slides in, now pointing at B) while the left gears keep turning, unaffected. |

**Characters:** Student (confused), Professor (proud).
**Ends with:** both panels visible. Transition: everything fades except the CPU with A on it, which returns to (0, 0.6).
**Implementation notes:** keep the robotic arm cheap: two `Line`s plus a `Circle` joint, animated with `Rotate`.

### S09 — Freeze frame: machine state   (beats: B06) · ~1:30
**Purpose:** a process = machine state: address space (memory), registers (PC, stack pointer, frame pointer), I/O info (open files). "What must we write down to resume it?"
**Starts with:** CPU at (0, 0.6) with A on it (running).
**Layout:** A + CPU move to center-left (−0.5, 0.2). Three panels form around them: **Memory** column at left (−4.6, 0.2), 1.4 wide × 4.4 tall; **register bank** at right (3.6, 1.2), a 2 × 4 grid of small boxes; **open files** list at right-bottom (3.6, −1.6).

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "…if the OS is going to stop a process and resume it later, it needs to know exactly what a process *is*." | A is running on the CPU, with speed lines. |
| 2 | "Suppose we freeze a process mid-step." | **Freeze:** the whole screen desaturates (overlay at 40% `BG`), A's speed lines stop, and a pause glyph ⏸ appears over A. A camera-shutter flash (white rectangle, opacity 0.6 → 0, 0.2 s). |
| 3 | "What would we have to write down to bring it back perfectly?" | A blank clipboard / notepad appears at the bottom center (0, −2.4) with "To resume A:" and three empty bullet lines. |
| 4 | "In other words: what parts of the machine can this program read or change? That's its **machine state**." | Professor (explaining). Term highlight "machine state". |
| 5 | "First, **memory**. The instructions live in memory. So does the data the program reads and writes." | The Memory column `Create`s at left, with coral-tinted regions top to bottom: code, static data, heap, (free gap), stack. A line from A to the column. |
| 6 | "The memory a process can address is its **address space**." | A dashed coral brace around the coral regions. Term highlight "address space". The notepad's line 1 fills: "memory (address space)". |
| 7 | "Second, **registers**. Lots of instructions read and update them directly." | The register bank fades in at the right: 8 boxes with tiny values (e.g. `eax 42`, `ebx 7`…). The values flicker as if being written. |
| 8 | "The **program counter**, sometimes called the instruction pointer, says which instruction runs *next*." | One box labeled `PC` turns yellow. An arrow from it points into the memory column's code region, at a highlighted line. Term highlight "program counter (PC)". |
| 9 | "Lose it and the process forgets where it was." | The PC arrow flickers off for 0.3 s and A looks confused (no expression change; just the arrow vanishing and a "?" over the code). Then it comes back. |
| 10 | "The **stack pointer** and **frame pointer** keep track of the stack: function parameters, local variables, return addresses." | Two boxes `SP` and `FP` highlight in `MEM_COLOR`; arrows point to the stack region, where three small frames stack up (labeled params / locals / return addr). Terms highlighted in sequence. Notepad line 2: "registers (PC, SP, FP…)". |
| 11 | "Third, **I/O information**… the list of files it currently has open." | The open-files list appears below the register bank: `0 stdin`, `1 stdout`, `2 stderr`, `3 notes.txt`. Notepad line 3: "open files". |
| 12 | "So a process is a snapshot: memory, registers, open files. Save those and you can pause it like a video game!" | Student (excited). A brace gathers the three panels, labeled **machine state**. The notepad turns into a floppy-disk-like "SAVE SLOT" icon. |
| 13 | "Exactly the right instinct. Hold on to it. It's the heart of the context switch." | Professor (happy). The save-slot icon shrinks and docks in the top-right corner under the term strip (it stays visible as a reminder until S18). Un-freeze: overlay lifts, A starts running again. |

**Characters:** Professor (explaining → happy), Student (excited).
**Ends with:** CPU + A, memory column, register bank, open-files list, save-slot icon docked top-right.
**Implementation notes:** use a 4-region `Memory` helper (see New assets). The register values are `Text` in monospace (`Code` font). Use `ManimColor` interpolation for the freeze desaturation; a dark overlay rectangle is enough.

### S10 — The process menu   (beats: B07) · ~0:45
**Purpose:** what any OS lets you do with processes: create, destroy, wait, misc control, status.
**Starts with:** S09 end state.
**Layout:** a menu card at left (−3.6, 0.2), 4 × 4.6, title "Process API". A demo stage at right (2.8, 0.2) with one process.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "…every OS needs a way to work with them. We'll meet the real API in the next episode." | The S09 panels collapse into A (`Transform` the panels into a small glow that fades), leaving the CPU + A. These slide right to the demo stage. The menu card `FadeIn` with a "→ Ep. 05" tag in the corner. |
| 2 | "**Create**: you double-click an icon or type a command, and a new process is born." | Menu row 1 highlights. Stage: a cursor double-clicks a small icon, and B (mint) pops into existence beside A (`GrowFromCenter` with a bounce). |
| 3 | "**Destroy**: most processes exit on their own, but a runaway one can be killed." | Row 2. B spins around frantically (runaway), then a small "✕" stamps on it and it poofs (scale to 0 + puff particles). |
| 4 | "**Wait**: pause until some process finishes." | Row 3. A new process C appears and runs with a progress ring; A stands next to it with a clock icon (A expression blocked) until the ring completes, then A → ready. |
| 5 | "**Miscellaneous control**: for example, suspend a process for a while, then resume it." | Row 4. A pause ⏸ icon on C (C freezes, greyed), then play ▶ (C unfreezes). |
| 6 | "And **status**: how long has it run, and what state is it in?" | Row 5. An info tag pops out of A: "running · 3.2 s". |
| 7 | "That's… a menu." | Student (bored). |
| 8 | "A very powerful menu. Next episode, we order from it." | Professor (happy). The menu card does a little waiter-style flourish (a slight rotate wiggle). |

**Ends with:** menu card + A on CPU + C beside it. Transition: the menu card and C fade.
**Implementation notes:** the menu terms don't get full term highlights (they're bold in the script but act as a list); a row highlight is enough.

### S11 — Loading: disk to memory   (beats: B08, part 1) · ~0:50
**Purpose:** step 1 of process creation: load code + static data from disk (executable format) into the address space; eagerly vs. lazily.
**Starts with:** CPU + A (A will leave).
**Layout:** adapt **Figure 4.1**: CPU at (−2.6, 1.6) (1.4 × 1.4), Memory column at (2.6, 1.3) (1.4 × 3.4), horizontal bus line at y = −0.6 from x −5 to 5, a vertical stub down to the **Disk** at (0, −2.4). The file icon "program" sits on the disk.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Okay, but 'create' hides a lot. How does a file on disk actually *become* a running process?" | Student (curious). A hops off the CPU and exits right (waving). The CPU slides to (−2.6, 1.6). The Memory column (empty, with address marks) and the bus `Create`; the Disk rises in from below. |
| 2 | "Step one: **load**. Programs start out on disk, or on a flash-based SSD, in an **executable format**." | A step counter tag "1 / 5 · load" at top-center (0, 3.2). The grey "program" file on the disk opens to show two labeled chunks: "code", "static data" (`DIM`). Term highlights "load", then "executable format" (smaller). |
| 3 | "The CPU can't run instructions sitting on disk." | A dotted arrow from CPU straight to the Disk gets a red ✕. |
| 4 | "So the OS reads the code and static data, like initialized variables, into memory, into the new process's address space." | The code chunk and the static-data chunk copy up along the bus (moving along the path disk → bus → memory) and land in the top two regions of the Memory column, turning from `DIM` to the new process's color (sky, `PROCESS_COLORS[3]`, this will be process **D**). A dashed sky outline appears around the column: "address space of D". |
| 5 | "Early, simple systems did this **eagerly**: everything, all at once, before running." | Rewind the copy; replay it as one big block moving all at once. Label "eager". Term highlight "eagerly". |
| 6 | "Modern systems are **lazy**. They load pieces of code and data only when the program actually needs them." | Rewind again; now only a thin slice moves up, then later another slice on demand (a small "need this!" spark at the PC). Label "lazy". Term highlight "lazily". |
| 7 | "How that works needs paging and swapping, which come later in the series." | Tag "→ Ep. 18, 21" briefly next to "lazy". |
| 8 | "For now, just remember that the bits have to get from disk to memory." | Hold. The column shows code + static data in sky. |

**Ends with:** CPU, empty bus, disk, memory column with code + static data loaded (sky), step tag "1 / 5".

### S12 — Stack, heap, files, go!   (beats: B08, part 2) · ~1:00
**Purpose:** steps 2–5: stack with argc/argv, heap (malloc/free), three file descriptors, jump to main().
**Starts with:** S11 end state.
**Layout:** same as S11. The memory column fills out from top to bottom: code, static data, heap, (free), stack.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Step two: the **stack**. C programs use it for local variables, function parameters and return addresses." | Tag "2 / 5 · stack". The bottom region of the column fills in sky: "stack". Term highlight "stack". |
| 2 | "…and fills in the arguments to `main()`: `argc` and the `argv` array." | Two small cells slot into the top of the stack: `argc = 2`, `argv → ["./d", "x"]`. |
| 3 | "Step three, maybe: a **heap**. That's for data the program asks for while it runs, with `malloc()`, and gives back with `free()`." | Tag "3 / 5 · heap". A small heap region appears just below static data. Term highlight "heap". A `malloc()` label shoots a block into the heap; `free()` pulls a block out. |
| 4 | "Linked lists, hash tables, trees. It starts small, and the OS can grow it on request." | Tiny node-and-arrow linked-list glyph inside the heap; the heap region grows downward a bit (`stretch`). |
| 5 | "Step four: I/O setup. On UNIX, every process starts with three open **file descriptors**: standard input, standard output, and standard error." | Tag "4 / 5 · I/O". Three small plugs labeled `0 stdin`, `1 stdout`, `2 stderr` attach to the right side of the memory column, each with a cable out to a tiny keyboard icon (stdin) and a terminal icon (stdout/stderr). Term highlight "file descriptors". |
| 6 | "And finally, the OS jumps to the entry point, `main()`, using a special mechanism we'll see soon…" | Tag "5 / 5 · run". A bright arrow jumps from the CPU into the code region and lands on a highlighted line `main()`. "→ Ep. 06" tag beside it. |
| 7 | "…and hands the CPU over to the new process. The performance begins." | The address space (dashed sky outline) "condenses" into a sky Process creature **D** that pops out of the memory column, eyes opening (`blink`), and hops onto the CPU → running. The Computer pops in bottom-center (0, −2.9), scale 0.6, happy. Its LED turns green. |

**Characters:** Computer (happy).
**Ends with:** CPU with D running, memory column (all regions in sky), disk, bus, Computer. Transition to S13: everything except D fades.
**Implementation notes:** the region order top → bottom must match Figure 4.1 (code, static data, heap, …, stack). Use the same `Memory` helper as S09. Keep the stack and heap labels inside their regions, font 20.

### S13 — Running, ready, blocked   (beats: B09) · ~1:20
**Purpose:** the three-state model and its four transitions (scheduled, descheduled, I/O initiate, I/O done).
**Starts with:** D alone at center.
**Layout:** adapt **Figure 4.2**: three state "zones" as large circles, radius 1.1. **Running** at (−3, 1.2) with the CPU chip *inside* it. **Ready** at (3, 1.2), drawn as a small Queue. **Blocked** at (0, −1.6) with a clock. Arrows between zones, curved like the figure.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Once it's alive, a process is always in some **state**. In a simplified view, there are three." | Term highlight "process state". D waits at center while the three circles draw (`Create`), labels `Write`. |
| 2 | "**Running**: it's on a processor, executing instructions." | D hops into Running and onto the CPU inside it → running. The circle glows `CPU_COLOR`. |
| 3 | "**Ready**: it could run right now, but the OS has chosen to run someone else for the moment." | A (coral) and B (mint) appear in the Ready circle (→ ready), bouncing slightly. |
| 4 | "**Blocked**: it did something that means it *can't* run until some event happens." | The Blocked circle pulses. |
| 5 | "The classic example is asking the disk for data and waiting for the answer." | The small Disk icon at (2.4, −2.6), near Blocked. |
| 6 | "Moving from ready to running is being **scheduled**." | D quietly steps off the CPU into Ready (→ ready; the Running → Ready arrow pulses faintly, unlabeled). Then A hops from Ready into Running along the Ready → Running arrow (→ running). Arrow label "scheduled" writes. Term highlight "scheduled". |
| 7 | "Moving from running back to ready is being **descheduled**." | A hops back to Ready along the lower arrow; label "descheduled" writes. Term highlight "descheduled". D is scheduled again → Running. |
| 8 | "A running process that starts an I/O becomes blocked." | D sends a small request packet down to the Disk, then walks along the arrow "I/O: initiate" into Blocked → blocked (clock icon). |
| 9 | "It stays there until the I/O completes." | The disk spins; a progress dot travels back. |
| 10 | "Then it goes back to ready, and maybe straight to running again, if the OS decides so." | The packet returns; label "I/O: done" writes; D walks to Ready → ready. |
| 11 | "Why not just let it keep the CPU while it waits?" | Student (curious). |
| 12 | "Because waiting for a disk takes *ages* in CPU time. The CPU would sit there doing nothing." | Professor (worried). In the Running circle, the CPU chip shows a ghost D sitting idle on it with "zzz", and a tick counter beside it races up "1,000,000 cycles…". Then the ghost fades. |

**Characters:** Student (curious), Professor (worried).
**Ends with:** the complete state diagram with labels, D in Ready, A in Running (put A on the CPU at the end), B in Ready.
**Implementation notes:** step 6 needs a clean ordering. Before A is scheduled, D must leave the CPU. Do it as one choreographed swap: D → Ready (descheduled arrow pulses faintly), A → Running (scheduled arrow labeled). Then in step 7 reverse it, which labels "descheduled". The point is to show both arrow labels clearly, one at a time.

### S14 — Trace 1: CPU only   (beats: B10) · ~0:40
**Purpose:** reading a state trace: two CPU-only processes, 8 ticks, CPU always busy.
**Starts with:** the S13 state diagram.
**Layout:** the state diagram shrinks to the top-right (4.4, 2.0) at scale 0.45 as a "legend" and stays live. Main stage: CPU at (−3.2, 1.0) with P0 / P1 beside it. **Timeline** along y = −1.2 (row P0) and y = −1.8 (row P1), ticks 1..8 at x = −4.5..3.5, tick labels below at y = −2.4.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Let's watch two processes, zero and one, each needing just four ticks of CPU and no I/O." | D, A and B fade out of the legend. **P0** (coral) and **P1** (mint) appear next to the CPU; each holds a small "work: ▮▮▮▮" bar (4 cells). The empty timeline grid draws, with row labels "P0" and "P1". The legend now holds mini P0/P1 dots that track their state. |
| 2 | "Process zero runs for four ticks while process one waits, ready." | P0 on the CPU → running; P1 ready. Ticks 1–4 fill one by one (0.5 s each): row P0 running (solid coral), row P1 ready (mint outline). P0's work bar empties a cell per tick. |
| 3 | "At tick four, process zero is done." | P0 → done (check mark) and fades to half opacity at the side. Its row ends. |
| 4 | "Process one runs for ticks five to eight." | P1 hops onto the CPU; ticks 5–8 fill (row P1 solid). Tick 8: P1 → done. |
| 5 | "Eight ticks of work, eight ticks of time. The CPU never idled." | A row "CPU" under the timeline fills with 8 yellow cells; the label "CPU busy: 8 / 8" (in `CPU_COLOR`) appears. Hold 1 s. |

**Ends with:** completed 8-tick timeline + legend. Transition: the timeline clears (the blocks fade), and P0 and P1 reset to ready beside the CPU.
**Implementation notes:** build a reusable `Timeline(rows, ticks)` helper with `.fill(row, tick, state)` returning an animation. The book's Figure 4.3 is the source table; match it exactly.

### S15 — Trace 2, the bad way: just wait   (beats: B11, first part) · ~0:30
**Purpose:** show that waiting for I/O wastes the CPU (the counterfactual).
**Starts with:** S14 end (empty timeline, P0/P1 ready, legend). The timeline now has 10 ticks (it extends right), and a Disk appears at (−3.2, −0.2) under the CPU, close by.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Now make it interesting. Process zero runs for three ticks, then asks the disk for something." | The timeline extends to ticks 1..10 (it rescales to fit x −4.5..4.5). P0's work bar now reads "▮▮▮ · I/O · ▮▮". P0 runs ticks 1–3 (solid coral). At the end of tick 3 a request packet drops from P0 to the Disk. |
| 2 | "The I/O will take a few ticks." | A small "I/O: 3 ticks" tag by the Disk; the disk spins. |
| 3 | "So… we just wait?" | Student (curious). A translucent "WHAT IF" banner in the top-left area of the stage. |
| 4 | "We could. Watch what happens if we do: three ticks where the CPU does nothing." | Ticks 4–6: P0 row blocked (grey + clock), P1 still ready, CPU row idle (hatched grey ×3). |
| 5 | (Computer snores) | The Computer pops up at (5.2, −2.9) scale 0.6 → sleeping (zZz). |
| 6 | (rewind) | All of ticks 4–6 animate in reverse (blocks shrink away right to left, 0.8 s); the "WHAT IF" banner fades; the Computer → idle. |

**Characters:** Student (curious), Computer (sleeping → idle).
**Ends with:** timeline with ticks 1–3 filled (P0 running, P1 ready), P0 just issued its I/O, Disk spinning.

### S16 — Trace 2, the OS way   (beats: B11, rest) · ~1:10
**Purpose:** overlap I/O with computation (book Figure 4.4), and see the two scheduler decisions.
**Starts with:** S15 end state.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Instead, the OS notices that process zero is blocked and isn't using the CPU, so it runs process one." | P0 walks off the CPU to a spot next to the Disk → blocked (clock). The legend's P0 dot moves to Blocked. P1 hops onto the CPU → running. |
| 2 | "Ticks four, five and six: process one runs while zero waits on the disk." | Ticks 4–6 fill: P0 blocked (grey + clock), P1 running (mint solid), CPU row busy (yellow). |
| 3 | "At tick seven the I/O completes, and process zero moves to ready." | The packet returns to P0; P0 → ready (legend dot moves Blocked → Ready). Tick 7: P0 ready (coral outline), P1 running. |
| 4 | "Process one finishes at tick eight." | Tick 8: P1 running, then P1 → done. |
| 5 | "Then process zero runs ticks nine and ten, and is done." | P0 hops onto the CPU; ticks 9–10 P0 running; P0 → done. CPU row: 10 / 10 busy. The Computer (busy, LED amber) bounces happily. |
| 6 | "Notice that the OS just made two decisions." | The timeline dims except tick boundaries 3|4 and 7|8. |
| 7 | "First, it switched to process one during the I/O. That's clearly good: it kept the CPU busy." | A marker "①" at the 3|4 boundary; a green check; the CPU row's ticks 4–6 glow yellow. |
| 8 | "Second, when the I/O finished, it did *not* switch back to process zero right away." | Marker "②" at the 7|8 boundary with a big "?" in `TEXT`. |
| 9 | "It let process one finish first. Was that a good choice?" | An alternative ghost timeline briefly overlays ticks 7–10 (P0 running at 7–8, P1 at 9–10) in translucent colors, then fades, which shows that the other choice was possible. |
| 10 | "Uh… depends?" | Student (confused). |
| 11 | "That's the right answer more often than you'd think. Decisions like these are made by the OS's **scheduler**…" | Professor (happy). Term highlight "scheduler". A small figure (a referee's whistle or a conductor's baton icon) appears next to the CPU, labeled "scheduler". |
| 12 | "…and we'll spend several episodes on them." | A tag "→ Ep. 07–10" on the scheduler icon. |

**Characters:** Computer (busy), Student (confused), Professor (happy).
**Ends with:** completed 10-tick timeline + legend + scheduler icon. Transition: everything fades except the legend state diagram, which moves back to center-small.
**Implementation notes:** source is Figure 4.4; the timeline must match exactly (P0: R R R B B B Rdy Rdy R R; P1: Rdy Rdy Rdy R R R R R – –).

### S17 — The process list   (beats: B12, part 1) · ~0:35
**Purpose:** the OS tracks every process with a PCB; together they form the process list.
**Starts with:** the small state diagram at center.
**Layout:** state diagram at the left (−3.6, 0.4) at scale 0.7, with A, B, C, D placed in the zones (A running, B and D ready, C blocked). Process list at the right: a vertical stack of 4 PCB cards at x = 3.6, y = 2.0, 0.8, −0.4, −1.6 (each 3.6 × 1.0).

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "One last question. How does the OS *remember* all this? It's a program too, and like any program, it keeps data structures." | The state diagram fills with A, B, C, D. A thin outline labeled "OS" (in `KERNEL_COLOR`) draws around the right half of the screen, empty for now. |
| 2 | "For each process, it keeps a record. That record is called a **Process Control Block**, or **PCB**…" | A's PCB card slides out of A into the OS area: header color = coral, fields "pid: 1 · state: running · memory: … · files: …". Term highlight "Process Control Block (PCB)". |
| 3 | "(sometimes a process descriptor)" | A small `DIM` alias label under the term. |
| 4 | "All of those records together form the **process list**, also called the task list." | Cards for B, D (ready) and C (blocked) slide out in turn and stack. A bracket labeled "process list". Term highlight "process list". |
| 5 | "…who's ready, who's running, who's blocked and waiting on what…" | Each card's "state" field `Indicate`s as it's mentioned. C's card shows "waiting on: disk". |
| 6 | "…so the right one can be woken when its I/O completes." | A packet arrives from a small disk icon; the OS looks up C's card (it highlights), C moves Blocked → Ready in the diagram, and the card's state field changes "blocked" → "ready" (`Transform` the text). |

**Ends with:** state diagram + 4 PCB cards in the OS area.

### S18 — Inside a real PCB: xv6   (beats: B12, part 2) · ~0:35
**Purpose:** a real PCB (xv6 `struct proc`); the register context is the "save slot".
**Starts with:** S17 end state.
**Layout:** A's card zooms to the center and becomes a **Code block** (C, monokai, font 20, about 11 lines) at (−0.8, 0.2). Labels fly in at the right.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Here's a real one, from a small teaching operating system called xv6." | The other cards and the diagram fade to 20%. A's card expands and `Transform`s into the Code block (adapted from Figure 4.5, trimmed): `struct proc {` / `char *mem;` / `uint sz;` / `enum proc_state state;` / `int pid;` / `struct proc *parent;` / `struct file *ofile[NOFILE];` / `struct context context;` / `...` / `};`. Caption "xv6 (Figure 4.5, simplified)". |
| 2 | "Each process has an ID, a state, a pointer to its memory, its open files, its parent." | Highlight bars move line by line: `pid`, `state`, `mem`, `ofile`, `parent` (0.5 s each). |
| 3 | "And look at this field: the **register context**." | The `context` line highlights in yellow. Term highlight "register context". |
| 4 | "When a process is stopped, its registers get saved right here." | The docked "SAVE SLOT" icon from S09 flies down from the top-right corner and lands on the `context` line. A small register grid (from S09) appears next to it, and values stream from it into the save slot. |
| 5 | "To resume it, the OS loads them back into the real CPU." | A CPU chip appears at the right (4.4, 0.2); the values stream from the save slot into the CPU. |
| 6 | "That's the video-game save slot!" | Student (excited). |
| 7 | "That's the one. Restoring it is the context switch." | Professor (proud). Tag "context switch → Ep. 06". |

**Ends with:** Code block with `context` highlighted, CPU at the right, save slot gone (merged into the code line).

### S19 — Zombies and parents   (beats: B12, part 3) · ~0:40
**Purpose:** more states (initial, final/zombie); the parent reads the return code with `wait()`.
**Starts with:** S18 end state.
**Layout:** the code block shrinks to the top-left (−4.2, 1.8), scale 0.6, showing only `enum proc_state { UNUSED, EMBRYO, SLEEPING, RUNNABLE, RUNNING, ZOMBIE };`. Main stage: a parent process at (−1.5, −0.6), a child at (1.5, −0.6).

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Real systems also have a couple more states." | The code block swaps to the `enum proc_state` line (Transform). `EMBRYO` and `ZOMBIE` glow. |
| 2 | "There's an **initial** state while a process is being created." | Term highlight "initial". A child process (sky) assembles from fragments at (1.5, −0.6), still translucent (EMBRYO). |
| 3 | "And there's a **final** state, where a process has exited but hasn't been cleaned up yet. On UNIX that's called the **zombie** state." | The child → done briefly, then droops into zombie (grey, stitches). Term highlight "zombie". |
| 4 | "It sounds spooky, but it's useful. It lets the process's **parent**, the process that created it…" | A coral parent process appears at (−1.5, −0.6). A thin line labeled "parent" connects them. Term highlight "parent". |
| 5 | "…check its return code. Zero usually means success, anything else means something went wrong." | A tag hangs from the zombie: "exit code: 0 ✓" (green). Briefly, an alternative "1 ✗" flips in (red), then back to "0 ✓". |
| 6 | "The parent calls `wait()`, reads the result, and the OS cleans up." | The parent shows a speech bubble "wait()". The tag flies to the parent. The zombie fades away (`FadeOut` + shrink) and its PCB card (if visible in the dimmed list) is removed. |
| 7 | "Zombies. In my operating system." | Student (surprised). |
| 8 | "Relatively easy to kill, too. Different techniques are recommended, though." | Professor (happy). Hold 0.8 s for the joke. |

**Ends with:** the parent alone + code block. Transition: everything fades.

### S20 — Back to the illusion   (beats: B13) · ~0:40
**Purpose:** assemble the whole episode into one picture: the illusion explained.
**Starts with:** empty (section badge only).
**Layout:** the S01 laptop outline at center, scale 1.2, made translucent so its inside is visible. Inside: the CPU at (0, 0.6), a ready Queue at (−2, −0.8), a blocked spot with a disk at (2, −0.8), a mini process list at the right (5, 0.5), and a mini timeline at y = −2.4.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Let's go back to that laptop with a hundred programs and one CPU." | The laptop draws back in with the "programs: 137 · CPUs: 1" counters from S01/S02. |
| 2 | "Now we can see the trick." | The laptop body becomes translucent (stroke only, fill opacity 0.1). |
| 3 | "Each program is a process: memory, registers, open files, written down in a PCB." | Processes A, B, C, D appear inside; each spawns a mini PCB card that flies to the process list. |
| 4 | "The OS keeps them all on a list." | The list brackets. |
| 5 | "It hands the CPU to one, then another, quickly, sliding each between running, ready and blocked." | A short loop (~4 s): processes cycle on and off the CPU, one goes blocked at the disk and comes back; the mini timeline fills with colored slices; PCB state fields update in sync. |
| 6 | "A low-level mechanism does the switching. A policy decides who goes next." | The gear icon (mechanism, S08) appears by the CPU; the spotlight (policy, S08) appears above the queue. |
| 7 | "Many virtual CPUs. One real one." | The five shimmering virtual CPUs from S02 fade in along the top. Then they slide down and **merge** into the one real CPU (`Transform` all five into the chip). The chip flashes once. Hold 1.5 s. |

**Ends with:** the laptop world, one CPU glowing.

### S21 — Recap   (beats: B14) · ~0:35
**Purpose:** five takeaways.
**Starts with:** S20 end state.
**Layout:** the world fades; a numbered list at the left (−5.6 .. 1), font 30, one line each; an icon for each line at x = 4.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "So, today:" | The laptop world `FadeOut`; the header "Recap" in `VIRT`. |
| 2 | "A **process** is a running program…" | Line 1 writes; icon: file → process creature (mini replay). |
| 3 | "**Time sharing** the CPU creates the illusion of many CPUs, at the cost of performance." | Line 2; icon: a mini timeline with alternating slices. |
| 4 | "Mechanisms answer *how*; policies answer *which*." | Line 3; icon: gear + spotlight. |
| 5 | "A process is its machine state: address space, registers, open files." | Line 4; icon: the save slot. |
| 6 | "Processes move between **running**, **ready** and **blocked**, and the OS tracks them all in the **process list**." | Line 5; icon: the mini state diagram + a PCB card. Hold 1.5 s. |

**Ends with:** the full recap list. Section badge fades out.

### S22 — Teaser: a process that clones itself   (beats: B15) · ~0:25
**Purpose:** hook for 05 (Process API).
**Starts with:** S21 end state.
**Layout:** characters in dialogue mode. A single process at center (0, 1.2).

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Okay, I'm convinced processes exist. But how do I actually *make* one? From my own code?" | The recap list fades. The Student and Professor move to dialogue positions. Student (curious). A coral process appears at center (0, 1.2). |
| 2 | "With three of the strangest and most elegant calls in computing: `fork()`, `exec()` and `wait()`." | Professor (happy). The three call names appear above the process one by one, in monospace, in `TEXT`. |
| 3 | "A process that clones itself…" | The process splits into two identical copies (copy + shift apart with a stretchy "mitosis" squash), both coral and blinking in sync. Student → surprised. |
| 4 | "Next time." | Cut to black (FadeOut all, 0.5 s). Then "Next: 05 · The Process API" in `TEXT` with a `VIRT` dot. Hold 2 s. |

**Characters:** Student (curious → surprised), Professor (happy).
**Ends with:** black end card.

## New assets needed
Nothing below exists in `ostep_lib` yet. Build these as reusable props in an `ostep_lib/props/`
module; most will be reused across the Virtualization section.

- **`CPU`**: yellow rounded square chip with pins on four sides and an optional label; a `.slot_point()` helper gives the point where a running process stands.
- **`Memory(regions=[...])`**: tall column of stacked cells with addresses on the left; named regions (code, static data, heap, free, stack) that can be filled with a color; `.region(name)` access; works empty too.
- **`Disk`**: green cylinder (angled ellipse top); optional "spin" animation (a rotating stripe on the top ellipse).
- **`Bus`**: horizontal line with arrow ends plus a vertical stub; `.path(from, to)` for moving data along it.
- **`Timeline(rows, ticks)`**: Gantt grid with row labels and tick labels; `.fill(row, tick, state, color)` returns an animation using the state encoding table; `.extend(ticks)` rescales; also a CPU-utilization row.
- **`Queue(processes, label)`**: arranges processes in a row with a label underneath; `.push()` / `.pop()` animations.
- **`StateDiagram`**: the three-state diagram (Figure 4.2) with labeled curved arrows, zones that processes can be placed into, and a `.scale_to_legend()` preset. Mini state-tracking dots for the legend mode.
- **`CruxCard(question, subtitle, accent)`**, **`TipCard(title, body)`** / `AsideCard`, **`TermHighlight`** (write-big-then-dock behaviour), **`SectionBadge(number, title, accent)`**: the bible's cards, as described there.
- **`IllusionSplit(left_title, right_title)`**: divider + two titles; `.merge()` animation for S20.
- **`PCBCard(process, fields)`**: small card with a process-color header and updatable fields.
- **`RegisterBank(names)`**: grid of labeled register boxes with values; highlight single registers.
- **`hop_to(process, point)` animation**: arc path with squash-and-stretch. It is used constantly.
- **Icons:** laptop, browser, music note, chat bubble, game pad, envelope, file (with folded corner), sheet music, gear pair, spotlight, clipboard / save slot, menu card, keyboard, terminal, peach (callback), scheduler/whistle, pause/play glyphs, clock. All are simple primitives.
- **Process extras:** a "frozen" overlay (desaturate + ⏸) for S09/S10, an "embryo" translucent look for S19 (it can be just opacity 0.4 on `Process("ready")`), and a split/clone helper for S22.
- **Style:** move the label `FONT` from `characters/base.py` into `style.py` (noted earlier) so props and characters share it.

## Open questions
- **Process naming:** the traces use **P0/P1** (the book's names) in coral/mint, which reuses A/B's colors. Should they just be A and B instead, so names never change within the episode?
- **S05 chip grid:** the "40 chips" visual gag might read as busy. Is it OK, or should it just be a few chips plus a "×1000" counter?
- **S08 robotic arm and spotlight:** these are my visual metaphors for mechanism and policy. Keep them as the series' recurring icons for those two words? (If yes, add them to the bible's props table.)
- **Timeline encoding** (solid = running, outline = ready, grey + clock = blocked, hatched = idle): should this become a series standard in the bible now? It will matter in every scheduling episode.
- **xv6 code (S18):** it's trimmed to ~9 fields from Figure 4.5. Is that the right level of detail, or should we show the full struct briefly?
- **Scene granularity:** 22 scenes, each intended as one Manim `Scene` class, rendered separately and joined in editing. Or would you rather have fewer, longer classes?
