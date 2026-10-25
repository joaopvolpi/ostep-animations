# 09 — Scheduling: Proportional Share · Scene breakdown
> Script: Ostep/Scripts/09-cpu-sched-lottery.md · Scenes: 23 · Est. duration: ~14:00

## Visual overview
- **Core metaphor: a pie of CPU time, and a promise about how it's cut.** The cold open shows a 75/25 pie (coral / mint). Every scheduler in the episode is judged by one question: does the Timeline's coral/mint split match the pie? The pie is a small recurring "target" icon in the top-right corner during the lottery and stride scenes, and the Timeline's running tally is compared against it.
- **Three mechanisms, three visual forms** (so the viewer can tell them apart at a glance):
  1. **Lottery:** a raffle drum spitting out numbers, tickets laid on a **number strip** (a ruler). The winner is found by *where a number lands on the ruler*.
  2. **Stride:** **runners on lanes** along a pass-value number line. The runner farthest behind (lowest pass) is lit by the **Spotlight** and takes a step whose length is its stride.
  3. **CFS:** **vruntime meters** (small vertical fuel-gauge bars under each process) and a **red-black tree**. The lowest meter is lit by the Spotlight; the tree stores them in order.
- **Spotlight = policy ("which")**, as in 04 (S08). It appears in all three mechanisms to show what each one *does* with its numbers: always the same job (pick one), different rules.
- **Timeline** (from 04) is the shared ledger: lottery/stride/CFS runs all fill the same kind of Timeline, using the series' state encoding (running = solid, ready = outline, etc.).
- Props used (from the bible and ostep_lib): Crux card, Aside/Tip card, Term highlight, Section badge, CPU, Timeline, Queue, Code block, Spotlight, Process, PCB card (for the "state" tag), server_rack, stopwatch, ClockIcon, hop_to, `MathTex`. Characters: Professor, Student, Computer (only in the cold open and the teaser).

### Persistent assignments
| Thing | Look | Notes |
|---|---|---|
| Process **A** | `Process(label="A", color=PROCESS_COLORS[0])` (coral) | Same as 04. Always the first / "important" job. |
| Process **B** | `PROCESS_COLORS[1]` (mint) | |
| Process **C** | `PROCESS_COLORS[2]` (gold) | Lottery implementation example, stride, CFS Fig. 9.4. |
| Process **D** | `PROCESS_COLORS[3]` (sky) | CFS Fig. 9.4, and the "new job" in S13. |
| **Ticket** | Small rounded stub (0.35 × 0.2), notched on both sides, in the owner's process color, with `TEXT` stub lines | Stacks: a "ticket stack" is a few stubs fanned out, with a count label ("75"). Reused in S03–S13. |
| **Target pie** | 75/25 pie (coral sector 270°, mint sector 90°), radius 0.45 | Top-right corner (6.0, 3.0), `DIM` stroke, labeled "target" in font 18. Appears S01, returns S04/S10/S12/S21. |
| CPU home | `CPU_COLOR` chip, 1.4 × 1.4, at **(0, 0.6)** | The running process stands on top of it, as in 04. |
| Timeline home | Along the bottom, y = −2.2, x from −5 to 5, rows 0.45 tall | Same as 04. State encoding as in 04. |
| Characters (corner mode) | Student at (−5.8, −2.8), scale 0.75; Professor at (5.8, −2.8), scale 0.75, `flip()` | Default. "Dialogue mode" in S01 and S23: Student (−2.6, −1.2), Professor (2.6, −1.2), scale 1. |
| Section badge | Top-left (−6.6, 3.6): `VIRT` dot + "09 · Proportional Share", font 22, `DIM` | Appears in S02; stays until S22. |
| Term highlight | As in 04: written at (0, 2.9), font 54, `VIRT` underline, shrinks to top-right (6.6, 3.6) | Every bolded term's first appearance, except where noted. In the lottery and stride scenes the target pie takes (6.0, 3.0), so the term strip moves to (4.6, 3.6). |
| Mono figures | `MONO_FONT` for numbers in tables, code and strides | |

## Scenes

### S01 — A promise, not a metric   (beats: B01) · ~0:50
**Purpose:** feel the gap: existing schedulers chase a number (turnaround, response); none lets you promise a share like 75/25.
**Starts with:** empty (BG).
**Layout:** server rack icon at (0, 0.8), scale 1.4. Pie target at center-right (3.2, 0.8), radius 1.1. Characters in dialogue mode, entering at step 4. Three scheduler chips ("RR", "SJF", "MLFQ") at the bottom (−2.4, −2.4), (0, −2.4), (2.4, −2.4).

| # | Narration (exact words the action lands on) | On screen / animation |
|---|---|---|
| 1 | "Picture a cloud server." | `FadeIn` the server rack icon (from `ov_icons`) at (0, 0.8); a CPU chip glows on its front panel. |
| 2 | "Two customers share one CPU. One of them paid for three quarters of the machine. The other paid for one quarter." | Two small Process creatures (A coral, B mint) hop out of the rack to (−3.2, 0.8) and (−3.2, −0.2) as "customers". The pie draws at (3.2, 0.8): coral 75%, mint 25% (`Create` sectors, labels "75%" / "25%"). |
| 3 | "Easy. Round robin, with a twist." | Student slides in (curious) at the dialogue position. |
| 4 | "Round robin gives everyone the same share." | The "RR" chip (rounded rectangle, `DIM` frame) rises toward the pie; inside the chip, an even 50/50 split flashes; it bounces off with a small "≠". Professor slides in (thinking). |
| 5 | "Shortest-job-first promises nothing about shares." | "SJF" chip rises; a "?" pops over it; it drops. |
| 6 | "And the multi-level feedback queue *guesses* from behavior and hopes for the best." | "MLFQ" chip rises with a small question-mark cloud; a fuzzy outline of the pie wobbles and doesn't match; it drops. |
| 7 | "All of them chase a number: turnaround time, response time." | The three chips glow once each, each with a tiny label under it ("turnaround", "response", "guess"). |
| 8 | "None lets you say, on purpose, 'you get seventy-five percent.'" | The pie pulses (`Indicate`). Chips dim to 30%. |
| 9 | "So what would a scheduler that *keeps* that promise even look like?" | Student (confused). |
| 10 | "Surprisingly, like a raffle." | Professor (happy). A raffle drum (see New assets) rolls in from the right and rests at (3.2, −1.0), spinning slowly. Hold 1 s. |

**Characters:** Student (curious → confused), Professor (thinking → happy).
**Ends with:** server, two customers, pie, raffle drum; both characters in dialogue mode.
**Implementation notes:** the chips are simple `RoundedRectangle` + `Text`. The "bounce off" is `hop_to` with a bigger arc and a `Rotate`. The pie is `Sector` mobjects, not `PieChart`, so the colors stay under our control.

