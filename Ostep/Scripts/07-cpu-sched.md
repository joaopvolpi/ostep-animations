# 07 — Scheduling: Introduction
> Section: Virtualization · Source: Ostep/Chapters/07-cpu-sched.pdf · Est. duration: ~13:45 (1,800 spoken words ≈ 12:00 of narration, plus pauses)

## Logline
We know *how* the OS can stop one process and start another. But *which* one should it pick? This
episode builds scheduling policies from scratch: FIFO, Shortest Job First, Shortest Time-to-Completion
First and Round Robin. Each one fixes the last one's flaw, and we discover that no policy wins at
everything.

## Learning goals
- After watching, the viewer can compute **turnaround time** and **response time** for a small set of jobs.
- Explain the **convoy effect** and why FIFO suffers from it.
- Explain how **SJF** and **STCF** reduce turnaround time, and what **preemption** adds.
- Explain how **Round Robin** and its **time slice** improve response time, and what that costs.
- State the **trade-off**: a policy that is fair and responsive does badly on turnaround, and vice versa.
- Describe how a scheduler can overlap **I/O** with computation, and why knowing job lengths is the shakiest assumption.

## Concepts covered
| Term | Definition (book's wording or faithful paraphrase) | Beat |
|---|---|---|
| Scheduling policy (discipline) | The high-level algorithm that decides which process runs next; the *policy* to the context switch's *mechanism*. | B02 |
| Workload / job | The processes running in the system; a "job" is one of them, here seen as a fixed amount of CPU work. | B03 |
| Workload assumptions | Five simplifications: equal run-times, simultaneous arrival, run to completion, CPU only (no I/O), run-time known. | B03 |
| Scheduling metric | Something we use to *measure* a scheduler, so policies can be compared. | B04 |
| Turnaround time | T_turnaround = T_completion − T_arrival. A *performance* metric. | B04 |
| Fairness (Jain's Fairness Index) | The other kind of metric; it often conflicts with performance. | B04 |
| FIFO / FCFS | First In, First Out (First Come, First Served): run jobs in arrival order. Simple, so it's easy to implement. | B05 |
| Convoy effect | Short, potential consumers of a resource get queued behind a heavyweight consumer. | B06 |
| Shortest Job First (SJF) | Run the shortest job first, then the next shortest, and so on. Provably optimal for turnaround time when all jobs arrive together. | B07 |
| Non-preemptive / preemptive | A non-preemptive scheduler runs each job to completion; a preemptive one is willing to stop one process to run another (it uses the context switch). | B08 |
| Shortest Time-to-Completion First (STCF / PSJF) | SJF plus preemption: whenever a job arrives, run whichever job has the least time *left*. | B09 |
| Response time | T_response = T_firstrun − T_arrival. How soon a job is scheduled for the first time. | B10 |
| Round Robin (RR) / time slice (scheduling quantum) | Run each job for a time slice, then switch to the next in the run queue; repeat until all are done. The slice must be a multiple of the timer-interrupt period. | B11 |
| Amortization | When an operation has a fixed cost, pay it less often. A longer time slice amortizes the cost of context switching. | B11 |
| Trade-off | Fair policies (RR) do well on response time and badly on turnaround; unfair ones (SJF/STCF) do the reverse. | B12 |
| Overlap | Start an operation (I/O), then switch to other work while it runs, to raise utilization. | B13 |
| Oracle / a priori knowledge | Knowing each job's length in advance; real OSes usually don't. | B14 |
| Multi-level feedback queue | The teased answer: use the recent past to predict the future. | B16 |

## Script

### B01 — The family with three carts  `cold open` (~0:35)
**Narrator (V.O.):** You're at the supermarket. You've got one carton of milk. You pick the shortest
line, and just as you get there, the family in front of you starts unloading. Three carts. Piled high.
Plus a checkbook.

**Student** (frustrated): I'm going to be here all day.

**Professor** (thinking): Everyone has felt this. And everyone has an instinct about what the store
*should* do: let the milk go first.

**Narrator (V.O.):** The book's advice, by the way, is to take a long, deep breath. In. Out. It will be
okay. Now: that line is a **scheduler**, and the store just made a policy decision. Let's see how good
it was.

*Visual idea:* A checkout line drawn as a Queue of cartoon shoppers; the first has three huge carts, the
last holds one carton of milk. A tiny stopwatch ticks beside the milk shopper. The **Student** looks
frustrated at the bottom-left.

### B02 — The Crux  `crux` (~0:25)
> **THE CRUX: HOW TO DEVELOP SCHEDULING POLICY**
> How should we develop a basic framework for thinking about scheduling policies? What are the key
> assumptions? What metrics are important? What basic approaches have been used in the earliest
> computer systems?

**Narrator (V.O.):** Remember mechanisms versus policies? Last episode we met the mechanism: the
context switch. It tells the OS *how* to stop one process and start another. Today is about the
*which*. And the answer, as we'll see, is surprisingly full of trade-offs.

*Visual idea:* Crux card in the Virtualization accent (orange); section badge "07 · Scheduling". The
gear (mechanism) shrinks aside, and the spotlight (policy) rises into the center as the focus.

### B03 — Five convenient lies  `build-up` (~0:50)
**Narrator (V.O.):** To think clearly, let's first simplify. The processes running in the system are
the **workload**, and we'll call each one a **job**. We'll assume five things about the workload.

**Narrator (V.O.):** One: every job runs for the same amount of time. Two: all jobs arrive at the same
moment. Three: once started, a job runs to completion. Four: jobs only use the CPU. They never do I/O.
Five: the run-time of each job is known in advance.

**Student** (confused): Known in advance? How would the OS ever know that?

**Professor** (explaining): It wouldn't. That's the least realistic one, and it makes our scheduler
all-knowing. But these assumptions are scaffolding. We'll take them down, one at a time, until we have
a fully-operational scheduling discipline. Like a Death Star, but for CPUs.

*Visual idea:* Five padlock icons in a column, each with a one-line assumption. The fifth wobbles when
the Student questions it. They stay in a corner strip for the rest of the episode and open one by one.

### B04 — How good is a schedule?  `build-up` (~0:45)
**Narrator (V.O.):** To compare policies, we need a **scheduling metric**: a number that *measures*
how well a schedule does. For now, we'll use exactly one. **Turnaround time**. It's the time at which
a job completes, minus the time at which it arrived.

*MathTex on screen:* T_turnaround = T_completion − T_arrival

**Narrator (V.O.):** Since we've assumed every job arrives at time zero, turnaround is just completion
time. That fact will change when we relax the assumptions.

**Professor** (explaining): Turnaround is a *performance* metric. The other big family is **fairness**.
And the two tend to fight: a scheduler can maximize performance by starving a few jobs, which isn't
fair at all.

*Visual idea:* A stopwatch starts at a job's arrival and stops at its completion, with a bracket
labeled "turnaround". Then the formula writes in. A small "performance vs fairness" balance tilts.

### B05 — First In, First Out  `build-up` (~0:40)
**Narrator (V.O.):** The simplest policy imaginable: **First In, First Out**, FIFO, also called First
Come, First Served. Whoever arrives first runs first. It's simple, so it's easy to build, and with our
assumptions it works pretty well.

**Narrator (V.O.):** Three jobs, A, B and C. They all arrive together, but A arrived a hair before B,
and B a hair before C. Each needs ten seconds. A finishes at ten. B at twenty. C at thirty. Average
turnaround time: ten plus twenty plus thirty, over three. Twenty seconds.

*Visual idea:* Timeline (Figure 7.1): A, B, C, 10 s each; completion markers drop at 10, 20 and 30,
and the running average computes to 20.

### B06 — The convoy  `build-up` (~0:50)
**Student** (curious): Okay, but I bet there's a catch. What if the jobs aren't all the same length?

**Narrator (V.O.):** That's the first assumption going away. Same three jobs, but now A needs a hundred
seconds, and B and C need ten each. A is first in line, so A runs for a full hundred seconds. Then B
finishes at a hundred and ten. C at a hundred and twenty. The average: a hundred and ten seconds. Ouch.

**Narrator (V.O.):** This is the **convoy effect**: short consumers of a resource get stuck behind a
heavyweight one. It's your supermarket line again.

**Student** (excited): Just let B and C go first!

**Professor** (happy): Hold that thought.

*Visual idea:* Same Timeline (Figure 7.2) with a long coral A block and two tiny B, C blocks behind it.
The completion markers fall at 100, 110, 120; average readout "110 s" in red. Cross-fade to the
supermarket line from B01 with A as the cart family. Padlock 1 opens.

### B07 — Shortest Job First  `build-up` (~0:50)
**Narrator (V.O.):** That's exactly the next policy. **Shortest Job First**, SJF. Run the shortest job
first, then the next shortest, and so on.

**Narrator (V.O.):** Same three jobs. B finishes at ten. C at twenty. A at a hundred and twenty. Average
turnaround: fifty seconds. Same jobs, same work, and we cut the average by more than half just by
changing the order.

**Professor** (explaining): And if all jobs arrive together, SJF is provably optimal. We're in a systems
class, so we'll skip the proof. But the supermarket got there first: that's the "ten items or less" lane.

*Visual idea:* The Timeline blocks swap places (Transform): B, C, then A. Completion markers at 10, 20,
120; the average readout counts down from 110 to 50. A Tip card slides in: "Shortest job first: the
perceived time per customer matters" with a mini checkout lane sign. Padlock 1 stays open.

### B08 — Late arrivals  `build-up` (~0:50)
**Student** (curious): But what if everything doesn't arrive at once?

**Narrator (V.O.):** Right. The second assumption goes next. Now A arrives at time zero and needs a
hundred seconds. B and C arrive at time ten, and each needs ten.

**Narrator (V.O.):** SJF starts A, the only job it has. When B and C show up, A is already running, and
SJF never interrupts. So they wait until A finishes at a hundred. B finishes at a hundred and ten, and
C at a hundred and twenty. But their *turnaround* counts from their arrival at ten. So that's a hundred,
a hundred, and a hundred and ten. Average: a hundred and three point three three seconds. The convoy is back.

**Professor** (worried): The problem is that SJF is **non-preemptive**: it runs each job to completion
before it even considers another.

*Visual idea:* Timeline (Figure 7.4) with an arrow "[B, C arrive]" at t = 10; A's block keeps going.
Turnaround bars start at each arrival time, so B's and C's bars are 100 and 110 long, not 110 and 120.
Readout "103.33 s". Padlock 2 opens.

### B09 — Stopping a job mid-way  `build-up` (~0:50)
**Narrator (V.O.):** To fix this, we relax the third assumption: jobs don't have to run to completion.
The scheduler can stop A, run something else, and come back later. That's **preemption**. Old batch
systems were non-preemptive. Virtually every modern scheduler is **preemptive**, and it uses exactly the
machinery we built last time: the timer interrupt and the context switch.

**Narrator (V.O.):** Add preemption to SJF and you get **Shortest Time-to-Completion First**, STCF
(also called PSJF). Whenever a new job arrives, run whichever job has the *least time left*.

**Narrator (V.O.):** B and C arrive at ten. A has ninety seconds left. So A is preempted. B runs, then
C, then A finishes. Completions: one-twenty, twenty, thirty. Turnarounds: one-twenty, ten, and twenty.
Average: fifty seconds. And given our assumptions, STCF is provably optimal.

*Visual idea:* An Aside card "Preemptive schedulers" (the context switch gears from 06 appear). Then the
Timeline (Figure 7.5): A runs 0–10, B and C slide in at 10, A's block is interrupted and its remaining
bar waits beside the CPU; B 10–20, C 20–30, A 30–120. Readout "50 s". Padlock 3 opens.

### B10 — A new metric: response time  `build-up` (~0:50)
**Narrator (V.O.):** If all we cared about were batch jobs, we'd be done. But then came time-shared
machines, and people sitting at terminals, typing. Now they care about something else: how long until
the computer *responds*. That's **response time**: the time from when a job arrives to the first time it
runs.

*MathTex on screen:* T_response = T_firstrun − T_arrival

**Narrator (V.O.):** Look at SJF with three jobs of five seconds each. A runs first and responds at zero.
B waits five. C waits ten. Average response time: five seconds. Imagine typing a character and waiting
ten seconds because other jobs got in front.

**Student** (sad): That's a terrible terminal.

**Professor** (explaining): SJF, STCF, and their relatives are great for turnaround and bad for response.
So we need a new policy.

*Visual idea:* A Terminal with a cursor; the Student types a key and a stopwatch counts to 10 s before
the echo appears. Then the Timeline (Figure 7.6): A, B, C of five seconds with first-run markers at 0,
5, 10, and the response brackets in a different color than the turnaround brackets. Readout "response
avg: 5 s".

### B11 — Round Robin  `build-up` (~1:05)
**Narrator (V.O.):** Here's the idea. Instead of running jobs to completion, run one for a short
**time slice** (the book also calls it a **scheduling quantum**), then switch to the next job in the
queue, and the next, round and round until every job is done. This is **Round Robin**.

**Narrator (V.O.):** Same three five-second jobs, with a one-second slice. A, B, C, A, B, C. A runs
first, B second, C third, all within three seconds. Response times: zero, one, and two. Average: one
second. Down from five.

**Student** (curious): So make the slice really, really short?

**Professor** (worried): Careful. Every switch costs time. The time slice has to be a multiple of the
timer-interrupt period. If the timer fires every ten milliseconds, the slice is ten, twenty, any
multiple of ten.

**Narrator (V.O.):** And if a switch costs one millisecond and the slice is ten, then ten percent of the
time is wasted. Make the slice a hundred, and the waste falls under one percent. That's **amortization**:
if an operation has a fixed cost, do it less often. The cost of a switch is also more than saving
registers. The caches and other hardware state have to be warmed up all over again.

*Visual idea:* Timeline (Figure 7.7) with 15 thin one-second slices A B C A B C…; response brackets
at 0, 1, 2; readout "response avg: 1 s". Then a Queue with the ready jobs and a time-slice clock sweeping
as the spotlight rotates. A Tip card "Amortization": a bar with a red sliver for the switch (1 ms) next
to a 10 ms slice (10 %), then a 100 ms slice (under 1 %). Padlock stays.

### B12 — You can't have your cake and eat it  `build-up` (~0:45)
**Narrator (V.O.):** So Round Robin is great at response time. Now check its turnaround, with the same
three jobs. A finishes at thirteen. B at fourteen. C at fifteen. Average: fourteen seconds. SJF would have
given ten (five, ten and fifteen). RR is one of the *worst* policies for turnaround, even worse than FIFO in many cases. It stretches
every job out as long as it can.

**Student** (confused): So which one is right?

**Professor** (happy): Neither. That's a **trade-off**. A policy that divides the CPU evenly (a *fair*
one) does badly on turnaround. A policy that runs short jobs to completion does well on turnaround, but
makes others wait. You can't have your cake and eat it too.

*Visual idea:* Same Timeline, RR coloring; completion markers at 13, 14, 15 and the readout "turnaround
avg: 14 s" in red, next to the SJF's "10 s". A two-column scoreboard: SJF/STCF (turnaround good,
response bad) and RR (response good, turnaround bad), with a see-saw between them.

