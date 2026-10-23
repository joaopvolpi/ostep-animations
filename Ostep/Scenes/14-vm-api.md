# 14 — Interlude: Memory API · Scene breakdown
> Script: Ostep/Scripts/14-vm-api.md · Scenes: 18 · Est. duration: ~14:00

## Visual overview
- **Core visual: the address space from 13**, drawn as the existing `Memory` column with regions code / heap / free / stack (0 at top). It is the "map" for the whole episode. Stack allocations appear at the *bottom* (stack grows up), heap allocations at the *top of the heap region* (heap grows down toward `free`). Every C line is tied to a change in this one column, so the viewer always sees *where* a pointer, a block or an error lives.
- **Second visual: the CodeWalker** (p05) for every snippet, with one highlight bar (`TEXT` at 0.2 opacity). Code is on the right, the column on the left, and a `Terminal` under the code for outputs.
- **Third: pointer arrows.** A pointer variable is a small cell on the stack with an arrow into a heap block, in the owner's color. Blocks are drawn as small cell groups that slide out of the heap region. Freed blocks go hatched grey (`hatch_rect`, the "idle" look). Errors are always shown as a red flash on the exact cell involved.
- **Error gallery device:** each of the seven errors gets the same mini-structure: a snippet, the broken picture in the column, a red `x_mark`, then the fix with a `tick_mark`. The numbered "error chip" (e.g. `ERROR 3 · uninitialized read`, small, `DIM` outline, at (−3.6, −2.3)) keeps count from 1 to 7.
- **Key terms (Term unveil, veil + center):** *heap*, *malloc()* (both S04), *buffer overflow* (S09), *memory leak* (S11). Every other bolded term is a **Term note** (slides into the top-right dock, no veil); *cast* and *automatic memory management* are only spoken.
- Dependencies: `address_space_16kb` (`ostep_lib/props/p13_addrspace.py`, from 13).
- Props used: Memory (via `address_space_16kb`), CodeWalker (p05), Terminal, CruxCard, TermHighlight, SectionBadge, TipCard/AsideCard, UserKernelBoundary, PrivilegeGauge, magnifier_icon (p06), program_chip, mem_icon_small, `hatch_rect`, `padlock` (p07 `Padlock`), info_tag, x_mark, tick_mark, puff, Computer, Professor, Student, Process, `ep_tag`, `IllusionSplit`.

