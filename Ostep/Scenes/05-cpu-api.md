# 05 — Interlude: Process API · Scene breakdown
> Script: Ostep/Scripts/05-cpu-api.md · Scenes: 18 · Est. duration: ~14:00

## Visual overview
- **Core metaphor: a process is a creature with a "world" attached** (its address space, registers and PCB card, the freeze-frame panels from episode 04). `fork()` is **cell division**: the whole world duplicates and a second creature appears. `exec()` is **swapping the program inside the same creature**: the memory regions are wiped and refilled while the creature and its PID tag stay. `wait()` is the parent turning blocked (clock) until the child is collected.
- **Second metaphor: the Code block with two highlight bars** (one per process, in the process colors). Both bars sit on the same line after `fork()`, then split at the `if`. This is the picture of "same code, different world".
- **Third: the file-descriptor plugs** (0 stdin, 1 stdout, 2 stderr, from 04 S12). Redirection is *cutting cable 1 and plugging a file into slot 1*, before `exec()`. The plugs survive the `exec()` swap.
- The shell is a **loop diagram** (prompt → fork → exec / wait → prompt) with a highlighted **gap** between `fork` and `exec`. The gap becomes a "workshop" where the child's world is rearranged.
- Closing device: the **Process API menu card** from 04 returns (S16) and each row gets its UNIX call.
- Props used (from the bible and `ostep_lib`): Crux card, Aside/Tip card, Term highlight, Section badge, CPU, Memory, Disk, Timeline, Queue, State diagram (legend mode), PCB card, RegisterBank, User/Kernel boundary, Privilege gauge, Terminal, Code block, Spotlight, MenuCard, plug / keyboard / file / pause / play / puff / info tag / mini clock / x_mark / tick_mark / name_tag / padlock / pipe_glyph / book / desktop icons, `ep_tag`, `SpeedGauge`, whistle. Characters: Professor, Student, Process (Computer does not appear in this episode).

