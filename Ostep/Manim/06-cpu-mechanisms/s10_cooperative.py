import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403
from s09_regain_control import REST9, small_table  # noqa: E402


def trust_ribbon(text="cooperative: the OS trusts the process"):
    return Text(text.replace(": ", ":\n"), font_size=20, color=DIM, line_spacing=0.8).move_to(P3(-5.1, 2.5))


def build_end():
    """S10 end: LDE world with an empty user seat, awake token, trust ribbon, empty benches."""
    w = World("user", rest=REST9)
    w.add_ring("A")
    w.add_ring("B")
    tt = small_table()
    st = strip(CRUX_Q3)
    rib = trust_ribbon()
    return dict(w=w, tt=tt, strip=st, ribbon=rib)


class S10Cooperative(Ep06Scene):
    def construct(self):
        self.add_badge()
        self.add_docked_term("limited direct execution")
        stu, prof = corner_chars(True, "neutral", "neutral")
        w = World("user", rest=REST9)
        a = w.add_proc("A", "running", where="chip")
        b = w.add_proc("B", "ready", where="bench")
        w.add_ring("A")
        w.add_ring("B")
        tt = small_table()
        st = strip(CRUX_Q3)
        w.token.badge.set_fill(opacity=0.3).set_stroke(opacity=0.3)
        w.token.text.set_opacity(0.3)
        bottom_to(w.token, REST9)
        self.add(w.boundary, w.gauge, w.chip, *w.rings.values(), a, b, w.token, tt, st, stu, prof)

        # S10.1
        rib = trust_ribbon()
        mac = Text("early Mac, Xerox Alto", font_size=20, color=DIM).move_to(P3(4.9, 2.6))
        self.say("Early systems, like the first Macintosh, took the cooperative approach: the OS trusts processes "
                 "to give up the CPU periodically.",
                 Succession(self.note("cooperative approach"), AnimationGroup(Write(rib), FadeIn(mac))))

        # S10.2
        self.say("And most do, through system calls.",
                 AnimationGroup(w.down("A"), w.token.wake(1.2)))

        # S10.3
        y = snippet("yield()", 22).move_to(P3(-1.9, 2.15))
        self.say("Some systems even have an explicit yield call that does nothing but hand over the CPU.",
                 Succession(FadeIn(y, scale=1.3), Wait(1.0), AnimationGroup(FadeOut(y), w.up("B"))))

        # S10.4
        div = snippet("1/0", 22, RED_BAD).move_to(P3(1.9, 2.0))
        xm = x_mark(0.4).move_to(P3(3.4, 1.3))
        with self.narrate("A process that does something illegal, like dividing by zero, also traps into the OS, which will "
                          "probably terminate it."):
            self.play(FadeIn(div, scale=1.4))
            self.wait(0.5)
            self.play(w.down("B"))
            self.play(FadeOut(div), FadeIn(xm, scale=1.8))
            self.play(AnimationGroup(FadeOut(b), FadeOut(w.rings["B"]), FadeOut(xm)))
            self.play(w.up("A"))

        # S10.5
        loop = loop_arrow(0.4).move_to(a.get_right() + RIGHT * 0.45 + UP * 0.2)
        tl = Text("tick", font_size=24, color=DIM).move_to(P3(1.6, 1.3))
        num = Integer(1, font_size=34, color=TEXT).next_to(tl, RIGHT, buff=0.15)
        zz = zz_glyph(0.4).next_to(w.token, UR, buff=0.0)
        self.say("And if a program loops forever, and never makes a system call?", stu.change("curious"),
                 AnimationGroup(Rotate(a, TAU, about_point=a.get_center(), run_time=1.5), FadeIn(loop), FadeIn(tl), FadeIn(num),
                                w.token.dim_to(0.3, 1.0), FadeIn(zz)),
                 Succession(Wait(1.5), ChangeDecimalToValue(num, 9, run_time=2.5, rate_func=linear)))

        a.set_expression("ready")
        # S10.6
        comp = Computer("overwhelmed").scale(0.6).move_to(P3(0, -2.9))
        sw = PowerSwitch(0.8, on=True).move_to(P3(-4.9, 1.2))
        black = Rectangle(width=16, height=9).set_fill(BG, 1).set_stroke(width=0).set_z_index(30)
        self.say("Then there's one cure, the oldest in computing: reboot the machine.", prof.change("worried"),
                 Succession(FadeIn(comp, scale=0.5), FadeIn(sw), sw.flip(False), sw.flip(True),
                            FadeIn(black, run_time=0.15),
                            AnimationGroup(FadeOut(VGroup(loop, tl, num, zz, comp, sw, mac), run_time=0.05),
                                           hop_bottom(a, BENCH["A"], run_time=0.05), FadeIn(b, run_time=0.05),
                                           FadeIn(w.rings["B"], run_time=0.05), w.token.wake(0.05)),
                            FadeOut(black, run_time=0.2)))

        self.drop(sw)
        # S10.7
        self.say("That's the plan?", stu.change("sad"))
        self.beat(1.0)

        # S10.8
        body = VGroup(Text("Reboot is useful", font_size=26, color=TEXT, weight=BOLD),
                      Text("known state", font_size=22, color=DIM),
                      Text("reclaims leaked resources", font_size=22, color=DIM),
                      Text("easy to automate", font_size=22, color=DIM)).arrange(DOWN, buff=0.12)
        tip = TipCard(body, width=4.2).move_to(P3(3.6, 1.2))
        self.say("Reboot is more useful than it sounds: it returns the software to a known state, reclaims leaked "
                 "resources, and is easy to automate.",
                 Succession(tip.slide_in(), Wait(3.5), tip.slide_out()))
