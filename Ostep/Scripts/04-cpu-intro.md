# 04 — The Abstraction: The Process
> Section: Virtualization · Source: Ostep/Chapters/04-cpu-intro.pdf · Est. duration: ~12:00 (1,610 spoken words ≈ 10:45 of narration, plus pauses)

## Logline
Your computer seems to run dozens of programs at once on just a handful of CPUs. How? This episode
introduces the OS's first great trick: the **process**. We cover what it is, how one is born,
the states it moves through, and how the OS keeps track of all of them.

## Learning goals
- After watching, the viewer can explain the difference between a **program** and a **process**.
- Explain how **time sharing** creates the illusion of many CPUs, and what it costs.
- Tell a **mechanism** (*how*) apart from a **policy** (*which*).
- List what makes up a process's **machine state** (address space, registers including PC and stack pointer, open files).
- Describe the steps the OS takes to create a process, and trace a process through the **running / ready / blocked** states.

## Concepts covered
| Term | Definition (book's wording or faithful paraphrase) | Beat |
|---|---|---|
| Process | A running program; the OS's abstraction of a program in execution. | B03 |
| Virtualizing the CPU | Running one process, stopping it, running another, so that many virtual CPUs seem to exist when there is only one (or a few) physical CPU. | B04 |
| Time sharing | Letting a resource be used for a little while by one entity, then by another, and so on. | B04 |
| Space sharing | The counterpart: dividing a resource in space among those who want it (e.g. disk blocks). | B04 |
| Mechanism | Low-level method or protocol that implements a needed piece of functionality; answers *how*. | B05 |
| Context switch | The mechanism that lets the OS stop one program and start running another on a CPU. | B05 |
| Policy / scheduling policy | Algorithm for making a decision in the OS; answers *which* (e.g. which program runs next). | B05 |
| Modularity | Separating policy from mechanism lets you change one without rethinking the other. | B05 |
| Machine state | What a program can read or update while it runs. | B06 |
| Address space | The memory a process can address: its code, its data, its stack, its heap. | B06 |
| Registers, program counter (PC / IP), stack pointer, frame pointer | CPU registers in the process's state; the PC says which instruction runs next; the stack and frame pointers manage the stack (parameters, locals, return addresses). | B06 |
| Process API | Create, destroy, wait, miscellaneous control (suspend/resume), status. | B07 |
| Loading (eager vs lazy) | Reading code and static data from disk (in an executable format) into the address space; all at once (eagerly) or piece by piece as needed (lazily). | B08 |
| Stack / heap | Run-time stack for locals, parameters and return addresses (initialized with `argc`/`argv`); heap for dynamically allocated data (`malloc()` / `free()`). | B08 |
| File descriptors | In UNIX, each process starts with three open: standard input, output and error. | B08 |
| Process states: running, ready, blocked | Executing on a CPU / ready but not chosen / waiting for some event (e.g. I/O). | B09 |
| Scheduled / descheduled | Moved from ready to running / from running to ready. | B09 |
| Scheduler | The part of the OS that makes these decisions. | B11 |
| Process list (task list) | The OS data structure tracking all processes. | B12 |
| Process Control Block (PCB) / process descriptor | The structure holding information about one process. | B12 |
| Register context | Where a stopped process's registers are saved, so they can be restored later. | B12 |
| Initial / final (zombie) state | Being created / exited but not yet cleaned up. | B12 |
| Parent | The process that created another, and can `wait()` for it and read its return code. | B12 |

## Script

### B01 — Too many programs, too few CPUs  `cold open` (~0:50)
**Narrator (V.O.):** Look at your computer right now. A web browser. Music playing. A chat app, a
game in the background, maybe a mail client. Open a task manager and you'll find tens, maybe
hundreds of programs, all running *at the same time*.

**Student** (curious): Okay, sure. That's just… what computers do.

**Professor** (thinking): Is it? Let's open the case and count the CPUs.

**Narrator (V.O.):** One. Maybe four, or eight. Not a hundred. Each CPU can only follow one
stream of instructions at a time. And yet every one of those programs behaves as if it had a CPU
all to itself.

**Student** (confused): So… the computer is lying to us?

**Professor** (proud): Beautifully. And today we learn how.

*Visual idea:* A laptop with app icons swarming out of it; zoom inside to a lone CPU chip. The
**Computer** looks surprised. Counter "programs: 137" vs "CPUs: 1".

### B02 — The Crux  `crux` (~0:20)
> **THE CRUX:** How to provide the illusion of many CPUs?
> Although there are only a few physical CPUs available, how can the OS provide the illusion of a
> nearly-endless supply of said CPUs?

**Narrator (V.O.):** Last time, we watched the OS pull off this trick with four copies of a tiny
program, printing A, B, C and D. Today we find out what it's actually juggling. Answering this
question introduces the most fundamental idea the operating system gives us.

*Visual idea:* Crux card in the Virtualization accent color (orange); section badge "04 · The Process" appears top-left.

### B03 — A program is not a process  `build-up` (~0:55)
**Narrator (V.O.):** First, a distinction. A **program** is a lifeless thing. It's a file on your
disk, a bunch of instructions and maybe some static data. It just sits there, waiting to spring
into action.

**Narrator (V.O.):** Think of sheet music. Sheet music is not a song. Nothing happens until
someone performs it. The operating system is the performer. It takes those bytes and brings them
to life.

**Narrator (V.O.):** That living, running program has a name: a **process**. Informally, that's
the whole definition. *A process is a running program.*

**Student** (curious): So if I open two browser windows…

**Professor** (happy): One program, two performances. Two processes.

*Visual idea:* A grey, still file icon on a Disk; it lifts off, gains color, eyes open and becomes
a **Process** creature (ready). Term highlight: "process". Then a second copy of the same file
becomes a second process with a different color.

### B04 — Taking turns  `build-up` (~1:15)
**Student** (curious): So we have a hundred processes and one CPU. Easy: just buy more CPUs.

**Professor** (worried): One CPU per process? We'd need a hundred chips, then a thousand when you
open more tabs. That doesn't scale.

**Narrator (V.O.):** Here's what the OS does instead. It runs process A for a tiny slice of time.
Then it stops A and runs B. Then C. Then back to A. Each slice lasts only a few milliseconds. To
any human, and in a sense to each program, it looks like they're all running at once.

**Narrator (V.O.):** This is **virtualizing the CPU**: turning one physical CPU into what looks
like many virtual ones. It's our peach again: snatch it from whoever isn't using it, and hand it
to the next eater. The basic technique is called **time sharing**. One resource is used for
a little while by one, then by another.

**Student** (excited): It's like a juggler! Only one ball in the hand at a time, but they're all
in the air.

**Professor** (explaining): Good picture. But notice the price. If three processes share one CPU,
each one runs *slower* than it would alone. Time sharing trades performance for the illusion.

**Narrator (V.O.):** By the way, time sharing has a sibling: **space sharing**. Instead of taking
turns, you split the resource up. Your disk works like this. A block given to one file stays with
that file until the file is deleted.

*Visual idea:* Illusion split: left side shows A, B and C each "on their own CPU"; right side
shows the real single CPU with processes hopping on and off, and a Timeline filling with colored
slices. Small Tip card for space sharing: a disk bar divided into colored blocks.

### B05 — How vs. which  `build-up` (~1:05)
**Student** (confused): Wait, but somebody has to *do* the switching. And somebody has to decide
who's next.

**Professor** (proud): Two different jobs. You've just spotted one of the best design ideas in
operating systems.

**Narrator (V.O.):** The first job is a **mechanism**. That's low-level machinery that answers a
*how* question. *How* do we stop one program and start another? That mechanism is called a
**context switch**, and it gets its own episode later.

**Narrator (V.O.):** The second job is a **policy**. That's an algorithm that answers a *which*
question. Given all the processes that could run, *which* one should run now? That's a
**scheduling policy**. It might look at history (who ran the most in the last minute?), at what
kind of programs these are, or at what we're optimizing for: snappy interaction or total throughput.

**Narrator (V.O.):** Keeping the two apart is a form of **modularity**. You can swap in a smarter
policy without rebuilding the machinery underneath.

*Visual idea:* Screen splits into two labeled panels, "HOW: mechanism" (gears turning, a
process being lifted off the CPU) and "WHICH: policy" (a judge-like pointer choosing from a
Queue of processes). Tip card: "Separate policy and mechanism".

### B06 — What *is* a process, exactly?  `build-up` (~1:30)
**Narrator (V.O.):** "A running program" is a nice slogan. But if the OS is going to stop a process
and resume it later, it needs to know exactly what a process *is*. Here's a good way to think
about it. Suppose we freeze a process mid-step. What would we have to write down to bring it back
perfectly?

**Professor** (explaining): In other words: what parts of the machine can this program read or
change? That's its **machine state**.

**Narrator (V.O.):** First, **memory**. The instructions live in memory. So does the data the
program reads and writes. The memory a process can address is its **address space**.

**Narrator (V.O.):** Second, **registers**. Lots of instructions read and update them directly. A
few are special. The **program counter**, sometimes called the instruction pointer, says which
instruction runs *next*. Lose it and the process forgets where it was. The **stack pointer** and
**frame pointer** keep track of the stack: function parameters, local variables, return addresses.

**Narrator (V.O.):** Third, **I/O information**. Programs talk to storage, so the process
includes things like the list of files it currently has open.

**Student** (excited): So a process is a snapshot: memory, registers, open files. Save those and
you can pause it like a video game!

**Professor** (happy): Exactly the right instinct. Hold on to it. It's the heart of the context
switch.

*Visual idea:* A running Process on the CPU freezes (screen dims, "paused" frame). Three panels
assemble around it: Memory column (code / data / stack / heap), a register bank with PC
highlighted pointing at a line of code, a small "open files" list. They group under a brace:
"machine state".

### B07 — What can you do with a process?  `build-up` (~0:45)
**Narrator (V.O.):** If processes are the thing the OS hands us, then every OS needs a way to work
with them. We'll meet the real API in the next episode. But any operating system offers something
like this.

**Narrator (V.O.):** **Create**: you double-click an icon or type a command, and a new process is
born. **Destroy**: most processes exit on their own, but a runaway one can be killed. **Wait**:
pause until some process finishes. **Miscellaneous control**: for example, suspend a process for a
while, then resume it. And **status**: how long has it run, and what state is it in?

**Student** (bored): That's… a menu.

**Professor** (happy): A very powerful menu. Next episode, we order from it.

*Visual idea:* A five-item menu card; each item gets a tiny demo on a Process creature: pops into
existence, poofs away, a clock while another finishes, a pause/play icon, an info tag.

### B08 — How a process is born  `build-up` (~1:50)
**Student** (curious): Okay, but "create" hides a lot. How does a file on disk actually *become* a
running process?

**Narrator (V.O.):** Step one: **load**. Programs start out on disk, or on a flash-based SSD, in an
**executable format**. The CPU can't run instructions sitting on disk. So the OS reads the code and
static data, like initialized variables, into memory, into the new process's address space.

**Narrator (V.O.):** Early, simple systems did this **eagerly**: everything, all at once, before
running. Modern systems are **lazy**. They load pieces of code and data only when the program
actually needs them. How that works needs paging and swapping, which come later in the series.
For now, just remember that the bits have to get from disk to memory.

**Narrator (V.O.):** Step two: the **stack**. C programs use it for local variables, function
parameters and return addresses. The OS sets aside memory for it, and fills in the arguments to
`main()`: `argc` and the `argv` array.

**Narrator (V.O.):** Step three, maybe: a **heap**. That's for data the program asks for while it
runs, with `malloc()`, and gives back with `free()`. Linked lists, hash tables, trees. It starts
small, and the OS can grow it on request.

**Narrator (V.O.):** Step four: I/O setup. On UNIX, every process starts with three open **file
descriptors**: standard input, standard output, and standard error. That's how a program can read
your keyboard and print to your terminal from line one.

**Narrator (V.O.):** And finally, the OS jumps to the entry point, `main()`, using a special
mechanism we'll see soon, and hands the CPU over to the new process. The performance begins.

**Computer** (happy): *(power LED flickers to green)*

*Visual idea:* Adapt Figure 4.1: Disk at bottom, CPU and Memory above, connected by a bus. Code and
static data stream up from the disk into the Memory column. The stack appears at the bottom with
`argc`/`argv`, the heap appears above the data, three small plugs labeled stdin/stdout/stderr
attach, then an arrow jumps to `main()`. The Process creature opens its eyes and steps onto the CPU.

### B09 — Running, ready, blocked  `build-up` (~1:20)
**Narrator (V.O.):** Once it's alive, a process is always in some **state**. In a simplified view,
there are three.

**Narrator (V.O.):** **Running**: it's on a processor, executing instructions. **Ready**: it could
run right now, but the OS has chosen to run someone else for the moment. **Blocked**: it did
something that means it *can't* run until some event happens. The classic example is asking the
disk for data and waiting for the answer.

**Narrator (V.O.):** The OS moves processes between ready and running whenever it likes. Moving
from ready to running is being **scheduled**. Moving from running back to ready is being
**descheduled**.

**Narrator (V.O.):** A running process that starts an I/O becomes blocked. It stays there until
the I/O completes. Then it goes back to ready, and maybe straight to running again, if the OS
decides so.

**Student** (curious): Why not just let it keep the CPU while it waits?

**Professor** (worried): Because waiting for a disk takes *ages* in CPU time. The CPU would sit
there doing nothing.

*Visual idea:* Adapt Figure 4.2: three circles (Running on the CPU, Ready as a Queue, Blocked as a
waiting area with a clock). A Process walks each arrow as it is named; arrow labels appear:
scheduled, descheduled, I/O: initiate, I/O: done.

### B10 — A trace: CPU only  `build-up` (~0:40)
**Narrator (V.O.):** Let's watch two processes, zero and one, each needing just four ticks of
CPU and no I/O.

**Narrator (V.O.):** Process zero runs for four ticks while process one waits, ready. At tick four,
process zero is done. Process one runs for ticks five to eight. Eight ticks of work, eight ticks
of time. The CPU never idled.

*Visual idea:* Adapt Figure 4.3 as a Timeline (ticks 1–8) with two rows; blocks fill in tick by
tick, colored by state. Process creatures above the CPU swap at tick 5. "CPU busy: 8/8".

### B11 — A trace: with I/O  `build-up` (~1:40)
**Narrator (V.O.):** Now make it interesting. Process zero runs for three ticks, then asks the disk
for something. The I/O will take a few ticks.

**Student** (curious): So… we just wait?

**Narrator (V.O.):** We could. Watch what happens if we do: three ticks where the CPU does nothing.

**Computer** (sleeping): *(snore)*

**Narrator (V.O.):** Instead, the OS notices that process zero is blocked and isn't using the CPU,
so it runs process one. Ticks four, five and six: process one runs while zero waits on the disk.
At tick seven the I/O completes, and process zero moves to ready. Process one finishes at tick
eight. Then process zero runs ticks nine and ten, and is done.

**Computer** (busy): *(LED amber, happily crunching)*

**Narrator (V.O.):** Notice that the OS just made two decisions. First, it switched to process one
during the I/O. That's clearly good: it kept the CPU busy. Second, when the I/O finished, it did
*not* switch back to process zero right away. It let process one finish first. Was that a good
choice?

**Student** (confused): Uh… depends?

**Professor** (happy): That's the right answer more often than you'd think. Decisions like these are
made by the OS's **scheduler**, and we'll spend several episodes on them.

*Visual idea:* Adapt Figure 4.4. First a quick "what if we wait" version where the Timeline shows
grey idle blocks and the Computer falls asleep; rewind (reverse animation); then the real trace,
ticks 1–10, with Process 0 turning blocked (clock icon) at tick 4 and ready at 7. Highlight the two
decision points with question marks.

### B12 — The OS keeps a list  `build-up` (~1:30)
**Narrator (V.O.):** One last question. How does the OS *remember* all this? It's a program too,
and like any program, it keeps data structures.

**Narrator (V.O.):** For each process, it keeps a record. That record is called a **Process
Control Block**, or **PCB** (sometimes a process descriptor). All of those records together form
the **process list**, also called the task list. It's the OS's roll call of every process: who's
ready, who's running, who's blocked and waiting on what, so the right one can be woken when its
I/O completes.

**Narrator (V.O.):** Here's a real one, from a small teaching operating system called xv6. Each
process has an ID, a state, a pointer to its memory, its open files, its parent. And look at this
field: the **register context**. When a process is stopped, its registers get saved right here.
To resume it, the OS loads them back into the real CPU.

**Student** (excited): That's the video-game save slot!

**Professor** (proud): That's the one. Restoring it is the context switch.

**Narrator (V.O.):** Real systems also have a couple more states. There's an **initial** state while
a process is being created. And there's a **final** state, where a process has exited but hasn't
been cleaned up yet. On UNIX that's called the **zombie** state. It sounds spooky, but it's useful.
It lets the process's **parent**, the process that created it, check its return code. Zero usually
means success, anything else means something went wrong. The parent calls `wait()`, reads the
result, and the OS cleans up.

**Student** (surprised): Zombies. In my operating system.

**Professor** (happy): Relatively easy to kill, too. Different techniques are recommended, though.

*Visual idea:* A list of PCB cards, one per Process creature, each with pid, state and color tag;
states update live as processes move. Zoom into one card → a simplified xv6 `struct proc` Code
block (~8 lines), highlight `context`. A Process turns into a grey zombie, its parent Process
"collects" it with `wait()`, and it fades away.

### B13 — Back to the illusion  `big picture` (~0:40)
**Narrator (V.O.):** Let's go back to that laptop with a hundred programs and one CPU. Now we can
see the trick. Each program is a process: memory, registers, open files, written down in a PCB.
The OS keeps them all on a list. It hands the CPU to one, then another, quickly, sliding each
between running, ready and blocked. A low-level mechanism does the switching. A policy decides who
goes next.

**Narrator (V.O.):** Many virtual CPUs. One real one.

*Visual idea:* Pull back to the cold-open laptop, made transparent: inside, the CPU with processes
cycling on and off, the Timeline running, and the process list updating. Illusion split
converges: left and right halves merge.

### B14 — Recap  `recap` (~0:35)
**Narrator (V.O.):** So, today:
1. A **process** is a running program. The OS brings a lifeless program to life.
2. **Time sharing** the CPU creates the illusion of many CPUs, at the cost of performance.
3. Mechanisms answer *how*; policies answer *which*.
4. A process is its machine state: address space, registers, open files.
5. Processes move between **running**, **ready** and **blocked**, and the OS tracks them all in
   the **process list**.

*Visual idea:* Five-item recap list, each with a tiny icon reusing the episode's props.

### B15 — Teaser  `teaser` (~0:25)
**Student** (curious): Okay, I'm convinced processes exist. But how do I actually *make* one? From
my own code?

**Professor** (happy): With three of the strangest and most elegant calls in computing: `fork()`,
`exec()` and `wait()`. A process that clones itself… Next time.

*Visual idea:* A Process creature splits into two identical copies; cut to black with "Next: 05 ·
The Process API".

## Cut / deferred material
- **Homework (process-run.py simulation):** cut from the video. It could become an on-screen
  "try it yourself" link at the end.
- **References** (Brinch Hansen's Nucleus/microkernels, Multics, Hydra, Dennis & Van Horn): cut. A
  one-line nod to history could be added if desired.
- **How the context switch works / how the OS regains control:** deferred to 06 (Direct Execution).
- **Lazy loading via paging and swapping:** mentioned, deferred to the memory episodes (18, 21–22).
- **Scheduling policies:** deferred to 07–10.
- **File descriptors in depth:** deferred to the persistence section (39).
- **Full xv6 `proc` struct and states (UNUSED, EMBRYO, SLEEPING, RUNNABLE…):** shown simplified; the
  mapping of xv6 names to running/ready/blocked is not explained.

## Callbacks & setups
- Callbacks to earlier episodes (01–03 Overview):
  - The `cpu` demo with A, B, C, D (B02).
  - The peach (B04).
  - "Policy" and "resource manager" (B05; re-defined briefly here).
  - The Illusion split motif (B04, B13).
- Setups paid off later:
  - "Video-game save slot" / register context → context switch (06).
  - The two decisions in the I/O trace → scheduler (07+).
  - The `wait()` + zombie + parent idea → the Process API (05).
  - Lazy loading → paging and swapping (18, 21).
  - The **Illusion split** motif → the virtualization of memory (13).

## Open questions
- **Length:** ~12 min is on the long side. B07 (Process API menu) and B12's zombie section could
  be shortened if you'd rather land around 10 min.
- **Analogies:** I used *sheet music vs. performance* (program vs process), a *juggler* (time
  sharing) and a *video-game save slot* (machine state / register context). These are mine, not
  the book's. Keep, swap, or reduce?
- **"Professor (proud)" self-praise** shows up a few times. Is that the tone you want, or should it be rarer?
