import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403

REST9 = P3(-1.8, -2.3)
TT9 = P3(-4.2, -1.55)


def small_table():
    return TrapTable(width=3.4, height=1.6, filled=3, dim_rows=(1,)).move_to(TT9)


def build_end():
    """S09 end: LDE world, A running, B on its bench, dim OS token, trap table, crux strip."""
    w = World("user", rest=REST9)
    w.add_proc("A", "running", where="chip")
    w.add_proc("B", "ready", where="bench")
    w.add_ring("A")
    w.add_ring("B")
    bottom_to(w.token, REST9)
    w.token.badge.set_fill(opacity=0.3).set_stroke(opacity=0.3)
    w.token.text.set_opacity(0.3)
    tt = small_table()
    st = strip(CRUX_Q3)
    return dict(w=w, tt=tt, strip=st)


class S09RegainControl(Ep06Scene):
    def construct(self):
        self.add_badge()
        self.add_docked_term("limited direct execution")
        stu, prof = corner_chars(True, "neutral", "neutral")
        w = World("user", rest=REST9)
        a = w.add_proc("A", "running", where="chip")
        w.add_ring("A")
        tt = small_table()
        leg = chart_legend()
        self.add(w.boundary, w.gauge, w.chip, w.rings["A"], a, w.token, tt, leg, stu, prof)
        b = w.add_proc("B", "ready", where="bench")
        w.add_ring("B")

        # S09.1
        stop = DashedLine(w.token.get_top() + UP * 0.05, P3(-0.7, 0.1), dash_length=0.12).add_tip(tip_length=0.2)
        start = DashedLine(w.token.get_top() + UP * 0.05, P3(3.2, 0.7), dash_length=0.12).add_tip(tip_length=0.2)
        l1 = Text("stop", font_size=22, color=TEXT).move_to(P3(-1.4, -0.9))
        l2 = Text("start", font_size=22, color=TEXT).move_to(P3(1.2, -0.5))
        self.say("Problem number two: switching between processes. Sounds simple: just stop one and start another.",
                 Succession(AnimationGroup(FadeIn(w.rings["B"]), FadeIn(b, shift=DOWN * 0.3)), Wait(1.5),
                            AnimationGroup(Create(stop), FadeIn(l1)), AnimationGroup(Create(start), FadeIn(l2))))

        # S09.2
        zz = zz_glyph(0.4).next_to(w.token, UR, buff=0.0)
        self.say("But if a process is running on the CPU, then by definition the OS is not running.",
                 prof.change("thinking"),
                 AnimationGroup(w.token.dim_to(0.3, 1.0), FadeIn(zz), Uncreate(stop), Uncreate(start), FadeOut(l1), FadeOut(l2)))

        # S09.3
        self.say("And if the OS isn't running…",
                 Succession(w.token.reach(P3(-1.8, -0.45), run_time=0.5), w.token.retract(0.3),
                            w.token.reach(P3(-1.8, -0.45), run_time=0.5), w.token.retract(0.3)))

        # S09.4
        lock = padlock_icon(0.4, KERNEL_COLOR).next_to(w.token, UP, buff=0.0)
        lk = Text("locked out", font_size=20, color=KERNEL_COLOR).next_to(lock, UP, buff=0.05)
        self.say("…it can't do anything about it.", stu.change("confused"), AnimationGroup(FadeIn(lock, scale=1.5), FadeIn(lk)))

        # S09.5
        crux = CruxCard(CRUX_Q3, CRUX_SUB3, accent=VIRT).move_to(P3(0, 0.4))
        self.play(FadeOut(VGroup(lock, lk, zz, leg)), FadeIn(crux, shift=DOWN * 1.5), run_time=1.0)
        self.beat(1.2)
        self.play(crux.dock((0, 3.2, 0), 22))
