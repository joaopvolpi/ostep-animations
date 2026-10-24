import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403

LEFT_C = P3(-3.45, 0.3)
RIGHT_C = P3(3.45, 0.3)
PANEL_W, PANEL_H = 6.3, 4.6


def ik(origin, target, l1, l2):
    """Elbow-up 2-link inverse kinematics: returns (a1, a2) absolute angles."""
    d = np.array(target) - np.array(origin)
    r = min(np.linalg.norm(d[:2]), l1 + l2 - 1e-3)
    base = np.arctan2(d[1], d[0])
    c = np.clip((l1 ** 2 + r ** 2 - l2 ** 2) / (2 * l1 * r), -1, 1)
    a1 = base - np.arccos(c)
    elbow = np.array(origin) + l1 * P3(np.cos(a1), np.sin(a1))
    e2 = np.array(target) - elbow
    a2 = np.arctan2(e2[1], e2[0])
    return a1, a2


def arm_move(arm, target, carry=None, offset=None, run_time=1.0):
    """Animate the arm tip to ``target`` (optionally carrying a mobject whose
    center stays at tip + offset)."""
    a10, a20 = arm.a1, arm.a2
    a11, a21 = ik(arm._origin, target, arm.l1, arm.l2)

    def upd(m, alpha):
        a = smooth(alpha)
        m.set_pose(a10 + (a11 - a10) * a, a20 + (a21 - a20) * a)
        if carry is not None:
            carry.move_to(m.tip() + offset)
    return UpdateFromAlphaFunc(arm, upd, run_time=run_time)