### B13 — When jobs wait on the disk  `build-up` (~1:05)
**Narrator (V.O.):** Now the fourth assumption. Real jobs do I/O. When a job asks the disk for data,
it's **blocked**, so the scheduler has to run someone else. And when the I/O completes, there's another
decision.

**Narrator (V.O.):** Two jobs, A and B, each need fifty milliseconds of CPU. But A computes for ten,
then does a ten-millisecond I/O, over and over. B just computes for fifty. Using STCF, what should the
scheduler do?

**Narrator (V.O.):** The trick: treat each ten-millisecond burst of A as its own little *job*. When the
system starts, the shortest job is A's first burst. It runs. Then A goes to the disk and B takes over.
When A's I/O completes, a new short job appears. It preempts B, runs ten milliseconds, then B returns.
Back and forth.

**Narrator (V.O.):** This is **overlap**: while A waits on the disk, B uses the CPU. Everyone finishes
sooner than if we ran A, waited, ran A, waited, and only *then* ran B.

**Student** (excited): So interactive jobs run often, and the CPU hogs fill the gaps!

*Visual idea:* Timeline with two lanes, CPU and Disk (Figure 7.8): A, disk, A, disk… then B alone for
50 ms; the CPU lane has idle gaps. Rewind. Figure 7.9: A and B alternate on the CPU while A's I/O fills
the disk lane; no gaps. Tip card "Overlap enables higher utilization". Padlock 4 opens.

