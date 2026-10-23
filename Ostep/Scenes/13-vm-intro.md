# 13 — The Abstraction: Address Spaces · Scene breakdown
> Script: Ostep/Scripts/13-vm-intro.md · Scenes: 20 · Est. duration: ~11:30

## Visual overview
- **Core metaphor: one memory column, drawn two ways.** The `Memory` prop (0 at top) is the whole
  episode. First it is *physical* memory (the early machine, then the 512KB machine of Figure 13.2),
  then it becomes *one process's private picture*: the 16KB **address space** of Figure 13.3
  (code / heap / free / stack). The pivotal image (S12) is that private column **lifting off and landing on a
  slice of the physical column** (A's 16KB lands at physical 320KB), which the viewer then keeps in mind for 14, 15 and the rest
  of the memory arc.
- **Two recurring columns, one canonical look each (reused by later episodes):**
  - *Virtual / address-space column* ("AS16"): `Memory(regions=["code", "heap", ("free", 6), "stack"],
    addresses=["0KB", "1KB", "2KB", "15KB", "16KB"], width=1.6, height=4.4)`. Region heights are
    *not to scale* (free is 13KB in the book, drawn as 6 units of weight); a small zigzag "break" mark on the free
    region says so. Free is DIM-hatched (`hatch_rect`). Code/heap/stack use fixed shades: code = `MEM_COLOR`,
    heap = `MEM_COLOR` lighter, stack = `MEM_COLOR` darker; the **owner process's color** shows as the frame/outline
    when it belongs to A, B or C.
  - *Physical column* ("PHYS512"): `Memory(regions=[("OS",1),("free",1),("C",1),("B",1),("free",1),("A",1),("free",2)],
    addresses=["0KB","64KB","128KB","192KB","256KB","320KB","384KB","448KB","512KB"], width=2.0, height=4.4)`.
    OS slice `KERNEL_COLOR`; A, B, C slices use the process colors; free slices hatched DIM. This is Figure 13.2 exactly.
  Both are built by the new helper module in "New assets" so 14 and 15 draw them identically.
- **Persistent assignments**

| Thing | Look |
|---|---|
| Process A | `Process(label="A", color=PROCESS_COLORS[0])` coral. Its slice/column outline is coral everywhere. |
| Process B | `PROCESS_COLORS[1]` mint. The one that "scribbles" in the protection scene. |
| Process C | `PROCESS_COLORS[2]` gold. |
| OS | `KERNEL_COLOR` (red) block, with the `KernelToken` "OS" badge when a label is needed. |
| Section badge | `VIRT` dot + "13 · Address Spaces", at (−6.6, 3.6), appears in S01, stays to S19. |
| Terms | **Key terms (Term unveil, `terms.show`, veil + center): *address space* (S09), *virtual address* (S13), *virtualizing memory* (S14)**; they are never in neighbouring rows. **Term notes (`terms.note`, no veil):** *multiprogramming* (S04), *time sharing* (S05), *protection* (S08), *stack* and *heap* (S10, one note each), *transparency* (S15), *efficiency* (S16), *isolation* (S17). Each docks top-right, replacing the previous one. |
| Crux strip | Docks at y = 3.0 in S12 and stays through S18. |
| Characters (corner mode) | Student at (−5.8, −2.8) scale 0.75; Professor at (5.8, −2.8) scale 0.75, `flip()`. Content stays inside x ∈ (−4.6, 4.6) at y < −1.2. |

- Props used: Terminal, Memory, Disk, CPU, Queue, Process, Padlock, AlarmClock, ClockIcon, Peach,
  AsideCard, TipCard, CruxCard, TermHighlight (unveil + note), SectionBadge, Code (small), `hatch_rect`, `x_mark`,
  `tick_mark`, `save_slot`, `glass_pane`, `SpeedGauge`, `ep_tag`, `hop_to`, `make_translucent`.
- The five **sound-off** takeaways the pictures must carry: (1) early memory = one program; (2) many programs in one
  memory can trample each other; (3) a private column per process with code at the top, stack and heap growing toward each other;
  (4) address 0 in the private column is physical 320KB in the real one; (5) the printed addresses are in the private column.

## Scenes

### S01 — The numbers that lie   (beats: B01, first part) · ~0:35
**Purpose:** hook: the three addresses a C program prints are not real.
**Starts with:** empty (BG).
**Layout:** Section badge top-left (−6.6, 3.6). Terminal at center (0, 0.4), 7.2 × 2.4. Student bottom-left corner, Professor bottom-right (not yet on screen).

| # | Narration | On screen / animation |
|---|---|---|
| 1 | (before the first line) | Badge `Write`s in: `VIRT` dot + "13 · Address Spaces". Terminal `FadeIn`s with the prompt; `$ ./va` is typed (`Terminal.type`). |
| 2 | "Write a tiny C program." | A small `Code` panel (`va.c`, the 9 lines from the book, font 16, 4 wide) slides in at the left of the terminal and the terminal shifts right. |
| 3 | "Print the address of `main`. Print the address of a variable on the stack. Print a pointer you got from `malloc`." | The code lines `printf(... main)`, `printf(... malloc(100e6))`, `printf(... &x)` are highlighted one after another by a moving bar. |
| 4 | "Run it, and out come three big, strange numbers." | The code panel fades out, the terminal re-centers. `print` three lines (MONO): "location of code : 0x1095afe50", "location of heap : 0x1096008c0", "location of stack: 0x7fff691aea64". Hold 1 s. |
| 5 | "Here is a secret. None of those numbers is real." | The three numbers pulse once each and a jagged crack line (3 short `Polyline`s in `KERNEL_COLOR`) runs through each line. |
| 6 | "Every address you have ever printed from a program is a fiction, a story the operating system tells your program." | A rounded stamp "FICTION" (rotated −8°, `KERNEL_COLOR` frame) thumps onto the terminal (`GrowFromCenter`, tiny shake). Pause 1 s. |

**Characters:** none yet.
**Ends with:** badge, terminal with the three cracked lines and the stamp.
**Implementation notes:** `Code` text is the book's `va.c` verbatim. The stamp is a local helper (rect + text); reused in S18 as "virtual".

### S02 — "Fake?"   (beats: B01, second part) · ~0:15
**Purpose:** the Student's disbelief, and the hand-off to "when the OS didn't need to lie".
**Starts with:** S01 end state.
**Layout:** characters enter corner mode.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "The addresses my program prints are *fake*?" | Student `FadeIn` bottom-left, expression → surprised, looks at the terminal; Professor `FadeIn` bottom-right, neutral. A "!" pops over the Student. |
| 2 | "\"Fake\" is harsh. Remember last time: every address a program generates is virtual. Let's say carefully arranged." | Professor → happy. The stamp text changes "FICTION" → "ARRANGED" (`Transform`, small). |
| 3 | "To see why the OS tells this story, we have to go back to a time when it didn't need to." | Professor → explaining. The terminal and stamp `FadeOut` (0.6 s); the Professor's gaze follows them out. Student → curious. |

**Characters:** Student (surprised → curious), Professor (neutral → happy → explaining).
**Ends with:** badge and both characters; empty center.

### S03 — When memory was easy   (beats: B02) · ~0:50
**Purpose:** the simplest world: OS plus one program in a single physical memory; no illusion.
**Starts with:** S02 end state.
**Layout:** physical Memory at center-left (−2.2, 0.2), `width=2.2` (a one-off: OS / Current program), addresses "0KB", "64KB", "max". A Process at (2.6, 0.4) in the right half. Tags for the book labels sit *inside* the cells.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "In the early days, memory was simple. Physical memory looked like a single column, with address zero at the top." | The Memory column draws (`Create`), addresses writing in at the left. A small "0" pulses at the top. |
| 2 | "First comes the operating system: really just a library of routines, sitting at address zero." | Top slice (0 to 64KB) fills `KERNEL_COLOR` (`fill_cell`) with "Operating System" text and a tiny book icon (`book`). |
| 3 | "Above it, one running program, starting at sixty-four kilobytes, and using all the rest." | The lower, bigger slice fills `MEM_COLOR`: "Current program". A Process (neutral color, label "P") grows in at the right, standing on a mini CPU. |
| 4 | "That's it. No illusions." | A thin line connects P to the program slice. A magnifier-free gesture: P's eyes sweep the column top to bottom (`look_at`). |
| 5 | "The program sees the real machine, the real addresses. Life was easy for OS developers." | Little address tags ("64KB", "max") glow on the column to say "the real addresses". Professor → happy. |
| 6 | "So what changed?" | Student → curious. |
| 7 | "Money. Those machines cost hundreds of thousands, even millions of dollars." | Professor → explaining. A price tag with "$ $ $ $" hops in beside the column and bobs. |
| 8 | "Leaving one idle while a single program waits is a very expensive way to wait." | P turns `blocked`, a clock spins above it (`ClockIcon.spin`); the CPU under it fades to grey and the price tag turns red. Pause 1 s. |

**Characters:** Student (curious), Professor (happy → explaining).
**Ends with:** the early-days column (OS + program), P blocked with the CPU dim and the price tag.
**Implementation notes:** adapts Figure 13.1. Keep `Memory` color semantics: OS slice red, program blue.

### S04 — Sharing the machine   (beats: B03) · ~0:50
**Purpose:** multiprogramming: switch to another program when one waits on I/O, so the CPU stays busy.
**Starts with:** S03 end state.
**Layout:** the column and price tag fade. A CPU at center (0, 1.0) scale 1. A ready Queue "Ready" at (0, −0.9) holding B and C. A blocked tray at the right (3.2, −0.9) with a clock.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "So people started to share. First came **multiprogramming**." | The column and tag `FadeOut`. Term note *multiprogramming* (slides into the dock, no veil). After the dock, the CPU chip grows at center with A standing on it (running). |
| 2 | "Several programs are ready to run at the same time," | Queue "Ready" draws with B and C (ready outline) below the CPU. |
| 3 | "and when one stops to wait for an I/O, the OS switches to another." | A turns `blocked` and `hop_to`s the tray at the right, a clock spinning; B hops onto the CPU (running). A small `KernelToken` pulses on the chip during the swap. |
| 4 | "The CPU stays busy. Utilization goes up." | The CPU is lit solid yellow; a small gauge (`SpeedGauge`) beside it rises to full. |
| 5 | "You remember this from the ready queue and the blocked state:" | The state diagram's colors flash briefly on the Queue and the tray (the labels "ready", "blocked" fade in small, then out). |
| 6 | "the same trick that helps the CPU is about to cause trouble for memory." | Student → confused, "?" over his head. A small `Memory` column fades in at the left with a "?" in it and blinks (a foreshadow). Hold 0.5 s. |

**Characters:** Student (curious → confused), Professor (explaining).
**Ends with:** CPU with B running, A in the blocked tray, C waiting, a faint "?" memory column at the left, term strip *multiprogramming*.
**Implementation notes:** reuse 04's Queue and blocked clock exactly. The faint column is `make_translucent`; it is replaced in S05.

### S05 — Time sharing   (beats: B04, first half) · ~0:35
**Purpose:** *time sharing* = interactivity; each user wants a timely answer.
**Starts with:** S04 end state.
**Layout:** center: a "batch" mini-timeline (long) on the left and a "live" desk at the right. Remove everything first.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Then people wanted more. Programmers were tired of waiting hours between debug cycles." | The scene `FadeOut`s, except the Section badge. A long thin Timeline strip at (−1.5, 1.0) with a single clock sweeping very slowly, label "hours". |
| 2 | "They wanted to sit at the machine and get an answer *now*." | The strip shrinks to a tick; a `desktop` icon at (2.8, 0.4) with a small prompt "> run" and an answer "ok" popping up immediately. |
| 3 | "This is **time sharing**:" | Term note *time sharing* (slides into the dock, no veil). |
| 4 | "many users, each wanting an interactive, timely response." | Three small desks (A coral, B mint, C gold) in a row at (−2.4, 0.4), (0, 0.4), (2.4, 0.4) each with a tiny chat bubble "ok" lighting up in turn. A thin shared CPU chip at the bottom-center (0, −1.2) is connected to all three. Student → curious. |

**Characters:** Student (curious), Professor (neutral).
**Ends with:** three desks (A, B, C) feeding one CPU; strip *time sharing*.
**Implementation notes:** desks use the `desktop` icon from `ov_icons`, tinted by process color. Keep text ≤ 8 words on screen.

### S06 — The slow way   (beats: B04, second half) · ~0:40
**Purpose:** naive time sharing by swapping all of memory to disk, and why it is brutally slow.
**Starts with:** S05 end state.
**Layout:** physical Memory (width 2.0, 4.4 tall, no regions, 6 equal cells) at (−3.0, 0.1); a CPU at (0.6, 1.3) scale 0.8; a Disk at (3.4, −0.3). Save slot icon between CPU and memory.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "So run one program for a while, then switch to the next one. We already know how to switch the CPU. What's the catch?" | Desks fade; the Memory column, CPU and Disk appear. All memory cells are filled with A's coral. A is running on the CPU. Student's "?" above. |
| 2 | "Memory. A program expects all of memory to itself." | Professor → explaining. A glow runs through every cell of the column ("all of it"). |
| 3 | "So here is the naive way: stop A, copy *everything* in memory out to the disk," | A → `ready`. The cells peel off and stream down in a column of blocks into the Disk, one after another (`LaggedStart`, ~2 s). The Disk spins. |
| 4 | "load B from the disk, run B for a while, and so on." | The Disk's mint blocks stream back up into the cells (B's color); B hops onto the CPU. |
| 5 | "Saving the registers is quick: a few numbers." | The `save_slot` icon flicks out of the CPU with 3 tiny colored registers and returns almost instantly (0.3 s). A "fast" check (`tick_mark`) glows beside it. |
| 6 | "But saving all of memory to disk is brutally slow, and the bigger memory grows, the worse it gets." | The cell column grows taller (scale ×1.2); the block stream is replayed visibly slower with a clock spinning. A red `x_mark` flashes by the Disk. |
| 7 | "The CPU sits idle while the disk grinds." | The CPU turns grey with a hatch overlay (idle encoding) and a "zZz" glyph; the Disk's platter spins. Student → frustrated. |
| 8 | "That's awful. Just leave them there!" | Student's bubble: **"Leave them there!"** (3 words). Pause 0.5 s. |

