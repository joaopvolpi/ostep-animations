# Animations

3Blue1Brown-style educational animations made with ManimCE (v0.19.1, Python 3.10).

- `Ostep/` — the OSTEP operating-systems series. **Start with `Ostep/README.md`** (series bible).
  - `Chapters/` — the book's chapters as numbered PDFs (`INDEX.md` lists them).
  - `Scripts/` — narrated scripts (made by the `ostep-script` skill).
  - `Scenes/` — scene breakdowns (made by the `ostep-scenes` skill).
- `ostep_lib/` — shared Manim code: palette (`style.py`) and characters. See `ostep_lib/README.md`.
  - `Manim/` — scene code per episode; `Renders/` — finished episodes (made by `ostep-render`).
- `.claude/skills/` — `ostep-script` (chapter → script), `ostep-scenes` (script → scenes),
  `ostep-render` (scenes → Manim code → video).
- `scripts/` — personal notes.

Render a scene: `python -m manim -ql <file.py> <SceneName>` (`-qh` for 1080p, `-p` to open after).
