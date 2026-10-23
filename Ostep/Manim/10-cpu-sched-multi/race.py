"""Shared stage for S08 (the list race) and S09 (the lock fix)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common_more import *  # noqa: E402,F401,F403
from ostep_lib.props.p05_code import CodeWalker  # noqa: E402

POP_SRC = """int List_Pop() {
    Node_t *tmp = head;
    int value = head->value;
    head = head->next;
    free(tmp);
    return value;
}"""

POP_LOCK_SRC = """int List_Pop() {
    lock(&m);
    Node_t *tmp = head;
    int value = head->value;
    head = head->next;
    free(tmp);
    unlock(&m);
    return value;
}"""

NODE_X = [1.1, 2.4, 3.7]
LIST_Y = 1.3
CHIP_XS = (1.6, 4.2)
CHIP_Y = -1.3
TC = (COL["A"], COL["D"])


def make_node(val, x):
    r = RoundedRectangle(width=0.8, height=0.6, corner_radius=0.1).set_fill(mix(MEM_COLOR, BG, 0.7), 1)
    r.set_stroke(MEM_COLOR, 2.5)
    t = mono(str(val), 24)
    g = VGroup(r, t.move_to(r)).move_to(P3(x, LIST_Y))
    return g


def build_race_stage(broken=False, src=POP_SRC):
    code = CodeWalker(src, font_size=20)
    code.code.move_to(P3(-3.9, 0.8))
    nodes = [make_node(v, x) for v, x in zip((5, 3, 8), NODE_X)]
    null = mono("NULL", 20, DIM).move_to(P3(5.0, LIST_Y))
    arrows = VGroup(*[Arrow(nodes[i].get_right(), (nodes[i + 1].get_left() if i < 2 else null.get_left() + LEFT * 0.05),
                            buff=0.05, stroke_width=3, color=DIM, tip_length=0.15) for i in range(3)])
    head_lab = label("head", 22, DIM)
    head_arrow = Arrow(UP * 0.5, ORIGIN, buff=0, stroke_width=4, color=TEXT, tip_length=0.15)
    hv = VGroup(head_lab, head_arrow).arrange(DOWN, buff=0.05)
    hv.next_to(nodes[0], UP, buff=0.05)
    chips = [CPU(size=0.8, label=f"CPU {i + 1}") for i in range(2)]
    threads = []
    for ch, x, col in zip(chips, CHIP_XS, TC):
        ch.move_to(P3(x, CHIP_Y))
        t = Process("running", color=col, label=None).scale(0.4)
        place_on(t, ch.slot_point())
        threads.append(t)
    return dict(code=code, nodes=nodes, null=null, arrows=arrows, hv=hv, chips=chips, threads=threads)


def tmp_chip(color, text="tmp"):
    r = RoundedRectangle(width=0.7, height=0.34, corner_radius=0.08).set_fill(color, 0.9)
    r.set_stroke(outline_of(color), 2)
    t = Text(text, font=MONO_FONT, font_size=16, color=INK).move_to(r)
    return VGroup(r, t)
