import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403
from s09_regain_control import REST9, small_table  # noqa: E402
from s10_cooperative import trust_ribbon  # noqa: E402

KS11 = P3(3.6, -1.9)
SW11 = P3(-1.9, -0.95)


def make_timer():
    return AlarmClock(0.4).move_to(TIMER_POS)


def build_end():
    """S11 end: chip at the kernel seat with the token, A frozen on its bench, k-stack(A) holds A's packet,
    timer running, trap table with 3 rows."""
    w = World("kernel", rest=REST9)
    a = w.add_proc("A", "ready", where="bench")
    b = w.add_proc("B", "ready", where="bench")
    w.add_ring("A")
    w.add_ring("B")
    w.token_on_chip()
    tt = small_table()
    tt.row(1).set_color(TEXT)
    ks = KernelStack("k-stack(A)").move_to(KS11)
    pk = RegPacket(COL["A"]).move_to(ks.slot_point(0)).scale(1.3)
    ks.items.append(pk)
    timer = make_timer()
    timer.led.set_fill(GREEN_OK, 1)
    st = strip(CRUX_Q4)
    rib = trust_ribbon("no trust needed")
    return dict(w=w, a=a, b=b, tt=tt, ks=ks, pk=pk, timer=timer, strip=st, ribbon=rib)


