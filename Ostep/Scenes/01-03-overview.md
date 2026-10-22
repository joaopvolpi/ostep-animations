# 01–03 — Overview: What Is an Operating System? · Scene breakdown
> Script: Ostep/Scripts/01-03-overview.md · Scenes: 24 · Est. duration: ~14:00

## Visual overview
- **Core metaphor: the system stack.** It's built in S05: hardware at the bottom (CPU, Memory,
  Disk), the OS as a band in the middle, programs (Process creatures) on top. It returns in every
  piece of the episode: the demos zoom into one part of the hardware row, and the map (S23) is
  that same stack with the three pieces attached to it.
- **Signature motif: the peach → Illusion split.** One physical thing, many virtual copies.
  The peach (S07–S08) is the cartoon version. The `cpu` (S10) and `mem` (S12) demos are the same
  picture with real hardware. Episode 04 calls back to the peach on its CPU, so the peach design
  must stay identical.
- **Each of the three pieces gets a four-part rhythm:** (1) run a tiny program from the book in a
  terminal, (2) a surprising output, (3) what's really happening, drawn as the mechanism moving,
  (4) its crux card. Viewers learn the pattern and anticipate the reveal.
- **Section accent switches per piece:** neutral `INTRO` for S01–S06 and S18–S24, `VIRT` orange
  for S07–S12, `CONC` cyan for S13–S14, `PERS` green for S15–S17. The section badge's dot and the
  term-highlight underline follow it.
- Props used (from the bible): Crux card, Aside/Tip card, Term highlight, Section badge, CPU, Memory,
  Disk, Timeline, User/Kernel boundary, Illusion split, Code block. Characters: Professor, Student,
  Computer, Process.

### Persistent assignments
| Thing | Look | Notes |
|---|---|---|
| Process **A / B / C / D** (`cpu` demo, S10) | `PROCESS_COLORS[0..3]`: coral, mint, gold, sky; labels "A"…"D" | **Same as episode 04**, so the callback in 04's S03 matches. |
| Peach eaters (S07–S08) | Four Processes in the same four colors, no labels | Foreshadows A–D. |
| `mem` processes (S11–S12) | PID 24113 = `PROCESS_COLORS[4]` (lilac), PID 24114 = `PROCESS_COLORS[5]` (pink); labels "PID 24113", "PID 24114" (font 18) | |
| Threads T1 / T2 (S13–S14) | `Process(...)` scaled ×0.65, colors `PROCESS_COLORS[1]` / `PROCESS_COLORS[3]`, labels "T1", "T2" | A stand-in until a Thread character exists (see Open questions). |
| The peach | Circle r = 0.55, fill `#FFB07A`, a darker `#F88017` crease arc, small green leaf (two arcs, `PERS`) | Reused in episode 04's S06. Define it once in `ostep_lib/props`. |
| CPU home | `CPU_COLOR` chip 1.4 × 1.4 at **(0, 0.6)** in "world" scenes | Same as 04. |
| Characters (corner mode) | Student (−5.8, −2.8), scale 0.75, facing right · Professor (5.8, −2.8), scale 0.75, `flip()` | Same as 04. **Dialogue mode:** Student (−2.6, −1.2), Professor (2.6, −1.2), scale 1. |
| Section badge | Top-left (−6.6, 3.6): accent dot + "01–03 · Overview", font 22, `DIM` | The dot color follows the current section accent. Appears in S04. |
| Term highlight | Same as 04: written at (0, 2.9) font 54, accent underline, then docks at top-right (6.6, 3.6) font 26 | |
| Terminal | Rounded rect, fill `#111111`, `DIM` stroke, monospace text, `TEXT` output and `DIM` prompt; standard size 5.6 × 3.6 | New asset; also used in 05. |
| System stack | Hardware row y = −2.3 (CPU at −3, Memory at 0, Disk at 3, each scale 0.6); OS band y = −0.9, 10 × 0.8, `KERNEL_COLOR` fill 0.25 + stroke, label "Operating System"; programs row y = 0.8 | New recurring prop; S05, S06, S17, S23. |

## Scenes

### S01 — Welcome   (beats: B01, lines 1–2) · ~0:20
**Purpose:** meet the two hosts; set the tone.
**Starts with:** empty (BG).
**Layout:** dialogue mode. Title at (0, 2.6).

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Welcome! This is a series about operating systems…" | Professor walks in from the right to (2.6, −1.2) (happy) and waves (small rotate wiggle). |
| 2 | "…based on a book called *Operating Systems: Three Easy Pieces*." | Title `Write`s at (0, 2.6), font 44: "Operating Systems: Three Easy Pieces". Under it, `DIM` font 22: "Remzi H. Arpaci-Dusseau & Andrea C. Arpaci-Dusseau · free at ostep.org". |
| 3 | "I'm called 'Professor'. Who are you?" | A name tag "Professor" pops on the Professor's bow tie for 1.5 s. Professor `look_at` the left edge. |
| 4 | "Hi, Professor! I'm called 'Student', as you might have guessed. And I'm ready to learn!" | Student bounces in from the left to (−2.6, −1.2) (excited). Name tag "Student". The two look at each other. |

**Characters:** Professor (happy), Student (excited).
**Ends with:** title + credit line, both characters in dialogue mode.

### S02 — Three easy pieces   (beats: B01, lines 3–9) · ~0:50
**Purpose:** introduce the three ideas and their colors.
**Starts with:** S01 end state.
**Layout:** the title shrinks to (0, 3.3) at font 28. Three piece cards in a row at y = 1.0 (x = −4, 0, 4), each 3.2 × 1.6, rounded, filled at 0.15 with their accent and stroked in the accent.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "First question: why *three easy pieces*?" | Student (curious). The words "Three Easy Pieces" in the title `Indicate`. |
| 2 | "Richard Feynman gave famous lectures on physics…" | Professor (explaining). A book silhouette appears at (−1.2, 1.2) labeled "Six Easy Pieces · Feynman" (font 24). |
| 3 | "We're doing three easy pieces on operating systems." | The "Six" book slides left and fades to 40%; a second book "Three Easy Pieces · OS" appears beside it. |
| 4 | "Which is fitting, since operating systems are about half as hard as physics." | A tiny equation writes between them: `MathTex` "\frac{6}{2} = 3", font 36. Hold 1 s for the joke. Both books fade. |
| 5 | "So what are the pieces?" | Student (curious). |
| 6 | "**Virtualization**." | Card 1 (x = −4) `GrowFromCenter` in `VIRT`, label "Virtualization". |
| 7 | "**Concurrency**." | Card 2 in `CONC`, "Concurrency". |
| 8 | "**Persistence**." | Card 3 in `PERS`, "Persistence". Professor (proud). |
| 9 | "How it decides what program runs next on a CPU." | A mini CPU icon with a hopping process pops into card 1. |
| 10 | "How it copes when memory overflows." | A mini Memory column overflowing (cells spill over the top) also pops into card 1. |
| 11 | "How it stores information on disks." | A mini Disk pops into card 3. |
| 12 | "Even how to build systems that keep working when parts of them fail." | Below the cards (0, −0.4): three small networked boxes, one turns red with an ✕, and the others keep blinking green. Tag "+ distributed systems" in `DIM`. |
| 13 | "I have no idea what you're talking about, really." | Student (confused). A "?" sits over the cards. |
| 14 | "Good! That means you're in the right place." | Professor (happy). The "?" pops. |