**Characters:** Student (curious → frustrated), Professor (explaining).
**Ends with:** CPU idle (hatched), Memory column half in A's color / half in B's, Disk, red mark; no new text.
**Implementation notes:** timing rule: the "fast" and "slow" visuals must contrast: registers 0.3 s vs memory 3 s. Use `Memory.fill_cell` with `LaggedStart`.

### S07 — Everyone stays in memory   (beats: B05, first half) · ~0:35
**Purpose:** Figure 13.2: processes stay in memory together; the CPU runs one and the others wait.
**Starts with:** S06 end state.
**Layout:** Disk and CPU idle state fade. **PHYS512** physical column at (−3.4, 0.1), 2.0 wide, addresses at the left. CPU at (2.6, 1.2) scale 0.8 with A running; Ready queue at (2.6, −0.8) with B, C.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Leave the processes in memory and switch between them there." | Professor → happy. The disk fades; the column's cells re-shuffle into the Figure 13.2 layout. |
| 2 | "Here's the book's picture of a 512-kilobyte machine." | Address labels write in: "0KB" ... "512KB" down the left. "512KB" is highlighted at the bottom. |
| 3 | "The OS at the top." | Top slice fills `KERNEL_COLOR` "OS"; the `KernelToken` pulses on it. |
| 4 | "Then three processes, A, B and C, each with a small slice carved out for it." | C's slice (128–192) fills gold, B's (192–256) mint, A's (320–384) coral, each with its letter; the free slices stay hatched. Three Process creatures appear in the right half, each a thin colored line to its slice. |
| 5 | "One CPU, so one runs while the other two wait in the ready queue." | A on the CPU (running); B and C in the Ready queue (outline). A thin marker "now" on A's slice. |
| 6 | "Switching is fast again." | A and B swap (`hop_to`); the "now" marker jumps to B's slice instantly. Quick green tick. |

