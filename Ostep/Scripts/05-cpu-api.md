# 05 — Interlude: Process API
> Section: Virtualization · Source: Ostep/Chapters/05-cpu-api.pdf · Est. duration: ~14:00 (1,800 spoken words ≈ 12:00 of narration, plus pauses)

## Logline
Last time we saw that every OS lets you create, wait for and control processes. UNIX does it with
three strange calls: `fork()` clones a process, `exec()` turns it into a different program, and
`wait()` lets the parent catch up. This episode shows what each one does, and why splitting
"create" in two is the trick that makes the shell possible.

## Learning goals
- After watching, the viewer can explain what `fork()` does, why parent and child get different return values, and why the output order is not guaranteed.
- Explain how `wait()` makes the order deterministic, and what `exec()` does (and does not) do.
- Explain why UNIX separates `fork()` from `exec()`, using the shell and output redirection as the example.
- Name the other control tools: signals (`kill`), users and the superuser, and `ps` / `top`.

## Concepts covered
| Term | Definition (book's wording or faithful paraphrase) | Beat |
|---|---|---|
| Process API / interlude | The practical interfaces the OS presents for creating and controlling processes. | B02 |
| Process identifier (PID) | Each process has a name, in most systems a number; in UNIX it is used to do things to a process (e.g. stop it). | B03 |
| `fork()` | System call that creates a new process: an (almost) exact copy of the calling process. | B03 |
| Parent / child | The creator and the newly created process. The child does not start at `main()`; it comes to life as if it had called `fork()` itself. | B03 |
| Return value of `fork()` | The parent receives the child's PID; the child receives 0. | B04 |
| Non-deterministic | Output that can differ between runs, because the CPU scheduler decides who runs first. | B05 |
| CPU scheduler | Decides which process runs at a given moment; complex, so we can't make strong assumptions about it. | B05 |
| `wait()` (and `waitpid()`) | System call that blocks the parent until a child finishes, then returns in the parent. | B06 |
| `exec()` family | Loads code and static data from a given executable over the current process, re-initializes heap and stack, and runs it with the given arguments. It does not create a process, and a successful call never returns. | B07 |
| Shell | A user program that shows a prompt and runs the commands you type, using `fork()`, `exec()` and `wait()`. | B08 |
| Redirection | Sending a program's output to a file (`>`): the shell closes standard output and opens the file before `exec()`. | B09 |
| Pipe | An in-kernel queue connecting one process's output to another's input (`pipe()`). | B09 |
| Get it right (Lampson's law) | "Neither abstraction nor simplicity is a substitute for getting it right." | B10 |
| Signal | A way to tell a process to pause, die, and so on (`kill()`, control-c, control-z); a process can "catch" signals with `signal()`. | B11 |
| User / superuser (root) | The OS lets many users in and only lets each control their own processes; the superuser can control all of them. | B11 |
| Man pages (RTFM), `ps`, `top` | Manual pages, and the tools that list processes and their resource use. | B12 |

## Script

### B01 — A program that talks to itself  `cold open` (~0:45)
**Narrator (V.O.):** Last time, we ended with a promise: a process that clones itself. So let's see
it. Here is a tiny C program. It prints "hello". Then it hits an `if` and an `else`. If it's the
child, print "child". Otherwise, print "parent".

**Narrator (V.O.):** Let's run it.

**Student** (confused): Wait. "Hello" appeared once. But then *both* "child" and "parent" showed up.
That's an `if` and an `else`. How can both of them run?

**Professor** (happy): Because after one particular line, there are two of the program.

**Narrator (V.O.):** Today we meet the three calls UNIX uses to make and manage processes.

*Visual idea:* A **Terminal** runs `./p1` and prints three lines. Next to it, the trimmed `p1.c` as a
**Code block** with a moving highlight bar that walks line by line. Student puzzled with a "?".

### B02 — The Crux  `crux` (~0:25)
> **THE CRUX: HOW TO CREATE AND CONTROL PROCESSES**
> What interfaces should the OS present for process creation and control? How should these
> interfaces be designed to enable powerful functionality, ease of use, and high performance?

**Narrator (V.O.):** This is an *interlude*. A short, practical episode about a real interface, with
real code you can type in yourself. In episode four, we listed what any OS must offer: create,
destroy, wait, miscellaneous control, status. Now we order from that menu, the UNIX way.

*Visual idea:* Crux card in `VIRT` orange; an **Aside card** "INTERLUDES: practical things" slides
in and out. Section badge "05 · Process API". The five-item menu card from episode 04 flashes by.

### B03 — fork(): one becomes two  `build-up` (~1:25)
**Narrator (V.O.):** First, a name. Every process has an ID, a number the OS uses to refer to it.
It's the **process identifier**, or **PID**. Our program starts with PID 29146. In UNIX, if you
want to do something to a process, like stop it, the PID is how you name it.

**Narrator (V.O.):** Now the interesting part. The program calls **`fork()`**. It's a system call:
a request to the OS, so it crosses into the kernel. And what the OS does is create a new process.
Not an empty one. An *almost exact copy of the caller*.

**Narrator (V.O.):** Same code. Its own copy of the address space, its own registers, its own program
counter. Remember our freeze-frame from last time, memory, registers, open files? The OS just
copied all of it. The creator is the **parent**. The new process is the **child**.

**Student** (curious): So the child starts again from the top, at `main()`?

**Professor** (explaining): No, and that's the odd part. Notice "hello" printed only once. The child
never ran that line. It simply comes to life *inside* the call to `fork()`, as if it had called it
itself. Two processes, both about to return from the same call.

**Professor** (happy): The book warns you that `fork()` is the strangest routine you'll ever call.
It's right.

*Visual idea:* Process creature coral "PID 29146" runs on the CPU, ready to call `fork()`; it crosses
the **User/Kernel boundary**. In the kernel, its PCB card and **Memory** column are duplicated like
a cell dividing: a mint "PID 29147" appears, with its own Memory column, registers and the same
highlighted line in the Code block. Term highlights: "PID", "fork()".

### B04 — Who is who?  `build-up` (~1:00)
**Student** (confused): But if they're identical, how does each one know whether it's the parent or
the child? They run the same code.

**Narrator (V.O.):** They're not *quite* identical. The child has the same memory, but a private
copy. What either one changes afterwards, the other never sees. And there's one more difference:
the value that `fork()` returns.

**Narrator (V.O.):** The parent gets back the PID of the new child, 29147. The child gets back zero.
That single number is the whole trick. The `if` checks it. Zero? You're the child, take this branch.
Anything else? You're the parent, take that one.

**Student** (excited): So the code is the same, but the world is different. Each process walks
down its own branch.

**Professor** (proud): Both processes, one program, two paths.

*Visual idea:* Both processes return from `fork()` carrying a tag: coral gets "rc = 29147", mint gets
"rc = 0". The Code block now shows two highlight bars (coral and mint) that split at the `if`: coral
goes to the `else`, mint to the `rc == 0` branch. Each prints its own line into the Terminal.

### B05 — Who goes first?  `build-up` (~0:55)
**Narrator (V.O.):** Now look at the output again. "Parent" printed before "child". But run it
another time, and you might get the opposite order.

**Student** (frustrated): The same program, the same input, and different output? Is it broken?

**Professor** (explaining): It's **non-deterministic**, and it isn't broken. Say we have a single
CPU. After `fork()`, there are two processes ready to run. Which one goes first?

**Narrator (V.O.):** That's the job of the CPU **scheduler**, and from our point of view it's
unpredictable. Both processes sit in the ready queue, and either could be picked. We can't make strong
assumptions about what it will choose.

**Professor** (worried): This looks like a small annoyance now. Remember it. In the concurrency
section, it becomes a very big deal.

*Visual idea:* Two Process creatures (coral, mint) wait in the ready **Queue**; a **Spotlight**
(policy icon) picks one. Replay twice with different winners; the Terminal output shows both
orders, side by side. Term highlight "non-deterministic".

### B06 — wait(): let the child finish  `build-up` (~1:00)
**Narrator (V.O.):** Sometimes order matters. Suppose the parent wants to know that its child has
finished before it continues. For that, there's **`wait()`**. The parent calls it, and the OS *blocks* the
parent, our old blocked state, until a child exits. Then `wait()` returns, with the PID of the child
that finished.

**Narrator (V.O.):** Add one `wait()` to the parent's branch, and the output becomes deterministic.
Can you see why? Pause the video and think about it.

**Narrator (V.O.):** Two cases. If the child happens to run first, it prints and exits, and when the
parent finally runs, `wait()` returns immediately. If the parent runs first, it calls `wait()` right
away, blocks, and the CPU goes to the child. Only once the child has exited does the parent wake up.
Either way, the child prints first.

**Student** (excited): And the exited child waits for its parent in the zombie state!

**Professor** (happy): The zombie finally has a job. There's a sibling call, `waitpid()`, with more
control, and rare cases where `wait()` returns early. But for us, this is the rule.

*Visual idea:* The two cases as two **Timeline** rows replayed one after the other. In case 2, the
coral parent turns blocked (clock) in the **State diagram** legend, then ready again when the mint child
turns zombie and is collected. Terminal now always prints child, then parent.

### B07 — exec(): become someone else  `build-up` (~1:20)
**Narrator (V.O.):** `fork()` alone is a bit limited. It only gives us copies of the *same* program.
What if the child should run something different? That's the third call: **`exec()`**.

**Narrator (V.O.):** In our next example, the child calls a variant of `exec()` to run `wc`, the
word-counting program, on the file `p3.c`. And the output shows the counts: 29 lines, 107 words, 1,030
bytes. Let's look inside.

**Narrator (V.O.):** Given the name of an executable and some arguments, `exec()` loads code and static
data from that file, and *overwrites* the process's current code segment and static data with it. The
heap and the stack are re-initialized. Then the OS runs the new program, passing the arguments as its
`argv`. Sound familiar? It's the loading step from last episode, applied to a process that already exists.

**Student** (surprised): So it makes a new process?

**Professor** (explaining): No, and that's the key point. `exec()` creates *no* process. The same
process, same PID, becomes a different program. If it works, `exec()` never returns. The code
that came after it is gone. In our example, the line "this shouldn't print out" never prints.

**Narrator (V.O.):** On Linux there are six variants of `exec()`, with different ways of passing the
arguments, but they do the same thing.

*Visual idea:* The mint child's Memory column: its code region (labeled `p3`) is wiped and replaced
by a file icon labeled `wc` flying in from a **Disk**; heap and stack reset. Same creature, same
PID tag, new program label. A ghost of the line after `exec()` fades away. Terminal prints `29 107 1030 p3.c`.

### B08 — Why two calls?  `build-up` (~1:30)
**Student** (frustrated): Hold on. All of this seems like a strange way to launch a program. First
clone yourself, then replace yourself? Why not one simple call, "run this program"?

**Professor** (proud): That's the question the whole design hangs on. Let's look at who launches
programs for a living: the **shell**.

**Narrator (V.O.):** The shell is just an ordinary user program. It shows you a prompt, and waits.
You type a command: a program name and its arguments. The shell finds the executable, calls
`fork()` to create a child, calls some variant of `exec()` in the child to run the command, and
calls `wait()` in the parent until the command finishes. Then it prints the prompt again.

**Narrator (V.O.):** And here's the key. Between `fork()` and `exec()`, there's a gap, where the code
is running in the child, but it's still the shell's code. That gap is a chance to rearrange the
child's world *before* the new program starts.

*Visual idea:* A **Terminal** with a prompt; the typed command `wc p3.c` spawns a loop diagram (a
circular arrow): prompt → fork → exec → wait → prompt, with the shell as a gold process. The gap
between `fork` and `exec` is highlighted as a small "workshop" box with a wrench.

### B09 — Redirection and pipes  `build-up` (~1:30)
**Narrator (V.O.):** Let's use the gap. You type: `wc p3.c > newfile.txt`. The `>` sign means the
output of `wc` should go into a file, not the screen. This is **redirection**.

**Narrator (V.O.):** The shell does it in the gap. In the child, before `exec()`, it closes standard
output, then opens the file. UNIX always hands out the lowest free file descriptor. Remember our
three plugs, 0, 1, 2? Plug zero is taken, plug one was just freed, so the file takes plug number one. And open files stay open across
`exec()`. So when `wc` later prints, it prints "to the screen", exactly as always, and the text
lands in the file instead.

**Student** (excited): And `wc` doesn't even know!

**Professor** (happy): And the proof is easy. Run the command, and the screen stays empty. Then read the file, and all
the expected output is there.

**Narrator (V.O.):** Redirection connects a program to a file. A close relative connects it to another program: the **pipe**. The `pipe()` call makes a queue inside the
kernel. One process's output is connected to one end, another process's input to the other. So you can
chain tools: look for a word in a file with `grep`, and pipe the result into `wc` to count how many.
All without changing a single line in either program.

*Visual idea:* Adapt Figure 5.4. The mint child with three plugs (0 stdin, 1 stdout, 2 stderr from
episode 04). Step 1: plug 1 pops out, goes to the screen icon. Step 2: `close(1)`, the cable is cut;
`open("p4.output")` plugs a file icon into slot 1. Step 3: `exec(wc)`; the process body changes, but the
plugs remain. Output flows to the file. Then a pipe glyph connecting two processes.

### B10 — Tip: get it right  `build-up` (~0:30)
**Narrator (V.O.):** Pipes, redirection, a whole shell, from two small calls. One reason to see this design as a classic is a rule named after Butler Lampson:
**get it right**. Neither abstraction nor simplicity is a substitute for getting it right. There are
many ways to design process creation. But the UNIX designers' combination of `fork()` and `exec()` is simple, and immensely
powerful.

**Professor** (neutral): Not everybody agrees. A recent paper argues for a simpler call, `spawn()`.
The authors of the book have opinions. You're allowed to have your own.

*Visual idea:* **Tip card** "GET IT RIGHT (Lampson's law)" slides in from the side. A tiny
`spawn()` tag appears with a question mark, then slides off.

### B11 — Signals, users and the root  `build-up` (~1:15)
**Narrator (V.O.):** Back to the interface. Beyond those three calls, there are more. In UNIX, `kill()` sends a
**signal** to a process. A signal can tell the process to pause, to die, or other useful things. Your shell wires
some to keystrokes: control-c sends an interrupt, which normally terminates the process. Control-z sends a stop, which pauses it, and you
can resume it later with `fg`. That's the "suspend and resume" from our menu.

**Narrator (V.O.):** A process can also *catch* a signal with `signal()`: run its own code when one arrives.

**Student** (curious): Wait. Then can I kill anyone's process? Say, the one my roommate started on the same machine?

**Professor** (explaining): That's why systems have **users**. You log in, and you can control your
own processes. Not anybody else's. Sharing the machine safely needs that rule.

**Narrator (V.O.):** There's one exception: the **superuser**, or **root**. They can administer the
system and control any process. Powerful, and dangerous. Use it rarely.

**Professor** (worried): With great power comes great responsibility. The French Revolution said it
first, apparently.

*Visual idea:* A coral process with a keyboard: "ctrl-c" pops a lightning-bolt signal that hits it
(it turns done); "ctrl-z" gives a pause glyph; `fg` gives a play glyph. Then two process groups
under two user name tags; a signal bounces off a force field of the other user. A crown tag "root" lets it through.

### B12 — Useful tools  `build-up` (~0:35)
**Narrator (V.O.):** To see all this in practice, some tools help. `ps` lists the processes running on your
system. `top` shows which of them are using the most CPU. Humorously, `top` often claims that `top` is the
top resource hog. And `kill` and `killall` send signals. Use them carefully, or you could kill your window manager.

**Student** (bored): Is there a manual for every flag?

**Professor** (happy): There is. They're the **man pages**. When someone replies, "RTFM", they mean
you should go read them.

*Visual idea:* A **Terminal** running `ps` (small process list) then `top` (bars). An **Aside card**
"RTFM — read the man pages" slides in with a little book icon.

### B13 — Back to the menu  `big picture` (~0:45)
**Narrator (V.O.):** Let's wrap up by going back to the menu from last time. **Create**: that's `fork()`, and
usually `exec()` right after. **Wait**: that's `wait()`. **Destroy** and **miscellaneous control**:
signals, via `kill()`. **Status**: `ps` and `top`. A handful of simple calls, combined, are enough to
build a shell, redirection, pipes, and more.

**Narrator (V.O.):** And we've only skimmed the surface. The book recommends reading Stevens and Rago to
go deeper. We'll return to file descriptors when we get to file systems.

*Visual idea:* The five-item menu card from episode 04 returns; each row gets its UNIX call written next to it,
one by one, with the matching prop from this episode (clone, wait clock, lightning, tag).

### B14 — Recap  `recap` (~0:35)
**Narrator (V.O.):** So, today:
1. **`fork()`** creates a new process: a nearly exact copy. The parent gets the child's PID, and the child gets zero.
2. The order is up to the scheduler, so output is **non-deterministic**. **`wait()`** makes the parent wait for its child.
3. **`exec()`** turns the current process into a different program, without creating a new one.
4. Keeping `fork()` and `exec()` apart lets the shell set up redirection and pipes in between.
5. **Signals**, **users** and the **superuser** control who can do what to which process.

*Visual idea:* Five-item recap list, each with a mini icon: split blob, clock, file swap, plugs, lightning bolt.

### B15 — Teaser  `teaser` (~0:30)
**Student** (curious): All these calls say "the OS creates this", "the OS stops that". But when my program
is running on the CPU, the OS isn't. How does it ever get control back?

**Professor** (thinking): Good question. And if the OS watched every instruction, we'd lose all the
speed. We want programs to run *directly* on the CPU, but we want to stay in charge.

**Professor** (happy): Next time: limited direct execution.

*Visual idea:* A process runs on the CPU, while a tiny Professor-sized OS figure watches from behind
a glass wall, out of reach. Cut to black: "Next: 06 · Direct Execution".

## Cut / deferred material
- **Homework (fork.py simulation and code questions):** cut from the video; could become an on-screen "try it yourself" link. (Its questions, e.g. what a variable looks like in the parent and child after `fork()`, are touched on in B04.)
- **References:** cut, except the spawn() paper note in B10 and the Stevens and Rago pointer in B13.
- **Full `p1.c`–`p4.c` listings with includes and error handling:** shown trimmed (the `fork failed` branch is omitted, flagged on screen).
- **Orphans and what happens to children when a parent exits (homework 4):** not covered.
- **`waitpid()`, the six `exec()` variants, `open()` flags, `process groups`:** mentioned only by name.
- **`pipe()` internals and file descriptors in depth:** deferred to the persistence section (39).
- **Scheduling and non-determinism in depth:** deferred to 07–10 and the concurrency section.

## Callbacks & setups
- Callbacks to earlier episodes:
  - The Process API menu (04, B07): create, destroy, wait, control, status (B02, B13).
  - Machine state / freeze-frame (04, B06) in B03; loading from disk in B07.
  - Blocked state and ready queue (04, B09) in B05–B06; zombie and parent's `wait()` (04, B12) in B06.
  - File descriptors 0, 1, 2 (04, B08) in B09. Scheduler (04) in B05.
  - System call / User-Kernel boundary (01–03) in B03.
- Setups paid off in later episodes:
  - Scheduler and non-determinism → 07–10, and concurrency (26+).
  - File descriptors, pipes → persistence section (39).
  - "Who keeps control while a program runs?" → 06 Direct Execution.

## Open questions
- **Length:** ~14:00 is at the upper end of the 8–15 min target. B10 (Tip + `spawn()`), B12 (tools) and half of B11 could be cut to land near 11:00.
- **Analogy added:** B03 reuses the freeze-frame idea from 04 and B04 says "the world is different". These are mine, not the book's.
- **Spider-Man / French Revolution joke (B11):** from the book's superuser aside. Keep or cut?
- **Code on screen:** `p1.c` is trimmed (error check removed) to fit the ~12-line limit. OK?
