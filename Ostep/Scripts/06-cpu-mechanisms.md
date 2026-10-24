# 06 — Mechanism: Limited Direct Execution
> Section: Virtualization · Source: Ostep/Chapters/06-cpu-mechanisms.pdf · Est. duration: ~14:00 (~2,000 spoken words ≈ 13:20 of narration, plus pauses)

## Logline
Time sharing needs two things that pull in opposite directions: programs that run at full speed, and an OS that stays in charge. This episode builds **limited direct execution**: user and kernel mode, system calls, the trap table, the timer interrupt and the context switch, until the OS can let a program run free and still take the CPU back whenever it wants.

## Learning goals
- After watching, the viewer can explain **direct execution**, and why running programs directly creates two problems: restricted operations and switching between processes.
- Describe **user mode** and **kernel mode**, and trace a **system call** through **trap**, **trap table** and **return-from-trap**.
- Explain why the OS cannot regain the CPU by asking nicely, and how the **timer interrupt** solves it (cooperative vs. non-cooperative).
- Walk through a **context switch** step by step: which registers are saved, where, and why `return-from-trap` ends up in a different process.
- State the idea of **limited** direct execution: set up the hardware (trap handlers, timer) at boot, then run processes in a restricted mode.

## Concepts covered
| Term | Definition (book's wording or faithful paraphrase) | Beat |
|---|---|---|
| Direct execution | Just run the program directly on the CPU: create a process entry, allocate memory, load the code, jump to `main()`, and later come back to the kernel. | B03 |
| Limited direct execution (LDE) | Direct execution with limits set up in advance by the OS and the hardware, so the OS keeps control without slowing the program. | B02, B12 |
| Restricted operations | Things like issuing I/O or getting more memory, which a process must not be able to do on its own. | B04 |
| User mode / kernel mode | A restricted processor mode for applications / the privileged mode the OS runs in, with full access to the machine. | B04 |
| Privileged operation | An instruction (e.g. I/O, installing a trap table) that only runs in kernel mode; in user mode it raises an exception and the process is likely killed. | B04, B06 |
| System call | The way a user program asks the kernel to carefully expose key functionality: files, processes, communication, memory. | B05 |
| Trap / return-from-trap | One instruction that jumps into the kernel and raises the privilege level; its counterpart returns to the caller and lowers it again. | B05 |
| Kernel stack | A per-process stack where the hardware saves registers (PC, flags, a few more) on a trap, and restores them on return-from-trap. | B05 |
| Trap table / trap handlers | A table, set up by the OS at boot, telling the hardware which code to run on each event (system call, timer, keyboard…). | B06 |
| System-call number | What the user code puts in a register instead of an address; the kernel checks it and runs the matching code. A form of protection. | B06 |
| Cooperative approach | The OS trusts processes to give up the CPU through system calls (e.g. `yield`) or by doing something illegal. | B08 |
| Timer interrupt | A timer device raises an interrupt every so many milliseconds; the running process is halted and an OS interrupt handler runs. | B09 |
| Non-cooperative approach | The OS takes control with hardware help, whether the process cooperates or not. | B09 |
| Scheduler | The part of the OS that decides whether to keep running the current process or switch. | B10 |
| Context switch | Save a few register values of the running process (onto its kernel stack) and restore a few of the soon-to-run process, so `return-from-trap` resumes the other one. | B10 |
| Disable interrupts / locking | Ways to keep the kernel safe from interrupts that arrive during interrupt handling; a topic for the concurrency section. | B11 |

## Script

### B01 — Just run it  `cold open` (~0:45)
**Student** (curious): Last time I asked how the OS ever gets control back once my program is on the CPU. So let's start simple. What's the simplest way to run a program? Load it, jump to `main()`, and get out of the way?

**Professor** (explaining): That's called direct execution, and it has one huge advantage. It's *fast*. No middleman. The program runs natively on the hardware.

**Student** (excited): Great. Ship it.

**Professor** (worried): Now the program decides to read every file on the disk. Or to scribble over memory that isn't its own. Or just to run `while (1)` until the sun burns out.

**Student** (confused): And the OS does… what, exactly?

**Narrator (V.O.):** Nothing. The OS isn't running. The program is. The OS can only watch from the sidelines.

**Professor** (thinking): An operating system with no control over anything is just a library. A very sad state of affairs for an aspiring operating system.

*Visual idea:* A Process (A) runs happily on the CPU with a green "FAST" gauge. It starts scribbling over a Memory column, then spins in a tight loop. The OS, a small red box, stands to the side and cannot reach the CPU. The Computer is overwhelmed.

### B02 — The Crux  `crux` (~0:35)
> **THE CRUX: HOW TO EFFICIENTLY VIRTUALIZE THE CPU WITH CONTROL**
> The OS must virtualize the CPU in an efficient manner while retaining control over the system. To do so, both hardware and operating-system support will be required.

**Narrator (V.O.):** To virtualize the CPU, the OS has to share it among many processes by time sharing. That raises two challenges, pulling in opposite directions. The first is **performance**: no excessive overhead. The second is **control**: processes must not be able to run forever, or touch what they shouldn't.

**Narrator (V.O.):** The answer is a technique with a long name: **limited direct execution**. *Direct*: run the program on the CPU itself. *Limited*: the guard rails we build now.

*Visual idea:* Crux card in the Virtualization accent. Two arrows, "performance" and "control", pull a process in opposite directions; they merge into the term "limited direct execution" (term highlight).

### B03 — The naive protocol  `build-up` (~1:00)
**Narrator (V.O.):** Here's direct execution as a protocol. The OS creates a process entry, allocates memory, loads the program (that's the work behind `exec()` from last time), sets up the stack, clears the registers, and *calls* `main()`. The program runs, and *returns*. The OS frees the memory and removes the entry.