**Characters:** Professor (happy), Student (neutral → curious).
**Ends with:** PHYS512 with OS, C, B, A; CPU with B running, A and C in the queue.
**Implementation notes:** adapt Figure 13.2 exactly (slice positions in the layout line). The "now" marker is a small arrow ◄ built from a `Triangle`.

### S08 — Protection   (beats: B05, second half) · ~0:35
**Purpose:** feel the new problem: nothing stops B from overwriting A; name it **protection**.
**Starts with:** S07 end state.
**Layout:** unchanged, but the CPU/queue are dimmed to 30%. The viewer's eyes stay on PHYS512.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "But now there's a new problem." | Dim the CPU/queue; Student → confused. |
| 2 | "Wait. If we all live in one memory, what stops B from just reaching over and scribbling on A?" | B (mint process on the right) shoots a mint arrow that bends into A's coral slice and leaves scribble marks (`Squiggle`s) in it; A's slice flickers coral → mint. A (Process) → `zombie`. |
| 3 | "Nothing. Yet." | Professor → worried. Everything holds one beat; a red "?!" glyph over A. |
| 4 | "That's called a **protection** problem." | Term note *protection* (slides into the dock, no veil). |
| 5 | "You do not want a process to read another's memory, or worse, write to it. Or to touch the OS's own memory." | Two arrows: B → A's slice (labeled "read", then "write", the second in red), and B → OS slice. Both get a red `x_mark`. A `Padlock` (closed, red) snaps around A's slice and then around the OS slice. Pause 1 s. |

