"""Continuity check between consecutive scenes of an episode (no image reading needed).

    python tools/continuity.py 01-03            # all boundaries, draft renders
    python tools/continuity.py 04 --threshold 0.1 -q h

For every boundary it compares the LAST frame of scene N with the FIRST frame of scene N+1 in
Ostep/Renders/<ep>/<quality>/scenes/ and prints the share of pixels that changed, plus the
bounding box of the change (in frame units, x in [-7.1, 7.1], y in [-4, 4]).  A scene that starts
exactly where the previous one ended gives ~0 %.  Anything above the threshold is a "jump":
characters or props that are not in the same place, scale or expression.  Deliberate cuts
(a scene that starts from an empty screen, or a title card) show up too: ignore those.

Exit code is 0 either way; read the table.
"""
import argparse
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
RENDERS = ROOT / "Ostep" / "Renders"
QUALITY = {"l": "480p15", "m": "720p30", "h": "1080p60"}
TMP = ROOT / ".cache" / "continuity"
PIX_TOL = 24          # per-channel difference that counts as "changed"


def resolve(ep):
    hits = sorted(p.name for p in RENDERS.iterdir() if p.is_dir() and p.name.startswith(ep))
    if not hits:
        sys.exit(f"no renders for {ep}")
    return hits[0]


def frame(video: Path, out: Path, last: bool):
    out.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["ffmpeg", "-y", "-loglevel", "error"]
    cmd += ["-sseof", "-0.2"] if last else ["-ss", "0"]
    cmd += ["-i", str(video), "-update", "1", "-frames:v", "1", str(out)]
    subprocess.run(cmd, check=True)
    return np.asarray(Image.open(out).convert("RGB")).astype(int)


def last_frame(video: Path, out: Path):
    # -sseof lands on the last frames; keep the final one written
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-sseof", "-0.2", "-i", str(video),
                    "-update", "1", str(out)], check=True)
    return np.asarray(Image.open(out).convert("RGB")).astype(int)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("episode")
    ap.add_argument("-q", "--quality", default="l", choices=QUALITY)
    ap.add_argument("--threshold", type=float, default=0.15, help="flag boundaries above this %% of pixels")
    ap.add_argument("--clusters", type=int, default=3, help="blobs to list per flagged boundary")
    ap.add_argument("--dir", help="folder of scene mp4s (default: the episode's Renders scenes folder)")
    a = ap.parse_args()

    if a.dir:
        ep, folder = Path(a.dir).name, Path(a.dir)
    else:
        ep = resolve(a.episode)
        folder = RENDERS / ep / QUALITY[a.quality] / "scenes"
    scenes = sorted(folder.glob("s*.mp4"))
    if len(scenes) < 2:
        sys.exit("need at least two rendered scenes")
    print(f"{ep}: {len(scenes) - 1} boundaries, flag > {a.threshold}% changed pixels\n")
    flagged = 0
    for prev, nxt in zip(scenes, scenes[1:]):
        end = last_frame(prev, TMP / "end.png")
        start = frame(nxt, TMP / "start.png", last=False)
        if end.shape != start.shape:
            print(f"{prev.stem} -> {nxt.stem}: size differs, skipped")
            continue
        diff = (np.abs(end - start).max(axis=2) > PIX_TOL)
        pct = 100.0 * diff.mean()
        flag = "  <-- JUMP" if pct > a.threshold else ""
        flagged += bool(flag)
        print(f"{prev.stem:32s} -> {nxt.stem:32s} {pct:6.2f}%{flag}")
        if flag:
            for box, share in clusters(diff)[:a.clusters]:
                print(f"{'':34s}  {share:5.2f}%  {box}")
    print(f"\n{flagged} boundary(ies) above the threshold")


def clusters(diff, grow=9):
    """Connected blobs of changed pixels (dilated so a glyph or a body is one blob),
    biggest first, as ('x[..] y[..]', share of the frame in %) with frame units."""
    from scipy import ndimage
    h, w = diff.shape
    blobs, n = ndimage.label(ndimage.binary_dilation(diff, iterations=grow))
    fw, fh = 14.222, 8.0
    out = []
    for i, sl in enumerate(ndimage.find_objects(blobs), start=1):
        ys, xs = sl
        n_px = int(diff[sl][blobs[sl] == i].sum())
        if n_px < 12:
            continue
        box = (f"x[{(xs.start / w - 0.5) * fw:5.1f},{(xs.stop / w - 0.5) * fw:5.1f}] "
               f"y[{(0.5 - ys.stop / h) * fh:5.1f},{(0.5 - ys.start / h) * fh:5.1f}]")
        out.append((box, 100.0 * n_px / (h * w)))
    return sorted(out, key=lambda t: -t[1])


if __name__ == "__main__":
    main()