**Student** (curious): That's just calling a function.

**Professor** (explaining): Exactly, which is why it's so fast. But it raises two problems. One: how do we stop the program from doing what we don't want, while still running it efficiently? Two: how does the OS stop it, to switch to another process?

*Visual idea:* Figure 6.1 as a two-column chart (OS | Program) that fills row by row, with a single arrow call → return. Then two big question marks appear over it, numbered 1 and 2, which become the labels of the next two sections.

### B04 — Problem 1: dangerous instructions  `build-up` (~1:15)
> **THE CRUX: HOW TO PERFORM RESTRICTED OPERATIONS**
> A process must be able to perform I/O and some other restricted operations, but without giving the process complete control over the system. How can the OS and hardware work together to do so?

**Narrator (V.O.):** Which gives us the first question to answer: *How to perform restricted operations?* Problem number one. What if the process wants to do something *restricted*, like reading from the disk?

**Student** (curious): So just let it. It's *its* program.

**Professor** (worried): A file system checks permissions before it opens a file. If any process could talk to the disk directly, it would skip the check, and read or write the whole disk. All protection gone.

**Student** (confused): Then let the OS inspect every instruction before it runs.

**Professor** (thinking): Safe, and slow. We'd throw away the point of direct execution. We want the *hardware* to help.

**Narrator (V.O.):** So the CPU gets two **modes**. In **user mode**, code is restricted: if a process tries to issue an I/O request, the processor raises an exception, and the OS will most likely kill it. In **kernel mode**, where the OS runs, code can do anything, including every privileged operation.

**Narrator (V.O.):** You've met this: the dashed line from our first episode, user above, kernel below, and the gauge that reads which side you're on. Now it goes to work.

*Visual idea:* User/Kernel boundary and Privilege gauge. A Process in the user zone reaches a hand toward a Disk below the line, a wall stops it, a "!" flashes and a red X stamps it (killed). Then a red "OS" token reaches the Disk freely.

### B05 — Knocking on the kernel's door  `build-up` (~1:15)
**Student** (confused): But then how does a program ever read a file?

**Narrator (V.O.):** With a **system call**. System calls let the kernel carefully expose a few key services: the file system, creating and destroying processes, talking to other processes, allocating memory. Real systems offer a few hundred. Early UNIX had about twenty.

**Narrator (V.O.):** To make one, the program runs a special instruction: a **trap**. It jumps into the kernel and raises the privilege level, both at once. Now the OS can do the privileged work, if it allows it. When it's done, a **return-from-trap** goes back to the program and lowers the privilege level.

**Narrator (V.O.):** The hardware must save the caller's registers, to be able to come back. On x86, it pushes the program counter, the flags and a few more onto a per-process **kernel stack**. Return-from-trap pops them off again.

**Student** (curious): When I write `open()` in C, it looks like an ordinary function call.

**Professor** (happy): It is. A call into the C library, which puts the arguments in agreed places, executes the trap, and unpacks the result. Somebody wrote that assembly for you.

*Visual idea:* Process A in the user zone sends a "trap" arrow down across the line (boundary flash, gauge flips to KERNEL). A's registers fly into a kernel stack tray. The OS does its work, then a "return-from-trap" arrow carries A's registers back up (gauge flips to USER).

