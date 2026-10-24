import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403

S6_DISK = P3(5.05, -2.2)
S6_REST = P3(3.3, -1.4)


def build_end():
    """S06 end: LDE world, chip at the user seat with A running, empty k-stack(A), handler box, Disk."""
    w = World("user", rest=S6_REST)
    a = w.add_proc("A", "running", where="chip")
    w.add_ring("A")
    ks = KernelStack("k-stack(A)").move_to(KSTACK_POS["A"])
    hb = handler_box(width=2.2)
    bottom_to(w.token, S6_REST)
    disk = Disk().scale(0.6).move_to(S6_DISK)
    return dict(w=w, a=a, ks=ks, hb=hb, disk=disk)


class S06SystemCall(Ep06Scene):
    def construct(self):
        self.add_badge()
        self.add_docked_term("user mode / kernel mode")
        stu, prof = corner_chars(True, "neutral", "neutral")
        w = World("kernel", rest=S6_REST)
        w.token_on_chip()
        disk = Disk().move_to(P3(4.2, -2.2))
        ks = KernelStack("k-stack(A)").move_to(KSTACK_POS["A"])
        hb = handler_box()
        a = w.add_proc("A", "ready", where="bench")
        ring = w.add_ring("A")
        self.add(w.boundary, w.gauge, w.chip, w.token, disk, stu, prof)

        # S06.1
        self.say("But then how does a program ever read a file?", stu.change("confused"),
                 Succession(AnimationGroup(FadeIn(ks), FadeIn(hb), FadeIn(ring), FadeIn(a),
                                           disk.animate.scale(0.6).move_to(S6_DISK), run_time=1.0),
                            w.up("A")))

        # S06.2
        door = door_in_line().move_to(P3(0, BY)).set_z_index(1)
        self.say("With a system call.", FadeIn(door), self.term("system call"))

        # S06.3
        icons = [FileIcon(None, width=0.35).move_to(P3(-2.4, -1.0)),
                 bottom_to(proc("C", "ready", scale=0.3, label=None), P3(-1.4, -1.25)),
                 chat_icon(0.5).move_to(P3(1.4, -1.0)),
                 VGroup(Rectangle(width=0.45, height=0.3).set_fill(MEM_COLOR, 0.4).set_stroke(MEM_COLOR, 2),
                        Text("0x", font=MONO_FONT, font_size=14, color=TEXT)).move_to(P3(2.4, -1.0))]
        self.say("System calls let the kernel carefully expose a few key services: the file system, creating and "
                 "destroying processes, talking to other processes, allocating memory.",
                 Succession(Wait(1.5), *[AnimationGroup(FadeIn(ic, shift=UP * 0.2), run_time=0.6) if k == 3 else
                                         Succession(FadeIn(ic, shift=UP * 0.2, run_time=0.6), Wait(1.8))
                                         for k, ic in enumerate(icons)]))

        # S06.4
        c1 = Text("~300", font_size=54, color=CPU_COLOR).move_to(P3(0, -2.2))
        c2 = Text("~20", font_size=54, color=CPU_COLOR).move_to(P3(0, -2.2))
        t2 = tag("early UNIX", TEXT, 22).next_to(c2, DOWN, buff=0.2)
        self.say("Real systems offer a few hundred. Early UNIX had about twenty.",
                 Succession(FadeIn(c1), Wait(0.8), AnimationGroup(Transform(c1, c2), FadeIn(t2)), Wait(0.7),
                            AnimationGroup(FadeOut(c1), FadeOut(t2), FadeOut(VGroup(*icons)))))

        # S06.5
        trap_code = snippet("trap", 24, CPU_COLOR).move_to(P3(1.7, 1.7))
        self.say("To make one, the program runs a special instruction: a trap.",
                 Succession(FadeIn(trap_code, shift=LEFT * 0.2), Indicate(trap_code, color=CPU_COLOR)),
                 late(1.0, self.note("trap")))

        # S06.6
        pk = RegPacket(COL["A"]).move_to(a.get_center())
        self.say("It jumps into the kernel and raises the privilege level, both at once.",
                 Succession(FadeIn(pk, scale=0.4, run_time=0.4),
                            AnimationGroup(ks.push(pk, run_time=1.0), Succession(Wait(0.3), w.down("A")))))
        self.play(FadeOut(trap_code), run_time=0.3)

        # S06.7
        allowed = tag("allowed?", GREEN_OK, 20).move_to(P3(2.5, -0.85))
        data = Square(0.2).set_fill(DISK_COLOR, 1).set_stroke(TEXT, 1).move_to(disk.get_center())
        self.say("Now the OS can do the privileged work, if it allows it.",
                 Succession(w.token.reach(disk.get_left() + UP * 0.1, run_time=0.8), FadeIn(allowed, scale=1.3),
                            Indicate(allowed, color=GREEN_OK), FadeIn(data),
                            AnimationGroup(PacketFly(data, P3(0.95, -1.5), arc=0.3, run_time=1.0), w.token.retract(0.8))))

        # S06.8
        a.set_expression("running")
        self.say("When it's done, a return-from-trap goes back to the program and lowers the privilege level.",
                 Succession(FadeOut(allowed),
                            w.token_hop_rest(0.45),
                            w.ride("user", riders=(data,), rt=0.9),
                            AnimationGroup(w.hop_on_chip("A"), ks.pop(to=P3(0, 1.6), fade=True, run_time=0.9)),
                            Wiggle(a, scale_value=1.08, rotation_angle=0.05, run_time=0.6)),
                 late(0.5, self.note("return-from-trap")))
        self.remove(pk)
        self.play(FadeOut(data), run_time=0.3)

        # S06.9
        pk2 = RegPacket(COL["A"]).move_to(a.get_center())
        saved = Text("saved by hardware", font_size=22, color=CPU_COLOR).move_to(P3(-3.6, -0.7))
        self.say("The hardware must save the caller's registers, to be able to come back.",
                 Succession(FadeIn(pk2, scale=0.4, run_time=0.4), ks.push(pk2, run_time=1.6), FadeIn(saved)))

        # S06.10
        lab = RegPacket(COL["A"], labels=["PC", "flags", "..."]).move_to(ks.slot_point(0))
        kl = Text("kernel stack", font_size=22, color=KERNEL_COLOR).move_to(P3(-3.6, -2.75))
        self.say("On x86, it pushes the program counter, the flags and a few more onto a per-process kernel stack.",
                 Succession(AnimationGroup(FadeOut(saved), ReplacementTransform(pk2, lab)),
                            AnimationGroup(FadeIn(kl, shift=UP * 0.1), Wait(1.5)), FadeOut(kl)))
        ks.items[-1] = lab

        # S06.11
        self.say("Return-from-trap pops them off again.",
                 ks.pop(to=a.get_center(), fade=True, run_time=1.2))

        # S06.12
        sn = snippet('fd = open("notes.txt", ...);', 20).move_to(P3(-3.3, 2.0))
        self.say("When I write open() in C, it looks like an ordinary function call.", stu.change("curious"),
                 FadeIn(sn, shift=RIGHT * 0.5))

        # S06.13
        chips = VGroup(*[tag(t, TEXT, 14) for t in ("args to regs", "syscall number", "trap!")]).arrange(RIGHT, buff=0.1)
        box = RoundedRectangle(width=5.0, height=2.0, corner_radius=0.12).set_stroke(USER_COLOR, 3).set_fill(USER_COLOR, 0.06)
        box.move_to(P3(-3.4, 2.35))
        sn.move_to(box.get_center() + UP * 0.1)
        chips.move_to(box.get_bottom() + UP * 0.35)
        cl = Text("C library", font_size=22, color=USER_COLOR, weight=BOLD).move_to(box.get_corner(UL) + P3(0.7, -0.25))
        trap_arrow = Arrow(box.get_bottom() + RIGHT * 1.5, P3(-0.4, -0.2), buff=0.05, color=CPU_COLOR, stroke_width=5)
        self.say("It is. A call into the C library, which puts the arguments in agreed places, executes the trap, "
                 "and unpacks the result.", prof.change("happy"),
                 Succession(AnimationGroup(FadeIn(box), FadeIn(cl), sn.animate.move_to(box.get_center() + UP * 0.2)),
                            LaggedStart(*[FadeIn(c) for c in chips], lag_ratio=0.5), GrowArrow(trap_arrow),
                            FadeOut(trap_arrow)))

        # S06.14
        hand = tag("hand-coded assembly", CPU_COLOR, 18).move_to(box.get_bottom() + DOWN * 0.0)
        self.say("Somebody wrote that assembly for you.", prof.change("proud"),
                 Succession(FadeIn(hand, scale=1.2), Wait(1.0), FadeOut(VGroup(box, cl, sn, chips, hand), run_time=0.6)),
                 min_time=2.2)
