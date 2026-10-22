# 06 — Mechanism: Limited Direct Execution · Scene breakdown
> Script: Ostep/Scripts/06-cpu-mechanisms.md · Scenes: 18 · Est. duration: ~14:00

## Visual overview
- **Core metaphor: the CPU chip rides across the dashed line.** The User/Kernel boundary from 01–03 becomes the stage of the whole episode. User mode is above the line, kernel mode below. The **CPU chip** has two seats: a *user seat* above the line (a Process creature stands on it) and a *kernel seat* below it (a red **OS token** stands on it). A **trap** or **interrupt** sends the chip sliding down across the line (boundary flash, **Privilege gauge** flips to KERNEL); **return-from-trap** sends it back up. So the viewer *sees* who holds the CPU and in which mode. Everything the OS does happens below the line, everything a program does above it.
- **Second metaphor: a pause/resume package.** A process's registers travel as a small stack of colored cells (a "register packet", in the process's color). The hardware drops it onto a **kernel stack** tray at a trap, and picks it up at return-from-trap. For the context switch, the kernel registers go into the **save slot** from episode 04 (the floppy icon), so the "video-game save" setup is paid off.
- **Third metaphor: baby-proofing.** In S16 the whole stage becomes a playroom with a cabinet lock, a socket cover and a wall timer.
- **Structure of the episode:** the naive "direct execution" protocol is drawn first (S03) as a two-column chart. Problem 1 (S04–S08) adds the line, trap, trap table and the three-column protocol (Figure 6.2). Problem 2 (S09–S14) adds the timer and the context switch, and ends with Figure 6.3 on the Timeline.
- Props used (from the bible): Crux card, Tip/Aside card, Term highlight, Section badge, CPU, Memory, Disk, **User/Kernel boundary**, **Privilege gauge**, Timeline, Queue, State diagram (legend), PCB card, Register bank, **Save slot**, Code block, Mechanism/policy icons, Peach (not used). Characters: Professor, Student, Computer, Process.

### Persistent assignments
| Thing | Look | Notes |
|---|---|---|
| Process **A** | `Process(label="A", color=PROCESS_COLORS[0])` (coral) | Same as episode 04. The main actor. |
| Process **B** | `PROCESS_COLORS[1]` (mint) | The other process in the cooperative and context-switch scenes. |
| Process **C** | `PROCESS_COLORS[2]` (gold) | Only in S18 (teaser queue). |
| Register packet | 3 tiny cells (0.18 × 0.18) in a row, filled with the owner's process color | A's = coral, B's = mint. A packet in `KERNEL_COLOR` = kernel registers of that process. |
| **OS token** | Rounded badge, `KERNEL_COLOR` fill, white "OS", 0.9 × 0.55; stands on the kernel-seat chip | The OS "running". |
| CPU chip | `CPU_COLOR`, scale 0.8 (1.12 × 1.12) in the LDE world | **User seat (0, 0.55)** (chip center; the process stands on top). **Kernel seat (0, −1.9)** (the OS token stands on top). |
| User/Kernel boundary | Dashed line at **y = −0.3**, user zone tinted `USER_COLOR` 0.08, kernel zone `KERNEL_COLOR` 0.10; labels "user mode" (−6.2, 0.2) and "kernel mode" (−6.2, −0.8), exactly as in 01–03 S20 | Appears in S04 and stays through S16 (with the zone tints). |
| Privilege gauge | The 01–03 widget at the right edge (**6.4, 0**), reads USER / KERNEL | Flips in sync with every crossing. |
| Benches | Where a non-running process waits: **A bench (−3.4, 1.0)** and **B bench (3.4, 1.0)** in the user zone; the process is `ready` with a process-color outline ring under it | In the cooperative / switch scenes. |
| Kernel stack | Narrow tray with a label `k-stack(A)` / `k-stack(B)`, 1.6 wide × 1.4 tall; **A's at (−3.6, −1.9)**, **B's at (3.6, −1.9)** | Register packets stack inside. |
| Trap table | Card, 3.2 × 1.9, `KERNEL_COLOR` frame, header "TRAP TABLE", rows `syscall → handler`, `timer → handler`, `keyboard → handler` | Kernel zone, upper left at (−4.4, −1.7) when shown with other things; centered in S07. |
| Characters (corner mode) | Student (−5.8, −2.8), scale 0.75, facing right; Professor (5.8, −2.8), scale 0.75, `flip()`. **In the kernel-heavy scenes (S06–S14) they scale to 0.6 and sit at (±6.1, −3.0).** | Dialogue mode (S01, S18): Student (−2.6, −1.2), Professor (2.6, −1.2), scale 1. |
| Section badge | Top-left (−6.6, 3.6): `VIRT` dot + "06 · Direct Execution", font 22, `DIM` | Appears in S02, stays until S16. |
| Term highlight | As in episode 04: written at (0, 2.9), font 54, `VIRT` underline, shrinks to top-right (6.6, 3.6) | Every bolded term's first appearance. |
| Timeline | Episode-04 standard (running = solid, ready = outline, etc.). New row `OS` (`KERNEL_COLOR` solid blocks). | S13 and S15. |

## Scenes

### S01 — Just run it   (beats: B01) · ~0:45
**Purpose:** feel why direct execution is attractive (fast) and why it is scary (nobody can stop a misbehaving program).
**Starts with:** empty (BG).
**Layout:** dialogue mode, then a CPU at (0, 0.7) with Process A standing on top, the **Memory** column at left (−4.6, 0.7), 1.2 wide × 3.2 tall, the **Disk** at right (4.6, 0.6). A tiny red "OS" box at the bottom center (0, −2.2), scale 0.6 (the OS "on the sidelines").

| # | Narration (exact words the action lands on) | On screen / animation |
|---|---|---|
| 1 | "What is the simplest way to run a program? Load it, jump to `main()`, and get out of the way?" | Student (curious) and Professor (neutral) slide in to dialogue mode. A appears, an arrow from a "main()" label hops it onto the CPU (`hop_to`). |
| 2 | "That's called direct execution, and it has one huge advantage. It's *fast*. No middleman." | Professor (explaining). A speed gauge (the episode-04 `SpeedGauge`) next to the CPU swings to full, with a small "FAST" label in green. |
| 3 | "The program runs natively on the hardware." | A runs with a faint speed-lines glow. |
| 4 | "Great. Ship it." | Student (excited). Pause 0.5 s. |
| 5 | "Now the program decides to read every file on the disk." | Professor (worried). A's arm (a thin line) shoots to the Disk; files fly out of it into A. |
| 6 | "Or to scribble over memory that isn't its own." | A's line stretches to the Memory column, scribbling coral marks across all its cells (including ones outside "its" region). |
| 7 | "Or just to run `while (1)` until the sun burns out." | A spins in place; a loop arrow circles over it. The Computer pops up at bottom-center (0, −2.9), scale 0.6 → overwhelmed. |
| 8 | "And the OS does… what, exactly?" | Student (confused). The OS box at the bottom waves a tiny arm at the CPU, can't reach it (a translucent wall). |
| 9 | "Nothing. The OS isn't running. The program is. The OS can only watch from the sidelines." | The OS box dims. A glows `CPU_COLOR` on the chip. Hold 1 s. |
| 10 | "An operating system with no control over anything is just a library. A very sad state of affairs for an aspiring operating system." | Professor (thinking). The OS box shrinks into a book icon labeled "library"; Student (sad). |