### Persistent assignments
| Thing | Look | Notes |
|---|---|---|
| **Address space** | `address_space_16kb()` (13's canonical AS16: `Memory(regions=["code","heap",("free",6),"stack"], addresses=["0KB","1KB","2KB","15KB","16KB"])`), placed at (−3.6, 0.3), scaled to fit y −1.8..2.4 | Addresses in KB on the left, 0 at top. Use its `.grow_heap(k)` / `.grow_stack(k)` / `.region_arrows()` for heap and stack growth. Free is large, so blocks slide out of the heap region's lower edge and grow downward. Code region keeps the chip `prog`. |
| **Program** | `Process(label="prog", color=PROCESS_COLORS[0])` coral | Only appears in S01 (running a program), S11 (leak). |
| **Allocation colors** | block/pointer pair 1 = coral (`x`), pair 2 = mint (`y` / `dst`), pair 3 = gold | An arrow and its block share one color. Freed = hatched grey. |
| **Stack cells** | Small rounded cells inside the stack region, `USER_COLOR` outline, name in `MONO_FONT` | Frames appear from the bottom of the region upward. |
| **Heap blocks** | Cell groups (`MEM_COLOR` fill 0.35 + allocation-color outline) inside the heap region | Slide out from the top of the heap region; height ∝ size. |
| **Code snippets** | `CodeWalker`, monokai, font 20, ≤ 8 lines, anchored at (2.4, 1.3), caption in `DIM` | Error checks omitted; caption "(error checks omitted)" when relevant. |
| **Terminal** | `Terminal(4.6 × 1.4)` at (2.2, −1.6), prompt `prompt>` in `DIM` | Right edge < 4.7 so the Professor in the corner stays clear. |
| **Error chip** | Small chip with a number and a name, font 22, `DIM` outline | Appears at (−3.6, −2.3) (below the column), swaps per error. Fade the old chip in the same row before the new one writes. |
| Section badge | `VIRT` dot + "14 · Memory API" at (−6.6, 3.6) | Appears in S02, stays until S17. |
| Characters | Corner mode: Student (−5.8, −2.8), scale 0.75; Professor (5.8, −2.8), scale 0.75, `flip()` | Computer appears only in S11. |

## Scenes

### S01 — "But it worked before!"   (beats: B01) · ~0:45
**Purpose:** hook: a program can look right and still be wrong. Sets up the episode's tip ("it ran" ≠ "it is correct").
**Starts with:** empty (BG).
**Layout:** a large `Terminal` at center (0, 0.5), 7 × 2.6. Characters in corner mode. A big bubble above the Student.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Our student has written a C program. It compiles. No warnings." | Terminal `FadeIn`; it types `prompt> gcc prog.c -o prog` and prints nothing. A small `tick_mark` at its right. Student (neutral) and Professor (neutral) `FadeIn`. |
| 2 | "Run it once. Correct answer. Run it again. Correct answer. A third time. Correct again." | `prompt> ./prog` → `42`, a `tick_mark` after it. Repeats twice more, 0.8 s apart, the Terminal scrolling. |
| 3 | "See? It works." | Student → excited, with a small "✓"-free `tick_mark` beside his head. |
| 4 | "Then they run it on a friend's laptop." | A `Laptop` outline (small, 3 wide) slides in from the right at the Terminal's top-right; the Terminal's border recolors to match the "other machine" look (outline `DIM` → `TEXT`). |
| 5 | "Segmentation fault. But it worked before! It must be the compiler. Or the operating system. Or the professor." | Terminal prints `Segmentation fault` in red. Student → frustrated; speech bubble "But it worked before!". Three tiny chips `compiler`, `OS`, `professor` pop out of the bubble in a row (font 20), each with a `Circumscribe`, as the Student lists them. |
| 6 | "It's almost always the code. And "it worked before" is the most famous last sentence in C." | Professor → happy. The three chips fall away; a single chip `your code` replaces them with a ring, then everything fades. |
| 7 | "Today we meet the part of C where those sentences get written: the memory you ask for yourself." | Terminal and bubbles `FadeOut`. Hold 0.5 s on the empty screen. |

**Characters:** Student (neutral → excited → frustrated), Professor (neutral → happy).
**Ends with:** characters in corners, nothing else.
**Implementation notes:** the "last sentence in C" text is not displayed; it's a pure joke line. Keep red only on the segfault text.

### S02 — The Crux   (beats: B02) · ~0:20
**Purpose:** pose the question and show the map.
**Starts with:** S01 end state.
**Layout:** Crux card centered (0, 0.3), 9 × 3. Then it docks to a strip at (0, 3.0). The address-space column slides in at (−3.6, 0.3).

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "This is another interlude: a practical episode, real code, a real interface." | Section badge "14 · Memory API" `FadeIn` top-left. Crux card (`VIRT` frame) writes: **"How to allocate and manage memory?"** with the book's subtitle (small, `DIM`): "What interfaces are commonly used? What mistakes should be avoided?" |
| 2 | "Last time we drew the address space: code, heap, stack." | Crux card `dock()`s to the strip at y = 3.0. The `Memory` column (regions code / heap / free / stack) slides in from the left at (−3.6, 0.3); the four regions flash in order. |
| 3 | "Now we ask how a program actually *uses* the heap and the stack, and how it gets hurt." | The heap and stack regions get a soft glow in turn; a small crack glyph (a thin red zig-zag line) draws across the boundary between heap and free, then fades. |

**Characters:** corner mode; Student looks at the card, Professor neutral.
**Ends with:** badge, crux strip, the address-space column. Characters in corners.

### S03 — Stack: automatic memory   (beats: B03) · ~0:55
**Purpose:** stack memory appears and disappears with function calls, managed by the compiler.
**Starts with:** S02 end state.
**Layout:** column at left; CodeWalker (anchored (2.4, 1.3)) showing
```
void func() {
  int x;
  ...
}
```
plus a one-line caller `func();` above it. Terminal absent.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "C programs use two kinds of memory. The first is the **stack**." | Term note: *stack*. The stack region of the column (bottom) pulses. |
| 2 | "Say a function `func()` needs an integer, `x`. You just write `int x;`. That's it." | The CodeWalker `write_in`s the 4 lines; the bar lands on `int x;`. |
| 3 | "The compiler does the rest. When you call `func()`, it makes room for `x` on the stack." | A small cell `x` slides up into the stack region from its bottom edge (a "frame": `func` header + `x`), with a tiny gear (`GearPair`, scale 0.3) turning beside the stack labeled "compiler". The caller line `func();` gets the bar for 0.6 s. |
| 4 | "When you return, it takes that room back. You never asked, and you never give back." | The bar moves to `}`; the frame shrinks down and vanishes with a small `puff`. |
| 5 | "That's why the book calls it **automatic** memory: the allocations and deallocations are managed *implicitly*." | Term note: *automatic memory*. The gear icon reappears; text "implicit" (font 26, `DIM`) writes beside the stack and fades before the next row. |
| 6 | "That sounds perfect. Why would I want anything else?" | Student → curious. |
| 7 | "Because of what "takes it back when you return" means. If you want some information to live *beyond* the call, you had better not leave it on the stack." | Professor → explaining. Replay row 3–4 quickly: a frame appears, its `x` cell holds `7`; on return the frame vanishes and the `7` fades with it. A small `info_tag` "gone after return" near the vanishing cell, fading after 1.2 s. |

**Characters:** Student (curious), Professor (explaining).
**Ends with:** column with an empty stack, CodeWalker with the 4 lines (bar on `}`), characters.
**Implementation notes:** `Memory` has no "push frame" helper: build frames as small `RoundedRectangle`+`mono_text` placed with `region("stack")`; keep them as plain mobjects added/removed by the scene. The term-highlight docks replace each other (stack → automatic memory).

### S04 — Heap: memory you manage   (beats: B04) · ~1:00
**Purpose:** introduce the heap and `malloc()`; one line uses both kinds of memory.
**Starts with:** S03 end state, CodeWalker faded.
**Layout:** column left; CodeWalker right with `int *x = malloc(sizeof(int));` (3 lines: `void func() {` / that line / `}`).

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "For long-lived memory, there's the second kind. The **heap**." | Term unveil: *heap*. The heap region glows in the column. |
| 2 | "Here, every allocation and every deallocation is handled *explicitly*, by you, the programmer." | A small hand icon (`hand`) beside the heap region, label "you" (font 24). It fades in the next row. |
| 3 | "That's a heavy responsibility. And, as the book says, certainly the cause of many bugs." | Professor → worried. Tiny bug glyphs (three small dots with legs) scurry out of the heap region and back. |
| 4 | "But if you're careful, you can use it without too much trouble. Here's how you put an integer on the heap." | CodeWalker `write_in` the 3 lines; bar on line 2. |
| 5 | "`int *x = malloc(sizeof(int))`. Look at what lives where. The declaration `int *x` is a pointer, and the compiler makes room for *that* on the stack." | Bar highlights `int *x`; a stack frame (`func`) with the cell `x` (coral) slides up into the stack, empty. A label "pointer" in `DIM` under it. |
| 6 | "The call to **`malloc()`** asks for space for an integer on the heap, and returns its address." | Term unveil: *malloc()*. A packet labeled `malloc(4)` flies from the code into the heap region (it does **not** cross a boundary yet); a coral block (one cell) slides out of the heap region top. Its address `2KB` tag is shown for 1 s. |
| 7 | "Upon success. On failure, it returns `NULL`." | A ghost `NULL` text flashes in the heap in red with an `x_mark`, then fades. |
| 8 | "That address is then stored in the pointer, on the stack." | A coral arrow draws from the stack cell `x` into the heap block. |
| 9 | "So one line, two kinds of memory. The pointer lives on the stack, and the integer lives on the heap?" | Student → surprised. Both the stack cell and the heap block `Indicate`. |
| 10 | "Exactly. And because of its explicit nature, the heap is the focus of the rest of this episode." | Professor → proud. The stack side dims to 40%; the heap glows. Hold 1 s. |

**Characters:** Student (surprised), Professor (worried → proud).
**Ends with:** column with the stack cell `x` pointing at the coral heap block; CodeWalker (3 lines, bar on line 2).
**Implementation notes:** the packet is a small chip, not crossing the boundary: this episode's `UserKernelBoundary` shows up only in S15. Highlight docked term: *malloc()* replaces *heap*.

### S05 — The malloc() call   (beats: B05) · ~1:00
**Purpose:** `malloc()` signature, `sizeof()` as compile-time, and the cast.
**Starts with:** S04 end state, minus the CodeWalker content (it will be replaced). The column dims to 50% (it is context only).
**Layout:** CodeWalker at (1.6, 1.3). A man-page card (rounded rectangle, 5 × 1.2) *below* the code at (1.6, −0.4), inside the content zone.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "`malloc()` is simple. You pass it a size, it either gives you a pointer to the new space, or fails and returns `NULL`." | Code line 1 `void *malloc(size_t size);` appears in a small man-page card with the header `man malloc` (`DIM`). A small "size in" arrow and "pointer or NULL out" arrow around it. |
| 2 | "Run `man malloc` and you'll see the signature: it takes a `size_t`, and returns a `void` pointer." | `size_t` and `void *` each get `Indicate`; the card shows `#include <stdlib.h>` as the first line. |
| 3 | "You include `stdlib.h`. In truth you don't even need to: the C library links in by default. The header just lets the compiler check that you call it correctly." | The `#include` line gets an `info_tag` "only for checking"; a tick on "calls checked". |
| 4 | "Now, nobody types a raw number like ten. That's considered poor form." | The card fades. A chip `malloc(10)` appears with an `x_mark` and a small "poor form" label (font 24). It fades. |
| 5 | "Instead, we use `sizeof()`. To make room for a double, `malloc(sizeof(double))`." | CodeWalker `write_in`s `double *d = (double *) malloc(sizeof(double));`; the bar covers it. |
| 6 | "The compiler turns that into eight at compile time. Which is why `sizeof()` is an *operator*, not a function call." | `sizeof(double)` gets a ring; it `Transform`s into `8`; a tag "compile time" (`CPU_COLOR`) hangs under it. A "gear + calendar" is **not** used; keep it as text only. |
| 7 | "And what's that `(double *)` in front of `malloc`?" | Student → confused; `(double *)` gets a "?" over it. |
| 8 | "A **cast**. `malloc()` returns a `void` pointer: "here is an address, you decide what it means"." | Professor → explaining. The `(double *)` part is circled; a `void *` arrow becomes a `double *` arrow (Transform). |
| 9 | "The cast just tells readers, and the compiler, "yes, I know what I'm doing". It isn't needed for correctness." | An `info_tag` "reassurance only" next to the cast. Then a **Tip card** "WHEN IN DOUBT, TRY IT OUT" slides in from the right with the body "Write code. Test it. Don't just trust the docs." (≤8 words) and slides out. |

**Characters:** Student (confused), Professor (explaining).
**Ends with:** CodeWalker with the `double *d` line; column dimmed.
**Implementation notes:** the Tip card is the book's tip (page 3). Keep it under 4 s. `man malloc` card is a plain rounded rectangle with `mono_text`.

### S06 — sizeof() can fool you   (beats: B06) · ~1:10
**Purpose:** `sizeof` of a pointer vs an array; strings need `strlen + 1`.
**Starts with:** S05 end state.
**Layout:** two panels side by side: left (−3.2, 0.5) "pointer", right (3.2, 0.5) "array". A mini Terminal at the bottom center (0, −2.0), 6 × 1.0, replacing the big Terminal. The address-space column fades for this scene.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Careful. `sizeof()` is not always the number you expect." | The column and previous code fade. Mini Terminal appears. |
| 2 | "Look at this. We allocate space for an array of ten integers. Fine." | Left panel: CodeWalker `int *x = malloc(10 * sizeof(int));` / `printf("%d\n", sizeof(x));`. A pointer cell `x` (coral) and a heap block of ten cells (coral outline) draw with an arrow. Bar on line 1. |
| 3 | "Then we print `sizeof(x)`." | Bar moves to line 2. |
| 4 | "Four. Or eight on a 64-bit machine. Not forty." | Terminal prints `8`. A bracket sweeps *only* the pointer cell `x`, labeled `8 bytes`. A ghost `40` in `DIM` with an `x_mark`. |
| 5 | "What? I asked for ten integers!" | Student → surprised. |
| 6 | "But `sizeof()` doesn't know that. It looks at the type of `x`. And `x` is a *pointer*, and a pointer is four or eight bytes, no matter how much it points at. It's the size of the arrow, not of the thing the arrow points to." | Professor → explaining. The bracket pulses on the arrow; the ten-cell block dims. |
| 7 | "Contrast that with `int x[10]`. Here the compiler *can* see that you have ten integers, so `sizeof(x)` gives forty." | Right panel appears: CodeWalker `int x[10];` / `printf("%d\n", sizeof(x));`; a ten-cell block drawn directly on the stack (no pointer). A bracket spans all ten cells labeled `40 bytes`. Terminal prints `40`. |
| 8 | "One more trap: strings. To copy a string, don't use `sizeof()`. Use `malloc(strlen(s) + 1)`." | Both panels fade. A single string `"hello"` appears as cells `h e l l o` center (0, 0.8); code line `malloc(strlen(s) + 1)` writes above it. |
| 9 | "The plus one is for the end-of-string character." | A sixth cell, `\0`, drops in and is highlighted `CPU_COLOR`; label "+1". |
| 10 | "Forget it, and you'll be one byte short. Remember that: we'll meet it again." | Professor → worried. The `\0` cell flickers red once. Hold 1 s. |

**Characters:** Student (surprised), Professor (explaining → worried).
**Ends with:** the string cells with `\0`, the code line; Terminal fades.
**Implementation notes:** adapt the book's page-3 snippets. The "pointer vs block" must be spatially obvious: the arrow is short, the block long.

### S07 — free(): the hard part   (beats: B07) · ~0:50
**Purpose:** `free()` takes the pointer; size is tracked by the library.
**Starts with:** string cells; the address-space column fades back in at left.
**Layout:** column at (−3.6, 0.3) with a coral pointer `x` on the stack and a 10-cell coral block in the heap; CodeWalker right with `int *x = malloc(10 * sizeof(int));` / `...` / `free(x);`.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "It turns out that allocating is the *easy* part. Knowing when, how, and even *if* to free memory is the hard part." | The string cells fade; the column returns with the coral pointer and heap block already in place (as after S04). The CodeWalker `write_in`s three lines; bar on line 1. The `free(x)` line is drawn with a faint `DIM` glow only. |
| 2 | "To release heap memory you no longer use, call **`free()`** with the pointer `malloc()` gave you." | Term note: *free()*. Bar moves to line 3. |
| 3 | "That's all it takes: one argument." | The coral arrow pulses once; a packet `x` flies from the pointer to the code line. |
| 4 | "Wait. How does it know how much to free? I didn't tell it the size." | Student → curious. A "?" above the block. |
| 5 | "You didn't. The allocation library keeps track of the size of each region itself." | Professor → thinking. A small tag `40` on the block's top edge (a "header") fades in, labeled "tracked by the library" (font 22). |
| 6 | "All you have to do is hand the pointer back." | The block turns hatched grey and slides into the "free" region; the arrow from the stack cell turns dashed (but stays: this is the seed for the dangling pointer later). The header tag fades. |

**Characters:** Student (curious), Professor (thinking).
**Ends with:** column with the hatched freed block and a dashed arrow from `x`; CodeWalker (3 lines).
**Implementation notes:** keep the dashed arrow subtle; S13 reuses this exact picture. The header tag is the only place the idea of "size metadata" appears.

### S08 — Error 1: forgetting to allocate   (beats: B08) · ~1:10
**Purpose:** use a pointer that points nowhere; segfault; the tip.
**Starts with:** S07 end state. The column resets to: `dst` pointer cell on the stack, no heap blocks.
**Layout:** column left; CodeWalker (2.4, 1.3); Terminal below (2.2, −1.6); error chip below the column (−3.6, −2.3).

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Now we get to the part you'll get to know well: what goes wrong." | The previous code and blocks fade; the column resets to an empty heap. Student → neutral. |
| 2 | "Memory errors compile and run with hardly a peep from the compiler. Compiling is necessary to build a C program. It is far from sufficient." | Terminal `FadeIn` showing `prompt> gcc bug.c` → silence with a green `tick_mark`. The word "sufficient" in a small chip `compiles ≠ correct` (`DIM`). |
| 3 | "The first mistake: forgetting to allocate." | Error chip writes: `ERROR 1 · forgetting to allocate`, `x_mark` color `KERNEL_COLOR` dot. |
| 4 | "Many routines expect memory to exist before you call them. `strcpy(dst, src)` copies a string to a destination pointer." | CodeWalker `write_in`: `char *src = "hello";` / `char *dst;` / `strcpy(dst, src);`. Bar on line 3; a small arrow from `src` to `dst` with the label "copy". |
| 5 | "Here, `src` is `"hello"`, and `dst` is declared as a `char` pointer, and... nothing else." | Bar goes to lines 1 and 2. A stack cell `src` (with `"hello"` pointing into the code region) and a stack cell `dst` appear; `dst` is empty, with an `x`-shaped "uninitialized" mark. |
| 6 | "Where does `dst` point? Nowhere you own." | A red arrow leaves `dst` and points at random into the `free` region (flickers between spots). |
| 7 | "The copy writes into the void, and the program dies with a **segmentation fault**." | Bar on line 3; chars `h e l l o` fly toward the red arrow target; a flash on the target; Terminal prints `Segmentation fault`. Term note: *segmentation fault*. |
| 8 | "Which the book translates, loosely, as: *you did something wrong with memory and I am angry.*" | Computer is **not** used. Student → surprised; a small anger-mark glyph on the Terminal for 1.2 s (the red text trembles). |
| 9 | "The fix: allocate first. `malloc(strlen(src) + 1)`, then copy." | Rewind: bar on line 2; code line changes (`Transform`) to `char *dst = malloc(strlen(src) + 1);`. A mint block (6 cells) slides from the heap; `dst` points at it; the copy fills the cells `h e l l o \0`; green `tick_mark`; Terminal prints nothing (fresh `prompt>`). |
| 10 | "Or use `strdup()` and let the library do both." | A small chip `strdup(src)` swaps for the two lines briefly; it fades. |
| 11 | "And remember our student: *it compiled, or it ran once, does not mean it is correct.*" | Professor → worried. A **Tip card** "COMPILED OR IT RAN ≠ IT IS CORRECT" slides in (body: "It worked before? Debug first. Blame later." ≤ 8 words), then slides out. The `≠` is drawn with `MathTex(r"\neq")`. |

**Characters:** Student (surprised), Professor (worried).
**Ends with:** column with the mint block holding `hello`, `dst` pointer, error chip 1 (kept), Terminal at a fresh prompt.
**Implementation notes:** the "random arrow" is a pure visual of an uninitialized pointer; keep it grey-to-red. Don't show an actual address value.

### S09 — Error 2: not enough memory   (beats: B09) · ~0:55
**Purpose:** buffer overflow: one byte too small; three possible outcomes; why that's dangerous.
**Starts with:** S08 end state.
**Layout:** the heap region zoomed: a **zoomed strip** (a `Memory`-like row of cells, `MemoryStrip`) at center-right (2.4, 0.4) with a 5-cell mint block `dst` followed by two neighbor cells (a coral block) — a "zoom" bracket links it to the heap region in the column. CodeWalker (one line) above the strip at (2.4, 2.0), inside the content zone (y ≤ 2.55). Error chip 2 at (−3.6, −2.3).

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Close cousin: allocating *almost* enough." | Error chip 1 fades; chip `ERROR 2 · not enough memory` writes. |
| 2 | "Remember the plus one? Leave it out, and `dst` is one byte too small." | CodeWalker: `char *dst = malloc(strlen(src));` — `+ 1` is shown as a ghost, struck. The mint block shrinks to 5 cells and the strip appears (zoomed from the heap region). |
| 3 | "The copy runs one byte past the end. This is called a **buffer overflow**." | The five letters fill the block; the `\0` flies to the sixth cell, *outside* the block, landing on the neighbor cell. Red flash on that cell. Term unveil: *buffer overflow*. |
| 4 | "And that crashes right away, right?" | Student → excited (naively). |
| 5 | "Sometimes. That's the nasty part." | Professor → worried. Replay the landing three times, in a small row of three mini-strips labeled with numbers, each showing a different outcome: |
| 6 | "Depending on how `malloc()` is implemented, the program often runs seemingly fine. The byte might land in the padding the library added." | Mini 1: the extra byte lands in a grey hatched "padding" cell; nothing happens; a `tick_mark` (misleading) in `DIM`. |
| 7 | "Or on a variable nobody uses any more. Or on a variable that *is* in use." | Mini 2: lands on an unused cell (grey) fine. Mini 3: lands on a coral neighbor's cell and its value flickers (`7` → `0`); a red bolt. |
| 8 | "In the best cases, an overflow is harmless. In others, it is the root of many security vulnerabilities." | A `padlock` icon on the strip opens with a shake (a break-in, not an unlock); label "security hole" (font 22, `KERNEL_COLOR`). |
| 9 | "And here's the lesson again: even though it ran correctly once, it doesn't mean it's correct." | The three minis `FadeOut`. Hold 0.8 s. |

**Characters:** Student (excited → confused), Professor (worried).
**Ends with:** the strip fades; column back at normal state with the 5-cell mint block and its neighbor.
**Implementation notes:** reuse the `Padlock` from p07; the open animation reads as a break-in, not an unlock.

### S10 — Error 3: uninitialized read   (beats: B10) · ~0:30
**Purpose:** fresh heap memory holds leftover garbage.
**Starts with:** S09 end state.
**Layout:** column left; a fresh 4-cell block in the heap (gold). A variable `v` on the stack. A mini Terminal (2.2, −1.6), 4.6 × 1.0.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Third: you call `malloc()` correctly, but forget to put values in." | Chip 2 fades; chip `ERROR 3 · uninitialized read` writes. A gold 4-cell block slides out of the heap; the cells are blank-looking but have *ghost digits* (`7f3a`, `00c1`…) in `DIM`. |
| 2 | "Later, the program does an **uninitialized read**: it reads whatever happened to be on the heap." | Term note: *uninitialized read*. An arrow carries the ghost value from a cell into the stack variable `v`; `v` shows `0x7f3a`. |
| 3 | "If you're lucky, it's zero. If you're not, it's something random, and harmful." | The cell flips to `0` (a green `tick_mark`, `DIM`). Rewind: a different run, a different random value; the Terminal prints a different number each of two runs (`812734`, `-5`), in red. |

**Characters:** corner mode; Professor worried.
**Ends with:** the gold block with ghost digits, chip 3.

### S11 — Error 4: the memory leak   (beats: B11, first half) · ~0:40
**Purpose:** forgetting to free; long-running programs run out of memory; garbage collectors don't fix reference leaks.
**Starts with:** S10 end state, with the stack and heap reset to empty.
**Layout:** column left; CodeWalker (2.4, 1.0): `while (1) {` / `  char *p = malloc(1024);` / `  /* no free */` / `}`. Computer in the corner bottom-center (0.5, −2.7), scale 0.6, `idle`.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Fourth: forgetting to free. That's a **memory leak**." | Chip 3 fades; chip `ERROR 4 · memory leak` writes. Term unveil: *memory leak*. |
| 2 | "For a long-running program, like a web server, slow leaking eventually uses everything up. Then it must be restarted." | Bar loops lines 2–3. Each loop a block slides out of the heap region into the `free` space; the old pointer `p` is overwritten (the old arrow turns into a faint ghost, the block stays). Blocks accumulate faster each time (0.6 s → 0.2 s). The free region shrinks to nothing. Computer (bottom-center) fades in → busy → overwhelmed; a red flash at the full heap. |
| 3 | "But what about languages with a garbage collector? Don't they take care of this?" | Student → curious. |
| 4 | "Many newer languages do support **automatic memory management**: you ask for an object with something like `new`, but never free it." | Professor → explaining. (Spoken only, no term card.) The CodeWalker swaps to `obj = new Thing();`. |
| 5 | "A **garbage collector** runs, finds what has no references left, and frees it." | Term note: *garbage collector*. A broom glyph (a thin brush icon, simple lines) sweeps blocks with grey arrows (no pointer) into the free region. |
| 6 | "But note: if you still hold a reference to something, no collector will ever free it. So leaks remain a problem even in modern languages." | A block with a live coral arrow stays; the broom skips it; a tag "still referenced" (`DIM`); a small `x_mark` on the broom. |

**Characters:** Student (curious), Professor (explaining), Computer (idle → busy → overwhelmed).
**Ends with:** heap region partly full with a "still referenced" block; Computer fades out.
**Implementation notes:** the broom is a small new glyph (see New assets). The first heap-full flash is a simple recolor, no particles.

### S12 — When the process exits   (beats: B11, second half) · ~0:30
**Purpose:** short-lived programs don't leak for real; two levels of memory management.
**Starts with:** S11 end state, heap full of coral blocks and `free` empty (the leaky state from the previous scene).
**Layout:** column left; a `Process` (coral, `prog`) at the right (3.2, 0.5) running; an Aside card (right side, x 0..6.6) appears at the end.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "And in C? My little program never frees anything and it's fine." | Student → confused. The CodeWalker fades; a small coral `Process` "prog" hops in at the right, running. |
| 2 | "For a short-lived program, that can be reasonable. When the process dies, the OS takes back *all* of its pages: code, stack, and heap." | Professor → neutral. The Process turns done and puffs out. The column's code, heap, and stack regions all fade to hatched, then restore to empty (a `KERNEL_COLOR` bracket on the column labeled "the OS takes it all back"). |
| 3 | "Nothing is lost for good." | Hold 0.8 s; a `tick_mark` by the bracket. |
| 4 | "There are two levels of management: the OS hands memory to processes and takes it back when they exit. The second level lives *inside* each process, in `malloc()` and `free()`." | A thick `KERNEL_COLOR` frame appears around the *whole* column with a label "level 1 · the OS" (font 22); inside the heap region a thin `USER_COLOR` frame with "level 2 · malloc / free". Both labels fade in turn. |
| 5 | "Still, make freeing a habit. Good habits are what protect you in the long-running program." | Professor → worried. An **Aside card** "WHY NO MEMORY IS LEAKED ONCE YOUR PROCESS EXITS" slides in with a one-line body "The OS reclaims everything at exit." (6 words), slides out. |

**Characters:** Student (confused), Professor (neutral → worried).
**Ends with:** the empty column; chip 4 faded; frames faded.
**Implementation notes:** Aside card title is the book's; keep the body ≤ 8 words. The two frames fade together at the end.

### S13 — Errors 5, 6, 7: freeing wrongly   (beats: B12) · ~1:05
**Purpose:** dangling pointer, double free, invalid free: three mini-scenes in the same heap.
**Starts with:** S12 end state: empty column. The first mini-scene sets up its own state.
**Layout:** column left; CodeWalker (2.4, 1.3); error chip at (−3.6, −2.3); no Terminal.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Fifth: freeing too early." | Chip `ERROR 5 · freeing too early` writes. Code: `free(x);` / `*x = 5;`. A coral block with pointer `x` is drawn quickly (as in S07). |
| 2 | "You call `free()`, and then keep using the pointer. That's a **dangling pointer**." | Bar on line 1: block turns hatched grey; the arrow stays, dashed. Term note: *dangling pointer*. |
| 3 | "It still holds the old address, but the memory is no longer yours. The next use might crash." | Bar on line 2: a write packet flies along the dashed arrow into the grey block; red flash. |
| 4 | "Or, if you call `malloc()` again, the library may hand that same memory to someone else, and now two parts of your program are scribbling on each other." | New line `y = malloc(...)`. A mint pointer `y` appears; the same block turns mint; *two* arrows (coral dashed, mint solid) point at it; two values alternate (`5` / `9`) inside it. |
| 5 | "Sixth: freeing twice." | Error chip 5 fades; chip `ERROR 6 · double free` writes. Fresh column; a gold block; code `free(z);` / `free(z);`. |
| 6 | "A **double free**. The result is undefined." | Term note: *double free*. First `free(z)`: block hatched. Second: the bar re-lands; a "?" appears over the free region. |
| 7 | "The allocation library may get confused and do all sorts of weird things. Crashes are the common outcome." | The free-region cells scramble (small flickers), a crack glyph and a red flash. |
| 8 | "Seventh: calling `free()` incorrectly." | Chip 6 fades; chip `ERROR 7 · invalid free` writes. Code: `free(p + 3);` / `free(&n);`. |
| 9 | "`free()` expects a pointer that `malloc()` gave you. Anything else, and bad things happen. That's an **invalid free**." | Term note: *invalid free*. A heap block with pointer `p` (green outline `tick_mark` on the base address). Two calls: (a) pointer into the *middle* of the block; the call bounces off the block's interior with an `x_mark`; (b) the address of a stack variable `n`; bounces too. |
| 10 | "So that's seven ways to hurt myself with two functions." | Student → frustrated. The seven chip names fly into a small vertical list at the right (font 20) and stack: 1..7. |
| 11 | "Seven ways. And you've heard all of them now." | Professor → happy. Hold 1.2 s. |

**Characters:** Student (frustrated), Professor (happy).
**Ends with:** list of seven errors at the right (x 3.6..6.6, y −1.8..2.0, font 20); column empty.
**Implementation notes:** each mini-scene is ≤ 15 s; reset the column with a quick fade between them (not a cut). Row 10's list becomes the recap's error row in S17: keep it as one mobject.

### S14 — The tools   (beats: B13) · ~0:20
**Purpose:** purify and valgrind exist to find these errors.
**Starts with:** S13 end state (list of seven at right; column empty).
**Layout:** Terminal center (0, 0.4), 7 × 2.4; list of errors moves to the left side as a thin column.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "Because mistakes are so common, a whole ecosystem of tools exists to catch them." | Column and chips fade. Terminal `FadeIn`; it types `prompt> valgrind ./prog`. |
| 2 | "**Purify** and **valgrind** are two excellent ones." | Output lines print (3 lines): `Invalid write of size 1`, `definitely lost: 1,024 bytes`, `Invalid free()`. Each line gets a link icon to the error name in the list (a thin line to the matching list item, which pulses). A `magnifier_icon` scans the output. |
| 3 | "Once you get used to them, you'll wonder how you survived without them." | Professor → happy. Hold 0.8 s. |

**Characters:** Professor (happy), Student neutral.
**Ends with:** Terminal with report; everything fades at the next scene.
**Implementation notes:** "Purify" is named only in narration (no term card). Output text is illustrative, not copied from a real run.

### S15 — Under the hood: brk and mmap   (beats: B14) · ~1:05
**Purpose:** `malloc`/`free` are library calls on top of system calls that move the break or create anonymous regions.
**Starts with:** Terminal only; everything fades to empty (badge + crux strip stay).
**Layout:** a **User/Kernel boundary** at y = −0.9 (user above, kernel below), a Privilege gauge at (6.0, −0.9) (built at final size). The address-space column at left is scaled to 0.85 (height 3.6, center (−3.6, 0.8), spanning 2.6..−1.0) so it sits wholly in the user zone; the boundary line is drawn at y = −1.2 instead of −0.9. A "library box" (rounded rectangle, label `malloc / free`, `USER_COLOR` outline) wraps the heap region.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "You might have noticed we never mentioned *system calls*." | The column slides in; the boundary draws (`USER_COLOR` above, `KERNEL_COLOR` below), gauge shows USER. |
| 2 | "That's because `malloc()` and `free()` aren't system calls. They're *library* calls." | The library box draws around the heap region. `malloc` / `free` chips sit in it. A crossed-out `syscall` chip with an `x_mark` flashes under the boundary. |
| 3 | "The library manages space inside your virtual address space, but it is itself built on system calls that ask the OS for more memory, or hand some back." | A thin vertical arrow goes from the library box down toward the boundary, labeled "when it runs out". |
| 4 | "One is `brk`. It changes the location of the end of the heap, called the **break**." | Term note: *break*. A thin marker line (the "break") sits at the bottom of the heap region; label `break`. A packet `brk(new)` flies from the library box across the boundary (`UserKernelBoundary.cross`, gauge → KERNEL, flash), and returns; the break marker slides down by two cells and the heap region grows into `free`. |
| 5 | "Give it a new address, and the heap grows, or shrinks." | The break marker moves down, then up again (shrink), each time with the region's color following. |
| 6 | "A cousin, `sbrk`, takes an increment instead. You should never call either yourself: let the library do it, or you'll make something go horribly wrong." | A chip `sbrk(+n)` appears next to `brk(new)`; both get a `stop_sign_tag` with "don't call directly". |
| 7 | "There's another way to get memory from the OS: `mmap()`." | A chip `mmap()` crosses the boundary the same way; gauge flips and returns. |
| 8 | "It can create an **anonymous** region inside your program, one that isn't tied to any file, but to swap space, something we'll see later." | Term note: *anonymous region*. A new block appears in the `free` area, labeled "anonymous"; a dashed link to a small `Disk` icon labeled "swap space" in the kernel zone at (4.0, −2.4) with an `ep_tag("→ later")`. |
| 9 | "You can then treat it like a heap and manage it." | The anonymous block shows a heap-like block sliding out inside it. |
| 10 | "So when I call `malloc()`, the OS isn't even involved?" | Student → curious. |
| 11 | "Often not. The library hands out pieces of what it already has, and only asks the OS when it runs out." | Professor → explaining. Three quick `malloc` calls: packets stay inside the library box and blocks appear without any crossing; then one big request crosses. |

**Characters:** Student (curious), Professor (explaining).
**Ends with:** column with the library box, break marker, anonymous block, swap disk, boundary and gauge. Everything fades next scene except badge and strip.
**Implementation notes:** `PrivilegeGauge` must be built at its final size (no scaling after creation). The scaled column keeps address labels readable (font 16); check with `OSTEP_CHECK`.

### S16 — calloc() and realloc()   (beats: B15) · ~0:30
**Purpose:** two more calls, for zeroed memory and for growing a block.
**Starts with:** empty (badge + strip).
**Layout:** column at left (back to scale 1.0, (−3.6, 0.3)) with a coral 4-cell block; CodeWalker (2.4, 1.3).

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "A couple more calls, briefly. `calloc()` allocates *and* zeroes the memory before it returns, which prevents the uninitialized reads we saw earlier." | The column fades in. Code: `int *a = calloc(4, sizeof(int));` A mint 4-cell block slides out, cells filling with `0 0 0 0` in sequence; a small `tick_mark`. |
| 2 | "And `realloc()` is for when your array needs to grow." | Code: `a = realloc(a, 8 * sizeof(int));`. The mint block's right neighbor is a coral block (no room to grow). |
| 3 | "It makes a new, larger region, copies the old one into it, and returns a pointer to the new region." | A new 8-cell block (mint) appears in free space below; the four values flow across (`MoveAlongPath`); the old block turns hatched grey; the arrow from `a` moves to the new block. |

**Characters:** corner mode; Student nods (neutral).
**Ends with:** the column with the new block. Fades.
**Implementation notes:** no term card for `calloc`/`realloc` (names only), consistent with the script.

### S17 — Recap   (beats: B16) · ~0:35
**Purpose:** four takeaways.
**Starts with:** empty (badge + strip).
**Layout:** header "Recap" in `VIRT` at (−4.2, 2.2); numbered list at left (font 26) x −5.6..1; icon per line at x = 4.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "So, today:" | Header "Recap" writes. |
| 2 | "The **stack** is automatic: the compiler allocates when you call, and frees when you return. The **heap** is explicit: you `malloc()` and you `free()`." | Line 1: "stack: automatic · heap: explicit". Icon: the stack/heap column (mini). |
| 3 | "Use `sizeof()`, and remember it measures the type, not what the pointer points to. Strings need `strlen() + 1`." | Line 2: "sizeof(type), strlen + 1". Icon: a small ruler over a pointer. |
| 4 | "Seven classic errors: forgetting to allocate, too little, uninitialized, leaks, dangling pointers, double frees, invalid frees." | Line 3: "7 classic errors". Icon: the seven-item list from S13 (small). |
| 5 | "`malloc()` and `free()` are library calls, built on `brk` and `mmap()`. Tools like valgrind help you find the rest." | Line 4: "library calls over brk / mmap". Icon: the magnifier. Hold 1.5 s. |

**Ends with:** the recap list; section badge and crux strip fade out.

### S18 — Teaser: is that address real?   (beats: B17) · ~0:30
**Purpose:** hook for 15: the addresses a program sees are virtual.
**Starts with:** S17 end state (badge faded).
**Layout:** dialogue mode (Student (−2.6, −1.2), Professor (2.6, −1.2), scale 1). A mini Terminal at the top-left content zone (−3.6, 1.8), 5 × 1.0.

| # | Narration | On screen / animation |
|---|---|---|
| 1 | "One more thing. When I print the pointer `x` from `malloc()`, I get an address. A real address in memory?" | Recap fades; characters move to dialogue mode; Student → curious. The Terminal prints `prompt> ./prog` → `x = 0x1a2b3c4`. |
| 2 | "Great question. Remember `va.c` from episode 13, the program that printed the addresses of its code, heap and stack? Every address your program prints is a *virtual* address." | Professor → thinking. A small `va.c`-style stamp "virtual" (13's stamp helper) lands on the address. The `IllusionSplit` draws (vertical, titles "What the program sees" / "What really happens"); the address moves to the left half, inside a small Memory column. |
| 3 | "The program thinks the heap lives right there. The hardware knows better." | On the right half a physical Memory column appears; a dotted arrow from the address bounces to a *different* spot with a "?". |
| 4 | "Next time: how does the hardware turn a virtual address into a real one? Address translation." | Professor → happy. Text "address translation" writes at the center; everything `FadeOut` (0.5 s); end card "Next: 15 · Address Translation" (with a `VIRT` dot) holds for 2 s. |

**Characters:** Student (curious), Professor (thinking → happy).
**Ends with:** black end card.

## New assets needed
- **`broom_glyph` / `GarbageCollector`** (S11): a small broom icon (a stick + bristle fan, simple lines) with `.sweep(blocks, to)` returning an animation; skips blocks that have a live pointer. Suggested in `p14_icons.py`.
- **`HeapDemo` / allocation helpers** (S03–S13, S16): small helpers on top of `Memory` so scenes don't redo the same work: `stack_frame(name, cells)`, `heap_block(n, color)`, `slide_out_of(region)`, `free_block(block)` (hatched grey, returns to `free`), `pointer_arrow(cell, block, color, dashed=False)`, `scramble(block)` (ghost digits). Keep them as functions in `p14_heap.py`, no new classes needed except an optional `HeapBlock` (VGroup of cells with `.size`, `.free()`, `.set_cells()`).
- **`ErrorChip(n, name)`** (S08–S13): small numbered chip with `.swap_to(n, name)`.
- **Break marker** (S15): a thin line with a `break` label and `.move_to_cell(i)`; usable as part of `p14_heap.py`.
- **Man-page card** (S05): rounded rectangle with a header `man malloc` and mono lines; use `FileIcon`-style rectangle (no new class needed if built ad hoc).
- Existing, reused as-is: `Memory`, `CodeWalker`, `Terminal`, `UserKernelBoundary`, `PrivilegeGauge`, `Padlock` (p07), `magnifier_icon`, `stop_sign_tag`, `program_chip`, `hatch_rect`, `IllusionSplit`, `ep_tag`. No new character expressions are needed.

## Open questions
- **Key terms:** unveils are heap, malloc(), buffer overflow, memory leak. Swap one (e.g. segmentation fault or dangling pointer) if you prefer.
- **Length:** ~14:00. Trim candidates: S14 (tools, 0:20), S16 (calloc/realloc, 0:30), the garbage-collector rows in S11 (≈ 0:20), the three-outcome minis in S09.
- **Broom glyph:** keep the garbage-collector broom, or leave the collector as text only?
- **Computer in S11:** one appearance at bottom center, since corners are taken by the Student and Professor. OK, or skip the Computer?
- **Error chip count:** the chip with numbers 1 to 7 is my device; the book does not number the errors.
