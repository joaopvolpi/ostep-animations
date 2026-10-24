"""Silence check per scene (text only, no frames): finds scenes that start or go quiet for too long.

    python tools/silence.py 04            # draft renders
    python tools/silence.py 04 --max-start 1.0 --max-gap 2.5 -q h

Reads the per-scene .srt files in Ostep/Renders/<ep>/<quality>/scenes/ and reports, for every scene,
(a) the first caption's start time (a scene must open with narration, <= --max-start s), and
(b) any gap between captions longer than --max-gap s, and (c) a silent tail after the last caption.
It also prints the last and first caption of consecutive scenes so you can read the hand-off
between them (does scene N+1 pick up where N left off?).
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RENDERS = ROOT / "Ostep" / "Renders"
QUALITY = {"l": "480p15", "m": "720p30", "h": "1080p60"}
T = re.compile(r"(\d+):(\d+):(\d+)[,.](\d+) --> (\d+):(\d+):(\d+)[,.](\d+)")


def secs(h, m, s, ms):
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000


def parse(path):
    out, cur = [], None
    for line in path.read_text(encoding="utf-8").splitlines():
        m = T.search(line)
        if m:
            g = m.groups()
            cur = [secs(*g[:4]), secs(*g[4:]), ""]
            out.append(cur)
        elif cur is not None and line.strip() and not line.strip().isdigit():
            cur[2] = (cur[2] + " " + line.strip()).strip()
    return out


def duration(video):
    try:
        r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                            str(video)], capture_output=True, text=True)
        return float(r.stdout.strip())
    except Exception:
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("episode")
    ap.add_argument("-q", default="l")
    ap.add_argument("--max-start", type=float, default=1.0)
    ap.add_argument("--max-gap", type=float, default=2.5)
    a = ap.parse_args()
    eps = [p for p in RENDERS.iterdir() if p.is_dir() and p.name.startswith(a.episode)]
    if not eps:
        sys.exit(f"no renders for {a.episode}")
    d = eps[0] / QUALITY[a.q] / "scenes"
    prev_last = None
    for srt in sorted(d.glob("*.srt")):
        caps = parse(srt)
        flags = []
        if not caps:
            print(f"{srt.stem}: NO CAPTIONS")
            prev_last = None
            continue
        if caps[0][0] > a.max_start:
            flags.append(f"opens silent for {caps[0][0]:.1f}s")
        for x, y in zip(caps, caps[1:]):
            if y[0] - x[1] > a.max_gap:
                flags.append(f"gap {y[0]-x[1]:.1f}s at {x[1]:.0f}s")
        dur = duration(srt.with_suffix(".mp4"))
        if dur and dur - caps[-1][1] > a.max_gap:
            flags.append(f"silent tail {dur-caps[-1][1]:.1f}s")
        print(f"{srt.stem}: {'; '.join(flags) if flags else 'ok'}")
        if prev_last:
            print(f"    hand-off: \"{prev_last[:70]}\" -> \"{caps[0][2][:70]}\"")
        prev_last = caps[-1][2]


if __name__ == "__main__":
    main()