### B06 — Where does a trap go?  `build-up` (~1:15)
**Student** (curious): Wait. The trap jumps into the kernel. *Which* code? Does the program say?

**Professor** (worried): It must never say. A program that picks any address in the kernel could jump just past a permission check. That's a Very Bad Idea.

**Narrator (V.O.):** So the kernel decides in advance. At boot the machine starts in kernel mode, free to configure the hardware. One of the first things the OS does is install a **trap table**: it tells the hardware what code to run on a disk interrupt, a keyboard interrupt, a system call. Those are the **trap handlers**, and the hardware remembers them until the next reboot. Installing the table is itself a privileged instruction.

**Student** (excited): And if I *could* install my own table?

**Professor** (explaining): Then every trap would run your code, in kernel mode. You'd own the machine.

**Narrator (V.O.):** The program doesn't give an address. It gives a **system-call number**. The handler checks that it's valid and runs the matching code. That indirection is **protection**: user code can only *request* a service. And the kernel stays suspicious even then. A `write()` whose buffer points inside kernel memory must be refused.

*Visual idea:* A "trap table" card in the kernel zone with rows (syscall → handler, timer → handler, keyboard → handler). The user process tries to write its own address on a sticky note and the note bounces off the boundary. The Padlock icon sits on the table. A tip card slides in for the `write()` buffer check.

### B07 — The whole protocol  `build-up` (~1:30)
**Narrator (V.O.):** Let's put it together. Limited direct execution has two phases. At boot, in kernel mode, the OS initializes the trap table, and the hardware remembers the system-call handler.

**Narrator (V.O.):** Then, to run a process, the OS creates the entry, allocates memory, loads the program, sets up the stack. It fills the *kernel stack* with the starting registers, and executes a **return-from-trap**.

**Student** (surprised): A return? From a trap that never happened?

**Professor** (proud): A pretend return. That's the "special mechanism" I promised in episode four, the one that jumps to `main()`. The hardware restores the registers, moves to user mode, and jumps in.

**Narrator (V.O.):** The program runs. When it needs a service, it traps: registers saved, kernel mode, trap handler. The OS does the work, and returns from the trap. The registers come back, user mode returns, and the program continues right after the trap. Finally `main()` returns into `exit()`, one more system call, and the OS cleans up. The program ran directly on the CPU nearly the whole time.

*Visual idea:* Adapt Figure 6.2 as a three-column chart (OS | Hardware | Program) that scrolls downward in time, with a cursor that follows the row being narrated. Alongside, the CPU chip rides up and down across the dashed line, and the gauge flips with it.

### B08 — Problem 2: when the OS isn't running  `build-up` (~1:20)
**Narrator (V.O.):** Problem number two: switching between processes. Sounds simple: just stop one and start another.

**Professor** (thinking): But if a process is running on the CPU, then by definition the OS is *not* running. And if the OS isn't running…

**Student** (confused): …it can't do anything about it.

> **THE CRUX: HOW TO REGAIN CONTROL OF THE CPU**
> How can the operating system regain control of the CPU so that it can switch between processes?

**Narrator (V.O.):** There are two answers. Let's start with the polite one. Early systems, like the first Macintosh, took the **cooperative approach**: the OS *trusts* processes to give up the CPU periodically. And most do, through system calls. Some systems even have an explicit `yield` call that does nothing but hand over the CPU. A process that does something illegal, like dividing by zero, also traps into the OS, which will probably terminate it.

**Student** (curious): And if a program loops forever, and never makes a system call?

**Professor** (worried): Then there's one cure, the oldest in computing: reboot the machine.

**Student** (sad): That's the plan?

**Professor** (neutral): Reboot is more useful than it sounds: it returns the software to a known state, reclaims leaked resources, and is easy to automate.

*Visual idea:* A and B share the CPU. A calls `yield()`; the CPU passes to B (the cooperative case). Then A enters an infinite loop with a loop arrow, B waits ready and a clock ticks, the Computer overwhelmed, a "reboot" power switch flips. A small tip card: "Reboot is useful: known state, reclaims leaked resources, easy to automate."

### B09 — The alarm clock  `build-up` (~1:10)
> **THE CRUX: HOW TO GAIN CONTROL WITHOUT COOPERATION**
> How can the OS gain control of the CPU even if processes are not being cooperative? What can the OS do to ensure a rogue process does not take over the machine?

