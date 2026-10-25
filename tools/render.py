"""Render OSTEP episodes: Manim scenes -> Ostep/Renders, with optional burned-in captions.

Usage (from the project root):
    python tools/render.py 04                       # all scenes, draft (480p15), captions on, assembled
    python tools/render.py 04 --scenes S05-S07      # some scenes (no assembly unless --assemble)
    python tools/render.py 01-03 -q h               # final quality (1080p60)
    python tools/render.py 04 --no-captions         # clean video, no caption band
    python tools/render.py 04 --no-render           # re-caption / re-assemble existing renders only
    python tools/render.py 05 --check-only          # layout check only (Manim dry run: no video, faster)

Output, per episode and quality (e.g. Ostep/Renders/04-cpu-intro/480p15/):
    scenes/<stem>.mp4, scenes/<stem>.srt      clean Manim output + its subcaptions
    captioned/<stem>.mp4                      scene with the caption band (if captions)
    <episode>.mp4                             assembled episode (captioned unless --no-captions)
    <episode>.srt                             single-line captions for the whole episode
    layout/<stem>.jsonl                       layout-check findings (see ostep_lib/layout.py; review
                                              them with tools/overlap_sheet.py)

Captions: the animation is scaled to 90% and placed at the top of the frame; captions sit in the
band below it, so they can never overlap the animation. Each caption is one line (long narration
chunks are split and timed proportionally), in the series font (CMU Serif).
"""
from __future__ import annotations

import argparse
import time
import contextlib
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIM_DIR = ROOT / "Ostep" / "Manim"
RENDERS = ROOT / "Ostep" / "Renders"
CACHE = ROOT / ".cache"
QUALITY = {"l": "480p15", "m": "720p30", "h": "1080p60", "k": "2160p60"}

# Caption layout (fractions of the output frame)
CONTENT_SCALE = 0.90          # animation size inside the frame
TOP_MARGIN = 0.012            # gap above the animation
FONT_FRAC = 0.047             # caption font size / frame height
MAX_LINE_FRAC = 0.92          # max caption width / frame width
TEXT_COLOR = "ECECEC"         # style.TEXT
BG_COLOR = "1C1C1C"           # style.BG
FONT_NAME = "CMU Serif"
FONT_FILE = "cmunrm.otf"
LAYOUT_WARNINGS: list[str] = []   # filled by render_scene, summarized at the end


# --------------------------------------------------------------------------- helpers
def run(cmd, **kw):
    r = subprocess.run(cmd, cwd=ROOT, **kw)
    if r.returncode:
        sys.exit(f"command failed ({r.returncode}): {' '.join(map(str, cmd))}")
    return r


def even(x: float) -> int:
    return int(round(x / 2)) * 2


def probe(path: Path, entries: str) -> list[str]:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", entries,
         "-of", "csv=p=0", str(path)], capture_output=True, text=True, cwd=ROOT).stdout
    return out.strip().split(",")


def duration(path: Path) -> float:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", str(path)], capture_output=True, text=True).stdout
    return float(out.strip())


def resolve_episode(arg: str) -> str:
    eps = sorted(p.name for p in MANIM_DIR.iterdir() if p.is_dir())
    hits = [e for e in eps if e == arg or e.startswith(arg)]
    if len(hits) != 1:
        sys.exit(f"episode '{arg}' matches {hits or 'nothing'}; available: {eps}")
    return hits[0]


def scene_files(ep: str, selection: str | None) -> list[tuple[str, Path, str]]:
    """[(scene_id 'S05', file, class_name)] in order, filtered by selection."""
    out = []
    for f in sorted((MANIM_DIR / ep).glob("s[0-9][0-9]_*.py")):
        m = re.search(r"^class\s+(S\d+\w*)\s*\(", f.read_text(encoding="utf-8-sig"), re.M)
        if not m:
            print(f"! no scene class in {f.name}, skipped")
            continue
        out.append((f"S{f.name[1:3]}", f, m.group(1)))
    if selection:
        wanted = set()
        for part in selection.upper().split(","):
            a, _, b = part.partition("-")
            lo, hi = int(a.strip()[1:]), int((b or a).strip()[1:])
            wanted |= {f"S{i:02d}" for i in range(lo, hi + 1)}
        out = [s for s in out if s[0] in wanted]
    return out