**Characters:** Student (confused), Professor (worried).
**Ends with:** PHYS512 with A and OS padlocked, scribble residue faded, term strip *protection*.
**Implementation notes:** the scribble is a short `Polyline` zigzag in B's color on A's slice; fade it out at the end. One Padlock design (`p07_*`).

### S09 — An easy-to-use picture   (beats: B06) · ~1:00
**Purpose:** introduce the **address space** as a private, easy picture of memory, and build the 16KB example's code region.
**Starts with:** S08 end state.
**Layout:** PHYS512 slides to the right half and shrinks to scale 0.5 at (4.3, 0.2) (still visible, dimmed to 40%). The new **AS16** column (the virtual column) grows at center-left (−1.4, 0.2), 1.6 wide, 4.4 tall.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "So the OS needs a better idea. Not raw memory, but an *easy-to-use picture* of memory, one for each program." | PHYS512 shrinks away. A single translucent copy of a column (`make_translucent`) appears floating above each of the three process creatures (A, B, C) in the right half: three private columns, small. |
| 2 | "We call this abstraction the **address space**." | Term unveil *address space*. The three small columns merge into one, which glides to center-left and grows to the full AS16 column (empty cells, addresses "0KB" ... "16KB" writing in). |
| 3 | "It is the running program's view of memory in the system, and understanding it is the key to understanding how memory is virtualized." | A coral eye icon (Process A looking at the column) + the label "A's view" under the column (DIM, small). Pause 1 s. |
| 4 | "What's in it? Everything the program needs. The **code**:" | Student → curious. The top region of AS16 is highlighted ("code") and a mini instruction list (3 grey lines) writes in beside it. |
| 5 | "the instructions have to live in memory somewhere." | The instruction lines drop into the top region (`Transform` into the region's cell). The label "code" stays. |
| 6 | "And two more things we'll get to in a second." | Two faint dashed ghost regions (heap, stack) pulse with "?" under the free region; Professor → explaining. |
| 7 | "Let's use a tiny example. Sixteen kilobytes of address space." | Addresses highlight "0KB" and "16KB"; a bracket (`Brace`) with the label "16KB" on the right of the column. |
| 8 | "The book uses tiny examples because the math is easier." | A tiny label "tiny on purpose" (DIM) fades in beside the column, then out. |
| 9 | "The code sits at the top, starting at address zero and packed into the first kilobyte. Code is static, so we know it won't need any more room." | The code region fills `MEM_COLOR` from 0 to 1KB (bracket "1KB" on the left); a small "static" tag with a lock (`Padlock` open→closed) appears; Student nods. |

**Characters:** Student (curious), Professor (explaining).
**Ends with:** AS16 column with only the code region filled, ghost heap/stack hints, term strip *address space*.
**Implementation notes:** Figure 13.3 adapted. Remove the word "view" labels before S10 writes new labels (fade "A's view" and "tiny on purpose" at the end of the scene). Row 8's label never exceeds 3 words.

### S10 — Stack and heap   (beats: B07, first half) · ~0:45
**Purpose:** what the stack and the heap are, one at a time.
**Starts with:** S09 end state.
**Layout:** AS16 stays at center-left (−1.4, 0.2). A mini C panel (`Code`, font 16, 4.2 wide) at the right (3.2, 0.9). Characters in corners.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "You said two more things." | Student → curious (look at the column). Ghost regions pulse. |
| 2 | "The **stack** keeps track of where the program is in the function call chain." | Term note *stack* (slides into the dock, no veil). The bottom region (15KB–16KB) of AS16 fills a darker `MEM_COLOR` with label "stack". On the code panel `f(){ g(); }` the highlight bar walks f → g. |
| 3 | "It holds local variables, arguments, and return values," | Three tiny cards ("x", "arg", "ret") drop into the stack region as stacked frames. |
| 4 | "and it grows and shrinks as functions call and return." | When `g()` returns, one frame pops out (`FadeOut` + shift down), then a new one pushes. |
| 5 | "The **heap** is for dynamically allocated memory:" | Term note *heap* (slides into the dock, no veil). The region just under the code (1KB–2KB) fills lighter `MEM_COLOR`, label "heap". |
| 6 | "what you get from `malloc()` in C, or `new` in C++ or Java." | The code panel shows `p = malloc(100);` (highlight bar); a small block (the allocation, tinted) slides into the heap region labeled "p". |
| 7 | "The program asks for it, the program is responsible for it." | The block gets a tiny "you!" hand-pointer: `hand` icon pointing to it. Student → neutral. |

**Characters:** Student (curious → neutral), Professor (explaining).
**Ends with:** AS16 with code (top, 0–1KB), heap (1–2KB), free (hatched), stack (15–16KB) and the code panel; term strip *heap*.
**Implementation notes:** frames of the stack are 0.35-high rounded rectangles clipped to the stack region. The call chain `f → g` code is 3 lines (`void f(){ g(); }`, `void g(){ int x; }`, `main`). Fade the old region labels' "?" ghosts before filling.

### S11 — Opposite ends   (beats: B07, second half) · ~0:45
**Purpose:** why heap and stack sit at opposite ends and grow toward each other; honest caveats.
**Starts with:** S10 end state.
**Layout:** code panel fades. AS16 slides to center (0, 0.2) and the free region's DIM hatching shows the shared space. Two arrows: one under the heap pointing down (↓, `MEM_COLOR` light), one above the stack pointing up (↑, `MEM_COLOR` dark).

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Both of these grow and shrink while the program runs, so where do we put them?" | Code panel `FadeOut`; AS16 centers. Student → curious. Two "?" glyphs hover above the heap and stack. |
| 2 | "At opposite ends." | The two arrows draw: down from the heap's bottom edge, up from the stack's top edge. |
| 3 | "The heap starts just after the code, at one kilobyte, and grows down." | The heap region extends downward by two steps (each 0.3, a small `malloc` bubble per step); a "1KB" tick on its top edge. |
| 4 | "The stack starts at the bottom, at sixteen kilobytes, and grows up." | The stack region extends upward by two steps; a "16KB" tick at its base. |
| 5 | "Each has room to grow, and the free space in the middle is shared." | A double-headed arrow across the hatched free region, with a tiny "(free)" label; both regions shrink back to starting size (`Transform`). |
| 6 | "One honest note. This layout is a convention." | Professor → worried. The arrows blink; a small `AsideCard` slides in from the right: "A convention" (title "NOTE"). |
| 7 | "You could arrange things differently, and when we get to threads, several stacks will have to share one address space, so this neat picture will stop working." | The card's body shows two extra stack slabs jammed into the free region with a red `x_mark` ("threads: later", tiny `ep_tag("→ Ep. 26")`). |
| 8 | "And real programs hold other things too, like statically initialized variables. We're ignoring those for now." | The card text swaps to "…and more (ignored)"; the card `slide_out`s. Pause 1 s. |

**Characters:** Student (curious), Professor (explaining → worried → explaining).
**Ends with:** the final AS16 column, centered at (0, 0.2), with code, heap, stack, free, the growth arrows, and the addresses.
**Implementation notes:** this is the canonical AS16 pose that later episodes reuse. Fade the card's old text before the new row 8 text lands (same slot).

### S12 — The lie   (beats: B08) · ~1:10
**Purpose:** show that the private column is not where the program really lives; pose the crux.
**Starts with:** S11 end state.
**Layout:** AS16 shifts to the left third (−4.0, 0.2) and shrinks (scale 0.8). PHYS512 comes back at the right (3.3, 0.1). Characters in corners.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Now the twist. When we describe this address space, we are describing an *abstraction*." | Student → curious. AS16 slides left, shrinks; a label "A's address space" (DIM, below the column, coral) writes in. |
| 2 | "The program is not really in memory at addresses zero through sixteen kilobytes." | The "0KB…16KB" labels flash; a red dashed `x_mark` hovers over the row "0KB" ("not here"). |
| 3 | "It's loaded at some arbitrary physical address." | PHYS512 `FadeIn`s on the right with all processes (OS, C, B, A) in place. |
| 4 | "Look at the 512-kilobyte machine again. Process A is not at zero. It sits at three hundred and twenty kilobytes." | A's 64KB slice pulses coral; the address label "320KB" is circled (`Circumscribe`). Then a translucent copy of the AS16 column lifts off the left column, shrinks (to the slice's size) and **lands on A's slice** at 320KB (`PacketFly`-style arc, 1.5 s). |
| 5 | "B and C are elsewhere. And yet every one of them believes its own memory starts at zero." | Two other translucent copies (mint and gold) land on B's and C's slices. Above each slice a little "0" tag appears in the process color (three "0" tags at different heights). Student's thought bubble: **"0?"**. Pause 1 s. |
| 6 | (pause 0.5 s) | Everything `FadeOut` except the badge. |
| 7 | "THE CRUX: How can the OS build this abstraction of a private, potentially large address space for multiple running processes (all sharing memory) on top of a single, physical memory?" | `CruxCard` (accent `VIRT`, question as written) `.write()` at center, hold 3 s, then `.dock()` to the strip at y = 3.0 (the question trimmed to the strip). Professor → thinking. |
| 8 | (hold) | The diagram returns under the strip: AS16 (left, scale 0.8) and PHYS512 (right) with the landed copies, as at the end of row 5. |

