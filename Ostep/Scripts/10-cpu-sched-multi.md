# 10 — Multiprocessor Scheduling (Advanced)
> Section: Virtualization · Source: Ostep/Chapters/10-cpu-sched-multi.pdf · Est. duration: ~16:00 (2,530 words incl. dialogue ≈ 16:50 at 150 wpm; beat durations below sum to ~16:05 with the narration tightened in recording)

## Logline
Your laptop has eight CPUs, and every scheduler we have met so far was built for one. Adding CPUs
sounds like it should make life easier. It doesn't. Caches, stale data, locks and idle cores turn
scheduling into a new problem, and the two classic answers (one shared queue, or one queue per
CPU) each fail in their own way.

## Learning goals
- After watching, the viewer can explain why a program that uses one CPU does not get faster with more CPUs.
- Describe how **caches** and **locality** speed up a CPU, and why several caches create the **cache coherence** problem (and how **bus snooping** fixes it).
- Explain why shared scheduler data needs **locks**, and why those locks hurt as CPUs are added.
- Define **cache affinity** and say why a scheduler should respect it.
- Compare **SQMS** and **MQMS**, name each one's weakness (scalability and affinity vs. **load imbalance**), and describe **migration** and **work stealing** as the fix.

## Concepts covered
| Term | Definition (book's wording or faithful paraphrase) | Beat |
|---|---|---|
| Multiprocessor / multicore | A system with several CPUs; multicore = several CPU cores packed on one chip. | B01 |
| Parallel program, threads | A single-CPU program must be rewritten (for example with threads) to spread its work across CPUs. | B01 |
| Hardware cache | Small, fast memory that holds copies of popular data found in the (slower, larger) main memory. | B03 |
| Temporal locality | Data that was just accessed is likely to be accessed again soon. | B04 |
| Spatial locality | If a program accesses address x, it is likely to access nearby addresses too. | B04 |
| Cache coherence | The problem of keeping several caches' views of one shared memory consistent. | B05 |
| Bus snooping | Each cache watches the bus that connects caches to memory; on seeing an update to data it holds, it **invalidates** its copy or **updates** it. | B06 |
| Mutual exclusion / lock | Primitives that make shared-structure updates atomic. Needed even with coherent caches. | B07 |
| Lock-free data structure | A way to avoid locks; complex, used only on occasion. | B07 |
| Cache affinity | A process that runs on a CPU builds up state in its caches (and TLBs); running it there again is faster. | B08 |
| SQMS (single-queue multiprocessor scheduling) | All jobs in one queue; each CPU picks the next job from it. | B09 |
| Scalability | How well a design keeps working as CPUs are added. SQMS's locks contend more as CPUs grow. | B09 |
| MQMS (multi-queue multiprocessor scheduling) | One scheduling queue per CPU; a job is placed on exactly one queue. | B11 |
| Load imbalance | Some CPUs have much more work than others, or sit idle. | B12 |
| Migration | Moving a job from one CPU to another to rebalance load. | B13 |
| Work stealing | A queue low on jobs peeks at another queue; if it is notably fuller, it steals one or more jobs. | B14 |
| O(1), CFS, BFS | The three Linux multiprocessor schedulers: O(1) and CFS use multiple queues, BFS uses a single queue (proportional-share, based on EEVDF). | B15 |

## Script

### B01 — Eight cores, one slow program  `cold open` (~1:00)
**Student** (excited): My new laptop has eight cores! So now every program I write runs eight
times faster, right?

**Professor** (thinking): Let's test that. Take a normal C program, the kind you've written all
semester. Run it on this machine.

**Narrator (V.O.):** One core lights up. Seven sit idle. A typical program only uses a single CPU.
Adding CPUs does not make it run faster. To use eight cores, you'd have to rewrite it to run in
**parallel**, perhaps using **threads**. Remember the threads from the first episodes, the ones that
fought over the shared counter?

**Student** (confused): Okay, so that's the programmer's problem. What does it have to do with the OS?

**Professor** (explaining): Everything. Because the moment you *do* have eight busy threads, plus
every other process on the machine, someone has to decide who runs on which core. And everything we
learned about scheduling assumed exactly one CPU.

**Narrator (V.O.):** Quick note. The book calls this an *advanced* chapter. It leans on ideas from
concurrency, which we haven't fully covered yet. So we'll sketch those parts, and promise to come
back to them later.

*Visual idea:* A laptop with a row of eight CPU chips inside; one chip glows yellow, seven dark. The Student's bubble says "8x?". Term "multicore" on the chip row. Then a program splits into threads and lights up the rest.

### B02 — The Crux  `crux` (~0:20)
> **THE CRUX: HOW TO SCHEDULE JOBS ON MULTIPLE CPUS**
> How should the OS schedule jobs on multiple CPUs? What new problems arise? Do the same old
> techniques work, or are new ideas required?

**Narrator (V.O.):** Which brings us to the question behind this whole episode: how to schedule jobs on multiple CPUs? What new problems arise? Do the same old techniques work, or are new ideas required? So that's the question. Do the old techniques work, or do we need new ideas?
Spoiler: a bit of both. But to see why, we first have to look at what changed in the *hardware*.

*Visual idea:* Crux card in the Virtualization accent (orange); section badge "10 · Multi-CPU Scheduling".

### B03 — Caches: a fast shelf  `build-up` (~0:45)
**Narrator (V.O.):** Here is the single CPU we've been using all along. And now, a detail we've
been hiding: the **cache**.

**Narrator (V.O.):** Main memory holds *all* the data, but it's slow. Tens of nanoseconds, maybe
hundreds. So the CPU keeps a small, fast memory right next to it: a **hardware cache**. It holds
copies of popular data from main memory. Think of the books on your desk versus the ones in the
library across town.

**Narrator (V.O.):** The first time the program loads a value, the CPU has to go all the way to
memory. It copies the value into the cache on the way back. The next time, it finds the value in the
cache, and gets it in just a few nanoseconds. The large slow memory suddenly looks like a fast one.

*Visual idea:* Adapt Figure 10.1: CPU with a cache strip attached, Memory below. A load request travels to Memory (slow, long trail with a stopwatch "~100 ns") and returns with a copy that lands in the cache; the second load hits the cache (short trail, "~few ns").

### B04 — Locality  `build-up` (~0:35)
**Student** (curious): But the cache is tiny. How does it know what to keep?

**Narrator (V.O.):** It guesses, and the guess works because of **locality**. There are two kinds.
**Temporal locality**: data you just used is likely to be used again soon, like a loop counter, or
the instructions of the loop itself. **Spatial locality**: if you touch address x, you will probably
touch the neighbors soon, like a program walking through an array.

**Narrator (V.O.):** Programs show both kinds all the time, so caches work well. Keep this in mind.
It is the whole reason the rest of the episode matters.

*Visual idea:* Two mini panels. Temporal: the same memory cell lights up again and again inside a loop. Spatial: a row of cells lights up one after another, and the cache grabs a neighbor-sized chunk.

### B05 — Two CPUs, two caches  `build-up` (~1:20)
**Narrator (V.O.):** Now the tricky part. Add a second CPU. Each CPU has its own cache, and both
share one main memory, connected by a **bus**.

**Narrator (V.O.):** Watch what can go wrong. Memory holds a value at some address. The program, on
CPU one, reads it. It's not in CPU one's cache, so it's fetched from memory: the value is seven. The
program then changes it to nine. But writing all the way back to slow main memory takes a while, so
the system, usually, just updates the cache and does the write to memory *later*.

**Narrator (V.O.):** Now the OS stops the program and moves it to CPU two. (The book's example
calls the old value D and the new one D-prime.) The program reads the same address again. CPU two's
cache has nothing. So it fetches from main memory, which still holds the *old* value. Seven.
Not nine.

**Student** (surprised): The program just read stale data. The wrong answer, from the right address!

**Professor** (worried): This is the problem of **cache coherence**. Each cache has its own view of
the "one" shared memory, and the views disagree. Research on it fills libraries. We'll skip the
nuance, and take a computer architecture course for that.

*Visual idea:* Adapt Figure 10.2: two CPUs with caches, the Bus line, Memory underneath. The value "7" travels up into cache 1, turns into "9" (the cache cell glows), memory still says 7. The Process hops to CPU 2 and reads: the stale "7" arrives, with a red mismatch flash. The Computer looks surprised/error.

### B06 — Bus snooping  `build-up` (~0:50)
**Narrator (V.O.):** The fix is the hardware's job. And the basic idea is delightfully nosy. Every
cache watches the bus, the wire connecting everything to memory. This is **bus snooping**.

**Narrator (V.O.):** When a cache sees an update for data it holds, it reacts in one of two ways. It
can **invalidate**: throw its own copy away, so the next read has to fetch the fresh value. Or it
can **update**: put the new value into its own cache too. Either way, the one shared memory stays
one shared memory. Write-back caches, like our example, make this trickier, because the write to
memory isn't visible until later. But you can imagine how the basic scheme works.

**Student** (excited): So the hardware makes sure the program sees the right value, no matter which
CPU it's on. Then we're done!

**Professor** (happy): Hold that thought.

*Visual idea:* Replay the problem with a magnifier-eye on each cache watching the Bus. Cache 1's update goes out on the bus; cache 2 sees it and either crosses out its old copy (invalidate) or rewrites it to 9 (update). Two small labels alternate. Tick on the Student's idea, then the Professor's "hold that thought" dims it.

### B07 — Coherence isn't enough: locks  `build-up` (~1:15)
**Narrator (V.O.):** Coherent caches guarantee that every CPU sees the *same* memory. They don't
guarantee that two CPUs will modify it in a sensible *order*. Here is a shared linked list, and the
routine that removes the head from it.

**Narrator (V.O.):** Read the head into a temporary variable. Remember its value. Move the head
forward. Free the old head. Return the value. Now imagine threads on two CPUs both run the first
line at the same time. Each has its own private temporary, because that lives on its own stack. Both
point to the *same* head. So both remove the same element, both free it, and the program frees
memory twice. Even with perfect cache coherence.

**Narrator (V.O.):** The solution, as you may remember from the first episodes, is **mutual
exclusion**: wrap the routine in a **lock**. Lock at the top, unlock at the end, and only one CPU at
a time is inside. We won't get into the details here. They're the subject of the whole concurrency
section. But hold on to one fact: locks have a cost. As the number of CPUs grows, accessing a
shared, locked data structure gets *slow*.

**Narrator (V.O.):** There are also **lock-free** structures that avoid locks, but they are
complicated, and used only on occasion.

*Visual idea:* Code block of Figure 10.3 (`List_Pop`). Two thread-processes on two CPUs execute line 7 simultaneously, each with a private `tmp` arrow to the same head node. Both free the node: a double-free "boom". Rewind, then a padlock wraps the routine: the second CPU waits outside the door.

### B08 — Cache affinity  `build-up` (~0:45)
**Narrator (V.O.):** One last piece of hardware. When a process runs on a CPU, it gradually fills
that CPU's caches (and its TLBs, which we'll meet in the memory episodes) with its own data. It
builds up *state*. This is called **cache affinity**: the CPU is warm for that process.

