import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403
from s06_system_call import build_end as s06_end  # noqa: E402

REST7 = P3(-2.6, -2.3)
TT_POS = P3(3.5, -1.45)
H_COLS = [CPU_COLOR, VIRT, USER_COLOR]


def handler_boxes():
    g = VGroup()
    for name, c, x in zip(("syscall", "timer", "keyboard"), H_COLS, (2.3, 3.5, 4.7)):
        b = RoundedRectangle(width=1.1, height=0.45, corner_radius=0.08).set_fill(c, 0.12).set_stroke(c, 2.5)
        t = Text(name, font=FONT, font_size=16, color=TEXT).move_to(b)
        g.add(VGroup(b, t).move_to(P3(x, -3.05)))
    return g


class S07TrapTable(Ep06Scene):
    def construct(self):
        self.add_badge()
        self.add_docked_term("return-from-trap")
        stu, prof = corner_chars(True, "neutral", "neutral")
        d = s06_end()
        w, a, ks, hb, disk = d["w"], d["a"], d["ks"], d["hb"], d["disk"]
        w.rest = REST7
        self.add(w.boundary, w.gauge, w.chip, *w.rings.values(), a, w.token, ks, hb, disk, stu, prof)

        # S07.1
        sticky = sticky_note("jump to 0x40", 0.9).move_to(P3(1.7, 1.6))
        b1 = tag("check permission", TEXT, 22).move_to(P3(-1.7, -1.7))
        b2 = tag("do the work", TEXT, 22).move_to(P3(1.7, -1.7))
        arr = DashedLine(sticky.get_bottom() + DOWN * 0.1, b1.get_top() + UP * 0.05, dash_length=0.12).add_tip(tip_length=0.2)
        self.say("Wait. The trap jumps into the kernel. Which code? Does the program say?", stu.change("curious"),
                 AnimationGroup(FadeOut(ks), FadeOut(hb), FadeOut(disk), w.token_hop_rest(0.6), FadeIn(sticky)),
                 Succession(Wait(1.5), AnimationGroup(FadeIn(b1), FadeIn(b2)), Create(arr)))

        # S07.2
        arr2 = DashedLine(sticky.get_bottom() + DOWN * 0.1, b2.get_top() + UP * 0.05, dash_length=0.12).add_tip(tip_length=0.2)
        self.say("It must never say. A program that picks any address in the kernel could jump just past a "
                 "permission check.", prof.change("worried"),
                 Succession(ReplacementTransform(arr, arr2), Indicate(b2, color=RED_BAD, scale_factor=1.2),
                            Flash(b2.get_center(), color=RED_BAD, flash_radius=0.5)))

        # S07.3
        xm = x_mark(0.5).move_to(sticky.get_center())
        self.say("That's a Very Bad Idea.",
                 Succession(FadeOut(arr2), FadeIn(xm, scale=1.8), ShiftBy(VGroup(sticky, xm), DOWN * 1.7, run_time=0.6),
                            w.boundary.flash_at(1.7, RED_BAD), ShiftBy(VGroup(sticky, xm), UP * 1.7, run_time=0.6)))

        # S07.4
        sw = PowerSwitch(0.9, on=False).move_to(P3(-4.8, -1.9))
        boot = Text("BOOT", font_size=22, color=TEXT, weight=BOLD).next_to(sw, DOWN, buff=0.5)
        self.say("So the kernel decides in advance. At boot the machine starts in kernel mode, free to configure "
                 "the hardware.",
                 Succession(AnimationGroup(FadeOut(a), FadeOut(w.rings["A"]), FadeOut(sticky), FadeOut(xm), FadeOut(b1), FadeOut(b2)),
                            w.down(None), AnimationGroup(FadeIn(sw), FadeIn(boot)), sw.flip(True)))

        # S07.5
        tt = TrapTable(filled=0, dim_rows=(1,)).move_to(TT_POS)
        steps = [FadeIn(tt, run_time=0.8)]
        for i in range(3):
            steps += [w.token.reach(P3(tt.get_left()[0] + 0.05, TT_POS[1] + 0.4 - 0.4 * i), run_time=0.5),
                      tt.add_row(i), w.token.retract(0.3)]
        self.say("One of the first things the OS does is install a trap table…",
                 Succession(*steps), late(0.3, self.note("trap table")))

        # S07.6
        hbx = handler_boxes()
        ars = VGroup(*[Arrow(P3(x, TT_POS[1] - 0.95), P3(x, -2.8), buff=0.02, stroke_width=3, tip_length=0.12, color=c)
                       for x, c in zip((2.3, 3.5, 4.7), H_COLS)])
        slot = RoundedRectangle(width=1.2, height=0.4, corner_radius=0.06).set_fill(CARD_FILL, 1).set_stroke(DIM, 2).move_to(P3(0, -2.95))
        rem = Text("remember", font_size=20, color=DIM).next_to(slot, LEFT, buff=0.15)
        addr = Text("0x1000", font=MONO_FONT, font_size=18, color=TEXT).move_to(tt.header).set_z_index(20)
        self.say("…it tells the hardware what code to run on a disk interrupt, a keyboard interrupt, a system call.",
                 Succession(AnimationGroup(FadeIn(hbx, shift=UP * 0.2), *[GrowArrow(a_) for a_ in ars]),
                            AnimationGroup(FadeIn(slot), FadeIn(rem)), FadeIn(addr),
                            PacketFly(addr, slot.get_center(), arc=0.3, run_time=1.2)))

        # S07.7
        lk = padlock_icon(0.3, GREEN_OK).move_to(slot.get_right() + RIGHT * 0.3)
        self.say("Those are the trap handlers, and the hardware remembers them until the next reboot.",
                 Succession(self.note("trap handlers"), FadeIn(lk, scale=1.6)))

        # S07.8
        load = Arrow(tt.get_bottom() + LEFT * 1.3, slot.get_right() + RIGHT * 0.65, buff=0.08, color=KERNEL_COLOR, stroke_width=4)
        priv = Text("privileged", font_size=22, color=KERNEL_COLOR, weight=BOLD).move_to(P3(1.5, -2.3))
        self.say("Installing the table is itself a privileged instruction.",
                 AnimationGroup(GrowArrow(load), FadeIn(priv)))

        # S07.9
        mine = bottom_to(proc("A", "ready", scale=0.8), P3(-2.8, 0.8))
        mt = TrapTable(rows=("my code", "my code", "my code"), filled=3, width=3.6).scale(0.4).move_to(P3(-2.8, 2.5))
        self.say("And if I could install my own table?", stu.change("excited"),
                 AnimationGroup(FadeOut(VGroup(load, priv, sw, boot)), FadeIn(mine), FadeIn(mt)))

        # S07.10
        pl = padlock_icon(0.5, RED_BAD).move_to(P3(-2.8, BY + 0.05))
        self.say("Then every trap would run your code, in kernel mode. You'd own the machine.", prof.change("explaining"),
                 Succession(ShiftBy(mt, DOWN * 2.2, run_time=1.0), AnimationGroup(FadeIn(pl, scale=1.5), w.boundary.flash_at(-2.8, RED_BAD)),
                            Indicate(pl, color=RED_BAD), ShiftBy(mt, UP * 2.2, run_time=1.0), FadeOut(pl)))

        # S07.11
        eax = VGroup(RoundedRectangle(width=1.3, height=0.42, corner_radius=0.06).set_fill(CARD_FILL, 1).set_stroke(DIM, 2),
                     Text("eax", font=MONO_FONT, font_size=20, color=DIM)).move_to(P3(-0.9, 1.4))
        eax[1].move_to(eax[0].get_left() + RIGHT * 0.4)
        card = tag("#5", CPU_COLOR, 22).move_to(mine.get_right() + UP * 0.5)
        self.say("The program doesn't give an address. It gives a system-call number.",
                 Succession(AnimationGroup(FadeOut(mt), FadeIn(eax), FadeIn(card), self.note("system-call number")),
                            PacketFly(card, eax[0].get_right() + LEFT * 0.35, arc=0.3, run_time=0.8)))

        # S07.12
        ok = tick_mark(0.3).next_to(w.token, UP, buff=0.05)
        hit = tag("#5 = open()", CPU_COLOR, 18).next_to(hbx[0], DOWN, buff=0.0).shift(DOWN * 0.0)
        hit.move_to(P3(2.3, -3.52))
        self.say("The handler checks that it's valid and runs the matching code.",
                 Succession(PacketFly(card, w.token.get_center(), arc=0.4, fade=True, run_time=1.0), FadeIn(ok, scale=1.5),
                            tt.highlight_row(0), hbx[0][0].animate.set_fill(CPU_COLOR, 0.6), FadeIn(hit)))

        # S07.13
        t1 = VGroup(Text("jump to an address", font_size=22, color=TEXT), x_mark(0.2)).arrange(RIGHT, buff=0.15)
        t2 = VGroup(Text("system-call number", font_size=22, color=TEXT), tick_mark(0.2)).arrange(RIGHT, buff=0.15)
        both = VGroup(t1, t2).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to(P3(3.6, 1.6))
        pr_l = Text("protection", font_size=26, color=KERNEL_COLOR, weight=BOLD).move_to(P3(3.6, 2.4))
        self.say("That indirection is protection: user code can only request a service.",
                 Succession(FadeOut(ok), FadeIn(pr_l), FadeIn(both)))

        # S07.14
        tip = TipCard("Be wary of user inputs.", width=4.0, font_size=26).move_to(P3(3.6, 1.7))
        wcode = snippet("write(fd, buf, n)", 22).move_to(P3(-3.3, 1.4))
        kmem = VGroup(Rectangle(width=0.9, height=1.6).set_fill(KERNEL_COLOR, 0.5).set_stroke(KERNEL_COLOR, 3),
                      Text("kernel memory", font_size=16, color=TEXT)).move_to(P3(-3.6, -1.9))
        kmem[1].move_to(kmem[0].get_top() + UP * 0.2)
        bufarr = Arrow(wcode.get_bottom() + RIGHT * 0.2, kmem[0].get_top() + UP * 0.45, buff=0.05, color=RED_BAD, stroke_width=4)
        x2 = x_mark(0.4).move_to(kmem[0].get_center())
        self.say("And the kernel stays suspicious even then. A write() whose buffer points inside kernel memory must "
                 "be refused.", prof.change("proud"),
                 Succession(AnimationGroup(FadeOut(both), FadeOut(pr_l), FadeOut(VGroup(mine, eax, hit)), tip.slide_in()),
                            AnimationGroup(FadeIn(wcode), FadeIn(kmem)), GrowArrow(bufarr), FadeIn(x2, scale=1.8)))
        self.play(tip.slide_out(), FadeOut(VGroup(wcode, kmem, bufarr, x2)), run_time=0.8)
