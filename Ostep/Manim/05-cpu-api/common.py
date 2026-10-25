"""Episode 05 (Interlude: Process API): constants, helpers and state builders.

Every scene starts from a builder here (``build_*``) so scenes can be rendered independently and
still match the previous scene's "Ends with" state.
"""
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_ROOT = _HERE.parents[2]
for _p in (str(_ROOT), str(_HERE)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import numpy as np  # noqa: E402
from manim import *  # noqa: E402,F401,F403
from ostep_lib import *  # noqa: E402,F401,F403
from ostep_lib.props.p04_timeline import Timeline  # noqa: E402
from ostep_lib.props.p04_queue import Queue  # noqa: E402
from ostep_lib.props.p04_state_diagram import StateDiagram  # noqa: E402
from ostep_lib.props.p04_icons import *  # noqa: E402,F401,F403

# ---------------------------------------------------------------------------
# Persistent assignments
# ---------------------------------------------------------------------------
PAR = PROCESS_COLORS[0]     # coral: parent (PID 29146)
CHI = PROCESS_COLORS[1]     # mint: child (PID 29147)
SHC = PROCESS_COLORS[2]     # gold: shell
SKY = PROCESS_COLORS[3]     # sky: grep / wc program
VIO = PROCESS_COLORS[4]     # violet: wc in the pipe
PID_P, PID_C = 29146, 29147
CHAR_SCALE = 0.75
STUDENT_CORNER = np.array([-5.8, -2.8, 0.0])
PROF_CORNER = np.array([5.8, -2.8, 0.0])
STUDENT_DIALOGUE = np.array([-2.6, -1.2, 0.0])
PROF_DIALOGUE = np.array([2.6, -1.2, 0.0])
BADGE_TEXT = "05 · Process API"
CRUX_Q = "How to create and control processes?"
CRUX_SUB = ("What interfaces should the OS present for process creation and control? "
            "How should they be designed for power, ease of use and high performance?")
OK_GREEN = "#8BE07A"

P1C = r'''printf("hello (pid:%d)\n", getpid());
int rc = fork();
if (rc == 0) {
  printf("child (pid:%d)\n", getpid());
} else {
  printf("parent of %d (pid:%d)\n",
         rc, getpid());
}'''
P1_OUT = ["hello (pid:29146)", "parent of 29147 (pid:29146)", "child (pid:29147)"]


def P3(x, y=0.0):
    return np.array([float(x), float(y), 0.0])


# ---------------------------------------------------------------------------
# Characters and processes
# ---------------------------------------------------------------------------
def student_corner(expr="neutral"):
    return Student(expr).scale(CHAR_SCALE).move_to(STUDENT_CORNER)


def prof_corner(expr="neutral"):
    return Professor(expr).scale(CHAR_SCALE).flip().move_to(PROF_CORNER)


def student_dialogue(expr="neutral", pos=None):
    s = Student(expr)
    return bottom_to(s, (STUDENT_DIALOGUE if pos is None else pos) + DOWN * 1.05)


def prof_dialogue(expr="neutral", pos=None):
    p = Professor(expr).flip()
    return bottom_to(p, (PROF_DIALOGUE if pos is None else pos) + DOWN * 1.05)


def proc(color, expr="ready", scale=1.0, label=None):
    p = Process(expr, color=color, label=label)
    if scale != 1.0:
        p.scale(scale)
    return p


def set_label(p, text):
    """Instantly change (or drop, with None) the label under a Process creature."""
    p.label_text = text
    p._label_mob = None
    return p.set_expression(p.expression)


def relabel_on_floor(p, text):
    """Give a creature its label back after it landed unlabeled: the label goes under the feet, so the
    creature rises by the label's height and the label's bottom is where its feet were."""
    b0 = p.get_bottom()[1]
    set_label(p, text)
    return p.shift(UP * (b0 - p.get_bottom()[1]))


def cpu_side_label(cpu, text, font_size=22):
    """A creature's label placed left of a CPU, level with the creature standing on it."""
    t = Text(text, font_size=font_size, color=TEXT, weight="BOLD")
    return t.move_to(P3(cpu.get_x() - 1.5, cpu.body.get_top()[1] + 0.25))


def bottom_to(mob, point):
    mob.shift(np.array(point, dtype=float) - mob.get_bottom())
    return mob


def feet_for_bottom(mob, point):
    return np.array(point, dtype=float) + (base_point(mob) - mob.get_bottom())


def seat(p, cpu):
    return bottom_to(p, cpu.slot_point() + UP * 0.02)


def hop_bottom(p, point, **kw):
    return hop_to(p, feet_for_bottom(p, point), **kw)


def hop_seat(p, cpu, **kw):
    return hop_bottom(p, cpu.slot_point() + UP * 0.02, **kw)


def queue_mover(mob, point, run_time=0.5, **kw):
    return hop_bottom(mob, point, run_time=run_time, **kw)


# ---------------------------------------------------------------------------
# Overlays
# ---------------------------------------------------------------------------
def make_badge():
    return SectionBadge(BADGE_TEXT, accent=VIRT)


def crux_strip():
    return CruxCard(CRUX_Q, CRUX_SUB, accent=VIRT).strip()


def dock_term_now(terms, text):
    m = terms.docked_now(text)
    return m


def code_cap(walker_or_mob, text="p1.c (error check omitted)"):
    return Text(text, font_size=18, color=DIM).next_to(walker_or_mob, DOWN, buff=0.15)


# ---------------------------------------------------------------------------
# Terminals
# ---------------------------------------------------------------------------
def mk_term(width, n_lines, font_size=18, title=None):
    """A Terminal tall enough for ``n_lines`` lines."""
    probe = Terminal(width=width, height=3.0, font_size=font_size)
    h = 0.44 + 0.2 + n_lines * probe.line_h + 0.04
    return Terminal(width=width, height=h, font_size=font_size, title=title)


def fill_term(term, items):
    """Instantly fill a Terminal: items are ``("cmd", text)`` / ``("out", text)`` or plain
    strings (output)."""
    for it in items:
        kind, text = ("out", it) if isinstance(it, str) else it
        if kind == "cmd":
            term.type(text)
        else:
            term.print(text)
    return term


def p1_term(n=3, cmd=True, width=5.0, font_size=18, lines=4):
    t = mk_term(width, lines, font_size)
    items = ([("cmd", "./p1")] if cmd else []) + P1_OUT[:n]
    return fill_term(t, items)


def p1_walker(font_size=18, caption=True):
    w = CodeWalker(P1C, font_size=font_size, caption="p1.c (error check omitted)" if caption else None)
    return w


# ---------------------------------------------------------------------------
# Scene base
# ---------------------------------------------------------------------------
class Ep05Scene(NarratedScene):
    """NarratedScene + the episode's overlays and an end-of-scene bounds check."""

    def setup(self):
        super().setup()
        self.terms = TermHighlight(accent=VIRT)

    def check_bounds(self, label="end", xlim=6.9, ylim=3.85):
        for m in self.mobjects:
            pts = [sm.points for sm in m.get_family() if len(sm.points)
                   and (getattr(sm, "stroke_opacity", 1) > 0.01 or sm.get_fill_opacity() > 0.01)]
            if not pts:
                continue
            pts = np.vstack(pts)
            x0, x1 = pts[:, 0].min(), pts[:, 0].max()
            y0, y1 = pts[:, 1].min(), pts[:, 1].max()
            if x0 < -xlim or x1 > xlim or y0 < -ylim or y1 > ylim:
                print(f"OOB[{label}]: {type(m).__name__} x=({x0:.2f},{x1:.2f}) y=({y0:.2f},{y1:.2f})")

    def tear_down(self):
        self.check_bounds()
        super().tear_down()

    def add_badge(self):
        self.badge = make_badge()
        self.add(self.badge)
        return self.badge

    def add_corner_chars(self, s_expr="neutral", p_expr="neutral"):
        self.stu = student_corner(s_expr)
        self.prof = prof_corner(p_expr)
        self.add(self.stu, self.prof)
        return self.stu, self.prof

    def fade_stage(self, *keep, run_time=0.8):
        """Fade out everything except ``keep`` (+ the docked term): a clean hand-off to the next scene."""
        keep = {id(k) for k in keep if k is not None} | {id(self.terms.docked)}
        gone = []

        def collect(m):
            # a play() with an AnimationGroup can leave a kept mobject nested in a scene-level group:
            # look inside such groups instead of fading them whole
            if id(m) in keep or getattr(m, "is_scrim", False):
                return
            if any(id(x) in keep for x in m.get_family()[1:]):
                for s in m.submobjects:
                    collect(s)
            else:
                gone.append(m)
        for m in self.mobjects:
            collect(m)
        if gone:
            self.play(*[FadeOut(m) for m in gone], run_time=run_time)

    def add_docked_term(self, text):
        m = dock_term_now(self.terms, text)
        self.add(m)
        return m

    def term(self, text, **kw):
        return self.terms.show(text, **kw)


# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------
def mono(text, size=22, color=TEXT):
    return Text(text, font=MONO_FONT, font_size=size, color=color)


def tagged(text, color=TEXT, size=20, stroke=DIM):
    return info_tag(text, color=color, font_size=size, stroke=stroke)


def caption_below(mob, text, size=18, color=DIM, buff=0.12):
    return Text(text, font_size=size, color=color).next_to(mob, DOWN, buff=buff)


# ---------------------------------------------------------------------------
# State builders
# ---------------------------------------------------------------------------
def build_s01_end():
    """Code walker (p1.c) + Terminal with 3 output lines + both characters."""
    walker = p1_walker().move_to(P3(-3.6, 0.5))
    term = p1_term(3, cmd=True, width=5.0, lines=4).move_to(P3(3.2, 0.7))
    stu = student_corner("confused")
    prof = prof_corner("happy")
    return dict(walker=walker, term=term, stu=stu, prof=prof)


def build_s02_end():
    """Badge, crux strip and both characters (corner mode)."""
    return dict(badge=make_badge(), strip=crux_strip(), stu=student_corner("curious"), prof=prof_corner("neutral"))


CPU_S3 = P3(-2.0, 0.15)
BOUNDARY_Y = -0.8
GAUGE_S3 = P3(6.35, -0.8)
CODE_CARD_AT = P3(3.4, 2.0)
MINI_TERM_AT = P3(3.4, 0.6)


def card_code(lines=1, font_size=16):
    src = ['printf("hello (pid:%d)\\n", getpid());', 'int rc = fork();'][:lines]
    return CodeWalker("\n".join(src), font_size=font_size)


def build_s03_end():
    cpu = CPU(1.4).move_to(CPU_S3)
    par = proc(PAR, "running", label=None)
    seat(par, cpu)
    par_lbl = cpu_side_label(cpu, f"PID {PID_P}")
    bd = UserKernelBoundary(y=BOUNDARY_Y)
    gauge = PrivilegeGauge(height=1.6, level="kernel").move_to(GAUGE_S3)
    packet = program_chip("fork()", CPU_COLOR, 18).move_to(P3(-0.8, -1.7))
    c1 = card_code(1).move_to(CODE_CARD_AT)
    code = card_code(2)
    code.shift(c1.get_top() - code.get_top())      # same alignment as in S03
    code_bar = code.add_bar(TEXT, 2)
    mt = mk_term(4.6, 1, 18)
    fill_term(mt, ["hello (pid:29146)"]).move_to(MINI_TERM_AT)
    return dict(cpu=cpu, par=par, par_lbl=par_lbl, bd=bd, gauge=gauge, packet=packet, code=code, code_bar=code_bar, mt=mt)


WORLD_L, WORLD_R = P3(-3.4, -0.1), P3(3.4, -0.1)
S4_TERM_AT = P3(0, -2.5)


def build_s04_end():
    """Both worlds side by side, PC markers on the same line, one-line terminal."""
    pw = ProcessWorld(PAR, PID_P).place(WORLD_L)
    cw = ProcessWorld(CHI, PID_C).place(WORLD_R)
    pm, cm = pw.pc_marker(PAR), cw.pc_marker(CHI)
    mt = mk_term(4.4, 1, 18)
    fill_term(mt, ["hello (pid:29146)"]).move_to(S4_TERM_AT)
    b1, b2 = s4_bubbles()
    return dict(pw=pw, cw=cw, pm=pm, cm=cm, mt=mt, b1=b1, b2=b2)


S5_CREATURE_L, S5_CREATURE_R = P3(-5.0, 0.8), P3(5.0, 0.8)
S5_CODE_AT = P3(0, 0.9)
S5_TERM_AT = P3(0, -2.35)


def build_s05_end():
    walker = p1_walker(caption=False).move_to(S5_CODE_AT)
    b_par = walker.add_bar(PAR, 7)
    b_chi = walker.add_bar(CHI, 5)
    term = mk_term(6.0, 3, 16)
    fill_term(term, P1_OUT).move_to(S5_TERM_AT)
    cp = proc(PAR, "ready", scale=0.7, label=f"PID {PID_P}").move_to(S5_CREATURE_L)
    cc = proc(CHI, "ready", scale=0.7, label=f"PID {PID_C}").move_to(S5_CREATURE_R)
    t_par = tagged("rc = 29147", PAR, 20, PAR).move_to(P3(-5.0, 1.95))
    t_chi = tagged("rc = 0", CHI, 20, CHI).move_to(P3(5.0, 1.95))
    return dict(walker=walker, b_par=b_par, b_chi=b_chi, term=term, cp=cp, cc=cc, t_par=t_par, t_chi=t_chi)


def zombie_glyph(scale=0.4):
    return Process("zombie", label=None).scale(scale)


def s4_bubbles():
    b1 = tagged("returning\nfrom fork()", PAR, 16, PAR).move_to(P3(-0.95, 1.0))
    b2 = tagged("returning\nfrom fork()", CHI, 16, CHI).move_to(P3(0.95, 1.0))
    return b1, b2


# ---- S09 / S10 / S11 builders ------------------------------------------------
def build_s09_end():
    """Terminal + shell loop (gap highlighted) + gold sh at the prompt + mint clone in the gap."""
    term = mk_term(5.0, 6, 18).move_to(P3(-3.4, 1.0))
    fill_term(term, [("cmd", "wc p3.c"), "29  107  1030 p3.c"])
    term.prompt_line()
    loop = ShellLoop(cx=3.4)
    loop.arrows["f_e"].set_stroke(CPU_COLOR, 6, family=False)
    loop.arrows["f_e"].tip.set_fill(CPU_COLOR).set_stroke(CPU_COLOR)
    sh = proc(SHC, "ready", scale=0.55, label="sh")
    bottom_to(sh, loop.stand_point("prompt"))
    gap_mid = loop.arrows["f_e"].point_from_proportion(0.5)
    gap_sh = proc(CHI, "ready", scale=0.4, label="sh").move_to(gap_mid + RIGHT * 0.2)
    return dict(term=term, loop=loop, sh=sh, gap_sh=gap_sh)


S11_GREP, S11_WC, S11_PIPE = P3(-3.2, 1.0), P3(3.2, 1.0), P3(0, 1.0)


def build_s11_extras(d, dim=0.25):
    """The padlock tags and the count readout S11 leaves on screen (dimmed for the Tip)."""
    lk1 = VGroup(padlock_icon(0.3), Text("code unchanged", font_size=18, color=TEXT)).arrange(RIGHT, buff=0.1)
    lk2 = lk1.copy()
    lk1.next_to(d["grep"], DOWN, buff=0.15)
    lk2.next_to(d["wc"], DOWN, buff=0.15)
    ctab = VGroup(Text("count:", font_size=20, color=DIM), mono("3", 28, CPU_COLOR)).arrange(RIGHT, buff=0.12)
    ctab.next_to(d["wc"], UP, buff=0.15)
    g = VGroup(lk1, lk2, ctab)
    if dim is not None:
        g.set_opacity(dim)
    return g


def build_s11_end(dim=0.25):
    pipe = KernelPipe(center=(0, 1.0), width=3.2, slots=5)
    grep = proc(SKY, "ready", scale=0.7, label="grep").move_to(S11_GREP)
    wcp = proc(VIO, "ready", scale=0.7, label="wc").move_to(S11_WC)
    p1 = plug_glyph("1", TEXT, 16).move_to(grep.get_right() + RIGHT * 0.45 + DOWN * 0.1)
    p0 = plug_glyph("0", TEXT, 16).move_to(wcp.get_left() + LEFT * 0.45 + DOWN * 0.1)
    c1 = Line(p1.get_right(), pipe.left_end() + LEFT * 0.0).set_stroke(CPU_COLOR, 4)
    c0 = Line(pipe.right_end(), p0.get_left()).set_stroke(USER_COLOR, 4)
    term = mk_term(7.0, 2, 18)
    fill_term(term, [("cmd", "grep -o foo file | wc -l"), "3"]).move_to(P3(0, -1.9))
    g = VGroup(pipe, grep, wcp, p1, p0, c1, c0, term)
    if dim is not None:
        g.set_opacity(dim)
    return dict(group=g, pipe=pipe, grep=grep, wc=wcp, p1=p1, p0=p0, c1=c1, c0=c0, term=term)