**Narrator (V.O.):** The next time that process runs, it runs faster on the same CPU, because much
of its state is already there. Put it on a different CPU, and it must reload everything, slowly. It
still runs correctly, thanks to coherence, just slower.

**Professor** (explaining): So a multiprocessor scheduler should consider cache affinity. When
possible, keep a process on the same CPU.

*Visual idea:* A process on CPU 0 with a cache that fills with its color as time passes (a "warmth" meter rising). Then it hops to CPU 1: CPU 1's cache is empty, the meter resets and the process runs slow (small stopwatch).

### B09 — Attempt 1: one shared queue (SQMS)  `build-up` (~1:15)
**Student** (curious): Fine. So what's the simplest scheduler? Take the one we already have and
share it?

**Narrator (V.O.):** Exactly the simplest approach. Put all jobs into a single queue. Each CPU,
whenever it needs work, grabs the next job from it. This is **single-queue multiprocessor
scheduling**, or **SQMS**. It needs almost no new work. Take any single-CPU policy, and let it pick
the best job to run, and then the second best for the second CPU, and so on.

**Narrator (V.O.):** But there are two problems. The first: **scalability**. The queue is shared, so
the scheduler must lock it. And as we just saw, locks hurt more and more as CPUs grow. More time is
spent waiting for the lock, less time doing the work the system is supposed to do. (The book wishes
it had a real measurement here. Take our word for it, for now.)