**Characters:** Student (curious → confused), Professor (explaining → thinking).
**Ends with:** crux strip docked at y = 3.0; AS16 at left, PHYS512 at right with A, B and C copies landed; "0" tags fade out.
**Implementation notes:** the central image of the series' memory arc: a *translucent copy that flies*. `make_translucent` copy of AS16, `Succession(MoveAlongArc, ScaleToFit)`. For the crux card, remember the strip must be ≤ 8.2 wide: pass the book's wording through `CruxCard` (it docks with font 24). Crux text here is a verbatim of the book. Row 7 narration is spoken once; the card appears under the Professor's line, not separately.

### S13 — A virtual address   (beats: B09, first half) · ~0:45
**Purpose:** a load from address 0 is a **virtual address**; the data really sits at 320KB.
**Starts with:** S12 end state (the A copy stays; B and C copies fade first).
**Layout:** A's AS16 at left (−4.0, 0.2); PHYS512 at right (3.3, 0.1); a CPU chip at the center (0, 1.4) scale 0.7 with A running. A small `Code` line `load 0` (MONO, font 22) above A's column.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Here is what that means in practice. Process A runs a load from address zero." | B and C's copies fade. The `Code` line "load 0" appears next to the CPU; a coral arrow leaves the CPU and enters the "0KB" row of A's column; the cell glows. |
| 2 | "We call this a **virtual address**." | Term unveil *virtual address*. The arrow's head carries a small tag "virtual 0" (coral, MONO). |
| 3 | "It is what the program sees." | The eye icon + "A sees: 0" highlight under the column. |
| 4 | "But the data isn't at physical address zero. That's where the OS lives." | The arrow continues across the center toward PHYS512's top (0KB) and bounces off the red OS slice with a small "no!" shake (`x_mark`; Student → confused). |
| 5 | "The OS, together with some help from the hardware, makes sure the load goes to physical address three hundred and twenty kilobytes, where A really is." | A `KernelToken` and a small gear (`GearPair`, scale 0.4) appear at the middle of the arrow; the arrow bends smoothly down and lands on A's slice at 320KB, the cell glows coral; a "physical 320KB" tag appears (MONO, DIM). Pause 1 s. |