### B14 — No more oracle  `build-up` (~0:35)
**Narrator (V.O.):** One padlock left: the OS knows how long each job will run. We said this was the
worst assumption, and it is. Both SJF and STCF need to know job lengths before running them. In a
general-purpose OS, the system usually knows very little about how long a program will run.

**Student** (confused): So the best schedulers we found can't actually be built?

**Professor** (thinking): Not as they stand. How do we behave like SJF without that knowledge? And how
do we keep response time good, like Round Robin? Keep that question.

*Visual idea:* The fifth padlock; the Timeline for STCF is overlaid with a crystal-ball icon that cracks
(the oracle). The padlock does not open. "?" over the next job in the Queue.

### B15 — Big picture and recap  `recap` (~0:45)
**Narrator (V.O.):** Let's step back. We started with a supermarket line and built four policies. FIFO is
simple but suffers from the convoy effect. SJF fixes that for jobs that arrive together. STCF fixes it
when they don't, using preemption. And Round Robin gives up turnaround to win on response time. Two
metrics, and no policy wins both.

**Narrator (V.O.):** So, today:
1. A **policy** decides *which* process runs next, and we compare policies using **metrics**.
2. **Turnaround time** measures completion; **response time** measures how soon a job first runs.
3. FIFO, SJF and STCF are good for turnaround; SJF and STCF fix the convoy.
4. **Round Robin** is good for response time and bad for turnaround. That's a fundamental trade-off.
5. Overlapping I/O with computation raises utilization, but the OS can't see the future.