**Narrator (V.O.):** The second problem is cache affinity. Take five jobs, A through E, and four
CPUs. Each CPU simply takes the next job from the shared queue, so over time the jobs bounce around.
A on CPU zero, then CPU one, then CPU two. Each time it lands on a cold cache. This is exactly the
opposite of what affinity wants.

*Visual idea:* Queue A–E with four CPUs pulling from it; a padlock on the queue, with CPUs lining up and a stopwatch of "waiting". Then Figure (page 6) schedule grid: 4 rows (CPU 0–3), every job shifts one CPU per slice, diagonal pattern, cache warmth meters constantly resetting.

### B10 — Patching SQMS with affinity  `build-up` (~0:40)
**Narrator (V.O.):** Real SQMS schedulers add an affinity mechanism. Let some jobs stay put, and
move others around to balance the load. For our five jobs: A, B, C and D each stay on their own CPU.
Only job E *migrates*, from CPU to CPU, so the load stays fair. A different job could take the
migrating role the next time round, if you want fairness among the others too.

**Professor** (explaining): It works. But it's complex to build. So SQMS is easy to write, and
doesn't scale or preserve affinity well.

*Visual idea:* The same four-CPU grid, now with A to D locked onto CPU 0–3 (warm caches glow) and only E hopping from CPU to CPU (Figure on page 7).

