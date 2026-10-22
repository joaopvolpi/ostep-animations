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

Render an episode (output in `Ostep/Renders/<episode>/<quality>/`):
```
python tools/render.py 04                    # draft 480p, captions on, assembled episode
python tools/render.py 04 --scenes S05-S07   # just some scenes
python tools/render.py 04 -q h               # final 1080p60
python tools/render.py 04 --no-captions      # clean video without the caption band
python tools/render.py 04 --no-render        # re-caption / re-assemble existing renders
```
Captions are single-line, CMU Serif, in a band below the (90%-scaled) animation.
Re-download the book PDFs with `python tools/download_ostep.py Ostep/Chapters`.
