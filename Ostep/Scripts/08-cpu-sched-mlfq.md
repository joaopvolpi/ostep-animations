# 08 — Scheduling: The Multi-Level Feedback Queue
> Section: Virtualization · Source: Ostep/Chapters/08-cpu-sched-mlfq.pdf · Est. duration: ~14:00 (1,900 spoken words ≈ 12:40 of narration, plus pauses)

## Logline
Last time we learned two good ideas for scheduling, and learned that each one needs something the OS doesn't have: knowledge of how long a job will run. This episode builds the **Multi-Level Feedback Queue**, which gets around that by *watching* jobs instead of asking them. We build it one rule at a time, and every new rule fixes a flaw in the one before.

## Learning goals
- After watching, the viewer can explain why a scheduler that doesn't know job lengths can still favor short jobs, by using **history**.
- Describe MLFQ's **queues and priority levels**, and state Rules 1 and 2 (priority, then round robin within a level).
- Trace a job through the queues using Rules 3 and 4 (enter at the top, **allotment**, demotion), including a long job, a short job arriving, and a job that does I/O.
- Explain **starvation** and **gaming the scheduler**, and how the **priority boost** (Rule 5) and **better accounting** (the final Rule 4) fix them.
- Name the tuning knobs of an MLFQ (number of queues, time slice per queue, allotment, boost period) and why they are hard to set.

