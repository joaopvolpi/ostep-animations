# OSTEP Animated — Series Guide

An educational video series on operating systems, adapted chapter by chapter from
*Operating Systems: Three Easy Pieces* (Remzi & Andrea Arpaci-Dusseau, v1.10, free at
https://pages.cs.wisc.edu/~remzi/OSTEP/), animated in the style of 3Blue1Brown with ManimCE.

This document is the **series bible**: the rules every script and every scene follows, so that
episodes feel like one series. Skills that write scripts and scenes must read it first.

---

## 1. Pipeline

```
Ostep/Chapters/NN-slug.pdf      the book chapter (source of truth for content)
        │  skill: ostep-script
        ▼
Ostep/Scripts/NN-slug.md        narrated explanation script (story + dialogue)
        │  skill: ostep-scenes
        ▼
Ostep/Scenes/NN-slug.md         scene breakdown: exactly what is on screen, and when
        │  skill: ostep-render
        ▼
Ostep/Manim/NN-slug/sXX_*.py    one Manim scene per file, using ostep_lib (style, characters, props)
        │
        ▼
Ostep/Renders/NN-slug/          assembled episode .mp4 + .srt subtitles from the narration
```

File names keep the chapter number and slug from `Ostep/Chapters/INDEX.md`
(e.g. `04-cpu-intro`). Front matter is `00a–00c`, appendices `A1–A8`.

## 2. What the series is

- **Audience:** curious programmers and CS students. They can read a little C, but they don't know
  OS internals. Assume no prior OS knowledge beyond earlier episodes.
- **Promise:** each episode makes one big idea feel *obvious in hindsight*. We show
  *why* the OS needs a mechanism before we show *what* the mechanism is.
- **Faithful to the book:** concepts, terminology, examples and numbers come from the chapter.
  We may re-order, simplify, or invent analogies, but we never contradict the book. When we
  simplify, the narration says so ("we're ignoring X for now").
- **Length:** ~8–15 min per regular chapter, ~2–4 min for the short *Dialogue* chapters,
  which become dialogue-only "cold opens" for a section.

## 3. Voice and storytelling

- **Narrator** = the Professor's voice in voice-over. When the Professor is on screen, the
  narration becomes dialogue. Tone: warm, precise, lightly witty (like the book). No hype.
- **Problem first.** Every concept appears as the answer to a problem the viewer already feels.
  The book's **THE CRUX** boxes are the backbone. Each crux is posed as an explicit question
  on screen, and the episode is the journey to its answer. **A crux on screen is always read
  aloud** (and so captioned), the question and follow-up text word for word as written on the card, inside a natural spoken
  lead-in ("So, the crux is: …", "Which brings us to…"), not a mechanical "The crux:" label every
  time. The crux is part of the narration, not a silent graphic.
- **The Student asks the viewer's questions** at the moment the viewer would ask them:
  confusion, objections, "wait, why not just…?". Naive ideas are welcome. We try them,
  watch them fail, and learn why.
- **Concrete before abstract:** a tiny example with real numbers (e.g. three jobs of 10 ms)
  before the general rule. Only then name the concept, and highlight the term on screen.
- **One idea per beat.** Never introduce two new terms in the same sentence.
- **Callbacks:** reuse metaphors and props from earlier episodes and say so ("remember our ready
  queue?"). Each episode ends with a recap and a hook into the next one.
- **Episode arc (default):**
  1. *Cold open:* a short hook. Use a puzzle, a paradox, or a dialogue moment.
  2. *The Crux:* the question card.
  3. *Build-up:* naive attempt → failure → better idea, repeated for each mechanism or policy.
  4. *The big picture:* how the pieces fit together.
  5. *Recap:* 3–5 key takeaways, shown as a list.
  6. *Teaser:* the next problem this creates.

## 4. Characters

Implemented in `ostep_lib/characters` (API in `ostep_lib/README.md`, visual reference in
`ostep_lib/characters/expression_sheet.png`). Use only the listed expressions. If a scene needs
a new one, add it to the library first.

| Character | Role | Personality | Expressions |
|---|---|---|---|
| **Professor** | The guide; the narrator when on screen. Mirrors the Professor in the book's dialogues. | Patient, wry, loves a good analogy; occasionally pleased with their own jokes. | neutral, explaining, happy, thinking, surprised, worried, proud |
| **Student** | The viewer's stand-in. Mirrors the Student in the dialogues. | Curious, a bit impatient, proposes naive solutions, celebrates "aha!" moments. | neutral, curious, confused, excited, sad, frustrated, surprised, bored |
| **Computer** | The machine itself: the hardware the OS manages. | Honest and literal. It does exactly what it's told and visibly suffers when misused. | idle, happy, busy, overwhelmed, sleeping, error, surprised |
| **Process** (many) | Running programs, as small colored blobs with a label (`A`, `B`, `PID 42`). | Each wants the CPU; they queue, run, block, and finish. | ready, running, blocked, done, zombie |

Usage rules:
- Characters are **commentators**: they appear at the edges (usually bottom corners) and react.
  The concept diagram owns the center of the screen.
- Professor and Student face each other in dialogue (Student on the left, Professor on the right).
- **Standard host positions** (library constants, in every episode): corner mode = scale 0.75 at
  (−5.8, −2.8) and (5.8, −2.8); dialogue mode = scale 1.0 at (−2.6, −1.2) and (2.6, −1.2). A character is
  positioned by a fixed design anchor, not by its bounding box, so the same position holds for every
  expression and scale. Use `host_pair` and `host_mode_anims`, and never redefine the positions.
- Use expressions to **mark the emotional beat**: confusion before an explanation, excitement at
  the payoff, worry when a design has a flaw.
- Processes are both characters and diagram elements. A process keeps the **same color and label
  throughout an episode** so viewers can track it.
- Later sections may add characters (for example threads as smaller "child" blobs of a process).
  Add them to the library and to this table.

## 5. Visual style

Palette constants live in `ostep_lib/style.py`. Never hard-code colors in scenes.

- **Background** `BG` (#1C1C1C), text `TEXT`, secondary text `DIM`.
- **Section accent** (matches the book's website): Virtualization `VIRT` orange,
  Concurrency `CONC` cyan, Persistence `PERS` green, Security `SEC` teal; intro/overview
  episodes use `INTRO` warm off-white (#E8E2D0), because the website's yellow is taken by the CPU. The accent colors the
  title card, the crux card frame and the section badge.
- **Concept colors** (consistent across the whole series):
  CPU = `CPU_COLOR` (yellow) · Memory = `MEM_COLOR` (blue) · Disk/storage = `DISK_COLOR` (green) ·
  Kernel / OS / privileged = `KERNEL_COLOR` (red) · User space = `USER_COLOR` (light blue).
- **Typography:** the series font is **Computer Modern** (`FONT = "CMU Serif"`), the TeX family
  3Blue1Brown uses, so `Text` and `MathTex` look like one family. Importing `ostep_lib` makes it the
  default for `Text`/`MarkupText`/`Paragraph`. Monospace (code, terminals, addresses) is
  `MONO_FONT = "CMU Typewriter Text"`. `Text` is for prose and labels, `MathTex` only for real
  formulas (e.g. turnaround time), `Code` for C snippets (monokai style, small, max ~12 lines on
  screen, font `MONO_FONT`). The fonts are installed per-user from MiKTeX's `cm-unicode` package.
  They lack ✓ ★ ≈ ↔. Use `tick_mark()`, `Star` or `MathTex` for those.
- **Motion:** smooth and purposeful, 3b1b-style. `Create`/`Write` for new things,
  `Transform` to show that one thing *becomes* another, `Indicate`/`Circumscribe` to point,
  `FadeOut` to clean up. Leave a pause (~1 s) after every key reveal. Never cut a diagram away
  abruptly. Transform it into the next one when possible.
- **Layout:** 16:9, keep a ~0.5 unit safe margin. Center = diagram; bottom corners = characters;
  top band = chrome only (see below). Avoid more than ~25 words of on-screen text at once.
- **Screen zones** (constants in `ostep_lib.props.core`; frame is x ∈ [−7.1, 7.1], y ∈ [−4, 4]):

  | Zone | Where | Holds |
  |---|---|---|
  | Chrome row | y ≈ 3.6 (`CHROME_ROW_Y`) | Section badge (left, from x = −6.6); docked term (right-aligned at x = 6.6, ≤ 2.6 wide). |
  | Crux strip | centered at y = 3.0 (`CRUX_STRIP_Y`), ≤ 8.2 wide | The docked crux question. |
  | Content | y ≤ 2.55 (`CONTENT_TOP`), x ∈ [−6.6, 6.6] | Everything else: diagrams, labels, scene titles, cards. |
  | Characters | bottom corners | Professor / Student / Computer. |

  **Introducing a key term** never shares space with the scene. `TermHighlight.show()` veils the
  whole scene with a scrim, writes the term large at the center, then lifts the veil while the
  term docks to the chrome row. Scene text never goes in the top band. Fade old labels out
  before new text lands where they were.

## 6. Recurring visual vocabulary ("props")

Concepts keep the **same visual form in every episode**. When a scene needs one of these, use it
as described. When a new recurring prop is invented, add it here.

| Prop | Look | Used for |
|---|---|---|
| **Crux card** | Rounded rectangle, accent-colored frame, small "THE CRUX" header, the question in bold, the follow-up in `DIM`. Read aloud as it writes (`say_crux`), then docks to a strip at y = 3.0. | The book's crux boxes; the central question of the episode or segment. |
| **Aside / Tip card** | Smaller card, `DIM` frame, "ASIDE" or "TIP" header; slides in from the side. | Book asides and tips; side notes that pause the main story. |
| **Term highlight** | Two strengths. **Unveil** (`terms.show`): the scene dims under a veil; the term is written large at the center, underlined in accent color, then docks top-right as the veil lifts. **Note** (`terms.note`): the term just slides into the top-right dock. | Unveil: only the episode's **3–4 key terms** (the ones the crux hinges on, e.g. *process*, *context switch*), never two in a row, and each term only once in the series (in the episode that teaches it). Note: every other new term. Minor vocabulary can simply be spoken and appear in the captions. |
| **CPU** | Yellow square chip with pins; the process currently running sits *on* it. | Anything that executes. Multiple chips for multi-CPU. |
| **Memory** | Tall blue column of stacked cells with addresses on the left (0 at top). | Physical memory, address spaces (code / heap / free / stack regions). |
| **Disk** | Green cylinder (platter seen at an angle). | Persistent storage, I/O. |
| **User/Kernel boundary** | Horizontal dashed line across the screen: user mode above (`USER_COLOR`), kernel mode below (`KERNEL_COLOR`). | System calls, traps, privilege. Crossing it is always animated. |
| **Timeline** | Horizontal time axis with colored blocks per process (Gantt chart). | Scheduling, time sharing, context switches. |
| **Queue** | Processes standing in a row with a label ("Ready queue"). | Ready / blocked queues, waiting for a lock. |
| **Illusion split** | Screen split: left "what the program sees" (virtual), right "what really happens" (physical). | Virtualization: CPU, memory. The series' signature motif. |
| **Code block** | `Code` mobject; the executing line is highlighted with a moving bar. | Showing real C from the book (`fork()`, `malloc()`...). |
| **Section badge** | Small top-left tag: section accent dot + chapter number + title. | Persistent orientation during the episode. |
| **System stack** | Hardware row (CPU, Memory, Disk) at the bottom, the OS as a `KERNEL_COLOR` band in the middle, Process creatures on top. | What the OS is; routing requests through the OS. |
| **Terminal** | Dark rounded console, `MONO_FONT`, prompt in `DIM`. | Running the book's example programs. |
| **Peach** | Peach-colored circle with a crease and a green leaf. | The book's virtualization metaphor; always the same design. |
| **Era ribbon** | Horizontal history ribbon with a sliding marker. | History segments. |
| **Privilege gauge** | Small vertical gauge reading USER / KERNEL. | Mode switches, next to the User/Kernel boundary. |
| **State diagram** | Figure 4.2: Running (with the CPU), Ready (a queue tray), Blocked (a clock), labeled arrows; can shrink to a corner legend with tracking dots. | Process states, everywhere after episode 04. |
| **PCB card** | Small card with a process-color header and fields (pid, state, …); a stack of them = the process list. | The OS's bookkeeping. |
| **Mechanism / policy icons** | Gears (and a robotic arm) = mechanism, *how*. A spotlight picking a process = policy, *which*. | Every time these two words come up. |
| **Save slot** | A floppy-like icon. | The register context: what's saved to pause and resume a process. |
| **OS token** | A small red "OS" badge (`KernelToken`) that rides on the CPU chip when the kernel is running. | Who is on the CPU: the OS or a process (traps, timer interrupts, context switches). |
| **Alarm clock** | `AlarmClock` that rings. | The timer interrupt, wherever it appears. |
| **Padlock** | `Padlock`: red when closed, green when open. | Assumptions, protection, locks: one padlock design for the series. |
| **MLFQ ladder** | `MLFQLadder`: stacked priority lanes, with jobs moving between them. | Multi-level queues (08, plus small versions in 10/11). |
| **Raffle drum** | `RaffleDrum` with process-colored `Ticket`s. | Proportional share and lottery (09, and 08's teaser). |
| **Cache CPU** | `CacheCPU`: a CPU chip with a small cache strip under it. | Caches, coherence and affinity (10); later TLBs. |
| **Eye** | `EyeIcon` with a moving pupil. | Watching or snooping, and "the program doesn't notice" (10–15). |
| **Metric readout** | `MetricReadout`: the average formula written term by term, with the final value boxed green or red. | Every scheduling metric (turnaround, response). |

**Timeline state encoding (series standard):** running = solid process color; ready = process-color
outline (fill 0.15); blocked = `DIM` at 0.35 with a clock; idle CPU = dark grey hatched;
CPU busy = `CPU_COLOR`; done = empty.

## 7. Writing conventions for scripts and scenes

- Scripts live in `Ostep/Scripts/`, scenes in `Ostep/Scenes/`. Both are Markdown.
- Narration lines are written exactly as they should be spoken. Write numbers the way they're said
  when that matters ("ten milliseconds").
- Characters' lines use `**Professor** (expression):` format.
- Each script beat has an ID (`B01`, `B02`...); scenes reference beats so the two files stay in sync.
- Each scene has an ID (`S01`...), an estimated duration, and a "state at end" so the next scene
  knows what is already on screen.
- **Continuity:** a scene starts exactly where the previous one ended (same positions, scale,
  expressions, docked term, crux strip). Only a deliberate cut may differ. `tools/continuity.py <NN>`
  compares the last frame of every scene with the first frame of the next and flags jumps.
- Anything uncertain or worth discussing goes in a final **Open questions** section rather than being guessed.