**Narrator (V.O.):** Which leaves us with a harder question: *How to gain control without cooperation?* The answer was found many years ago, and it's simple: a **timer interrupt**.

**Narrator (V.O.):** A timer device can be programmed to raise an interrupt every few milliseconds. When it fires, the running process is halted, whatever it was doing, and a pre-configured **interrupt handler** in the OS runs. The OS has regained control. It can stop this process and start another.

**Narrator (V.O.):** The OS prepares this at boot, like the system-call handler. It tells the hardware which code to run when the timer fires, and it *starts the timer*, a privileged operation. The hardware does its part too: it saves the running program's state onto the kernel stack, the same dance as a trap, though this time the program never asked.

**Student** (curious): So the process doesn't even notice?

**Professor** (happy): Like a movie paused and played again. This is the **non-cooperative** approach: the OS takes control by force, with hardware help. And a process that misbehaves gets one strike: it's out.

*Visual idea:* The same infinite loop as B08, but now an alarm clock icon on the OS side rings every tick. A flash across the boundary, the gauge flips, A is pulled off the CPU, and the OS token takes the chip. A tip card: "Misbehaving process? One strike and you're out."

### B10 — The context switch  `build-up` (~2:00)
**Narrator (V.O.):** Now the OS is back in control, by a system call or a timer interrupt. It must decide: keep running this process, or switch? That's the job of the **scheduler**, and its policies fill the next episodes.

**Narrator (V.O.):** If the decision is to switch, the OS runs a low-level piece of code: the **context switch**. Remember the save slot from episode four?

**Student** (excited): The video-game save! Pause one, load the other!

**Professor** (proud): Exactly. Save a few registers of the running process, restore a few of the next one. Then return-from-trap doesn't go back to the process that was interrupted. It goes into the *other* one.

**Narrator (V.O.):** Watch it with A and B. A is running. The timer fires. The hardware saves A's registers on A's kernel stack and enters the kernel. The handler decides to switch, and calls `switch()`. That routine saves A's current registers into A's process structure, restores B's from B's process structure, and switches the stack, to B's kernel stack.

**Narrator (V.O.):** Then the OS executes return-from-trap. The hardware restores B's registers, moves to user mode, and jumps to B's program counter. B is running.

**Student** (confused): So there are two kinds of saving?

**Professor** (explaining): Yes. When the timer fires, the *hardware* saves the user registers on the kernel stack. When the OS switches, the *software* saves the kernel registers into the process structure. That second save makes the system look as if it trapped into the kernel from B, not from A. We enter `switch()` in A's context and leave it in B's.

**Narrator (V.O.):** In xv6, that's a few lines of x86 assembly: store the registers into the old context, load them from the new one, switch the stack, and `ret`.

*Visual idea:* Adapt Figure 6.3 on the Timeline: A running (coral), timer interrupt, kernel block, B running (mint). The Save slot icon hovers: A's register bank flies into A's slot, B's slot flies into the CPU. Then zoom into a trimmed `swtch` Code block (Figure 6.4) with the stack-switch line highlighted.

### B11 — How long does it take? And what about concurrency?  `build-up` (~0:50)
**Narrator (V.O.):** How long does all this take? In 1996, on a 200-megahertz machine, a system call took about four microseconds, and a context switch about six. Modern systems do almost ten times better. Not everything speeds up with the CPU, though: many OS operations are bound by memory bandwidth.

**Student** (confused): What if a timer interrupt fires *during* a system call?

**Professor** (happy): Good question, and the answer belongs to the whole second piece of this series. One simple trick is to **disable interrupts** while handling one, but not for long, or you lose some. Real kernels also use **locking** to protect their data structures. Concurrency, later.

*Visual idea:* A stopwatch with "4 µs" and "6 µs" (1996) shrinking to "< 1 µs" today. An Aside card. Then a second timer interrupt arrives while the kernel runs; a gate (a small shield) closes in front of it: "disable interrupts"; a tag "→ Concurrency".

### B12 — Baby-proofing the CPU  `big picture` (~0:40)
**Narrator (V.O.):** One more picture to hold onto. This is how the world works, too. When parents baby-proof a room, they lock the cabinets with dangerous things and cover the electrical sockets. Once that's done, the baby can roam freely, and the parents can relax.

**Narrator (V.O.):** The OS baby-proofs the CPU. At boot it sets up the trap handlers and starts the timer. Then it runs processes only in restricted mode, at full speed, and steps in only for privileged operations, or when a process has held the CPU too long.

