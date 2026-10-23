# 14 — Interlude: Memory API
> Section: Virtualization · Source: Ostep/Chapters/14-vm-api.pdf · Est. duration: ~14:00 (~1,850 spoken words ≈ 12:20 of narration, plus pauses)

## Logline
Your program asks the OS for memory in two ways: the stack, which the compiler manages for you, and the heap, which you manage yourself with `malloc()` and `free()`. Asking is easy. Giving back, sizing, and not touching what you shouldn't is where programs die. This episode shows the API, then walks through the seven classic ways to get it wrong.

## Learning goals
- After watching, the viewer can explain the difference between stack (automatic) and heap (explicit) memory, and which one a given variable lives in.
- Write a correct `malloc()` call, including `sizeof()` and the `strlen(s) + 1` idiom, and say what `free()` takes and why it needs no size.
- Name and recognize the common memory errors: forgetting to allocate, buffer overflow, uninitialized read, memory leak, dangling pointer, double free, invalid free.
- Explain why `malloc()`/`free()` are library calls rather than system calls, and what `brk`/`sbrk` and `mmap()` do underneath.

## Concepts covered
| Term | Definition (book's wording or faithful paraphrase) | Beat |
|---|---|---|
| Stack (automatic) memory | Allocations and deallocations are managed *implicitly* by the compiler; space appears when you call a function and vanishes when you return. | B03 |
| Heap memory | Memory for long-lived data; all allocations and deallocations are *explicitly* handled by the programmer. | B04 |
| `malloc()` | Pass it a size; it returns a pointer to that much heap space, or `NULL` on failure. | B04, B05 |
| `sizeof()` | A compile-time operator, not a function call; use it to ask for the right size. | B05, B06 |
| Cast | Telling the compiler "I know what I'm doing" about the `void *` that `malloc()` returns; not needed for correctness. | B05 |
| `free()` | Takes one argument, a pointer returned by `malloc()`; the size is tracked by the allocation library. | B07 |
| Automatic memory management / garbage collector | In newer languages you never call `free()`; a collector frees what has no references left. | B08 |
| Segmentation fault | The fancy term for "you did something wrong with memory and the machine is angry". | B08 |
| Buffer overflow | Not allocating enough memory; writing past the end of a buffer. | B09 |
| Uninitialized read | Reading heap data you never filled in: unknown value. | B10 |
| Memory leak | Forgetting to free memory you no longer use. | B11 |
| Dangling pointer | Freeing memory before you are done with it; the pointer still points at it. | B12 |
| Double free | Freeing memory more than once; the result is undefined. | B12 |
| Invalid free | Calling `free()` with a value that `malloc()` never returned. | B12 |
| purify, valgrind | Tools that help find memory errors. | B13 |
| `brk` / `sbrk`, the break | System calls that move the end of the heap (the "break"). The library is built on them; never call them directly. | B14 |
| `mmap()`, anonymous region, swap space | Create a memory region not tied to a file (backed by swap space, later); can be managed like a heap. | B14 |
| `calloc()`, `realloc()` | `calloc()` allocates and zeroes; `realloc()` makes a larger region, copies the old one, and returns the new pointer. | B15 |

## Script

### B01 — "But it worked before!"  `cold open` (~0:45)
**Narrator (V.O.):** Our student has written a C program. It compiles. No warnings.

**Narrator (V.O.):** Run it once. Correct answer. Run it again. Correct answer. A third time. Correct again.

**Student** (excited): See? It works.

**Narrator (V.O.):** Then they run it on a friend's laptop.

**Student** (frustrated): Segmentation fault. But it worked before! It must be the compiler. Or the operating system. Or the professor.

**Professor** (happy): It's almost always the code. And "it worked before" is the most famous last sentence in C.

**Narrator (V.O.):** Today we meet the part of C where those sentences get written: the memory you ask for yourself.

*Visual idea:* A **Terminal** runs `./prog` three times, each printing `42` with a green tick; the fourth run prints `Segmentation fault`. Student goes excited, then frustrated; a speech bubble "But it worked before!".

### B02 — The Crux  `crux` (~0:20)
> **THE CRUX: HOW TO ALLOCATE AND MANAGE MEMORY**
> In UNIX/C programs, understanding how to allocate and manage memory is critical in building robust and reliable software. What interfaces are commonly used? What mistakes should be avoided?

**Narrator (V.O.):** This is another interlude: a practical episode, real code, a real interface. Last time we drew the address space: code, heap, stack. Now we ask how a program actually *uses* the heap and the stack, and how it gets hurt.

*Visual idea:* Crux card in `VIRT` orange; section badge "14 · Memory API". The address-space `Memory` column from 13 slides in at the left as the "map" for the episode.

### B03 — Stack: memory that cleans up after itself  `build-up` (~0:55)
**Narrator (V.O.):** C programs use two kinds of memory. The first is the **stack**. Say a function `func()` needs an integer, `x`. You just write `int x;`. That's it.

**Narrator (V.O.):** The compiler does the rest. When you call `func()`, it makes room for `x` on the stack. When you return, it takes that room back. You never asked, and you never give back. That's why the book calls it **automatic** memory: the allocations and deallocations are managed *implicitly*.

**Student** (curious): That sounds perfect. Why would I want anything else?

**Professor** (explaining): Because of what "takes it back when you return" means. If you want some information to live *beyond* the call, you had better not leave it on the stack.

*Visual idea:* In the **Memory** column, the stack region at the bottom. Code block shows `func() { int x; }`. A frame `x` appears in the stack region on the call and is erased on the return, with a small "gone" puff. Term highlights: "stack", "automatic".

### B04 — Heap: memory you manage  `build-up` (~1:00)
**Narrator (V.O.):** For long-lived memory, there's the second kind. The **heap**. Here, every allocation and every deallocation is handled *explicitly*, by you, the programmer.

**Narrator (V.O.):** That's a heavy responsibility. And, as the book says, certainly the cause of many bugs. But if you're careful, you can use it without too much trouble. Here's how you put an integer on the heap.

**Narrator (V.O.):** `int *x = malloc(sizeof(int))`. Look at what lives where. The declaration `int *x` is a pointer, and the compiler makes room for *that* on the stack. The call to **`malloc()`** asks for space for an integer on the heap, and returns its address. Upon success. On failure, it returns `NULL`. That address is then stored in the pointer, on the stack.

**Student** (surprised): So one line, two kinds of memory. The pointer lives on the stack, and the integer lives on the heap?

**Professor** (proud): Exactly. And because of its explicit nature, the heap is the focus of the rest of this episode.

*Visual idea:* The Memory column now shows both regions. `CodeWalker` highlights the one line; first the pointer cell `x` appears in the stack; then an arrow leaves it, `malloc` hops into the heap, and a cell slides out of the heap region and the arrow points at it. Term highlight: "heap". A tiny ghost `NULL` flashes for the failure case.

### B05 — The malloc() call  `build-up` (~1:00)
**Narrator (V.O.):** `malloc()` is simple. You pass it a size, it either gives you a pointer to the new space, or fails and returns `NULL`. Run `man malloc` and you'll see the signature: it takes a `size_t`, and returns a `void` pointer. You include `stdlib.h`. In truth you don't even need to: the C library links in by default. The header just lets the compiler check that you call it correctly.

**Narrator (V.O.):** Now, nobody types a raw number like ten. That's considered poor form. Instead, we use `sizeof()`. To make room for a double, `malloc(sizeof(double))`. The compiler turns that into eight at compile time. Which is why `sizeof()` is an *operator*, not a function call.

**Student** (confused): And what's that `(double *)` in front of `malloc`?

**Professor** (explaining): A **cast**. `malloc()` returns a `void` pointer: "here is an address, you decide what it means". The cast just tells readers, and the compiler, "yes, I know what I'm doing". It isn't needed for correctness.

*Visual idea:* `CodeWalker` on `double *d = (double *) malloc(sizeof(double));`. The `sizeof(double)` part is circled and morphs into `8`, tagged "compile time". The cast gets a small info tag "reassurance only". A **Tip card** "WHEN IN DOUBT, TRY IT OUT" slides in at the end of the beat and slides out.

### B06 — sizeof() can fool you  `build-up` (~1:10)
**Narrator (V.O.):** Careful. `sizeof()` is not always the number you expect. Look at this. We allocate space for an array of ten integers. Fine. Then we print `sizeof(x)`.

**Narrator (V.O.):** Four. Or eight on a 64-bit machine. Not forty.

**Student** (surprised): What? I asked for ten integers!

**Professor** (explaining): But `sizeof()` doesn't know that. It looks at the type of `x`. And `x` is a *pointer*, and a pointer is four or eight bytes, no matter how much it points at. It's the size of the arrow, not of the thing the arrow points to.

**Narrator (V.O.):** Contrast that with `int x[10]`. Here the compiler *can* see that you have ten integers, so `sizeof(x)` gives forty.

**Narrator (V.O.):** One more trap: strings. To copy a string, don't use `sizeof()`. Use `malloc(strlen(s) + 1)`. The plus one is for the end-of-string character. Forget it, and you'll be one byte short. Remember that: we'll meet it again.

*Visual idea:* Two panels. Left: pointer `x` on the stack, a ten-cell array in the heap, Terminal prints `8`. Left panel bracket sweeps only the pointer. Right: `int x[10]` as a ten-cell block, bracket spans all ten, Terminal prints `40`. Then a string `"hello"` laid out in cells: h e l l o plus a final `\0` cell highlighted as "+1".

### B07 — free(): the hard part  `build-up` (~0:50)
**Narrator (V.O.):** It turns out that allocating is the *easy* part. Knowing when, how, and even *if* to free memory is the hard part.

**Narrator (V.O.):** To release heap memory you no longer use, call **`free()`** with the pointer `malloc()` gave you. That's all it takes: one argument.

**Student** (curious): Wait. How does it know how much to free? I didn't tell it the size.

**Professor** (thinking): You didn't. The allocation library keeps track of the size of each region itself. All you have to do is hand the pointer back.

*Visual idea:* `x = malloc(10 * sizeof(int))`, heap block of ten cells. `free(x)` makes the block dim and return to "free" space. A small hidden "ledger" tag attached to the block's header reads `40` and is revealed with `Indicate` when the Student asks. Term highlight: "free()".

### B08 — Error 1: forgetting to allocate  `build-up` (~1:10)
**Narrator (V.O.):** Now we get to the part you'll get to know well: what goes wrong. Memory errors compile and run with hardly a peep from the compiler. Compiling is necessary to build a C program. It is far from sufficient.

**Narrator (V.O.):** The first mistake: forgetting to allocate. Many routines expect memory to exist before you call them. `strcpy(dst, src)` copies a string to a destination pointer. Here, `src` is `"hello"`, and `dst` is declared as a `char` pointer, and... nothing else.

**Narrator (V.O.):** Where does `dst` point? Nowhere you own. The copy writes into the void, and the program dies with a **segmentation fault**. Which the book translates, loosely, as: *you did something wrong with memory and I am angry.*

**Narrator (V.O.):** The fix: allocate first. `malloc(strlen(src) + 1)`, then copy. Or use `strdup()` and let the library do both.

**Professor** (worried): And remember our student: *it compiled, or it ran once, does not mean it is correct.*

*Visual idea:* `CodeWalker` runs the 3-line snippet. The pointer `dst` appears in the stack with an uninitialized arrow pointing at the "free" region, flashing red; the copy writes towards it; the Terminal prints `Segmentation fault`. Rewind: a heap block appears; `dst` points at it; the string fills it; a green tick. Term highlight: "segmentation fault". Tip card: "COMPILED OR IT RAN ≠ IT IS CORRECT".

### B09 — Error 2: not enough memory  `build-up` (~0:55)
**Narrator (V.O.):** Close cousin: allocating *almost* enough. Remember the plus one? Leave it out, and `dst` is one byte too small. The copy runs one byte past the end. This is called a **buffer overflow**.

**Student** (excited): And that crashes right away, right?

**Professor** (worried): Sometimes. That's the nasty part. Depending on how `malloc()` is implemented, the program often runs seemingly fine. The byte might land in the padding the library added. Or on a variable nobody uses any more. Or on a variable that *is* in use.

**Narrator (V.O.):** In the best cases, an overflow is harmless. In others, it is the root of many security vulnerabilities. And here's the lesson again: even though it ran correctly once, it doesn't mean it's correct.

*Visual idea:* Heap block of 5 cells for `"hello"`, sixth char `\0` lands in the neighbor cell. Three outcomes play as a small branching row: (1) empty padding: nothing happens; (2) a neighboring block's cell flickers and changes value; (3) crash flash. A red label "security hole" with the `padlock` icon opens on the third. Term highlight: "buffer overflow".

### B10 — Error 3: uninitialized memory  `build-up` (~0:30)
**Narrator (V.O.):** Third: you call `malloc()` correctly, but forget to put values in. Later, the program does an **uninitialized read**: it reads whatever happened to be on the heap. If you're lucky, it's zero. If you're not, it's something random, and harmful.

*Visual idea:* A freshly `malloc`'d block of cells shows scrambled hex bytes from a previous owner (ghost digits). A read arrow collects `0x7f3a…` into a variable; Terminal prints a random number on the next run, a different one. Term highlight: "uninitialized read".

### B11 — Error 4: the memory leak  `build-up` (~1:00)
**Narrator (V.O.):** Fourth: forgetting to free. That's a **memory leak**. For a long-running program, like a web server, slow leaking eventually uses everything up. Then it must be restarted.

**Student** (curious): But what about languages with a garbage collector? Don't they take care of this?

**Professor** (explaining): Many newer languages do support **automatic memory management**: you ask for an object with something like `new`, but never free it. A **garbage collector** runs, finds what has no references left, and frees it. But note: if you still hold a reference to something, no collector will ever free it. So leaks remain a problem even in modern languages.

**Student** (confused): And in C? My little program never frees anything and it's fine.

**Professor** (neutral): For a short-lived program, that can be reasonable. When the process dies, the OS takes back *all* of its pages: code, stack, and heap. Nothing is lost for good. There are two levels of management: the OS hands memory to processes and takes it back when they exit. The second level lives *inside* each process, in `malloc()` and `free()`.

**Professor** (worried): Still, make freeing a habit. Good habits are what protect you in the long-running program.

*Visual idea:* A heap region fills with blocks over a loop; the pointers disappear one by one (grey out) but the blocks remain until the free region shrinks to nothing; the **Computer** reacts (overwhelmed). Then the process "exits" (puff) and the whole address space is wiped by a bracket labeled "OS takes it all back". An **Aside card** "WHY NO MEMORY IS LEAKED ONCE YOUR PROCESS EXITS" slides in. Term highlights: "memory leak", "garbage collector".

### B12 — Errors 5, 6, 7: freeing wrongly  `build-up` (~1:05)
**Narrator (V.O.):** Fifth: freeing too early. You call `free()`, and then keep using the pointer. That's a **dangling pointer**. It still holds the old address, but the memory is no longer yours. The next use might crash. Or, if you call `malloc()` again, the library may hand that same memory to someone else, and now two parts of your program are scribbling on each other.

**Narrator (V.O.):** Sixth: freeing twice. A **double free**. The result is undefined. The allocation library may get confused and do all sorts of weird things. Crashes are the common outcome.

**Narrator (V.O.):** Seventh: calling `free()` incorrectly. `free()` expects a pointer that `malloc()` gave you. Anything else, and bad things happen. That's an **invalid free**.

**Student** (frustrated): So that's seven ways to hurt myself with two functions.

**Professor** (happy): Seven ways. And you've heard all of them now.

*Visual idea:* Three mini-scenes, same heap. (5) `free(x)`; `x` keeps a dashed arrow into a freed block; `malloc` returns that same block for `y`; both arrows now point at it, both coral and mint write into it. (6) `free(x)` twice; the second one hits a block already in "free" and a red crack. (7) `free` is called with a pointer into the middle of a block, or a stack variable's address; the call bounces off with a red X. Term highlights, one per mini-scene: "dangling pointer", "double free", "invalid free" (kept small, 0.8 s).

### B13 — The tools  `build-up` (~0:20)
**Narrator (V.O.):** Because mistakes are so common, a whole ecosystem of tools exists to catch them. **Purify** and **valgrind** are two excellent ones. Once you get used to them, you'll wonder how you survived without them.

*Visual idea:* A **Terminal** runs `valgrind ./prog`; a report appears with three lines ("invalid write", "definitely lost") each tied by a line to the code. A magnifier icon scans. (No extra term highlight: names only.)

### B14 — Under the hood: brk and mmap  `big picture` (~1:05)
**Narrator (V.O.):** You might have noticed we never mentioned *system calls*. That's because `malloc()` and `free()` aren't system calls. They're *library* calls. The library manages space inside your virtual address space, but it is itself built on system calls that ask the OS for more memory, or hand some back.

**Narrator (V.O.):** One is `brk`. It changes the location of the end of the heap, called the **break**. Give it a new address, and the heap grows, or shrinks. A cousin, `sbrk`, takes an increment instead. You should never call either yourself: let the library do it, or you'll make something go horribly wrong.

**Narrator (V.O.):** There's another way to get memory from the OS: `mmap()`. It can create an **anonymous** region inside your program, one that isn't tied to any file, but to swap space, something we'll see later. You can then treat it like a heap and manage it.

**Student** (curious): So when I call `malloc()`, the OS isn't even involved?

**Professor** (explaining): Often not. The library hands out pieces of what it already has, and only asks the OS when it runs out.

*Visual idea:* Address-space **Memory** with a **User/Kernel boundary**: `malloc`/`free` sit above it in user space as a small "library" box wrapped around the heap region. When heap space runs out, a request crosses the boundary: `brk(newbreak)`; a thin "break" marker slides down and the heap grows into "free". Then a second block appears as an anonymous region: `mmap()` labeled "anonymous". Term highlights: "break", "anonymous".

### B15 — Other calls  `build-up` (~0:30)
**Narrator (V.O.):** A couple more calls, briefly. `calloc()` allocates *and* zeroes the memory before it returns, which prevents the uninitialized reads we saw earlier. And `realloc()` is for when your array needs to grow: it makes a new, larger region, copies the old one into it, and returns a pointer to the new region.

*Visual idea:* `calloc`: cells appear already `0`. `realloc`: a 4-cell block next to a free gap; a bigger 8-cell block appears elsewhere, contents flow across, old block is freed, the pointer arrow moves.

### B16 — Recap  `recap` (~0:35)
**Narrator (V.O.):** So, today:
1. The **stack** is automatic: the compiler allocates when you call, and frees when you return. The **heap** is explicit: you `malloc()` and you `free()`.
2. Use `sizeof()`, and remember it measures the type, not what the pointer points to. Strings need `strlen() + 1`.
3. Seven classic errors: forgetting to allocate, too little, uninitialized, leaks, dangling pointers, double frees, invalid frees.
4. `malloc()` and `free()` are library calls, built on `brk` and `mmap()`. Tools like valgrind help you find the rest.

*Visual idea:* Four-item recap list with mini icons: stack/heap, ruler, seven small bug icons, a tool/magnifier.

### B17 — Teaser  `teaser` (~0:30)
**Student** (curious): One more thing. When I print the pointer `x` from `malloc()`, I get an address. A real address in memory?

**Professor** (thinking): Great question. Remember `va.c` from episode 13, the program that printed the addresses of its code, heap and stack? Every address your program prints is a *virtual* address. The program thinks the heap lives right there. The hardware knows better.

**Professor** (happy): Next time: how does the hardware turn a virtual address into a real one? Address translation.

*Visual idea:* Terminal prints `0x...` pointer; the Illusion split from 13 slides in (what the program sees on the left, what really happens on the right); the address gets a "?" arrow into a physical memory column. End card "Next: 15 · Address Translation".

## Cut / deferred material
- **Homework (malloc programs, `valgrind`, `gdb`, vector with `realloc` exercises):** cut; could become a "try it yourself" link.
- **References (Purify, valgrind papers, Stevens & Rago, Werthman buffer overflow survey, Novark et al.):** cut, except tool names in B13.
- **`void *` and C pointer syntax in depth:** only as much as needed to read the snippets.
- **How the allocator keeps track (free lists, size headers):** B07 only says "the library tracks it"; implementation is chapter 17 (free-space management).
- **`brk`/`sbrk` and `mmap()` details, swap space:** named only; swap space is covered with paging (21+).
- **The segmentation-fault footnote:** shortened (the "you will soon learn why it's called that" is a hook to chapter 16).

## Callbacks & setups
- Callbacks to earlier episodes:
  - Address space with code / heap / stack (13) in B02–B14.
  - `fork()`/`exec()` (05, B07: "heap and stack are re-initialized") connects to the process-exit and memory reclaim in B11.
  - System call and user/kernel boundary (01–03, 06) in B14: library call vs system call.
  - Safety and protection (06): segfault as the OS or hardware stopping a bad access (a one-sentence nod in B08).
- Setups paid off in later episodes:
  - Why it is called a "segmentation fault" → 16 (Segmentation).
  - Free-space management inside `malloc()` → 17.
  - Anonymous regions backed by swap space → 21 and 22 (swapping).
  - Virtual addresses printed by the program → 15.

## Open questions
- **Length:** ~14:00 is at the top of the 8-15 min range. Trim candidates to reach ~11:30: B09 (overflow outcomes), B13 (tools), B15 (calloc/realloc), the garbage-collector exchange in B11.
- **Seven errors as a gag count:** "seven ways" is mine; the book lists seven headings (forgetting to allocate, not enough, uninitialized, forgetting to free, freeing early/dangling, freeing repeatedly, calling free incorrectly). OK?
- **"Compiler, OS or professor" joke in B01:** my wording, riffing on the book's tip. Keep?
- **Teaser:** assumes 13 states that all printed addresses are virtual. If 13 already shows `printf("%p")`, B17 should call back to that exact moment.
- **Simplification flagged:** B05 drops `#include` ceremony and B04/B05 omit error checks on `NULL` (mentioned once only).
