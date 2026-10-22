# 09 — Scheduling: Proportional Share
> Section: Virtualization · Source: Ostep/Chapters/09-cpu-sched-lottery.pdf · Est. duration: ~14:00 (~2,000 spoken words ≈ 13:20 of narration, plus pauses)

## Logline
Every scheduler so far optimized a number: turnaround time, response time. But what if you just want to *promise* each program a slice of the CPU, say 75% and 25%? This episode shows three ways to keep that promise: a raffle (**lottery scheduling**), a clockwork version of it (**stride scheduling**), and the scheduler that ran Linux for years (**CFS**).

## Learning goals
- After watching, the viewer can explain what a **proportional-share** scheduler promises, and how **tickets** represent a share.
- Trace a lottery decision by walking the process list with a running counter, and explain why the result is only *probabilistically* fair.
- Compute **stride** values and **pass** values, and explain how stride scheduling hits the proportions exactly.
- Explain how Linux's **CFS** uses **vruntime**, **sched_latency**, **min_granularity** and **nice** weights to share the CPU.
- Say why CFS keeps runnable processes in a **red-black tree**, and what it does to a process that wakes from a long sleep.

## Concepts covered
| Term | Definition (book's wording or faithful paraphrase) | Beat |
|---|---|---|
| Proportional-share (fair-share) scheduler | Instead of optimizing turnaround or response time, try to guarantee that each job gets a certain percentage of CPU time. | B01 |
| Lottery scheduling | Every so often, hold a lottery to decide which process runs next; processes that should run more often get more chances to win. | B01, B03 |
| Ticket | Represents the share of a resource a process should receive; the percent of tickets a process holds is its share. | B03 |
| Randomness (as a tool) | Avoids corner-case behavior, needs almost no state, and is fast. | B03 |
| Ticket currency | A user allocates tickets among their own jobs in any currency they like; the system converts to the global currency. | B04 |
| Ticket transfer | A process temporarily hands its tickets to another (e.g. client to server). | B04 |
| Ticket inflation | A process temporarily raises or lowers its own ticket count; only sensible among mutually trusting processes. | B04 |
| Lottery implementation | A list of jobs, a total ticket count, a random winner, and a counter that walks the list until it exceeds the winner. | B05 |
| Fairness metric F | Time the first job completes divided by the time the second completes; 1 is perfectly fair. | B06 |
| Ticket-assignment problem | How many tickets should each job get? Open. | B07 |
| Stride scheduling | A deterministic fair-share scheduler: each job has a stride inversely proportional to its tickets and a pass value; always run the job with the lowest pass. | B08 |
| Completely Fair Scheduler (CFS) | Linux's fair-share scheduler, built to be efficient and scalable. | B10 |
| Virtual runtime (vruntime) | Per-process counter of accumulated run time; CFS always picks the lowest. | B10 |
| sched_latency | Period over which CFS tries to be fair (typically 48 ms); divided by the number of processes to get the time slice. | B11 |
| min_granularity | Lower bound on the time slice (typically 6 ms), so context switching doesn't dominate. | B11 |
| Nice / weight | Priority from -20 to +19 (default 0), mapped through a table to a weight that scales time slices and vruntime growth. | B12 |
| Red-black tree | A balanced tree where insert and delete are logarithmic; CFS keeps runnable processes ordered by vruntime in it. | B13 |
| Waking from sleep | On wake-up, CFS sets the process's vruntime to the minimum in the tree, preventing it from monopolizing the CPU. | B14 |

## Script

### B01 — A promise instead of a metric  `cold open` (~0:50)
**Narrator (V.O.):** Picture a cloud server. Two customers share one CPU. One of them paid for three quarters of the machine. The other paid for one quarter.

**Student** (curious): Easy. Round robin, with a twist.

**Professor** (thinking): Round robin gives everyone the same share. Shortest-job-first promises nothing about shares. And the multi-level feedback queue *guesses* from behavior and hopes for the best.

**Narrator (V.O.):** All of them chase a number: turnaround time, response time. None lets you say, on purpose, "you get seventy-five percent."

**Student** (confused): So what would a scheduler that *keeps* that promise even look like?

**Professor** (happy): Surprisingly, like a raffle.

*Visual idea:* A server rack with a pie chart split 75/25 (coral / mint). Chips for RR, SJF and MLFQ each try to fit into the pie and bounce off with a "?"; a raffle drum rolls in at the end.

### B02 — The Crux  `crux` (~0:20)
> **THE CRUX: HOW TO SHARE THE CPU PROPORTIONALLY**
> How can we design a scheduler to share the CPU proportionally? What are the key mechanisms for doing so? How effective are they?

**Narrator (V.O.):** This kind of scheduler is called **proportional-share**, or sometimes **fair-share**. Instead of minimizing a time, it tries to guarantee that each job gets a certain percentage of the CPU. Let's find out how.

*Visual idea:* Crux card in the Virtualization accent (orange); section badge "09 · Proportional Share" top-left; term highlight "proportional share".

### B03 — Tickets and the lottery  `build-up` (~1:30)
**Narrator (V.O.):** Here's the idea, from a paper by Waldspurger and Weihl. Every so often, hold a lottery to decide who runs next. Processes that deserve more of the CPU get more chances to win. That's **lottery scheduling**.

**Narrator (V.O.):** The thing you hold is a **ticket**. Tickets represent a share. The percent of the tickets you own is the percent of the resource you should get.

**Narrator (V.O.):** Say process A holds seventy-five tickets and process B holds twenty-five. A hundred in total, numbered zero to ninety-nine. A owns zero through seventy-four. B owns seventy-five through ninety-nine. Each time slice, the scheduler picks a winning number, finds its owner, and runs that process.

**Student** (excited): A raffle! Draw a ticket, run the winner!

**Narrator (V.O.):** Let's draw twenty. Sixty-three: A. Eighty-five: B. Seventy: A. Thirty-nine: A. Seventy-six: B. And so on. After twenty slices, A has run sixteen times and B four.

**Student** (confused): Four out of twenty. That's twenty percent, not twenty-five.

**Professor** (explaining): Right. Lottery scheduling is *probabilistically* correct, not guaranteed. The longer the two jobs compete, the closer they get to seventy-five and twenty-five.

*Visual idea:* Two Process creatures A (coral) and B (mint) holding stacks of ticket stubs, 75 and 25, laid out on a number strip 0 to 99. A raffle drum spits out numbers; the matching process hops onto the CPU while a **Timeline** fills slice by slice (20 slices, B getting 4). A "20%" label appears and sits next to the "25%" target.

### B04 — Tip: use randomness  `build-up` (~0:50)
**Student** (frustrated): Hold on. We're letting the OS flip coins? Isn't that sloppy?

**Professor** (happy): It's the most beautiful part. Random buys you three things.

**Narrator (V.O.):** One: no nasty corner cases. Some clever algorithms have a workload that makes them fall apart, like the LRU policy we'll meet in the memory episodes. Random has no such workload. Two: almost no state. A counting scheduler must track every process's CPU use; random only needs each process's tickets. Three: speed, as long as the random number is quick.

*Visual idea:* An Aside/Tip card "TIP: Use randomness" slides in; three short vignettes, one per advantage: a worst-case workload bouncing off a die, a tiny PCB card with a single "tickets" field, a stopwatch.

### B05 — Playing with tickets  `build-up` (~1:20)
**Narrator (V.O.):** The ticket is a flexible tool. The book gives three tricks.

**Narrator (V.O.):** **Ticket currency.** User A has a hundred tickets and two jobs, A1 and A2. She gives each five hundred tickets in *her own* currency. User B has a hundred tickets and one job, B1, with ten of his. The system converts: A1 and A2 become fifty global tickets each, B1 becomes a hundred. Two hundred in total, and the lottery runs on those.

**Narrator (V.O.):** **Ticket transfer.** A client asks a server for help, and lends it its tickets while the server works. The server hands them back when it's done.

**Narrator (V.O.):** **Ticket inflation.** A process raises or lowers its own ticket count. Among strangers that's useless, since a greedy process would print tickets and take over. Among friends, a process that needs the CPU can just say so.

**Student** (curious): So a ticket is a unit of ownership.

**Professor** (proud): Exactly. Need to represent a proportion of anything? Try a ticket.

*Visual idea:* Three small panels in turn. Currency: two user cards with their local ticket counts, arrows converting to global numbers (50, 50, 100). Transfer: a client Process hands a ticket bundle to a server Process, then gets it back. Inflation: a Process's ticket stack grows; a second, greedy one grows absurdly and gets a red "no trust" cross.

### B06 — Implementation: walk the list  `build-up` (~1:30)
**Narrator (V.O.):** How hard is it to build? Barely. You need a good random number generator, a list of processes, and the total number of tickets.

**Narrator (V.O.):** Three jobs. A has a hundred tickets, B has fifty, C has two hundred and fifty. Four hundred in total. Say the random number comes out as three hundred.

**Narrator (V.O.):** Walk the list with a counter. Start at zero. A adds a hundred: the counter is a hundred. Is that more than three hundred? No, keep going. B adds fifty: a hundred and fifty. Still no. C adds two hundred and fifty: four hundred. Now it's more than three hundred. Stop. C wins.

**Student** (excited): It's like laying the tickets end to end on a ruler, and seeing whose stretch the winner lands on!

**Professor** (happy): That's the picture. A tip: sort the list from most tickets to fewest. It doesn't change correctness, but the big holders get found early, so you walk fewer nodes.

*Visual idea:* Adapt Figure 9.1: a Code block of the decision loop (the executing line highlighted by a moving bar) beside a linked list of three job nodes (Job:A Tix:100, Job:B Tix:50, Job:C Tix:250). A counter ticks 0, 100, 150, 400 while a pointer hops node to node. Then the tickets lay out as one 0-to-400 ruler with the 300 marker landing in C's gold stretch.

### B07 — How fair is it?  `build-up` (~1:00)
**Narrator (V.O.):** Let's measure that fairness. Two jobs, same length, a hundred tickets each. Ideally they'd finish at the same time.

**Narrator (V.O.):** The book defines a **fairness metric**: the time the first job finishes, divided by the time the second finishes. Ten and twenty give zero point five. Finishing together gives one: perfectly fair.

**Narrator (V.O.):** Over thirty trials, with jobs from one to a thousand time slices long, the pattern is clear. Short jobs: poor fairness. Only long jobs let the lottery converge.

**Student** (sad): So for short jobs it's kind of unfair. And how many tickets does each job get, anyway?

**Professor** (explaining): The book is honest about that one. It's the **ticket-assignment problem**, and it's still open.

*Visual idea:* Two Timeline rows finishing at 10 and 20, F = 10/20 = 0.5 written as `MathTex`. Then adapt Figure 9.2: a fairness curve (0 to 1, x axis: job length from 1 to 1000, log scale) drawn from 0.5 up toward 1.0. A question-mark card "How many tickets?" hovers beside it.

### B08 — Stride scheduling  `build-up` (~1:50)
**Student** (frustrated): Why use randomness at all, then? Can't we get the proportions exactly right?

**Narrator (V.O.):** Waldspurger asked the same question. His answer is **stride scheduling**: a deterministic fair-share scheduler.

**Narrator (V.O.):** Each job gets a **stride**, which is inversely proportional to its tickets. Take our three jobs: a hundred, fifty and two hundred and fifty tickets. Divide ten thousand by each. A has a stride of one hundred. B, two hundred. C, forty.

**Narrator (V.O.):** Each job also keeps a **pass** value, starting at zero. The rule is simple: run the job with the lowest pass. Then add its stride to its pass.

**Narrator (V.O.):** Everyone starts at zero, so pick A. After its slice, A's pass is a hundred. B and C are lower, so B runs next. B's pass becomes two hundred. Now C is lowest, runs, and goes to forty. C is still lowest. It runs again: eighty. Again: a hundred and twenty. Now A, at a hundred, runs. And so on.

**Narrator (V.O.):** Follow it to the end of the cycle, when all three passes meet at two hundred. C ran five times, A twice, B once. Five, two, one: exactly the ratio of their tickets, two hundred and fifty, a hundred, and fifty.

**Student** (surprised): Exactly. Not "probably". Every time.

**Professor** (proud): Every time. Small stride, large share: the busy ones barely advance on the number line.

*Visual idea:* Three runners (A coral, B mint, C gold) on three lanes of a number line starting at 0; each step is a bar whose length is the stride (A: 100, B: 200, C: 40). The scheduler **Spotlight** always lights the runner farthest behind. Adapt Figure 9.3 as a table filling in row by row while a **Timeline** records who ran (A B C C C A C C ...). At the end all three lanes meet at 200 and a "C ×5 · A ×2 · B ×1" brace appears.

### B09 — So why keep the lottery?  `build-up` (~0:55)
**Student** (curious): Then stride beats lottery, right? Why did we bother with lottery?

**Professor** (explaining): One good reason. Lottery has *no global state*. Watch. In the middle of our stride example, a new job shows up. What should its pass value be?

**Narrator (V.O.):** Zero? Then it's far below everyone and monopolizes the CPU until it catches up. Anything else? You have to decide what. With lottery, a new job just arrives with its tickets. Add them to one global total, and go.

**Student** (excited): Lottery is sloppy but flexible. Stride is exact but fussy.

**Professor** (happy): That's the trade.

*Visual idea:* The stride number line again, with a new runner D (sky) dropping in at 0 and racing ahead alone while the others wait, a red "monopoly" flash. Then the lottery drum: a new ticket stack simply slides in and the total ticks up 400 → 450.

### B10 — Linux CFS: the idea  `build-up` (~1:20)
**Narrator (V.O.):** Now for the real world. For years, Linux used a scheduler with a similar goal, reached in a very different way: the **Completely Fair Scheduler**, or **CFS**.

**Narrator (V.O.):** Its other goal is efficiency. Scheduling steals CPU time from the programs it schedules. In a study of Google's data centers, even after heavy optimization, about five percent of all CPU time went to scheduling. So CFS must decide fast.

**Narrator (V.O.):** Its counter is **virtual runtime**, or **vruntime**. A running process accumulates vruntime, at the same rate as real time. When it's time to choose, CFS picks the process with the *lowest* vruntime.

**Student** (curious): Like stride's pass value?

**Professor** (happy): Same flavor: whoever has had the least goes next.

*Visual idea:* A "scheduling tax" meter: a coin slot labeled "≈5%" siphoning from a CPU. Then four processes, each with a small vruntime meter filling while it runs; a Spotlight picks the emptiest meter.

### B11 — How long is a turn?  `build-up` (~1:20)
**Student** (confused): But when does CFS stop the running process? Every millisecond?

**Narrator (V.O.):** That's the tension. Switch often, and you're fair even over tiny windows, but you pay for every context switch. Switch rarely, and you're efficient, but unfair in the short run.

**Narrator (V.O.):** CFS uses two knobs. First, **sched_latency**, typically forty-eight milliseconds, divided by the number of runnable processes. Four processes: twelve milliseconds each. CFS runs one for twelve, then switches to a process with lower vruntime. Our four take turns. Then two finish, and the other two get twenty-four each.

**Narrator (V.O.):** Ten processes? Forty-eight over ten is four point eight milliseconds: too small. So the second knob, **min_granularity**, typically six milliseconds, says never go below this. Ten processes get six each. Not perfectly fair over forty-eight, but close, and cheap.

*Visual idea:* Adapt Figure 9.4: a Timeline from 0 to 250 ms with processes A, B, C, D (coral, mint, gold, sky). First a "48 ms ÷ 4 = 12 ms" equation, blocks of 12 ms; C and D finish and the remaining two get 24 ms. Then a second Timeline with 10 processes: "48 ÷ 10 = 4.8" is crossed out and replaced by a floor line "min 6 ms". A tiny ticking clock symbol for the timer interrupt.

### B12 — Nice and weights  `build-up` (~1:30)
**Student** (curious): Can I tell CFS that one program matters more? With tickets, I can.

**Narrator (V.O.):** CFS doesn't use tickets. It uses an old UNIX mechanism called **nice**: a value from minus twenty to plus nineteen, default zero. Positive means nicer, so you get less. Negative means higher priority.

**Narrator (V.O.):** CFS maps each nice value to a **weight** with a lookup table. Nice zero is one thousand twenty-four. Nice minus five is three thousand one hundred twenty-one. A process's time slice is its weight over the sum of all weights, times sched_latency.

**Narrator (V.O.):** Try it. A has nice minus five, B has nice zero. A gets about three quarters of forty-eight: thirty-six milliseconds. B gets twelve.

**Narrator (V.O.):** vruntime is scaled too: it grows by real run time times one thousand twenty-four, over the weight. A, being heavier, accumulates vruntime at a third of B's rate, so it keeps winning and runs longer.

**Student** (excited): Heavier means a longer slice *and* a slower meter!

**Professor** (proud): And the table only cares about the *difference* in nice values. Five and ten behave exactly like minus five and zero.

*Visual idea:* A dial "nice −20 … +19" feeding a lookup table; two bars A (weight 3121) and B (1024) fill the 48 ms bar in a 36:12 split, as MathTex shows the time_slice formula with numbers. Two vruntime meters: A's fills at one third of B's speed. Reuse the **Timeline**.

### B13 — Why a red-black tree?  `build-up` (~1:10)
**Narrator (V.O.):** One more efficiency problem. "Pick the lowest vruntime" sounds easy, but servers run thousands of processes, and the choice happens every few milliseconds.

**Student** (curious): Keep a sorted list. The lowest is at the front.

**Narrator (V.O.):** Taking the first is quick. But after it runs, its vruntime grows, and it must be re-inserted in order. With vruntimes one, five, nine, ten, fourteen, eighteen, seventeen, twenty-one, twenty-two and twenty-four, that means scanning the list: linear time. Terrible at a thousand processes.

**Narrator (V.O.):** CFS uses a **red-black tree**, ordered by vruntime. It's *balanced*: it does a little extra work on each insert to stay shallow, so find, insert and delete are all logarithmic. And only runnable processes live in the tree. A sleeper is removed.

**Professor** (explaining): Knowing which data structure fits is a hallmark of good engineering. A list was fine once. At this scale, it isn't.

*Visual idea:* Adapt Figure 9.5: a red-black tree with ten nodes (1, 5, 9, 10, 14, 17, 18, 21, 22, 24), black and red nodes. Compare with a plain sorted list: a pointer scans along the list to re-insert a node (counter "n steps"), then the same insert in the tree takes about 3 hops (counter "log n"). A sleeping process (blocked, with a clock) is lifted out of the tree.

### B14 — The sleeper problem  `build-up` (~0:55)
**Narrator (V.O.):** One last trap. A runs all the time. B sleeps for ten seconds. When B wakes, its vruntime is ten seconds behind A's.

**Student** (surprised): So B hogs the CPU for ten seconds while A starves!

**Narrator (V.O.):** It would. So when a job wakes, CFS sets its vruntime to the minimum in the tree. No monopoly. The price: jobs that sleep for short periods, again and again, never get their fair share.

*Visual idea:* A's vruntime meter climbing while B's is parked 10 s behind; B wakes, the gap glows red; the meter jumps up to the tree's minimum. A small "cost" tag: "short sleepers lose out".

### B15 — The big picture  `big picture` (~0:55)
**Narrator (V.O.):** Let's step back. Lottery shares the CPU by random draw. Stride does it deterministically. CFS does it with vruntime, weights and a tree, built for efficiency at scale.

**Student** (confused): So these are the best schedulers? Why did we bother with MLFQ?

**Professor** (worried): No scheduler is a panacea. These don't mesh well with I/O: a job that sleeps often misses its share. And they leave a hard question open: how many tickets, or which nice value, should your text editor get? MLFQ-style schedulers handle that automatically.

**Narrator (V.O.):** Still, in many domains that isn't the main worry. In a cloud data center, you might give a quarter of the CPU to a Windows VM and the rest to your Linux install. Proportional share is simple and effective there. And Linux keeps changing: since version 6.6, its default is a scheduler called EEVDF. Just when you thought you were done.

*Visual idea:* The three approaches as three columns (lottery drum, stride number line, CFS tree) in the same 75/25 pie from the cold open, now filled in. Then a cloud icon with VMs: a 25/75 pie around a CPU. An ep tag "Linux 6.6 → EEVDF" in the corner.

### B16 — Recap  `recap` (~0:35)
**Narrator (V.O.):** So, today:
1. A **proportional-share** scheduler promises each job a *share*, instead of minimizing a time.
2. **Lottery scheduling** uses **tickets** and a random draw. Simple, cheap, and fair in the long run.
3. **Stride scheduling** uses strides and pass values to get the shares exactly right.
4. **CFS** runs the process with the lowest **vruntime**, with a time slice from sched_latency, bounded by min_granularity, and scaled by nice weights.
5. CFS keeps runnable processes in a **red-black tree**, so finding the next one is fast even with thousands.

*Visual idea:* Five-item recap list, each with a tiny icon: pie, raffle drum, stride bar, vruntime meter, tree.

### B17 — Teaser  `teaser` (~0:30)
**Student** (curious): Everything so far has been about one CPU. My laptop has eight. What changes?

**Professor** (worried): Quite a lot, I'm afraid. Caches, locks, and one queue that eight CPUs all want to touch at once...

**Student** (surprised): Uh oh.

*Visual idea:* The single CPU splits into four chips sharing one Queue; processes crowd the queue and reach for it from every side. Cut to black with "Next: 10 · Multi-CPU Scheduling".

## Cut / deferred material
- **Homework (lottery.py simulation):** cut. It could become an on-screen "try it yourself" link.
- **Footnote on counting from zero (Dijkstra):** cut, apart from the ticket numbers running 0 to 99.
- **Footnote on getting an unbiased random number in a range:** cut.
- **Most of the weight table:** only the entries for nice 0 and -5 are shown, plus a glimpse of the table's shape.
- **"Other CFS fun"** (cache-aware heuristics, multi-CPU strategies, scheduling groups of processes): one line at most. Multi-CPU is episode 10.
- **EEVDF:** a single mention in the big picture.
- **Ticket transfer / inflation:** one short demo each, no deeper discussion.
- **References** (Waldspurger, Kanev et al., Jones on CFS, Bouron et al., Zijlstra on EEVDF): cut. Waldspurger and Weihl are credited in narration.

## Callbacks & setups
- Callbacks to earlier episodes:
  - **04 The Process:** the Timeline, ready Queue, and the idea of a scheduling **policy** ("which").
  - **07 CPU Scheduling:** turnaround and response time, RR and SJF as schedulers that chase a number (B01); RR as the base CFS extends (B11).
  - **08 MLFQ:** "guesses from behavior" (B01), and the book's own back-reference in the summary (B15).
  - **Peach / resource-sharing metaphor** (01–03): optional, in the cloud-VM image (B15).
- Setups paid off later:
  - LRU's worst-case workload (B04) → swapping policies (22).
  - Hypervisor / VM cloud share (B15) → virtual memory and hypervisors later in the series.
  - Per-CPU queues and locking (B17) → Multi-CPU scheduling (10), and later concurrency (26+).

## Open questions
- **Length:** ~14 min is at the long end of the 8–15 min target (the chapter has three big topics). B05 (ticket mechanisms) and B14 (the sleeper problem) could be shortened if you'd like ~10 min.
- **Weights in B12:** the table's other values are skipped. OK, or show a "peek at the table"?
- **Stride cycle in B08:** the book's Figure 9.3 ends at "all passes = 200" after 8 listed rows; the narration summarizes the full cycle as C×5, A×2, B×1 (eight slices, matching 250:100:50). Confirm that's the level of detail wanted.
- **Teaser:** the book never mentions multi-CPU in this chapter; the hook (B17) is my bridge to episode 10.
- **User naming in B05:** the book names users "A" and "B" and jobs A1, A2, B1. These clash with Process A and B colors. I suggest drawing users as neutral cards and the jobs as small coral/mint chips.