### B11 — Attempt 2: one queue per CPU (MQMS)  `build-up` (~1:00)
**Narrator (V.O.):** So some systems flip the design around. Give every CPU its own queue. This is
**multi-queue multiprocessor scheduling**, or **MQMS**.

**Narrator (V.O.):** Each queue runs its own policy, say round robin. A new job gets placed on
exactly one queue, by some heuristic: pick randomly, or the one with fewer jobs. After that, each
CPU schedules *independently*. No shared structure, no shared lock. With two CPUs and four jobs, A
and C go to queue zero, B and D to queue one. CPU zero alternates between A and C, CPU one between
B and D.

**Narrator (V.O.):** The payoff is real. MQMS is naturally scalable: more CPUs, more queues, and the
locks are never in contention. And a job stays on its CPU, so affinity comes for free.

**Student** (excited): That sounds perfect.

**Professor** (worried): That is what I would say, if I hadn't been paying attention to the title
of the next section.

*Visual idea:* Two Queues (Q0: A, C; Q1: B, D) feeding CPU 0 and CPU 1. A round-robin Timeline (Figure on page 8): CPU 0 = A A C C A A C C, CPU 1 = B B D D B B D D. The padlock from B09 disappears, the cache warmth meters stay full.

### B12 — The trouble: load imbalance  `build-up` (~1:15)
**Narrator (V.O.):** Suppose job C finishes. Queue zero now holds only A. Queue one still holds B
and D. Run round robin on each queue independently, and what happens? CPU zero runs A, and only
A, all the time. CPU one still splits its time between B and D. So A gets *twice* as much CPU as B
or D. That's not the fair share the scheduler wanted.

**Narrator (V.O.):** It gets worse. Suppose A finishes too. Queue zero is now empty. CPU zero has
nothing to do. It sits idle, while CPU one is juggling two jobs. How terrible.

**Computer** (sleeping): *(snore, half of the CPUs dark)*

**Narrator (V.O.):** This is **load imbalance**, the fundamental problem of multi-queue scheduling.

**Narrator (V.O.):** And that leaves us with a second crux: how to deal with load imbalance?

> **THE CRUX: HOW TO DEAL WITH LOAD IMBALANCE**
> How should a multi-queue multiprocessor scheduler handle load imbalance, so as to better achieve
> its desired scheduling goals?

*Visual idea:* Figure sequence from page 8. C finishes (done check): CPU 0's timeline becomes AAAAAAAAA, CPU 1 still BBDD; share brace "A: 2x". Then A finishes, CPU 0's row turns into hatched idle blocks; second Crux card (small) docks.

### B13 — Migration  `build-up` (~1:20)
**Narrator (V.O.):** The obvious answer: move jobs around. We've seen this word before. **Migration**.
Take a job from a busy CPU, and give it to an idle one.