**Characters:** Student (curious → excited → confused → sad), Professor (explaining → worried → thinking), Computer (overwhelmed).
**Ends with:** CPU with A (spinning), Memory (scribbled), Disk, the "library" book at the bottom, both characters in dialogue mode, the Computer overwhelmed.
**Implementation notes:** use `SpeedGauge` (04) for "FAST". Memory scribble = random coral `Line`s over the cells.

### S02 — The Crux   (beats: B02) · ~0:35
**Purpose:** pose the question, and introduce the two forces (performance, control) and the name of the technique.
**Starts with:** S01 end state.
**Layout:** Crux card centered (0, 0.4), 9 × 3. Characters glide to corner mode.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | (transition) | The stage fades; the Computer drops out. The characters glide to corner mode. The Crux card `Write`s in the `VIRT` accent: **"How to efficiently virtualize the CPU with control?"**, subtitle (font 22, `DIM`): "The OS must virtualize the CPU in an efficient manner while retaining control over the system. Both hardware and operating-system support will be required." |
| 2 | "To virtualize the CPU, the OS has to share it among many processes by time sharing." | Card shrinks to the top strip (0, 3.2). Below it, a small Timeline strip (three alternating colored slices) shows time sharing (callback to 04). |
| 3 | "That raises two challenges, pulling in opposite directions." | Two arrows pull a Process creature in opposite directions: left, a stopwatch (`stopwatch` icon) "performance"; right, a hand/walls icon "control". |
| 4 | "The first is **performance**: no excessive overhead." | The stopwatch pulses. The Process leans left. |
| 5 | "The second is **control**: processes must not be able to run forever, or touch what they shouldn't." | The walls pulse. The Process leans right. |
| 6 | "The answer is a technique with a long name: **limited direct execution**." | The two arrows slide together into a tight line. Term highlight "limited direct execution" (docks to the top bar at the end of the scene). |
| 7 | "*Direct*: run the program on the CPU itself. *Limited*: the guard rails we build now." | The word "direct" lights up (a CPU glyph under it); "limited" lights up (a little fence glyph under it). Section badge "06 · Direct Execution" forms top-left. |

**Characters:** Student (neutral → curious), Professor (explaining).
**Ends with:** section badge, crux strip, term strip "limited direct execution"; the two icons (stopwatch, walls) fade. Nothing else.

### S03 — The naive protocol   (beats: B03) · ~1:00
**Purpose:** draw direct execution as a protocol (Figure 6.1), then pose the two problems that become the two halves of the episode.
**Starts with:** S02 end state.
**Layout:** a two-column chart centered: header row "OS" (left column, x = −3.2) and "Program" (right column, x = 3.2), a thin horizontal rule below, rows 0.45 tall starting at y = 1.8. Font 24, `MONO_FONT` for `main()`.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Here's direct execution as a protocol." | The chart frame draws (headers "OS" / "Program"). |
| 2 | "The OS creates a process entry, allocates memory, loads the program, sets up the stack, clears the registers…" | Rows write in the left column, one at a time (0.7 s each): `Create entry for process list`, `Allocate memory for program`, `Load program into memory`, `Set up stack with argc/argv`, `Clear registers`. Each has a tiny icon at its left (PCB card, memory, disk→memory arrow, stack, registers). |
| 3 | "…and *calls* `main()`." | Row `Execute call main()` writes with "call" in bold; an arrow runs from that row across to the right column. |
| 4 | "The program runs, and *returns*." | Right column: rows `Run main()` and `Execute return from main` write; the second row's arrow returns to the left column. |
| 5 | "The OS frees the memory and removes the entry." | Left rows `Free memory of process` and `Remove from process list` write. Hold 1 s. |
| 6 | "That's just calling a function." | Student (curious). A call arrow and a return arrow trace over the chart (one `Indicate` each). |
| 7 | "Exactly, which is why it's so fast." | Professor (explaining). The chart gets a small green "FAST" tag. |
| 8 | "But it raises two problems. One: how do we stop the program from doing what we don't want, while still running it efficiently?" | Professor (worried). Two big numerals, ① and ②, pop in at the chart's right edge. ① lights up: a mini icon of A reaching toward the Disk, a red "!" over it. |
| 9 | "Two: how does the OS stop it, to switch to another process?" | ② lights up: a mini icon of the CPU with A, and B waiting behind a wall. Hold 1 s. |

**Characters:** Student (curious), Professor (explaining → worried).
**Ends with:** the chart with ① and ② at the right; characters in corners. Transition to S04: the chart slides left and dims to 25% (it will return in S08 in an expanded form), and ① stays.
**Implementation notes:** adapt **Figure 6.1**. This is the first use of the reusable `ProtocolChart` (New assets).