**Characters:** Student (curious → confused), Professor (explaining).
**Ends with:** the bent arrow from virtual 0 to physical 320KB with the OS+hardware badge; term strip *virtual address*.
**Implementation notes:** the bend is a `CubicBezier` path drawn in two segments (so the arrow can bounce, then reroute). Translation is only *hinted* (gear, badge); the mechanism is 15's job. Fade "load 0" and the eye label at the end of the scene.

### S14 — Virtualizing memory   (beats: B09, second half) · ~0:35
**Purpose:** name it, tie it to the peach and the two `mem` programs.
**Starts with:** S13 end state.
**Layout:** arrow and badge stay. The **Illusion split** is *not* used (the picture is the split already). Callback props at the bottom center.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "When the OS does this, we say it is **virtualizing memory**." | Term unveil *virtualizing memory*. |
| 2 | "The program thinks it is loaded at a particular address, with a potentially huge space." | A's column grows taller and fades at the bottom (a "..." tail) to hint "huge"; a thought bubble over A: a cloud with a tall column. |
| 3 | "The reality is quite different. This is the key to every modern computer system." | The thought bubble pops; the real, small slice on PHYS512 pulses coral. Professor → proud. |
| 4 | "Same trick as the peach! One real thing, many pretend ones." | Student → excited, bubble **"Peach!"**. A small `Peach` (scale 0.5) hops between the two columns; three translucent `virtual_copy` peaches appear above A, B, C's columns, one real peach below. |
| 5 | "And the same as the two `mem` programs that both printed `0x200000`: same address, different bytes underneath. Remember that one?" | The peaches fade. Two mini terminal lines at the bottom (MONO, 20): "PID 24113: 0x200000", "PID 24114: 0x200000". Each line's arrow points to a different slice on PHYS512 (coral and mint). Pause 1 s. |

**Characters:** Student (excited), Professor (proud).
**Ends with:** the two-column picture, bent arrow; all callbacks faded; term strip *virtualizing memory*.
**Implementation notes:** peaches via `Peach.virtual_copy`. The `mem` terminal lines are `Text` in `MONO_FONT`, not a full Terminal.

### S15 — Transparency   (beats: B10) · ~0:50
**Purpose:** goal one: the program must not notice the virtualization.
**Starts with:** S14 end state.
**Layout:** everything fades, leaving the crux strip and badge. Center: Process A (scale 1.0) at (−2.6, 0.3), a `glass_pane` (a faint vertical pane) at (−0.8, 0.3), and the physical column at the right (2.6, 0.2) scale 0.7. Goals list slot: three icon dots at the bottom, y = −1.6, x = −1.2, 0, 1.2 (empty rings).

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "So the OS now has a job: virtualize memory, and do it with style. To keep it honest, it needs goals." | The scene clears (`FadeOut`). Three empty rings (goal slots) draw at the bottom: "1", "2", "3". |
| 2 | "The first is **transparency**." | Term note *transparency* (slides into the dock, no veil). Ring 1 fills `VIRT`. |
| 3 | "The virtualization should be invisible to the running program." | A (running) faces a wall of columns; a glass pane between A and the machinery becomes more and more transparent (opacity 0.5 → 0.05). |
| 4 | "The program shouldn't know that memory is virtualized. It should behave as if it has its own private physical memory." | A's thought bubble holds a tidy full column labeled "mine". Behind the pane, the physical column with A, B, C slices stays visible to the viewer only. |
| 5 | "Behind the scenes, the OS and the hardware do all the work of multiplexing memory among many jobs, and that implements the illusion." | `KernelToken` and `GearPair` appear behind the pane at the physical column; the three slices swap places and are re-mapped (small arrows), A doesn't react. |
| 6 | "Invisible? I thought \"transparent\" meant you can see everything." | Student → confused. |
| 7 | "In everyday speech, yes. Here it's the opposite: the illusion must not be *visible* to the program." | Professor → explaining. An `AsideCard` ("ASIDE", body "transparent = unseen") slides in at the right (x = 4.2, y = 0.4); a small eye icon with a slash appears. |
| 8 | "A transparent window; you don't see the glass." | The aside slides out; the pane flashes, then disappears altogether (`FadeOut`). Pause 1 s. |

**Characters:** Student (confused), Professor (explaining).
**Ends with:** A with its thought-bubble column; machinery at right; goal ring 1 filled; term strip *transparency*.
**Implementation notes:** `glass_pane` from `p05_icons`. Fade the aside before row 8 text lands in the same area; keep aside body ≤ 4 words.

