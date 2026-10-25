import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403
from s13_watching_a_switch import build_end as s13_end  # noqa: E402
from s14_xv6_code import stage_mobs  # noqa: E402

MINI_SCALE = 0.45
MINI_CENTER = P3(3.3, 0.0)
ROOM = P3(-3.3, 0.3)


def mini_world():
    """The whole LDE world (boundary, chip, A running, sleeping token, gauge, trap table, timer) at 45%."""
    boundary = UserKernelBoundary(y=BY, x_range=(-7.2, 7.2), label_size=26)
    chip = CPU(CHIP, label="CPU", pins=3).move_to(USER_SEAT).set_z_index(2)
    a = proc("A", "running", scale=PS)
    bottom_to(a, chip.slot_point() + UP * 0.2).set_z_index(4)
    token = KernelToken().set_z_index(5)
    bottom_to(token, P3(-2.3, -2.3))
    token.badge.set_fill(opacity=0.35).set_stroke(opacity=0.35)
    token.text.set_opacity(0.35)
    gauge = PrivilegeGauge(height=1.6, width=0.4, level="user").move_to(GAUGE_POS)
    tt = TrapTable(filled=3, width=3.4, height=1.6).move_to(P3(3.2, -1.6))
    timer = AlarmClock(0.4).move_to(P3(4.4, 2.2))
    timer.led.set_fill(GREEN_OK, 1)
    g = VGroup(boundary, chip, a, token, gauge, tt, timer)
    g.scale(MINI_SCALE)
    g.shift(MINI_CENTER - g.get_center())
    g.parts = dict(boundary=boundary, chip=chip, a=a, token=token, gauge=gauge, tt=tt, timer=timer)
    return g


def room_parts():
    room = RoundedRectangle(width=5.0, height=3.2, corner_radius=0.3).set_stroke(DIM, 3).set_fill(DIM, 0.05).move_to(ROOM)
    rug = Ellipse(width=2.0, height=0.5).set_fill(COL["B"], 0.25).set_stroke(COL["B"], 2).move_to(ROOM + P3(0, -0.8))
    baby = bottom_to(proc("A", "ready", scale=0.6), ROOM + P3(0, -0.75)).set_z_index(4)
    cab = cabinet_lock(1.1).move_to(ROOM + P3(-1.8, 0.2))
    soc = socket_cover(0.9).move_to(ROOM + P3(1.8, -0.4))
    clock = ClockIcon(0.3).move_to(ROOM + P3(0, 1.2))
    return dict(room=room, rug=rug, baby=baby, cab=cab, soc=soc, clock=clock)


def build_end():
    r = room_parts()
    m = mini_world()
    return dict(r=r, m=m)


class S16BabyProofing(Ep06Scene):
    def construct(self):
        self.add_badge()
        self.add_docked_term("locking")
        stu, prof = corner_chars(True, "neutral", "neutral")
        d = s13_end()
        w = d["w"]
        w.boundary.set_z_index(-5)
        stage = stage_mobs(d)
        self.add(*stage, stu, prof)
        r = room_parts()
        m = mini_world()
        P = m.parts
        dimmer = Rectangle(width=7.3, height=8.2).set_fill(BG, 0.65).set_stroke(width=0).move_to(P3(3.35, 0)).set_z_index(8)

        self.allow_overlap(P["tt"].rule, P["tt"], "the table rule hugs its first row at 45% size")
        # S16.1
        self.say("One more picture to hold onto. This is how the world works, too.",
                 AnimationGroup(FadeOut(VGroup(*stage), run_time=1.0), FadeIn(m, run_time=1.0), FadeIn(dimmer, run_time=1.0)),
                 Succession(Wait(0.8), AnimationGroup(FadeIn(r["room"]), FadeIn(r["rug"]), FadeIn(r["baby"]))))

        # S16.2
        self.say("When parents baby-proof a room, they lock the cabinets with dangerous things and cover the "
                 "electrical sockets.",
                 Succession(GrowFromCenter(r["cab"]), Wait(1.5), GrowFromCenter(r["soc"])))

        # S16.3
        baby = r["baby"]
        self.say("Once that's done, the baby can roam freely, and the parents can relax.",
                 Succession(ShiftBy(baby, LEFT * 0.8, run_time=1.0), ShiftBy(baby, RIGHT * 1.6, run_time=1.5),
                            ShiftBy(baby, LEFT * 0.8, run_time=1.0)))
        baby.set_expression("running")

        # S16.4
        tl = m.parts["boundary"].line
        a1 = Arrow(r["cab"].get_top() + UP * 0.05, P3(tl.get_left()[0] + 2.2, tl.get_center()[1]) + UP * 0.05, buff=0.05, color=DIM, stroke_width=3)
        a2 = Arrow(r["soc"].get_right() + RIGHT * 0.05, P["tt"].get_left() + LEFT * 0.05, buff=0.05, color=DIM, stroke_width=3)
        a3 = Arrow(r["clock"].get_right() + RIGHT * 0.05, P["timer"].get_left() + LEFT * 0.05, buff=0.05, color=DIM, stroke_width=3)
        self.say("The OS baby-proofs the CPU.",
                 Succession(FadeIn(r["clock"]), AnimationGroup(GrowArrow(a1), GrowArrow(a2), GrowArrow(a3)),
                            FadeOut(dimmer, run_time=1.0)))

        # S16.5
        sw = PowerSwitch(0.5, on=True).move_to(P3(0.3, -2.8))
        self.say("At boot it sets up the trap handlers and starts the timer.",
                 Succession(FadeIn(sw), Indicate(P["tt"], color=CPU_COLOR, scale_factor=1.15), Indicate(P["timer"], color=CPU_COLOR, scale_factor=1.3)))

        # S16.6
        fast = tag("FAST", GREEN_OK, 20).move_to(P3(3.3, 2.5))
        dy = (KERNEL_SEAT - USER_SEAT) * MINI_SCALE
        chip, a = P["chip"], P["a"]
        fx = chip.get_center()[0]
        by = P["boundary"].line.get_center()[1]
        up = -dy
        self.say("Then it runs processes only in restricted mode, at full speed, and steps in only for privileged "
                 "operations, or when a process has held the CPU too long.",
                 Succession(FadeIn(fast), Wait(2.0),
                            AnimationGroup(ShiftBy(chip, dy, run_time=0.6), ShiftBy(a, dy, run_time=0.6), Flash(P3(fx - 0.65, by), color=CPU_COLOR, flash_radius=0.2)),
                            AnimationGroup(ShiftBy(chip, up, run_time=0.6), ShiftBy(a, up, run_time=0.6)),
                            Wait(1.5),
                            AnimationGroup(ShiftBy(chip, dy, run_time=0.6), ShiftBy(a, dy, run_time=0.6), Flash(P3(fx - 0.65, by), color=CPU_COLOR, flash_radius=0.2)),
                            AnimationGroup(ShiftBy(chip, up, run_time=0.6), ShiftBy(a, up, run_time=0.6))))

        # S16.7
        self.say("So that's the \"limited\" in limited direct execution!", stu.change("excited"),
                 self.note("limited direct execution"))

        # S16.8
        self.say("That's the \"limited.\"", prof.change("proud"))
        self.beat(1.5)
        self.play(FadeOut(self.badge))