**Narrator (V.O.):** The easy case first. Queue zero is empty, queue one holds B and D. Just move
one of them, say B, over to CPU zero. One migration, balanced load, everybody's happy.

**Student** (curious): And the harder case?

**Narrator (V.O.):** Here's a trickier one. A is alone on CPU zero. B and D share CPU one. One
migration doesn't fix this: moving B just flips the problem. The load is three jobs on two CPUs.
Nobody can give a whole CPU's worth to everyone, so the answer is *continuous* migration. Keep
switching jobs around. First A alone on CPU zero, and B and D alternate on CPU one. After a few
time slices, B moves to CPU zero to compete with A, while D enjoys a few slices alone on CPU
one. And the load stays balanced, over time.

**Professor** (explaining): There are many other migration patterns. But the real question is the
decision: *how* should the system decide to migrate?

*Visual idea:* Figure on page 9: Q0 empty, Q1 B, D: B hops over (easy). Then the tricky one: the timeline with A, B, D switching CPUs (A A A A B A B A B B B B on CPU 0, B D B D D D D A D A D on CPU 1). Migrating jobs get a small suitcase glyph; their cache-warmth meters drop on each migration (callback to affinity).

### B14 — Work stealing  `build-up` (~1:00)
**Narrator (V.O.):** One basic approach is **work stealing**. A queue that's running low on jobs
occasionally *peeks* at another queue to see how full it is. If the other queue is notably fuller,
the low queue **steals** one or more jobs to balance the load.

**Student** (confused): How often should it peek?

**Narrator (V.O.):** There's the catch. If CPUs peek too often, they take locks on each other's
queues, the overhead goes up, and we've rebuilt SQMS, the thing we were trying to escape. If they
peek too rarely, we're back to severe load imbalance. Finding the right threshold is, as is common
in system policy design, a black art.

**Professor** (happy): That's the honest answer. And here's another tension: every steal throws away
a bit of cache affinity.

*Visual idea:* Q0 empty, Q1 holding B, D, E. A small eye icon hops from Q0 to Q1 every few seconds; at "peek too often" it blinks wildly with a lock icon on Q1 and a stopwatch; at "too rarely" CPU 0 stays hatched idle. A job slides from Q1 to Q0 when stolen.

### B15 — What Linux did  `build-up` (~0:50)
**Narrator (V.O.):** So what does a real system do? Interestingly, in the Linux community no single
solution won. Three different multiprocessor schedulers arose over time. The **O(1) scheduler**, the
**Completely Fair Scheduler**, or **CFS**, and the **BF Scheduler**, or **BFS**.

**Narrator (V.O.):** O(1) and CFS use *multiple* queues. BFS uses a *single* queue. So, both
approaches can work, in practice. They differ in more than that. O(1) is a priority-based scheduler,
a bit like the MLFQ we saw before. It changes a process's priority over time and runs the highest
first, with interactivity as a focus. CFS, in contrast, is deterministic and proportional-share,
like the stride scheduling from last time. BFS is also proportional-share, but built on a more
complicated scheme called Earliest Eligible Virtual Deadline First, EEVDF.

**Narrator (V.O.):** (And about that "BF" in BFS: the book says you should look it up yourself. It is
not for the faint of heart.)

*Visual idea:* Three cards in a row labeled O(1), CFS, BFS. Under each, a mini queue diagram: O(1) and CFS with several small queues, BFS with a single queue. A tag on each: "priority (MLFQ-like)", "proportional share (stride-like)", "proportional share (EEVDF)". The "BF" in BFS is covered by a small "ask your search engine" sticker.

### B16 — The big picture  `big picture` (~0:50)
**Narrator (V.O.):** Let's put it all in one place. The single-queue approach is simple to build and
balances load well, but struggles to scale to many processors, and loses cache affinity. The
multi-queue approach scales better and handles affinity well, but has trouble with load
imbalance, and is more complicated.

**Narrator (V.O.):** Whichever approach you choose, there is no simple answer. Building a
general-purpose scheduler remains a daunting task, because small code changes can lead to large
behavioral differences. Only try it if you know exactly what you are doing, or, at least, if you are
getting paid a large amount of money to do so.

*Visual idea:* A two-column comparison table card built from the episode's props: SQMS (one queue + padlock icon + a bouncing job) vs MQMS (two queues + a hatched idle CPU). Rows: simple / scales / affinity / balances load, with tick and cross marks (green/red).