### Persistent assignments
| Thing | Look | Notes |
|---|---|---|
| **Parent** (PID 29146) | `Process(label="PID 29146", color=PROCESS_COLORS[0])` (coral) | Same color as Process A in 04. The same PIDs are used in every example (the book's outputs show different PIDs per run; we keep one pair so viewers can track them). |
| **Child** (PID 29147) | `PROCESS_COLORS[1]` (mint) | Also the child of the shell in S09–S11. |
| **Shell** `sh` | `PROCESS_COLORS[2]` (gold), label "sh" | S09–S11 only. |
| **grep / wc in the pipe** | `PROCESS_COLORS[3]` (sky) / `[4]` | S11 only. |
| **Programs** | A program is a small file icon with a label chip: `p1`/`p3` in `DIM`, `wc` in sky | The code region of a Memory column shows its program chip. |
| Section badge | Top-left (−6.6, 3.6): `VIRT` dot + "05 · Process API", font 22, `DIM` | Appears in S02, stays on until S17. |
| Term highlight | Two strengths. **Unveil** (`terms.show`: scrim, big term at center, then docks top-right) only for the key terms: `fork()`, non-deterministic, `exec()`, redirection, signal. **Note** (`terms.note`: slides straight into the top-right dock, no veil) for every other term: PID, parent, child, `wait()`, shell, pipe, user, superuser (root), man pages. | The dock is carried over between scenes (each scene starts with the previous docked term). |
| Characters (corner mode) | Student at (−5.8, −2.8), scale 0.75, facing right. Professor at (5.8, −2.8), scale 0.75, `flip()`. | Default. "Dialogue mode" (S18): Student (−2.6, −1.2), Professor (2.6, −1.2), scale 1. |
| Terminal | `Terminal` prop, `MONO_FONT`, prompt `prompt>` in `DIM` | The "what the user sees" window, reused in nearly every scene. |
| Code block `p1.c` (trimmed) | `Code`, monokai, font 20, 8 lines, at (−3.9, 0.5) when used | Error check omitted; caption "p1.c (error check omitted)" in `DIM`. |

Trimmed `p1.c` used throughout (line numbers used in the tables below):
```
1  printf("hello (pid:%d)\n", getpid());
2  int rc = fork();
3  if (rc == 0) {
4    printf("child (pid:%d)\n", getpid());
5  } else {
6    printf("parent of %d (pid:%d)\n",
7           rc, getpid());
8  }
```

## Scenes

### S01 — A program that talks to itself   (beats: B01) · ~0:45
**Purpose:** pose the puzzle: one `hello`, but both the `if` and the `else` branch ran. Pick up from 04's teaser.
**Starts with:** black (BG).
**Layout:** Code block (p1.c trimmed) left (−3.9, 0.5), caption under it. Terminal right (3.2, 0.7), 5 × 2.4. Characters in corner mode.

| # | Narration (exact words the action lands on) | On screen / animation |
|---|---|---|
| 1 | "Last time, we ended with a promise: a process that clones itself." | A single coral Process (ready, no label) at (0, 1.0) blinks, then splits into two identical copies (the 04 S22 "mitosis" squash). Both slide out of frame and fade. |
| 2 | "So let's see it. Here is a tiny C program." | Code block `Write`s in, line by line, at left. Caption "p1.c (error check omitted)". Student (curious) and Professor (neutral) `FadeIn` in the corners. |
| 3 | "It prints "hello"." | A highlight bar (neutral `TEXT` at 0.2 opacity) lands on line 1. |
| 4 | "Then it hits an `if` and an `else`." | The bar moves to line 3 (`if`). |
| 4b | "If this is the child process, the new one that fork creates, it prints child. If it's the parent process, the original one, it prints parent." | `Indicate` line 4 in mint (child), then line 6 in coral (parent). |
| 5 | "Let's run it." | Terminal `FadeIn`; `prompt> ./p1` types. Output prints one line every 0.5 s: `hello (pid:29146)`, `parent of 29147 (pid:29146)`, `child (pid:29147)`. |
| 6 | "Wait. "Hello" appeared once. But then *both* "child" and "parent" showed up. That's an `if` and an `else`. How can both of them run?" | Student → confused, a "?" above. Terminal lines 2 and 3 `Indicate` together; code lines 4 and 6 flash together with a "?" between them. |
| 7 | "Because after one particular line, there are two of the program." | Professor → happy. A ring `Circumscribe`s line 2 (`int rc = fork();`) in the code. |
| 8 | "Today we meet the three calls UNIX uses to make and manage processes." | Three call names write in a row at the top, `fork()` `exec()` `wait()`, in `MONO_FONT`, then fade. Hold 0.5 s. |

**Characters:** Student (curious → confused), Professor (neutral → happy).
**Ends with:** Code block + Terminal (3 lines) + both characters. Nothing else.
**Implementation notes:** reuse the mitosis helper from 04 S22 (see New assets: `clone_process`). Never show the `fork failed` branch; the caption says so.

### S02 — The Crux   (beats: B02) · ~0:25
**Purpose:** state the episode's question and link it to 04's menu.
**Starts with:** S01 end state.
**Layout:** Crux card centered (0, 0.3), 9 × 3; then shrinks to a strip at (0, 3.2).

| # | Narration | On screen / animation |
|---|---|---|
| 1 | (transition; spoken as the crux: "Which brings us to the question behind all of it: ...") | Code block and Terminal `FadeOut` while the crux writes. Section badge "05 · Process API" `FadeIn` top-left. Crux card (`VIRT` frame, "THE CRUX" header) writes the question in bold: **"How to create and control processes?"** |
| 2 | "This is an *interlude*. A short, practical episode about a real interface, with real code you can type in yourself." | Subtitle writes in smaller, `DIM`: "What interfaces should the OS present for process creation and control? How should they be designed for power, ease of use and high performance?" An **Aside card** "INTERLUDES" (≤8 words: "Practical things. Real code. Type it in.") slides in from the right and out again. |
| 3 | "In episode four, we listed what any OS must offer: create, destroy, wait, miscellaneous control, status." | The 04 **MenuCard** ("Process API", 5 rows) slides in at the left (−3.6, −0.8), scale 0.6; the five rows highlight in turn, 0.4 s each. |
| 4 | "Now we order from that menu, the UNIX way." | MenuCard fades. The Crux card shrinks to a one-line strip at the top-center (0, 3.2), "How to create and control processes?", font 24. |

**Characters:** corner mode; Student looks at the card, Professor neutral.
**Ends with:** section badge, crux strip, characters in corners. Nothing else.

### S03 — A name, and a call to the kernel   (beats: B03, first half) · ~0:35
**Purpose:** every process has a PID; `fork()` is a system call (crosses into the kernel).
**Starts with:** S02 end state.
**Layout:** CPU at (−2.0, 0.6) (1.4 × 1.4) with the coral parent standing on it. A single-line **Code card** at right (3.4, 1.8). A mini Terminal under it (3.4, 0.6), 4.6 × 0.9. The **User/Kernel boundary** at y = −0.8 appears mid-scene (user above, kernel below); a **Privilege gauge** at the far right (6.0, −0.8).

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "First, a name. Every process has an ID, a number the OS uses to refer to it." | The CPU `GrowFromCenter`; the coral parent (label "PID 29146") hops onto it, running. A `name_tag` icon pulses beside the label. |
| 2 | "It's the **process identifier**, or **PID**." | Term note "process identifier (PID)". |
| 3 | "Our program starts with PID 29146." | Code card writes `printf("hello (pid:%d)\n", getpid());`; the mini Terminal prints `hello (pid:29146)`. |
| 4 | "In UNIX, if you want to do something to a process, like stop it, the PID is how you name it." | A tag `stop 29146` with a pause glyph appears above the parent, an arrow pointing at its label; then fades (no action taken). |
| 5 | "Now the interesting part." | Code card adds line 2, `int rc = fork();`, with the highlight bar. Pause 0.5 s. |
| 6 | "The program calls **`fork()`**. It's a system call: a request to the OS, so it crosses into the kernel." | Term highlight "fork()". The boundary draws (dashed, `USER_COLOR` above, `KERNEL_COLOR` below) and the gauge shows USER. A small packet labeled `fork()` leaves the parent and crosses the line (`UserKernelBoundary.cross`); the gauge flips to KERNEL; the zone below flashes red at the crossing. |

**Characters:** corner mode; Student curious (looks at the PID tag), Professor explaining at row 6.
**Ends with:** parent on CPU at (−2.0, 0.6), boundary at y = −0.8 with the `fork()` packet in the kernel zone, gauge KERNEL, Code card (2 lines), mini Terminal "hello (pid:29146)".

### S04 — The cell divides   (beats: B03, second half) · ~0:50
**Purpose:** `fork()` creates an almost exact copy of the whole machine state; the child comes to life *inside* `fork()`, not at `main()`.
**Starts with:** S03 end state.
**Layout:** two "worlds", each = creature (top, y = 2.0) + **Memory** column (1.2 × 3.0, regions: code, static data, heap, stack) + **RegisterBank** (2 × 3, PC highlighted) + a small **PCB card** (pid field) + three tiny plugs "0 1 2" (open files). Parent world at left (x = −3.4), child world at right (x = 3.4). Center (0, 0.4) holds the term/label area. A one-line mini Terminal at bottom center (0, −2.5), 4 × 0.6.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "And what the OS does is create a new process." | Boundary, CPU, packet, Code card and mini Terminal fade. The parent's world assembles at the center in coral tint (Memory column, registers, PCB, plugs; the 04 S09 panels, quick), with a pause glyph over the creature ("frozen mid-call"). |
| 2 | "Not an empty one. An *almost exact copy of the caller*." | The text "almost exact copy" writes under the world (font 30). The parent world slides left to x = −3.4; a translucent ghost of it peels off and drifts to x = 3.4. |
| 3 | "Same code. Its own copy of the address space, its own registers, its own program counter." | The ghost fills in mint, in a cascade: Memory cells copy one by one; register values copy; the PC marker copies. Each copied panel gets a tiny tag: "address space", "registers", "PC". The child PCB card is created with `pid: 29147` (the pid field flips from 29146). A mint creature (label "PID 29147") appears above it and blinks. |
| 4 | "Remember our freeze-frame from last time, memory, registers, open files? The OS just copied all of it." | A brace across each world's panels labeled **machine state** (callback to 04); the small save-slot icon pulses between the two worlds. |
| 5 | "The creator is the **parent**. The new process is the **child**." | Labels "parent" (coral) and "child" (mint) write under the creatures. Term notes "parent", then "child". |
| 6 | "So the child starts again from the top, at `main()`?" | Student → curious. A small `main()` flag marker appears over the child's code region top, with a "?". |
| 7 | "No, and that's the odd part. Notice "hello" printed only once." | Professor → explaining. The flag gets an `x_mark` and fades. A one-line mini Terminal appears at the bottom: `hello (pid:29146)` (single line). |
| 8 | "The child never ran that line. It simply comes to life *inside* the call to `fork()`, as if it had called it itself." | In both code regions a PC arrow (coral, mint) points at the same line, `int rc = fork();`, with a small bubble "returning from fork()" on each. The child → ready (eyes open) and the pause glyph on the parent lifts. |
| 9 | "Two processes, both about to return from the same call." | Both PC arrows pulse together. Pause 1 s. |
| 10 | "The book warns you that `fork()` is the strangest routine you'll ever call. It's right." | Professor → happy; Student → surprised. Hold 0.8 s. |

**Characters:** Student (curious → surprised), Professor (explaining → happy).
**Ends with:** both worlds side by side (coral left, mint right), both PC arrows on the `fork()` line, the one-line Terminal, term strip "child".
**Implementation notes:** build a `ProcessWorld` composite with `.clone_to(point, color)` returning the cascade animation. The pid-field flip is the one visible difference at this stage; keep the rest identical on purpose.

### S05 — Who is who?   (beats: B04) · ~1:00
**Purpose:** the return value of `fork()` (child PID vs 0) is how the same code takes two branches; memories are private.
**Starts with:** S04 end state.
**Layout:** both worlds collapse into small "memory icons" beside their creatures: coral creature at (−5.0, 0.8), mint at (5.0, 0.8), each with a memory icon below it. Code block (p1.c, 8 lines) at center (0, 0.8). Terminal at the bottom (0, −2.3), 6 × 1.4, already showing `hello (pid:29146)`.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "But if they're identical, how does each one know whether it's the parent or the child? They run the same code." | Student → confused. The worlds shrink into the memory icons; the Code block `FadeIn`s at the center with two bars (coral, mint) at line 2. A "?" over each creature. |
| 2 | "They're not *quite* identical. The child has the same memory, but a private copy." | Each memory icon shows a cell `x = 100`. A padlock icon appears between them. |
| 3 | "What either one changes afterwards, the other never sees." | Coral's cell changes to `x = 101` (flash); mint's stays `x = 100`. |
| 4 | "And there's one more difference: the value that `fork()` returns." | `Circumscribe` line 2; both creatures `look_at` it. |
| 5 | "The parent gets back the PID of the new child, 29147." | A tag "rc = 29147" flies from line 2 to the coral creature and docks beside it. |
| 6 | "The child gets back zero." | A tag "rc = 0" flies to the mint creature. |
| 7 | "That single number is the whole trick. The `if` checks it." | Both bars move to line 3. Above each creature: coral shows `29147 == 0`  with an `x_mark`; mint shows `0 == 0` with a `tick_mark`. |
| 8 | "Zero? You're the child, take this branch. Anything else? You're the parent, take that one." | Mint bar drops to line 4, coral bar to line 6. Terminal prints `parent of 29147 (pid:29146)` and then `child (pid:29147)`. |
| 9 | "So the code is the same, but the world is different. Each process walks down its own branch." | Student → excited. The two bars walk on, diverging. |
| 10 | "Both processes, one program, two paths." | Professor → proud. Hold 1 s on the two bars. |

**Characters:** Student (confused → excited), Professor (proud).
**Ends with:** Code block with both bars on their branches; Terminal with 3 lines (as in S01); creatures at the sides with their rc tags.
**Implementation notes:** use the multi-bar `CodeWalker` helper (see New assets). The `x = 100` demo is a tiny aside; keep it under 4 seconds.

### S06 — Who goes first?   (beats: B05) · ~0:55
**Purpose:** after `fork()` both processes are ready; the scheduler decides the order, so output is non-deterministic.
**Starts with:** S05 end state.
**Layout:** CPU at (0, 1.0). Ready **Queue** at (0, −0.8) with the coral and mint creatures. Two small Terminals at the bottom: "run 1" at (−2.3, −2.5) and "run 2" at (2.3, −2.5), each 3.6 × 1.1. The Code block fades.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Now look at the output again. "Parent" printed before "child". But run it another time, and you might get the opposite order." | The Code block fades; the Terminal shrinks to the "run 1" slot (parent line, then child line highlighted). A second Terminal appears at "run 2" and prints `./p1` → `hello`, `child`, `parent of 29147…` (opposite order). |
| 2 | "The same program, the same input, and different output? Is it broken?" | Student → frustrated. An `MathTex(r"\neq")` glyph appears between the two Terminals. |
| 3 | "It's **non-deterministic**, and it isn't broken." | Professor → explaining. Term highlight "non-deterministic". The glyph fades. |
| 4 | "Say we have a single CPU. After `fork()`, there are two processes ready to run. Which one goes first?" | The CPU `GrowFromCenter`. The coral and mint creatures settle into the Ready queue (→ ready). A "?" over the CPU. |
| 5 | "That's the job of the CPU **scheduler**, and from our point of view it's unpredictable." | The whistle icon (04 scheduler) appears next to the CPU, labeled "scheduler". A **Spotlight** appears above the queue. |
| 6 | "Both processes sit in the ready queue, and either could be picked." | Spotlight beam sweeps to coral → coral hops onto the CPU (running); "run 1" Terminal's first line after `hello` highlights. Rewind (coral hops back). Beam moves to mint → mint hops on; "run 2" highlights. |
| 7 | "We can't make strong assumptions about what it will choose." | The spotlight wobbles between the two. Both creatures wobble in sync. |
| 8 | "This looks like a small annoyance now. Remember it. In the concurrency section, it becomes a very big deal." | Professor → worried. An `ep_tag("→ Concurrency")` in `CONC` (cyan) pops next to the scheduler icon. Hold 1 s. |

**Characters:** Student (frustrated), Professor (explaining → worried).
**Ends with:** CPU, Queue (both processes ready), spotlight, scheduler icon, the two Terminals. Transition: everything fades except the two creatures.

### S07 — wait(): let the child finish   (beats: B06) · ~1:00
**Purpose:** `wait()` blocks the parent until a child exits, which makes the order deterministic. Two cases, one result.
**Starts with:** the coral and mint creatures only.
**Layout:** a small **State diagram** in legend mode at the top-right (4.8, 2.0), scale 0.45, with a coral dot and a mint dot. A single-line **Code card** at the top-left (−4.0, 2.6): `int rc_wait = wait(NULL);`. **Timeline** at center-left (x −5.0..2.5): rows "parent" (y = 0.6), "child" (y = 0.0), "CPU" (y = −0.6), 6 ticks. A mini Terminal at the bottom (0, −2.3), 5 × 1.1.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Sometimes order matters. Suppose the parent wants to know that its child has finished before it continues." | The legend and Timeline draw. The coral parent and mint child stand above the timeline's left edge, ready. |
| 2 | "For that, there's **`wait()`**." | Term note "wait()". The Code card writes in. |
| 3a | "The parent calls it, and from then on it can't move forward until one of its children finishes. So the OS doesn't let it hold the CPU. It blocks the parent, our old blocked state, and the CPU is free for the child." | `Indicate` the Code card, then the parent; the Blocked zone of the legend glows, then the child is indicated. |
| 3b | "Let's watch it, one step at a time. First, the parent runs, and calls `wait()`." | Timeline cell 1: parent running, child ready, CPU busy; parent's dot → Running. |
| 3c | "Right away, the parent is blocked. The child moves from ready to running, and gets the CPU." | Cell 2: parent blocked (clock), child running; dots: parent → Blocked, child → Running. |
| 3d | "The child keeps running, while the parent just waits." | Cell 3: same states. |
| 3e | "Then the child exits." | The child turns zombie (grey, stitched); its dot moves back. |
| 4 | "Now `wait()` returns in the parent, and `rc_wait` holds the PID of the child that finished. The parent goes from blocked, to ready, to running again." | The zombie fades; a tag "returns 29147" flies to the parent; the parent's dot goes Blocked → Ready → Running, with pauses between. Timeline is cleared. |
| 5 | "Add one `wait()` to the parent's branch, and the output becomes deterministic. Can you see why? Pause the video and think about it." | Professor → thinking. A `progress_ring` appears at the center and fills over 3 s ("your turn"); no other motion. |
| 6 | "Two cases. If the child happens to run first, it prints and exits, and when the parent finally runs, `wait()` returns immediately." | Label "case 1". Ticks 1–2: child solid mint, parent ready outline; child exits → zombie tag at tick 2. Tick 3: parent runs, tag "returns at once". Terminal: `child (pid:29147)`, then `parent of 29147 (rc_wait:29147) …`. |
| 7 | "If the parent runs first, it calls `wait()` right away, blocks, and the CPU goes to the child." | Rewind; label "case 2". Tick 1: parent solid coral, the `wait()` tag. Ticks 2–3: parent blocked (grey + clock), child solid. Terminal is cleared and reprints in the same order. |
| 8 | "Only once the child has exited does the parent wake up. Either way, the child prints first." | Tick 4: child exits, parent → ready; tick 5: parent runs. A `tick_mark` and the caption "child always first" in `CPU_COLOR`. |
| 9 | "And the exited child waits for its parent in the zombie state!" | Student → excited; the zombie mini-icon in the timeline pulses (callback to 04). |
| 10 | "The zombie finally has a job. There's a sibling call, `waitpid()`, with more control, and rare cases where `wait()` returns early. But for us, this is the rule." | Professor → happy. A small tag `waitpid()` writes beside the Code card (not a full term highlight) and fades. |

**Characters:** Professor (thinking → happy), Student (excited).
**Ends with:** timeline (case 2), legend, Code card, Terminal with the two lines in order.
**Implementation notes:** Timeline helpers from 04: `fill(row, tick, state)`, `unfill_ticks` for the rewind. A "zombie" glyph is a small grey process icon (the 04 zombie expression at 0.4 scale).

### S08 — exec(): become someone else   (beats: B07) · ~1:20
**Purpose:** `exec()` replaces the current program's code and static data, resets heap and stack, runs it; same process, same PID; it never returns.
**Starts with:** the mint child creature.
**Layout:** mint child at the left (−4.4, 1.0) with its **Memory** column (1.3 × 3.4) at (−2.4, 0.6); code region labeled `p3`. **Disk** at (3.2, −1.0) with a file icon `wc`. **Code card** at the top-right (3.4, 2.0), three lines. A **Terminal** at the bottom (0.8, −2.4), 6 × 1.2.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "`fork()` alone is a bit limited. It only gives us copies of the *same* program." | The previous scene fades. The mint child and its Memory column appear; the code region shows the chip `p3`. A ghost coral twin appears briefly beside it with the same `p3` chip, then fades. |
| 2 | "What if the child should run something different? That's the third call: **`exec()`**." | Term highlight "exec()". The `p3` chip gets a "?" ("p3 → ?"). |
| 3 | "In our next example, the child calls a variant of `exec()` to run `wc`, the word-counting program, on the file `p3.c`." | The Code card slides in: `char *myargs[3] = {"wc", "p3.c", NULL};` / `execvp(myargs[0], myargs);` / `printf("this shouldn't print out");`. Lines 1–2 highlight. The Disk rises in with the file `wc`; a small `p3.c` file icon attaches as an argument tag. |
| 4 | "And the output shows the counts: 29 lines, 107 words, 1,030 bytes." | Terminal prints `29  107  1030 p3.c`; the three numbers get small labels (lines, words, bytes) in turn. The Terminal then dims. |
| 5 | "Let's look inside." | Hold 0.8 s. |
| 6 | "Given the name of an executable and some arguments, `exec()` loads code and static data from that file…" | A packet (`exec()`) arrives at the process; an arrow from the Disk's `wc` file reaches the Memory column's code and static-data regions. |
| 7 | "…and *overwrites* the process's current code segment and static data with it." | The old `p3` content shatters out of the two regions (fragments fall and fade); the regions refill in sky with the chip `wc`. |
| 8 | "The heap and the stack are re-initialized." | Heap and stack regions flash and clear; a small cell `argv: wc p3.c` appears at the top of the stack. |
| 9 | "Then the OS runs the new program, passing the arguments as its `argv`." | A PC arrow jumps to the top of the `wc` code. Speed lines on the creature. The PID tag "PID 29147" gets `Indicate`d: unchanged. |
| 10 | "Sound familiar? It's the loading step from last episode, applied to a process that already exists." | An `info_tag` "← Ep. 04: load" near the disk arrow, fading after 1.5 s. |
| 11 | "So it makes a new process?" | Student → surprised. |
| 12 | "No, and that's the key point. `exec()` creates *no* process. The same process, same PID, becomes a different program." | Professor → explaining. The text "same process · new program" writes (font 30); a `Transform` shows the creature's PID tag staying put while the program chip changed. |
| 13 | "If it works, `exec()` never returns. The code that came after it is gone." | A one-way arrow into the creature with "no way back"; Code card line 3 greys and gets a strike-through. |
| 14 | "In our example, the line "this shouldn't print out" never prints." | The Terminal's output stays as before; the struck line fades with an `x_mark`. |
| 15 | "On Linux there are six variants of `exec()`, with different ways of passing the arguments, but they do the same thing." | Six small chips `execl execlp execle execv execvp execvpe` appear in a row (font 18, `MONO_FONT`) and collapse into one chip `exec()`. |

**Characters:** Student (surprised), Professor (explaining).
**Ends with:** mint child with `wc` loaded (sky regions, PC at the top), Code card dimmed, Terminal with the wc output.
**Implementation notes:** program chips are `DIM` rounded rectangles with `MONO_FONT` text. Keep the "same PID" visual a calm hold, not a flashy effect. Step 15 is the last 4 s and can be trimmed.

### S09 — Why two calls? The shell   (beats: B08) · ~1:30
**Purpose:** introduce the shell as a loop of fork / exec / wait, and show that the gap between `fork` and `exec` is where the child's world can be changed.
**Starts with:** mint child + Memory column (S08), then everything fades except a small `p3.c` text.
**Layout:** Terminal on the left (−3.4, 1.0), 5 × 2.6. **Loop diagram** at the right, centered at x = 3.4: node "prompt" (3.4, 2.4), node "fork" (3.4, 1.2), then a split: left node "child: exec" (2.1, −0.3) and right node "parent: wait" (4.7, −0.3); both arrows merge back along the right edge to "prompt". The gold shell creature `sh` stands at the "prompt" node.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Hold on. All of this seems like a strange way to launch a program. First clone yourself, then replace yourself? Why not one simple call, "run this program"?" | Crux strip fades. Student → frustrated. A DIM chip `run("wc")` appears at the center with a "?". |
| 2 | "That's the question the whole design hangs on. Let's look at who launches programs for a living: the **shell**." | Professor → proud. The chip slides off to a corner and dims. The Terminal fades in at left with `prompt>` and a cursor; the gold `sh` creature enters at right. Term note "shell". |
| 3 | "The shell is just an ordinary user program." | `sh` gets a small tag "user program" in `USER_COLOR`. |
| 4 | "It shows you a prompt, and waits." | The "prompt" node of the loop draws and lights; `sh` waits (ready), the cursor blinks. |
| 5 | "You type a command: a program name and its arguments." | The Terminal types `wc p3.c` and Enter. |
| 6 | "The shell finds the executable, calls `fork()` to create a child…" | Node "fork" draws and lights. `sh` splits (mitosis): a mint clone labeled "sh" appears and the path forks to the two nodes. |
| 7 | "…calls some variant of `exec()` in the child to run the command…" | Node "child: exec" lights; the mint clone's label changes "sh" → "wc" (crossfade), sky program chip. |
| 8 | "…and calls `wait()` in the parent until the command finishes." | Node "parent: wait" lights; gold `sh` → blocked (clock). The mint `wc` runs with a progress ring; the Terminal prints `29  107  1030 p3.c`. |
| 9 | "Then it prints the prompt again." | `wc` → done and fades; `sh` returns to "prompt" (→ ready); the Terminal prints a fresh `prompt>`; the loop's return arrow `Indicate`s. |
| 10 | "And here's the key. Between `fork()` and `exec()`, there's a gap, where the code is running in the child, but it's still the shell's code." | Replay in slow motion: the segment of the child's path between "fork" and "exec" turns `CPU_COLOR` yellow with a bracket labeled "still shell code"; a mint clone labeled "sh" sits in the gap. |
| 11 | "That gap is a chance to rearrange the child's world *before* the new program starts." | A "workshop" box (dashed outline with a spinning `GearPair` and a wrench glyph) wraps the gap. Hold 1 s. |

**Characters:** Student (frustrated), Professor (proud).
**Ends with:** Terminal, the loop diagram with the gap and the workshop box, `sh` (gold) at the parent node and the mint "sh" clone in the gap.
**Implementation notes:** build the loop as a `ShellLoop` helper (nodes, arrows, `.light(node)`, `.highlight_gap()`); arrows are curved `ArcBetweenPoints`.

### S10 — Redirection   (beats: B09, first half) · ~1:00
**Purpose:** use the gap: close fd 1, open a file, then `exec()`. The file descriptors survive the `exec()`, so `wc` prints into the file without knowing.
**Starts with:** S09 end state.
**Layout:** Terminal at the top-left (−3.6, 2.4), 5 × 1.0 (one line). Center: the mint clone (labeled "sh") at (0, 1.0), standing on a **FdTable**: three plugs (0 stdin, 1 stdout, 2 stderr) in a row at y = −0.2, each with a cable: 0 → keyboard icon (−4.2, −1.4), 1 → screen icon (0, −1.8), 2 → screen icon (2.0, −1.8). A file icon `newfile.txt` waits at the right (4.6, −0.2). Three step chips at the bottom (0, −2.6): `close(1)`, `open(file)`, `exec(wc)`, all dim.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Let's use the gap. You type: `wc p3.c > newfile.txt`." | The loop diagram fades except the gap's clone, which moves to the center; plugs and devices draw in. The Terminal at the top-left shows `prompt> wc p3.c > newfile.txt`, with the `>` colored `VIRT`. |
| 2 | "The `>` sign means the output of `wc` should go into a file, not the screen." | The `>` pulses; the file icon `newfile.txt` appears at the right with a ghost dotted arrow from plug 1 to it. |
| 3 | "This is **redirection**." | Term highlight "redirection". |
| 4 | "The shell does it in the gap." | The workshop glow around the clone; the three step chips light up one at a time during the next rows. |
| 5 | "In the child, before `exec()`, it closes standard output, then opens the file." | Chip `close(1)` lights: the cable from plug 1 is cut (spark), plug 1 pops out and the slot is dashed and empty. |
| 6 | "UNIX always hands out the lowest free file descriptor. Remember our three plugs, 0, 1, 2? Plug zero is taken, plug one was just freed, so the file takes plug number one." | Chip `open(file)` lights: a scanning pointer ticks slot 0 (taken, `x_mark`), slot 1 (free, `tick_mark`); the file icon flies up and plugs into slot 1; a cable runs from slot 1 to the file. Tag "lowest free = 1". |
| 7 | "And open files stay open across `exec()`." | Chip `exec(wc)` lights: the clone's label changes "sh" → "wc" (crossfade, sky); the plugs and cables `Indicate` — unchanged. |
| 8 | "So when `wc` later prints, it prints "to the screen", exactly as always, and the text lands in the file instead." | `wc` runs; text lines flow down the cable from slot 1 into the file icon, which fills with `29  107  1030 p3.c`; the screen icon stays empty. |
| 9 | "And `wc` doesn't even know!" | Student → excited, with a thought bubble "I just print to stdout…" |
| 10 | "And the proof is easy. Run the command, and the screen stays empty. Then read the file, and all the expected output is there." | Professor → happy. The Terminal prints a fresh prompt with no output; then `prompt> cat newfile.txt` prints `29  107  1030 p3.c`. |

**Characters:** Student (excited), Professor (happy).
**Ends with:** the `wc` process on the FdTable with plug 1 into the file, filled file icon, Terminal with `cat` output. Transition: everything fades except the Terminal.
**Implementation notes:** adapt Figure 5.4; the narration says `p4.output` in the Terminal but `newfile.txt` in the diagram, which is fine (the book uses both). The plugs are the same prop as 04 S12 (`plug` icon plus cable); wrap as `FdTable` (see New assets).

### S11 — Pipes   (beats: B09, second half) · ~0:30
**Purpose:** `pipe()` connects one process's output to another's input via a kernel queue.
**Starts with:** Terminal only.
**Layout:** `grep` (sky) at (−3.2, 1.0), `wc` ([4], violet) at (3.2, 1.0); a **pipe** at the center (0, 1.0) inside a thin `KERNEL_COLOR` band labeled "kernel". Terminal at the bottom (0, −1.9), 7 × 1.0.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Redirection connects a program to a file. A close relative connects it to another program: the **pipe**." | Term note "pipe". The `pipe_glyph` draws at the center. |
| 2 | "The `pipe()` call makes a queue inside the kernel." | The pipe becomes a tube with queue slots; a red band "kernel" fades in around it. |
| 3 | "One process's output is connected to one end, another process's input to the other." | `grep` and `wc` creatures hop in. A cable from `grep`'s plug 1 → the left end of the pipe; a cable from the right end → `wc`'s plug 0. |
| 4 | "So you can chain tools: look for a word in a file with `grep`, and pipe the result into `wc` to count how many." | The Terminal types `grep -o foo file \| wc -l`; small "foo" tokens flow through the pipe; a counter on `wc` ticks 1, 2, 3; the Terminal prints `3`. |
| 5 | "All without changing a single line in either program." | Both creatures get a padlock-style tag "code unchanged". Hold 1 s. |

**Characters:** corner mode; Student looks at the pipe.
**Ends with:** the pipe scene. Transition: everything dims to 25% for the Tip.

### S12 — Tip: get it right   (beats: B10) · ~0:30
**Purpose:** Lampson's law; `fork()` + `exec()` is simple and powerful; not everyone agrees.
**Starts with:** S11 end state, dimmed.
**Layout:** a **Tip card** slides in from the right, covering x 0..6.6, y −1.8..2.6.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Pipes, redirection, a whole shell, from two small calls. One reason to see this design as a classic is a rule named after Butler Lampson: **get it right**." | Tip card slides in ("TIP: GET IT RIGHT (LAMPSON'S LAW)", `DIM` frame). Big text "Get it right." writes. |
| 2 | "Neither abstraction nor simplicity is a substitute for getting it right." | The card body writes the sentence (11 words). A `layers` icon (abstraction) and a plain circle (simplicity) each get an `x_mark` beside "…a substitute". |
| 3 | "There are many ways to design process creation. But the UNIX designers' combination of `fork()` and `exec()` is simple, and immensely powerful." | Two chips, `fork()` and `exec()`, appear left of the card and snap together like puzzle pieces with a small glow. |
| 4 | "Not everybody agrees. A recent paper argues for a simpler call, `spawn()`. The authors of the book have opinions. You're allowed to have your own." | Professor → neutral. A chip `spawn()` slides in with a "?", hovers, slides out. Hold 0.8 s. |

**Characters:** Professor (neutral).
**Ends with:** the Tip card slides out; the dimmed scene fades; screen empty except the badge.

### S13 — Signals   (beats: B11, first half) · ~0:45
**Purpose:** `kill()` sends signals; ctrl-c terminates, ctrl-z stops (resume with `fg`); a process can catch a signal.
**Starts with:** empty (badge).
**Layout:** the coral creature (running, speed lines) at center (0, 0.8). A keyboard icon at the left (−3.8, 0.0) with keycaps. A mini Terminal at the bottom (0, −2.2), 4.5 × 0.9.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Back to the interface. Beyond those three calls, there are more. In UNIX, `kill()` sends a **signal** to a process." | The coral process enters at center. Term highlight "signal". A lightning-bolt glyph labeled `kill(pid, sig)` flies in from the top-left and hits it: the creature squashes and recovers. |
| 2 | "A signal can tell the process to pause, to die, or other useful things." | Three small signal chips drift out of the bolt: a pause glyph, an `x_mark`, a "…" (other). |
| 3 | "Your shell wires some to keystrokes: control-c sends an interrupt, which normally terminates the process." | The keyboard icon appears; keycaps "ctrl" and "c" press; a bolt labeled `SIGINT` hits; the process → done and pops into a puff. |
| 4 | "Control-z sends a stop, which pauses it, and you can resume it later with `fg`." | A fresh coral process appears. Keycaps "ctrl" + "z" press, bolt `SIGTSTP`; the process freezes (greyed, pause glyph). The Terminal types `fg`; a play glyph; the process resumes. |
| 5 | "That's the "suspend and resume" from our menu." | The 04 menu row "Misc. control" pops at the top-left, small, with a `tick_mark`, then fades. |
| 6 | "A process can also *catch* a signal with `signal()`…" | The process holds up a small box labeled `handler()`; a bolt flies in and is caught (the box flashes; the bolt is absorbed). |
| 7 | "…run its own code when one arrives." | Three tiny code lines unroll from the box (`handler() {` / `  …` / `}`) while the process keeps running. Hold 1 s. |

**Characters:** Student (curious) at row 3, then neutral.
**Ends with:** the coral process with the `handler()` box; keyboard icon; Terminal. Transition: everything fades.

### S14 — Users and the superuser   (beats: B11, second half) · ~0:30
**Purpose:** users can only control their own processes; the superuser (root) can control all.
**Starts with:** empty.
**Layout:** two rounded groups: left "you" (name_tag) containing coral and gold creatures at (−3.6, 0.8); right "roommate" containing the sky creature at (3.6, 0.8). A force-field shield (a translucent dashed arc) around the right group. At the top-center (0, 2.6), a "root" crown tag appears later.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Wait. Then can I kill anyone's process? Say, the one my roommate started on the same machine?" | Student → curious. A bolt arcs from the left group toward the sky process and bounces off the shield. |
| 2 | "That's why systems have **users**. You log in, and you can control your own processes. Not anybody else's." | Professor → explaining. Term note "user". The two groups and name tags appear; a bolt from "you" hits the coral process (squash) but is blocked at the shield. |
| 3 | "Sharing the machine safely needs that rule." | A `padlock` icon on the shield. Hold 1 s. |
| 4 | "There's one exception: the **superuser**, or **root**." | Term note "superuser (root)". A crown-tagged "root" figure (a small process with a crown) enters at the top-center; its bolt passes through the shield and hits the sky process. |
| 5 | "They can administer the system and control any process. Powerful, and dangerous. Use it rarely." | The crown pulses; a `shutdown` chip with a warning triangle appears and fades. |
| 6 | "With great power comes great responsibility. The French Revolution said it first, apparently." | Professor → worried. An **Aside card** "THE SUPERUSER" slides in with the quote "With great power comes great responsibility." (≤8 words) and slides out. |

**Characters:** Student (curious), Professor (explaining → worried).
**Ends with:** both groups, shield, root figure. Transition: everything fades.

### S15 — Useful tools   (beats: B12) · ~0:35
**Purpose:** `ps`, `top`, `kill`/`killall`, and man pages.
**Starts with:** empty (badge).
**Layout:** a big Terminal at center-left (−1.2, 0.6), 7 × 3.4. Aside card slides in from the right at the end.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "To see all this in practice, some tools help. `ps` lists the processes running on your system." | The Terminal types `ps`; prints a table `PID  CMD` with 4 rows (`29146 p1`, `29147 p1`, `29150 sh`, `29151 ps`); a coloured dot (coral, mint, gold) in front of the first three. |
| 2 | "`top` shows which ones are using the most CPU." | The Terminal clears; `top` shows bars, sorted descending; the bars animate. |
| 3 | "Humorously, `top` often claims that `top` is the top resource hog." | `Indicate` the first row, which reads `top`. Hold 0.6 s for the joke. |
| 4 | "And `kill` and `killall` send signals. Use them carefully, or you could kill your window manager." | The Terminal types `killall …`; a small `desktop` icon (window) pops and vanishes with an `x_mark`. |
| 5 | "Is there a manual for every flag?" | Student → bored. |
| 6 | "There is. They're the **man pages**. When someone replies, "RTFM", they mean you should go read them." | Professor → happy. Term note "man pages". The Terminal types `man ps` and a page header `PS(1)` appears. An **Aside card** "RTFM: read the man pages" (with a `book` icon) slides in and out. |

**Characters:** Student (bored), Professor (happy).
**Ends with:** Terminal with a man page header. Transition: everything fades.

### S16 — Back to the menu   (beats: B13) · ~0:45
**Purpose:** map the UNIX calls to the five items of the menu from 04.
**Starts with:** empty (badge).
**Layout:** the **MenuCard** at the left (−3.2, 0.3), 4.6 × 4.4, title "Process API", rows create / destroy / wait / misc. control / status. A column of UNIX chips at the right (3.0, 0.3).

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Let's wrap up by going back to the menu from last time." | The MenuCard slides in with the five rows. |
| 2 | "**Create**: that's `fork()`, and usually `exec()` right after." | Row 1 highlights; chips `fork()` and `exec()` fly in next to it with the clone icon. |
| 3 | "**Wait**: that's `wait()`." | Row 3 highlights; chip `wait()` with a clock. |
| 4 | "**Destroy** and **miscellaneous control**: signals, via `kill()`." | Rows 2 and 4 get a joint bracket; the chip `kill()` with the bolt glyph arrives. |
| 5 | "**Status**: `ps` and `top`." | Row 5 highlights; chips `ps` and `top` with an `info_tag`. |
| 6 | "A handful of simple calls, combined, are enough to build a shell, redirection, pipes, and more." | The chips `fork() exec() wait()` link into a chain; from it a Terminal icon, a `>` and a `|` pop out. |
| 7 | "And we've only skimmed the surface. The book recommends reading Stevens and Rago to go deeper." | A `book` icon with "Stevens & Rago" appears and fades. |
| 8 | "We'll return to file descriptors when we get to file systems." | An `ep_tag("→ Ep. 39")` sticks to the `>` and `|` glyphs, then everything fades. |

**Characters:** corner mode; both characters nod (Professor happy).
**Ends with:** empty (badge only).

### S17 — Recap   (beats: B14) · ~0:35
**Purpose:** five takeaways.
**Starts with:** empty (badge).
**Layout:** header "Recap" in `VIRT` at the top; a numbered list at the left (−5.6 .. 1), font 28; an icon for each line at x = 4.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "So, today:" | Header "Recap" writes. |
| 2 | "**`fork()`** creates a new process: a nearly exact copy. The parent gets the child's PID, and the child gets zero." | Line 1: "fork() clones a process". Icon: a blob splitting into two (coral, mint). |
| 3 | "The order is up to the scheduler, so output is **non-deterministic**. **`wait()`** makes the parent wait for its child." | Line 2: "scheduler picks the order; wait() waits". Icon: a clock beside a zombie. |
| 4 | "**`exec()`** turns the current process into a different program, without creating a new one." | Line 3: "exec() becomes another program". Icon: a file swapping into a creature. |
| 5 | "Keeping `fork()` and `exec()` apart lets the shell set up redirection and pipes in between." | Line 4: "fork and exec apart: redirection, pipes". Icon: the three plugs. |
| 6 | "**Signals**, **users** and the **superuser** control who can do what to which process." | Line 5: "signals, users, root: who controls what". Icon: a bolt and a crown. Hold 1.5 s. |

**Ends with:** the full recap list. Section badge fades out.

### S18 — Teaser: who stays in charge?   (beats: B15) · ~0:30
**Purpose:** hook for 06 (Direct Execution): how does the OS keep control while programs run directly on the CPU?
**Starts with:** S17 end state.
**Layout:** dialogue mode. CPU at (0, 1.2) with a coral process running (speed lines). At the bottom edge (0, −0.4) a red `KERNEL_COLOR` band labeled "OS" with a `GearPair`, behind a translucent glass pane (a rectangle with a diagonal highlight) that separates it from the CPU.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "All these calls say "the OS creates this", "the OS stops that". But when my program is running on the CPU, the OS isn't. How does it ever get control back?" | The recap fades; characters move to dialogue mode; Student → curious. The CPU, running coral and the glass-separated "OS" band fade in. A "?" over the band. |
| 2 | "Good question. And if the OS watched every instruction, we'd lose all the speed." | Professor → thinking. Instruction dots crawl past a "checkpoint" gate under the OS's eye; the `SpeedGauge` drops to a low reading. |
| 3 | "We want programs to run *directly* on the CPU, but we want to stay in charge." | The gate disappears; the gauge returns to full; a dotted line with a "?" connects the OS band to the CPU through the glass. |
| 4 | "Next time: limited direct execution." | Professor → happy. The text "limited direct execution" writes at the center. Then everything `FadeOut` (0.5 s) and the end card "Next: 06 · Direct Execution" (with a `VIRT` dot) holds for 2 s. |

**Characters:** Student (curious), Professor (thinking → happy).
**Ends with:** black end card.

## New assets needed
Nothing here exists in `ostep_lib` yet unless noted. Suggested module: `ostep_lib/props/p05_*.py`.
- **`clone_process(proc, color, to)`**: the "mitosis" split helper (04's S22 listed it as needed; it is not in the README). Squash, stretch, separate; returns the new creature and an animation.
- **`ProcessWorld(color, pid, label)`**: a composite of creature + Memory column (4 regions) + RegisterBank (PC) + small PCB card + three tiny plugs. Methods: `.collapse()` (to a memory icon + creature), `.clone_to(point, color)` (cascade copy animation, including the pid-field flip), `.set_program(chip)` for S08.
- **`CodeWalker(code, bars)`**: a `Code` block with several colored highlight bars. Methods: `.move_bar(i, line)`, `.add_bar(color)`, `.indicate(line)`. 04 describes a single moving bar; this needs more than one.
- **`FdTable(slots)`**: three plugs (0 stdin, 1 stdout, 2 stderr) with cables to device icons. Methods: `.cut(i)`, `.plug_into(i, device)`, `.scan_free()`. The plug, keyboard and terminal icons exist in `p04_icons`.
- **`ShellLoop`**: the prompt → fork → (exec / wait) → prompt diagram with `.light(node)` and `.highlight_gap()`, plus the "workshop" box (dashed outline, gears, wrench glyph).
- **`KernelPipe`**: a tube with queue slots inside a thin red kernel band, with tokens that flow through (extends the `pipe_glyph` icon).
- **Signal glyphs:** a lightning bolt (with a text label), a keycap (`ctrl`, `c`, `z`), a `handler()` box, a shield / force-field arc, a crown tag for "root", a window-frame "desktop" icon if the existing one doesn't read well.
- **`MenuCard` with custom rows**: check that `p04_icons.MenuCard` accepts the five rows and per-row highlights; if not, add `.highlight_row(i)` and `.attach_chip(i, text)`.
- **Zombie mini-icon:** the 04 `zombie` expression at scale 0.4, for Timeline rows (it can be built from existing assets).
- **Glass pane** (for S18): a translucent rounded rectangle with a diagonal highlight stripe.
- No new character expressions are needed.

## Open questions
- **Length:** ~14:00 is at the top of the 8–15 min target. Candidates to trim: S12 (Tip + `spawn()`, 0:30), S15 (tools, 0:35), S14 (users, 0:30), or S11 (pipes, 0:30). Which first?
- **Child of the shell:** I use mint (the "child" color) for the shell's clone, and gold only for the shell itself. After `exec()` the clone keeps its mint color but gets a `wc` label. Is that right, or should a process change color when it changes program?
- **PIDs:** one fixed pair (29146 / 29147) is used in every example, whereas the book's outputs show different PIDs per run. OK?
- **Episode numbers in tags:** "→ Ep. 39" (file descriptors / persistence, S16) and "← Ep. 04" (S08) are hard-coded; please confirm 39 against the final index.
- **Terminal outputs:** the `ps`/`top` rows and the `x = 100` private-memory demo (S05) are my inventions, not from the book. Keep?
- **S07 pause:** a 3 s silent "think about it" beat with a progress ring, as the book does. Is a silent pause acceptable, or should the narration fill it?
- **Superuser quote (S14):** the French Revolution joke comes from the book's reference note. Keep or cut?
