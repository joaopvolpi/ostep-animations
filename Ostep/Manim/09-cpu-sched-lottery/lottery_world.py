"""Shared builder for the lottery implementation scenes (S08 and S09)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403

CODE_SRC = """int counter = 0;
int winner = getrandom(0, totaltickets);
node_t *current = head;
while (current) {
    counter = counter + current->tickets;
    if (counter > winner)
        break;
    current = current->next;
}
// current is the winner"""

JOBS = [("A", 100, COL["A"]), ("B", 50, COL["B"]), ("C", 250, COL["C"])]
COUNTER_AT = P3(2.9, -1.35)
WINNER_AT = P3(2.9, -0.7)


def counter_text(v):
    return mono(f"counter = {v}", 22).move_to(COUNTER_AT, aligned_edge=LEFT)


def winner_text(v="?"):
    return mono(f"winner = {v}", 22).move_to(WINNER_AT, aligned_edge=LEFT)


def build_s08():
    cw = CodeWalker(CODE_SRC, font_size=18)
    cw.move_to(P3(-3.7, -0.3))
    jl = JobList(JOBS, at=(0.8, 1.2), gap=1.9, radius=0.34, font_size=18)
    bars = VGroup()
    for i, (n, t, c) in enumerate(JOBS):
        r = Rectangle(width=t * 0.008, height=0.14).set_fill(c, 0.9).set_stroke(outline_of(c), 1.5)
        r.move_to(jl.node_center(i) + DOWN * 0.95)
        bars.add(r)
    total = Text("total: 400", font_size=20, color=DIM).move_to(P3(5.8, 1.95))
    drum = RaffleDrum(0.7).move_to(P3(0.9, -0.75))
    dlab = mono("getrandom(0, totaltickets)", 16, DIM).move_to(P3(1.0, -1.7))
    cpu = CPU(size=0.8, label="CPU").move_to(P3(6.0, -0.9))
    return dict(cw=cw, jl=jl, bars=bars, total=total, drum=drum, dlab=dlab, cpu=cpu)
