# 01–03 — Overview: What Is an Operating System?
> Section: Intro · Source: Ostep/Chapters/01-dialogue-threeeasy.pdf, 02-intro.pdf, 03-dialogue-virtualization.pdf · Est. duration: ~14:00 (1,870 spoken words ≈ 12:30 of narration, plus pauses)

## Logline
A program just fetches and runs instructions, one after another. So who lets dozens of programs share
one CPU, one memory and one disk without stepping on each other? This pilot introduces the
operating system and the series' three big ideas, **virtualization**, **concurrency** and
**persistence**, through four tiny programs that behave in surprising ways.

## Learning goals
- After watching, the viewer can say what an **operating system** is and why it exists (to make the machine easy to use, correctly and efficiently).
- Explain **virtualization** (physical → virtual) using the CPU and memory demos.
- Describe why **concurrency** is hard, from the shared-counter demo.
- Explain why we need **persistence** and what the **file system** does.
- Name the OS's design goals, and the historical idea of **system calls** and **user/kernel mode**.

## Concepts covered
| Term | Definition (book's wording or faithful paraphrase) | Beat |
|---|---|---|
| Three easy pieces | The book's three key ideas: virtualization, concurrency, persistence. | B01 |
| Fetch, decode, execute / Von Neumann model | The processor fetches an instruction from memory, figures out which it is, does it, and moves on to the next. | B02 |
| Operating system (OS) | The body of software that makes it easy to run programs, lets them share memory, interact with devices, and so on, making sure the system operates correctly and efficiently. | B03 |
| Virtualization | Taking a physical resource (processor, memory, disk) and transforming it into a more general, powerful, easy-to-use virtual form of itself. | B03–B04 |
| Virtual machine | Another name for the OS, because of virtualization. | B03 |
| System calls / standard library | The few hundred interfaces the OS exports to applications. | B03 |
| Resource manager | The OS's role of managing the CPU, memory and disk: efficiently, fairly, or toward other goals. | B03 |
| Physical vs virtual (the peach) | One physical resource presented to each user as their own virtual copy. | B04 |
| Virtualizing the CPU | Turning one (or a few) CPUs into a seemingly infinite number, so many programs seem to run at once. | B05 |
| Policy | Answers questions like "which program should run?". | B05 |
| Physical memory | An array of bytes; read by giving an address, written by giving an address and data. | B06 |
| Process identifier (PID) | Unique number per running process. | B06 |
| Virtual address space / virtualizing memory | Each process accesses its own private address space, which the OS maps onto physical memory. | B06 |
| Concurrency, threads | Problems that arise when working on many things at once in the same program; a thread is a function running in the same memory space as other functions. | B07 |
| Atomic | Executed all at once. The counter increment (load, increment, store) isn't. | B07 |
| Persistence, volatile | Storing data so it survives power loss and crashes; DRAM loses data when power goes away. | B08 |
| I/O device, hard drive, SSD | Hardware that stores long-lived information. | B08 |
| File system, files | The OS software that manages the disk and stores the user's files reliably and efficiently. | B08 |
| Device driver | OS code that knows how to deal with a specific device. | B08 |
| Journaling / copy-on-write | Write protocols that let a system recover after a crash during writes (named only). | B08 |
| Abstractions, performance (overheads), protection, isolation, reliability | Design goals of an OS (plus energy efficiency, security, mobility). | B09 |
| Batch processing | Early computing: jobs set up and run in a batch by a human operator. | B10 |
| System call vs procedure call, hardware privilege level, user mode / kernel mode, trap, trap handler, return-from-trap | A system call jumps into the OS while raising the privilege level; it returns with a return-from-trap. | B10 |
| Multiprogramming, memory protection | Loading many jobs and switching rapidly between them to improve CPU utilization, especially while waiting for I/O. | B10 |
| UNIX, shell, pipes | The influential, simple and powerful OS from Bell Labs. | B10 |

## Script

### B01 — A dialogue on the book  `cold open` (~1:40)
**Professor** (happy): Welcome! This is a series about operating systems, based on a book called
*Operating Systems: Three Easy Pieces*. I'm here to teach you what you need to know. I'm called
"Professor". Who are you?

**Student** (excited): Hi, Professor! I'm called "Student", as you might have guessed. And I'm
ready to learn!

**Student** (curious): First question: why *three easy pieces*?

**Professor** (explaining): Richard Feynman gave famous lectures on physics, and some of the basics
were collected in a book called *Six Easy Pieces*. We're doing three easy pieces on operating
systems. Which is fitting, since operating systems are about half as hard as physics.

**Student** (curious): So what are the pieces?

**Professor** (proud): **Virtualization**. **Concurrency**. **Persistence**. Learn those three ideas,
and you learn how an operating system works. How it decides what program runs next on a CPU. How
it copes when memory overflows. How it keeps many things happening at once from tripping over each
other. And how it stores information on disks.

**Student** (confused): I have no idea what you're talking about, really.

**Professor** (happy): Good! That means you're in the right place.

**Student** (curious): And what's the best way to learn this stuff?

**Professor** (explaining): Watch, think, and then *do*. Write real code that solves real problems.
As Confucius said…

**Student** (excited): "I hear and I forget. I see and I remember. I do and I understand." Or
something like that.

**Professor** (surprised): How did you know what I was going to say?!

**Student** (neutral): It seemed to follow. Also, the philosopher Xunzi is actually a
better source for that quote.

**Professor** (happy): Well. I think we're going to get along just fine.

*Visual idea:* Professor (right) and Student (left) face each other on an empty stage. Title card
"Operating Systems: Three Easy Pieces" writes in; three cards slide out labeled
Virtualization (VIRT), Concurrency (CONC), Persistence (PERS) in their accent colors. On
"I hear… I see… I do", three words appear one by one, with "I see" glowing, a nod to the series format.

### B02 — What happens when a program runs?  `build-up` (~0:55)
**Narrator (V.O.):** Let's start at the bottom. What happens when a program runs?

**Narrator (V.O.):** Something very simple. The processor **fetches** an instruction from memory.
It **decodes** it, figuring out which instruction this is. Then it **executes** it: add two
numbers, access memory, check a condition, jump to a function. Then it moves on to the next
instruction. And the next. Millions, these days *billions*, of times per second, until the
program finishes.

**Narrator (V.O.):** That's the **Von Neumann** model of computing. Modern processors play some
wild tricks under the hood to go faster, but they keep up the appearance of exactly this: one
instruction at a time, in order.

**Student** (bored): Sounds simple.

**Professor** (thinking): It is. Until you want to run *more than one* of them.

*Visual idea:* A CPU chip and a Memory column with a short instruction list. A highlight cycles
fetch → decode → execute, moving the program counter down the list, faster and faster until it blurs.

### B03 — Enter the operating system  `crux` (~1:20)
**Narrator (V.O.):** While a program runs, a lot of other things are going on, all with one goal:
making the system **easy to use**. There's a body of software in charge of that. It lets you run
programs, even many at once. It lets programs share memory and talk to devices. That software is
the **operating system**, or **OS**.

**Narrator (V.O.):** Its main technique is called **virtualization**. The OS takes a *physical*
resource, like the processor, memory or a disk, and transforms it into a more general, more
powerful, easier-to-use *virtual* form of itself. That's why the OS is sometimes called a
**virtual machine**.

> **THE CRUX:** How to virtualize resources?
> What mechanisms and policies does the OS use to virtualize? How does it do so efficiently? What
> hardware support is needed?

**Narrator (V.O.):** To let you tell this virtual machine what to do, like run a program, allocate
memory or open a file, the OS offers a few hundred **system calls**. We sometimes say it provides
a **standard library** to applications.

**Narrator (V.O.):** And because many programs share the CPU, the memory and the disks, the OS is
also a **resource manager**. It hands those resources out efficiently and fairly.

**Professor** (explaining): Fun fact: early names for the OS were "the supervisor" and even "the
master control program". The second one sounded a little overzealous, so "operating system" won.

*Visual idea:* A layered stack forms: hardware at the bottom (CPU, Memory, Disk props), the OS as
a band above it (KERNEL_COLOR), and programs (Process creatures) on top. A crux card in neutral
(Intro) color. Three labels attach to the OS band one by one: "virtual machine", "standard
library", "resource manager".

### B04 — The peach  `build-up` (~1:30)
**Student** (curious): But what *is* virtualization, oh noble Professor?

**Professor** (explaining): Imagine we have a peach.

**Student** (confused): A peach?

**Professor** (explaining): A peach. Call it the **physical** peach. Now, many eaters would like to
eat this peach. What we'd like is to give each of them their *own* peach, so they're all happy.
These are **virtual** peaches. We create many virtual peaches out of the one physical peach. The
important part is the illusion: to each eater, it looks like they have a real peach of their own.

**Student** (curious): So you're sharing the peach, and they don't even know it?

**Professor** (happy): Exactly.

**Student** (frustrated): But there's only one peach. If I were sharing a peach, I think I'd notice.

**Professor** (proud): Ah, but most of the time eaters are napping, or doing something else. So you
snatch the peach away and give it to someone else for a while. And so we create the illusion of
many virtual peaches: one for each person!

**Student** (bored): Sounds like a bad campaign slogan. You're talking about computers, right?

**Professor** (happy): Right. Let's take a real one.

*Visual idea:* One physical peach at center (a simple orange-pink circle with a leaf). Four small
eaters around it (Process creatures). Each one gets a translucent "virtual peach" in front of
them. Then reveal: the real peach hops from eater to eater whenever one naps (blocked expression).
This is the series' first Illusion split.

### B05 — Virtualizing the CPU  `build-up` (~1:30)
**Narrator (V.O.):** Here's a tiny program called `cpu`. All it does is wait for one second, print
the word you gave it, and repeat. Forever.

**Narrator (V.O.):** Run it with "A" on a computer with one processor, and every second you get… an
A. Then another A. Not thrilling.

**Narrator (V.O.):** Now let's run *four* of them at once: A, B, C and D. One processor. And yet:
A, B, D, C, A, B, D, C… All four seem to be running at the same time.

**Narrator (V.O.):** That's the peach, for real. The OS, with some help from the hardware, creates
an **illusion**: that the system has a very large number of virtual CPUs. This is
**virtualizing the CPU**, and it's the subject of the next several episodes.

**Narrator (V.O.):** It also raises new questions. If two programs both want to run right now,
*which* one should? Questions like that are answered by a **policy**. Deciding them is the OS's job
as resource manager.

*Visual idea:* A terminal panel with a Code block (Figure 2.1, trimmed to the loop). The output
streams "A". Then four Process creatures labeled A–D appear above a single CPU and take turns on
it while the terminal prints A B D C A B D C in sync. Illusion split: left "4 CPUs?", right "1 CPU".

### B06 — Virtualizing memory  `build-up` (~1:40)
**Narrator (V.O.):** Now memory. Physical memory is simple. It's an array of bytes. To **read**, you
give an address. To **write**, you give an address and the data. Every running program touches
memory constantly, even just to fetch its own instructions.

**Narrator (V.O.):** Here's another tiny program, `mem`. It asks for a little memory with
`malloc()`, prints the address it got, stores a zero there, and then once a second adds one and
prints it. Each line starts with the program's **process identifier**, or **PID**, a number unique
to each running program.

**Narrator (V.O.):** Run it once: the memory is at address `0x200000`, and the value counts 1, 2, 3, 4.

**Narrator (V.O.):** Now run two copies at once. Look at the addresses. *Both* say `0x200000`. The
same address! And yet each one counts up on its own: 1, 1, 2, 2, 3, 3. They never interfere.

**Student** (confused): How can two programs use the same address without overwriting each other?

**Professor** (proud): Because "the same address" isn't the same *place*. Each process gets its own
private **virtual address space**, and the OS maps it onto the real, physical memory. Same address
on the outside, different bytes underneath. That's **virtualizing memory**.

*Visual idea:* Memory column as a strip of cells. Two Process creatures (PID 24113, PID 24114)
each hold a card "p = 0x200000". Each one has its own private Memory column (virtual). Then the
Illusion split: arrows from both virtual 0x200000 cells map to two *different* cells in one
physical Memory column, and the counters tick in parallel.

### B07 — Concurrency  `build-up` (~1:50)
**Narrator (V.O.):** Second piece: **concurrency**. That's the name for a host of problems that
show up when you work on many things at once. The OS itself ran into them first. It's juggling
processes, after all. Today, any **multi-threaded** program meets them too.

**Narrator (V.O.):** A **thread** is like a function running in the same memory as other
functions, with more than one active at a time. This program creates two threads. Each one adds
one to a shared counter, once per loop iteration, and the number of iterations is a command-line argument.

**Narrator (V.O.):** You might want to pause the video here to read the code.

**Narrator (V.O.):** Say we ask for a thousand iterations. Two threads, a thousand each. The final value?

**Student** (excited): Two thousand!

**Narrator (V.O.):** Two thousand. Correct. Now loops equals a hundred thousand. We expect two
hundred thousand… and we get 143,012. Run it again: 137,298. Wrong, and wrong *differently*.

**Student** (frustrated): Huh?? It's the same program!

**Professor** (explaining): Here's why. That one line of C, counter plus plus, looks like a single step, but it isn't one instruction.
The compiler breaks it into several, and the CPU runs them one at a time. Here, it's three: load
the value from memory into a register, add one, store it back. Those three don't happen
**atomically**, all at once. So if the two threads interleave in the middle, one update can
overwrite the other.

> **THE CRUX:** How to build correct concurrent programs?
> When many threads execute concurrently in the same memory space, how can we build a correctly
> working program? What primitives does the OS need to provide, and what does the hardware need to provide?

*Visual idea:* Two thread creatures (smaller Process blobs, same color family) share one memory
cell "counter". Fast-forward counter: 2000 ✓. Then the 100,000 run lands on 143012 with a red
mismatch against 200000. Zoom: load → add → store as three steps per thread; interleave them so
one store visibly overwrites the other (counter goes 5 → 6, 6, not 7). Crux card in CONC cyan.

### B08 — Persistence  `build-up` (~1:40)
**Narrator (V.O.):** Third piece: **persistence**. Memory, the DRAM in your computer, is
**volatile**. Cut the power, or crash, and everything in it is gone. So we need hardware and
software that store data *persistently*.

**Narrator (V.O.):** The hardware is some kind of **I/O device**: a **hard drive**, or more and more
often a **solid-state drive**. The software is the **file system**. It stores the files you create,
reliably and efficiently.

**Narrator (V.O.):** Unlike the CPU and memory, the OS does *not* give each program a private
virtual disk. Files are meant to be **shared**. You write `main.c` in an editor. The compiler reads
it and writes an executable. Then you run that. Three programs, passing files along like a relay.

**Narrator (V.O.):** In code, writing "hello world" to a file is three system calls: `open()`,
`write()`, `close()`. Behind them, the file system figures out where on disk the data goes, keeps
its own bookkeeping, and talks to the device through a **device driver**. And it has to survive a
crash *in the middle* of all that, using tricks like **journaling** or **copy-on-write**.

> **THE CRUX:** How to store data persistently?
> What techniques are needed to manage persistent data correctly, with high performance, and
> reliably in the face of failures in hardware and software?

**Computer** (error): *(the screen flickers off mid-write, then comes back)*

**Student** (surprised): So what happens to my file if it crashes halfway?

**Professor** (happy): Hold that thought for the whole third part of the series.

*Visual idea:* Memory column with values; a power switch flips and the cells fade to empty. A Disk
cylinder in DISK_COLOR keeps its contents. A file icon passes editor → gcc → ./main (relay). io.c
Code block (Figure 2.6, trimmed to open/write/close), each call crossing a line into the OS band
and down to the Disk. Crux card in PERS green.

### B09 — What makes a good OS?  `build-up` (~1:10)
**Narrator (V.O.):** So an OS virtualizes resources, handles concurrency, and stores files
persistently. If we're going to build one, what should we aim for?

**Narrator (V.O.):** First, **abstractions** that make the system easy to use. Abstraction is how
we build anything big in computing. We write C without thinking about assembly, assembly without
thinking about logic gates, gates without thinking about transistors.

**Narrator (V.O.):** Second, **performance**. Virtualization is worth it, but not at any cost. We
want to **minimize the overheads**, in extra time and in extra space.

**Narrator (V.O.):** Third, **protection**. One misbehaving program, malicious or just buggy, must
not harm the others, or the OS itself. The principle behind that is **isolation**.

**Narrator (V.O.):** Fourth, **reliability**. If the OS fails, *everything* fails, so it has to keep
running. Add **energy efficiency**, **security** and **mobility**, and you have a long wish list.

*Visual idea:* A stack of abstraction layers (transistors → gates → assembly → C → programs)
builds up and then collapses into a single "abstraction" badge. Then four goal badges appear in a
row: a stopwatch (performance), walls between Process creatures (protection/isolation), a heartbeat
line (reliability), and a small group (energy, security, mobility).

### B10 — How we got here  `build-up` (~2:20)
**Narrator (V.O.):** These ideas didn't arrive all at once. Engineers learned them the hard way.

**Narrator (V.O.):** In the beginning, the OS was **just a library** of handy routines, like I/O
code, so programmers didn't have to write it themselves. On the old mainframes, one program ran at
a time. A *human operator* decided the order. Jobs were run in a **batch**. Nobody sat at the
machine interactively. It was simply too expensive to let it sit idle.

**Narrator (V.O.):** Then came a realization: code that runs on behalf of the OS is *special*. If
any program could read anywhere on the disk, privacy would be gone. So the **system call** was
invented, pioneered by the Atlas computer. It's not a normal **procedure call**. It jumps into the
OS *and* raises the **hardware privilege level**. Applications run in **user mode**, where the
hardware restricts what they can do: no direct disk I/O, no touching any memory they like. A
special **trap** instruction jumps to a **trap handler** set up by the OS, and switches to
**kernel mode**, with full access to the hardware. When the OS is done, a **return-from-trap**
drops back to user mode, right where the application left off.

**Student** (curious): So programs ask permission, and the OS does the dangerous stuff?

**Professor** (happy): Exactly. Remember that dashed line. We'll cross it a lot.

**Narrator (V.O.):** Next, cheaper **minicomputers** brought **multiprogramming**. Load several jobs,
and switch between them rapidly, especially while one waits for slow I/O. That made **memory
protection** and **concurrency** critical. This era also gave us **UNIX**, from Ken Thompson and
Dennis Ritchie at Bell Labs. It was simple and powerful, built from small programs chained with
**pipes**, and written in the new C language.

**Narrator (V.O.):** Then the **personal computer**. At first it was a great leap *backwards*.
Early systems like DOS had no memory protection, and early Mac OS let one stuck program freeze the
entire machine. Eventually the old lessons returned. macOS has UNIX at its core. Windows NT
adopted the great ideas. Linux, started by Linus Torvalds, runs most of the internet and Android.
Your phone runs an OS far closer to a 1970s minicomputer's than to an early PC's.

*Visual idea:* A horizontal Timeline across eras: mainframe (a queue of punch-card jobs and a
human-operator icon), Atlas (the **User/Kernel boundary** dashed line appears; a Process sends a
trap arrow down across it into the KERNEL_COLOR zone and returns), minicomputer (several Process
creatures swapping on one CPU), UNIX (small boxes connected by pipes: `grep foo file.txt | wc -l`),
PC (one crashing Process scribbles over everyone's memory; Computer error), modern (laptop, server,
phone icons all labeled "UNIX-like ideas").

### B11 — The map  `recap` (~0:50)
**Narrator (V.O.):** So, an operating system is the software that makes a computer easy to use,
correctly and efficiently. Here's our map.

**Narrator (V.O.):**
1. **Virtualization**: one physical CPU and one memory become many virtual ones.
2. **Concurrency**: doing many things at once, correctly.
3. **Persistence**: data that survives power loss and crashes.
4. Along the way: abstraction, performance, protection and reliability, and the user/kernel line
   that makes protection possible.

**Narrator (V.O.):** We won't go deep into networking or graphics. We'll touch on security where the
OS must protect programs and files. But the three pieces are the core.

*Visual idea:* The three piece cards from B01 return, each now with its demo as a thumbnail (cpu
letters, mem counters, threads counter + disk). The dashed user/kernel line runs underneath all three.

### B12 — Into virtualization  `teaser` (~0:45)
**Professor** (happy): And so we reach the first of our three pieces: virtualization.

**Student** (excited): The peach thing! Tell me more. How does it actually *work*?

**Professor** (thinking): In time, young student, in good time. We'll start with the most basic
illusion of all: the CPU. And the thing the OS creates to pull it off: the **process**.

**Student** (sad): I'm a little worried you're going to start talking about peaches again.

**Professor** (happy): Don't worry too much. I don't even like peaches.

*Visual idea:* The peach rolls off-screen. The Virtualization card grows to fill the screen in VIRT
orange. "Next: 04 · The Process".

## Cut / deferred material
- **Homework section** (simulation vs real-code homeworks, the ostep-projects repo): cut. It could be
  a short link in the description.
- **References**: cut.
- **The "dialogues are for thinking" exchange** and "not much of a life outside this book" joke: cut for time.
- **Detailed history asides** (Multics, BSD/Bill Joy, Sun, the UNIX lawsuits, GNU, NeXTStep):
  compressed to one line each, or dropped.
- **Address-space randomization / stack smashing** (footnote): cut (no mention in the episode).
- **"Should be using Emacs"** footnote joke: cut (optional Easter egg on screen).
- Every mechanism mentioned here is deferred to its own episode: scheduling (07–10), address
  translation (15+), threads and locks (26+), file systems (39+), journaling (42).

## Callbacks & setups
- Callbacks: none; this is the series opener.
- Setups paid off later:
  - The **peach** and the **Illusion split** → every virtualization episode (04, 13).
  - `cpu` demo with four processes → 04's cold open and the scheduler episodes.
  - `mem` demo with the same address → 13 (Address Spaces) and 15 (Address Translation).
  - Counter race (143,012) → 26 (Concurrency and Threads) and 28 (Locks).
  - The **User/Kernel boundary** line → 06 (Direct Execution).
  - "What happens to my file if it crashes halfway?" → 42 (FSCK and Journaling).

## Open questions
- **Length:** ~14 min is near the upper limit. If it's too long, B10 (history, ~2:20) could shrink to
  ~1:00, or become a separate bonus short.
- **The Confucius/Xunzi exchange:** kept as the series motto ("I see and I remember"). Keep it, or
  shorten to just the quote?
- **"Operating systems are about half as hard as physics"** and other book jokes are kept almost
  verbatim. Is that the humor level you want throughout?
- **Book attribution:** the Professor names the book in B01. Do you also want an on-screen credit
  (authors and the free URL) at the start or end of each episode?
- **Threads before the threads episode:** B07 shows "thread creatures" as smaller Process blobs.
  There is no Thread character yet. Should we add one to the library now, or reuse Process for now?
