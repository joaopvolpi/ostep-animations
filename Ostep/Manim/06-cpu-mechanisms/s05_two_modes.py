import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403
from s04_restricted_operations import build_end as s04_end  # noqa: E402

S5_DISK = P3(4.2, -2.2)
REST5 = P3(-2.4, -2.5)


class S05TwoModes(Ep06Scene):
    def construct(self):
        self.add_badge()
        self.add_docked_term("limited direct execution")
        stu, prof = corner_chars(True, "neutral", "neutral")
        d = s04_end()
        glyph, lk, disk, a, st = d["glyph"], d["lock"], d["disk"], d["a"], d["strip"]
        self.add(stu, prof, st, disk, a, glyph, lk)
        w = World("user", rest=REST5)
        a.set_z_index(4)

        # S05.1
        self.say("So the CPU gets two modes.",
                 AnimationGroup(FadeOut(st), w.boundary.draw(1.5),
                                disk.animate(run_time=1.5).move_to(S5_DISK),
                                ReplacementTransform(VGroup(glyph, lk), w.chip),
                                FadeIn(w.gauge)),
                 Succession(Wait(1.6), hop_bottom(a, w.chip_slot(), run_time=0.7)),
                 late(1.0, self.note("user mode / kernel mode")))
        a.set_expression("running")

        # S05.2
        req = Arrow(a.get_right() + UP * 0.1, P3(2.1, -0.28), buff=0, stroke_width=5, color=COL["A"])
        io = Text("I/O", font=MONO_FONT, font_size=22, color=COL["A"]).next_to(req, RIGHT, buff=0.1).shift(UP * 0.2)
        self.say("In user mode, code is restricted: if a process tries to issue an I/O request…",
                 Succession(Wait(1.0), AnimationGroup(GrowArrow(req), FadeIn(io), run_time=1.5)))

        # S05.3
        bang = Text("!", font_size=48, color=RED_BAD, weight=BOLD).next_to(a, UP, buff=0.0)
        xm = x_mark(0.5).move_to(a.get_center())
        priv = Text("privileged operation", font_size=30, color=KERNEL_COLOR, weight=BOLD).move_to(P3(4.0, 1.7))
        self.say("…the processor raises an exception, and the OS will most likely kill it.",
                 Succession(AnimationGroup(req.animate.put_start_and_end_on(P3(1.9, -0.1), P3(1.0, 0.5)).set_color(RED_BAD),
                                           w.boundary.flash_at(2.1, RED_BAD), run_time=0.7),
                            FadeIn(bang, scale=1.6), FadeIn(xm, scale=1.8), Wait(0.5),
                            AnimationGroup(FadeOut(a, shift=DOWN * 0.3), FadeOut(bang), FadeOut(xm), FadeOut(req), FadeOut(io))),
                 Succession(Wait(1.5), FadeIn(priv, shift=UP * 0.2), Wait(1.5), FadeOut(priv)))

        # S05.4
        pk = Square(0.2).set_fill(DISK_COLOR, 1).set_stroke(TEXT, 1).move_to(disk.top_point())
        self.say("In kernel mode, where the OS runs, code can do anything, including every privileged operation.",
                 Succession(FadeIn(w.token, shift=UP * 0.2, run_time=0.5),
                            w.token_hop_chip(seat=USER_SEAT, rt=0.6),
                            w.ride("kernel", riders=(w.token,), rt=0.9),
                            w.token.reach(disk.get_left() + UP * 0.2, run_time=0.8),
                            PacketFly(pk, w.token.get_center(), arc=0.3, fade=True, run_time=0.9),
                            w.token.retract(0.4)))

        # S05.5
        thumb = VGroup(RoundedRectangle(width=2.4, height=1.2, corner_radius=0.1).set_fill(CARD_FILL, 1).set_stroke(DIM, 2),
                       DashedLine(P3(-1.0, 0), P3(1.0, 0), dash_length=0.1).set_stroke(TEXT, 2),
                       Text("user", font_size=16, color=USER_COLOR).move_to(P3(-0.7, 0.35)),
                       Text("kernel", font_size=16, color=KERNEL_COLOR).move_to(P3(-0.7, -0.35)))
        thumb.move_to(P3(-4.5, 2.0))
        make_translucent(thumb, 0.6, 0.7)
        self.say("You've met this: the dashed line from our first episode, user above, kernel below, and the gauge "
                 "that reads which side you're on. Now it goes to work.",
                 stu.change("excited"),
                 Succession(FadeIn(thumb), Wait(1.0), AnimationGroup(w.boundary.pulse(2, 2.0),
                                                                     thumb.animate(run_time=2.0).move_to(P3(-2.0, BY)).set_opacity(0))))