### S02 — The Crux   (beats: B02) · ~0:25
**Purpose:** pose the question and name the category: proportional-share.
**Starts with:** S01 end state.
**Layout:** Crux card centered (0, 0.3), 9 × 3. Characters glide to corner mode.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | (transition) | Server, customers, chips and drum `FadeOut`; the pie shrinks to the top-right target position (6.0, 3.0). The Section badge "09 · Proportional Share" writes in at the top-left. Characters glide to corners. |
| 2 | "A raffle. Hold that thought, because it brings us to the crux: How to share the CPU proportionally?" (then the subtitle question, read as it fades in) | Crux card, `VIRT` frame, header "THE CRUX" (font 22): **"How to share the CPU proportionally?"** (font 34). Subtitle (font 22, `DIM`): "What are the key mechanisms for doing so? How effective are they?" |
| 3 | "This kind of scheduler is called **proportional-share**, or sometimes **fair-share**." | Term highlight "proportional share" (alt label "fair-share" underneath in `DIM`). |
| 4 | "Instead of minimizing a time, it tries to guarantee that each job gets a certain percentage of the CPU." | The pie pulses; a tiny Timeline strip (one row, 10 cells) draws under the crux card and fills 7–8 coral, 2–3 mint, as a preview. |
| 5 | "Let's find out how." | The card shrinks to a one-line strip at top-center (0, 3.2), font 24 "How to share the CPU proportionally?". The preview strip fades. |

**Characters:** corner mode; Student looks at the card (`look_at`), Professor neutral.
**Ends with:** section badge, crux strip at top-center, target pie at (6.0, 3.0), term strip "proportional share" at (4.6, 3.6), characters in corners.

### S03 — Tickets   (beats: B03, first half) · ~0:45
**Purpose:** a ticket = a share; the percent of tickets you hold is the percent of CPU you should get. Define the lottery rule.
**Starts with:** S02 end state.
**Layout:** two Process creatures A (−3.6, −0.4) and B (3.6, −0.4), scale 1. Each holds a ticket stack above it (A's stack at (−3.6, 0.9), B's at (3.6, 0.9)). A number strip (a horizontal ruler, x −5..5, y = −1.6) with ticks at 0, 25, 50, 75, 99. The CPU at (0, 1.0), lower in the frame of the top strip.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Here's the idea, from a paper by Waldspurger and Weihl." | A paper icon with "Waldspurger & Weihl, 1994" fades in at (0, 2.2) and slides up into the corner. |
| 2 | "Every so often, hold a lottery to decide who runs next." | The raffle drum appears at the CPU's left (−1.9, 1.0) and spins; a number ball pops out and hovers. |
| 3 | "Processes that deserve more of the CPU get more chances to win. That's **lottery scheduling**." | Term highlight "lottery scheduling". A and B appear below; their ticket stacks `FadeIn` (A tall, B short, no numbers yet). |
| 4 | "The thing you hold is a **ticket**." | Term highlight "ticket". One stub flies from A's stack to the center and enlarges briefly. |
| 5 | "Tickets represent a share. The percent of the tickets you own is the percent of the resource you should get." | A caption writes at (0, −2.9), font 26: "tickets = share". The stacks show counts: "75" over A, "25" over B. |
| 6 | "Say process A holds seventy-five tickets and process B holds twenty-five. A hundred in total, numbered zero to ninety-nine." | The number strip draws (0..99). A's 75 stubs stack along 0–74, B's along 75–99, each in its color. Labels "0", "74", "75", "99" under the ruler; a "total: 100" tag at the right end. |
| 7 | "Each time slice, the scheduler picks a winning number, finds its owner, and runs that process." | A winning number "63" pops out of the drum and drops onto the ruler (a marker), landing in A's coral stretch. A hops onto the CPU (running). Hold 1 s. |
| 8 | "A raffle! Draw a ticket, run the winner!" | Student (excited). |

**Characters:** Student (excited at step 8).
**Ends with:** A and B with ticket stacks, number strip 0–99 with A/B stretches, CPU with A running, drum, winning-ticket marker at 63.
**Implementation notes:** the number strip is a `NumberLine` (0–99, no numbers) overlaid with colored `Rectangle`s; a simple pointer `Triangle` is the marker. The drum is a new prop (see New assets).

### S04 — Twenty draws   (beats: B03, second half) · ~0:45
**Purpose:** a concrete run: 20 slices, B wins 4 (20%) — near, but not exactly, 25%. It's probabilistic, not a guarantee.
**Starts with:** S03 end state.
**Layout:** number strip stays at y = −0.2. A **Timeline** (one CPU row, 20 ticks) appears along y = −2.2, x −5.8..5.8. The pie target at (6.0, 3.0). A running tally appears at (0, 2.2): "A: 0 · B: 0".

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Let's draw twenty." | The Timeline draws, ticks 1–20; the tally appears. The CPU and process creatures shrink to scale 0.7 and move up. |
| 2 | "Sixty-three: A. Eighty-five: B. Seventy: A. Thirty-nine: A. Seventy-six: B." | Five draws, ~0.9 s each. Each: the drum spits a number; the marker lands on the ruler; the owner's color flashes; the tick fills in the owner's color. Sequence: 63 A, 85 B, 70 A, 39 A, 76 B. |
| 3 | "And so on." | The remaining 15 draws run quickly (0.25 s each), filling the Timeline: A B A A B A A A A A A B A B A A A A A A (winning numbers 17 29 41 36 39 10 99 68 83 63 62 43 0 49 12 flicker at the marker). |
| 4 | "After twenty slices, A has run sixteen times and B four." | The tally settles at "A: 16 · B: 4". A brace under the Timeline's B ticks reads "4 / 20 = 20%". |
| 5 | "Four out of twenty. That's twenty percent, not twenty-five." | Student (confused). The target pie pulses next to a new label "20%", struck lightly by a "≠ 25%" tag. |
| 6 | "Right. Lottery scheduling is *probabilistically* correct, not guaranteed." | Professor (explaining). Under the brace the caption "probabilistic, not guaranteed" writes. |
| 7 | "The longer the two jobs compete, the closer they get to seventy-five and twenty-five." | The Timeline extends right (`extend`) with fast ticks; the A/B proportions in a small bar above it drift toward 75/25. A thin dotted line at 75% of the bar; the actual proportion wobbles toward it. Hold 1 s. |