# --------------------------------------------------------------------------- captions
def parse_srt(path: Path) -> list[tuple[float, float, str]]:
    def t(s):
        h, m, rest = s.strip().split(":")
        sec, ms = rest.split(",")
        return int(h) * 3600 + int(m) * 60 + int(sec) + int(ms) / 1000
    entries = []
    for block in re.split(r"\n\s*\n", path.read_text(encoding="utf-8-sig").strip()):
        lines = block.strip().splitlines()
        if len(lines) >= 3 and "-->" in lines[1]:
            a, b = lines[1].split("-->")
            entries.append((t(a), t(b), " ".join(l.strip() for l in lines[2:])))
    return entries


class LineSplitter:
    """Splits text into single caption lines that fit the frame, measured with the real font."""

    def __init__(self, width: int, height: int):
        from PIL import ImageFont
        self.size = max(12, round(height * FONT_FRAC))
        self.max_w = width * MAX_LINE_FRAC
        self.font = ImageFont.truetype(str(font_dir() / FONT_FILE), self.size)

    def fits(self, s: str) -> bool:
        return self.font.getlength(s) <= self.max_w

    def split(self, text: str) -> list[str]:
        words, lines, cur = text.split(), [], ""
        for w in words:
            cand = f"{cur} {w}".strip()
            if self.fits(cand):
                cur = cand
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        return self._balance(lines)

    def _balance(self, lines: list[str]) -> list[str]:
        # Avoid a tiny dangling last line: move words from the previous line while both fit.
        if len(lines) >= 2 and len(lines[-1].split()) <= 2:
            prev, last = lines[-2].split(), lines[-1].split()
            while len(prev) > 3 and self.fits(" ".join([prev[-1]] + last)):
                last.insert(0, prev.pop())
                if len(last) > len(prev):
                    break
            lines[-2:] = [" ".join(prev), " ".join(last)]
        return lines


def single_line_entries(entries, splitter: LineSplitter):
    out = []
    for a, b, text in sorted(entries):
        lines = splitter.split(text)
        total = sum(len(l) for l in lines) or 1
        t = a
        for l in lines:
            d = (b - a) * len(l) / total
            out.append((t, t + d, l))
            t += d
    # Manim's subcaptions can overlap by a frame or two; two live events make libass stack
    # them (pushing one up into the animation). Clamp so captions never overlap.
    for i in range(len(out) - 1):
        a, b, t = out[i]
        nxt = out[i + 1][0]
        if b > nxt:
            out[i] = (a, max(a, nxt), t)
    return [e for e in out if e[1] - e[0] > 0.01]