### S16 — Efficiency   (beats: B11, first half) · ~0:35
**Purpose:** goal two: fast (time) and small (space), with hardware help.
**Starts with:** S15 end state.
**Layout:** A and pane fade. Left (−2.6, 0.5): a `SpeedGauge`. Right (2.4, 0.5): a small column plus a "bookkeeping" side tab. Goal ring 2 at bottom.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Goal two: **efficiency**." | Term note *efficiency* (slides into the dock, no veil). Ring 2 fills `VIRT`. |
| 2 | "Virtualization should be as fast as possible: not making programs run much slower." | The `SpeedGauge` appears; the needle drops to a slow value and then rises to "fast" (a green mark). A small snail (stopwatch + `x_mark`) for the slow case flashes. |
| 3 | "And as small as possible: not using too much memory for the structures that make virtualization work." | A Memory column appears at right with a thin tab on its side labeled "tables"; the tab swells and eats the column, then is trimmed back to a sliver. A green tick. |
| 4 | "To be fast, the OS will lean on hardware, including something called a TLB. We'll get there." | A chip icon (CPU scale 0.5) lights up beside the gauge with the tag "hardware"; a tiny `ep_tag("→ Ep. 19")`. Student → curious; Professor → happy. |

**Characters:** Student (curious), Professor (happy).
**Ends with:** the gauge, the sliver-tab column, hardware chip, rings 1 and 2 filled; term strip *efficiency*.
**Implementation notes:** `SpeedGauge` from `p04_icons`. The TLB is not named on screen except in the `ep_tag`; do not show the TLB diagram.

### S17 — Protection and isolation   (beats: B11, second half) · ~0:45
**Purpose:** goal three, protection (callback to S08), and the Isolation principle.
**Starts with:** S16 end state.
**Layout:** gauge and column fade. Center (0, 0.4): three cocoons (rounded rects, A coral, B mint, C gold) each holding a small private column. A `KERNEL_COLOR` OS block under them. Ring 3 at the bottom.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Goal three is where we started: protection." | Ring 3 fills `VIRT`. The padlock from S08 returns for a moment as a callback (small, red). |
| 2 | "The OS must protect processes from each other, and itself from them." | The three cocoons draw (one around each private column); the OS block below gets its own cocoon. |
| 3 | "When a process does a load, a store, or an instruction fetch, it must not be able to touch anything outside its own address space." | B's arrow (load / store / fetch labels cycle) tries to leave its cocoon toward A's and the OS's; each attempt bounces back off the cocoon wall with a spark; a `ShieldGate`-style shake. |
| 4 | "That gives us a principle we'll use all through the book: **isolation**." | Term note *isolation* (slides into the dock, no veil). |
| 5 | "If two things are properly isolated, one can fail without hurting the other." | B's cocoon goes red (B → `zombie`, a crash glyph); A and C stay untouched, their cocoons calm green rings. A TipCard ("THE PRINCIPLE OF ISOLATION", body "One can fail. The other doesn't.") slides in from the right. |
| 6 | "Each process should run in its own little cocoon, safe from faulty or malicious neighbors." | The tip card slides out; the three cocoons pulse once together. Student → excited (a short nod); Professor → proud. |