## Concepts covered
| Term | Definition (book's wording or faithful paraphrase) | Beat |
|---|---|---|
| Multi-Level Feedback Queue (MLFQ) | A scheduler with multiple queues, each at a different priority level, that uses feedback (the observed behavior of jobs) to set their priorities. Described by Corbato et al. in 1962 (CTSS). | B02, B03 |
| Queue / priority level | MLFQ has a number of distinct queues, each assigned a different priority level. A ready job is on exactly one queue; the job on a higher queue is chosen to run. | B03 |
| Rule 1 | If Priority(A) > Priority(B), A runs (B doesn't). | B04 |
| Rule 2 | If Priority(A) = Priority(B), A and B run in round robin (using the time slice of the given queue). | B04 |
| Learning from history | Use a job's observed behavior (past) to predict its future behavior. | B03, B05 |
| Interactive vs. CPU-bound job | A job that repeatedly gives up the CPU to wait for input vs. one that uses the CPU intensively for long periods. | B05 |
| Allotment | The amount of time a job can spend at a given priority level before the scheduler reduces its priority. (Starting out: allotment = one time slice.) | B06 |
| Rule 3 | When a job enters the system, it is placed at the highest priority (the topmost queue). | B06 |
| Rule 4a / 4b (first attempt) | 4a: if a job uses up its allotment while running, its priority is reduced (it moves down one queue). 4b: if a job gives up the CPU (e.g. for I/O) before the allotment is up, it stays at the same priority level (its allotment is reset). | B06 |
| MLFQ approximates SJF | It doesn't know whether a job is short, so it first *assumes* it might be; if it is short, it runs quickly and completes, if not, it slowly moves down and proves itself a long, batch-like job. | B08 |
| Starvation | Too many interactive jobs consume all CPU time, so long-running jobs never receive any. | B10 |
| Gaming the scheduler | Doing something sneaky to trick the scheduler into giving you more than your fair share (e.g. issuing an I/O just before the allotment ends). | B10 |
| Priority boost (Rule 5) | After some time period S, move all the jobs in the system to the topmost queue. | B11 |
| Voodoo constants | Values that seem to require black magic to set correctly (John Ousterhout's term). `S` is one. | B12 |
| Ousterhout's Law | Avoid voodoo constants if at all possible. | B12 |
| Accounting / the final Rule 4 | Track total CPU time used at each level; once the allotment is used up (regardless of how many times the job gave up the CPU), the job is demoted. | B13 |
| Parameterizing the scheduler | Number of queues, time slice per queue, allotment, boost frequency: no easy answers, only experience. | B14 |
| Advice / hints | Interfaces (e.g. `nice`) that let users suggest priorities; the OS may or may not follow them. | B15 |
| Decay-usage scheduling | Priority computed by a formula from recent CPU usage, which decays over time (FreeBSD). | B15 |

## Script

### B01 — Two jobs, no labels  `cold open` (~0:50)
**Narrator (V.O.):** Two jobs just arrived at the scheduler. One of them is tiny: a keystroke, an echo on the screen, done in a blink. The other will grind through numbers for an hour. From the outside, they look exactly the same.

**Student** (curious): Easy. Shortest job first, like last time.

**Professor** (thinking): If we knew which one was which. SJF and STCF need each job's length *in advance*, and the OS almost never has it.

**Student** (frustrated): Fine. Round robin, then.

**Professor** (explaining): Round robin keeps **response time** low: the keyboard feels snappy. But it drags every job out, so **turnaround time** is awful.

**Student** (confused): So we're stuck.

**Professor** (happy): Not stuck. We can't see the future. But we *can* watch the past.

*Visual idea:* Two mystery boxes ("?") slide into a scheduler spotlight: one tiny, one huge, both wrapped identically; labels "keystroke?" and "one hour?" fade in then get replaced by "?". Small SJF and RR icons from 07 get a red X and a half-check. The Student and Professor in dialogue mode.

### B02 — The Crux  `crux` (~0:30)
> **THE CRUX: HOW TO SCHEDULE WITHOUT PERFECT KNOWLEDGE?**
> How can we design a scheduler that both minimizes response time for interactive jobs while also minimizing turnaround time, without *a priori* knowledge of job length?

**Narrator (V.O.):** Today's answer is one of the most famous ideas in scheduling: the **Multi-Level Feedback Queue**, or **MLFQ**. It was first described in 1962, in the Compatible Time-Sharing System, and it helped earn its creator, Fernando Corbato, the Turing Award. We'll build it in five rules. Each one is the answer to a problem with the one before.

*Visual idea:* Crux card in the Virtualization orange; section badge "08 · MLFQ" appears top-left. The five rule slots appear empty below, like a blank rulebook.

### B03 — Queues and priority levels  `build-up` (~0:50)
**Narrator (V.O.):** MLFQ doesn't have one ready queue. It has several, each at a different **priority level**. A job that's ready to run sits on exactly one of them, and the scheduler picks from the highest queue that has anything in it.

**Narrator (V.O.):** Picture a ladder. In the book's first figure there are eight queues. Jobs A and B sit at the top, C in the middle, D at the bottom.

**Narrator (V.O.):** And the big idea: the scheduler will *learn* from history. What a job did a moment ago tells us what it will probably do next.

**Professor** (explaining): Branch predictors and caches do this too. But careful: when the past is a bad guide, such a system can decide worse than one with no knowledge at all.

*Visual idea:* The ready Queue from 04 splits into a ladder of lanes (Q8 at the top "high priority", Q1 at the bottom "low priority"), adapting Figure 8.1. A, B, C, D hop into their lanes. A Tip card slides in: "TIP: Learn from history."

### B04 — Rules 1 and 2  `build-up` (~0:45)
**Narrator (V.O.):** Rule one: if the priority of A is greater than the priority of B, A runs, and B doesn't.

**Narrator (V.O.):** Rule two: if A and B have the *same* priority, they take turns, round robin. That's the same time-slice rotation we already know.

**Narrator (V.O.):** So with this picture, A and B alternate forever. And C and D?

**Student** (frustrated): They never run! That's an outrage.

**Professor** (worried): It is, and we'll come back to it. But first: with priorities this rigid, everything depends on where each job sits. So who decides that?

*Visual idea:* Rules 1 and 2 appear on a "rulebook" panel on the right as one-liners. The CPU at the top lane: A and B hop on and off in alternation (a Timeline row fills A, B, A, B). C and D look up from their lanes with sad faces.

### B05 — Priorities that change  `build-up` (~0:45)
**Student** (curious): So who sets the priorities?

**Professor** (explaining): Nobody sets them once and for all. The key to MLFQ is that it *varies* a job's priority based on what it does, its **observed behavior**.

**Narrator (V.O.):** A job that keeps giving up the CPU to wait for the keyboard smells interactive, so MLFQ keeps its priority high. A job that burns the CPU for long stretches smells like a batch job, so MLFQ lowers its priority. The scheduler *infers* which is which, from history.

*Visual idea:* Two job traces side by side. B (mint) shows short bursts of CPU followed by a keyboard icon and a gap; A (coral) shows one long unbroken bar. B glides up the ladder toward the top lane; A sinks toward the bottom. Labels "interactive" and "CPU-bound".

### B06 — Attempt #1: allotment and Rules 3 and 4  `build-up` (~0:55)
**Narrator (V.O.):** To turn this into rules, we need one new concept: the **allotment**. It's the amount of time a job can spend at a given priority level before the scheduler lowers its priority. To keep things simple, we'll say for now that the allotment is exactly one time slice.

**Narrator (V.O.):** Rule three: when a job enters the system, it starts at the highest priority, the topmost queue.

**Narrator (V.O.):** Rule four, part A: if a job uses up its allotment while running, it moves down one queue.

**Narrator (V.O.):** Rule four, part B: if a job gives up the CPU, for example for an I/O, *before* its allotment is up, it stays where it is, and its allotment is reset.

**Student** (curious): So a job that keeps the CPU too long gets punished, and a job that's polite gets to stay?

**Professor** (happy): Exactly. Let's watch it work. From now on we use three queues, which the book calls Q2, Q1 and Q0, and a ten-millisecond time slice.

*Visual idea:* The ladder is reduced to three lanes (Q2 / Q1 / Q0) and a Timeline appears underneath with a row per queue. An "allotment bar" (fuel gauge) is attached to the running job. Rules 3, 4a, 4b are appended to the rulebook; 4a with a down arrow, 4b with a "reset" glyph.

### B07 — Example 1: a single long job  `build-up` (~0:45)
**Narrator (V.O.):** First example. One long-running job, A, alone in the system.

**Narrator (V.O.):** It arrives in the top queue, Q2. After ten milliseconds, it has used its allotment, so it moves down to Q1. Another ten milliseconds, and it moves down again, to Q0. And there it stays, running in the lowest queue until it's done. Pretty simple.

*Visual idea:* Figure 8.2. A (coral) enters Q2, the allotment gauge drains, A drops to Q1, then Q0. The Timeline fills: one block in Q2, one in Q1, then a long run of blocks in Q0 up to 200 ms.

### B08 — Example 2: along came a short job  `build-up` (~1:00)
**Narrator (V.O.):** Now a more interesting one. A is still running in the lowest queue. At time one hundred milliseconds, B arrives. B is an interactive job, and it only needs twenty milliseconds of CPU.

**Narrator (V.O.):** Rule three puts B in the top queue. By Rule one, B beats A, so B runs. Ten milliseconds later, B has used its allotment, and it moves down to Q1. Ten more, and B is *finished*, before it ever reaches the bottom. Now A resumes where it left off.

**Student** (excited): Wait. We never told the scheduler B was short!

**Professor** (proud): Right. That's the beauty of it. Since MLFQ can't know whether a job is short or long, it first *assumes* it might be short, and gives it high priority. If it really is short, it runs quickly and completes. If it isn't, it sinks down the queues and proves itself a long, batch-like job. In this way MLFQ approximates SJF.

*Visual idea:* Figure 8.3 (left). A continues in Q0; at 100 ms, B (mint) drops in at the top of the ladder. B runs in Q2, drops to Q1, runs, and finishes (check mark). A resumes. The Timeline shows both. Spotlight picks B at the top.

### B09 — Example 3: what about I/O?  `build-up` (~0:45)
**Narrator (V.O.):** Third example: I/O. Suppose B, the interactive job, only needs one millisecond of CPU before it asks for input, and it's competing with the long job A.

**Narrator (V.O.):** B runs for one millisecond and then blocks. That is giving up the CPU before the allotment is used up. So Rule four B applies: B stays at the same priority level. Each time B comes back from its I/O, it's still at the top, still ahead of A. The interactive job stays snappy, which is exactly the goal.

*Visual idea:* Figure 8.3 (right). B shows a thin sliver block in Q2 every time, followed by a clock icon (blocked), then back to the top lane; A's long blocks fill Q0 between slivers. The 4b rule glows on the rulebook.

### B10 — Three problems  `build-up` (~1:05)
**Narrator (V.O.):** So we have a basic MLFQ. Short and interactive jobs fly, and long ones share what's left. But it has serious flaws.

**Professor** (thinking): Can you spot them? Pause the video, and think as deviously as you can.

**Narrator (V.O.):** First: **starvation**. With too many interactive jobs, they consume *all* the CPU, and long jobs never get any.

**Narrator (V.O.):** Second: a smart user can **game the scheduler**, tricking it into giving them more than their fair share. Rule four B is the hole. Just before the allotment is used up, issue an I/O, and you keep your priority. Do that at ninety-nine percent of the allotment, every time, and one job can nearly monopolize the CPU.

**Professor** (worried): On a shared server, that's a **security** problem. Scheduling policy has to resist attack.

**Narrator (V.O.):** Third: programs change. A CPU-bound job may become interactive, but with our rules it's stuck at the bottom.

*Visual idea:* Three cards appear one at a time (starvation: a long job behind a wall of mint and gold interactive jobs; gaming: a job taps an "I/O" button at 99% on its allotment gauge; change: a coral job at the bottom sprouts a keyboard icon and can't climb). A Tip card with a padlock: "TIP: Scheduling must be secure from attack."

### B11 — Attempt #2: the priority boost  `build-up` (~1:00)
**Narrator (V.O.):** Let's fix starvation first. What if we guarantee that every job makes *some* progress? Simple idea: every so often, throw everybody back in the top queue.

**Narrator (V.O.):** That's Rule five: after some time period S, move all the jobs in the system to the topmost queue. This is the **priority boost**.

**Narrator (V.O.):** It solves two problems at once. A job in the top queue shares the CPU round robin, so it can't starve. And a CPU-bound job that turned interactive gets treated properly once it's boosted.

**Narrator (V.O.):** Here's the long job A, competing with two short interactive jobs, B and C. On the left, no boost: once B and C arrive, A is starved. On the right, we boost every hundred milliseconds. That's too small for a real system, but fine for a picture. Now A runs periodically.

*Visual idea:* Figure 8.4, left and right panels. First the left (no boost): A runs at Q0 until B and C arrive, then a wall of mint/gold slivers in Q2 with A frozen. Then rewind to the right: a stopwatch ticks 100 ms, an up-arrow lifts all jobs to Q2, A runs briefly at the top. Rule 5 appears on the rulebook.

### B12 — The voodoo constant  `build-up` (~0:35)
**Student** (curious): So what should S be?

**Narrator (V.O.):** Hard question. John Ousterhout called values like this **voodoo constants**, because they seem to need black magic to set. Too high, and long jobs starve. Too low, and interactive jobs lose their share.

**Professor** (explaining): Hence **Ousterhout's Law**: avoid voodoo constants if you can. Often you can't, so you get a config file of defaults an administrator tweaks, or, these days, machine-learned values.

*Visual idea:* A dial labeled `S` with a hand-drawn "?" and sparks; sliding to the left (too low) shows interactive jobs squeezed, to the right (too high) shows the long job starving. An Aside card: "TIP: Avoid voodoo constants (Ousterhout's Law)".

### B13 — Attempt #3: better accounting  `build-up` (~0:55)
**Narrator (V.O.):** Now gaming. The culprits are Rules four A and four B: the scheduler *forgets* how much CPU a job already used whenever it does I/O.

**Narrator (V.O.):** The fix is better **accounting**. At each level, the scheduler keeps track of the allotment used, even across I/Os. Once it's spent, the job is demoted. One long burst or many small ones: it doesn't matter.

**Narrator (V.O.):** So we merge four A and four B into one rule: once a job uses up its allotment at a given level, regardless of how many times it has given up the CPU, its priority is reduced.

**Narrator (V.O.):** On the left, the gamer B issues an I/O before every allotment ends, stays on top, and dominates the CPU. On the right, with the new rule, it slowly sinks. No unfair share.

*Visual idea:* Figure 8.5, left and right. The allotment gauge from earlier: before, an I/O resets it to full; now it stays drained across I/Os. Rules 4a and 4b on the rulebook merge (`Transform`) into a single Rule 4. Timeline: the left shows B hogging Q2; the right shows B stepping down.

### B14 — Turning the knobs  `build-up` (~0:55)
**Narrator (V.O.):** Plenty of questions remain. How many queues? How long a time slice at each level? How big an allotment? How often to boost? There are no easy answers, only experience with real workloads.

**Narrator (V.O.):** One common idea: high-priority queues get *short* slices, ten milliseconds or less, because interactive jobs alternate quickly. Low-priority queues hold CPU-bound jobs, so they get *long* slices, hundreds of milliseconds.

**Narrator (V.O.):** In this example, the top queue has a ten-millisecond slice, the middle one twenty, the bottom one forty. Two jobs run through the top, then the middle, then settle into long, uninterrupted runs at the bottom.

*Visual idea:* A control panel of four sliders (queues, slice per queue, allotment, boost period). Then Figure 8.6: the Timeline with lanes drawn at different widths: thin slices at Q2, wider at Q1, widest at Q0; A and B alternate in each.

### B15 — MLFQ in the wild  `build-up` (~0:50)
**Narrator (V.O.):** Real systems tune these knobs differently. The Solaris Time-Sharing class is an editable table. By default: sixty queues, slices growing from twenty milliseconds at the top to a few hundred at the bottom, and a boost about once a second.

**Narrator (V.O.):** FreeBSD skips the table. It computes priority from CPU used, and that usage *decays* over time, which plays the role of the boost.

**Narrator (V.O.):** Some schedulers reserve the top levels for the OS itself. And many accept **advice**: the UNIX `nice` command raises or lowers a job's priority, a little.

**Professor** (explaining): The OS rarely knows what's best, so it takes *hints*. It isn't obliged to obey.

*Visual idea:* A table card "Solaris TS: 60 queues, 20 ms → hundreds of ms, boost ~1 s"; a formula card "priority = f(CPU used, decaying)"; a `nice` terminal line. Tip card: "TIP: Use advice where possible."

### B16 — The big picture: five rules  `big picture` (~0:45)
**Narrator (V.O.):** Let's put it all together. Here are the five rules, as refined.

**Narrator (V.O.):** One: higher priority runs. Two: equal priority takes turns, round robin, using the time slice of that queue. Three: new jobs start at the top. Four: a job that uses up its allotment at a level moves down, however many times it gave up the CPU. Five: every so often, everybody goes back to the top.

**Narrator (V.O.):** That's why it's called a Multi-Level *Feedback* Queue. It has *multiple levels* of queues, and it uses *feedback* to decide a job's priority. History is its guide.

**Narrator (V.O.):** It doesn't demand to know a job in advance. It watches. Short jobs get excellent response, close to SJF or STCF, and long jobs still make fair progress. BSD UNIX derivatives, Solaris, and Windows NT and its successors all use a form of MLFQ as their base scheduler.

*Visual idea:* The finished ladder, Timeline and rulebook, all together. Jobs A, B, C cycle through a short loop: B and C hop on the top lane and finish; A sinks, gets boosted, sinks again. The five rules highlight one at a time as they fire. Then the OS logos' stand-ins (BSD, Solaris, Windows NT) as small name tags.

### B17 — Recap  `recap` (~0:35)
**Narrator (V.O.):** So, today:
1. MLFQ uses several queues at different priority levels, and the CPU goes to the highest one.
2. It doesn't know job lengths, so it **learns from history**: new jobs start at the top and sink as they use their allotment.
3. Jobs that give up the CPU quickly keep a high priority, so interactive jobs stay snappy, and the scheduler approximates SJF.
4. A **priority boost** stops starvation, and **better accounting** stops gaming.
5. Every knob, the number of queues, the slice lengths, `S`, takes tuning, and none has an obvious best value.

*Visual idea:* Five-item recap list, each with a tiny icon (ladder, history clock, mint job at the top, boost arrow + padlock, dial).

### B18 — Teaser  `teaser` (~0:25)
**Student** (curious): MLFQ is clever. But it has so many knobs, and the rules keep patching each other. Isn't there a simpler way to share the CPU fairly?

**Professor** (happy): There is. Forget turnaround and response for a moment. What if we just promised each job a *share* of the CPU, and picked the next one by drawing a ticket from a hat?

**Student** (surprised): The scheduler gambles?

**Professor** (proud): Next time.

*Visual idea:* A hat or jar fills with colored tickets (A coral ×3, B mint ×1, C gold ×1); one ticket is pulled; cut to black with "Next: 09 · Lottery Scheduling".

## Cut / deferred material
- **Homework (mlfq.py simulation):** cut from the video. It could become an on-screen "try it yourself" link at the end.
- **References** (CTSS, Solaris Internals, decay-usage paper, Y+18, etc.): cut. CTSS and Corbato are named in B02.
- **Fine details of Solaris's table and FreeBSD's formula:** reduced to one sentence each (B15). The book itself doesn't go into the formula.
- **Machine-learning-based tuning of S (A+17):** mentioned in a half-sentence in B12.
- **Which end of the queue a job returning from I/O is added to (homework Q6, `-I` flag):** cut; it is an open question in the book.
- **Proportional-share scheduling:** deferred to 09 (Lottery Scheduling); multi-CPU scheduling is in 10.

## Callbacks & setups
- Callbacks to earlier episodes:
  - 07: SJF/STCF need job lengths; Round Robin vs. turnaround and response time (B01). The ready queue from 04 grows into the priority ladder (B03).
  - 04: running / ready / blocked, and I/O blocking (B09), plus the "scheduler" and the "policy vs. mechanism" idea (policy = the five rules).
  - 06: the timer interrupt that makes time slices possible (B06, mentioned only via the time slice).
- Setups paid off in later episodes:
  - "Proportional share" and the ticket jar (B18) → 09 Lottery Scheduling.
  - Multiple queues and priority → 10 Multi-CPU Scheduling (per-CPU queues vs. a single shared queue).
  - Learn from history (B03) → caching and page replacement later in the series.

## Open questions
- **Length:** ~14 min is at the top of the regular-chapter range. If you want it shorter, merge B12 (voodoo constants) into B11, and B15 (real systems) into B14, which would save about 1:15 and land near 12:45.
- **Queue naming:** the book uses Q8..Q1 in Figure 8.1 but Q2..Q0 in all later figures. I keep that split (a ladder of eight first, then three). OK?
- **"Gaming" demo:** the book's text says a job could run for 99% of the allotment; its Figure 8.5 shows a gray job alternating with the black one. I use the same B (mint) as the gamer, which also plays the "good" interactive job earlier. Should the gamer be a new job with a different color?
- **Teaser:** the Student's "isn't there a simpler way?" slightly editorializes MLFQ; the book simply moves on to proportional share. Fine?
