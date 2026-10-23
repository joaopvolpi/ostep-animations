# 15 — Mechanism: Address Translation · Scene breakdown
> Script: Ostep/Scripts/15-vm-mechanism.md · Scenes: 22 · Est. duration: ~16:20

## Visual overview
- **Core metaphor: an adder and a comparator sit in the memory path.** Episode 06 put the CPU chip on the user/kernel line. Here the chip gets a small box underneath it, the **MMU**: a **bounds** register over a comparator, a **base** register over an adder. Every address the program generates is an **address chip** (a small pill with a number) that leaves the CPU, passes the comparator (check), passes the adder (+ base), and lands in physical memory as a different number. The viewer *sees* the translation happen on every access; the OS never appears in that path (it is the "direct execution" part).
- **Second metaphor: "what A sees / what really happens"**, the series' Illusion split. Left: A's address space, always drawn 0 at the top, never moving. Right: physical memory, where A's slot sits at 32 KB. The two are joined only by the MMU in the middle. The viewer sees the left column stay put while the right one shows the truth.
- **Third: LDE for memory.** The same actors as 06 return, in the same roles: OS token (red) for the kernel, the trap table (with two new rows), the timer, the PCB cards (now holding base and bounds), the privilege gauge. Scenes S12–S18 deliberately look like 06 S06–S13 with memory attached, and Figures 15.5 and 15.6 reuse `ProtocolChart` exactly as 06 used it for Figures 6.1/6.2.
- **Structure:** cold open and crux (S01–S02); the philosophy (S03); the tiny world and program (S04–S05); the relocation problem and its software failure (S06–S07); base register, trace (S08–S09); bounds, MMU, example table (S10–S11); hardware support (S12–S13); OS responsibilities (S14–S15); boot and runtime figures (S16–S18); big picture, price, recap, teaser (S19–S22).
- **Props used (from the bible and lib):** Crux card, Aside/Tip card, Term unveil / Term note, Section badge, CPU, Memory, Illusion split, User/Kernel boundary + Privilege gauge, PCB card, Register bank, Save slot, KernelToken, `cpu_ride`, `KernelStack`, `TrapTable`, `ProtocolChart`, `AlarmClock`, `Padlock` / `PadlockStrip`, Code block / `CodeWalker`, `RoboticArm`, Queue (not used), Characters.