class S08HowVsWhich(Ep04Scene):
    def construct(self):
        self.add_badge()
        self.add_docked_term("space sharing")
        stu, prof = self.add_corner_chars("neutral", "explaining")
        d = build_s06_parts(final=True)
        add_s06_world(self, d)
        split, cpu, ps, tl = d["split"], d["cpu"], d["ps"], d["tl"]

        # S08.1 -- collapse to the right-side world: A on the CPU, B and C queued
        q = Queue(label="Ready", center=(0, -2.0), slots=3, spacing=1.2, font_size=24)
        a, b, c = ps["A"], ps["B"], ps["C"]
        left_side = VGroup(d["vcpus"], *d["vps"].values(), d["gauges"])
        q_spots = [q.slot_point(0), q.slot_point(1)]
        cpu_target = cpu.copy().move_to(CPU_HOME)
        q.items = [b, c]
        dq = Text("do?", font_size=34, color=CPU_COLOR, weight="BOLD")
        wq = Text("who?", font_size=34, color=VIRT, weight="BOLD")
        with self.narrate("Wait, back to taking turns. Somebody has to do the switching. And somebody has to decide who's next."):
            self.play(FadeOut(left_side), FadeOut(split), FadeOut(tl),
                      cpu.animate.move_to(CPU_HOME),
                      a.animate.shift(cpu_target.slot_point() + UP * 0.02 - a.get_bottom()),
                      b.animate.move_to(b.copy().shift(q_spots[0] - b.get_bottom())),
                      c.animate.move_to(c.copy().shift(q_spots[1] - c.get_bottom())),
                      FadeIn(q), run_time=1.4)
            self.play(a.change("running"), c.change("ready"), run_time=0.3)
            dq.next_to(a, RIGHT, buff=0.3)
            wq.next_to(q.tray, RIGHT, buff=0.4).shift(UP * 0.7)
            self.play(stu.change("confused", look_at=cpu), FadeIn(dq, scale=1.5), FadeIn(wq, scale=1.5))
        self.beat(0.5)

        # S08.2 -- split into two panels
        lp = RoundedRectangle(width=PANEL_W, height=PANEL_H, corner_radius=0.2).move_to(LEFT_C).set_stroke(DIM, 2)
        rp = RoundedRectangle(width=PANEL_W, height=PANEL_H, corner_radius=0.2).move_to(RIGHT_C).set_stroke(DIM, 2)
        world_l = VGroup(cpu, a)
        cpu_pos = P3(-4.4, -1.1)
        new_q = Queue(label="Ready", center=(3.45, -1.55), slots=3, spacing=1.05, font_size=22)
        with self.narrate("Two different jobs. You've just spotted one of the best design ideas in operating systems."):
            self.play(prof.change("proud"), FadeOut(dq), FadeOut(wq), run_time=0.6)
            self.play(Create(lp), Create(rp),
                      world_l.animate.scale(0.8).move_to(cpu_pos + (world_l.get_center() - cpu.get_center()) * 0.8),
                      Transform(q, new_q),
                      b.animate.scale(0.85).move_to(new_q.slot_point(0) + UP * 1.39 * 0.85 / 2),
                      c.animate.scale(0.85).move_to(new_q.slot_point(1) + UP * 1.39 * 0.85 / 2),
                      run_time=1.4)
        q_slots = [new_q.slot_point(0), new_q.slot_point(1)]
        bottom_to(b, q_slots[0])
        bottom_to(c, q_slots[1])

        # S08.3
        how = Text("HOW · mechanism", font_size=30, color=TEXT, weight="BOLD").move_to(LEFT_C + UP * 1.95)
        which = Text("WHICH · policy", font_size=30, color=TEXT, weight="BOLD").move_to(RIGHT_C + UP * 1.95)
        with self.narrate("The first job is a mechanism."):
            self.play(self.term("mechanism"), late(2.4, Write(how, run_time=0.8)))

        # S08.4
        gears = GearPair(radius=0.5).move_to(P3(-1.6, 0.9))
        gears.add_updater(lambda m, dt: (m.big.rotate(-0.9 * dt), m.small.rotate(0.9 * dt * m.r1 / m.r2)))
        self.say("That's low-level machinery that answers a how question.", FadeIn(gears, scale=0.6, run_time=0.8))

        # S08.5
        arm = RoboticArm(l1=1.6, l2=1.4, color="#B8B8B8", joint_color=KERNEL_COLOR)
        arm.move_origin(P3(-2.2, -1.55))
        arm.set_pose(*ik(arm._origin, P3(-2.4, 0.9), 1.6, 1.4))
        grab = a.get_top() + UP * 0.05
        offset = a.get_center() - grab
        park = P3(-3.0, 1.55)
        holder = Process("ready", color=DIM, label="next").scale(0.8 * 1.0)
        make_translucent(holder, 0.5, 0.8)
        bottom_to(holder, cpu.slot_point() + UP * 0.02)
        with self.narrate("How do we stop one program and start another?"):
            self.play(FadeIn(arm), run_time=0.5)
            self.play(arm_move(arm, grab, run_time=0.8))
            a.set_expression("ready")
            self.play(arm_move(arm, park - offset, carry=a, offset=offset, run_time=1.0))
            self.play(FadeIn(holder, shift=DOWN * 0.3), run_time=0.6)

        # S08.6
        tag = ep_tag("→ Ep. 06").scale(0.9).next_to(gears, RIGHT, buff=0.12).shift(DOWN * 0.35)
        self.say("That mechanism is called a context switch, and it gets its own episode later.",
                 self.note("context switch"), late(1.6, FadeIn(tag, scale=1.3, run_time=0.5)))

        # S08.7
        self.say("The second job is a policy. That's an algorithm that answers a which question.",
                 self.term("policy"), late(2.4, Write(which, run_time=0.8)))

        # S08.8
        spot = Spotlight(height=1.9, spread=0.5)
        spot.move_beam_to(b.get_bottom() + LEFT * 1.0)
        sp_lab = Text("scheduling policy", font_size=24, color=VIRT).move_to(RIGHT_C + UP * 1.55)
        with self.narrate("Given all the processes that could run, which one should run now? "
                          "That's a scheduling policy."):
            self.play(FadeIn(spot), run_time=0.5)
            self.play(spot.animate.move_beam_to(b.get_bottom()), run_time=0.6)
            self.play(spot.animate.move_beam_to(c.get_bottom()), run_time=0.6)
            self.play(spot.animate.move_beam_to(b.get_bottom()), run_time=0.5)
            self.play(spot.animate.move_beam_to(c.get_bottom()), run_time=0.6)
            self.play(Write(sp_lab), run_time=0.8)

        # S08.9-11
        chips_y = 0.95
        hist = VGroup(mini_bar_chart(0.45), Text("history", font_size=18, color=DIM))
        work = VGroup(tag_icon(0.55), Text("workload", font_size=18, color=DIM))
        goal = VGroup(dial_icon(0.6), Text("interactive vs. throughput", font_size=15, color=DIM))
        for g in (hist, work, goal):
            g[1].next_to(g[0], DOWN, buff=0.06)
        # keep the lamp area (above the queue) clear: two chips left, one right
        hist.move_to(P3(1.2, chips_y))
        work.move_to(P3(2.35, chips_y))
        goal.move_to(P3(5.3, chips_y))
        self.say("It might look at history (who ran the most in the last minute?),",
                 FadeIn(hist, shift=DOWN * 0.2, run_time=0.6))
        self.say("at what kind of programs these are,", FadeIn(work, shift=DOWN * 0.2, run_time=0.6))
        self.say("or at what we're optimizing for: snappy interaction or total throughput.",
                 FadeIn(goal, shift=DOWN * 0.2, run_time=0.6),
                 late(0.6, Rotate(goal[0].needle, -0.9, about_point=goal[0][3].get_center(),
                                              run_time=0.8, rate_func=there_and_back)))

        # S08.12
        seam = Line(P3(0, -1.9), P3(0, 2.5)).set_stroke(TEXT, 3)
        tip = TipCard(VGroup(), title="TIP · Separate policy and mechanism", width=6.0, height=0.62)
        tip.move_to(P3(0, 2.95))
        with self.narrate("Keeping the two apart is a form of modularity."):
            self.play(self.note("modularity"))
            self.play(Create(seam), FadeIn(tip, shift=DOWN * 0.2), run_time=0.8)

        # S08.13
        spot2 = Spotlight(height=1.9, spread=0.5, color="#BFE6FF")
        spot2.move_beam_to(b.get_bottom() + RIGHT * 8)
        self.say("You can swap in a smarter policy without rebuilding the machinery underneath.",
                 Succession(spot.animate(run_time=0.7).shift(RIGHT * 8),
                            spot2.animate(run_time=0.8).move_beam_to(b.get_bottom())))
        self.beat(1.0)

        # transition: keep only the CPU with A, back at home
        gears.clear_updaters()
        keep = VGroup(cpu, a)
        protected = (self.badge, self.terms.docked, stu, prof)
        for m in list(self.mobjects):
            if m not in (cpu, a) and (cpu in m.get_family() or a in m.get_family()):
                self.remove(m)
                self.add(*[x for x in m.submobjects if x not in (cpu, a)])
        self.add(cpu, a)
        others = [m for m in self.mobjects if m not in (cpu, a) and m not in protected]
        a.set_expression("running")
        a_t = a.copy().scale(1 / 0.8)
        bottom_to(a_t, CPU(CPU_SIZE).move_to(CPU_HOME).slot_point() + UP * 0.02)
        self.play(*[FadeOut(m) for m in others], cpu.animate.scale(1 / 0.8).move_to(CPU_HOME),
                  Transform(a, a_t), run_time=1.0)
        self.wait(0.3)