*Visual idea:* A summary scoreboard table: rows FIFO / SJF / STCF / RR, columns turnaround and response
with a green or red mark (the numbers from the examples). Then a five-item recap list with the
episode's icons. The Professor and Student react in the corners.

### B16 — Teaser  `teaser` (~0:20)
**Student** (curious): So how does a real scheduler decide, if it can't see the future?

**Professor** (happy): By watching the recent past. If a job has been short so far, it's probably short
again. That idea has a name: the multi-level feedback queue.

*Visual idea:* A staircase of queues with a process hopping between them, then cut to black with "Next:
08 · The Multi-Level Feedback Queue".

## Cut / deferred material
- **Homework (scheduler.py simulation):** cut from the video. It could become an on-screen "try it
  yourself" link at the end.
- **References** (Cobham on SJF, Kleinrock on RR, Coffman/Kleinrock on scheduling, Jain, Orwell, Mogul/Borg
  on cache effects): cut. The *Animal Farm* nod, the Wikipedia cake saying, and the Italian proverb are
  cut.
- **Jain's Fairness Index:** mentioned by name only, with no formula.
- **Provability of SJF/STCF optimality:** stated, proof omitted (as in the book).
- **Footnote 3 (alternative definition of response time):** skipped.
- **Worst-case RR response-time equation (homework question 7):** skipped.
- **Predicting the future (MLFQ):** deferred to 08. Lottery/proportional share to 09, multi-CPU to 10.

