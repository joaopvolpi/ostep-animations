# 15 — Mechanism: Address Translation
> Section: Virtualization · Source: Ostep/Chapters/15-vm-mechanism.pdf · Est. duration: ~16:00 (~2,150 spoken words ≈ 14:20 of narration, plus pauses)

## Logline
Every program believes its memory starts at address zero and belongs to it alone, yet there is only one RAM. This episode is limited direct execution for memory: a tiny piece of hardware adds a **base** to every address and checks it against a **bounds**, and the OS sets it up at boot, at process start, and at every context switch.

## Learning goals
- After watching, the viewer can explain **address translation**: `physical address = virtual address + base`, performed by the hardware on every memory reference.
- Explain what the **bounds** register adds (protection) and trace a legal and an out-of-bounds translation by hand.
- List the hardware support needed (modes, base/bounds registers, privileged instructions to change them, exceptions) and recognize it as "LDE for memory".
- List the OS's jobs: allocate (free list) at process creation, reclaim at termination, save/restore base and bounds at context switch, install exception handlers at boot.
- Read the book's boot and runtime timelines (Figures 15.5 and 15.6), and explain **internal fragmentation**, the flaw that motivates segmentation.

## Concepts covered
| Term | Definition (book's wording or faithful paraphrase) | Beat |
|---|---|---|
| Address translation (hardware-based) | On every memory access (fetch, load, store) the hardware changes the virtual address into the physical address where the data really is. | B03 |
| Interposition | Inserting yourself on an interface (here: each memory reference) to add functionality without changing the client. | B03 |
| Transparency | The process has no idea its memory was relocated or that its addresses are translated. | B05 |
| Static relocation / loader | Early software trick: the loader rewrites the program's addresses before running. No protection, hard to move later. | B05 |
| Base register | Hardware register holding where the address space starts in physical memory; added to every virtual address. | B06 |
| Dynamic relocation (base and bounds) | Translation done at run time by hardware, so address spaces can even move after the process has started. | B06 |
| Virtual address / physical address | The address the process generates / the address that actually goes to memory. | B06, B07 |
| Bounds (limit) register | Holds the size of the address space; the hardware checks every virtual address against it. | B08 |
| Exception | The CPU stops the user program and runs an OS handler when it does something illegal (out of bounds, privileged instruction). | B08 |
| Memory management unit (MMU) | The part of the CPU that helps with address translation; for now the base and bounds registers plus a little circuitry. One pair per CPU. | B08 |
| Privileged instructions | Instructions, usable only in kernel mode, that change base/bounds or register exception handlers. | B09 |
| Free list | A list of the ranges of physical memory not in use; the OS's data structure for allocating address spaces. | B10 |
| Process structure / PCB | Per-process record where the OS saves the base and bounds at a context switch. | B10 |
| Exception handler | OS code, installed at boot, that runs when the hardware raises an exception. | B11 |
| Internal fragmentation | Space inside an allocated unit that goes unused (here, the gap between heap and stack). | B14 |

## Script

### B01 — Two programs, one address  `cold open` (~0:40)
**Student** (curious): Last time you told me every address my program prints is a virtual one, and that every program thinks its memory starts at zero.

**Professor** (explaining): Right. Program A keeps a variable at fifteen kilobytes. Program B keeps its own variable at fifteen kilobytes too.

**Student** (confused): The same address. And neither one overwrites the other?

**Professor** (happy): Neither. And there is only *one* RAM.

**Student** (surprised): So somebody is lying.

**Narrator (V.O.):** Somebody is. The illusion is beautiful, and today we build it. And not slowly: it has to happen on *every* instruction fetch, every load, every store.

*Visual idea:* Two address-space columns (A coral, B mint), each with a cell at 15KB; arrows from both aim at the same cell of a single physical column. Collision flash, then a "?" between the arrows and the column.

### B02 — The Crux  `crux` (~0:35)
> **THE CRUX: HOW TO EFFICIENTLY AND FLEXIBLY VIRTUALIZE MEMORY**
> How can we build an efficient virtualization of memory? How do we provide the flexibility needed by applications? How do we maintain control over which memory locations an application can access, and thus ensure that application memory accesses are properly restricted? How do we do all of this efficiently?

**Narrator (V.O.):** Three words in that question. **Efficiency:** programs run at full speed, which needs hardware help. **Control:** no program touches memory that isn't its own, and no program touches the OS. And **flexibility:** programs use their address space however they like.

**Narrator (V.O.):** That should sound familiar. Efficiency and control: that was the whole story of limited direct execution.

*Visual idea:* Crux card (VIRT accent). Below it, three icons appear (stopwatch, padlock, open hand) labelled efficiency, control, flexibility. The first two glow and a ghost of the episode-06 "user/kernel line" slides behind them.

### B03 — LDE, again, for memory  `build-up` (~1:00)
**Student** (curious): So what's the trick? Same as for the CPU?

**Professor** (explaining): Same philosophy. Remember limited direct execution: let the program run directly on the hardware, and step in only at key moments.

**Narrator (V.O.):** For memory, the program just runs. Its instructions fetch, load and store *directly*, no OS in the way. But on each of those memory references the **hardware** quietly steps in. It takes the address the program used, and changes it into the address where the data really is. That is **address translation**.

**Narrator (V.O.):** The hardware alone can't virtualize memory. It only provides the fast, low-level mechanism. The OS has to get involved at a few key moments: to set the hardware up, to keep track of which memory is free and which is used, and to step in when something goes wrong.

**Professor** (proud): There's a name for what the hardware does here: **interposition**. It sits in the middle of an interface, and adds a power the client never asked for. Notice that the program doesn't change at all. That's called transparency, and we'll get to it.

**Narrator (V.O.):** Same recipe as episode six: hardware does the fast part, the OS does the setup and the policing.

*Visual idea:* A CPU with every memory arrow passing through a thin ring ("translator") on its way to physical Memory; the label on the arrow changes as it crosses. Beside it, a faded legend of episode 06 (chip on the user/kernel line). Tip card: interposition is powerful.

### B04 — A tiny program: x = x + 3  `build-up` (~1:15)
**Narrator (V.O.):** To make this concrete we need a tiny program and a tiny world. First, the world. We'll make three simplifying assumptions, and the book is honest about it: they're almost laughable. We'll relax them one by one in the next episodes. The address space is placed in physical memory **contiguously**. It is smaller than physical memory. And every address space is exactly the same size.

**Professor** (worried): Go ahead, laugh. It'll be the OS laughing at you later, when you try to understand TLBs. That's just how the OS rolls.

**Narrator (V.O.):** Now the program. One line of C: `x = x + 3`, where `x` is `3000`. The compiler turns it into three instructions: load `x` from memory into a register, add three, store it back. The instructions live at addresses 128, 132 and 135, in the code region near the top. The variable lives at fifteen kilobytes, on the stack, near the bottom of a sixteen-kilobyte address space.

**Narrator (V.O.):** Run it, and the process makes five memory references. Fetch the instruction at 128. Load from fifteen kilobytes. Fetch at 132. Fetch at 135. Store to fifteen kilobytes. Every one of these is a **virtual address**, the address the program *thinks* it is using.

*Visual idea:* Assumption strip (three padlocks, series style) flashes and docks small. Then Figure 15.1: a 16KB address-space column (code, heap, free, stack), the three instructions at the top with `x = 3000` at 15KB. A cursor walks the five memory references, lighting cells.

### B05 — Not at address zero  `build-up` (~1:15)
**Narrator (V.O.):** Here's the problem. From the program's point of view, its address space starts at zero and goes up to sixteen kilobytes. But the OS wants to put the process somewhere else, and not necessarily at zero. In this physical memory of sixty-four kilobytes, the OS keeps the first sixteen for itself, and puts our process at thirty-two kilobytes.

**Student** (confused): So when the program asks for address 128…

**Professor** (explaining): …it has to actually reach 32,896. We need to **relocate** the process, and do it **transparently**: the program must never notice.

**Student** (curious): Easy. Before running, rewrite every address in the program. Add thirty-two thousand to each.

**Professor** (thinking): Funny, that's exactly what early systems did. It's called **static relocation**. A piece of software, the **loader**, rewrites the addresses in the executable before it runs.

**Student** (excited): Problem solved!

**Professor** (worried): Not quite. First, no protection. Nothing stops the program from computing a bad address, and touching another process or the OS. Second, once placed, the address space is hard to move.

**Narrator (V.O.):** We want hardware to do this at run time.

*Visual idea:* Figure 15.2: physical column (OS grey 0–16KB, free, a 16KB slot at 32KB for A, free). A's address-space column slides from the left into the slot; its "0" lands on 32KB. Then a loader robot rewrites `movl 0x0(%ebx)` to `movl 32K…` in the code; one rewritten instruction points into the OS region and the Aside card flashes red. Aside card: software-based relocation.

### B06 — The base register  `build-up` (~0:45)
**Narrator (V.O.):** The idea comes from the first time-sharing machines of the late nineteen-fifties. The hardware gets two registers per CPU. The first is the **base** register.

**Narrator (V.O.):** When the program is written and compiled, it assumes it lives at address zero. When it starts running, the OS decides where it really goes in physical memory, and sets the base register to that. Here: thirty-two kilobytes.

**Narrator (V.O.):** From then on, every memory reference the process generates gets translated by the hardware. The rule is one line. **Physical address equals virtual address plus base.**

**Professor** (happy): That's all. An addition.

*Visual idea:* CPU chip with a small MMU region and a base-register cell. The OS token writes `32 KB` into it (kernel mode). The formula `physical = virtual + base` writes under the chip, with the words coloured: virtual (process color), base (kernel-ish), physical (MEM_COLOR).

### B07 — Translating one instruction at a time  `build-up` (~0:55)
**Narrator (V.O.):** Let's trace it. The program counter is 128. The hardware needs the instruction, so it first adds the base: 128 plus 32,768 is 32,896. The memory fetches from there.

**Narrator (V.O.):** The instruction executes: load from virtual address fifteen kilobytes. Again the hardware adds the base. Fifteen kilobytes plus thirty-two kilobytes is forty-seven kilobytes. That's where the 3000 really sits.

**Student** (curious): And the program has no idea any of this happened.

**Professor** (proud): None. It wrote 128 and 15K, and it saw its own data. That's the illusion. Because we translate at run time, the technique is called **dynamic relocation**. And because we can change the base later, even after the process has started, we can move address spaces around.

*Visual idea:* An address chip "128" (process color) travels from the CPU through the adder (+ base) and exits as "32,896" (MEM_COLOR), landing in the physical column. Repeat with 15KB → 47KB, the cell lights and `3000` flies back. Split view: left what A sees (still at 128, 15K), right what really happens.

### B08 — The bounds register and the MMU  `build-up` (~1:20)
**Student** (curious): The book said "base *and* bounds". Where are the bounds?

**Narrator (V.O.):** The second register is the **bounds** register, sometimes called the limit. It's there for protection. Before translating, the hardware checks: is this virtual address inside the address space? If the virtual address is greater than or equal to the bounds, or negative, the CPU raises an **exception**, and the process is probably terminated.

**Narrator (V.O.):** In our example the bounds is sixteen kilobytes. Let's try different numbers, the book's example: a tiny process with a four-kilobyte address space, loaded at sixteen kilobytes. Virtual address zero becomes sixteen kilobytes. One kilobyte becomes seventeen. Three thousand becomes 19,384. And 4,400? That's past the end of the address space. Fault.

**Narrator (V.O.):** Simplification: bounds can also hold the *end* address instead of the size; the check is then done after adding. Equivalent. We'll assume the size.

**Student** (curious): So where does all this circuitry live?

**Professor** (explaining): In the CPU. One pair of registers per CPU. The part of the processor that helps with translation is called the **memory management unit**, the **MMU**. For now it's two registers, an adder and a comparator. It will grow as we get more sophisticated.

*Visual idea:* A comparator gate (`<`) is added in front of the adder inside the MMU. Chip passes: green tick. A bounds-cell "16 KB" appears next to base. Then four address chips in a row on the table (0, 1KB, 3000, 4400): the last bounces off the comparator, a red bolt (exception) leaves the CPU. The MMU box is outlined and named (Term highlight).

### B09 — What the hardware must provide  `build-up` (~1:10)
**Narrator (V.O.):** Let's collect what we need from the hardware. It's the same list as limited direct execution, extended.

**Narrator (V.O.):** One: two CPU modes, user and kernel, exactly as in episode six. Two: the base and bounds registers, as part of the MMU. Three: circuitry to translate and check bounds, which is quite simple. Four: **privileged instructions** to update base and bounds. Only in kernel mode. Five: privileged instructions to register exception handlers. And six: the ability to raise exceptions.

**Student** (excited): Why must changing the base be privileged?

**Professor** (worried): Imagine a user process that could set the base register while running. Set it to zero, and the whole machine is yours. Wreak havoc. Now quickly flush that thought from your mind.

**Narrator (V.O.):** So if user code tries to change base or bounds, it's the same story as in episode six: the CPU raises an exception, and the OS's handler for "tried to execute a privileged operation" runs. Same for an out-of-bounds access. And the hardware needs a way to be *told* where those handlers are. Remember the trap table? A few more privileged instructions fill it.

*Visual idea:* Six checklist items appear one at a time as small icons rather than text (gauge, register pair, MMU, padlock on registers, trap-table row, bolt). A user process tries to write the base register; a hand bounces off a padlock, "!" and the bolt hits the OS, which shows the "illegal instruction" row of the trap table lighting. Then the six items dock into the Figure 15.3 table.

### B10 — What the OS must do  `build-up` (~1:25)
**Narrator (V.O.):** Hardware gives us new features, and the OS gets new jobs. There are exactly four moments where it must act.

**Narrator (V.O.):** First, **when a process is created.** The OS has to find room for its address space. By our assumptions each address space is the same size and smaller than physical memory, so the OS sees physical memory as an array of slots, and tracks which are free in a data structure: the **free list**. Here, the free list has two entries, 16 to 32 kilobytes and 48 to 64 kilobytes.

**Narrator (V.O.):** Second, **when a process terminates**, gracefully or because it was killed. The OS takes its memory back and puts it on the free list, and cleans up related data structures.

**Narrator (V.O.):** Third, **at a context switch.** There is only one pair of base and bounds registers per CPU, and each process has different values. So when the OS stops a process, it saves the base and bounds into the process structure, the PCB. When it resumes one, it restores them.

**Student** (curious): So that's what lives in the PCB.

**Professor** (happy): Plus the registers you met in episode six. And because the OS controls the base, it can even move an address space. Deschedule the process. Copy the memory to the new place. Update the saved base. Resume, and the process wakes up, oblivious to its new neighborhood.

*Visual idea:* PCB card callback (A coral). Free-list card next to a 64KB physical column. B (mint) arrives: free-list entry highlights, base value flows into the PCB. B terminates: its slot becomes free again. A and B swap on the CPU: base and bounds register values flicker and swap through the PCB cards. Finally A's slot slides from 32KB to 48KB and its PCB base value ticks from 32 to 48.

### B11 — Booting the machine  `build-up` (~0:45)
**Narrator (V.O.):** The fourth moment is **exceptions**, and for that we go back to boot. The book shows boot and run as two timelines. First, the boot.

**Narrator (V.O.):** The machine starts in kernel mode. The OS initializes the trap table. The hardware remembers the addresses of the handlers: system call, timer, **illegal memory access**, and **illegal instruction**. The OS starts the interrupt timer. It initializes the process table and the free list.

**Student** (curious): So the trap table now has two new rows.

**Professor** (explaining): Right. The OS decides, in advance, what to do when a process misbehaves. And what it will do is usually not nice. It will most likely terminate the process. The OS is highly protective of the machine it is running.

*Visual idea:* Figure 15.5 as a 2-column ProtocolChart (OS @ boot | Hardware), "(No Program Yet)". The rows write in; trap-table card on a stage thumbnail gets its rows, now including the two new ones; the timer alarm clock starts.

### B12 — Running A and B  `build-up` (~1:40)
**Narrator (V.O.):** Now the run, Figure 15.6. To start process A, the OS allocates an entry in the process table, allocates memory for the process, sets the base and bounds registers, and executes a return-from-trap into A.

**Narrator (V.O.):** The hardware restores A's registers, moves to user mode, and jumps to A's first instruction. A runs. To fetch each instruction, the hardware translates the virtual address and fetches. For an explicit load or store, it checks that the address is legal, translates, and performs it. The OS isn't involved at all.

**Narrator (V.O.):** At some point the timer fires. The hardware moves to kernel mode and jumps to the timer handler. The OS decides to run B. It calls `switch()`: save A's registers into A's process structure, *including its base and bounds*; restore B's, including B's. Return-from-trap into B.

**Narrator (V.O.):** The hardware restores B's registers, moves to user mode, and B runs. And B executes a bad load: an address outside its bounds. The hardware says no: it moves to kernel mode and jumps to the trap handler. The OS decides to kill B, deallocates its memory, and frees its entry in the process table.

**Student** (excited): It's the same dance as episode six, with memory attached!

**Professor** (proud): Exactly. In most cases the OS just sets up the hardware and lets the process run directly. Only when a process misbehaves does the OS have to get involved.

*Visual idea:* Figure 15.6 as a 3-column ProtocolChart (OS | Hardware | Program) with a small stage thumbnail (CPU + MMU registers + physical memory) in a corner so the base register visibly changes at the switch and B's slot is freed at the end. Rows highlighted in sync, with the OS rows light and the Program rows long.

### B13 — The big picture  `big picture` (~0:30)
**Narrator (V.O.):** Step back. This is address translation: the hardware adds a base and compares to a bound on every reference, quickly. The result is the illusion we promised: each process has a private address space starting at zero, while many of them really sit in one memory, at different places. All of it transparent to the process.

**Narrator (V.O.):** And it gives us **protection**. Remember the process that scribbled over everything in episode six? Now it can't. If processes could overwrite memory freely, they could overwrite the trap table and take over the system. Without protection, the OS wouldn't be in control.

*Visual idea:* Illusion split. Left: A, B, C each see 0 to 16KB. Right: the physical column with three slots at three places. The scribbler from episode six reaches toward the OS region and bounces off the MMU (comparator lights red).

### B14 — The price: wasted space  `build-up` (~0:45)
**Narrator (V.O.):** Of course, there's a catch. Look at the slot of process A, thirty-two to forty-eight kilobytes. The code and heap are at the top. The stack is at the bottom. In between: free space the process isn't using, but that nobody else can use either. It's inside the slot we allocated.

**Narrator (V.O.):** This waste is called **internal fragmentation**: space *inside* an allocated unit that goes unused. Physical memory may have room for more processes, but we only offer fixed-size slots.

**Student** (sad): So most of the slot is air?

**Professor** (thinking): Most of it. We need something more flexible.

*Visual idea:* Zoom on A's slot: code and heap at the top, stack at the bottom, a large hatched "allocated but not in use" middle. Term highlight: internal fragmentation. A second process tries to squeeze in and bounces off the slot's wall.

### B15 — Recap  `recap` (~0:30)
**Narrator (V.O.):** So, today:
1. **Address translation**: the hardware turns each virtual address into a physical one, on every reference.
2. **Base and bounds**: add the base, check the bound. Fast, simple, transparent.
3. The hardware needs **modes, registers, privileged instructions and exceptions**; the OS needs a **free list**, a save and restore at context switch, and exception handlers set at boot.
4. **Protection**: a process can only touch its own address space.
5. The cost is **internal fragmentation**.

*Visual idea:* Five-item recap list with icons: adder (+) on the chip, base/bounds registers, hardware/OS checklist, MMU bouncing a scribbler, hatched slot.

### B16 — Teaser  `teaser` (~0:20)
**Student** (curious): The stack and the heap are tiny. Why give them a whole sixteen-kilobyte slot?

**Professor** (happy): What if we didn't? What if the code, the heap and the stack each got their own base and bounds?

**Student** (excited): Three pairs of registers, three little slots!

**Professor** (proud): That's the next episode: **segmentation**.

*Visual idea:* The 16KB column slices into code, heap and stack pieces that float apart to three different places in physical memory, each with its own tiny base/bounds tag. End card: "Next: 16 · Segmentation".

## Cut / deferred material
- **Homework (`relocation.py`, random base/limit, simulator questions):** cut. A "try it yourself" mention could go at the end.
- **References (M65, P90, SS74, S04, WL+93, W17) and footnote 1 ("wreak havoc" etymology):** cut. The "wreak havoc" joke is kept as one line (B09).
- **Footnote 2** (fixed-size stack below the code, heap growing): cut; it belongs to the flexibility discussion in the segmentation episode.
- **Bounds register stored as size vs. end address:** one sentence in B08, as a simplification note.
- **Details of free-list data structures:** only the term; real allocators come with free-space management (17).
- **x86 assembly specifics (`ebx`, `eax`, `movl`):** shown but not explained beyond "load, add, store".
- **Hardware extensions that grow the MMU (TLBs, page tables):** named in passing only (B04), covered from 18 on.

## Callbacks & setups
- Callbacks to earlier episodes:
  - **06 (LDE):** the whole episode is built as "LDE for memory": efficiency and control (B02), hardware + OS split (B03), user/kernel modes and privileged instructions (B09), trap table at boot (B11), return-from-trap, timer interrupt and `switch()` (B12), the scribbling process of 06 S01 (B13), the context-switch save/restore extended with base and bounds (B10, B12).
  - **13 (address spaces), assumed:** virtual addresses, the address-space layout, "every program thinks it starts at 0" (B01, B04). **14 (memory API), assumed:** `malloc`/`free` and the heap are just the process's own business inside its bounds.
  - **04 (process):** the PCB card, the save slot; **07:** the five padlock assumptions (B04, the three padlocks).
  - **Mechanism vs. policy:** the mechanism here is hardware + OS; the free-list policy (which slot) is deferred.
- Setups paid off in later episodes:
  - **Segmentation (16):** per-segment base and bounds, as a fix for internal fragmentation (B14, B16).
  - **Free-space management (17), paging (18), TLBs (19):** growing the MMU; the free list; relaxing the "same size" assumption.

## Open questions
- **Example sizes:** the book uses a 16KB process at 32KB (Fig 15.2) and then an unrealistically small 4KB process at 16KB for the translation table. I keep both, and say "different example, smaller numbers" in B08. Should the table instead use process A's real numbers (virtual 0, 1KB, 3000 → 32KB.., and 17KB → fault) for continuity? The book's table is in KB-aligned numbers that look nicer; I'd rather use gold process C for it.
- **Assumption (3) "all address spaces are the same size"** conflicts with the 4KB example. I flag it in narration only by calling it "a tiny, unrealistic example".
- **Length:** ~16:00 is over the regular 8–15 range (beat times add to ~14:50 before pauses). B12 (Figure 15.6) and B10 are the heaviest. Candidate cuts: the "move an address space" step in B10, or the table example in B08.
- **Dependence on 13 and 14:** I assume 13 introduced address spaces and virtual addresses and 14 covered `malloc`/`free`. Recheck the callbacks when those scripts land.
- **"Wreak havoc" joke (B09)** is a slight paraphrase of the book's footnote; keep or drop?
