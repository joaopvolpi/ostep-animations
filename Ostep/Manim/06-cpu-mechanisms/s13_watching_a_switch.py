import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403
from s11_timer_interrupt import make_timer  # noqa: E402
from s12_scheduler_switch import build_end as s12_end  # noqa: E402

CS13 = 1.12 * 0.7
KSEAT13 = P3(0, -1.1)
REST13 = P3(-2.9, -2.4)
KS13 = {"A": P3(-4.4, -1.6), "B": P3(4.4, -1.6)}
PCB13 = {"A": P3(-1.4, -1.8), "B": P3(1.4, -1.8)}


def pcb13(name):
    card = PCBCard(name, COL[name], [("pid", "1" if name == "A" else "2"), ("state", "ready")], width=1.6, height=1.0,
                   cols=1, font_size=14, header_width=0.4, title_font=22)
    lab = Text(f"proc({name})", font=MONO_FONT, font_size=14, color=COL[name]).next_to(card, UP, buff=0.04)
    g = VGroup(card, lab).move_to(PCB13[name])
    g.card = card
    return g


def make_timeline13():
    return Timeline(["A", "B", "OS"], ticks=10, colors=[COL["A"], COL["B"], KERNEL_COLOR], x_range=(-3.5, 3.5),
                    top=-2.78, row_height=0.28, row_step=0.34, tick_labels=False, label_font=16)


def build_world13(phase="start"):
    """S13 stage.  phase 'start': A running (user seat), B on its bench, timeline ticks 1-3 filled.
    phase 'end': B running, A on its bench, k-stack(A) holds A's packet, full timeline."""
    w = World("user", chip_size=CS13, user_seat=USER_SEAT, kernel_seat=KSEAT13, ps=0.7, token_scale=0.7, rest=REST13)
    a = w.add_proc("A", "running" if phase == "start" else "ready", where="chip" if phase == "start" else "bench")
    b = w.add_proc("B", "ready" if phase == "start" else "running", where="bench" if phase == "start" else "chip")
    w.add_ring("A")
    w.add_ring("B")
    ksA = KernelStack("k-stack(A)").move_to(KS13["A"])
    ksB = KernelStack("k-stack(B)").move_to(KS13["B"])
    pA, pB = pcb13("A"), pcb13("B")
    timer = make_timer()
    tl = make_timeline13()
    pkA = pkB = None
    if phase == "start":
        for t in (1, 2, 3):
            tl.set_block("A", t, "running")
            tl.set_block("B", t, "ready")
        pkB = RegPacket(COL["B"]).move_to(ksB.slot_point(0)).scale(1.3)
        ksB.items.append(pkB)
    else:
        for t in (1, 2, 3, 4):
            tl.set_block("A", t, "running")
        for t in (1, 2, 3, 4, 5, 6):
            tl.set_block("B", t, "ready")
        for t in (5, 6, 7):
            tl.set_block("A", t, "ready")
        tl.set_block("OS", 5, "running")
        tl.set_block("OS", 6, "running")
        tl.set_block("B", 7, "running")
        pkA = RegPacket(COL["A"]).move_to(ksA.slot_point(0)).scale(1.3)
        ksA.items.append(pkA)
        pA.card.set_field_now("state", "ready")
        pB.card.set_field_now("state", "running")
    return dict(w=w, a=a, b=b, ksA=ksA, ksB=ksB, pA=pA, pB=pB, timer=timer, tl=tl, pkA=pkA, pkB=pkB)


def build_end():
    return build_world13("end")