**Characters:** Student (curious → excited), Professor (explaining → proud).
**Ends with:** three cocoons (B's repaired), rings 1, 2, 3 filled; term strip *isolation*.
**Implementation notes:** microkernels are cut (see script). The tip card body is ≤ 8 words. Fade the callback padlock before the cocoons draw.

### S18 — Every address is virtual   (beats: B12) · ~1:00
**Purpose:** payoff of the cold open: the three printed addresses live in the *virtual* column; "if you can print it, it's virtual".
**Starts with:** S17 end state.
**Layout:** everything fades but the badge and strip. Left (−3.6, 0.3): the Terminal from S01 with the three lines (scaled to 0.7). Right (2.6, 0.2): a **tall virtual column** (AS16 canonical look, scale 1.0), top label "0x0" (code is near 0 in the picture), bottom label "the far end".

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Back to the program from the start. Here are the three addresses it printed on a 64-bit Mac." | The terminal returns with the three lines (MONO). The virtual column draws at right, its regions already labeled (code / heap / stack). |
| 2 | "Code: `0x1095afe50`." | The first line highlights; an arrow arcs from it to the code region (top of the column); a pin lands. |
| 3 | "Heap: `0x1096008c0`." | Second line highlights; an arrow to the heap region, just under the code; pin. |
| 4 | "Stack: `0x7fff691aea64`." | Third line highlights; its arrow travels far down to the stack, the very bottom; pin. |
| 5 | "Look at the order. Code comes first. Then the heap. And the stack is all the way at the other end of this big virtual space, just like our picture." | The three pins light in order (1, 2, 3); a zig-zag on the long arrow to the stack, showing the big gap. Student → excited. |
| 6 | "And now you know the twist. All of them are virtual addresses." | The "FICTION"/stamp from S01 returns as a stamp reading "VIRTUAL" on each terminal line, one after another (0.3 s apart); the cracks from S01 do not return. |
| 7 | "If you can print it, it's virtual." | Professor → proud. The terminal lines gain the tag "virtual" (`USER_COLOR`). |
| 8 | "Only the OS, with the hardware, knows where the bytes really are. So never forget: an address your program shows you is an illusion of how things are laid out in memory." | A shy PHYS512 (scale 0.5, 30% opacity) fades in at the lower right with the OS badge on it, and "the OS knows" label; an `AsideCard` ("ASIDE", body "Every address you see is virtual") slides in at the left and out. Pause 1 s. |

**Characters:** Student (excited), Professor (proud).
**Ends with:** terminal (three tagged lines) and the virtual column with three pins; faint physical column; term strip *isolation* is replaced by nothing (clear it).
**Implementation notes:** the same addresses as S01 (copy exactly). Fade the S01-style stamp before the aside enters. Call `terms.clear()` at the end of the scene so the recap is clean.

### S19 — Recap   (beats: B13) · ~0:30
**Purpose:** five takeaways as one list.
**Starts with:** S18 end state.
**Layout:** the stage clears. A numbered list at left (−5.4 .. 1.0), font 30; one icon per line at x = 4.0 (y = 1.8, 0.8, −0.2, −1.2, −2.2), clear of the corner characters (x = ±5.8). Characters look at the list.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "What do we carry out of this episode?" | Everything `FadeOut`. Header "The address space" in `VIRT`, font 34, `Write` at (−3.4, 2.4) (inside the content zone, y ≤ 2.55). |
| 2 | "One: early machines had one program in memory, and nothing to hide." | Line 1 `Write`s: "1. One program, no illusions". Icon: the early column (OS + program). |
| 3 | "Two: sharing memory made protection a problem." | Line 2: "2. Sharing needs protection". Icon: red padlock. |
| 4 | "Three: the OS's answer is the address space, a private, easy picture of memory, with code, heap and stack." | Line 3: "3. Address space: code, heap, stack". Icon: AS16 mini. |
| 5 | "Four: virtualizing memory means a virtual address is not a physical one." | Line 4: "4. Virtual is not physical". Icon: the bent arrow 0 → 320KB. |
| 6 | "Five: the goals are transparency, efficiency, and protection." | Line 5: "5. Transparent, efficient, protected". Icon: three filled rings. Hold 1.5 s. |

**Characters:** both neutral, looking at the list.
**Ends with:** full recap list and five icons; badge fades.
**Implementation notes:** same layout as 04's S21 and 11's S09. Total text ≈ 22 words including header; each line ≤ 6 words.

### S20 — Teaser   (beats: B14) · ~0:25
**Purpose:** hook into 14: how a program *asks* for memory.
**Starts with:** S19 end state.
**Layout:** characters to dialogue mode (Student (−2.6, −1.2), Professor (2.6, −1.2) flipped). AS16 canonical column center-top (0, 1.2) scale 0.7.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "So my program thinks it has a big private memory. But how does it *ask* for more? Where does `malloc()` get it?" | The recap `FadeOut`s. Characters glide to dialogue mode. AS16 `FadeIn` with the heap region; Student → curious; a bubble: **"malloc(?)"** above his head. |
| 2 | "That's the next question. How a program talks to this memory: `malloc()` and `free()`, and the mistakes that come with them." | Professor → happy. The heap grows (`malloc`), then one block flashes and a small bug glyph (a red "!" ) hops out of it. |
| 3 | "And after that, the real trick: how a virtual address becomes a physical one." | The bent arrow 0 → 320KB from S13 draws faintly across the column to a tiny PHYS512 at the right (30% opacity). |
| 4 | (end card) | `FadeOut` everything (0.5 s). End card: "Next: 14 · Memory API" in `TEXT` with a `VIRT` dot (`ep_tag` style). Hold 2 s. |

**Characters:** Student (curious), Professor (happy).
**Ends with:** end card.
**Implementation notes:** the end card must match episode 14's slug. The bug glyph is just a small red "!" in a circle (`x_mark` style), no new asset.

## New assets needed
- **`ostep_lib/props/p13_addrspace.py`** (auto-imported; canonical shared asset for 13, 14 and 15; the single owner of the memory-arc column look so 14 and 15 reuse it):
  - `address_space_16kb(owner_color=None, title=None, scale=1.0)`: the canonical AS16 `Memory` (regions code / heap / (free, weight 6) / stack, addresses "0KB","1KB","2KB","15KB","16KB"), with a zigzag "not to scale" break mark on the free region and `hatch_rect` hatching; `.grow_heap(k)`, `.grow_stack(k)` animations (the heap region extends downward, the stack upward, free shrinks); `.region_arrows()` (the two growth arrows); `.set_owner(color)` for the process-color outline.
  - `physical_512kb(layout=None)`: the Figure 13.2 `Memory` (slices OS / free / C / B / free / A / free), `.slice_of("A")` returning the A slice center, `.land(copy, name)` (a translucent AS16 copy flies and lands on a slice).
  - `memory_copy_fly(source_column, target_slice, run_time=1.5)`: the arc + shrink animation of S12 (a `Succession` of `ShiftAlongArc` and `ScaleToFit`), reused by 15.
- **`stamp(text, color, angle)`** helper (rounded rect + rotated text). Local to the scene file is fine; used in S01 and S18.
- **`cocoon(content, color)`** helper: a rounded rect around a small column with a glossy ring (S17). Local to the scene file.
- No new character expressions are needed.
- Existing props verified: `glass_pane`, `SpeedGauge` (`p05_icons`, `p04_icons`), `Padlock`, `Peach`, `Terminal`, `Queue`, `Memory`, `hatch_rect`.

## Open questions
- **Crux placement:** S12 puts the crux after the protection / address-space setup, as in the book. Alternatively, a one-line crux card could follow the cold open. Keep the book's order?
- **AS16 is not to scale** (free region compressed to 6 weight units). Is a visible "break" mark enough, or should the free region be drawn at its true 13KB height (code and stack would be thin, ~0.27 each)?
- **S18 stack address** (`0x7fff691aea64`) is much larger than the heap's. In the drawing the stack sits at "the far end"; I do not draw a numeric axis. OK?
- **Student "worried"** does not exist, so S13 row 4 uses `confused`. Same workaround as the script.
- **Term count:** eleven term highlights in 11 minutes. If that feels heavy, *stack* and *heap* could share one highlight, and *transparency/efficiency* could be written in the goal rings instead.
- **Episode 12** (dialogue) was not available when this was written; callbacks to it are limited to the overview (01-03) peach and `mem` examples. Please check the 12 script for any overlap in the cold open.