class S11TimerInterrupt(Ep06Scene):
    def construct(self):
        self.add_badge()
        self.add_docked_term("cooperative approach")
        stu, prof = corner_chars(True, "neutral", "neutral")
        w = World("user", rest=REST9)
        a = w.add_proc("A", "ready", where="bench")
        b = w.add_proc("B", "ready", where="bench")
        w.add_ring("A")
        w.add_ring("B")
        tt = small_table()
        tt.row(1).set_color(DIM)
        old = strip(CRUX_Q3)
        rib = trust_ribbon()
        self.add(w.boundary, w.gauge, w.chip, w.token, tt, old, rib, *w.rings.values(), a, b, stu, prof)

        # S11.1
        new = strip(CRUX_Q4)
        timer = make_timer()
        loop = loop_arrow(0.4).move_to(P3(0, 2.7))
        self.say("Which leaves us with a harder question: How to gain control without cooperation?", ReplacementTransform(old, new))
        self.say("The answer was found many years ago, and it's simple: a timer interrupt.",
                 Succession(FadeIn(timer, shift=LEFT * 0.8), self.term("timer interrupt")),
                 Succession(Wait(1.0), AnimationGroup(w.hop_on_chip("A"), FadeIn(loop))))
        a.set_expression("running")

        # S11.2
        every = Text("every X ms", font_size=20, color=DIM).move_to(P3(5.0, 1.05))
        ticks = VGroup(*[Line(P3(4.3 + 0.35 * k, 0.7), P3(4.3 + 0.35 * k, 0.9)).set_stroke(CPU_COLOR, 3) for k in range(5)])
        self.say("A timer device can be programmed to raise an interrupt every few milliseconds.",
                 Succession(AnimationGroup(timer.spin(1, 1.0), FadeIn(every)),
                            *[AnimationGroup(timer.ring(0.8), FadeIn(ticks[k])) for k in range(3)]))

        # S11.3
        bl = bolt(0.3).move_to(timer.get_center())
        self.say("When it fires, the running process is halted, whatever it was doing…",
                 Succession(timer.ring(0.8), PacketFly(bl, w.chip.get_center() + UP * 0.8, arc=0.3, run_time=0.9),
                            AnimationGroup(FadeOut(bl), FadeOut(loop), Flash(a.get_center(), color=CPU_COLOR))))
        a.set_expression("ready")

        # S11.4
        self.say("…and a pre-configured interrupt handler in the OS runs.",
                 Succession(w.down("A"), tt.highlight_row(1), Wait(0.5)),
                 late(1.5, self.note("interrupt handler")))

        # S11.5
        t1 = tag("keep A?", DIM, 20).move_to(P3(-1.7, -0.75))
        t2 = tag("run B?", DIM, 20).move_to(P3(1.7, -0.75))
        self.say("The OS has regained control. It can stop this process and start another.", stu.change("excited"),
                 AnimationGroup(FadeIn(t1, scale=1.3), FadeIn(t2, scale=1.3), tt.unhighlight()))

        # S11.6
        sw = PowerSwitch(0.7, on=False).move_to(SW11 + P3(0, 0.0))
        boot = Text("at boot", font_size=18, color=DIM).next_to(sw, UP, buff=0.4)
        rowp = P3(tt.get_right()[0] + 0.05, tt.row(1).get_center()[1])
        self.say("The OS prepares this at boot, like the system-call handler.",
                 Succession(AnimationGroup(FadeOut(t1), FadeOut(t2), FadeIn(sw), FadeIn(boot)), sw.flip(True),
                            w.token.reach(rowp, run_time=0.6), tt.row(1).animate.set_color(TEXT), w.token.retract(0.4),
                            FadeOut(VGroup(sw, boot))))

        # S11.7
        btn = tag("START", TEXT, 20).move_to(P3(5.0, 0.35))
        priv = Text("privileged", font_size=20, color=KERNEL_COLOR, weight=BOLD).next_to(btn, DOWN, buff=0.1)
        req = Arrow(P3(-3.4, 0.9), P3(-3.4, -0.25), buff=0, color=COL["A"], stroke_width=4)
        self.say("It tells the hardware which code to run when the timer fires, and it starts the timer, a "
                 "privileged operation.",
                 Succession(FadeIn(btn), w.token.reach(btn.get_bottom() + DOWN * 0.05, run_time=0.8),
                            AnimationGroup(btn[0].animate.set_fill(GREEN_OK, 0.6), timer.start(), FadeIn(priv)),
                            w.token.retract(0.5),
                            GrowArrow(req), w.boundary.flash_at(-3.4, RED_BAD), FadeOut(req)))

        # S11.8
        ks = KernelStack("k-stack(A)").move_to(KS11)
        pk = RegPacket(COL["A"]).move_to(a.get_center())
        hw = Text("hardware", font_size=20, color=CPU_COLOR).move_to(P3(2.0, -0.9))
        never = tag("A never asked", DIM, 18).next_to(a, UP, buff=0.05)
        self.say("The hardware does its part too: it saves the running program's state onto the kernel stack, the "
                 "same dance as a trap, though this time the program never asked.",
                 Succession(FadeIn(ks), FadeIn(pk, scale=0.4, run_time=0.4), FadeIn(hw), ks.push(pk, run_time=1.6),
                            FadeIn(never, scale=1.3)))

        # S11.9
        self.say("So the process doesn't even notice?", stu.change("curious"), FadeOut(VGroup(never, hw, btn, priv)))

        # S11.10
        pg = PauseGlyph(0.5).next_to(a, UP, buff=0.1)
        pl = PlayGlyph(0.5).move_to(pg)
        self.say("Like a movie paused and played again.", prof.change("happy"),
                 Succession(FadeIn(pg), ReplacementTransform(pg, pl), Wait(0.5), FadeOut(pl)))

        # S11.11
        tip = TipCard("Use the timer interrupt to regain control", width=5.0, font_size=24).move_to(P3(0, 1.9))
        rib2 = trust_ribbon("no trust needed")
        self.say("This is the non-cooperative approach: the OS takes control by force, with hardware help.",
                 Succession(self.note("non-cooperative"), AnimationGroup(Transform(rib, rib2), timer.ring(0.8)), tip.slide_in(LEFT)))


        # S11.12
        tip2 = TipCard("Misbehaving process? One strike, and you're out.", title="TIP", width=5.0, font_size=24).move_to(P3(0, 1.9))
        self.say("And a process that misbehaves gets one strike: it's out.",
                 Succession(tip.slide_out(LEFT), tip2.slide_in(LEFT), Wait(1.0), tip2.slide_out(LEFT)))