class S13WatchingASwitch(Ep06Scene):
    def construct(self):
        self.add_badge()
        self.add_docked_term("context switch")
        stu, prof = corner_chars(True, "neutral", "neutral")
        old = s12_end()
        ow = old["w"]
        oldmobs = [ow.boundary, ow.gauge, ow.chip, *ow.rings.values(), old["a"], old["b"], ow.token, old["tt"], old["ks"],
                   old["pk"], old["timer"], old["sA"], old["sB"], old["ret"]]
        self.add(*oldmobs, stu, prof)
        d = build_world13("start")
        w, a, b, ksA, ksB, pA, pB, timer, tl = (d[k] for k in ("w", "a", "b", "ksA", "ksB", "pA", "pB", "timer", "tl"))
        pkB = d["pkB"]
        capt = []

        def caption(text, color=CPU_COLOR):
            t = Text(text, font_size=20, color=color).move_to(P3(0, 1.75))
            return t

        # S13.1
        newmobs = [w.gauge, w.chip, *w.rings.values(), a, b, ksA, ksB, pA, pB, timer, tl, pkB]
        w.boundary.set_z_index(-5)
        self.say("Watch it with A and B.",
                 AnimationGroup(FadeOut(VGroup(*[m for m in oldmobs if m is not ow.boundary]), run_time=1.0),
                                *[FadeIn(m, run_time=1.2) for m in newmobs]))
        self.add(w.token)
        w.token.set_opacity(1)

        # S13.2
        self.say("A is running.", AnimationGroup(tl.fill("A", 4, "running"), tl.fill("B", 4, "ready"), Wiggle(a, scale_value=1.05, run_time=0.8)))

        # S13.3
        bl = bolt(0.3).move_to(timer.get_center())
        self.say("The timer fires.",
                 Succession(timer.ring(0.8), AnimationGroup(PacketFly(bl, w.chip.get_center() + UP * 0.5, arc=0.3, fade=True, run_time=0.9),
                                                            tl.fill("OS", 5, "running"))))

        # S13.4
        pk = RegPacket(COL["A"]).move_to(a.get_center())
        c1 = caption("hardware: save regs(A) → k-stack(A)")
        self.say("The hardware saves A's registers on A's kernel stack and enters the kernel.",
                 Succession(FadeIn(pk, scale=0.4, run_time=0.4), FadeIn(c1),
                            AnimationGroup(ksA.push(pk, run_time=1.2), Succession(Wait(0.3), w.down("A")),
                                           tl.fill("A", 5, "ready"), tl.fill("B", 5, "ready"))))

        # S13.5
        sw = snippet("switch()", 20).move_to(P3(0, 0.1))
        self.say("The handler decides to switch, and calls switch().",
                 AnimationGroup(FadeIn(sw, shift=DOWN * 0.2), tl.fill("OS", 6, "running"), tl.fill("A", 6, "ready"), tl.fill("B", 6, "ready")))

        # S13.6
        rk = RegPacket(KERNEL_COLOR).move_to(w.token.get_center())
        c2 = caption("OS: save regs(A) → proc(A)")
        self.say("That routine saves A's current registers into A's process structure…",
                 Succession(AnimationGroup(FadeOut(c1), FadeIn(c2), FadeIn(rk, scale=0.5)),
                            PacketFly(rk, pA.get_center(), arc=0.4, end_scale=0.5, fade=True, run_time=1.2)))

        # S13.7
        rb = RegPacket(KERNEL_COLOR).move_to(pB.get_center())
        rb.cells.set_stroke(COL["B"], 3)
        c3 = caption("OS: restore regs(B) from proc(B)")
        self.say("…restores B's from B's process structure…",
                 Succession(AnimationGroup(FadeOut(c2), FadeIn(c3), FadeIn(rb, scale=0.5)),
                            PacketFly(rb, w.token.get_center(), arc=0.4, fade=True, run_time=1.2)))

        # S13.8
        sp = Arrow(w.token.get_left(), ksA.get_right() + RIGHT * 0.05, buff=0.05, color=CPU_COLOR, stroke_width=4)
        sp2 = Arrow(w.token.get_right(), ksB.get_left() + LEFT * 0.05, buff=0.05, color=CPU_COLOR, stroke_width=4)
        sptag = Text("SP", font=MONO_FONT, font_size=18, color=CPU_COLOR).move_to(P3(-1.3, -0.75))
        self.say("…and switches the stack, to B's kernel stack.",
                 Succession(AnimationGroup(FadeOut(c3), GrowArrow(sp), FadeIn(sptag)),
                            AnimationGroup(ReplacementTransform(sp, sp2), sptag.animate.move_to(P3(1.3, -0.75)),
                                           ksA.dim_down(), ksB.glow())))

        # S13.9
        rt = Text("return-from-trap (into B)", font_size=22, color=TEXT, weight=BOLD).move_to(P3(0, 0.6))
        self.say("Then the OS executes return-from-trap.",
                 AnimationGroup(FadeOut(sw), FadeOut(sp2), FadeOut(sptag), FadeIn(rt, shift=UP * 0.2)))

        # S13.10
        b.set_expression("running")
        self.say("The hardware restores B's registers, moves to user mode, and jumps to B's program counter. B is running.",
                 Succession(FadeOut(rt),
                            w.token_hop_rest(0.45),
                            AnimationGroup(w.ride("user", rt=0.9), tl.fill("B", 7, "running"), tl.fill("A", 7, "ready")),
                            AnimationGroup(w.hop_on_chip("B"), ksB.pop(to=P3(0, 1.1), fade=True, run_time=0.9)),
                            AnimationGroup(ksB.plain(), ksA.plain())))
        self.remove(pkB)
        pA.card.set_field_now("state", "ready")

        # S13.11
        q1 = Text("?", font_size=40, color=CPU_COLOR, weight=BOLD).next_to(ksA, UP, buff=0.35)
        q2 = Text("?", font_size=40, color=CPU_COLOR, weight=BOLD).next_to(pA, UP, buff=0.05)
        self.say("So there are two kinds of saving?", stu.change("confused"), AnimationGroup(FadeIn(q1, scale=1.5), FadeIn(q2, scale=1.5)))

        # S13.12
        p1 = CurvedArrow(P3(-3.4, 0.5), ksA.get_top() + UP * 0.05, angle=0.6, color=COL["A"])
        t1 = tag("hardware · implicit", COL["A"], 16).move_to(P3(-3.0, -0.55))
        self.say("Yes. When the timer fires, the hardware saves the user registers on the kernel stack.", prof.change("explaining"),
                 AnimationGroup(FadeOut(q1), FadeOut(q2), Create(p1), FadeIn(t1)))

        # S13.13
        p2 = Arrow(P3(-0.6, -1.3), pA.get_right() + RIGHT * 0.05, buff=0, color=KERNEL_COLOR, stroke_width=5)
        t2 = tag("software · explicit", KERNEL_COLOR, 16).move_to(P3(-1.4, -1.05))
        self.say("When the OS switches, the software saves the kernel registers into the process structure.",
                 AnimationGroup(FadeOut(p1), FadeOut(t1), GrowArrow(p2), FadeIn(t2)))

        # S13.14
        ghost = w.chip.virtual_copy()
        ghost.move_to(P3(-1.0, -1.1))
        g1 = Text("trapped from A", font_size=16, color=DIM).next_to(ghost, UP, buff=0.1)
        g2 = Text("trapped from B", font_size=16, color=DIM).move_to(P3(1.0, -1.1)).shift(UP * 0.55)
        self.say("That second save makes the system look as if it trapped into the kernel from B, not from A.",
                 Succession(AnimationGroup(FadeOut(p2), FadeOut(t2), FadeIn(ghost), FadeIn(g1)),
                            AnimationGroup(ghost.animate(run_time=1.5).move_to(P3(1.0, -1.1)), FadeOut(g1, run_time=0.5),
                                           late(1.0, FadeIn(g2, run_time=0.5)),
                                           CyclicReplace(ksA.label, ksB.label, run_time=1.5)),
                            CyclicReplace(ksA.label, ksB.label, run_time=0.6), FadeOut(ghost), FadeOut(g2)))

        # S13.15
        osblocks = tl.blocks_in("OS")
        lab = Text("enter as A → leave as B", font_size=20, color=TEXT).move_to(P3(4.3, -3.1))
        arr = Arrow(lab.get_left() + LEFT * 0.05, osblocks.get_right() + RIGHT * 0.05, buff=0.05, color=KERNEL_COLOR, stroke_width=4)
        self.say("We enter switch() in A's context and leave it in B's.",
                 AnimationGroup(FadeIn(lab), GrowArrow(arr), Indicate(osblocks, color=KERNEL_COLOR)))
        self.beat(1.5)