**Student** (excited): So that's the "limited" in limited direct execution!

**Professor** (proud): That's the "limited."

*Visual idea:* A room (the CPU stage) with a cabinet lock on the Disk, a socket cover on the I/O port, and a timer on the wall, with a Process creature playing happily in the middle. Dissolve into the full diagram: boundary, trap table, timer, kernel stacks.

### B13 — Recap  `recap` (~0:35)
**Narrator (V.O.):** So, today:
1. **Limited direct execution**: run programs directly for speed, within limits set up by the OS and the hardware.
2. **User and kernel mode** protect the machine. Programs reach the kernel only through **system calls**: **trap** in, **return-from-trap** out.
3. The **trap table**, installed at boot, is the only place a trap can go.
4. The **timer interrupt** lets the OS regain control, even from a process that never cooperates.
5. A **context switch** saves one process's registers and restores another's.

*Visual idea:* Five-item recap list with icons: gauge, trap arrow, trap table, alarm clock, save slot.

### B14 — Teaser  `teaser` (~0:25)
**Student** (curious): So the OS can take the CPU back whenever it wants, and swap one process for another. Great. But *when* should it? And *who* should it pick?

**Professor** (happy): Ah. That's no longer a mechanism question. That's a policy question. The machinery is done. Next time we meet the scheduler.

*Visual idea:* A Queue of processes A, B, C; a Spotlight sweeps across them without landing. Cut to black with "Next: 07 · CPU Scheduling".

## Cut / deferred material
- **Homework (measuring system call and context-switch costs, lmbench-style, pipes, `sched_setaffinity`):** cut. Could be a "try it yourself" link at the end.
- **References** (Atlas, Alto, Mac OS 9, lmbench, Microreboot, Intel manuals, return-into-libc): cut. The "Very Bad Idea" footnote (return-oriented programming, S07) is reduced to a half-sentence.
- **x86 specifics** of what the processor pushes (PC, flags, a few more): kept as one sentence.
- **xv6 `swtch` assembly line by line (Figure 6.4):** shown only as a trimmed block with highlights; no instruction-by-instruction explanation.
- **Scheduling decisions (which process to run):** deferred to 07–10.
- **Concurrency during interrupts, locking:** only sketched (B11); full treatment in the concurrency section (26+).
- **`write()` argument checking and other secure-OS caveats:** kept as one short tip; security episodes later.
- **Reboot tip:** kept as a short tip card (B08), not explained in depth.

## Callbacks & setups
- Callbacks to earlier episodes:
  - 05's teaser question, "how does the OS ever get control back?" (B01), and the glass-wall image (the OS watching from behind glass). `exec()` as the loading step (B03).
  - The dashed **User/Kernel boundary** and **Privilege gauge** from 01–03 (B04, B05, B07): finally put to work.
  - "Trap and return-from-trap" terms from 01–03 (B05).
  - The **save slot** / register context and the "video-game save" line from 04 (B10).
  - "Jumps to `main()` using a special mechanism we'll see soon" from 04 (B07): the fake return-from-trap.
  - **Mechanism vs. policy**, and "context switch gets its own episode" from 04 (B10, B14).
  - **Time sharing** and the process states (scheduled / descheduled) from 04 (B02, B10).
  - Process creation steps (create entry, allocate memory, load, stack with argc/argv) from 04 (B03).
- Setups paid off in later episodes:
  - The **scheduler** and its policies → 07–10.
  - **Interrupt handling and locks** (B11) → the concurrency section.
  - **Address translation / memory protection**, the other half of "user programs can't touch what they shouldn't" → memory section (13+, 15+).
  - **Multi-CPU** timers and context switches → 10.

## Open questions
- **Length:** ~14:00 is at the upper end of the 8–15 min target. B10 (context switch, 2:00) and B07 (protocol walk, 1:30) are the heaviest. Should B11 become a short aside, or be cut?
- **Student's "inspect every instruction" objection (B04):** this is my addition, not the book's, to motivate hardware modes. Keep?
- **Analogies:** I reused *save slot* (04) and the book's *baby-proofing*. No new analogy for the trap table beyond the "sticky note with an address" visual. Fine?
- **"Fake return-from-trap" (B07):** the book doesn't use the word "fake", but the first return-from-trap does start a process that never trapped. I flag it as a simplification in the narration. OK?
- **Order of 05:** resolved by the consistency pass. B01 now picks up 05's teaser question, and B03 names `exec()`.