**Characters:** Student (confused), Professor (explaining).
**Ends with:** completed 20-tick Timeline (then extended), tally "A: 16 · B: 4", proportion bar. Transition: all fades except the section badge and crux strip.
**Implementation notes:** pre-compute the 20-tick sequence (above, matching the book's output). Use `Timeline.fill_cpu` per tick with the owner's color.

### S05 — Tip: use randomness   (beats: B04) · ~0:40
**Purpose:** why random is a good design choice: three advantages.
**Starts with:** section badge and crux strip only.
**Layout:** Aside/Tip card centered-left (−1.0, 0.2), 6.4 × 4.6, header "TIP". Three vignettes inside the card in a vertical stack, each 1.2 tall at y = 1.2, 0, −1.2, with a number badge 1–3. The characters in corners.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Hold on. We're letting the OS flip coins? Isn't that sloppy?" | Student (frustrated). A coin icon flips over the CPU with a "sloppy?" thought bubble (`thinks`). |
| 2 | "It's the most beautiful part. Random buys you three things." | Professor (happy). The Tip card slides in from the left: "TIP: Use randomness". |
| 3 | "One: no nasty corner cases. Some clever algorithms have a workload that makes them fall apart, like the LRU policy we'll meet in the memory episodes." | Vignette 1: a small gear-shaped "clever algorithm" with a weird jagged workload bar bumping into it → cracks; a tag "LRU → Ep. 22". |
| 4 | "Random has no such workload." | The same jagged workload hits a die icon, which just shows random faces. A green check (use `tick_mark()`). |
| 5 | "Two: almost no state. A counting scheduler must track every process's CPU use; random only needs each process's tickets." | Vignette 2: left, three PCB cards with many fields ("cpu used: 12.4 ms"…); right, three PCB cards with only "tickets: 100". The left side is struck through. |
| 6 | "Three: speed, as long as the random number is quick." | Vignette 3: a `stopwatch` icon; the drum spits a ball in a blink. |

**Characters:** Student (frustrated), Professor (happy).
**Ends with:** the Tip card on screen with three vignettes. Transition: the card slides out.
**Implementation notes:** keep each vignette to ~1 glyph + ≤3 words. Use the Aside card prop with custom children.

### S06 — Ticket currency   (beats: B05, part 1) · ~0:35
**Purpose:** a user can allocate tickets among their own jobs in any currency; the system converts to global tickets.
**Starts with:** section badge and crux strip.
**Layout:** two user cards at left: "User A" (−4.6, 1.4) and "User B" (−4.6, −1.0), each 2.6 × 1.4 with a `DIM` frame, "100 tickets" in font 24. Jobs to the right (x = −0.4): A1 (coral, y = 1.9), A2 (coral, lighter, y = 0.9), B1 (mint, y = −1.0). Global column at the right (4.2, 0.4): a ticket stack "global" with total "200".

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "The ticket is a flexible tool. The book gives three tricks." | Three small tags appear in a row at the top: "currency", "transfer", "inflation" (`DIM`). The first lights up. |
| 2 | "**Ticket currency.** User A has a hundred tickets and two jobs, A1 and A2." | Term highlight "ticket currency". User A's card and jobs A1, A2 slide in (as small process chips). |
| 3 | "She gives each five hundred tickets in *her own* currency." | Under each of A1 and A2: "500 A-tickets" in a coral-tinted bubble. A caption "A's currency" at the card. |
| 4 | "User B has a hundred tickets and one job, B1, with ten of his." | User B's card and B1 slide in; B1 shows "10 B-tickets". |
| 5 | "The system converts: A1 and A2 become fifty global tickets each, B1 becomes a hundred." | Converter arrows (labeled "→ global") run from each job to the global column: "500 A-tickets → 50", "500 A-tickets → 50", "10 B-tickets → 100". The numbers `Transform` in place. |
| 6 | "Two hundred in total, and the lottery runs on those." | The global column stacks to 200 (A1 50, A2 50, B1 100). The drum at the right spins and drops a number onto the column. |

**Characters:** none (corners visible, passive).
**Ends with:** the currency diagram complete, "currency" tag lit.
**Implementation notes:** to avoid clashing with Process A/B, the user cards are neutral (`DIM` frame, white text); only the job chips use coral/mint. Mention this in code comments.

### S07 — Transfer and inflation   (beats: B05, part 2) · ~0:30
**Purpose:** two more ticket tricks; why inflation needs trust.
**Starts with:** S06 end state. The currency diagram slides out left; the "transfer" tag lights up.
**Layout:** left half "transfer" (−3.2, 0.4): a client Process (A coral, label "client") and a server (gold, label "server") facing each other. Right half "inflation" (3.2, 0.4): a Process with a ticket stack, plus a second greedy Process.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "**Ticket transfer.** A client asks a server for help, and lends it its tickets while the server works." | Term highlight "ticket transfer". A request packet goes from the client to the server; the client's ticket stack hops over to the server's stack (`hop_to`); the server's stack doubles. |
| 2 | "The server hands them back when it's done." | The stack hops back. A tick mark. |
| 3 | "**Ticket inflation.** A process raises or lowers its own ticket count." | Term highlight "ticket inflation". The right panel lights up: a process's stack grows (50 → 80) and shrinks back. |
| 4 | "Among strangers that's useless, since a greedy process would print tickets and take over." | A second process, grey-tinted, grows its stack to absurd height (1,000,000) and swallows the CPU icon; a red "✕" (`x_mark`). |
| 5 | "Among friends, a process that needs the CPU can just say so." | Two friendly processes (handshake icon) one raising a stack slightly; a green check. |
| 6 | "So a ticket is a unit of ownership." | Student (curious). |
| 7 | "Exactly. Need to represent a proportion of anything? Try a ticket." | Professor (proud). A tiny memory column and a CPU appear next to a ticket ("hypervisor memory share") for 1.5 s as a hint of generality (no explanation), then fade. |

**Characters:** Student (curious), Professor (proud).
**Ends with:** transfer + inflation panels; transition: everything fades except the section badge and crux strip.

### S08 — Implementation: the list   (beats: B06, first half) · ~0:50
**Purpose:** the scheduler is a tiny loop: random number, list of jobs, running counter.
**Starts with:** section badge and crux strip.
**Layout:** adapt **Figure 9.1**. A **Code block** (the decision code, 16 lines at font 18, monokai) at the left (−3.6, 0.0). At the right, the **linked list** (see New assets): head → [Job:A Tix:100] → [Job:B Tix:50] → [Job:C Tix:250] → NULL, nodes as gray discs (circle fill `DIM` 0.25 with the process color as outline), along x = 0.8..6.0, y = 1.2. A counter display at (3.4, −0.8) "counter = 0", and "winner = ?" at (3.4, −1.6).

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "How hard is it to build? Barely." | The Code block `FadeIn`; the "while (current)" lines are dimmed. |
| 2 | "You need a good random number generator, a list of processes, and the total number of tickets." | The drum (small) appears with "getrandom(0, totaltickets)" label; the list draws node by node (A, B, C); a "total: 400" tag at the list's right end. The code highlight bar rests at line 6 (`int winner = getrandom(...)`). |
| 3 | "Three jobs. A has a hundred tickets, B has fifty, C has two hundred and fifty. Four hundred in total." | Node labels write: "A · 100", "B · 50", "C · 250". Each node's stack of stubs is drawn proportionally under it (100, 50, 250 wide bars in coral, mint, gold). |
| 4 | "Say the random number comes out as three hundred." | The drum emits "300"; `winner = 300` appears at (3.4, −1.6). |
| 5 | "Walk the list with a counter. Start at zero." | A pointer `current` (an arrow labeled "current") appears at the head. The code highlight bar moves to line 9 (`node_t *current = head;`) and then line 10 (`while (current)`). The counter shows 0. |
| 6 | "A adds a hundred: the counter is a hundred. Is that more than three hundred? No, keep going." | `current` at A; code bar on line 11, counter ticks 0 → 100; line 12 `if (counter > winner)` bar, a small "100 > 300? no" bubble (red ✕). |
| 7 | "B adds fifty: a hundred and fifty. Still no." | `current` hops to B (line 14); counter 100 → 150; "150 > 300? no". |
| 8 | "C adds two hundred and fifty: four hundred. Now it's more than three hundred. Stop. C wins." | `current` hops to C; counter 150 → 400; "400 > 300? yes" (green check); the code bar jumps to `break;` (line 13), then the C node glows `CPU_COLOR` and C hops (as a Process creature) toward the CPU icon on the right. |

**Characters:** corner mode, passive.
**Ends with:** list with C highlighted, code at line 13, counter "400".
**Implementation notes:** the book's Figure 9.1 code is shown verbatim (comments trimmed to fit: ≤ 12 visible lines; dim the comment lines). The bar uses the same code-highlight bar as 04 (S18). Counter is a `DecimalNumber` with `ChangingDecimal`.

### S09 — The ruler view   (beats: B06, second half) · ~0:40
**Purpose:** the same lookup as a picture: tickets laid end to end; the winner lands in someone's stretch. A tip about sorting.
**Starts with:** S08 end state.
**Layout:** the code block and counter fade. The tickets lay out as a 0–400 ruler at y = 0.4, x −5.5..5.5: A (coral, 0–100), B (mint, 100–150), C (gold, 150–400). Marker at 300. Below: sorted-list demo at y = −1.5.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "It's like laying the tickets end to end on a ruler…" | Student (excited). The list nodes unfold into bars along the ruler, in order (A, B, C), `Transform`ing from the linked-list nodes. |
| 2 | "…and seeing whose stretch the winner lands on!" | The marker "300" drops from the top onto C's gold stretch; the ruler tick glows. |
| 3 | "That's the picture." | Professor (happy). |
| 4 | "A tip: sort the list from most tickets to fewest." | A **Tip** card header appears at the bottom (small, "TIP"). The ruler's blocks reorder in an animated swap to C, A, B (gold first). The linked list below also reorders: C → A → B. |
| 5 | "It doesn't change correctness, but the big holders get found early, so you walk fewer nodes." | Under each order, a counter of nodes visited for a random winner: "unsorted: 3 hops → sorted: 1 hop" (a quick demo with the 300 marker landing in C). A green check. |

**Characters:** Student (excited), Professor (happy).
**Ends with:** sorted ruler C, A, B and sorted list. Transition: fade to section badge + crux strip.

### S10 — How fair is it?   (beats: B07) · ~0:50
**Purpose:** a fairness metric F; short jobs are unfair under the lottery, long jobs converge; and the ticket-assignment problem is open.
**Starts with:** section badge and crux strip.
**Layout:** top half: two-row Timeline (jobs 1 and 2, each 100 tickets: two process-colored rows, coral and mint) at y = 1.6 and 1.1, x −4.5..4.5. Bottom half: **Axes** for the fairness plot at (0, −1.2), 6.5 × 2.6.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Let's measure that fairness. Two jobs, same length, a hundred tickets each." | Two processes A and B with equal ticket stacks (100 each). Timeline rows appear. |
| 2 | "Ideally they'd finish at the same time." | Both rows' blocks end at the same tick with a vertical dashed line. |
| 3 | "The book defines a **fairness metric**: the time the first job finishes, divided by the time the second finishes." | Term highlight "fairness metric". `MathTex` F = T₁ / T₂ writes at (0, 2.4). |
| 4 | "Ten and twenty give zero point five." | A's row ends at 10 (marker), B's at 20; the equation fills: F = 10/20 = 0.5. |
| 5 | "Finishing together gives one: perfectly fair." | The rows are replaced by two equal ones; F = 1 (gold glow). |
| 6 | "Over thirty trials, with jobs from one to a thousand time slices long, the pattern is clear." | The rows fade; the Axes draw: y "fairness" 0 to 1.0, x "job length" (log: 1, 10, 100, 1000). A dotted line at 1.0. |
| 7 | "Short jobs: poor fairness. Only long jobs let the lottery converge." | The curve (adapted from Figure 9.2) draws from (1, 0.5) up through (10, 0.8), (100, 0.96) to (1000, 1.0). A marker at the left labeled "short jobs: unfair", another at the right labeled "long jobs: fair". |
| 8 | "So for short jobs it's kind of unfair. And how many tickets does each job get, anyway?" | Student (sad), then (curious). A card with a big "?" and "how many tickets?" appears at (3.8, 2.4). |
| 9 | "The book is honest about that one. It's the **ticket-assignment problem**, and it's still open." | Professor (explaining). Term highlight "ticket-assignment problem". The card stays; an "open" stamp (`DIM`, rotated) hits it. |

**Characters:** Student (sad → curious), Professor (explaining).
**Ends with:** fairness plot, "?" card with the "open" stamp. Transition: fade all but the section badge and crux strip.
**Implementation notes:** adapted from **Figure 9.2** (use `Axes` with an `x_axis` log-spaced tick positions; plot the curve as a `VMobject` through a handful of digitized points). Keep it as a simple stylized curve.

### S11 — Stride scheduling: strides and passes   (beats: B08, first half) · ~0:50
**Purpose:** a deterministic alternative: stride (inverse of tickets) and pass.
**Starts with:** section badge and crux strip.
**Layout:** three lanes (rows) at y = 1.4, 0.4, −0.6 labeled by Process creatures (scale 0.55) A, B, C at x = −6.0. A **pass number line** from x = −5.2 to 5.2 (0 to 260) above them at y = 2.2. A table on the right is added in S12.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Why use randomness at all, then? Can't we get the proportions exactly right?" | Student (frustrated). The raffle drum wobbles at the corner and drops a bad draw (a "bad luck" cloud, 4/20). |
| 2 | "Waldspurger asked the same question. His answer is **stride scheduling**: a deterministic fair-share scheduler." | The drum rolls out of frame; term highlight "stride scheduling". The three lanes draw. |
| 3 | "Each job gets a **stride**, which is inversely proportional to its tickets." | Term highlight "stride". A caption: "stride ∝ 1 / tickets" (`MathTex`). |
| 4 | "Take our three jobs: a hundred, fifty and two hundred and fifty tickets." | Each lane's process gets a ticket stack: A "100", B "50", C "250". |
| 5 | "Divide ten thousand by each. A has a stride of one hundred. B, two hundred. C, forty." | `MathTex` lines: 10000 / 100 = 100, 10000 / 50 = 200, 10000 / 250 = 40, written next to each lane; each result flies into a **stride bar** (a horizontal bar whose length is the stride on the number line scale): A's bar 100, B's 200, C's 40. C (most tickets) gets the shortest bar. |
| 6 | "Each job also keeps a **pass** value, starting at zero." | Term highlight "pass". A small marker (flag, process-colored) planted at 0 on each lane; label "pass = 0". |
| 7 | "The rule is simple: run the job with the lowest pass. Then add its stride to its pass." | The **Spotlight** appears above the lanes. Rule card at the bottom (font 26): "1. run the lowest pass  2. pass += stride". The spotlight sweeps across the lanes. |

**Characters:** Student (frustrated), corner mode.
**Ends with:** three lanes with flags at 0, stride bars, rule card, Spotlight idle.

### S12 — Stride: a trace   (beats: B08, second half) · ~1:10
**Purpose:** replay Figure 9.3: the runners step in turn, and the final tally is exactly 5 : 2 : 1.
**Starts with:** S11 end state; the pass line scale 0–200 fits the screen. The table (see below) appears at the right.
**Layout:** lanes at left (x −5..1.6). A **Pass table** at the right (x 2.6..6.4, y 2.4..−2.2), header "Pass(A) Pass(B) Pass(C) | Who runs?", rows added each step. The **Timeline** at the bottom (y = −2.4, x −5..2) records who ran. The target pie is replaced by a small "5 : 2 : 1" tag at (6.0, 3.0) at the end.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Everyone starts at zero, so pick A." | Table row 1: (0, 0, 0) → A. The Spotlight lands on A (arbitrary tie-break, tag "tie → pick A"). A hops onto a small CPU chip at the lane's end (−1.6 pos): Timeline tick 1 coral. |
| 2 | "After its slice, A's pass is a hundred." | A's flag slides 0 → 100 along the lane (distance = A's stride bar), pass shows 100. Table row 2: (100, 0, 0). |
| 3 | "B and C are lower, so B runs next." | Spotlight sweeps from A to B (B and C tied at 0, pick B). B runs: tick 2 mint. B's flag slides to 200. Table row 3: (100, 200, 0) → B. |
| 4 | "B's pass becomes two hundred. Now C is lowest, runs, and goes to forty." | Spotlight to C (lowest). Tick 3 gold; C's flag 0 → 40; row 4 (100, 200, 40). |
| 5 | "C is still lowest. It runs again: eighty. Again: a hundred and twenty." | Two more C steps (40 → 80 → 120) with ticks 4–5 gold; rows 5, 6. The flags of A and B stay put. |
| 6 | "Now A, at a hundred, runs." | Spotlight jumps to A (100 < 120): A's flag 100 → 200; tick 6 coral. Row 7: (200, 200, 120). |
| 7 | "And so on." | Fast-forward (0.4 s each): C 120 → 160 → 200; ticks 7–8 gold. Rows 8–9. Now all three flags are at 200: a vertical line at 200 flashes "cycle complete". |
| 8 | "Follow it to the end of the cycle, when all three passes meet at two hundred. C ran five times, A twice, B once." | A tally bar under the Timeline: C ×5 (gold), A ×2 (coral), B ×1 (mint). The Timeline (8 ticks: A B C C C A C C) brackets with the counts. |
| 9 | "Five, two, one: exactly the ratio of their tickets, two hundred and fifty, a hundred, and fifty." | Tag "250 : 100 : 50 = 5 : 2 : 1" (`MathTex`) next to the tally; green check. |
| 10 | "Exactly. Not 'probably'. Every time." | Student (surprised). |
| 11 | "Every time. Small stride, large share: the busy ones barely advance on the number line." | Professor (proud). C's tiny step bar `Indicate`s. |