def fmt_srt(t: float) -> str:
    ms = int(round(t * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def fmt_ass(t: float) -> str:
    cs = int(round(t * 100))
    return f"{cs // 360000}:{cs // 6000 % 60:02d}:{cs // 100 % 60:02d}.{cs % 100:02d}"


def write_srt(path: Path, entries):
    path.write_text("".join(f"{i}\n{fmt_srt(a)} --> {fmt_srt(b)}\n{t}\n\n"
                            for i, (a, b, t) in enumerate(entries, 1)), encoding="utf-8")


def write_ass(path: Path, entries, width: int, height: int, size: int, band_top: int):
    margin_v = max(2, round((height - band_top - size) / 2))
    rgb = TEXT_COLOR
    color = f"&H00{rgb[4:6]}{rgb[2:4]}{rgb[0:2]}"
    head = (
        "[Script Info]\nScriptType: v4.00+\nWrapStyle: 2\nScaledBorderAndShadow: yes\n"
        f"PlayResX: {width}\nPlayResY: {height}\n\n"
        "[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, "
        "BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, "
        "Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
        f"Style: Cap,{FONT_NAME},{size},{color},{color},&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,"
        f"0,0,2,10,10,{margin_v},1\n\n"
        "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
    # Fixed position per line (bottom-center anchor): libass never collision-shifts it.
    pos = f"{{\\an2\\pos({width // 2},{height - margin_v})}}"
    body = "".join(f"Dialogue: 0,{fmt_ass(a)},{fmt_ass(b)},Cap,,0,0,0,,{pos}"
                   f"{t.replace('{', '(').replace('}', ')')}\n"
                   for a, b, t in entries)
    path.write_text(head + body, encoding="utf-8")


def font_dir() -> Path:
    """A folder with the CMU font files for libass/PIL (copied once into .cache/fonts)."""
    d = CACHE / "fonts"
    if not (d / FONT_FILE).exists():
        d.mkdir(parents=True, exist_ok=True)
        for src in (Path(os.environ.get("LOCALAPPDATA", "")) / "Microsoft/Windows/Fonts",
                    Path(os.environ.get("LOCALAPPDATA", "")) / "Programs/MiKTeX/fonts/opentype/public/cm-unicode"):
            if (src / FONT_FILE).exists():
                for f in src.glob("cmun*.otf"):
                    shutil.copy2(f, d / f.name)
                break
        else:
            sys.exit("CMU Serif (cmunrm.otf) not found; install MiKTeX package cm-unicode")
    return d


def caption_video(src: Path, srt: Path, dst: Path, single_srt_out: Path | None = None):
    w, h = map(int, probe(src, "stream=width,height"))
    cw, ch = even(w * CONTENT_SCALE), even(h * CONTENT_SCALE)
    x, y = even((w - cw) / 2), even(h * TOP_MARGIN)
    splitter = LineSplitter(w, h)
    entries = single_line_entries(parse_srt(srt), splitter) if srt.exists() else []
    if not srt.exists():
        print(f"! {src.name}: no subtitles found, adding an empty caption band")
    if single_srt_out:
        write_srt(single_srt_out, entries)
    ass = CACHE / "ass" / (dst.stem + ".ass")
    ass.parent.mkdir(parents=True, exist_ok=True)
    write_ass(ass, entries, w, h, splitter.size, y + ch)
    rel = lambda p: p.resolve().relative_to(ROOT).as_posix()
    vf = (f"scale={cw}:{ch}:flags=lanczos,pad={w}:{h}:{x}:{y}:color=0x{BG_COLOR},"
          f"ass={rel(ass)}:fontsdir={rel(font_dir())}")
    dst.parent.mkdir(parents=True, exist_ok=True)
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(src), "-vf", vf, "-c:v", "libx264",
         "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p", "-an", str(dst)])


# --------------------------------------------------------------------------- render + assemble
@contextlib.contextmanager
def render_lock(stale=900):
    """One Manim render at a time across every render.py run (parallel agents run out of memory).
    The lock is a file holding the owner's pid; a lock older than ``stale`` seconds is taken over."""
    lock = CACHE / "render.lock"
    lock.parent.mkdir(parents=True, exist_ok=True)
    while True:
        try:
            fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(fd, str(os.getpid()).encode())
            os.close(fd)
            break
        except FileExistsError:
            try:
                if time.time() - lock.stat().st_mtime > stale:
                    lock.unlink(missing_ok=True)
                    continue
            except FileNotFoundError:
                continue
            time.sleep(2)
    try:
        yield
    finally:
        lock.unlink(missing_ok=True)


def render_scene(ep: str, f: Path, cls: str, q: str, out_scenes: Path, check_only=False):
    media = CACHE / "media" / ep
    # layout checks on: only their [bounds]/[overlap:*] lines are shown (Manim's log is noise).
    # No caching: cached animations skip their frames, and with them the mid-animation checks.
    log = out_scenes.parent / "layout" / f"{f.stem}.jsonl"
    log.unlink(missing_ok=True)
    cmd = [sys.executable, "-m", "manim", f"-q{q}", "--disable_caching", "--media_dir", str(media)]
    if check_only:
        cmd.append("--dry_run")
    with render_lock():
        r = subprocess.run(cmd + [str(f), cls],
                           cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace",
                           env={**os.environ, "OSTEP_CHECK": "1", "OSTEP_CHECK_LOG": str(log),
                                "PYTHONIOENCODING": "utf-8"})
    if r.returncode:
        print(r.stdout[-3000:], r.stderr[-6000:], sep="\n")
        sys.exit(f"manim failed on {f.name} ({r.returncode})")
    warnings = [l for l in r.stdout.splitlines() if l.startswith(("[bounds]", "[overlap", "[ghost]"))]
    for l in warnings:
        print(f"  {l}")
    LAYOUT_WARNINGS.extend(f"{f.stem}: {l}" for l in warnings)
    if check_only:
        return
    vid_dir = media / "videos" / f.stem / QUALITY[q]
    mp4, srt = vid_dir / f"{cls}.mp4", vid_dir / f"{cls}.srt"
    out_scenes.mkdir(parents=True, exist_ok=True)
    shutil.copy2(mp4, out_scenes / f"{f.stem}.mp4")
    if srt.exists():
        shutil.copy2(srt, out_scenes / f"{f.stem}.srt")
    else:
        (out_scenes / f"{f.stem}.srt").unlink(missing_ok=True)
        print(f"! {cls}: Manim wrote no subtitles")


def concat(files: list[Path], dst: Path):
    lst = CACHE / "concat" / (dst.stem + ".txt")
    lst.parent.mkdir(parents=True, exist_ok=True)
    lst.write_text("".join(f"file '{p.resolve().as_posix()}'\n" for p in files), encoding="utf-8")
    run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst),
         "-c", "copy", str(dst)])