**Ends with:** title (small), three piece cards with their mini icons, characters in dialogue mode.
**Implementation notes:** these three cards are the same objects shown again in S23 (map) and S24. Build them in `common.py`.

### S03 — I hear, I see, I do   (beats: B01, lines 10–15) · ~0:35
**Purpose:** the series motto; the Student surprises the Professor.
**Starts with:** S02 end state.
**Layout:** the three cards shrink to a strip at y = 3.0 (scale 0.45). Three words centered at y = 1.0.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "And what's the best way to learn this stuff?" | Student (curious). The cards shrink to the top strip. |
| 2 | "Watch, think, and then *do*. Write real code that solves real problems." | Professor (explaining). A tiny code-editor glyph with a blinking cursor appears at (0, 1.0), then fades. |
| 3 | "As Confucius said…" | Professor `says` "As Confucius said…" (speech bubble). |
| 4 | "'I hear and I forget.'" | Student (excited) cuts in. Center: "I hear → I forget" writes, `DIM`. |
| 5 | "'I see and I remember.'" | "I see → I remember" writes under it, in `TEXT`, and **glows** (it's what this series is). |
| 6 | "'I do and I understand.' Or something like that." | "I do → I understand" writes under that, in `TEXT`. |
| 7 | "How did you know what I was going to say?!" | Professor (surprised). The Professor's bubble pops away. |
| 8 | "It seemed to follow. Also, the philosopher Xunzi is actually a better source for that quote." | Student (neutral). A small footnote tag slides in under the three lines: "attributed to Confucius; closer to Xunzi" (font 20, `DIM`). |
| 9 | "Well. I think we're going to get along just fine." | Professor (happy). Hold 1 s. |

**Ends with:** the card strip at the top, the three motto lines, characters in dialogue mode.

### S04 — Fetch, decode, execute   (beats: B02) · ~0:50
**Purpose:** what a running program does: the Von Neumann loop.
**Starts with:** S03 end state.
**Layout:** CPU at (−2.8, 0.4), 1.6 × 1.6. Memory column at (2.8, 0.4), 1.4 × 4.4, with 8 instruction cells (`add r1, r2`, `load r3, [x]`, `cmp r3, 0`, `jmp f`, …, font 18 monospace). A three-stage ring under the CPU at (−2.8, −1.8): FETCH → DECODE → EXECUTE.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Let's start at the bottom. What happens when a program runs?" | The motto and card strip fade. Characters glide to corner mode. The section badge appears (INTRO dot). The CPU and the Memory column `Create`. |
| 2 | "The processor **fetches** an instruction from memory." | Term highlight "fetch". The PC arrow (yellow, left of the memory column) points at cell 1; the cell's text copies and flies along a line into the CPU. Ring stage FETCH lights. |
| 3 | "It **decodes** it, figuring out which instruction this is." | Inside the CPU the copied text resolves into a label "ADD". Stage DECODE lights. Term "decode". |
| 4 | "Then it **executes** it: add two numbers, access memory, check a condition, jump to a function." | Stage EXECUTE lights; inside the CPU, a tiny "2 + 3 → 5" flashes. Term "execute". |
| 5 | "Then it moves on to the next instruction. And the next." | The PC arrow steps down to cell 2, then cell 3; the full ring cycles each time (0.8 s per cycle). |
| 6 | "Millions, these days *billions*, of times per second…" | The cycle accelerates to a blur; a counter beside the CPU, "instructions/s", rolls to "3,000,000,000". |
| 7 | "…until the program finishes." | The PC reaches the last cell `ret`; the cycle stops. Hold 0.5 s. |
| 8 | "That's the **Von Neumann** model of computing." | Term highlight "Von Neumann model". |
| 9 | "Modern processors play some wild tricks under the hood… but they keep up the appearance of exactly this: one instruction at a time, in order." | For 1.5 s the CPU interior shows chaos (several instructions flying in parallel, out of order, as small colored dashes). A "curtain" rectangle slides over it, painted with the neat single-step ring. Caption on the curtain: "the appearance: one at a time, in order". |
| 10 | "Sounds simple." | Student (bored). |
| 11 | "It is. Until you want to run *more than one* of them." | Professor (thinking). Next to the Memory column, a second and a third program's instruction lists slide in, all aiming at the one CPU. Hold 0.8 s. |

**Characters:** corner mode; Student (bored), Professor (thinking).
**Ends with:** CPU, memory column, 3 instruction lists, section badge.
**Implementation notes:** the instruction text is pseudo-assembly, not a real ISA. Keep it short.

### S05 — Enter the operating system   (beats: B03, paragraphs 1–2) · ~0:45
**Purpose:** introduce the OS as the software layer between programs and hardware; virtualization: physical → virtual.
**Starts with:** S04 end state.
**Layout:** the **System stack** (see the assignments table).

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "While a program runs, a lot of other things are going on, all with one goal: making the system **easy to use**." | The CPU and Memory column shrink and move into the hardware row (CPU at (−3, −2.3), Memory at (0, −2.3)); a Disk rises in at (3, −2.3). The three instruction lists turn into three Process creatures (A, B, C colors) in the programs row (x = −3, 0, 3; y = 0.8). Term highlight "easy to use" (no dock, just fades). |
| 2 | "It lets you run programs, even many at once." | The processes bounce once each. |
| 3 | "It lets programs share memory and talk to devices." | Short dashed lines from processes down to Memory and Disk, tangled and crossing. |
| 4 | "That software is the **operating system**, or **OS**." | The OS band slides in between the rows (y = −0.9) and **untangles** the lines: each line now goes process → OS band → hardware. Label "Operating System" on the band. Term highlight "operating system (OS)". |
| 5 | "Its main technique is called **virtualization**." | Term highlight "virtualization". |
| 6 | "The OS takes a *physical* resource, like the processor, memory or a disk…" | The CPU in the hardware row gets a tag "physical" and is copied: the copy travels up through the OS band… |
| 7 | "…and transforms it into a more general, more powerful, easier-to-use *virtual* form of itself." | …and emerges above the band as three translucent, glowing CPUs, one per process (tag "virtual"). The same happens quickly for Memory (three translucent memory columns). |
| 8 | "That's why the OS is sometimes called a **virtual machine**." | The band's label crossfades to "Operating System · a virtual machine" for 2 s, then back. Term highlight "virtual machine". |

**Ends with:** the system stack with the virtual CPUs and memories above the band.
**Implementation notes:** keep the hardware row small (scale 0.6) to leave room; translucency = fill opacity 0.25, stroke opacity 0.6.

### S06 — The crux, the API, the manager   (beats: B03, crux + paragraphs 3–5) · ~0:45
**Purpose:** the first crux; system calls (standard library); resource manager.
**Starts with:** S05 end state.
**Layout:** Crux card overlays the center (0, 0.8), then shrinks. The system stack stays underneath.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | (crux appears) | The virtual copies fade. Crux card (INTRO frame): **"How to virtualize resources?"**, subtitle (`DIM`, font 24): "What mechanisms and policies? How, efficiently? What hardware support?" `Write`. Hold 2 s, then it docks as a strip at (0, 3.2). |
| 2 | "…the OS offers a few hundred **system calls**." | Small doorways (rounded notches) appear along the top edge of the OS band, labeled `run`, `malloc`, `open`. A process sends a request arrow into a door. Term highlight "system calls". |
| 3 | "We sometimes say it provides a **standard library** to applications." | The band's label briefly reads "a standard library". Term (smaller). |
| 4 | "…the OS is also a **resource manager**. It hands those resources out efficiently and fairly." | The band's label → "a resource manager". Small hands reach up from the band to hand a CPU token to one process, then another, alternating. Term highlight "resource manager". |
| 5 | "Fun fact: early names for the OS were 'the supervisor' and even 'the master control program'." | Professor (explaining). Two name tags flutter onto the band: "the supervisor" (stays a second), then "MASTER CONTROL PROGRAM" in a menacing red glowing font that makes the band glow red. |
| 6 | "The second one sounded a little overzealous, so 'operating system' won." | The menacing tag gets stamped ✕ and falls off; the band returns to normal "Operating System". Student (excited) laughs. |

**Characters:** Professor (explaining), Student (excited).
**Ends with:** the system stack (no virtual copies), the crux strip at the top.

### S07 — The peach   (beats: B04, lines 1–5) · ~0:40
**Purpose:** physical vs virtual, in cartoon form.
**Starts with:** S06 end state.
**Layout:** dialogue mode again (it is a dialogue). A table line at y = −0.2 from x = −4 to 4. The peach at center (0, 0.4). Four eaters along the table: x = −3.6, −1.2, 1.2, 3.6, y = 0.4.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "But what *is* virtualization, oh noble Professor?" | The system stack and the crux strip fade. Characters → dialogue mode. Section badge dot → `VIRT`. Student (curious). |
| 2 | "Imagine we have a peach." | Professor (explaining). The peach drops in at (0, 0.4) with a small bounce. |
| 3 | "A peach?" | Student (confused). A "?" over the Student. |
| 4 | "Call it the **physical** peach." | A tag "physical" under the peach, `TEXT`. Term highlight "physical". |
| 5 | "Now, many eaters would like to eat this peach." | Four eater Processes hop in along the table (coral, mint, gold, sky), all looking at the peach (`look_at`). |
| 6 | "What we'd like is to give each of them their *own* peach, so they're all happy." | Each eater gets a translucent peach copy in front of it (copy of the peach, fill opacity 0.35, dashed outline). The eaters → ready (eager). |
| 7 | "These are **virtual** peaches." | Tag "virtual" under each copy. Term highlight "virtual". |
| 8 | "The important part is the illusion: to each eater, it looks like they have a real peach of their own." | A cone of view from each eater's eyes to its own copy. The real peach in the center dims to 50%. |

**Characters:** Student (curious → confused), Professor (explaining); 4 eater Processes.
**Ends with:** 4 eaters, each with a virtual peach, the dim real peach at center.

### S08 — Snatch the peach   (beats: B04, lines 6–11) · ~0:45
**Purpose:** the trick: give the real resource to whoever is using it, while others nap. This is time sharing in disguise.
**Starts with:** S07 end state.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "So you're sharing the peach, and they don't even know it?" | Student (curious). |
| 2 | "Exactly." | Professor (happy). |
| 3 | "But there's only one peach. If I were sharing a peach, I think I'd notice." | Student (frustrated). The virtual peaches flicker ("is it real?"). |
| 4 | "Ah, but most of the time eaters are napping, or doing something else." | Three eaters → blocked (eyes closed + clock, used here as "napping"); one (coral) stays ready. |
| 5 | "So you snatch the peach away and give it to someone else for a while." | The real peach (full opacity) slides along an arc to the coral eater, which takes a bite → running. Coral → blocked (naps); the gold one wakes → ready; the peach hops to gold. Repeat for mint and sky. Speed up for 3 more hops. |
| 6 | "And so we create the illusion of many virtual peaches: one for each person!" | Professor (proud). Pull back: a dashed **Illusion split** divider draws through the middle. Left half, titled "what each eater sees": four eaters, each with its own steady peach. Right half, titled "what really happens": one peach hopping. |
| 7 | "Sounds like a bad campaign slogan." | Student (bored). A campaign-poster frame briefly appears around "A PEACH FOR EVERY PERSON!" over the left half, then fades. |
| 8 | "You're talking about computers, right?" | — |
| 9 | "Right. Let's take a real one." | Professor (happy). On the right half, the hopping peach **morphs into a CPU chip**; the eaters morph into labeled processes A, B, C, D. Hold 1 s. |

**Characters:** Student (curious → frustrated → bored), Professor (happy → proud → happy).
**Ends with:** the illusion split. Right: one CPU + A–D. Left: four eaters with peaches (to be replaced).
**Implementation notes:** the hop is the same `hop_to` arc helper as episode 04 (applied to the peach). The "napping" here reuses the Process `blocked` expression.

### S09 — A tiny program: `cpu`   (beats: B05, lines 1–2) · ~0:30
**Purpose:** set up the first real demo.
**Starts with:** S08 end state.
**Layout:** Code block at left (−3.4, 0.6), font 20; Terminal at right (3.2, 0.4), 5.6 × 3.6.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Here's a tiny program called `cpu`." | The illusion split fades out entirely. A Code block (from **Figure 2.1**, trimmed to lines 14–18) writes: `char *str = argv[1];` / `while (1) {` / `    Spin(1);` / `    printf("%s\n", str);` / `}`. Title above it: `cpu.c`. Characters → corner mode. |
| 2 | "All it does is wait for one second, print the word you gave it, and repeat. Forever." | A highlight bar steps: `Spin(1)` (a small 1-second clock icon spins once), then `printf` (an arrow points to the terminal), then back to `while`. Two loops. |
| 3 | "Run it with 'A' on a computer with one processor…" | Terminal appears: `prompt> ./cpu "A"`. A tiny CPU chip glyph labeled "1 CPU" in the terminal's corner. |
| 4 | "…and every second you get… an A. Then another A. Not thrilling." | "A" lines print once per second, four of them; then `^C` and the prompt. Student (bored). |

**Ends with:** code block at left, terminal (cleared to a fresh prompt) at right.

### S10 — Four at once, one CPU   (beats: B05, lines 3–7) · ~0:55
**Purpose:** the CPU illusion for real (Figure 2.2); introduce "policy".
**Starts with:** S09 end state.
**Layout:** the code block fades. Terminal moves to the left (−3.6, 0.6), 5 × 4. A world at the right: CPU at (3.2, 1.0); A–D in a row below it at y = −0.8 (x = 1.7, 2.7, 3.7, 4.7). A mini Timeline at y = −2.2, x 1..6.3.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Now let's run *four* of them at once: A, B, C and D." | Terminal: `prompt> ./cpu A & ./cpu B & ./cpu C & ./cpu D &`, then `[1] 7353` … `[4] 7356`. As each job line prints, the matching Process (A–D) pops into the row on the right. |
| 2 | "One processor." | The CPU chip `GrowFromCenter` with a "×1" tag. |
| 3 | "And yet: A, B, D, C, A, B, D, C…" | **Sync:** each time the terminal prints a letter, that process hops onto the CPU (→ running) and its slice fills the timeline. The order is exactly A B D C A B D C A. A runs 2 cycles at 0.8 s per letter, then it speeds up. |
| 4 | "All four seem to be running at the same time." | Student (surprised). |
| 5 | "That's the peach, for real." | The peach icon flashes over the CPU for 0.5 s (callback). |
| 6 | "The OS, with some help from the hardware, creates an **illusion**: that the system has a very large number of virtual CPUs." | Above the row, four translucent virtual CPUs appear, one over each process, then many more fade in behind them (a field of faint chips, suggesting "very large"). Term highlight "illusion". |
| 7 | "This is **virtualizing the CPU**, and it's the subject of the next several episodes." | Term highlight "virtualizing the CPU". Tag "→ Ep. 04–10" by the CPU. |
| 8 | "If two programs both want to run right now, *which* one should?" | Two processes (B, C) both step toward the CPU at the same time and bump into each other. A "?" appears. |
| 9 | "Questions like that are answered by a **policy**." | Term highlight "policy". A spotlight cone from above picks C; B steps back. (Same spotlight icon as episode 04's S08.) |
| 10 | "Deciding them is the OS's job as resource manager." | A tiny OS band slides under the world with "resource manager" on it. Hold 0.8 s. |

**Characters:** Student (surprised).
**Ends with:** terminal (left), CPU world + timeline (right).
**Implementation notes:** the terminal output order must match Figure 2.2 (A B D C A B D C A…). Drive the hops from the same list that prints the letters.

### S11 — Memory is an array of bytes   (beats: B06, lines 1–3) · ~0:50
**Purpose:** physical memory = an array of addressed bytes; meet `mem` (Figure 2.3) and PIDs.
**Starts with:** S10 end state.
**Layout:** Memory drawn **horizontally** at the top (y = 2.0) as 12 cells, each 0.9 wide, with hex addresses under them (`0x1FFFFC`… `0x200008`…). Code block at left (−3.6, −0.8). Terminal at right (3.4, −0.8), 5.4 × 3.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Now memory." | Everything from S10 fades. A Term highlight "physical memory" appears. |
| 2 | "Physical memory is simple. It's an array of bytes." | The horizontal strip of cells draws left to right (`MEM_COLOR` stroke). |
| 3 | "To **read**, you give an address." | An arrow labeled `read 0x200000` points at a cell; its value "7" flies out. |
| 4 | "To **write**, you give an address and the data." | An arrow `write 0x200004 ← 9`: a "9" flies into that cell and replaces the old value. |
| 5 | "Every running program touches memory constantly, even just to fetch its own instructions." | Tiny pulses flicker along the strip (many reads per second). |
| 6 | "Here's another tiny program, `mem`." | Code block (**Figure 2.3**, trimmed): `int *p = malloc(sizeof(int));` / `printf("(%d) addr of p: %p\n", getpid(), p);` / `*p = 0;` / `while (1) {` / `    Spin(1);` / `    *p = *p + 1;` / `    printf("(%d) p: %d\n", getpid(), *p);` / `}`. Title `mem.c`. |
| 7 | "It asks for a little memory with `malloc()`, prints the address it got, stores a zero there…" | Highlights step through lines 1–3. On `malloc`, one cell in the strip turns lilac and is labeled "p". |
| 8 | "…and then once a second adds one and prints it." | The loop lines highlight; the lilac cell's value increments 0 → 1 → 2. |
| 9 | "Each line starts with the program's **process identifier**, or **PID**, a number unique to each running program." | Term highlight "process identifier (PID)". A lilac Process "PID 2134" appears next to the terminal (the book's single-run PID). |
| 10 | "Run it once: the memory is at address `0x200000`, and the value counts 1, 2, 3, 4." | Terminal: `prompt> ./mem` / `(2134) address pointed to by p: 0x200000` / `(2134) p: 1` … `p: 4`, in sync with the lilac cell's value. |

**Ends with:** horizontal memory strip, `mem.c` code, terminal, PID 2134 process.
**Implementation notes:** the book uses PID 2134 for the single run and 24113/24114 for the double run; keep both exactly. The lilac process is the same visual "kind" as 24113.

### S12 — Same address, different place   (beats: B06, lines 4–8) · ~0:55
**Purpose:** two processes, same virtual address, different physical cells → virtual address spaces (Figure 2.4).
**Starts with:** S11 end state.
**Layout:** **Illusion split**, horizontal this time. Top half, "what each process sees": two private memory strips side by side (x −5..−0.5 and 0.5..5, y = 2.2), each showing a highlighted cell `0x200000`. Bottom half, "what really happens": one physical strip (y = −1.4), wider, 16 cells. The processes stand at the far left/right of the top strips.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Now run two copies at once." | Code and terminal shrink into a corner tag `./mem & ./mem &` (top-center). PID 2134 morphs into **PID 24113** (lilac); a second process **PID 24114** (pink) appears. Each gets its own top strip (a copy of the memory strip). |
| 2 | "Look at the addresses. *Both* say `0x200000`. The same address!" | Both strips highlight cell `0x200000` and each process holds a card "p = 0x200000". The two cards `Indicate` at the same time. |
| 3 | "And yet each one counts up on its own: 1, 1, 2, 2, 3, 3." | The values in the two highlighted cells tick up alternately (lilac 1, pink 1, lilac 2, pink 2, …), driven by a mini output log at the top-center matching Figure 2.4. |
| 4 | "They never interfere." | Hold; neither value ever jumps. |
| 5 | "How can two programs use the same address without overwriting each other?" | Student (confused). |
| 6 | "Because 'the same address' isn't the same *place*." | Professor (proud). The divider draws; the physical strip appears below, labeled "physical memory". |
| 7 | "Each process gets its own private **virtual address space**…" | The top strips get dashed outlines in their process colors and the label "virtual address space". Term highlight "virtual address space". |
| 8 | "…and the OS maps it onto the real, physical memory." | Arrows: lilac `0x200000` → physical cell 3; pink `0x200000` → physical cell 11. The physical cells take the processes' colors and *also* tick up in sync. |
| 9 | "Same address on the outside, different bytes underneath. That's **virtualizing memory**." | Both arrows pulse together. Term highlight "virtualizing memory". |
| 10 | "A small honesty note: on a real machine you'd have to turn off a security feature called address-space randomization…" | Professor (worried). A small Aside card at the bottom-right (3.8, −3.0), "ASIDE · needs ASLR off", with a padlock icon. |
| 11 | "We'll explain why later." | The Aside card fades. |

**Characters:** Student (confused), Professor (proud → worried).
**Ends with:** the horizontal illusion split with the mapping arrows.
**Implementation notes:** this scene is the static preview of episode 13/15's address translation. Draw the mapping arrows with `CurvedArrow` so they cross the divider visibly.

### S13 — Two threads, one counter   (beats: B07, lines 1–7) · ~0:55
**Purpose:** concurrency surprise: the shared counter gives wrong and changing results (Figure 2.5).
**Starts with:** S12 end state.
**Layout:** Code block at left (−3.8, 0.4), font 20, **Figure 2.5** trimmed to the worker: `volatile int counter = 0;` / `void *worker(void *arg) {` / `    for (i = 0; i < loops; i++)` / `        counter++;` / `}` / `// main: create 2 threads, join both, print counter`. Right: a shared memory cell "counter" (big, 1.6 × 1.0, `MEM_COLOR`) at (3.2, 1.2), threads T1 at (1.6, −0.6) and T2 at (4.8, −0.6). Terminal strip at (3.2, −2.6), 6 × 1.2.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Second piece: **concurrency**." | Everything fades. The badge dot → `CONC`. Term highlight "concurrency". The piece card "Concurrency" flashes briefly at the top. |
| 2 | "…a host of problems that show up when you work on many things at once. The OS itself ran into them first." | A mini callback: the four A–D processes jostling at the CPU (2 s), labeled "the OS juggles too". |
| 3 | "Today, any **multi-threaded** program meets them too." | Term highlight "multi-threaded". |
| 4 | "A **thread** is like a function running in the same memory as other functions, with more than one active at a time." | One process outline (big, dashed) contains two small blobs T1 and T2 (mint, sky). The outline is labeled "one program · one memory". Term highlight "thread". |
| 5 | "This program creates two threads. Each one adds one to a shared counter, over and over, *loops* times." | The code block writes. T1 and T2 leave the outline to their positions; a line from each to the shared "counter" cell. Each thread taps the cell: "+1". |
| 6 | "Loops equals a thousand. Two threads, a thousand each. The final value?" | Terminal: `prompt> ./threads 1000`. The counter spins fast. |
| 7 | "Two thousand!" | Student (excited). |
| 8 | "Two thousand. Correct." | The counter lands on **2000**; a green ✓. Terminal: `Final value : 2000`. |
| 9 | "Now loops equals a hundred thousand. We expect two hundred thousand…" | Terminal: `./threads 100000`. A `DIM` "expected: 200000" tag beside the counter. |
| 10 | "…and we get 143,012." | The counter lands on **143012** in red; it shakes. Terminal: `Final value : 143012   // huh??` |
| 11 | "Run it again: 137,298. Wrong, and wrong *differently*." | It runs again → **137298**, red. Terminal: `// what the??` |
| 12 | "Huh?? It's the same program!" | Student (frustrated). |

**Characters:** Student (excited → frustrated).
**Ends with:** code, counter cell (137298, red), T1/T2, terminal.

### S14 — Load, add, store   (beats: B07, lines 8–9 + crux) · ~0:55
**Purpose:** why: `counter++` is three non-atomic steps; an interleaving loses an update.
**Starts with:** S13 end state.
**Layout:** zoom in: the shared counter cell at top-center (0, 2.2) showing **5**. T1 at left (−4, 0.2) and T2 at right (4, 0.2), each with a small register box `r` next to it. Two step lanes (−4..−1 and 1..4, y −0.6..−2.6) list "load / add 1 / store" for each thread, plus a clock/step arrow at the far left.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Here's why. Adding one to the counter isn't one step. It's three:" | Professor (explaining). The code line `counter++;` flies out of the code block to the center and **splits** into three lines: `load r ← counter`, `r = r + 1`, `store counter ← r`. |
| 2 | "load the value from memory into a register, add one, store it back." | T1 does all three in slow motion: 5 flies from the cell into T1's `r` box; it becomes 6; 6 flies back to the cell → **6**. Reset the cell to 5. |
| 3 | "Those three don't happen **atomically**, all at once." | Term highlight "atomically". The three steps are drawn as three separate blocks with gaps between them. |
| 4 | "So if the two threads interleave in the middle…" | Interleaving, step by step (each step 0.8 s, with a "step" counter): T1 load (r₁ = 5) → T2 load (r₂ = 5) → T1 add (r₁ = 6) → T2 add (r₂ = 6) → T1 store (cell = 6) → T2 store (cell = 6). |
| 5 | "…one update can overwrite the other." | The final store from T2 lands on the cell; a ghost "7" (what we expected) appears beside the cell and cracks/fades. Caption: "2 increments, +1 result". |
| 6 | (crux) | Crux card in `CONC`: **"How to build correct concurrent programs?"**, subtitle "Many threads, one memory: what primitives from the OS? from the hardware?" Hold 2 s. |
| 7 | (end) | Tag "→ Ep. 26–28". The card docks briefly, then everything fades. |

**Characters:** Professor (explaining).
**Ends with:** empty (badge only).
**Implementation notes:** it's the same interleaving we'll reuse in episode 26. Build it as a parameterized `InterleavingDemo` in `ostep_lib/props` (steps list → animation).

### S15 — Volatile vs persistent   (beats: B08, paragraphs 1–2) · ~0:35
**Purpose:** memory forgets when the power goes; disks remember; meet the file system.
**Starts with:** empty (badge).
**Layout:** Memory column at left (−3, 0.4) with 6 cells holding values; Disk at right (3, 0.2) with three file icons stacked on it. A power switch at the center top (0, 2.4).

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Third piece: **persistence**." | Badge dot → `PERS`. Term highlight "persistence". The memory column and the disk `FadeIn`. |
| 2 | "Memory, the DRAM in your computer, is **volatile**." | The column's label "DRAM". Term highlight "volatile". |
| 3 | "Cut the power, or crash, and everything in it is gone." | The power switch flips OFF (rotate the lever). The screen dims; the memory values fade to empty cells, one by one; the disk's files stay crisp. |
| 4 | "So we need hardware and software that store data *persistently*." | The power switch flips back ON. The memory is empty; the disk's files are still there, and they glow. |
| 5 | "The hardware is some kind of **I/O device**: a **hard drive**, or more and more often a **solid-state drive**." | The disk gets a tag "HDD"; a flat SSD rectangle slides in beside it, tag "SSD". Term highlight "I/O device". |
| 6 | "The software is the **file system**. It stores the files you create, reliably and efficiently." | A layer labeled "file system" (green tint) wraps over the disk (on the OS band height, (3, 1.6)). Term highlight "file system". |

**Ends with:** empty memory column, disk + SSD with files, file-system layer.

### S16 — Files are shared   (beats: B08, paragraph 3) · ~0:25
**Purpose:** unlike CPU and memory, storage is *not* virtualized per program; files flow between programs.
**Starts with:** S15 end state.
**Layout:** three program boxes in a row at y = 1.2: `emacs` (−4), `gcc` (0), `./main` (4), each a small Process wearing a tag. The disk at the bottom center (0, −2.0).

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Unlike the CPU and memory, the OS does *not* give each program a private virtual disk." | The memory column fades. The disk slides to (0, −2.0). Three processes appear at the top. A "private disk?" ghost icon appears under each process, then gets crossed out. |
| 2 | "Files are meant to be **shared**." | All three processes connect by lines to the *same* disk. |
| 3 | "You write `main.c` in an editor." | `emacs` writes: a file icon `main.c` pops out of it and drops into the disk. |
| 4 | "The compiler reads it and writes an executable." | The `main.c` file rises from the disk into `gcc`; `gcc` outputs a file `main` that drops into the disk. |
| 5 | "Then you run that. Three programs, passing files along like a relay." | `main` rises into `./main`, which blinks to life. A relay-baton arc connects the three handoffs. |

**Ends with:** three processes, disk, two files.
**Implementation notes:** the book says "you should be using Emacs"; an optional Easter egg is a tiny `DIM` footnote "(the book insists on Emacs)".

### S17 — Three system calls, one crash   (beats: B08, paragraph 4 + crux + lines) · ~0:50
**Purpose:** `open`/`write`/`close` are system calls into the file system; the FS must survive crashes.
**Starts with:** S16 end state.
**Layout:** system stack variant: the program (a Process) at the top (−4, 1.6) with the Code block next to it (−1, 1.6); the OS band at y = 0, containing a "file system" box (−1.5, 0) and a "device driver" box (2.5, 0); the Disk at (2.5, −2.2).

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "In code, writing 'hello world' to a file is three system calls: `open()`, `write()`, `close()`." | The S16 actors fade. Code block (**Figure 2.6**, trimmed): `int fd = open("/tmp/file", O_WRONLY \| O_CREAT \| O_TRUNC, S_IRWXU);` / `write(fd, "hello world\n", 12);` / `close(fd);`. The OS band slides in. As each call is named, its line highlights and a small envelope (the request) drops from the program down into the band through a "syscall" door. |
| 2 | "Behind them, the file system figures out where on disk the data goes, keeps its own bookkeeping…" | Inside the "file system" box, a mini map of disk blocks; one block gets chosen and marked; a small ledger icon updates. |
| 3 | "…and talks to the device through a **device driver**." | The request moves from the "file system" box to the "device driver" box, then down a cable to the Disk, which spins; "hello world" lands on a block. Term highlight "device driver". |
| 4 | "And it has to survive a crash *in the middle* of all that…" | During a second write, the Computer (scale 0.6, bottom-left (−5.4, −2.6)) → error. The screen flickers off for 0.3 s (full-frame black flash). The block on the disk is half-written (half green, half red). |
| 5 | "…using tricks like **journaling** or **copy-on-write**." | Two tiny icons appear by the disk: a notebook ("journal") and two overlapping pages ("copy-on-write"), each with "→ Ep. 42" in `DIM`. Terms highlighted together (smaller). |
| 6 | (crux) | Crux card in `PERS`: **"How to store data persistently?"**, subtitle "Correctly, fast, and reliably, even when hardware and software fail." |
| 7 | "So what happens to my file if it crashes halfway?" | Student (surprised), pointing at the half-written block. |
| 8 | "Hold that thought for the whole third part of the series." | Professor (happy). The half-written block gets a sticky note "later!" and the card docks. Computer → idle. |

**Characters:** Computer (error → idle), Student (surprised), Professor (happy).
**Ends with:** program + code, OS band with FS + driver, disk with a half-written block and a sticky note.

### S18 — What makes a good OS?   (beats: B09) · ~1:05
**Purpose:** design goals: abstraction, performance (overheads), protection (isolation), reliability, plus extras.
**Starts with:** S17 end state.
**Layout:** first a tower of 5 abstraction layers at center (0, 0.2), each 4 × 0.7. Then four goal badges in a row at y = 0.4 (x = −4.8, −1.6, 1.6, 4.8), 2.6 × 2.6 each, with a small row of three extras underneath at y = −2.0.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "So an OS virtualizes resources, handles concurrency, and stores files persistently. If we're going to build one, what should we aim for?" | S17 fades. Badge dot → `INTRO`. The three piece cards flash in a row at the top, then dock as a strip at (0, 3.3). |
| 2 | "First, **abstractions** that make the system easy to use." | Term highlight "abstraction". |
| 3 | "We write C without thinking about assembly…" | The tower builds bottom-up, quickly: "transistors", "logic gates", "assembly", "C", "programs". |
| 4 | "…assembly without thinking about logic gates, gates without thinking about transistors." | As each phrase lands, the layer under the current one dims ("you don't need to look down"). |
| 5 | (transition) | The tower collapses into badge 1: a layered-stack icon labeled "Abstraction". |
| 6 | "Second, **performance**." | Badge 2: a stopwatch. Term highlight "performance". |
| 7 | "Virtualization is worth it, but not at any cost. We want to **minimize the overheads**, in extra time and in extra space." | Inside badge 2: two small bars, "time" and "space", with a thin "overhead" slice on top of each that shrinks. Term "minimize overheads" (smaller). |
| 8 | "Third, **protection**. One misbehaving program, malicious or just buggy, must not harm the others, or the OS itself." | Badge 3: three processes separated by walls; one turns red and angry and bangs on a wall; the wall holds. Term highlight "protection". |
| 9 | "The principle behind that is **isolation**." | The walls glow. Term highlight "isolation". |
| 10 | "Fourth, **reliability**. If the OS fails, *everything* fails, so it has to keep running." | Badge 4: a heartbeat line (ECG) that keeps beating. Term highlight "reliability". |
| 11 | "Add **energy efficiency**, **security** and **mobility**, and you have a long wish list." | Three mini badges underneath: a leaf, a padlock, a phone. Then a scroll unrolls behind all badges as a "wish list" (comic touch). |

**Characters:** corner mode, no reactions needed (optional Student curious at step 1).
**Ends with:** 4 goal badges + 3 extras, the piece strip at the top.

### S19 — Just a library; the batch era   (beats: B10, paragraphs 1–2) · ~0:35
**Purpose:** history 1: the OS as a library; batch processing with a human operator.
**Starts with:** S18 end state.
**Layout:** a history **Timeline** (bible prop, used as an era ribbon) across the top (y = 2.6, x −6..6) with era markers: "mainframes", "Atlas", "minicomputers / UNIX", "PCs", "today". The scene stage is below it.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "These ideas didn't arrive all at once. Engineers learned them the hard way." | The badges fade. The era ribbon draws left to right; a marker sits on "mainframes". |
| 2 | "In the beginning, the OS was **just a library** of handy routines, like I/O code…" | A bookshelf icon labeled "OS = library" next to a giant mainframe cabinet (tall rectangles with blinking dots) at (−2, −0.4). Term highlight "just a library" (smaller). |
| 3 | "On the old mainframes, one program ran at a time." | A single Process sits on a CPU inside the mainframe. |
| 4 | "A *human operator* decided the order." | A simple humanoid operator icon (circle head + body; not a series character) at (2, −0.4) holds a stack of punch cards. |
| 5 | "Jobs were run in a **batch**." | A queue of 5 punch-card jobs feeds into the mainframe one at a time. Term highlight "batch processing". |
| 6 | "Nobody sat at the machine interactively. It was simply too expensive to let it sit idle." | A chair in front of the machine with a ✕; a "$$$ / hour" meter ticking fast next to the mainframe. |

**Ends with:** the era ribbon (marker on mainframes), mainframe + operator.

### S20 — The system call: crossing the line   (beats: B10, paragraph 3 + dialogue) · ~0:55
**Purpose:** system call vs procedure call; user/kernel mode; trap, trap handler, return-from-trap. This scene **introduces the User/Kernel boundary prop**.
**Starts with:** S19 end state.
**Layout:** the era marker moves to "Atlas". **User/Kernel boundary**: a horizontal dashed line at y = −0.3 across the screen; the area above is tinted `USER_COLOR` at 0.08 and labeled "user mode" (−6.2, 0.2), and the area below is tinted `KERNEL_COLOR` at 0.10 and labeled "kernel mode" (−6.2, −0.8). A Process (A, coral) at (−2.5, 1.2). The OS's trap handler box at (2, −1.8). The Disk at (5, −2.6).

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Then came a realization: code that runs on behalf of the OS is *special*." | The mainframe and the operator fade. The marker slides to "Atlas". |
| 2 | "If any program could read anywhere on the disk, privacy would be gone." | Process A reaches a long arm straight to the Disk and pulls out a file marked "someone else's" (red flash). |
| 3 | "So the **system call** was invented, pioneered by the Atlas computer." | Rewind the grab. The dashed boundary line **draws** across the screen, and the two tinted areas fade in. Term highlight "system call". |
| 4 | "It's not a normal **procedure call**." | On the user side, A calls a function box `f()`: a small arrow goes out and comes back on the *same level*. Label "procedure call". |
| 5 | "It jumps into the OS *and* raises the **hardware privilege level**." | A privilege meter (vertical gauge) at the right edge (6.4, 0) reads "USER". |
| 6 | "Applications run in **user mode**, where the hardware restricts what they can do: no direct disk I/O, no touching any memory they like." | Term highlight "user mode". A tries to reach the disk again; its arm hits the dashed line and bounces (a "denied" spark). |
| 7 | "A special **trap** instruction jumps to a **trap handler** set up by the OS…" | A emits a `trap` arrow that **crosses the line** downward (the line flashes where it's crossed) into the "trap handler" box. Terms highlighted "trap", "trap handler". |
| 8 | "…and switches to **kernel mode**, with full access to the hardware." | The privilege gauge flips to "KERNEL" (red). The handler reaches the Disk freely and gets A's data. Term highlight "kernel mode". |
| 9 | "When the OS is done, a **return-from-trap** drops back to user mode, right where the application left off." | A `return-from-trap` arrow goes back up across the line to A, carrying the data; the gauge flips back to "USER". A continues (a small bounce). Term highlight "return-from-trap". |
| 10 | "So programs ask permission, and the OS does the dangerous stuff?" | Student (curious). |
| 11 | "Exactly. Remember that dashed line. We'll cross it a lot." | Professor (happy). The dashed line pulses twice. Tag "→ Ep. 06". |

**Characters:** Student (curious), Professor (happy).
**Ends with:** the era ribbon on "Atlas", the user/kernel boundary and both zones, A, the handler box, the Disk.
**Implementation notes:** build `UserKernelBoundary` as a reusable prop (line + two tints + labels + a `cross(mobject, direction)` animation that flashes the crossing point). The privilege gauge is a small reusable widget too.

### S21 — Multiprogramming and UNIX   (beats: B10, paragraph 4) · ~0:35
**Purpose:** minicomputers → multiprogramming (switch on I/O) → memory protection + concurrency matter; UNIX and pipes.
**Starts with:** S20 end state.
**Layout:** the marker moves to "minicomputers / UNIX". Left stage (−3.2, 0): a CPU with 3 processes and a Disk. Right stage (3.2, 0): a pipeline of small boxes.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Next, cheaper **minicomputers** brought **multiprogramming**." | The boundary fades (it will return in episode 06). The marker slides. A minicomputer icon (a smaller cabinet) on the left stage; three processes (A, B, C colors) load into it at once. Term highlight "multiprogramming". |
| 2 | "Load several jobs, and switch between them rapidly, especially while one waits for slow I/O." | A asks the Disk for something → blocked (clock); B hops onto the CPU immediately → running. (This is the preview of episode 04's S16.) |
| 3 | "That made **memory protection** and **concurrency** critical." | Thin walls appear between the processes' memory (small colored strips under each process); a tiny CONC-cyan spark between B and C. Terms "memory protection" (smaller). |
| 4 | "This era also gave us **UNIX**, from Ken Thompson and Dennis Ritchie at Bell Labs." | Right stage: "UNIX" in a classic monospace font, large; under it in `DIM`: "Thompson & Ritchie · Bell Labs". |
| 5 | "It was simple and powerful, built from small programs chained with **pipes**…" | A pipeline: `grep foo file.txt` → `|` → `wc -l`. Text lines flow through the pipe (small dashes moving), and a number "3" comes out of `wc -l`. Term highlight "pipes". |
| 6 | "…and written in the new C language." | A small "C" badge attaches to the UNIX logo. |

**Ends with:** the era ribbon on "minicomputers / UNIX", the left and right stages.

### S22 — The PC detour and today   (beats: B10, paragraph 5) · ~0:35
**Purpose:** PCs forgot the lessons, then relearned them; UNIX ideas run everything today.
**Starts with:** S21 end state.
**Layout:** marker to "PCs", then "today". Center stage: a beige PC box (a reuse of the **Computer** character, scale 0.9, at (0, 0.2)).

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Then the **personal computer**." | The stages fade. The marker slides to "PCs". The Computer appears at center (happy). Term highlight "personal computer" (smaller). |
| 2 | "At first it was a great leap *backwards*." | The era ribbon's marker briefly slides *left* (backwards) with a comic skid, then returns. |
| 3 | "Early systems like DOS had no memory protection…" | Inside a memory strip under the Computer, one red Process scribbles across everyone's colored regions. Computer → error. |
| 4 | "…and early Mac OS let one stuck program freeze the entire machine." | A process spins forever on the CPU (a loop arrow); everything else freezes (desaturate). Computer → overwhelmed. Then the screen "reboots" (black flash) and the Computer → idle. |
| 5 | "Eventually the old lessons returned. macOS has UNIX at its core. Windows NT adopted the great ideas." | The marker slides to "today". Two generic desktop icons (an unbranded laptop and an unbranded desktop) each get a small "UNIX-like ideas" or "NT" tag. Walls between processes reappear in the memory strip. |
| 6 | "Linux, started by Linus Torvalds, runs most of the internet and Android." | A server rack and a phone outline appear, tag "Linux". (No logos or mascots: plain shapes and text only.) |
| 7 | "Your phone runs an OS far closer to a 1970s minicomputer's than to an early PC's." | The phone slides next to the minicomputer icon from S21 (fading back in); a "≈" between them, and the early PC icon to the side with a "≠". Hold 1 s. |

**Characters:** Computer (happy → error → overwhelmed → idle).
**Ends with:** the era ribbon on "today", the phone ≈ minicomputer.
**Implementation notes:** avoid brand logos entirely (no Apple, Windows or Tux marks). Use generic device outlines and text tags.

### S23 — The map   (beats: B11) · ~0:50
**Purpose:** recap as a map of the series: three pieces on top of the system stack, with the user/kernel line underneath.
**Starts with:** S22 end state.
**Layout:** the system stack from S05 (centered, scale 0.9), the three piece cards from S02 above it at y = 2.4 (x = −4, 0, 4), each now holding a thumbnail of its demo. The dashed User/Kernel line sits right above the OS band.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "So, an operating system is the software that makes a computer easy to use, correctly and efficiently. Here's our map." | The ribbon and the devices fade. The system stack rebuilds quickly (hardware → OS band → programs). The section badge's dot → `INTRO`. |
| 2 | "**Virtualization**: one physical CPU and one memory become many virtual ones." | The Virtualization card drops onto the stack above the CPU and Memory; a thumbnail inside: letters "A B D C" + the two `0x200000` arrows. Faint virtual copies flash over the CPU and Memory. |
| 3 | "**Concurrency**: doing many things at once, correctly." | The Concurrency card lands above the programs; a thumbnail: two threads and a counter "143012" crossed out → "200000 ✓". |
| 4 | "**Persistence**: data that survives power loss and crashes." | The Persistence card lands above the Disk; a thumbnail: file + disk + power switch. |
| 5 | "Along the way: abstraction, performance, protection and reliability, and the user/kernel line that makes protection possible." | The four goal badges (mini) line up along the bottom (y = −3.2). The dashed User/Kernel line draws across, just above the OS band, and pulses. |
| 6 | "We won't go deep into networking or graphics." | Two small `DIM` tags at the far right, "networking", "graphics", slide in and fade to 30% with a "(other courses)" note. |
| 7 | "We'll touch on security where the OS must protect programs and files." | A small `SEC` teal padlock tag stays, labeled "security". |
| 8 | "But the three pieces are the core." | The three cards `Indicate` together. Hold 1.5 s. |

**Ends with:** the full map.
**Implementation notes:** thumbnails are scaled-down copies of the actual S10/S12/S13–S14/S15 mobjects (rebuild them with `common.py` builders at scale 0.25).

### S24 — Into virtualization   (beats: B12) · ~0:45
**Purpose:** a dialogue outro that hands off to episode 04.
**Starts with:** S23 end state.
**Layout:** dialogue mode. The Virtualization card grows to fill the screen at the end.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "And so we reach the first of our three pieces: virtualization." | The map fades except the Virtualization card, which moves to center-top (0, 2.2) and grows ×1.5. Characters → dialogue mode. Professor (happy). |
| 2 | "The peach thing! Tell me more. How does it actually *work*?" | Student (excited). The peach pops onto the card. |
| 3 | "In time, young student, in good time." | Professor (thinking). |
| 4 | "We'll start with the most basic illusion of all: the CPU." | The peach on the card morphs into a CPU chip. |
| 5 | "And the thing the OS creates to pull it off: the **process**." | A coral Process (A) hops out of the card and onto the CPU (→ running). Term highlight "process" (this is a *preview*; episode 04 gives the definition). |
| 6 | "I'm a little worried you're going to start talking about peaches again." | Student (sad). The peach peeks back in from the bottom edge of the frame. |
| 7 | "Don't worry too much. I don't even like peaches." | Professor (happy). The peach rolls away off the right edge. |
| 8 | (end card) | The Virtualization card expands to fill the screen in `VIRT` orange, then fades to BG. End card: "Next: 04 · The Process" with a `VIRT` dot. Hold 2 s. |

**Characters:** Professor (happy → thinking → happy), Student (excited → sad).
**Ends with:** black/BG end card.

## New assets needed
These are in addition to the episode 04 list (CPU, Memory, Disk, Timeline, Queue, cards, term
highlight, section badge, illusion split, `hop_to`, icons), which this episode needs too. Build
them in `ostep_lib/props/` unless noted.

- **Style constant `INTRO`**: an accent for intro/overview episodes. There is none in the bible yet. Suggestion: `TEXT`-ish warm white `#E8E2D0`. The book's site uses yellow for Intro, but yellow is `CPU_COLOR`.
- **`SystemStack`**: hardware row (CPU, Memory, Disk) + OS band + programs row, with methods to light up a resource, insert virtual copies above the band, and route request lines through the band (S05, S06, S17, S23).
- **`Peach`**: the peach mobject (see the assignments table); reused in episode 04.
- **`Terminal`**: rounded console with a prompt; `.type(cmd)` and `.print(line)` animations, auto-scroll, and an optional CPU-count glyph in the corner.
- **`MemoryStrip`**: a *horizontal* memory array with hex addresses, `.read(addr)`, `.write(addr, value)` animations, and cell coloring (S11, S12). A variant of `Memory`.
- **`MappingArrows`**: virtual cell → physical cell curved arrows across a horizontal illusion split (S12). This makes `IllusionSplit` support an `orientation="horizontal"` option.
- **`InterleavingDemo(steps)`**: shared cell + two thread lanes + per-thread register boxes; plays a list of `(thread, op)` steps (load/add/store) (S14). It will be reused in episode 26.
- **`UserKernelBoundary`**: the dashed line + tinted zones + labels, with a `cross()` animation (S20). This is the bible's prop, made real here. Plus a small **`PrivilegeGauge`** (USER/KERNEL).
- **`EraRibbon(eras)`**: a horizontal history ribbon with a sliding marker (S19–S22).
- **Icons:** book, code-editor glyph, punch-card stack, mainframe cabinet, minicomputer, generic humanoid operator, server rack, phone, laptop/desktop outlines, power switch, SSD, journal notebook, copy-on-write pages, sticky note, padlock, leaf, stopwatch, ECG line, wish-list scroll, pipe glyph, campaign-poster frame, file icon, spotlight (shared with episode 04). All primitives; **no brand logos**.
- **Thread stand-in:** for now, `Process` scaled ×0.65 with "T1"/"T2" labels. If you want a proper `Thread` character, it should be added to `ostep_lib/characters` (see Open questions).
- **Bible update:** add `SystemStack`, `Terminal`, `Peach` and `EraRibbon` to the props table (§6), and `INTRO` to the palette (§5).

## Open questions
- **Intro accent color:** OK with a warm off-white (`#E8E2D0`) for overview episodes, or do you prefer another color?
- **Thread character:** create a dedicated `Thread` character now (e.g. a mini blob that is visibly "inside" a parent process), or keep the scaled-Process stand-in until episode 26?
- **On-screen credit:** S01 shows the authors and "free at ostep.org" under the title. Is that the credit format you want for every episode (e.g. also in the end card)?
- **Real names:** the narration names Feynman, Thompson & Ritchie, and Torvalds, as text only. No likenesses are drawn, and no logos. OK?
- **S06 "MASTER CONTROL PROGRAM" gag:** it's a nod to the book's *Tron* footnote. Keep it, or too silly?
- **History scenes (S19–S22, ~2:25):** these are the most "illustrative" and least mechanism-driven. If we need to cut time, S22 can shrink to ~0:15.