**Characters:** Student (surprised), Professor (proud).
**Ends with:** completed pass table, the 8-tick Timeline, tally "C ×5 · A ×2 · B ×1". Transition: lanes/table fade; the Timeline and tally fade. Back to badge + strip.
**Implementation notes:** source: Figure 9.3 (use its rows verbatim: 0/0/0 A; 100/0/0 B; 100/200/0 C; 100/200/40 C; 100/200/80 C; 100/200/120 A; 200/200/120 C; 200/200/160 C; 200/200/200 ...). The Spotlight is the one from 04 (S08), moved with `move_beam_to`. The "5:2:1" total includes the last step to 200: C ×5, A ×2, B ×1.

### S13 — So why keep the lottery?   (beats: B09) · ~0:40
**Purpose:** stride needs per-process state and a rule for newcomers; lottery needs only a global total. That is its advantage.
**Starts with:** section badge and crux strip.
**Layout:** split screen: left panel "Stride" (x −6.4..−0.4), right panel "Lottery" (x 0.4..6.4). Each has the three process creatures A, B, C (scale 0.5) and a new job D (sky) waiting at the top edge.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Then stride beats lottery, right? Why did we bother with lottery?" | Student (curious). The split panels draw. |
| 2 | "One good reason. Lottery has *no global state*." | Professor (explaining). Left: A, B, C carry pass flags (200, 200, 200). Right: A, B, C carry only ticket stacks. A tag "no per-process state" in the right panel. |
| 3 | "In the middle of our stride example, a new job shows up. What should its pass value be?" | D drops into the left panel; a "pass = ?" bubble above it. |
| 4 | "Zero? Then it's far below everyone and monopolizes the CPU until it catches up." | D's flag planted at 0 (vs. 200 for the others); D's lane runs alone, Timeline fills sky ×N; a red "monopoly" banner. |
| 5 | "Anything else? You have to decide what." | The flag bounces among several values with "?" marks. |
| 6 | "With lottery, a new job just arrives with its tickets. Add them to one global total, and go." | Right: D slides in with its ticket stack; the "total" counter (at the top of the panel) ticks 400 → 450; D takes its turn and the Timeline shows normal sharing. |
| 7 | "Lottery is sloppy but flexible. Stride is exact but fussy." | Student (excited). Left panel label "exact, fussy"; right "flexible, approximate" (font 24, `DIM`). |
| 8 | "That's the trade." | Professor (happy). Hold 1 s. |

