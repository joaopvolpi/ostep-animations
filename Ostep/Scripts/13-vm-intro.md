# 13 — The Abstraction: Address Spaces
> Section: Virtualization · Source: Ostep/Chapters/13-vm-intro.pdf · Est. duration: ~11:30 (~1,540 spoken words ≈ 10:15 of speech, plus pauses)

## Logline
Every program believes it owns a huge, private memory that starts at address zero. That is a lie, and
this episode shows why the OS needs it: sharing one memory among many programs is useless unless each
one gets an easy, safe picture of its own, the **address space**.

## Learning goals
- After watching, the viewer can explain why early single-program memory was simple, and why multiprogramming and time sharing broke that simplicity.
- Explain why swapping whole memories to disk is too slow, and why processes stay in memory together, which makes **protection** necessary.
- Describe the **address space** of a process (code, heap, stack) and why the heap and the stack sit at opposite ends.
- Explain what it means to **virtualize memory**: a **virtual address** is not where the data really lives (the book's example: virtual 0 is physical 320KB).
- Name the three goals of a VM system: **transparency**, **efficiency**, **protection**, and why every address a programmer ever prints is virtual.

## Concepts covered
| Term | Definition (book's wording or faithful paraphrase) | Beat |
|---|---|---|
| Multiprogramming | Several processes are ready to run at once, and the OS switches between them, for example when one performs an I/O, to raise CPU utilization. | B03 |
| Time sharing | Many users share the machine at once, each wanting a timely (interactive) response from their running tasks. | B04 |
| Protection | One process must not be able to read, or worse write, another process's memory (or the OS's). | B05 |
| Address space | The running program's view of memory: an easy-to-use abstraction of physical memory, holding the program's code, stack and heap. | B06 |
| Stack | Region that keeps track of where the program is in the function call chain; holds local variables, arguments and return values. | B07 |
| Heap | Region for dynamically allocated, user-managed memory (`malloc()` in C, `new` in C++/Java). | B07 |
| Virtual address | The address a program sees, for example a load at address 0. The OS and hardware translate it to a physical address. | B09 |
| Virtualizing memory | The OS (with hardware support) gives a program the illusion of a private, large memory at particular addresses; the reality is different. | B09 |
| Transparency | The virtualization is invisible to the running program; it behaves as if it had its own private physical memory. | B10 |
| Efficiency | Virtualization should be fast (time) and not waste memory on supporting structures (space); hardware support such as TLBs will help. | B11 |
| Isolation (principle) | If two entities are properly isolated, one can fail without affecting the other. | B11 |

## Script

### B01 — The numbers that lie  `cold open` (~0:45)
**Narrator (V.O.):** Write a tiny C program. Print the address of `main`. Print the address of a
variable on the stack. Print a pointer you got from `malloc`. Run it, and out come three big, strange
numbers.

**Narrator (V.O.):** Here is a secret. None of those numbers is real. Every address you have ever
printed from a program is a fiction, a story the operating system tells your program.

**Student** (surprised): The addresses my program prints are *fake*?

**Professor** (happy): "Fake" is harsh. Remember last time: every address a program generates is virtual. Let's say carefully arranged. To see why the OS tells this story, we have to go back to a time when it didn't need to.

*Visual idea:* A Terminal runs `va.c` and prints three hex lines (code, heap, stack). The numbers glow, then crack like glass; a small "lie" stamp. Cut to an empty memory column: "back to the beginning".

### B02 — When memory was easy  `build-up` (~0:50)
**Narrator (V.O.):** In the early days, memory was simple. Physical memory looked like a single
column, with address zero at the top. First comes the operating system: really just a library of
routines, sitting at address zero. Above it, one running program, starting at sixty-four kilobytes,
and using all the rest.

**Narrator (V.O.):** That's it. No illusions. The program sees the real machine, the real addresses.
Life was easy for OS developers.

**Student** (curious): So what changed?

**Professor** (explaining): Money. Those machines cost hundreds of thousands, even millions of dollars. Leaving one idle while a single program waits is a very expensive way to wait.

*Visual idea:* Physical `Memory` column (0 at top): OS block gray at the top (0 to 64KB), "Current program" below it. A Process stands beside it and sees everything. A price tag "$$$$$$" floats by.

### B03 — Sharing the machine  `build-up` (~0:50)
**Narrator (V.O.):** So people started to share. First came **multiprogramming**. Several programs
are ready to run at the same time, and when one stops to wait for an I/O, the OS switches to
another. The CPU stays busy. Utilization goes up.

**Narrator (V.O.):** You remember this from the ready queue and the blocked state: the same
trick that helps the CPU is about to cause trouble for memory.

*Visual idea:* Callback to episode 04: a CPU with processes A, B, C in a ready queue; A goes blocked (clock icon), B hops onto the CPU. The CPU never goes dark.

### B04 — Time sharing, and a slow idea  `build-up` (~1:15)
**Narrator (V.O.):** Then people wanted more. Programmers were tired of waiting hours between debug
cycles. They wanted to sit at the machine and get an answer *now*. This is **time sharing**: many
users, each wanting an interactive, timely response.

**Student** (curious): So run one program for a while, then switch to the next one. We already know how to switch the CPU. What's the catch?

**Professor** (explaining): Memory. A program expects all of memory to itself. So here is the naive way: stop A, copy *everything* in memory out to the disk, load B from the disk, run B for a while, and so on.

**Narrator (V.O.):** Saving the registers is quick: a few numbers. But saving all of memory to disk
is brutally slow, and the bigger memory grows, the worse it gets. The CPU sits idle while the disk grinds.

**Student** (frustrated): That's awful. Just leave them there!

*Visual idea:* A Memory column filled with A's color; arrows stream it down to a Disk (green), then B's color streams back in. The CPU chip beside it sits dim with a clock. Student's "just leave them!" bubble.

### B05 — Everyone stays in memory  `build-up` (~1:00)
**Professor** (happy): Exactly. Leave the processes in memory and switch between them there. Here's the book's picture of a 512-kilobyte machine. The OS at the top. Then three processes, A, B and C, each with a small slice carved out for it. One CPU, so one runs while the other two wait in the ready queue.

**Narrator (V.O.):** Switching is fast again. But now there's a new problem.

**Student** (confused): Wait. If we all live in one memory, what stops B from just reaching over and scribbling on A?

**Professor** (worried): Nothing. Yet. That's called a **protection** problem. You do not want a process to read another's memory, or worse, write to it. Or to touch the OS's own memory.

*Visual idea:* Figure 13.2: physical Memory with OS, free gaps, C, B, A. A mini ready queue (B and C waiting while A runs). Then B's arrow reaches into A's slice and a red crack; A's Process goes `zombie`/error. A padlock closes between the slices.

### B06 — An easy-to-use abstraction  `build-up` (~1:00)
**Narrator (V.O.):** So the OS needs a better idea. Not raw memory, but an *easy-to-use picture* of
memory, one for each program. We call this abstraction the **address space**. It is the running
program's view of memory in the system, and understanding it is the key to understanding how memory
is virtualized.

**Narrator (V.O.):** What's in it? Everything the program needs. The **code**: the instructions
have to live in memory somewhere. And two more things we'll get to in a second.

**Narrator (V.O.):** Let's use a tiny example. Sixteen kilobytes of address space. The book uses
tiny examples because the math is easier. The code sits at the top, starting at address zero and
packed into the first kilobyte. Code is static, so we know it won't need any more room.

*Visual idea:* The 16KB address-space `Memory` column appears with addresses 0KB at the top. The code region fills in, 0 to 1KB, with a few instruction lines flashing.

### B07 — Stack and heap  `build-up` (~1:30)
**Student** (curious): You said two more things.

**Narrator (V.O.):** The **stack** keeps track of where the program is in the function call chain.
It holds local variables, arguments, and return values, and it grows and shrinks as functions call and return.

**Narrator (V.O.):** The **heap** is for dynamically allocated memory: what you get from `malloc()`
in C, or `new` in C++ or Java. The program asks for it, the program is responsible for it.

**Narrator (V.O.):** Both of these grow and shrink while the program runs, so where do we put them? At opposite ends. The heap starts just after the code, at one kilobyte, and grows down. The stack starts at the bottom, at sixteen kilobytes, and grows up. Each has room to grow, and the free space in the middle is shared.

**Professor** (explaining): One honest note. This layout is a convention. You could arrange things differently, and when we get to threads, several stacks will have to share one address space, so this neat picture will stop working. And real programs hold other things too, like statically initialized variables. We're ignoring those for now.

*Visual idea:* Stack and heap regions drawn in turn, arrows pointing into the free space. A malloc call grows the heap downward; a function call grows the stack upward. A mini C snippet beside it.

### B08 — The Crux: the lie  `crux` (~1:10)
**Narrator (V.O.):** Now the twist. When we describe this address space, we are describing an
*abstraction*. The program is not really in memory at addresses zero through sixteen kilobytes.
It's loaded at some arbitrary physical address.

**Narrator (V.O.):** Look at the 512-kilobyte machine again. Process A is not at zero. It sits at
three hundred and twenty kilobytes. B and C are elsewhere. And yet every one of them believes
its own memory starts at zero.

> **THE CRUX:** How can the OS build this abstraction of a private, potentially large address space for multiple running processes (all sharing memory) on top of a single, physical memory?

*Visual idea:* The 16KB address space from B07 on the left. The physical 512KB memory on the right with A's slice at 320KB. The A address space lifts and lands on the 320KB slice. Then the crux card, which docks.

### B09 — A virtual address  `build-up` (~1:15)
**Narrator (V.O.):** Here is what that means in practice. Process A runs a load from address zero.
We call this a **virtual address**. It is what the program sees.

**Narrator (V.O.):** But the data isn't at physical address zero. That's where the OS lives. The OS,
together with some help from the hardware, makes sure the load goes to physical address three hundred
and twenty kilobytes, where A really is.

**Narrator (V.O.):** When the OS does this, we say it is **virtualizing memory**. The program thinks it
is loaded at a particular address, with a potentially huge space. The reality is quite different. This is
the key to every modern computer system.

**Student** (excited): Same trick as the peach! One real thing, many pretend ones.

**Professor** (proud): And the same as the two `mem` programs that both printed `0x200000`: same address, different bytes underneath. Remember that one?

*Visual idea:* A's CPU load at address 0 sends an arrow into the virtual column; a translator "OS + hardware" pulse bends the arrow to physical 320KB. Peach flashes in the corner, then the two-copy `mem` terminal from 01-03, as a quick callback.

### B10 — Goal one: transparency  `build-up` (~0:50)
**Narrator (V.O.):** So the OS now has a job: virtualize memory, and do it with style. To keep it
honest, it needs goals. We'll meet them again and again. The first is **transparency**.

**Narrator (V.O.):** The virtualization should be invisible to the running program. The program
shouldn't know that memory is virtualized. It should behave as if it has its own private physical
memory. Behind the scenes, the OS and the hardware do all the work of multiplexing memory among many
jobs, and that implements the illusion.

**Student** (confused): Invisible? I thought "transparent" meant you can see everything.

**Professor** (explaining): In everyday speech, yes. Here it's the opposite: the illusion must not be *visible* to the program. A transparent window; you don't see the glass.

*Visual idea:* Term highlight; an Aside card with a "glass pane" vs "window you don't notice". Process A sits behind a pane of glass; the pane fades until the viewer forgets it.

### B11 — Goals two and three: efficiency, protection  `build-up` (~1:20)
**Narrator (V.O.):** Goal two: **efficiency**. Virtualization should be as fast as possible: not making
programs run much slower. And as small as possible: not using too much memory for the structures that
make virtualization work. To be fast, the OS will lean on hardware, including something called a TLB.
We'll get there.

**Narrator (V.O.):** Goal three is where we started: protection. The OS must protect processes from each other, and itself from them. When a process does a load, a store, or an instruction fetch, it must not be able to touch anything outside its own address space.

**Narrator (V.O.):** That gives us a principle we'll use all through the book: **isolation**. If two things are properly isolated, one can fail without hurting the other. Each process should run in its own little cocoon, safe from faulty or malicious neighbors.

*Visual idea:* A speed gauge and a small memory bar for efficiency (time vs space). Then three process cells each in a cocoon with a padlock; B tries to reach into A and bounces. Tip card "The principle of isolation".

### B12 — Every address is virtual  `big picture` (~1:00)
**Narrator (V.O.):** Back to the program from the start. Here are the three addresses it printed on
a 64-bit Mac. Code: `0x1095afe50`. Heap: `0x1096008c0`. Stack: `0x7fff691aea64`.

**Narrator (V.O.):** Look at the order. Code comes first. Then the heap. And the stack is all the
way at the other end of this big virtual space, just like our picture. And now you know the
twist. All of them are virtual addresses.

**Professor** (proud): If you can print it, it's virtual. Only the OS, with the hardware, knows where the bytes really are. So never forget: an address your program shows you is an illusion of how things are laid out in memory.

*Visual idea:* The terminal again; each printed address now sits on the same-colored region of the address-space column (code, heap, stack) in a bigger space. A "virtual" stamp lands on each. Aside card "Every address you see is virtual".

### B13 — Recap  `recap` (~0:30)
**Narrator (V.O.):** What do we carry out of this episode? One: early machines had one program in
memory, and nothing to hide. Two: sharing memory made protection a problem. Three: the OS's answer is the address space, a private, easy picture of memory, with code, heap and stack. Four: virtualizing memory means a virtual address is not a physical one. Five: the goals are transparency, efficiency, and protection.

*Visual idea:* Five-line recap card with small icons: early memory column, padlock, address space column, arrow from 0 to 320KB, three goal icons.

### B14 — Teaser  `teaser` (~0:25)
**Student** (curious): So my program thinks it has a big private memory. But how does it *ask* for more? Where does `malloc()` get it?

**Professor** (happy): That's the next question. How a program talks to this memory: `malloc()` and `free()`, and the mistakes that come with them. And after that, the real trick: how a virtual address becomes a physical one.

*Visual idea:* The address-space column with the heap growing, a `malloc(…)` bubble. Then the end card "Next: 14 · Interlude: Memory API".

## Cut / deferred material
- **Homework (`free`, `pmap`, `memory-user.c`):** a hands-on Linux exercise; omitted.
- **References** (Corbató, McCarthy, microkernel papers): omitted; the microkernel remark in the Isolation tip is cut for time.
- **Details of segmentation, paging, free-space management and swapping:** only previewed as "mechanisms and policies" in the teaser; they are chapters 15 onward.
- **Footnote 3** ("we'll convince you to drop the course"): a joke, omitted.
- **Translation itself:** only the *idea* that the load goes to 320KB is shown; the mechanism is episode 15.

## Callbacks & setups
- Callbacks to earlier episodes: the peach and the two `mem` programs sharing `0x200000` (01-03); ready queue, blocked state and context switch (04, 06); time sharing (07); multiprogramming (01-03); Illusion split.
- Setups paid off in later episodes: `malloc()`/`free()` and stack/heap use (14); translating virtual to physical addresses (15); TLBs for efficiency (19); threads breaking the stack/heap layout (26); protection and the Isolation principle (all later).

## Open questions
- **Placement of the Crux:** the book places it after the 16KB address space. I follow that (B08), after the viewer feels the protection problem. Is that late enough, or should it also appear in the cold open?
- **Student expression workaround:** the Student has no "worried"; B05 uses `confused`.
- **Teaser target:** book order says 14 is the Memory API, and the real trick (translation) is 15. I tease 14 first and mention 15. Please adjust once those episodes are final.
- **Overview facts:** I assume 01-03 showed the two `mem` programs printing `0x200000`, as its script says.