### S04 — Problem 1: restricted operations   (beats: B04, first half) · ~0:40
**Purpose:** show why a process must not be allowed to do I/O directly (permissions would be bypassed), and why "inspect every instruction" is not the answer.
**Starts with:** S03 end state (chart dimmed on the left; ①).
**Layout:** center stage: a **Disk** at (3.6, −1.2), a small file-system "checkpoint" gate (a booth with a bar) between a process and the Disk at (1.2, −0.4). Process A at (−2.0, 1.0). Crux card strip at top (0, 3.2): "How to perform restricted operations?" (small, `VIRT`).

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Problem number one. What if the process wants to do something *restricted*, like reading from the disk?" | The crux strip writes in at the top. A walks to the left of the screen; a request arrow "read" leaves A toward the Disk. |
| 2 | "So just let it. It's *its* program." | Student (curious). The arrow goes straight to the Disk; data flows back. |
| 3 | "A file system checks permissions before it opens a file." | Professor (worried). The arrow is rewound; the gate/booth appears in its path and checks a badge (green check on A's own file). |
| 4 | "If any process could talk to the disk directly, it would skip the check…" | A second request arrow goes around the booth, straight to the Disk. |
| 5 | "…and read or write the whole disk. All protection gone." | Every file on the Disk lights up; a padlock icon on the booth cracks open and falls (small `x_mark`). |
| 6 | "Then let the OS inspect every instruction before it runs." | Student (confused). A magnifying glass (circle + handle) hovers over a row of instructions flowing toward the CPU. |
| 7 | "Safe, and slow. We'd throw away the point of direct execution." | Professor (thinking). The instruction row crawls to a stop; the "FAST" tag from S03 turns red and reads "SLOW". |
| 8 | "We want the *hardware* to help." | The magnifier fades. A small CPU chip pulses with a lock glyph on it. |

**Characters:** Student (curious → confused), Professor (worried → thinking).
**Ends with:** the crux strip, the Disk, A, the CPU glyph pulsing. Everything else fades.

### S05 — Two modes: user and kernel   (beats: B04, second half) · ~0:35
**Purpose:** the hardware solution: user mode vs. kernel mode. Pay off the dashed line and the gauge from 01–03.
**Starts with:** S04 end state.
**Layout:** the **User/Kernel boundary** (y = −0.3) and its tints and labels. The **CPU chip** at the user seat (0, 0.55) with A on it. The **Disk** moves to the kernel zone (4.2, −2.2). The privilege gauge at (6.4, 0).

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "So the CPU gets two **modes**." | The dashed boundary **draws** across the screen (left to right) and the two zones tint in. The Disk slides down into the kernel zone. The CPU chip settles on the user seat with A standing on it. Term highlight "user mode / kernel mode" (docks small). |
| 2 | "In **user mode**, code is restricted: if a process tries to issue an I/O request…" | The gauge reads USER (cyan). A reaches toward the Disk; a request arrow leaves A and heads for the boundary. |
| 3 | "…the processor raises an exception, and the OS will most likely kill it." | The arrow hits the boundary and bounces (flash `flash_at`). A "!" pops over A, a red `x_mark` stamps it; A turns `done`/greyed and fades (`FadeOut`). Term highlight "privileged operation" (small, near the gauge). |
| 4 | "In **kernel mode**, where the OS runs, code can do anything, including every privileged operation." | The CPU chip (with a fresh A gone) is empty. A red **OS token** hops onto the chip; the chip slides down across the line to the kernel seat (0, −1.9) (`UserKernelBoundary.cross`); the gauge flips to KERNEL (red). The token's arm reaches the Disk freely; a data packet flows back. |
| 5 | "You've met this: the dashed line from our first episode, user above, kernel below, and the gauge that reads which side you're on. Now it goes to work." | The dashed line pulses once along its whole length; a small thumbnail of the 01–03 line appears (ghost) and merges into it (callback). Student (excited). |

**Characters:** Student (excited at step 5); Professor neutral.
**Ends with:** boundary + tints + labels, gauge at KERNEL, the CPU chip at the kernel seat with the OS token on it, Disk reachable below. A is gone (a fresh A will appear in S06). Section badge, term strip "user mode / kernel mode".
**Implementation notes:** the "chip crosses the boundary" animation (`cpu_ride(chip, seat)`) is the signature of the episode: chip slides along a vertical path, boundary flash at the crossing, gauge flips at the midpoint. A small `Text` "privileged" in `KERNEL_COLOR`, never more than ~25 words on screen.

### S06 — System call: trap and return-from-trap   (beats: B05) · ~1:15
**Purpose:** how a user program legitimately gets kernel services: system call, trap, return-from-trap, kernel stack, and the fact that `open()` is just a library call that traps.
**Starts with:** S05 end state, then A returns to the user seat.
**Layout:** LDE world: chip at the user seat with A; **kernel stack** tray `k-stack(A)` at (−3.6, −1.9); the OS box ("trap handler", `KERNEL_COLOR`, 2.4 × 1.0) at (3.4, −1.9); Disk at (5.4, −2.9) scale 0.6. Gauge at USER at start.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "But then how does a program ever read a file?" | Student (confused). The OS token slides off the chip to the handler box. The chip hops up to the user seat; A hops on (running). Gauge → USER. |
| 2 | "With a **system call**." | Term highlight "system call". A thin dotted door in the boundary (a small gap with a doorknob) fades in at (0, −0.3). |
| 3 | "System calls let the kernel carefully expose a few key services: the file system, creating and destroying processes, talking to other processes, allocating memory." | Four small icons (file, a new process blob, two chat bubbles, memory cell) fade in below the line next to the door, one per phrase (0.5 s apart). |
| 4 | "Real systems offer a few hundred. Early UNIX had about twenty." | A counter beside them: "~300" then it crossfades to a smaller "~20" tagged "early UNIX". |
| 5 | "To make one, the program runs a special instruction: a **trap**." | Term highlight "trap". A's code line (a small `Code` snippet `trap` in `MONO_FONT`, 1 line) lights up above A. |
| 6 | "It jumps into the kernel and raises the privilege level, both at once." | One motion: A's register packet (coral, 3 cells) pops out of A and the chip slides down across the line (flash, gauge → KERNEL); the OS token hops onto the chip; the chip lands on the kernel seat; A is left standing on the *user bench* (−3.4, 1.0) frozen (outline only). |
| 7 | "Now the OS can do the privileged work, if it allows it." | The token's arm reaches the Disk (a gate "allowed?" pulses green), data flows to the token. |
| 8 | "When it's done, a **return-from-trap** goes back to the program and lowers the privilege level." | Term highlight "return-from-trap". The chip rides back up; the data packet rides with it; A hops from the bench back on the chip (running); gauge → USER. A bounces. |
| 9 | "The hardware must save the caller's registers, to be able to come back." | Rewind slightly. The coral packet is shown flying from A into the `k-stack(A)` tray (stack pushes up), then (return) flies out and back into A. A caption: "saved by hardware". |
| 10 | "On x86, it pushes the program counter, the flags and a few more onto a per-process **kernel stack**." | The packet cells get tiny labels PC, flags, … (font 14). Term highlight "kernel stack" (small, beside the tray). |
| 11 | "Return-from-trap pops them off again." | The packet pops out of the tray back into A. |
| 12 | "When I write `open()` in C, it looks like an ordinary function call." | Student (curious). A `Code` snippet `fd = open("notes.txt", …);` slides in at the left of A. |
| 13 | "It is. A call into the C library, which puts the arguments in agreed places, executes the trap, and unpacks the result." | Professor (happy). The snippet is wrapped by a thin box labeled "C library" with three tiny chips inside (args → regs, syscall number, trap!). The trap arrow fires from the box. |
| 14 | "Somebody wrote that assembly for you." | A small tag "hand-coded assembly" on the box; a tiny hand-wave from Professor (blink). Hold 0.8 s. |

**Characters:** Student (confused → curious), Professor (happy).
**Ends with:** LDE world: chip at the user seat, A running, `k-stack(A)` empty, the handler box, the Disk, gauge USER, "system call", "trap" and "return-from-trap" in the term strip history.
**Implementation notes:** keep the `cpu_ride` helper to a consistent 0.8 s. The "bench" is where a frozen process waits while the chip is in the kernel: draw it as an outline copy (`make_translucent`) of the process with `ready` expression. Step 9 is a replay with a slower pace to show the stack.

### S07 — Where does a trap go? The trap table   (beats: B06) · ~1:15
**Purpose:** the kernel, not the program, decides where traps go; the trap table is installed at boot, via a privileged instruction; system-call numbers are an indirection that protects.
**Starts with:** S06 end state (A running, user seat).
**Layout:** a **Trap table** card centered in the kernel zone (0, −1.7), 3.6 × 1.9 (initially empty). Above the line, A at the user seat. A sticky note and a boot button appear along the way.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Wait. The trap jumps into the kernel. *Which* code? Does the program say?" | Student (curious). A holds a sticky note (`sticky_note`) with "jump to 0x…". A dotted arrow from the note points to a kernel-zone box labeled "check permission", with a second box "do the work" just past it. |
| 2 | "It must never say. A program that picks any address in the kernel could jump just past a permission check." | Professor (worried). The arrow lands on "do the work", skipping "check permission". A red bounding flash. |
| 3 | "That's a Very Bad Idea." | The sticky note crumples and a big red `x_mark` over it (a small joke: the note bounces off the boundary and drops back to A). |
| 4 | "So the kernel decides in advance. At boot the machine starts in kernel mode, free to configure the hardware." | A and the user seat fade; the chip is at the kernel seat with the OS token. A "BOOT" power switch (`PowerSwitch`) flips on at the left. The gauge reads KERNEL (red). |
| 5 | "One of the first things the OS does is install a **trap table**…" | Term highlight "trap table". The trap-table card draws in at center, empty. The OS token writes three rows into it, one by one: `syscall`, `timer`(grayed for now? no, shown dim), `keyboard`. |
| 6 | "…it tells the hardware what code to run on a disk interrupt, a keyboard interrupt, a system call." | Each row is linked to a small handler box (below the card) by an arrow. The CPU chip shows a tiny "remember" tag; the table's address (`0x…`) is copied into a small slot on the chip. |
| 7 | "Those are the **trap handlers**, and the hardware remembers them until the next reboot." | Term highlight "trap handlers". A small "remembered" lock icon closes on the chip's slot. |
| 8 | "Installing the table is itself a privileged instruction." | A small label "privileged" in `KERNEL_COLOR` sits on the arrow that loads the table address into the chip (no specific x86 instruction is shown). |
| 9 | "And if I *could* install my own table?" | Student (excited). A mischievous A (user seat reappears, scale 0.8) holds its own tiny table with rows reading "my code". |
| 10 | "Then every trap would run your code, in kernel mode. You'd own the machine." | Professor (explaining). A's table tries to cross the boundary and is blocked by a padlock (`padlock`) flashing red. The gauge stays KERNEL for the real table. |
| 11 | "The program doesn't give an address. It gives a **system-call number**." | Term highlight "system-call number". A hands over a small card with "#5" (a number tag) via a register cell labeled `eax`. |
| 12 | "The handler checks that it's valid and runs the matching code." | The handler (OS token) looks at the number: a green tick, then the card index 5 highlights a row ("open") in the trap table; the matching handler box lights. |
| 13 | "That indirection is **protection**: user code can only *request* a service." | Term highlight "protection" (small). A thin outline "request ✓" vs. "jump ✗" appears around the two ideas (sticky note ✗, number ✓). |
| 14 | "And the kernel stays suspicious even then. A `write()` whose buffer points inside kernel memory must be refused." | A Tip card slides in (`TIP`, `DIM` frame): "Be wary of user inputs." A `write(fd, buf, n)` code line, with `buf` an arrow into a red kernel-memory column; a red `x_mark` rejects it. |

**Characters:** Student (curious → excited), Professor (worried → explaining).
**Ends with:** a kernel zone with the filled trap table, the chip on the kernel seat; the Tip card slid out. The next scene resets to the user seat.
**Implementation notes:** `TrapTable` is a new reusable prop (see New assets). The "boot" scene is the only place where `PowerSwitch` is reused. Keep text per frame minimal: rows are short ("syscall → handler").

### S08 — The whole protocol   (beats: B07) · ~1:30
**Purpose:** assemble boot + run into **Figure 6.2**. Pay off the "special mechanism that jumps to `main()`" promise from episode 04.
**Starts with:** S07 end state.
**Layout:** a three-column **ProtocolChart** fills the screen: columns "OS (kernel mode)" (x = −4.5), "Hardware" (x = 0), "Program (user mode)" (x = 4.5), rows 0.4 tall (font 20), time going downward, y from 2.4. A small live thumbnail of the LDE world (boundary, chip, gauge) sits at the bottom-right corner (5.2, −2.4), scale 0.35, showing where the chip is. Section header "OS @ boot" then "OS @ run".

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Let's put it together. Limited direct execution has two phases." | The chart frame draws. A header "OS @ boot (kernel mode)" writes at the top-left. |
| 2 | "At boot, in kernel mode, the OS initializes the trap table, and the hardware remembers the system-call handler." | Rows: OS: **initialize trap table** (bold = privileged); Hardware: `remember address of… syscall handler`. The trap-table icon pulses; the thumbnail chip is at the kernel seat. |
| 3 | "Then, to run a process, the OS creates the entry, allocates memory, loads the program, sets up the stack." | The boot block shrinks upward; the header "OS @ run" appears. OS rows write: `Create entry for process list`, `Allocate memory for program`, `Load program into memory`, `Setup user stack with argv`. |
| 4 | "It fills the *kernel stack* with the starting registers, and executes a **return-from-trap**." | Row `Fill kernel stack with reg/PC` and bold `return-from-trap`. The thumbnail shows a packet landing on `k-stack(A)`. |
| 5 | "A return? From a trap that never happened?" | Student (surprised). A "?" pops over the return-from-trap row. |
| 6 | "A pretend return. That's the 'special mechanism' I promised in episode four, the one that jumps to `main()`." | Professor (proud). The "→ Ep. 06" tag from 04's S12 flies in from the left and lands on the row, then turns into a tick and fades (payoff). |
| 7 | "The hardware restores the registers, moves to user mode, and jumps in." | Hardware rows: `restore regs (from kernel stack)`, `move to user mode`, `jump to main`. The thumbnail chip rides up; the gauge → USER. Program column: `Run main()`. |
| 8 | "The program runs. When it needs a service, it traps: registers saved, kernel mode, trap handler." | Program: `Call system call`, `trap into OS` (bold). Hardware: `save regs (to kernel stack)`, `move to kernel mode`, `jump to trap handler`. The chip rides down. |
| 9 | "The OS does the work, and returns from the trap." | OS: `Handle trap`, `Do work of syscall`, bold `return-from-trap`. |
| 10 | "The registers come back, user mode returns, and the program continues right after the trap." | Hardware: `restore regs`, `move to user mode`, `jump to PC after trap`. The chip rides up. Program: `...`. |
| 11 | "Finally `main()` returns into `exit()`, one more system call, and the OS cleans up." | Program: `return from main`, `trap (via exit())`. OS: `Free memory of process`, `Remove from process list`. |
| 12 | "The program ran directly on the CPU nearly the whole time." | On the right, a highlight bar sweeps the Program column (long, solid user-mode stretch) and the OS rows (short). Hold 1.5 s. |

**Characters:** Student (surprised), Professor (proud).
**Ends with:** the full Figure 6.2 chart. Transition: the chart slides left and shrinks to a small legend ("LDE protocol") in the top-left; the stage resets to the LDE world with A running at the user seat.
**Implementation notes:** adapt **Figure 6.2** exactly (rows in the book's order). Bold rows = privileged instructions. The chart scrolls vertically as rows are added (everything above is dimmed to 0.5 so the current row is always readable). Two phases are kept as two stacked tables (boot, run), like the book.

### S09 — Problem 2: when the OS isn't running   (beats: B08, first half) · ~0:45
**Purpose:** the second problem: the OS cannot act while a process runs. Pose the crux.
**Starts with:** the LDE world: chip at the user seat, A running; B on the B bench (ready outline). The chart legend is docked at the top-left.
**Layout:** LDE world. The OS token rests next to the trap table in the kernel zone (−4.4, −1.7).

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Problem number two: switching between processes. Sounds simple: just stop one and start another." | B appears on its bench (ready outline, mint). A on the CPU. An arrow from the OS token to A: "stop" and from the token to B: "start" (dotted, hopeful). |
| 2 | "But if a process is running on the CPU, then by definition the OS is *not* running." | Professor (thinking). A is on the chip. The OS token goes translucent (dims to 0.3) with a small "zZ". The dotted arrows break. |
| 3 | "And if the OS isn't running…" | The token's arms flail at the boundary; nothing. |
| 4 | "…it can't do anything about it." | Student (confused). A "locked out" padlock on the token. |
| 5 | (crux card) | A Crux strip drops from the top (accent `VIRT`): **"How to regain control of the CPU?"** with the subtitle "...so that it can switch between processes?" (font 22). Hold 1.2 s, then it docks as a thin strip. |

**Characters:** Professor (thinking), Student (confused).
**Ends with:** LDE world (A running, B on the bench, the OS token dim), crux strip at top.

### S10 — The cooperative approach   (beats: B08, second half) · ~0:45
**Purpose:** cooperative scheduling: trust, `yield`, illegal operations, and the hang-forever failure that leads to "reboot".
**Starts with:** S09 end state.
**Layout:** LDE world. A "trust" ribbon label appears at the top center (0, 2.9) in `DIM`: "cooperative: the OS trusts the process".

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Early systems, like the first Macintosh, took the **cooperative approach**: the OS *trusts* processes to give up the CPU periodically." | Term highlight "cooperative approach". The "trust" ribbon writes. A small `ep_tag`-style tag "early Mac, Xerox Alto" (font 20, `DIM`). |
| 2 | "And most do, through system calls." | A makes a system call (`cpu_ride` down), the chip is at the kernel seat with the OS token. The OS token wakes (opacity 1.0). |
| 3 | "Some systems even have an explicit `yield` call that does nothing but hand over the CPU." | A `yield()` code chip pops over A, and the token directly swaps A for B: A hops to the A bench, B hops onto the chip, the chip rides up. B running (mint). |
| 4 | "A process that does something illegal, like dividing by zero, also traps into the OS, which will probably terminate it." | B shows a `1/0` badge; a trap arrow crosses the line; the token stamps a red `x_mark` on B; B fades out (done). A goes back on the chip. |
| 5 | "And if a program loops forever, and never makes a system call?" | Student (curious). A hops back on; A spins with the loop arrow. A tick counter beside the chip reads "tick 1, 2, 3 …" climbing. The OS token sleeps (dim). |
| 6 | "Then there's one cure, the oldest in computing: reboot the machine." | Professor (worried). The Computer pops up at bottom-center (0, −2.9), scale 0.6, overwhelmed → error. A power switch (`PowerSwitch`) flips off and on. The screen blinks to black for 0.3 s and comes back with a fresh, empty CPU. |
| 7 | "That's the plan?" | Student (sad). Pause 1 s. |
| 8 | (short tip) | A small Tip card slides in from the right, "TIP: Reboot is useful" with three short rows: "known state", "reclaims leaked resources", "easy to automate". It stays 2.5 s, then slides out. |

**Characters:** Student (curious → sad), Professor (worried), Computer (overwhelmed → error).
**Ends with:** the LDE world, empty user seat (A gone after the reboot), the OS token awake. Transition: A and B respawn on their benches (ready) in S11.
**Implementation notes:** the Tip text must stay under ~25 words. The reboot gag is a quick fade-to-black, not a full redraw.

### S11 — The timer interrupt   (beats: B09) · ~1:10
**Purpose:** the non-cooperative approach: a timer interrupt forces control back to the OS, set up at boot with a privileged instruction; the hardware saves state, as for a trap.
**Starts with:** S10 end state (respawned A and B).
**Layout:** LDE world. The **Timer** device at the top-right of the user zone (3.2, 2.4): a small alarm-clock icon in a hardware-grey box labeled "timer (hardware)". A crux strip at top: **"How to gain control without cooperation?"** (replaces the previous strip with a `Transform`).

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "The answer was found many years ago, and it's simple: a **timer interrupt**." | The crux strip transforms to the new question. The timer box slides in. Term highlight "timer interrupt". A runs on the chip in an infinite loop (loop arrow). |
| 2 | "A timer device can be programmed to raise an interrupt every few milliseconds." | The alarm clock face's hand spins; every 1 s a small bell ring animation (waves) fires. A small label "every X ms" with a tick mark on a mini Timeline. |
| 3 | "When it fires, the running process is halted, whatever it was doing…" | The timer rings; a lightning bolt flies from the timer to the CPU chip. A freezes (outline), regardless of the loop. |
| 4 | "…and a pre-configured **interrupt handler** in the OS runs." | The chip rides down across the line (gauge → KERNEL); the OS token hops on. Term highlight "interrupt handler". The trap table's `timer` row lights; a handler box lights. |
| 5 | "The OS has regained control. It can stop this process and start another." | The token looks at A and B (two thought bubbles with "keep A?" / "run B?"); no decision yet. Student (excited). |
| 6 | "The OS prepares this at boot, like the system-call handler." | Replay quickly (as a flashback): the boot power switch; the token adds the `timer` row to the trap table, which was dim until now (it was blank in S07 for this reason). |
| 7 | "It tells the hardware which code to run when the timer fires, and it *starts the timer*, a privileged operation." | A "START" button on the timer box is pressed by the token's arm; the box lights green; "privileged" tag in `KERNEL_COLOR`. A user-mode A tries to reach the timer and is bounced off by the boundary (`flash_at`). |
| 8 | "The hardware does its part too: it saves the running program's state onto the kernel stack, the same dance as a trap, though this time the program never asked." | Rewind to the instant of the interrupt. A's register packet (coral) flies into `k-stack(A)` by itself (labeled "hardware"), while A stays frozen. A small label "A never asked" pops up. |
| 9 | "So the process doesn't even notice?" | Student (curious). A's frozen face has no expression change. |
| 10 | "Like a movie paused and played again." | Professor (happy). A play/pause glyph pair (`PauseGlyph` / `PlayGlyph`) toggles over A; A resumes after return-from-trap (the chip rides up, A hops on). |
| 11 | "This is the **non-cooperative** approach: the OS takes control by force, with hardware help." | Term highlight "non-cooperative". The "trust" ribbon from S10 flips to "no trust needed". The timer box glows. A small Tip card "TIP: Use the timer interrupt to regain control" slides in briefly. |
| 12 | (tip) | A second tiny tip: "Misbehaving process? One strike, and you're out." (`TIP: Dealing with application misbehavior`), 3 s. |

**Characters:** Student (excited → curious), Professor (happy).
**Ends with:** LDE world with the timer active (ticking every 1 s), A frozen at the end of the scene, chip at the kernel seat. Timer, trap table (3 rows filled), `k-stack(A)` with A's packet.
**Implementation notes:** `AlarmClock` is a new simple icon (circle, two bells, two hands, `.ring()` = two curved waves). The flashback in step 6 is a 2 s quick-cut, not a full replay.

### S12 — The scheduler decides, then the switch   (beats: B10, first part) · ~0:30
**Purpose:** after regaining control, the OS decides (scheduler, policy, later episodes). If it switches, it runs a context switch, the "save slot" pay-off.
**Starts with:** S11 end state: chip at the kernel seat, the OS token on it, A frozen on its bench, `k-stack(A)` with A's packet.
**Layout:** LDE world plus a **save slot** icon (the episode-04 floppy) docked at (0, −3.0) near the bottom center, and a **scheduler spotlight** icon above the token (spotlight from episode 04, small).

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Now the OS is back in control, by a system call or a timer interrupt." | The token on the chip. Two small arrows enter it: a trap arrow from a system-call door and a bolt from the timer. |
| 2 | "It must decide: keep running this process, or switch?" | The spotlight (policy icon from 04) hovers over A and B (on their benches), swinging between them without landing. |
| 3 | "That's the job of the **scheduler**, and its policies fill the next episodes." | Term highlight "scheduler". A tag "→ Ep. 07–10" sticks on the spotlight. (Callback: policy = *which*.) |
| 4 | "If the decision is to switch, the OS runs a low-level piece of code: the **context switch**." | The spotlight stops on B. The gears icon (mechanism, from 04) appears on the token and spins. Term highlight "context switch". |
| 5 | "Remember the save slot from episode four?" | The **save slot** icon (floppy) pops into center with a short glow. A faint ghost of the 04 S09 register bank and memory panels flickers behind it. |
| 6 | "The video-game save! Pause one, load the other!" | Student (excited). A's frozen outline grows a floppy badge; B's outline grows a "load" arrow. |
| 7 | "Exactly. Save a few registers of the running process, restore a few of the next one." | Professor (proud). Two floppy-like slots appear, one per process: `save slot (A)` and `save slot (B)`; an arrow goes from the chip into A's, and from B's into the chip. |
| 8 | "Then return-from-trap doesn't go back to the process that was interrupted. It goes into the *other* one." | A dotted return arrow from the kernel up to the user zone swings from A's bench to B's bench and stays on B. Hold 1 s. |

**Characters:** Student (excited), Professor (proud).
**Ends with:** the LDE world with save-slot icons for A and B, the dotted return arrow pointing to B. Transition: the slots shrink into the kernel zone as "proc(A)" and "proc(B)" cards (PCB cards from 04).

### S13 — Watching a context switch   (beats: B10, second part) · ~1:00
**Purpose:** step through Figure 6.3: A running → timer interrupt → `switch()` → B running; two kinds of saves.
**Starts with:** S12 end state, rearranged: the Timeline at the bottom (y = −3.1, x −3.5..3.5, rows `A`, `B`, `OS`, 1 unit tall in total, scale 0.8). A running (user seat), B on its bench, `proc(A)` and `proc(B)` PCB cards in the kernel zone at (−1.4, −1.8) and (1.4, −1.8) (1.6 × 1.0), `k-stack(A)` and `k-stack(B)` at (−4.4, −1.6) and (4.4, −1.6). All the kernel items are inside the kernel zone, so the chip's kernel seat is at (0, −0.9) in this scene (chip scale 0.7). This is the only scene with this variant.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Watch it with A and B." | The layout settles. Timeline row A has a few coral running blocks already (ticks 1–3). |
| 2 | "A is running." | A on the chip (user seat). Timeline: A's next block fills (solid coral). |
| 3 | "The timer fires." | The alarm bell rings; a bolt flies to the chip. Timeline: the OS row's first block begins. |
| 4 | "The hardware saves A's registers on A's kernel stack and enters the kernel." | A's coral packet flies from A into `k-stack(A)`; the chip rides down, gauge → KERNEL, the token hops on. Caption "hardware: save regs(A) → k-stack(A)" (font 18). |
| 5 | "The handler decides to switch, and calls `switch()`." | The token looks at B; a `switch()` code chip pops up above it (`MONO_FONT`). Timeline: the OS block keeps growing. |
| 6 | "That routine saves A's current registers into A's process structure…" | A kernel-colored packet (red cells, "kernel regs") flies from the token into `proc(A)`. Caption "OS: save regs(A) → proc(A)". |
| 7 | "…restores B's from B's process structure…" | A mint-red packet flies from `proc(B)` into the token. Caption "OS: restore regs(B) ← proc(B)". |
| 8 | "…and switches the stack, to B's kernel stack." | A small pointer arrow (`SP`) on the token swings from `k-stack(A)` to `k-stack(B)`. The stack trays swap emphasis (A's dims, B's glows). |
| 9 | "Then the OS executes return-from-trap." | The `switch()` chip fades. The token raises its hand with a "return-from-trap (into B)" tag in bold. |
| 10 | "The hardware restores B's registers, moves to user mode, and jumps to B's program counter. B is running." | B's mint packet flies from `k-stack(B)` into B; the chip rides up; the gauge → USER; B hops from its bench onto the chip (running). Timeline: B's solid mint block begins; the OS row's block ends. A is now on its bench (ready outline). |
| 11 | "So there are two kinds of saving?" | Student (confused). Two question marks pop over the two packet trails. |
| 12 | "Yes. When the timer fires, the *hardware* saves the user registers on the kernel stack." | Professor (explaining). Highlight path 1 (coral → `k-stack(A)`) and tag it "hardware · implicit". |
| 13 | "When the OS switches, the *software* saves the kernel registers into the process structure." | Highlight path 2 (red → `proc(A)`) and tag it "software · explicit". |
| 14 | "That second save makes the system look as if it trapped into the kernel from B, not from A." | The ghost of the chip (translucent) slides from "trapped from A" to "trapped from B" at the kernel seat; the kernel stacks swap labels. |
| 15 | "We enter `switch()` in A's context and leave it in B's." | A bracket on the Timeline's OS block, labeled "enter as A → leave as B". Hold 1.5 s. |

**Characters:** Student (confused), Professor (explaining).
**Ends with:** the Timeline: A (coral), OS (red), B (mint); B running on the chip; `k-stack(A)` holds A's packet; A on its bench.
**Implementation notes:** adapt **Figure 6.3** (the three-column listing is NOT shown again here; we use the stage + Timeline instead, and the figure's key lines appear as captions). Use the `OS` row in the Timeline (new row, `KERNEL_COLOR`). Keep at most 3 captions on screen at once (fade old ones).

### S14 — The xv6 code   (beats: B10, third part) · ~0:30
**Purpose:** show that the context switch is real code (xv6 `swtch`): save into old, load from new, switch the stack, return.
**Starts with:** S13 end state.
**Layout:** the stage fades to 20%; a **Code block** (xv6 `swtch`, trimmed from Figure 6.4, about 12 lines, font 18, `MONO_FONT`) at the left-center (−1.5, 0.3). A small kernel-stack icon at the right (4.4, 0.4), plus the save-slot icon.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "In xv6, that's a few lines of x86 assembly:" | The Code block fades in, adapted from Figure 6.4: `swtch:` / `# save old registers` (`movl 4(%esp), %eax`, `popl 0(%eax)`, `movl %esp, 4(%eax)`, `movl %ebx, 8(%eax)` …) / `# load new registers` (`movl 4(%esp), %eax`, `movl 4(%eax), %esp`, `pushl 0(%eax)`, `ret`). Caption "xv6 (Figure 6.4, trimmed)". |
| 2 | "store the registers into the old context…" | The highlight bar covers the `save old` block; the save-slot icon at the right glows and a red packet flows into it (labeled "old"). |
| 3 | "…load them from the new one…" | The highlight moves to the `load new` block; a packet flows out of a second slot (labeled "new") into a CPU chip glyph. |
| 4 | "…switch the stack…" | The single line `movl 4(%eax), %esp` (the stack switch) highlights in `CPU_COLOR`; the stack icon's pointer swings from one tray to the other. |
| 5 | "…and `ret`." | The last line highlights. A small tag: "returns into the new process". Hold 1.2 s. |

**Characters:** none on screen (Professor neutral in the corner, optional).
**Ends with:** the Code block highlighted at `ret`. Transition: the block fades; the stage returns at full brightness for S15, with the Timeline still showing A / OS / B.
**Implementation notes:** reuse the episode-04 `Code` setup (monokai, `MONO_FONT`, small). AT&T syntax, so keep the `%` registers. Trim the book's listing to at most 12 lines; pick lines that make the three blocks visible: save, load, stack switch.

### S15 — How long? And what about concurrency?   (beats: B11) · ~0:50
**Purpose:** give the cost of traps and switches (microseconds), and flag the "interrupt during a system call" worry, deferred to concurrency.
**Starts with:** S14 end state (stage restored).
**Layout:** an Aside card on the right (2.6, 0.4), 5 × 3.6. A Timeline reappears at the bottom-left.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "How long does all this take?" | An Aside card "ASIDE: How long do context switches take?" slides in; a big stopwatch icon (`stopwatch`) pulses. |
| 2 | "In 1996, on a 200-megahertz machine, a system call took about four microseconds, and a context switch about six." | Two horizontal bars grow in the card: "system call ≈ 4 µs" and "context switch ≈ 6 µs" (a `MathTex(r"\approx")`, not the Unicode glyph) with a small label "Linux 1.3.37 · 200 MHz". |
| 3 | "Modern systems do almost ten times better." | Both bars shrink to about a tenth, relabeled "< 1 µs". |
| 4 | "Not everything speeds up with the CPU, though: many OS operations are bound by memory bandwidth." | A tiny bar "CPU speed ↗" climbing, next to a flatter bar "memory bandwidth" (`DIM`). |
| 5 | "What if a timer interrupt fires *during* a system call?" | Student (confused). The Aside card slides out. The chip is at the kernel seat with the token running a handler (progress bar); a second bolt from the timer arrives and hits the token mid-work. A "!" bursts. |
| 6 | "Good question, and the answer belongs to the whole second piece of this series." | Professor (happy). A tag "→ Concurrency" appears (using `ep_tag`-like styling, "Part II"). |
| 7 | "One simple trick is to **disable interrupts** while handling one, but not for long, or you lose some." | Term highlight "disable interrupts". A small shield/gate (`ShieldGate`) drops in front of the timer; the second bolt bounces off, then queues up waiting; a "too long?" clock shows bolts piling up (fading away: lost). |
| 8 | "Real kernels also use **locking** to protect their data structures." | A padlock (`padlock`) closes on the `proc(A)` card. Term highlight "locking". |
| 9 | "Concurrency, later." | The padlock and gate fade; a "→ Part II" tag fades in and out. |

**Characters:** Student (confused), Professor (happy).
**Ends with:** the LDE world, calm, no extras.
**Implementation notes:** the 1996/modern figures come from the Aside in the book. Do not overstate "ten times better": the narration says "almost" (the book says "almost an order of magnitude").

### S16 — Baby-proofing the CPU   (beats: B12) · ~0:40
**Purpose:** the big picture: set the limits up front, then let the process run free.
**Starts with:** S15 end state.
**Layout:** the LDE world dims to 40% and shrinks to the right half. At left, a **playroom** (a soft-rounded rectangle, 5 × 3.2, `DIM` outline) with a baby-play Process creature (A) in the middle.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "This is how the world works, too." | The playroom draws in. A (smaller, scale 0.6) sits on a rug. |
| 2 | "When parents baby-proof a room, they lock the cabinets with dangerous things and cover the electrical sockets." | A cabinet with a `padlock` appears (left), then a wall socket with a cover. Each icon pops in `GrowFromCenter`. |
| 3 | "Once that's done, the baby can roam freely, and the parents can relax." | A wanders happily left and right; a small happy parent figure (just a Professor head-and-shoulders, scale 0.5, neutral → happy) in a corner of the room. |
| 4 | "The OS baby-proofs the CPU." | The room's three items map to the LDE world on the right with arrows: cabinet lock → user mode (dashed boundary); socket cover → trap table; wall clock → timer. The LDE world un-dims. |
| 5 | "At boot it sets up the trap handlers and starts the timer." | The trap table and the timer light up one by one (each with the boot power switch icon). |
| 6 | "Then it runs processes only in restricted mode, at full speed, and steps in only for privileged operations, or when a process has held the CPU too long." | A runs on the chip at the user seat (full speed, a "FAST" tag in green from S01), the OS token asleep; two little interventions: a trap and a timer interrupt briefly send the chip down and back (two quick crossings), then A is back. |
| 7 | "So that's the 'limited' in limited direct execution!" | Student (excited). The word "limited" in the term strip pulses. |
| 8 | "That's the 'limited.'" | Professor (proud). Hold 1.5 s. |

**Characters:** Student (excited), Professor (proud).
**Ends with:** the LDE world fully lit, the playroom on the left, the term strip "limited direct execution" glowing. Section badge `FadeOut` at the end.
**Implementation notes:** `cabinet_lock` and `socket_cover` are small new icons (see New assets). The Professor cameo in the room is optional; if it looks cluttered, drop it.

### S17 — Recap   (beats: B13) · ~0:35
**Purpose:** five takeaways.
**Starts with:** S16 end state.
**Layout:** the world fades; a numbered list at left (−5.6..1), font 28, one line each; an icon per line at x = 4.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "So, today:" | The world `FadeOut`; header "Recap" in `VIRT`. |
| 2 | "**Limited direct execution**: run programs directly for speed, within limits set up by the OS and the hardware." | Line 1 writes; icon: a chip with a fence glyph around it. |
| 3 | "**User and kernel mode** protect the machine. Programs reach the kernel only through **system calls**: **trap** in, **return-from-trap** out." | Line 2; icon: the boundary with a trap arrow crossing and returning, plus the gauge flipping. |
| 4 | "The **trap table**, installed at boot, is the only place a trap can go." | Line 3; icon: the trap-table card with a padlock. |
| 5 | "The **timer interrupt** lets the OS regain control, even from a process that never cooperates." | Line 4; icon: the alarm clock ringing at a spinning process. |
| 6 | "A **context switch** saves one process's registers and restores another's." | Line 5; icon: the save slot with a swap arrow (A coral ↔ B mint). Hold 1.5 s. |

**Ends with:** the full recap list. Section badge fades out.

### S18 — Teaser: who runs next?   (beats: B14) · ~0:25
**Purpose:** hook for 07: the mechanism is done, the policy question remains.
**Starts with:** S17 end state.
**Layout:** dialogue mode. A **Queue** (A, B, C, label "Ready") at center (0, 0.6), with a **Spotlight** above it.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "So the OS can take the CPU back whenever it wants, and swap one process for another. Great. But *when* should it? And *who* should it pick?" | The recap list fades. Student and Professor move to dialogue positions. Student (curious). The Queue of A, B, C builds (coral, mint, gold) with a CPU chip above it. |
| 2 | "Ah. That's no longer a mechanism question. That's a policy question." | Professor (happy). The mechanism gear icon (spinning, dimmed) on the left; the spotlight (policy) lights on the right. |
| 3 | "The machinery is done. Next time we meet the scheduler." | The spotlight sweeps across A, B, C without landing. Cut to black (FadeOut all, 0.5 s). Then "Next: 07 · CPU Scheduling" in `TEXT` with a `VIRT` dot. Hold 2 s. |

**Characters:** Student (curious), Professor (happy).
**Ends with:** black end card.

## New assets needed
Nothing below exists in `ostep_lib` yet (the core, overview and episode-04 props are reused as much as possible).
- **`ProtocolChart(columns, rows)`**: the book's Figures 6.1 / 6.2 as a reusable multi-column listing. Header row with column titles, a rule, rows that `.write_row(col, text, bold=False)` returns an animation for, a moving highlight cursor, auto-dim of rows above the current one, and vertical auto-scroll. Works with 2 or 3 columns. Bold text = privileged / key instruction.
- **`KernelToken`**: a rounded red `KERNEL_COLOR` "OS" badge (0.9 × 0.55) that can stand on a `CPU` seat (`seat(cpu)`), with `.dim()`, `.wake()`, and a small arm (line) that can `.reach(point)`. It is the OS "running".
- **`cpu_ride(chip, seat, boundary, gauge)`**: helper animation: the chip slides vertically along an arc between the user seat and the kernel seat, triggers `boundary.flash_at(...)`, and flips the gauge at the midpoint.
- **`RegPacket(owner_color, labels=None)`**: three tiny cells in a row, filled in the owner's color (red = kernel regs); methods `.fly_to(point)` / `.fly_into(mob)` (move + shrink on arrival) and optional PC / flags labels.
- **`KernelStack(label)`**: narrow tray (1.6 × 1.4) with a label such as `k-stack(A)`; `.push(packet)` / `.pop()` animations, `.glow()` / `.dim()`.
- **`TrapTable(rows)`**: card (3.2–3.6 × 1.9) with a `KERNEL_COLOR` frame, header "TRAP TABLE", rows like `syscall → handler`; `.add_row(...)`, `.highlight_row(i)`, an optional `.padlock` that closes on it.
- **`AlarmClock`**: circle with two small bells on top, two hands, `.ring()` (two curved waves + a small shake), `.start()` / `.stop()` states, labeled "timer (hardware)".
- **`ShieldGate`**: a short vertical bar/gate that drops in front of an arrow or bolt (`.close()`, `.open()`), for "disable interrupts".
- **Icons:** `cabinet_lock` (a cabinet with a padlock), `socket_cover` (a wall socket with a cover), `fence_glyph` (a short fence, for "limited"), `magnifier`, `door_in_line` (the small doorway in the boundary), `booth_gate` (the permission check booth in S04). All simple Manim primitives.
- **Timeline `OS` row:** an extra row type for `Timeline` with `KERNEL_COLOR` solid blocks (the episode-04 `Timeline` supports custom colors; confirm the row label "OS" works there).
- **Bench:** a `bench(process)` helper: translucent copy of a process with an outline ring, used for "frozen / waiting" processes.

## Open questions
- **Chip rides the line vs. a fixed CPU:** the whole episode relies on the CPU chip physically moving between a user seat and a kernel seat. If this feels too cartoonish compared with 04's fixed chip, the fallback is a fixed chip with a color ring and only the OS token / process swapping on it. OK to go with the chip riding?
- **Pace of S06–S08:** they are the densest scenes (three scenes for trap, trap table and the protocol). If the episode feels long, S08 (Figure 6.2) could shrink to the highlights only. Keep the full chart?
- **Figure 6.3 vs. the stage in S13:** the book's Figure 6.3 is a three-column listing. I chose to show it as an animated stage with the Timeline instead (we already showed the three-column format in S08). Is that OK, or should S13 also show the book's figure (as a small corner legend)?
- **The OS token:** a red "OS" badge on the chip is a new recurring prop. Should it be added to the bible's props table?
- **xv6 `swtch` (S14):** trimmed to ~12 lines in AT&T syntax. Is that the right level for this audience, or should it be a cartoon of the code instead of real assembly?
- **Professor cameo in S16:** a mini Professor "parent" in the playroom is a joke that may clutter. Keep, or drop it?
- **Reboot gag in S10:** the black-out blink might look like a render glitch. OK, or replace it with a quick "power cycle" animation on a laptop icon?