**Characters:** Student (curious → excited), Professor (explaining → happy).
**Ends with:** the two panels with labels. Transition: fade all but the badge and crux strip.

### S14 — Enter Linux CFS   (beats: B10) · ~1:00
**Purpose:** introduce CFS's two goals (fair, efficient) and its counter, vruntime.
**Starts with:** section badge and crux strip.
**Layout:** center: CPU at (0, 1.0). Four processes A–D in a row below (y = −0.6, x −3..3), each with a small vertical **vruntime meter** (see New assets) next to it, height 0.9. A Linux penguin silhouette is not used (no brand assets); a simple "Linux" tag (monospace) at top-left of the stage.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Now for the real world. For years, Linux used a scheduler with a similar goal, reached in a very different way: the **Completely Fair Scheduler**, or **CFS**." | A "Linux" tag fades in; term highlight "Completely Fair Scheduler (CFS)". |
| 2 | "Its other goal is efficiency. Scheduling steals CPU time from the programs it schedules." | The CPU appears with a small coin-slot "tax" icon siphoning a thin yellow sliver off its top. |
| 3 | "In a study of Google's data centers, even after heavy optimization, about five percent of all CPU time went to scheduling." | A pie / bar chip shows 5% of the CPU's area in `KERNEL_COLOR`: "≈ 5%" with a "datacenter study" tag. |
| 4 | "So CFS must decide fast." | The `stopwatch` icon ticks fast near the CPU. |
| 5 | "Its counter is **virtual runtime**, or **vruntime**." | Term highlight "vruntime". The four processes and their meters fade in; meters at 0. |
| 6 | "A running process accumulates vruntime, at the same rate as real time." | A hops onto the CPU; A's meter fills steadily (a small tick-up counter beside it: "vruntime: 0 → 12 ms"). A real-time clock icon beside shows equal ticking. |
| 7 | "When it's time to choose, CFS picks the process with the *lowest* vruntime." | A stops; A's meter stays high, B, C, D are at 0. The Spotlight lands on B (a tie among B, C, D; pick B); B hops onto the CPU. |
| 8 | "Like stride's pass value?" | Student (curious). A faint ghost of stride's lanes flashes behind the meters (callback), then fades. |
| 9 | "Same flavor: whoever has had the least goes next." | Professor (happy). |

**Characters:** Student (curious), Professor (happy).
**Ends with:** CPU with B running, meters (A high, B filling, C and D at 0), the Spotlight.
**Implementation notes:** the vruntime meter is a new prop (see New assets). Don't draw a penguin; the "Linux" tag is text only.