### B17 — Recap  `recap` (~0:35)
**Narrator (V.O.):** So, today:
1. Programs that use one CPU don't speed up on many. And the OS must schedule across CPUs.
2. **Caches** use locality to speed things up; with several CPUs, hardware keeps them **coherent** by **bus snooping**.
3. Shared data still needs **locks**, which slow down as CPUs grow.
4. **Cache affinity**: keep a job on the same CPU when you can.
5. **SQMS** is simple but doesn't scale or keep affinity. **MQMS** scales, but suffers **load imbalance**, fixed by **migration** and **work stealing**.

*Visual idea:* Five-item recap list, each with a tiny icon: CPU row, cache + bus, padlock, warmth meter, two queues.

### B18 — Teaser  `teaser` (~0:30)
**Student** (curious): So after all this, we know how to schedule on one CPU, and on many. What's
left?

**Professor** (happy): One more short conversation, to pull the whole virtualization of the CPU
together. And then we leave the CPU behind, and virtualize memory.

**Narrator (V.O.):** But we will meet those locks again. Much of this chapter said "we'll see later".
Later is the concurrency section: threads, locks, and what they cost. Next: the CPU virtualization
dialogue.

*Visual idea:* The padlock and a thread glyph hop onto a "Part 2" tag in the corner; cut to black with "Next: 11 · Summary Dialogue".

## Cut / deferred material
- **Homework (multi.py simulation):** cut. Could become a "try it yourself" end card, as in 04.
- **References** (Anderson on spin locks, Boyd-Wickizer on Linux scalability, Goodman on bus snooping, Meehan's dissertation, SHW11, EEVDF paper, etc.): cut. Meehan's dissertation and EEVDF could be linked in the video description.
- **Cache coherence details (write-back vs write-through, MESI, directories):** only the book's level (invalidate or update) is shown. Deeper study left to computer architecture.
- **Mutual exclusion, lock implementations, lock-free structures, deadlock:** sketched in B07; real treatment in concurrency episodes 26–32 (the locks material around 28).
- **TLBs:** mentioned in B08 as part of CPU state; explained in the memory episodes (19).
- **Measurements of lock contention:** the book notes it would like to include one; we don't invent numbers.
- **Linux scheduler internals** (O(1) priority arrays, CFS red-black trees, EEVDF): one card; details are left to the book's pointer.
- **Super-linear speedup (homework 7):** cut.

## Callbacks & setups
- Callbacks to earlier episodes:
  - The shared-counter threads race from the Overview (B01, B07).
  - The single CPU, Queue, Timeline and scheduling idea from 04 and from 07 (round robin), MLFQ from 08 (O(1)) and stride/CFS from 09 (B15). Those episodes weren't available when this was written, so these callbacks assume they cover those topics as their titles say.
  - Process colors A to D stay as in 04.
  - "Migration" echoes the way processes hopped between CPU and queue in 04.
- Setups paid off in later episodes:
  - TLBs (19), caches again in the memory section.
  - Locks, threads and atomic updates (26–28).
  - 11 (Summary dialogue) closes the CPU virtualization section.

## Open questions
- **Length:** ~16 min is above the bible's 8–15 min. The chapter has two halves (hardware, then scheduling). Options: (a) split into two episodes, 10a hardware (B01–B08) and 10b scheduling (B09–B18), (b) keep as is, or (c) trim ~2 min by merging B03/B04, dropping B10 and shortening B15.
- **Size of the hardware segment:** B03–B08 are about 6 minutes of cache and coherence. It's the chapter's own proportion, but a viewer could be waiting for "scheduling". Should I trim B03/B04 by merging them?
- **Data values:** the book calls the shared value D and D′; I use 7 and 9 to avoid clashing with job D. I mention the book's names once. OK?
- **Analogy:** "books on your desk vs. the library across town" and "nosy bus" are mine, not the book's.
- **Callback assumptions:** I assume 07 covers round robin, 08 MLFQ, 09 stride/CFS and 11 is the summary dialogue. Please confirm once those files exist.
- **Humor:** the book's "Decepticons" footnote (a Transformers joke) is left out; the "BF" footnote is kept.