### Persistent assignments
| Thing | Look | Notes |
|---|---|---|
| Process **A** | `Process(label="A", color=PROCESS_COLORS[0])` (coral) | Same as 04–11. Address space 16 KB, **base = 32 KB (32768), bounds = 16 KB (16384)**. The main actor. |
| Process **B** | `PROCESS_COLORS[1]` (mint) | 16 KB, **base = 16 KB**. The one that does the bad load (Figure 15.6). |
| Process **C** | `PROCESS_COLORS[2]` (gold) | Only in S11: the book's tiny 4 KB example, loaded at 16 KB. Shown with a "(tiny example)" tag. |
| Address chip | Pill 0.9 × 0.32, font 20 `MONO_FONT`. **Virtual** = outline in the owner's process color, filled at 0.2; **physical** = `MEM_COLOR` fill. Class `AddressChip` (New assets). | Always labeled with the number; numbers are written the way the narration says them (`128`, `15 KB`, `32,896`, `47 KB`). |
| Translation stage | **Address-space column** (virtual, "what A sees") at (−4.9, 0.3), 1.3 wide × 4.0 tall, `address_space_16kb(owner_color=PROCESS_COLORS[0])` from `ostep_lib/props/p13_addrspace.py` (episode 13's canonical column: code / heap / free (weight 6) / stack, addresses 0KB, 1KB, 2KB, 15KB, 16KB, with the not-to-scale break mark); **physical column** at (4.9, 0.3), 1.3 × 4.0, `Memory(regions=[("OS",1),("free",1),("A",1),("free",1)])`, addresses 0, 16KB, 32KB, 48KB, 64KB. **CPU** at (0, 1.3) scale 0.9. **MMU box** under it at (0, −0.55), 4.4 × 1.8. | Left column label "what A sees" and right label "what really happens" (font 22, `DIM`) at y = 2.25, in the content zone. The Illusion split uses its default titles (y = 2.25). |
| MMU internals | `RegisterBank(["bounds","base"], cols=2)` along the box top (y = 0.05): `bounds` cell at x = −1.5, `base` cell at x = +1.5. Below them, a **comparator** circle "<" at (−1.5, −0.85) and an **adder** circle "+" at (1.5, −0.85), joined by a thin wire. Class `MMU` (New assets). | Registers read `32 KB` / `16 KB` for A. Wire path of an address chip: CPU slot → comparator → adder → out at (2.5, −0.85) → physical cell. |
| Section badge | Top-left (−6.6, 3.6): `VIRT` dot + "15 · Address Translation", font 22, `DIM` | Appears in S02, stays until S21. |
| Term unveil / note | **Key terms** (4): *address translation* (S03), *dynamic relocation* (S09), *memory management unit (MMU)* (S11), *internal fragmentation* (S20): `terms.show` (veil, center, docks top-right at (6.6, 3.6)), never in neighbouring rows. Every other term is a **Term note** (`terms.note`, slides into the top-right dock, no veil): *interposition, virtual address, transparency, static relocation, base register, physical address, bounds register, exception, privileged instructions, free list*. | Written below as "Term unveil: *X*" / "Term note: *X*". |
| Characters (corner mode) | Student (−5.8, −2.8), scale 0.75, facing right; Professor (5.8, −2.8), scale 0.75, `flip()` | **Dialogue mode** (S01, S22): Student (−2.6, −1.7), Professor (2.6, −1.7), scale 0.85. Computer not used in this episode. |
| Chart zone (S16–S18) | `ProtocolChart` content from y = 2.2 down; thumbnail stage bottom-right (5.2, −2.3), scale 0.35 | Same as 06 S08. |
| OS token / CPU seats | `KernelToken` on the CPU as in 06; **user seat** = the CPU slot (0, 1.3 + 0.63); in the full-LDE scenes (S12, S16–S18) the **User/Kernel boundary** is drawn at y = −0.3 only in the thumbnail | In the translation stage the boundary line is not drawn; the gauge (6.4, 1.6) shows the mode. |

## Scenes

### S01 — Two programs, one address   (beats: B01) · ~0:40
**Purpose:** pose the puzzle: two programs use the same address, and there is one RAM.
**Starts with:** empty (BG).
**Layout:** dialogue mode. Two small address-space columns at A (−5.8, 0.6) and B (−4.4, 0.6), each 1.0 wide × 3.0 tall with a cell labeled `15 KB` at the bottom (stack region). Physical column at (4.6, 0.6), 1.2 × 3.0, no labels. Curved arrows arc up over the center (peak y = 1.6) so they clear the characters.

| # | Narration (exact words the action lands on) | On screen / animation |
|---|---|---|
| 1 | "Last time you told me every address my program prints is a virtual one, and that every program thinks its memory starts at zero." | Student (curious) and Professor (neutral) slide in to dialogue mode. A's and B's address-space columns `FadeIn`; both labeled `0` at the top. |
| 2 | "Right. Program A keeps a variable at fifteen kilobytes. Program B keeps its own variable at fifteen kilobytes too." | Professor (explaining). Cell `15 KB` lights in each column; tiny chips `3000` in A's, `7` in B's. |
| 3 | "The same address. And neither one overwrites the other?" | Student (confused). A coral and a mint arrow arc from the two `15 KB` cells and aim at the **same** cell of the physical column (the physical column fades in as they go). |
| 4 | "Neither. And there is only *one* RAM." | Professor (happy). The two arrows collide at the cell: red flash (`flash_at`), `3000` and `7` overwrite each other in the cell (the chip flickers). |
| 5 | "So somebody is lying." | Student (surprised). A "?" pops between the columns and the physical cell. |
| 6 | "Somebody is. The illusion is beautiful, and today we build it." | The arrows and the "?" fade; the two small columns slide left and dim to 40%. |
| 7 | "And not slowly: it has to happen on *every* instruction fetch, every load, every store." | Three tiny labels `fetch`, `load`, `store` pop above the physical column (`GrowFromCenter`, 0.3 s apart), each with a tick-tock of a small stopwatch (`stopwatch` icon, scale 0.4) beside the last one. Hold 0.8 s. |

**Characters:** Student (curious → confused → surprised), Professor (neutral → explaining → happy).
**Ends with:** dimmed A/B columns at left, the physical column at right, `fetch`/`load`/`store` labels fading out; characters in dialogue mode.
**Implementation notes:** build A's and B's columns with `address_space_16kb(owner_color=…, scale=0.7)`; use the same two cells for the colored arrows via `CurvedArrow`. The collision is a visual joke, keep it under 1.5 s.

### S02 — The Crux   (beats: B02) · ~0:35
**Purpose:** pose the crux and name the three goals; tie them to LDE.
**Starts with:** S01 end state.
**Layout:** Crux card centered (0, 0.4), 9 × 3.4. Characters glide to corner mode. Three goal icons in a row at y = −1.2.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | (transition) | The stage fades. Characters glide to corner mode. Crux card `Write`s in the `VIRT` accent: **"How to efficiently and flexibly virtualize memory?"**; subtitle (font 22, `DIM`): "How do we keep control over which memory locations an application can access? How do we do all of this efficiently?" Section badge forms top-left. |
| 2 | (dock) | The card docks to the strip at (0, 3.0). |
| 3 | "Three words in that question. **Efficiency:** programs run at full speed, which needs hardware help." | Three icon slots appear one by one: stopwatch with the label "efficiency"; the first lights up. |
| 4 | "**Control:** no program touches memory that isn't its own, and no program touches the OS." | Padlock (series `Padlock`, closed) with "control"; it lights up. |
| 5 | "And **flexibility:** programs use their address space however they like." | An open hand (`hand`) with "flexibility"; it lights up. |
| 6 | "That should sound familiar. Efficiency and control: that was the whole story of limited direct execution." | The efficiency and control icons glow together; `ep_tag("← Ep. 06")` flies in from the left and lands between them, with a small fence glyph (`fence_glyph`). Student (neutral → curious). Hold 1 s. |

**Characters:** Student (neutral → curious), Professor (explaining).
**Ends with:** section badge, crux strip; the three icons then fade out (except nothing remains).
**Implementation notes:** the crux text is the book's. Keep subtitle ≤ 25 words, in the card only until the dock.

### S03 — LDE, again, for memory   (beats: B03) · ~1:00
**Purpose:** the philosophy: run directly, with hardware stepping in on each memory reference (address translation), OS sets it up; interposition.
**Starts with:** S02 end state.
**Layout:** CPU at center-left (−1.6, 0.6) scale 0.9; a small physical `Memory` column at (4.6, 0.3), 1.2 × 3.4, plain. A thin ring (the "translator") around the arrow path at (1.5, 0.6). A faded legend "LDE" at left (−5.6, 1.4): a tiny CPU chip with a fence glyph and `ep_tag("Ep. 06")`.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "So what's the trick? Same as for the CPU?" | Student (curious). Legend (chip + fence) fades in at left. |
| 2 | "Same philosophy. Remember limited direct execution: let the program run directly on the hardware, and step in only at key moments." | Professor (explaining). The legend pulses; a Process A hops on the CPU (`hop_to`). |
| 3 | "For memory, the program just runs. Its instructions fetch, load and store *directly*, no OS in the way." | Memory arrows `fetch`, `load`, `store` leave the CPU for the column, straight (no ring yet), reaching it fast. A "FAST" tag (green, as in 06) appears. |
| 4 | "But on each of those memory references the **hardware** quietly steps in." | The ring (translator) drops over the path; each arrow now passes through it. |
| 5 | "It takes the address the program used, and changes it into the address where the data really is." | An address chip `A: 15 KB` (virtual style) enters the ring and leaves as a different physical-style chip (`Transform` of the label to "?"; the real numbers come in S08). Term unveil: *address translation*. |
| 6 | "The hardware alone can't virtualize memory. It only provides the fast, low-level mechanism." | A gear (`GearPair`) appears on the ring ("hardware: mechanism", DIM). |
| 7 | "The OS has to get involved at a few key moments: to set the hardware up, to keep track of which memory is free and which is used, and to step in when something goes wrong." | KernelToken appears below the CPU (−1.6, −1.6); three short tags drop in beside it, one per phrase: "set up", "track free / used", "step in". Each tag lights when read. |
| 8 | "There's a name for what the hardware does here: **interposition**." | Term note: *interposition*. Tip card (series `TipCard`) slides in from the right: title "TIP", body "Interposition is powerful." Hold 1.5 s. |
| 9 | "It sits in the middle of an interface, and adds a power the client never asked for. Notice that the program doesn't change at all. That's called transparency, and we'll get to it." | Professor (proud). The ring glows between the CPU and the column; Process A on the CPU stays unchanged (a `Indicate`). Tip card slides out. |
| 10 | "Same recipe as episode six: hardware does the fast part, the OS does the setup and the policing." | The legend (chip + fence) moves next to the gear ring and the KernelToken; a dotted line joins them. Hold 1 s. |

**Characters:** Student (curious), Professor (explaining → proud).
**Ends with:** CPU with A, the ring on the path to the column, KernelToken below, gear icon and legend; term strip "interposition". Transition: all fades.
**Implementation notes:** "transparency" is only said here; its highlight is in S06. The ring is a plain `Annulus`; do not build the MMU yet.

### S04 — The tiny world   (beats: B04, first half) · ~0:30
**Purpose:** state the three simplifying assumptions and mark them as temporary.
**Starts with:** S03 end state, cleared.
**Layout:** a `PadlockStrip(3)` at center; three short labels to the right of each padlock.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "To make this concrete we need a tiny program and a tiny world. First, the world. We'll make three simplifying assumptions, and the book is honest about it: they're almost laughable." | Three closed padlocks pop in a column (`GrowFromCenter`, 0.3 s apart) at x = −2.2. Student (curious), Professor (happy). |
| 2 | "The address space is placed in physical memory **contiguously**." | Label 1 writes: "contiguous", with a tiny solid block icon. |
| 3 | "It is smaller than physical memory." | Label 2 writes: "smaller than physical memory"; a small block inside a bigger one. |
| 4 | "And every address space is exactly the same size." | Label 3 writes: "all the same size"; three equal blocks. |
| 5 | "Go ahead, laugh. It'll be the OS laughing at you later, when you try to understand TLBs. That's just how the OS rolls." | Professor (worried → happy). A tiny red OS token pokes its head from the right and shrugs. Padlock 1 wobbles (`wobble`). |
| 6 | "We'll relax them one by one in the next episodes." | A "later" tag; all three padlocks open one after the other (`PadlockStrip.open(i)`) then dim to 30% and the labels fade. |

**Characters:** Student (curious), Professor (happy).
**Ends with:** the three dim open padlocks at left (−5.8, 1.2) as a tiny "assumptions" legend, scale 0.5. No text.
**Implementation notes:** reuse the 07 assumption-padlock look; the OS token cameo is optional (drop if cluttered).

### S05 — A tiny program: `x = x + 3`   (beats: B04, second half) · ~0:55
**Purpose:** Figure 15.1 and the five memory references; first use of "virtual address".
**Starts with:** S04 end state.
**Layout:** left: the **address-space column** (−4.9, 0.3) (code, heap, free, stack); center-right: `Code` block (C then assembly), font 22, at (1.4, 1.2); a **reference list** (small, 5 rows) at (3.8, −1.4) revealed later.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Now the program. One line of C: `x = x + 3`, where `x` is `3000`." | The address-space column draws in. `Code` snippet `x = x + 3;` writes at (1.4, 1.6), a small tag `x = 3000` beside it. |
| 2 | "The compiler turns it into three instructions: load `x` from memory into a register, add three, store it back." | The C line `Transform`s into the three assembly lines `128: movl 0x0(%ebx), %eax`, `132: addl $0x03, %eax`, `135: movl %eax, 0x0(%ebx)` (`MONO_FONT`, font 20); each row has its own 0.5 s `Write`. |
| 3 | "The instructions live at addresses 128, 132 and 135, in the code region near the top." | The three assembly lines shrink and fly into the top of the code region of the column; addresses `128`, `132`, `135` stay as tiny labels beside the cells. Highlight the code region (`Indicate`). |
| 4 | "The variable lives at fifteen kilobytes, on the stack, near the bottom of a sixteen-kilobyte address space." | A cell `3000` writes into the stack region at 15KB (address label `15KB` highlighted). The address `16KB` at the column's bottom pulses. |
| 5 | "Run it, and the process makes five memory references." | A cursor (a small arrow) appears at the code region. The list header "5 memory references" writes. |
| 6 | "Fetch the instruction at 128." | Row 1 `fetch 128` writes; the cursor flashes at 128, the cell lights (`MEM_COLOR` pulse). |
| 7 | "Load from fifteen kilobytes." | Row 2 `load 15 KB`; cursor jumps to the stack cell; it lights. |
| 8 | "Fetch at 132. Fetch at 135. Store to fifteen kilobytes." | Rows 3, 4, 5 write quickly (0.4 s each); the cursor walks 132 → 135 → 15 KB; the stack cell flickers `3000` → `3003`. |
| 9 | "Every one of these is a **virtual address**, the address the program *thinks* it is using." | Term note: *virtual address*. Each of the five rows gets a thin outline in A's coral, as "virtual-style" chips. |

**Characters:** Professor (explaining), Student (neutral).
**Ends with:** the address-space column with code + `3000` in the stack; the five-row reference list; term strip "virtual address".
**Implementation notes:** adapt **Figure 15.1** (the instruction lines at 128/132/135). The `3000` → `3003` happens only visually (the book shows only the initial value), keep it quiet. At most one assembly code block on screen; the C line is removed when the assembly appears.

### S06 — Not at address zero   (beats: B05, first half) · ~0:35
**Purpose:** Figure 15.2: the OS puts the process elsewhere; the program must not notice. Term: transparency.
**Starts with:** S05 end state (column at left, reference list).
**Layout:** physical column at (4.9, 0.3) (OS, free, free slot, free); the A address-space column slides toward it. Label "what A sees" (−4.9, 2.35) and "what really happens" (4.9, 2.35).

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Here's the problem. From the program's point of view, its address space starts at zero and goes up to sixteen kilobytes." | The reference list fades. A's column gets a bracket `0 … 16 KB` (DIM). |
| 2 | "But the OS wants to put the process somewhere else, and not necessarily at zero." | The physical column fades in at right with the OS grey (0–16KB, label "OS"); the rest hatched ("not in use"). |
| 3 | "In this physical memory of sixty-four kilobytes, the OS keeps the first sixteen for itself, and puts our process at thirty-two kilobytes." | The physical column's address labels `0, 16KB, 32KB, 48KB, 64KB` write in. A copy of A's column (colored coral, translucent) travels (arc) across the screen and lands in the 32–48KB slot; A's column at left stays. Label "A" in the slot. |
| 4 | "So when the program asks for address 128…" | Student (confused). A chip `128` (virtual, coral) appears next to A's left column. |
| 5 | "…it has to actually reach 32,896." | A dotted arrow from the chip aims into the slot, the new number `32,896` fades in at the end of the arrow (MEM_COLOR, shown dim; the translation happens in S08). |
| 6 | "We need to **relocate** the process, and do it **transparently**: the program must never notice." | Professor (explaining). Term note: *transparency*. A coral "eye" (`EyeIcon` if available, else `magnifier_icon`) on the program's side shows no change. |

**Characters:** Student (confused), Professor (explaining).
**Ends with:** left: A's address-space column ("what A sees"); right: the physical column with A's coral slot at 32 KB; the dotted arrow `128 → 32,896`; term strip "transparency".
**Implementation notes:** adapt **Figure 15.2**. The relocation is an animation of a translucent *copy* so the left column stays exactly where it is (that is the whole idea of the illusion). Keep the hatched fill from `hatch_rect` for "not in use".

### S07 — Static relocation: the software idea   (beats: B05, second half) · ~0:35
**Purpose:** the naive fix (rewrite addresses with a loader), and why it fails (protection, moving).
**Starts with:** S06 end state.
**Layout:** the stage dims to 35%. At center, a `Code` block (two lines) at (0, 1.2); the loader robot (`RoboticArm` from 04) at (−3.2, 1.2). Aside card at the right (4.6, 0.2), 4.2 × 3.4.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Easy. Before running, rewrite every address in the program. Add thirty-two thousand to each." | Student (curious). A code line `movl 0x0(%ebx), %eax` appears at the center. |
| 2 | "Funny, that's exactly what early systems did." | Professor (thinking). The Aside card slides in: header "ASIDE", title "Software-based relocation". |
| 3 | "It's called **static relocation**. A piece of software, the **loader**, rewrites the addresses in the executable before it runs." | Term note: *static relocation*. The robot arm (labeled "loader", font 20) crosses out `0x0` and writes `0x8000` in the code line; the rewritten line `movl 0x8000(%ebx), %eax` is highlighted. |
| 4 | "Problem solved!" | Student (excited). A tick mark (`tick_mark()`) pops over the code line. |
| 5 | "Not quite. First, no protection." | Professor (worried). A second code line `movl 4000, %eax` (a deliberately bad address) appears; the loader rewrites it to point at a cell inside the grey OS block in the dimmed stage (a red arrow to the OS region). A red "!" over the arrow; no gate stops it. |
| 6 | "Nothing stops the program from computing a bad address, and touching another process or the OS." | The arrow lands in the OS block; the OS block flashes red. Padlock icon (open, red) on the code line. |
| 7 | "Second, once placed, the address space is hard to move." | A small moving-box icon tries to slide A's slot and gets stuck: the code lines in the slot are tangled by arrows pointing at old addresses. |
| 8 | "We want hardware to do this at run time." | Professor (explaining). The loader and Aside card fade out; the stage returns to full brightness. A faint gear icon ("hardware") pulses. Hold 1 s. |

**Characters:** Student (curious → excited), Professor (thinking → worried → explaining).
**Ends with:** S06 end state, restored; term strip "static relocation".
**Implementation notes:** Aside text per the book: "software-based relocation"; body on the card ≤ 25 words ("the loader rewrites each address; no protection; hard to move later"). The second line's `4000` echoes the book's aside (`movl 1000` rewritten to `movl 4000`); it is only an illustrative bad address here.

### S08 — The base register   (beats: B06) · ~0:50
**Purpose:** introduce the base register and the translation rule, and show it set by the OS.
**Starts with:** S07 end state.
**Layout:** the full translation stage: left address-space column; physical column at right; CPU (0, 1.3) with the MMU box beneath, base register only (the comparator and bounds register appear in S10). Formula at the bottom center (0, −2.5), above the characters.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "The idea comes from the first time-sharing machines of the late nineteen-fifties." | An `EraRibbon`-style tag (`ep_tag("1950s")`) flickers at the lower left; the MMU box draws in (empty, label "MMU" omitted for now), under the CPU. |
| 2 | "The hardware gets two registers per CPU. The first is the **base** register." | The two cells of the register bank appear, labeled `bounds` (dim, empty) and `base`. Term note: *base register*. |
| 3 | "When the program is written and compiled, it assumes it lives at address zero." | A's column pulses at its `0` (top); a coral chip `0` rests there. |
| 4 | "When it starts running, the OS decides where it really goes in physical memory, and sets the base register to that." | KernelToken hops onto the CPU; its arm reaches the `base` cell and writes `32 KB`. The gauge reads KERNEL. A's slot in the physical column lights (32–48KB). A thin dotted line links the base cell to the slot's top edge. |
| 5 | "Here: thirty-two kilobytes." | The base value `32 KB` pulses; the token retracts and leaves the chip; gauge flips to USER; A hops onto the CPU. |
| 6 | "From then on, every memory reference the process generates gets translated by the hardware. The rule is one line." | The adder circle `+` pops into the MMU under the base cell. Term note: *physical address*. |
| 7 | "**Physical address equals virtual address plus base.**" | The formula writes under the stage in `MONO_FONT`, font 28: `physical = virtual + base`, with `virtual` in A's coral, `base` in `KERNEL_COLOR` (set by the OS), `physical` in `MEM_COLOR`. |
| 8 | "That's all. An addition." | Professor (happy). The adder circle pulses once; Hold 1 s. |

**Characters:** Professor (happy at the end), Student neutral.
**Ends with:** stage with the MMU (base only, `32 KB`), the `+` adder, gauge USER, A on the CPU, the formula under the stage, term strip "physical address".
**Implementation notes:** the KernelToken sits on the chip only for this scene (kernel mode, setting the register). Use `hop_onto(cpu)` and `retract()`. The formula uses `Text` with `MONO_FONT` (not `MathTex`; it is code-like).

### S09 — Translating one instruction at a time   (beats: B07) · ~1:00
**Purpose:** trace the book's two translations and name dynamic relocation.
**Starts with:** S08 end state.
**Layout:** the translation stage; right side shows both columns. The formula remains.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Let's trace it. The program counter is 128." | A `PC` tag (`pc_marker`-style) on the left column at the cell 128 (coral). A's left column cell `128` lights. |
| 2 | "The hardware needs the instruction, so it first adds the base: 128 plus 32,768 is 32,896." | An address chip `128` (virtual) leaves the CPU, enters the adder; the base `32,768` fades in beside it; the chip emerges as `32,896` (physical, `MEM_COLOR`). |
| 3 | "The memory fetches from there." | The physical chip travels along the wire to the physical column and the cell at 32,896 (just under the 32KB line, in A's code part) lights; an instruction bubble `movl…` flies back to the CPU. The left column's `128` stays lit as the program's view. |
| 4 | "The instruction executes: load from virtual address fifteen kilobytes." | CPU: A shows `running` expression; a chip `15 KB` leaves the CPU. |
| 5 | "Again the hardware adds the base. Fifteen kilobytes plus thirty-two kilobytes is forty-seven kilobytes." | The chip enters the adder, `+ 32 KB`, leaves as `47 KB`. |
| 6 | "That's where the 3000 really sits." | It travels to the physical column; the cell at 47 KB (inside A's slot, near the bottom) lights and `3000` flies back along the same path to the CPU register (`eax` tag). The left column's `15KB` cell lights simultaneously. |
| 7 | "And the program has no idea any of this happened." | Student (curious). The left column shows only its own cells lit (128, then 15KB), and a coral "eye" pulses on A's face: nothing changed. |
| 8 | "None. It wrote 128 and 15K, and it saw its own data. That's the illusion." | Professor (proud). Split divider (dashed) flashes between left and right; "what A sees" / "what really happens" labels pulse in turn. |
| 9 | "Because we translate at run time, the technique is called **dynamic relocation**." | Term unveil: *dynamic relocation*. |
| 10 | "And because we can change the base later, even after the process has started, we can move address spaces around." | A's slot in the physical column twitches (a small wiggle) with an arrow toward 48 KB, and the base cell flickers `32 KB` ⇄ `48 KB` (quick). Hold 1.5 s. |

**Characters:** Student (curious), Professor (proud).
**Ends with:** the stage, base `32 KB`, A's slot lit, term strip "dynamic relocation".
**Implementation notes:** uses the new `MMU.translate(chip, va, ...)` helper (spec below); the left column deliberately never moves. The `128 → 32,896` and `15K → 47K` numbers are from the book. 15 KB + 32 KB = 47 KB; draw physical 47 KB at the right place in the 32–48 KB slot (it is 1 KB above the slot's bottom edge, the stack).

### S10 — The bounds register   (beats: B08, first half) · ~0:45
**Purpose:** the second register, the check, and what happens when it fails (exception).
**Starts with:** S09 end state.
**Layout:** the translation stage, now with the full MMU (bounds cell, comparator).

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "The book said base *and* bounds. Where are the bounds?" | Student (curious). The `bounds` cell lights up in the (previously dim) register bank. |
| 2 | "The second register is the **bounds** register, sometimes called the limit." | Term note: *bounds register*. The cell fills with `16 KB`; the comparator circle `<` pops in below it. |
| 3 | "It's there for protection. Before translating, the hardware checks: is this virtual address inside the address space?" | Address chip `15 KB` enters the comparator first: green tick; then the adder (as in S09). The left column's range `0…16 KB` brackets. |
| 4 | "If the virtual address is greater than or equal to the bounds, or negative, the CPU raises an **exception**…" | Term note: *exception*. A chip `17 KB` leaves the CPU, hits the comparator: red flash. A red bolt shoots out from the CPU box. Student (surprised). |
| 5 | "…and the process is probably terminated." | A "!" pops over A; a red `x_mark` stamps it; A turns `done` and fades out. A fresh A re-spawns on the CPU (ready → running) for the next scene. |
| 6 | "In our example the bounds is sixteen kilobytes." | The bounds cell pulses `16 KB`. A little arrow compares it to the address-space column height. |

**Characters:** Student (curious → surprised), Professor (explaining).
**Ends with:** the stage with the full MMU (`16 KB`, `32 KB`), a fresh A on the CPU, term strip "exception".
**Implementation notes:** `MMU.translate(..., ok=False)` makes the chip bounce off the comparator and fires the bolt. The chip `17 KB` is an arbitrary out-of-bounds example; the next scene uses the book's example.

### S11 — The memory management unit   (beats: B08, second half) · ~0:50
**Purpose:** the book's example table (4 KB at 16 KB) and the MMU name; the bounds-as-end-address footnote.
**Starts with:** S10 end state.
**Layout:** a mini translation stage: process C's tiny address-space column (−5.6, 0.0) (1.0 × 1.0 for "4 KB"), a mini physical column at right, the MMU box at center with `base 16 KB`, `bounds 4 KB`. A 2-column `ProtocolChart` ("Virtual", "Physical") on the right-lower side (3.4, −0.6), 4 rows. Tag "(tiny example)".

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Let's try different numbers, the book's example: a tiny process with a four-kilobyte address space, loaded at sixteen kilobytes." | The big stage shrinks to the MMU only; the registers read `bounds 4 KB`, `base 16 KB`. Gold Process C on the CPU. The tiny columns appear. Tag "tiny example". |
| 2 | "Virtual address zero becomes sixteen kilobytes." | Chip `0` → comparator ✓ → adder → `16 KB`. Table row 1 writes `0 → 16 KB`. |
| 3 | "One kilobyte becomes seventeen." | Chip `1 KB` → `17 KB`. Row 2: `1 KB → 17 KB`. |
| 4 | "Three thousand becomes 19,384." | Chip `3000` → `19,384`. Row 3: `3000 → 19384`. |
| 5 | "And 4,400? That's past the end of the address space. Fault." | Chip `4400` hits the comparator: bounce; red bolt. Row 4: `4400 → Fault (out of bounds)` in red. Hold 1 s. |
| 6 | "Simplification: bounds can also hold the *end* address instead of the size; the check is then done after adding. Equivalent. We'll assume the size." | Aside card (small) slides in: "Bounds can be a size or an end address. Same result." (≤ 12 words). The comparator and adder swap places in a quick replay, then swap back. |
| 7 | "So where does all this circuitry live?" | Student (curious). The table fades to the side. |
| 8 | "In the CPU. One pair of registers per CPU." | Professor (explaining). A thin frame closes around the CPU chip + MMU box. |
| 9 | "The part of the processor that helps with translation is called the **memory management unit**, the **MMU**." | Term unveil: *memory management unit (MMU)*. The MMU box gets its label "MMU". |
| 10 | "For now it's two registers, an adder and a comparator. It will grow as we get more sophisticated." | The four parts blink in turn. A faint "+ TLB? + page tables?" ghost label next to the box. Hold 1 s. |

**Characters:** Student (curious), Professor (explaining).
**Ends with:** the CPU + MMU box (labeled), with registers back to A's values (`32 KB`, `16 KB`) and A on the CPU; the table and tiny columns removed; term strip "MMU".
**Implementation notes:** the table uses `ProtocolChart(columns=["Virtual","Physical"], ...)` rows; the book's "Fault (out of bounds)" row is italic red. Hand back to A's numbers by animating the registers with `set_value`.

### S12 — The hardware's checklist, part 1   (beats: B09, first half) · ~0:45
**Purpose:** modes, registers, translate+check as the first three items (Figure 15.3).
**Starts with:** S11 end state.
**Layout:** the CPU + MMU at the center-right (1.6, 0.6). A vertical **checklist** at left (−3.4 → −0.4 in x, y from 1.8 down; row 0.55): empty row slots, each with an icon on the left and a short label (font 22). The privilege gauge at (6.4, 1.6).

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Let's collect what we need from the hardware. It's the same list as limited direct execution, extended." | The checklist frame draws. A faint ghost of 06's boundary + gauge flashes at the left (callback). |
| 2 | "One: two CPU modes, user and kernel, exactly as in episode six." | Row 1 writes: gauge icon + "user / kernel modes". The gauge flips USER → KERNEL → USER (`set_level`). |
| 3 | "Two: the base and bounds registers, as part of the MMU." | Row 2: register-pair icon + "base / bounds registers". The two cells of the MMU pulse. |
| 4 | "Three: circuitry to translate and check bounds, which is quite simple." | Row 3: adder+comparator icon + "translate + check". A chip runs through the MMU (✓). Student (surprised: "that's it?" bubble optional). |

**Characters:** Student (neutral → surprised), Professor (explaining).
**Ends with:** checklist with three rows (rows 4–6 slots still empty), the MMU on the right.
**Implementation notes:** the checklist is a vertical list of icon + short label, not the book's two-column table (that is S13's closing). Keep each label ≤ 4 words.

### S13 — The hardware's checklist, part 2   (beats: B09, second half) · ~0:45
**Purpose:** privileged instructions to change base/bounds and register handlers; exceptions; the "wreak havoc" joke.
**Starts with:** S12 end state.
**Layout:** same. Add a **TrapTable** at (−3.4, −1.3) (kernel color, 3 rows, small) near the bottom left. A user-mode A stands on the CPU.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Four: **privileged instructions** to update base and bounds. Only in kernel mode." | Term note: *privileged instructions*. Row 4: padlock (closed) + "privileged: set base / bounds". |
| 2 | "Why must changing the base be privileged?" | Student (excited, curious). |
| 3 | "Imagine a user process that could set the base register while running. Set it to zero, and the whole machine is yours." | Professor (worried). A hand/arm from A reaches the `base` cell and rewrites `32 KB` → `0`; the physical column's OS region flashes red as the base line points into it. Rewind (undo) at the next row. |
| 4 | "Wreak havoc. Now quickly flush that thought from your mind." | The rewrite fades (a `puff` icon from 04); Professor `blink`s. |
| 5 | "So if user code tries to change base or bounds, it's the same story as in episode six: the CPU raises an exception…" | The hand tries again; it bounces off the padlock on the register; a red bolt. Row 6: bolt icon + "raise exceptions". |
| 6 | "…and the OS's handler for 'tried to execute a privileged operation' runs." | The bolt flies down into the trap table; the row `illegal instruction → handler` lights. The KernelToken pops onto the chip; the gauge → KERNEL. |
| 7 | "Same for an out-of-bounds access." | A chip `17 KB` bounces off the comparator; the bolt hits the row `out-of-bounds → handler`; same token. |
| 8 | "And the hardware needs a way to be *told* where those handlers are." | Row 5: trap-table icon + "register handlers (privileged)". The token's arm writes the two rows into the trap table (illegal instruction, out-of-bounds) with a small `0x…` tag; padlock on the instruction. |
| 9 | "Remember the trap table? A few more privileged instructions fill it." | The trap-table card glows and a thin `ep_tag("← Ep. 06")` appears on it. Then the six rows of the checklist fly together and dock as a compact two-column legend "Hardware requirements" in the lower left (the book's Figure 15.3, names only). |

**Characters:** Student (curious), Professor (worried → explaining).
**Ends with:** the six-item checklist (compact, lower-left), the trap table with two new rows, the CPU back in user mode (gauge USER, token gone), A on the CPU.
**Implementation notes:** adapt **Figure 15.3** as six icon + short-name rows (≈ 18 words total on screen; the book's "notes" column is spoken, not shown). Order the checklist as the book does: modes, base/bounds registers, translate+check, privileged update instructions, privileged handler-registration instructions, raise exceptions. Make sure the rewrite-to-zero shot is clearly undone.

### S14 — OS jobs 1 and 2: create and terminate   (beats: B10, first part) · ~0:45
**Purpose:** Figure 15.4: memory management, with the free list; allocation at creation, reclaim at termination.
**Starts with:** S13 end state.
**Layout:** physical column at (4.9, 0.3) (OS, free, A, free); a **free-list card** at (0, 0.8), 2.6 × 1.8, `PCBCard`-style with header "FREE LIST" (`DIM` frame) and fields `16 – 32 KB`, `48 – 64 KB`; a PCB card for A at (−3.4, 0.8). Checklist and the hardware legend fade out. The new process B (mint) at the bottom left of the center (−1.6, −1.5), `ready`. Characters corner mode.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Hardware gives us new features, and the OS gets new jobs. There are exactly four moments where it must act." | The hardware legend fades; four tiny numerals ①–④ pop at the top-left of the content zone (−6.2, 2.2…) and stay as a progress mark; ① is lit. |
| 2 | "First, **when a process is created.** The OS has to find room for its address space." | B arrives from the left and stops at the center-left. The physical column fades in; A's slot is already there (32–48 KB). |
| 3 | "By our assumptions each address space is the same size and smaller than physical memory, so the OS sees physical memory as an array of slots, and tracks which are free in a data structure: the **free list**." | Term note: *free list*. The physical column gets slot dividers; the free-list card slides in. |
| 4 | "Here, the free list has two entries, 16 to 32 kilobytes and 48 to 64 kilobytes." | The two fields write; the corresponding slots (16–32, 48–64) light, one per entry. |
| 5 | (action) | The token searches: a magnifier hovers over the entries; entry `16 – 32 KB` is taken: it crosses off the free list and the slot (16–32) fills mint with label "B". B's PCB card appears with fields `base: 16 KB`, `bounds: 16 KB`. |
| 6 | "Second, **when a process terminates**, gracefully or because it was killed." | ② lights. B shows `done` (check) then fades; a red `x_mark` flashes on an alternate branch ("killed") for a beat. |
| 7 | "The OS takes its memory back and puts it on the free list, and cleans up related data structures." | B's slot hatches back to "free"; the entry `16 – 32 KB` reappears in the free list; B's PCB card fades out. Hold 1 s. |

**Characters:** Professor (explaining), Student (neutral).
**Ends with:** physical column (OS, free, A, free), free list with two entries, A's PCB card at left, ① ② lit.
**Implementation notes:** reuse `PCBCard` for the free-list card (fields = ranges, `set_field` to strike). Show the free list as the book's two entries only; no allocator policy. The "fixed slots" are a visual simplification of assumption 3, kept on screen as faint dividers.

### S15 — OS jobs 3 and 4: switching and moving   (beats: B10, second part) · ~0:55
**Purpose:** save/restore base and bounds at context switch; relocating an address space while it's descheduled.
**Starts with:** S14 end state, A running on the CPU; B (mint) on a bench (ready); both have PCB cards at (−3.6, 0.8) and (−3.6, −1.0) (1.7 × 1.2) with fields `base`, `bounds`.
**Layout:** CPU + MMU at center-right (1.0, 0.8); the physical column at (5.2, 0.3) with A at 32 KB and B at 16 KB (mint).

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Third, **at a context switch.**" | ③ lights. The timer (`AlarmClock`, small) at (−0.8, 2.2) rings; A is frozen (outline), the token takes the chip. |
| 2 | "There is only one pair of base and bounds registers per CPU, and each process has different values." | The two MMU cells flicker; a split label shows A's `32/16` on A's PCB and B's `16/16` on B's, both different. |
| 3 | "So when the OS stops a process, it saves the base and bounds into the process structure, the PCB." | The values (a small packet of two cells, coral) fly from the MMU's cells into A's PCB card; the cells empty. |
| 4 | "When it resumes one, it restores them." | B's packet (mint) flies from B's PCB card into the cells (`16 KB`, `16 KB`); B hops on the chip (running). |
| 5 | "So that's what lives in the PCB." | Student (curious). A's PCB `base`/`bounds` fields highlight. |
| 6 | "Plus the registers you met in episode six." | Professor (happy). A small ghost of 06's register packet appears beside the base/bounds packet and merges. |
| 7 | "And because the OS controls the base, it can even move an address space." | ④ lights. B is rescheduled off; A's slot goes `ready` (outline). |
| 8 | "Deschedule the process." | A frozen, token on chip. |
| 9 | "Copy the memory to the new place." | A's slot (32–48 KB) is duplicated: a translucent copy slides to 48–64 KB (arc); a progress ring on the token. |
| 10 | "Update the saved base." | A's PCB `base` field ticks from `32 KB` to `48 KB` (`set_field`). The old slot becomes free (hatched). |
| 11 | "Resume, and the process wakes up, oblivious to its new neighborhood." | A's packet flies into the MMU (`48 KB`); A hops on the chip; the **left address-space column is shown again, unchanged**, with a coral eye "nothing changed"; A runs. Hold 1.2 s. |

**Characters:** Student (curious), Professor (happy).
**Ends with:** stage with A (running) at 48 KB, B ready, PCB cards with updated base for A, ①–④ all lit then fading out.
**Implementation notes:** this scene is the base/bounds counterpart of 06 S13; reuse `RegPacket` for the two-cell packets and `PCBCard.set_field` for the base update. Keep timer, token and packets from 06 identical in look.

### S16 — Booting the machine   (beats: B11) · ~0:45
**Purpose:** Figure 15.5: what the OS does at boot (trap table with two new handlers, timer, tables).
**Starts with:** S15 end state, cleared to the chart stage.
**Layout:** a 2-column `ProtocolChart` ("OS @ boot (kernel mode)" at x = −3.0, "Hardware" at x = 2.6), header note "(no program yet)" (DIM); rows from y = 2.2, font 20. Thumbnail at (5.2, −2.3): the CPU on the kernel seat with the token, the trap table beside it.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "The fourth moment is **exceptions**, and for that we go back to boot." | ④ is replaced by an "exceptions" tag (the fourth item reborn). The chart frame draws; the section header "OS @ boot" writes. |
| 2 | "The book shows boot and run as two timelines. First, the boot." | A power switch (`PowerSwitch`) in the thumbnail flips on; the token lands on the chip (kernel seat). |
| 3 | "The machine starts in kernel mode. The OS initializes the trap table." | OS row: **initialize trap table** (bold = privileged). The trap-table card appears in the thumbnail (empty). |
| 4 | "The hardware remembers the addresses of the handlers: system call, timer, **illegal memory access**, and **illegal instruction**." | Hardware rows: `remember addresses of…`, then four sub-rows `system call handler`, `timer handler`, `illegal mem-access handler`, `illegal instruction handler` (0.5 s each). The trap table in the thumbnail fills (last two rows new, in `VIRT` outline). Terms "illegal mem-access" and "illegal instruction" are bold. |
| 5 | "The OS starts the interrupt timer." | OS row: **start interrupt timer**; Hardware row: `start timer; interrupt after X ms`. The thumbnail's `AlarmClock` starts. |
| 6 | "It initializes the process table and the free list." | OS rows: **initialize process table**, **initialize free list**. The thumbnail shows a free-list card with the two slots. |
| 7 | "So the trap table now has two new rows." | Student (curious). |
| 8 | "Right. The OS decides, in advance, what to do when a process misbehaves." | Professor (explaining). The two new rows glow in the chart and in the thumbnail. |
| 9 | "And what it will do is usually not nice. It will most likely terminate the process." | A tiny hostile guard icon (a small stop sign `stop_sign_tag` from 05) appears by the two rows; a red `x_mark`. |
| 10 | "The OS is highly protective of the machine it is running." | The token puffs up (scale 1.15, `Indicate`). Hold 1 s. |

**Characters:** Student (curious), Professor (explaining).
**Ends with:** the finished boot chart; the thumbnail with the trap table (4 rows), the timer ticking, the free list.
**Implementation notes:** adapt **Figure 15.5** exactly (rows in order: initialize trap table; remember addresses of… (four sub-rows); start interrupt timer; hardware: start timer; initialize process table; initialize free list). First use of `ProtocolChart` with a "(No Program Yet)" third header note in the book; we keep it as a small DIM header on the right.

### S17 — Running A   (beats: B12, first half) · ~0:55
**Purpose:** Figure 15.6, first half: start A, the hardware translates every access, the OS stays out.
**Starts with:** S16 end state: the chart slides up/left and shrinks to a small "boot" legend at the top-left; new 3-column chart "OS @ run (kernel mode) | Hardware | Program (user mode)" with columns at x = −4.5, 0, 4.5.
**Layout:** full chart; a thumbnail (5.2, −2.3) shows CPU + MMU registers + the physical column (A's slot, B's slot, OS).

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Now the run, Figure 15.6." | The chart frame draws; header "OS @ run". |
| 2 | "To start process A, the OS allocates an entry in the process table, allocates memory for the process, sets the base and bounds registers, and executes a return-from-trap into A." | OS rows: **To start process A:** `allocate entry in process table`, `alloc memory for process`, `set base/bound registers`, **return-from-trap (into A)**. The thumbnail: the token puts `32 KB` / `16 KB` into the MMU's two cells; a packet lands on `k-stack(A)`. |
| 3 | "The hardware restores A's registers, moves to user mode, and jumps to A's first instruction." | Hardware rows: `restore registers of A`, `move to user mode`, `jump to A's (initial) PC`. The thumbnail chip rides up (`cpu_ride`), gauge → USER, A hops on. |
| 4 | "A runs." | Program row: **Process A runs**. |
| 5 | "To fetch each instruction, the hardware translates the virtual address and fetches." | Program: `Fetch instruction`. Hardware: `translate virtual address`, `perform fetch`. In the thumbnail, an address chip passes the MMU; the physical cell lights. |
| 6 | "For an explicit load or store, it checks that the address is legal, translates, and performs it." | Program: `Execute instruction`. Hardware: `if explicit load/store: ensure address is legal / translate virtual address / perform load/store`. Thumbnail: chip ✓ → adder → physical. |
| 7 | "The OS isn't involved at all." | A highlight bar sweeps the OS column (empty at these rows); the OS token in the thumbnail sleeps (dimmed). Hold 1 s. |

**Characters:** Professor (explaining), Student neutral.
**Ends with:** the 3-column chart up to row `perform load/store`; `Process A runs` with `(A runs…)`; the thumbnail shows A running at the user seat.
**Implementation notes:** continue with the same `ProtocolChart` object used in S18; adapt **Figure 15.6** rows in the book's order (up to "(A runs…)"). Bold = privileged / kernel-mode actions. Thumbnail is the same "world" assets at scale 0.35.

### S18 — The switch, the bad load, and the kill   (beats: B12, second half) · ~1:05
**Purpose:** timer, `switch()` with base/bounds saved, B's illegal load, exception handler kills B and frees memory.
**Starts with:** S17 end state.
**Layout:** continues the chart (older rows dim to 0.5, scrolls). Thumbnail as in S17 with B's slot at 16 KB.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "At some point the timer fires." | Hardware row: **Timer interrupt**. The `AlarmClock` in the thumbnail rings; a bolt hits the chip. |
| 2 | "The hardware moves to kernel mode and jumps to the timer handler." | Hardware rows: `move to kernel mode`, `jump to handler`. The thumbnail chip rides down; token hops on; gauge → KERNEL. |
| 3 | "The OS decides to run B. It calls `switch()`: save A's registers into A's process structure, *including its base and bounds*; restore B's, including B's." | OS rows: **Handle timer**, `decide: stop A, run B`, `call switch() routine`, `save regs(A) to proc-struct(A) (including base/bounds)`, `restore regs(B) from proc-struct(B) (including base/bounds)`. The thumbnail MMU registers flicker `32 KB → 16 KB`: the `base` cell swaps (mint). "(including base/bounds)" is highlighted in `VIRT` accent. |
| 4 | "Return-from-trap into B." | OS row: **return-from-trap (into B)**. |
| 5 | "The hardware restores B's registers, moves to user mode, and B runs." | Hardware rows: `restore registers of B`, `move to user mode`, `jump to B's PC`. Program: **Process B runs**. The thumbnail chip rides up; B hops on. |
| 6 | "And B executes a bad load: an address outside its bounds." | Program row: `Execute bad load`. A chip `20 KB` (outside B's 16 KB bounds) leaves the CPU, hits the comparator (`16 KB`): red flash. |
| 7 | "The hardware says no: it moves to kernel mode and jumps to the trap handler." | Hardware rows: `load is out-of-bounds; move to kernel mode; jump to trap handler`. Red bolt; the chip rides down; trap-table row `out-of-bounds → handler` lights. |
| 8 | "The OS decides to kill B, deallocates its memory, and frees its entry in the process table." | OS rows: **Handle the trap**, `decide to kill process B`, `deallocate B's memory`, `free B's entry in process table`. B (thumbnail) gets a red `x_mark` and fades; B's slot (16–32 KB) hatches back to free. |
| 9 | "It's the same dance as episode six, with memory attached!" | Student (excited). A thin tag "← Ep. 06" on the chart's right edge. |
| 10 | "Exactly. In most cases the OS just sets up the hardware and lets the process run directly. Only when a process misbehaves does the OS have to get involved." | Professor (proud). A highlight bar sweeps the Program and Hardware columns (long), then taps the OS column (short rows). Hold 1.5 s. |

**Characters:** Student (excited), Professor (proud).
**Ends with:** the full Figure 15.6 chart; thumbnail with A's slot at 32 KB, B's freed, token on the chip in kernel mode.
**Implementation notes:** adapt **Figure 15.6** exactly. Reuse `ProtocolChart.sweep` for the bars. Step 6 uses an out-of-bounds chip with an arbitrary number (the book doesn't give one). Chart dims older rows and scrolls so the current row stays between y = 2.0 and −1.6.

### S19 — The big picture   (beats: B13) · ~0:30
**Purpose:** pull the idea together as the series' Illusion split, and pay off protection with the scribbler from 06.
**Starts with:** S18 end state; the chart slides left and shrinks to a small legend "address translation" (top-left), the thumbnail enlarges and relaxes into the translation stage; no characters change.
**Layout:** Illusion split: left "what each process sees" — three small address-space columns A, B, C (all `0` at top, each coral/mint/gold) at x = −5.6, −4.0, −2.4; right "what really happens" — physical column at (4.9, 0.3) with three slots (B 16KB, A 32KB, C 48KB) and the OS at 0–16KB. The MMU at center.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Step back. This is address translation: the hardware adds a base and compares to a bound on every reference, quickly." | The three columns appear at left; the physical column at right; each column's reference flies through the MMU (a quick triple pulse, in A, B, C colors) and lands in its own slot. |
| 2 | "The result is the illusion we promised: each process has a private address space starting at zero, while many of them really sit in one memory, at different places." | Left columns all pulse at `0`; right slots light at 16, 32, 48. Divider flashes. |
| 3 | "All of it transparent to the process." | The eye icons (three, coral/mint/gold) open and close: no change. |
| 4 | "And it gives us **protection**. Remember the process that scribbled over everything in episode six?" | A scribbler (A with a coral scribble line from 06 S01, `Process` with a small pencil) walks onto the CPU; its scribble arrow aims at the OS region. |
| 5 | "Now it can't." | A chip `20 KB` (the scribble, outside A's bounds) hits the comparator: red flash and bolt; the OS region stays untouched. |
| 6 | "If processes could overwrite memory freely, they could overwrite the trap table and take over the system." | A trap-table card on the OS region gets a scribble that fades (what would happen), and a padlock closes on it (`Padlock.close`). |
| 7 | "Without protection, the OS wouldn't be in control." | Hold 1 s on the closed padlock on the OS region. |

**Characters:** none on screen at the beginning, then Professor (neutral) in the corner for the last line.
**Ends with:** the Illusion split with three processes, the OS region with a closed padlock; term strip "exception".
**Implementation notes:** the scribbler is drawn with the same coral scribble marks used in 06 S01; reuse `Process`; use the default `IllusionSplit` titles (now at y = 2.25 via `title_y`). "protection" is not re-highlighted: it was introduced in 06.

### S20 — The price: wasted space   (beats: B14) · ~0:45
**Purpose:** internal fragmentation, the flaw that motivates segmentation.
**Starts with:** S19 end state; the stage dims; focus on A's slot (32–48 KB).
**Layout:** the physical column zooms to center (0, 0.3), scale 1.6 (so A's slot is ~2.8 tall). Characters in corners.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Of course, there's a catch. Look at the slot of process A, thirty-two to forty-eight kilobytes." | The column enlarges (`animate.scale`) and shifts so A's slot is centered; the other slots dim; the labels `32 KB`, `48 KB` stay. |
| 2 | "The code and heap are at the top. The stack is at the bottom." | A's slot shows its internal regions (Figure 15.2's detail): `Code`, `Heap` at the top; `Stack` at the bottom, each tinted coral. |
| 3 | "In between: free space the process isn't using, but that nobody else can use either." | The middle region is hatched (`hatch_rect`) with the label "allocated but not in use"; a red bracket marks it; a second process D (sky) tries to squeeze in and bounces off the slot wall. |
| 4 | "It's inside the slot we allocated." | The slot's outline thickens (`Indicate`). |
| 5 | "This waste is called **internal fragmentation**: space *inside* an allocated unit that goes unused." | Term unveil: *internal fragmentation*. |
| 6 | "Physical memory may have room for more processes, but we only offer fixed-size slots." | Student (sad). The free-slot entries in the neighboring areas show D's size not fitting; a cross. |
| 7 | "So most of the slot is air?" | Student (sad). The hatched region pulses. |
| 8 | "Most of it. We need something more flexible." | Professor (thinking). Hold 1.5 s on the hatched region. |

**Characters:** Student (sad), Professor (thinking).
**Ends with:** the zoomed slot with a large hatched middle; term strip "internal fragmentation".
**Implementation notes:** adapt the inside of **Figure 15.2** (code, heap, "allocated but not in use", stack) for the slot. D (sky) is only a prop for the squeeze-in gag.

### S21 — Recap   (beats: B15) · ~0:30
**Purpose:** five takeaways.
**Starts with:** S20 end state.
**Layout:** the stage fades; a numbered list at left (−5.6..1), font 26, one line each; an icon per line at x = 4.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "So, today:" | The world `FadeOut`; header "Recap" in `VIRT`. |
| 2 | "**Address translation**: the hardware turns each virtual address into a physical one, on every reference." | Line 1 writes; icon: an address chip passing the adder (`virtual → physical`). |
| 3 | "**Base and bounds**: add the base, check the bound. Fast, simple, transparent." | Line 2; icon: base/bounds registers with the comparator. |
| 4 | "The hardware needs **modes, registers, privileged instructions and exceptions**; the OS needs a **free list**, a save and restore at context switch, and exception handlers set at boot." | Line 3; icon: the six-icon checklist (compressed) and a PCB card. |
| 5 | "**Protection**: a process can only touch its own address space." | Line 4; icon: the MMU bouncing a scribble. |
| 6 | "The cost is **internal fragmentation**." | Line 5; icon: the hatched slot. Hold 1.5 s. |

**Ends with:** the full recap list. Section badge fades out.

### S22 — Teaser: slice it up   (beats: B16) · ~0:25
**Purpose:** hook for 16: segmentation.
**Starts with:** S21 end state.
**Layout:** dialogue mode (Student (−2.6, −1.7), Professor (2.6, −1.7), scale 0.85). A's 16 KB address-space column at center-left (−1.2, 0.8), 1.2 × 3.0.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "The stack and the heap are tiny. Why give them a whole sixteen-kilobyte slot?" | The recap fades. Student (curious). A's column appears with a large free middle highlighted (hatched). |
| 2 | "What if we didn't? What if the code, the heap and the stack each got their own base and bounds?" | Professor (happy). Two thin lines slice the column into three pieces (code, heap, stack). |
| 3 | "Three pairs of registers, three little slots!" | Student (excited). The three pieces float apart and fly to three different places in a small physical column at right; each lands with its own tiny tag `base / bounds`. The hatched middle disappears. |
| 4 | "That's the next episode: **segmentation**." | Professor (proud). Hold 1 s. Cut to black (FadeOut all, 0.5 s). Then "Next: 16 · Segmentation" in `TEXT` with a `VIRT` dot. Hold 2 s. |

**Characters:** Student (curious → excited), Professor (happy → proud).
**Ends with:** black end card.
**Implementation notes:** the pieces are copies of the `Memory` regions (`region(name)`); no term unveil or note here (the end card carries the name).

## New assets needed
**Dependency (episode 13):** `address_space_16kb()` and `physical_512kb()` / `memory_copy_fly()` from `ostep_lib/props/p13_addrspace.py` (spec in Ostep/Scenes/13-vm-intro.md, "New assets needed"). Use them for every address-space column here; the physical 64 KB column stays a plain `Memory` (not the 512 KB one). `memory_copy_fly` can drive the relocation copy in S06 and S15.

Nothing below exists in `ostep_lib` yet. Everything else is reused from 04–11 (see the persistent assignments).
- **`MMU(base=..., bounds=...)`** (prop, `p15_*.py`): the box described above (4.4 × 1.8), a `RegisterBank` with `bounds` and `base` cells, a comparator circle `<`, an adder circle `+`, and the wires. Methods: `translate(chip, va, base, bounds, ok=True)` returns one animation that moves an `AddressChip` from the CPU through comparator → adder to a given exit point and morphs its text from the virtual to the physical value (when `ok=False`, the chip bounces off the comparator, the comparator flashes red and a red bolt leaves); `set_registers(base, bounds)` (animation), `label_on()` to write the "MMU" label (S11), `show_parts(base_only=True)` to build the S08 partial state.
- **`AddressChip(text, kind="virtual"|"physical", color)`**: the small pill (0.9 × 0.32). `.retext(new)` animation, `.hop_to(point)`.
- **`TranslationStage(...)`** (layout helper, optional): builds the left address-space column, the physical column, the CPU and the MMU at the positions above, with helpers `a_cell(addr)` and `phys_cell(addr)` to light cells by address, so S08–S11 and S19 share one setup.
- **`eye_icon`** (an eye with a pupil; the shared-assets note already lists `EyeIcon`): used in S06 and S09 for "A doesn't notice". Reuse if it exists.
- **Small icons:** `checklist_row(icon, text)` helper for S12–S13; a "moving box" glyph for S07 (could be a rectangle with a double-headed arrow). All simple primitives.
- **Hatch for "not in use":** reuse `hatch_rect` (04). No new asset.
- **Free-list card:** reuse `PCBCard` (header "FREE LIST", fields = ranges); no new asset, but needs a way to strike or remove a field (`FadeOut` + shift is enough).
- **Memory with boundary labels:** the physical column needs address labels at region boundaries (0, 16KB, 32KB, 48KB, 64KB). If `Memory(regions=…)` can't take a per-boundary list, draw them as separate `Text` objects next to the column.

## Open questions
- **Length:** ~16:20 is above the 8–15 minute target. The biggest candidates to trim: S15 (the "move an address space" half), S07 (static relocation as a full scene instead of a one-line aside), and S11 (the table). Cut one or all? (Not cut yet, per the coordinator.)
- **MMU stage vs. Figure 15.6 thumbnail:** I show the figures as `ProtocolChart` plus a small stage thumbnail (like 06 S08), so the base register is seen changing at the switch. Is a thumbnail enough, or should the stage take the whole screen and the chart become a small side listing?
- **Process C (S11):** the book's 4 KB example conflicts with the "all the same size" assumption. I mark it "(tiny example)" and use gold C. Alternatively, use A's real numbers (0, 1 KB, 3000 → 32 KB, 33 KB, 35,768; 17 KB → fault). Which is better?
- **Key terms:** I chose *address translation*, *dynamic relocation*, *MMU* and *internal fragmentation* as the four unveils; the other ten terms are notes. Should *base and bounds* replace one of them?
- **Figure 15.3 as names only:** I show the six hardware requirements as icon + short name (the book's "Notes" column is spoken, not shown) to stay under 25 words. OK?
- **Dependence on 13 and 14:** the scenes assume 13 introduced the address-space column (code / heap / free / stack, 0 at top) and virtual addresses, and 14 `malloc`/`free`. Recheck the visual style of the address-space column when those scene files land.