### S15 — How long is a turn?: sched_latency   (beats: B11, first half) · ~0:40
**Purpose:** the time slice tension, then sched_latency / n; figure 9.4.
**Starts with:** S14 end state, collapsed to the left; a **Timeline** appears at the bottom.
**Layout:** Timeline along y = −1.2, x −5.5..5.5, 0..250 ms, one row per process (A–D) or a single CPU row with colored blocks (follow Figure 9.4: single row). The tension "dial" at the top (0, 2.6): a seesaw with "too often" (left: context-switch cost) and "too rarely" (right: unfair short-run).

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "But when does CFS stop the running process? Every millisecond?" | Student (confused). The CPU emits a rapid flicker with a "switch?" tag. |
| 2 | "That's the tension. Switch often, and you're fair even over tiny windows, but you pay for every context switch." | The seesaw draws; left side "switch often" lowers: "fair ✓ / cost ✗" with many tiny block ticks on the Timeline. |
| 3 | "Switch rarely, and you're efficient, but unfair in the short run." | The seesaw tips right: few long blocks, "efficient ✓ / unfair ✗". |
| 4 | "CFS uses two knobs. First, **sched_latency**, typically forty-eight milliseconds, divided by the number of runnable processes." | Term highlight "sched_latency". `MathTex`: 48 ms ÷ n. A bracket labeled "48 ms" spans the Timeline's first 48 ms. |
| 5 | "Four processes: twelve milliseconds each." | `MathTex` 48 ÷ 4 = 12 ms; the bracket divides into four blocks A B C D (coral, mint, gold, sky) labeled 12. |
| 6 | "CFS runs one for twelve, then switches to a process with lower vruntime." | The meters beneath the Timeline: after A's 12 ms block, A's meter is tall and B's is lowest; the Spotlight moves to B. The Timeline fills A, B, C, D at 0–48 ms, then repeats A B C D 48–96 ms. |
| 7 | "Our four take turns. Then two finish, and the other two get twenty-four each." | C and D get a check mark and leave; the Timeline continues with A (24), B (24), A, B, ... through 250 ms. Matches **Figure 9.4**: A B C D A B C D then A B A B A B (blocks of 24 ms). |

**Characters:** Student (confused), corner mode.
**Ends with:** completed Figure 9.4 Timeline to 250 ms; the "sched_latency" term strip.
**Implementation notes:** Figure 9.4 shows A B C D ×2 then A B ×3 pairs; use 12 ms blocks for the first 96 ms and 24 ms blocks afterwards. The seesaw is a simple `Line` + `Triangle` + two small tags.

### S16 — Too many processes: min_granularity   (beats: B11, second half) · ~0:30
**Purpose:** a floor on the time slice so context switches don't dominate.
**Starts with:** S15 end state.
**Layout:** the Timeline is cleared and re-drawn with ten rows' worth of small colored blocks (ten process dots at the left, `PROCESS_COLORS` cycling). Equations at the top (0, 2.4).

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Ten processes? Forty-eight over ten is four point eight milliseconds: too small." | Ten small process dots appear (colors cycling), `MathTex` 48 ÷ 10 = 4.8 ms. A Timeline of ten tiny blocks (4.8 ms each), with a tiny red "switch cost" flash at every boundary. |
| 2 | "So the second knob, **min_granularity**, typically six milliseconds, says never go below this." | Term highlight "min_granularity". A horizontal floor line at "6 ms" appears; the 4.8 blocks are crossed out. |
| 3 | "Ten processes get six each." | The Timeline redraws: ten blocks of 6 ms (60 ms total). `MathTex` "max(4.8, 6) = 6 ms". |
| 4 | "Not perfectly fair over forty-eight, but close, and cheap." | A bracket marks 48 ms; the tenth block hangs outside it ("round of 60 ms"). A small "cheap ✓" `tick_mark()`. |

**Characters:** corner mode, passive.
**Ends with:** the Timeline with ten 6 ms blocks, floor line, "min_granularity" in the term strip. Transition: fade all but badge and strip.

### S17 — Nice values and weights   (beats: B12, first half) · ~0:50
**Purpose:** how to prefer a process in CFS: nice → weight → bigger time slice. The 36 / 12 example.
**Starts with:** section badge and crux strip.
**Layout:** a **nice dial** at left (−4.4, 1.2): a horizontal slider from −20 to +19 with the default 0 marked. The weight table peek at right (3.2, 1.4): a 5-row excerpt of `prio_to_weight` in `MONO_FONT` (font 20) showing rows −5 (3121) and 0 (1024) highlighted. Bars at the bottom: a 48 ms bar at y = −1.8.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Can I tell CFS that one program matters more? With tickets, I can." | Student (curious). A ticket stack pops over A, then crosses out with a "no tickets in CFS" tag. |
| 2 | "CFS doesn't use tickets. It uses an old UNIX mechanism called **nice**: a value from minus twenty to plus nineteen, default zero." | Term highlight "nice". The slider draws; the knob rests at 0. |
| 3 | "Positive means nicer, so you get less. Negative means higher priority." | The knob slides right (a "polite" little bow on a process) and left ("pushy" on a process); small arrows "less CPU" ← → "more CPU". |
| 4 | "CFS maps each nice value to a **weight** with a lookup table." | Term highlight "weight". The table excerpt `FadeIn`s; an arrow from the knob's position to the matching row. |
| 5 | "Nice zero is one thousand twenty-four. Nice minus five is three thousand one hundred twenty-one." | Rows 0 → 1024 and −5 → 3121 highlight in turn. |
| 6 | "A process's time slice is its weight over the sum of all weights, times sched_latency." | `MathTex` (Equation 9.1): time_slice_k = weight_k / Σ weight_i · sched_latency. Writes left to right. |
| 7 | "Try it. A has nice minus five, B has nice zero." | A (coral) with a "nice −5" tag, B (mint) with "nice 0". |
| 8 | "A gets about three quarters of forty-eight: thirty-six milliseconds. B gets twelve." | Substitute: 3121 / (3121 + 1024) ≈ ¾, so ≈ 36 ms; B ≈ ¼, ≈ 12 ms. The 48 ms bar splits 36 (coral) | 12 (mint). |

**Characters:** Student (curious), corner mode.
**Ends with:** nice slider, weight table excerpt, equation, 36/12 bar.

### S18 — Weighted vruntime   (beats: B12, second half) · ~0:30
**Purpose:** vruntime is scaled by weight, so a heavier process's meter fills slower and it keeps winning.
**Starts with:** S17 end state; the table and slider shrink to the corner. The bar splits become meters.
**Layout:** two big vruntime meters (A at x = −2.4, B at x = 2.4, height 2.4) and the CPU at the center (0, 1.6). Equation at the top (0, 2.8). Timeline at y = −2.2.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "vruntime is scaled too: it grows by real run time times one thousand twenty-four, over the weight." | `MathTex` (Equation 9.2): vruntime_i += (weight_0 / weight_i) · runtime_i. The 1024 term highlights ("weight₀ = 1024"). |
| 2 | "A, being heavier, accumulates vruntime at a third of B's rate, so it keeps winning and runs longer." | A runs on the CPU for 12 ms of real time; A's meter rises by ⅓ of what B's would (a ghost bar shows "if A were B"). B runs 12 ms; B's meter rises 3× as much. The Spotlight keeps returning to A. The Timeline shows A running 36, B 12 (repeating). |
| 3 | "Heavier means a longer slice *and* a slower meter!" | Student (excited). |
| 4 | "And the table only cares about the *difference* in nice values. Five and ten behave exactly like minus five and zero." | Professor (proud). The slider shows a second pair of knobs (5 and 10); the ratio "3 : 1" appears over both pairs; check mark. |