def main():
    # Windows consoles are cp1252: never crash while printing a Manim traceback or a warning
    for s in (sys.stdout, sys.stderr):
        s.reconfigure(errors="replace")
    ap =argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("episode", help="episode folder or prefix, e.g. 04 or 01-03")
    ap.add_argument("--scenes", help="e.g. S05, S05-S07, S01,S09")
    ap.add_argument("-q", "--quality", default="l", choices=QUALITY, help="l=480p15 (draft), h=1080p60 (final)")
    cap = ap.add_mutually_exclusive_group()
    cap.add_argument("--captions", dest="captions", action="store_true", default=True, help="burn in captions (default)")
    cap.add_argument("--no-captions", dest="captions", action="store_false", help="clean video, no caption band")
    ap.add_argument("--no-render", action="store_true", help="reuse existing renders in Ostep/Renders")
    ap.add_argument("--assemble", action="store_true", help="assemble even when only some scenes are selected")
    ap.add_argument("--no-assemble", action="store_true")
    ap.add_argument("--check-only", action="store_true",
                    help="layout check only: Manim dry run, no video, no captions, no assembly")
    a = ap.parse_args()
    if a.check_only:
        a.captions, a.no_assemble = False, True

    ep = resolve_episode(a.episode)
    scenes = scene_files(ep, a.scenes)
    if not scenes:
        sys.exit("no scenes selected")
    out = RENDERS / ep / QUALITY[a.quality]
    out_scenes, out_cap = out / "scenes", out / "captioned"

    for sid, f, cls in scenes:
        print(f"== {sid} {cls}")
        if not a.no_render:
            render_scene(ep, f, cls, a.quality, out_scenes, a.check_only)
        if a.captions:
            src = out_scenes / f"{f.stem}.mp4"
            if not src.exists():
                sys.exit(f"missing {src}; render it first")
            caption_video(src, out_scenes / f"{f.stem}.srt", out_cap / f"{f.stem}.mp4")

    if not a.no_render:
        print(f"layout check: {len(LAYOUT_WARNINGS)} warning(s)"
              + (f" (review: python tools/overlap_sheet.py {a.episode})" if LAYOUT_WARNINGS else "")
              + "".join(f"\n  {w}" for w in LAYOUT_WARNINGS))

    full = a.scenes is None or a.assemble
    if full and not a.no_assemble:
        all_scenes = scene_files(ep, None)
        clean = [out_scenes / f"{f.stem}.mp4" for _, f, _ in all_scenes]
        missing = [p.name for p in clean if not p.exists()]
        if missing:
            print(f"! not assembling, missing scenes: {missing}")
            return
        parts = [out_cap / f"{f.stem}.mp4" for _, f, _ in all_scenes] if a.captions else clean
        missing = [p.name for p in parts if not p.exists()]
        if missing:
            print(f"! not assembling, missing captioned scenes: {missing} (run without --scenes)")
            return
        concat(parts, out / f"{ep}.mp4")
        # merged single-line subtitles for the whole episode
        splitter, merged, offset = None, [], 0.0
        for _, f, _ in all_scenes:
            v = out_scenes / f"{f.stem}.mp4"
            srt = out_scenes / f"{f.stem}.srt"
            if splitter is None:
                w, h = map(int, probe(v, "stream=width,height"))
                splitter = LineSplitter(w, h)
            if srt.exists():
                merged += [(s + offset, e + offset, t) for s, e, t in single_line_entries(parse_srt(srt), splitter)]
            offset += duration(v)
        write_srt(out / f"{ep}.srt", merged)
        print(f"episode: {out / f'{ep}.mp4'}  ({offset / 60:.1f} min, captions {'on' if a.captions else 'off'})")


if __name__ == "__main__":
    main()
