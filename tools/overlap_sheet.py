"""Contact sheets of the layout check's findings, for a quick visual review (one image, many crops).

    python tools/overlap_sheet.py 05                     # all findings of episode 05
    python tools/overlap_sheet.py 05 --scenes S07,S10    # only some scenes
    python tools/overlap_sheet.py 05 --kinds cover,edge  # only some kinds

Reads the findings that ``tools/render.py`` saved in Ostep/Renders/<ep>/<quality>/layout/*.jsonl
(one JSON per finding: scene, t, kind, a, b, box in frame units), grabs the frame at each finding's
time (+0.15 s) from the scene video, crops around the box (red outline) and tiles the crops,
numbered, into sheets of ``--per-sheet`` crops: Ostep/Renders/<ep>/<quality>/layout/sheet_<n>.png.
It prints the numbered list so each crop can be matched to its finding.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
RENDERS = ROOT / "Ostep" / "Renders"
QUALITY = {"l": "480p15", "m": "720p30", "h": "1080p60"}
FW, FH = 14.222, 8.0
TILE = (420, 260)


def frame(video, t, out):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", str(video), "-frames:v", "1", str(out)],
                   check=True)
    return Image.open(out).convert("RGB")


def crop(img, box, pad=1.0):
    W, H = img.size
    sx, sy = W / FW, H / FH

    def px(x, y):
        return (x + FW / 2) * sx, (FH / 2 - y) * sy
    x0, y1 = px(box[0], box[1])
    x1, y0 = px(box[2], box[3])
    d = ImageDraw.Draw(img)
    d.rectangle([x0 - 2, y0 - 2, x1 + 2, y1 + 2], outline=(255, 40, 40), width=2)
    # keep the tile's aspect ratio around the box
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    w = max(x1 - x0 + 2 * pad * sx, 3.2 * sx)
    h = max(y1 - y0 + 2 * pad * sy, w * TILE[1] / TILE[0])
    w = max(w, h * TILE[0] / TILE[1])
    c = img.crop((int(cx - w / 2), int(cy - h / 2), int(cx + w / 2), int(cy + h / 2)))
    return c.resize(TILE)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("episode")
    ap.add_argument("-q", default="l")
    ap.add_argument("--scenes")
    ap.add_argument("--kinds")
    ap.add_argument("--per-sheet", type=int, default=12)
    a = ap.parse_args()
    eps = [p for p in RENDERS.iterdir() if p.is_dir() and p.name.startswith(a.episode)]
    if not eps:
        sys.exit(f"no renders for {a.episode}")
    base = eps[0] / QUALITY[a.q]
    logdir = base / "layout"
    recs = []
    for f in sorted(logdir.glob("*.jsonl")):
        for line in f.read_text(encoding="utf-8").splitlines():
            if line.strip():
                r = json.loads(line)
                r["stem"] = f.stem
                recs.append(r)
    if a.scenes:
        want = {s.strip().upper() for s in a.scenes.split(",")}
        recs = [r for r in recs if r["stem"][:3].upper() in want]
    if a.kinds:
        kinds = set(a.kinds.split(","))
        recs = [r for r in recs if r["kind"].split(":")[0] in kinds]
    if not recs:
        print("no findings")
        return
    tmp = logdir / "_frame.png"
    try:
        font = ImageFont.truetype("arial.ttf", 22)
    except OSError:
        font = ImageFont.load_default()
    cols = 3
    for s in range(0, len(recs), a.per_sheet):
        chunk = recs[s:s + a.per_sheet]
        rows = (len(chunk) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * TILE[0], rows * TILE[1]), (0, 0, 0))
        for k, r in enumerate(chunk):
            n = s + k + 1
            img = frame(base / "scenes" / f"{r['stem']}.mp4", r["t"] + 0.15, tmp)
            tile = crop(img, r["box"])
            ImageDraw.Draw(tile).text((6, 4), str(n), fill=(255, 255, 0), font=font, stroke_width=2,
                                      stroke_fill=(0, 0, 0))
            sheet.paste(tile, ((k % cols) * TILE[0], (k // cols) * TILE[1]))
            print(f"{n:3d}. {r['stem']} t={r['t']}s [{r['kind']}] {r['a']} x {r['b']}")
        out = logdir / f"sheet_{s // a.per_sheet + 1}.png"
        sheet.save(out)
        print(f"   -> {out}")
    tmp.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