**Characters:** Student (excited), Professor (proud).
**Ends with:** two meters, the Timeline with the 36/12 pattern, the equations. Transition: fade all but badge and strip.
**Implementation notes:** the 5/10 pair is a table row demo: weights at 5 → 335 and 10 → 110: 335/110 ≈ 3.05, close to 3121/1024 ≈ 3.05. Show just the ratio, not the numbers, to avoid clutter.

### S19 — The red-black tree   (beats: B13) · ~1:10
**Purpose:** why a sorted list is too slow, and how a balanced tree helps. Only runnable processes live in it.
**Starts with:** section badge and crux strip.
**Layout:** left half: a sorted **list** of ten vruntime nodes (a horizontal row of 10 small circles at y = 1.5, x −6.0..−0.8, labels 1, 5, 9, 10, 14, 17, 18, 21, 22, 24). Right half: the **red-black tree** (see New assets, adapt **Figure 9.5**) at (3.2, 0.8). Counters at the bottom of each half: "steps".

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "One more efficiency problem. 'Pick the lowest vruntime' sounds easy, but servers run thousands of processes, and the choice happens every few milliseconds." | A counter "processes: 1000s" ticks up beside the CPU icon; a clock icon ticks every ms (flashing). |
| 2 | "Keep a sorted list. The lowest is at the front." | Student (curious). The list draws (ten nodes, sorted); the Spotlight sits on node "1" at the front. |
| 3 | "Taking the first is quick." | Node 1 is popped (`FadeOut` / slide) to the CPU. Counter: "1 step". |
| 4 | "But after it runs, its vruntime grows, and it must be re-inserted in order." | The node returns with a new value (say 20); a pointer scans along the list from the left, node by node, until it finds the spot (between 18 and 21). Counter ticks "8 steps". |
| 5 | "With vruntimes one, five, nine, ten, fourteen, eighteen, seventeen, twenty-one, twenty-two and twenty-four, that means scanning the list: linear time." | The values flash in the order spoken (the list shows them sorted: 1, 5, 9, 10, 14, 17, 18, 21, 22, 24; the book lists 18 before 17, so sync on count, not order). The label "O(n)" appears. |
| 6 | "Terrible at a thousand processes." | The list stretches off-screen to the right in a compressed ticker "1000 nodes → 1000 steps" and a red flag. |
| 7 | "CFS uses a **red-black tree**, ordered by vruntime." | Term highlight "red-black tree". The right half: the tree draws in (Figure 9.5: root 14, children 9 and 18, then 1, 10, 17, 22, then 5, 21, 24; reds and blacks as in the book). The leftmost node (1) is highlighted: "next to run". |
| 8 | "It's *balanced*: it does a little extra work on each insert to stay shallow, so find, insert and delete are all logarithmic." | A re-insertion of the same new value (20) in the tree: a pointer hops down 3 levels (14 → 18 → 22 → insert-left of 22, hinting at 21; keep it within 3 hops); counter "3 steps"; "O(log n)". A tiny recolor/rotation flash on a node. |
| 9 | "And only runnable processes live in the tree. A sleeper is removed." | A process with a clock/blocked state (D) lifts out of the tree and stands to the side with a "sleeping" tag. |
| 10 | "Knowing which data structure fits is a hallmark of good engineering. A list was fine once. At this scale, it isn't." | Professor (explaining). A **Tip** card header at the bottom: "Use efficient data structures when appropriate". |

**Characters:** Student (curious), Professor (explaining).
**Ends with:** the red-black tree with the lowest node highlighted; a sleeper to its side; the Tip card.
**Implementation notes:** the tree is a new prop (see New assets); use the book's exact shape (Figure 9.5). The new vruntime after running is 20 (invented, flagged as "e.g."). The narration lists the values as in the book (…18, 17…); on screen show the sorted set.

### S20 — The sleeper problem   (beats: B14) · ~0:40
**Purpose:** a process that sleeps for a long time would monopolize the CPU on waking; CFS resets its vruntime.
**Starts with:** section badge and crux strip.
**Layout:** two vruntime meters: A at (−2.4, 0.0) and B at (2.4, 0.0), each 2.2 tall, and a clock (`ClockIcon`) in the middle. CPU at the top center (0, 2.4). A time ruler "0 s → 10 s" at the bottom.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "One last trap. A runs all the time." | A on the CPU; A's meter rises steadily. |
| 2 | "B sleeps for ten seconds." | B gets a clock (blocked); B's meter stays flat; the time ruler fills to "10 s" as A's meter climbs. |
| 3 | "When B wakes, its vruntime is ten seconds behind A's." | B wakes (→ ready); a double-headed gap bracket "10 s" opens between the meters; the gap glows red. |
| 4 | "So B hogs the CPU for ten seconds while A starves!" | Student (surprised). Ghost timeline: B runs ten seconds in a row (a long mint bar) while A is blank; a red "starved" tag on A. Rewind. |
| 5 | "It would. So when a job wakes, CFS sets its vruntime to the minimum in the tree." | B's meter snaps up to the minimum (A's level, or the tree's lowest) with a bounce; the gap closes. A small tree icon with "min" appears at the corner. |
| 6 | "No monopoly. The price: jobs that sleep for short periods, again and again, never get their fair share." | The Timeline shows A and B alternating normally. A tag next to B: "frequent short sleeps → lose their share" with a small zZz. |

**Characters:** Student (surprised).
**Ends with:** the two meters equalized, the tag. Transition: fade all but badge and strip.

### S21 — The big picture   (beats: B15) · ~0:55
**Purpose:** compare the three approaches, name the limits, and show where proportional share is actually used.
**Starts with:** section badge and crux strip.
**Layout:** three columns at x = −4.4, 0, 4.4, y = 1.2: each with a small icon (drum, runners, tree) and one-word label ("random", "deterministic", "efficient"). Under them (y = −0.6) the 75/25 pie from S01 at each column, filled in 75/25 by Timeline strips. Later, a cloud icon with two VMs.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Let's step back. Lottery shares the CPU by random draw. Stride does it deterministically. CFS does it with vruntime, weights and a tree, built for efficiency at scale." | Three columns appear one by one, matching the three sentences: drum + "tickets"; runners + "pass"; meters + tree + "vruntime". Each column's tiny Timeline fills with ~75/25. |
| 2 | "So these are the best schedulers? Why did we bother with MLFQ?" | Student (confused). A small MLFQ chip (from S01) appears and peeks in at the right. |
| 3 | "No scheduler is a panacea. These don't mesh well with I/O: a job that sleeps often misses its share." | Professor (worried). Under the columns, a process with a clock and a half-empty share bar. |
| 4 | "And they leave a hard question open: how many tickets, or which nice value, should your text editor get?" | The "?" card from S10 returns, with a text-editor icon and "nice ?" "tickets ?". |
| 5 | "MLFQ-style schedulers handle that automatically." | The MLFQ chip lights up with a check; the card is crossed out beside it. |
| 6 | "Still, in many domains that isn't the main worry." | The question card slides away; the pie icon returns. |
| 7 | "In a cloud data center, you might give a quarter of the CPU to a Windows VM and the rest to your Linux install." | A cloud icon (see New assets) with a server rack; two VM windows, labeled "Windows" (mint, 25%) and "Linux" (coral, 75%), tied to the 75/25 pie. |
| 8 | "Proportional share is simple and effective there." | The pie's sectors pulse; a green check. |
| 9 | "And Linux keeps changing: since version 6.6, its default is a scheduler called EEVDF. Just when you thought you were done." | A small tag "Linux 6.6 → EEVDF" swaps in over the CFS column (a quick `Transform` of the tree icon into a new box with "EEVDF"); Student (surprised); Professor (happy). |