## Callbacks & setups
- Callbacks to earlier episodes:
  - Policy vs. mechanism, the spotlight and gear icons, and "was that a good scheduling choice?" (04).
  - The Timeline with the standard state encoding (04).
  - The ready Queue (04) and blocked = waiting on I/O (04).
  - The context switch and the timer interrupt, as the machinery that makes preemption possible and that sets the minimum time slice (06).
  - The video-game save slot may be shown as the cost of a switch (04/06).
- Setups paid off in later episodes:
  - "Use the recent past to predict the future" → MLFQ (08).
  - Fairness as a goal rather than a side effect → lottery scheduling (09).
  - "All of this on one CPU" → multi-CPU scheduling (10).

## Open questions
- **Length:** ~13:45 is at the long end of the 8–15 min range (the chapter is number-heavy). B08 and B09 could be merged, or B13 trimmed, to land nearer 12 min.
- **Grocery store cold open:** my own framing; the book only uses it as a tip (the "ten items or less"
  line) and as a footnote joke. I use it in B01 and B07. Keep it?
- **Padlocks for the five assumptions:** my visual device. Keep, or just a plain list?
- **Metric readouts:** each timeline shows a running average. I added "turnaround" in bracket-style bars
  and "response" in a different color. OK?
- **Time units:** the book says "seconds" for the first examples and "milliseconds" for I/O. I keep
  both as-is. Fine, or unify?
