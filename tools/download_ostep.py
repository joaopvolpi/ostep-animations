"""Download every OSTEP chapter PDF with the book's numbering.

Usage: python tools/download_ostep.py Ostep/Chapters
Front matter -> 00a..00c, numbered chapters -> 01..57, unnumbered appendices -> A1..A8.
"""
import re, sys, time, urllib.request
from pathlib import Path

BASE = "https://pages.cs.wisc.edu/~remzi/OSTEP/"
out = Path(sys.argv[1])
FRONT = {"dedication.pdf", "preface.pdf", "toc.pdf"}
out.mkdir(parents=True, exist_ok=True)

html = urllib.request.urlopen(BASE).read().decode("latin-1")
# Only the chapter table (starts at the "book-chapters" anchor)
html = html[html.index('name="book-chapters"'):]
html = html[: html.index("</table>")]

cells = re.findall(r"<td[^>]*>(.*?)</td>", html, re.S)
entries = []
front = 0
appendix = 0
for cell in cells:
    m = re.search(r"<a href=([\w\-]+\.pdf)[^>]*>(.*?)</a>", cell, re.S)
    if not m:
        continue
    pdf, title = m.group(1), re.sub(r"<[^>]+>", "", m.group(2)).strip()
    num = re.search(r"<small>\s*(\w+)\s*</small>", cell)
    if num:
        n = num.group(1)
        prefix = f"{int(n):02d}" if n.isdigit() else n
    elif pdf in FRONT:
        front += 1
        prefix = f"00{chr(ord('a') + front - 1)}"
    else:
        entries.append((None, pdf, title))   # appendix: numbered after sorting
        continue
    entries.append((prefix, pdf, title))

# Appendices keep the table's column order (VMM, monitors, labs)
order = {"dialogue-vmm.pdf": 0, "vmm-intro.pdf": 1, "dialogue-monitors.pdf": 2,
         "threads-monitors.pdf": 3, "dialogue-labs.pdf": 4, "lab-tutorial.pdf": 5,
         "lab-projects-systems.pdf": 6, "lab-projects-xv6.pdf": 7}
apps = sorted((e for e in entries if e[0] is None), key=lambda e: order.get(e[1], 99))
entries = [e for e in entries if e[0] is not None]
for e in apps:
    appendix += 1
    entries.append((f"A{appendix}", e[1], e[2]))

def key(e):
    p = e[0]
    if p.startswith("00"):
        return (0, p)
    return (1, int(p)) if p.isdigit() else (2, int(p[1:]))

entries.sort(key=key)
index = ["# OSTEP — Operating Systems: Three Easy Pieces (v1.10)", "",
         f"Source: {BASE}", "", "| # | File | Title |", "|---|---|---|"]
for prefix, pdf, title in entries:
    name = f"{prefix}-{pdf}"
    dest = out / name
    if not dest.exists():
        data = urllib.request.urlopen(BASE + pdf).read()
        if not data.startswith(b"%PDF"):
            print("NOT A PDF:", pdf); continue
        dest.write_bytes(data)
        time.sleep(0.3)
    index.append(f"| {prefix} | {name} | {title} |")
    print(name, "-", title)

(out / "INDEX.md").write_text("\n".join(index) + "\n", encoding="utf-8")
print(len(entries), "files")
