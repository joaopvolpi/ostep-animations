---
name: ostep-script
description: Turn an OSTEP book chapter (PDF in Ostep/Chapters) into a narrated, storytelling-style explanation script for the animated OS video series. Use when the user asks to write/generate/draft the script for a chapter (by number, slug or title), e.g. "write the script for chapter 7" or "/ostep-script 04".
---

# OSTEP chapter → explanation script

You turn one chapter of *Operating Systems: Three Easy Pieces* into the narration script for
one episode of the series. The output is what the audience **hears**, organized into beats,
plus light notes on what the beat should *show*. Detailed visuals come later, from the
`ostep-scenes` skill.

## Inputs

- The argument identifies the chapter: a number (`7`, `07`), a slug (`cpu-sched`), or a title.
  Resolve it with `Ostep/Chapters/INDEX.md`. If it's ambiguous, ask.
- Read **all** of these before writing:
  1. `Ostep/README.md`, the series bible (voice, episode arc, characters, props). Follow it.
  2. The chapter PDF in `Ostep/Chapters/` (read every page; use the `pages` parameter for long PDFs).
  3. The previous episode's script in `Ostep/Scripts/`, if one exists, so you can make callbacks
     and avoid re-explaining. Also skim `INDEX.md` for the next chapter's title (for the teaser).
  4. Any user notes in `scripts/` that relate to this chapter.

## Process

1. **Extract the content skeleton** (keep it in your head or in the Notes section; don't
   narrate yet):
   - Every **CRUX**, key term (with the book's definition), mechanism, policy, and example with
     its numbers. Also every aside/tip worth keeping.
   - The **dependency order**: which ideas need which other ideas.
   - What to **cut or defer**: homework, references, very deep tangents. List them in the output.
2. **Find the story.** Pick the central tension, usually the main crux. Then plan the arc from the
   bible: cold open → crux → build-up (naive attempt → failure → better idea, repeated) →
   big picture → recap → teaser. Each concept must enter as the answer to a felt problem.
3. **Write beats.** A beat is one idea, ~15–60 s of narration. For each beat:
   - Narration in the Professor's voice (V.O.), or dialogue lines when characters are on screen.
   - The Student interrupts where a viewer would be confused or skeptical.
   - **The crux is narration.** Every crux that appears on screen is read aloud (and so captioned),
     word for word as it is written on the card: "The crux:" + the question + the follow-up text. The
     blockquote under the beat title is what the card shows; write the same words as a Narrator
     line, then carry on from them. Don't paraphrase the crux, and don't skip it. This holds for
     every crux in the episode, including a second or third one.
   - Give concrete numbers before general rules. Introduce one new term at a time, and write it in
     **bold** the first time.
   - Add a short `Visual idea:` line (one or two sentences, referencing props from the bible where
     possible). Don't over-specify; that's the scene skill's job.
4. **Dialogue chapters** (`*-dialogue-*`, `*-dialogue`): keep the book's Professor/Student
   exchange as the core and tighten it. Add Computer/Process reactions. Target 2–4 minutes.
5. **Self-check** before saving:
   - Is every key term and crux from the chapter present, or explicitly listed as cut?
   - Is anything contradicting or overstating the book? Simplifications should be flagged in
     narration.
   - Could a viewer who only watched earlier episodes follow it?
   - Read the narration "aloud": short sentences, spoken rhythm, no walls of jargon.
   - Estimated duration fits the bible's target (≈150 spoken words per minute).

## Output

Write `Ostep/Scripts/<NN-slug>.md` (same prefix and slug as the PDF). If the file exists, ask
before overwriting. Use this structure:

```markdown
# <NN> — <Chapter title>
> Section: <Virtualization|Concurrency|Persistence|Security|Intro|Distribution> · Source: Ostep/Chapters/<file>.pdf · Est. duration: <mm:ss> (<word count> words)

## Logline
One or two sentences: the problem and the payoff of this episode.

## Learning goals
- After watching, the viewer can …  (3–5 bullets)

## Concepts covered
| Term | Definition (book's wording or faithful paraphrase) | Beat |

## Script

### B01 — <beat title>  `cold open` (~0:30)
**Narrator (V.O.):** …
**Student** (curious): …
**Professor** (explaining): …
*Visual idea:* …

### B02 — The Crux  `crux`
> **THE CRUX:** <the question, from the book>
> <the book's follow-up text, abridged to what fits on a card (≤ ~25 words)>
**Narrator (V.O.):** The crux: <the question, read verbatim>. <the follow-up text, read verbatim> …

(… more beats, each tagged with its arc stage: cold open | crux | build-up | big picture | recap | teaser)

## Cut / deferred material
- <what was left out and why, or which later episode covers it>

## Callbacks & setups
- Callbacks to earlier episodes: …
- Setups paid off in later episodes: …

## Open questions
- Anything you were unsure about, for the user to decide.
```

Character lines must use only the expressions listed in the bible. When you finish, tell the
user the file path, the estimated duration, the beat list (one line each), and the open questions.