**Characters:** Student (confused → surprised), Professor (worried → happy).
**Ends with:** the three columns, the cloud / VM image, and the EEVDF tag. Transition: fade all but the badge.

### S22 — Recap   (beats: B16) · ~0:35
**Purpose:** five takeaways.
**Starts with:** section badge only.
**Layout:** numbered list at the left (−5.6..1), font 28, one line each; an icon for each line at x = 4 (as in 04 S21).

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "So, today:" | Header "Recap" in `VIRT`. |
| 2 | "A **proportional-share** scheduler promises each job a *share*, instead of minimizing a time." | Line 1; icon: the 75/25 pie. |
| 3 | "**Lottery scheduling** uses **tickets** and a random draw. Simple, cheap, and fair in the long run." | Line 2; icon: the drum + a ticket stub. |
| 4 | "**Stride scheduling** uses strides and pass values to get the shares exactly right." | Line 3; icon: runners on a lane (mini). |
| 5 | "**CFS** runs the process with the lowest **vruntime**, with a time slice from sched_latency, bounded by min_granularity, and scaled by nice weights." | Line 4; icon: a vruntime meter. |
| 6 | "CFS keeps runnable processes in a **red-black tree**, so finding the next one is fast even with thousands." | Line 5; icon: a mini red-black tree. Hold 1.5 s. |

**Ends with:** the full recap list. Section badge fades out.

### S23 — Teaser: more than one CPU   (beats: B17) · ~0:30
**Purpose:** hook for 10 (Multi-CPU Scheduling).
**Starts with:** S22 end state.
**Layout:** characters in dialogue mode. A single CPU at (0, 1.4) that will split.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Everything so far has been about one CPU. My laptop has eight. What changes?" | The recap list fades. Student and Professor move to dialogue positions. Student (curious). The CPU chip appears at (0, 1.4) with a Queue under it (A–D). |
| 2 | "Quite a lot, I'm afraid. Caches, locks, and one queue that eight CPUs all want to touch at once…" | Professor (worried). The chip splits into four chips in a row (hop apart with a stretch); all of them reach (thin arrows) toward the one Queue; tiny sparks collide at the Queue. |
| 3 | "Uh oh." | Student (surprised). The Queue shakes; the cables tangle. |
| 4 | (end) | Cut to black (`FadeOut` all, 0.5 s). Then "Next: 10 · Multi-CPU Scheduling" in `TEXT` with a `VIRT` dot. Hold 2 s. |

**Characters:** Student (curious → surprised), Professor (worried).
**Ends with:** black end card.
**Implementation notes:** this episode comes right before 10, so the end card says "10"; if 10 is ever reordered, update here.

## New assets needed
- **`RaffleDrum(size)`** (core): a rotating wire cage (circle with a few slanted lines) on a stand with a small chute. `.spin()` (continuous rotate), `.draw(number, color=None)` returns an animation that pops a numbered ball out of the chute and hands it back as a Mobject (to `hop_to`).
- **`Ticket(color, label=None)` and `TicketStack(count, color, show_count=True)`**: notched stubs; the stack fans out 3–5 stubs with a count label. `.set_count(n)` animation; `.hop_to(point)`.
- **`NumberStrip(total, segments, labels)`**: horizontal ruler (0..total) with colored segments per owner; `.marker_at(n)` (pointer triangle), `.reorder(order)` to swap segments (S09).
- **`JobList(nodes, label)`**: a linked list of gray discs ("Job:A Tix:100") with arrows and "head"/"NULL" labels; `.pointer(i)` for `current`; `.reorder(order)`. Used in S08 and S09.
- **`PassLane(label, color, stride, pass_value)`**: one lane of the pass line, with a flag marker (`.step()` slides the flag by the stride) and a stride bar. Plus a **`PassTable(rows)`** for Figure 9.3 (it can also be a `MobjectTable`/`Table`).
- **`VruntimeMeter(color, height)`**: a vertical bar (fuel gauge) with a process-colored fill; `.add_runtime(ms, weight=1024)` animates the fill; `.set_level(v)`; `.gap_to(other)` returns a bracket.
- **`RBTree(spec)`**: the red-black tree of Figure 9.5 (nodes as circles with a black or red outline, small null stubs), `.highlight_min()`, `.insert_path(value)` for the pointer hop, `.remove(node)`.
- **`FairnessPlot`**: a thin wrapper over `Axes` with a log-x axis and the Figure 9.2 curve (the data points digitized by eye: (1, 0.5), (3, 0.7), (10, 0.8), (30, 0.9), (100, 0.96), (300, 0.98), (1000, 1.0)).
- **`TargetPie(shares)`**: the 75/25 pie target (`Sector`s), `.set_shares`, `.pulse()`.
- **Icons:** cloud + VM window (S21), coin flip / die (S05), a seesaw (S15), a handshake or "friends" glyph (S07), a paper/citation chip (S03), a "bad luck" cloud (S11). All are simple primitives (`ov_icons`-style).
- **Process extras:** none; a "nice" tag is just a small `Text` badge.
- **Existing assets reused:** `Timeline`, `Queue`, `CPU`, `Spotlight`, `CruxCard`, `AsideCard` / `TipCard`, `TermHighlight`, `SectionBadge`, `Code`, `PCBCard`, `server_rack`, `stopwatch`, `ClockIcon`, `tick_mark` / `x_mark`, `hop_to`, `MathTex`.

## Open questions
- **Length (~14:00) and scene count (23):** it's the longest regular episode so far. S07 (transfer and inflation) and S20 (the sleeper problem) are the easiest to cut or shorten if you want ~12 min.
- **Spotlight across all three mechanisms:** I reuse the Spotlight (policy icon from 04) for lottery's draw, stride's "lowest pass" and CFS's "lowest vruntime" to link the three. Keep, or use a different pointer for the lottery (the drum already picks)?
- **Pass-line tie-break (S12):** the book says "assume we pick A (arbitrarily)". I show a "tie → pick A" tag and then pick B in a tie at row 3 (it's also arbitrary). OK?
- **User cards in S06:** the book's users are "A" and "B", which clash with Process A and B. I draw the users as neutral cards and only color the job chips. Is that clear enough, or should the users be renamed (e.g. "Ann", "Ben") with a note on the change?
- **Hypervisor memory / "tickets for memory" aside (S07 step 7):** I add a 1.5 s visual hint (the book's Tip), with no narration. Drop it if it feels like clutter?
- **Fairness curve data (S10):** the curve is digitized by eye from Figure 9.2. Fine for a stylized plot?
- **Teaser (S23):** the book's chapter doesn't mention multi-CPU, so the hook is my bridge to episode 10. The end card hardcodes "10 · Multi-CPU Scheduling".
- **No Linux logo:** I avoid the penguin/branding and use a text tag only.
