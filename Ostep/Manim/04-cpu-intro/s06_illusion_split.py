import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


def juggler(rx=0.75, ry=0.6):
    """Three balls cycling on an elliptical juggling path above a hand;
    returns (group, tracker)."""
    path = DashedVMobject(Ellipse(width=2 * rx, height=2 * ry), num_dashes=24).set_stroke(DIM, 2)
    hand = VGroup(Arc(radius=0.22, start_angle=PI, angle=PI).set_stroke(STUDENT_COLOR, 6))
    hand.move_to(path.get_bottom() + DOWN * 0.12)
    balls = VGroup(*[Dot(radius=0.13, color=c).set_stroke(TEXT, 1.5) for c in (COL["A"], COL["B"], COL["C"])])
    t = ValueTracker(0)
    center = path.get_center()

    def upd(g):
        c = path.get_center()
        for k, b in enumerate(g):
            ang = -PI / 2 + TAU * ((t.get_value() + k / 3) % 1.0)
            b.move_to(c + P3(rx * np.cos(ang), ry * np.sin(ang)))
    balls.add_updater(upd)
    upd(balls)
    return VGroup(path, hand, balls), t


def titles_dip(split, hold=2.0):
    t = VGroup(split.left_title, split.right_title)
    return Succession(t.animate(run_time=0.4).set_opacity(0), Wait(hold), t.animate(run_time=0.5).set_opacity(1))


class S06IllusionSplit(Ep04Scene):
    def construct(self):
        self.add_badge()
        self.add_docked_term("process")
        stu, prof = self.add_corner_chars()
        cpu0, ps0 = build_world_s05_end()
        self.add(cpu0, *ps0.values())

        d = build_s06_parts(final=False)
        split, cpu, spots, vcpus, vps, tl = (d[k] for k in ("split", "cpu", "spots", "vcpus", "vps", "tl"))
        ps = ps0

        # S06.1
        self.say("Here's what the OS does instead.",
                 split.draw(run_time=1.2),
                 cpu0.animate(run_time=1.0).move_to(S06_CPU),
                 *[ps[n].animate(run_time=1.0).move_to(ps[n].copy().shift(spots[n] - ps[n].get_bottom()))
                   for n in "ABC"],
                 LaggedStart(*[FadeIn(v) for v in vcpus], *[FadeIn(vps[n]) for n in "ABC"],
                             lag_ratio=0.1, run_time=1.4),
                 FadeIn(tl.grid, tl.row_labels, run_time=1.0))
        cpu = cpu0

        tick = [0]

        def turn(prev, nxt, rt):
            anims = []
            if prev is not None:
                ps[prev].set_expression("ready")
                anims.append(hop_bottom(ps[prev], spots[prev], run_time=rt))
            ps[nxt].set_expression("running")
            anims.append(hop_seat(ps[nxt], cpu, run_time=rt))
            tick[0] += 1
            t = tick[0]
            col = tl.fill_column(t, {r: ("running" if r == nxt else "ready") for r in "ABC"}, run_time=rt)
            return anims, col

        # S06.2
        anims, col = turn(None, "A", 0.5)
        self.say("It runs process A for a tiny slice of time.",
                 Succession(AnimationGroup(*anims), col),
                 Indicate(vps["A"], scale_factor=1.1, run_time=1.0))

        # S06.3
        anims, col = turn("A", "B", 0.5)
        self.say("Then it stops A and runs B.", Succession(AnimationGroup(*anims), col),
                 Indicate(vps["B"], scale_factor=1.1, run_time=1.0))

        # S06.4
        with self.narrate("Then C. Then back to A."):
            anims, col = turn("B", "C", 0.45)
            self.play(Succession(AnimationGroup(*anims), col), Indicate(vps["C"], scale_factor=1.1, run_time=0.9))
            anims, col = turn("C", "A", 0.45)
            self.play(Succession(AnimationGroup(*anims), col), Indicate(vps["A"], scale_factor=1.1, run_time=0.9))

        # S06.5
        ms = Text("each slice: a few ms", font_size=20, color=DIM).next_to(tl, DOWN, buff=0.08).align_to(tl.grid, LEFT)
        with self.narrate("Each slice lasts only a few milliseconds."):
            self.play(FadeIn(ms), run_time=0.4)
            order = S06_ORDER[4:]
            prev = "A"
            for n in order:
                anims, col = turn(prev, n, 0.22)
                self.play(*anims, col)
                prev = n

        # S06.6
        self.say("To any human, and in a sense to each program, it looks like they're all running at once.",
                 LaggedStart(*[Indicate(vps[n], scale_factor=1.05, color=None) for n in "ABC"],
                             lag_ratio=0.0, run_time=1.2))
        self.beat(1.0)

        # S06.7
        vlabel, plabel = d["vlabel"], d["plabel"]
        titles = VGroup(split.left_title, split.right_title)
        with self.narrate("This is virtualizing the CPU: turning one physical CPU into what looks like many virtual ones."):
            self.play(self.terms.write("virtualizing the CPU"), titles.animate.set_opacity(0), run_time=0.8)
            self.play(FadeIn(vlabel, shift=UP * 0.2), FadeIn(plabel, shift=LEFT * 0.2), run_time=0.8)
            self.wait(0.6)
            self.play(self.terms.dock_anim(), titles.animate.set_opacity(1), run_time=0.8)

        # S06.8
        peach = Peach(radius=0.42).move_to(cpu.die)
        with self.narrate("It's our peach again: snatch it from whoever isn't using it, and hand it to the next eater."):
            self.play(FadeIn(peach, scale=0.5), run_time=0.6)
            self.wait(1.5)
            self.play(FadeOut(peach, scale=0.5), Indicate(cpu, color=CPU_COLOR), run_time=0.8)

        # S06.9
        with self.narrate("The basic technique is called time sharing. One resource is used for a little "
                          "while by one, then by another."):
            self.play(self.terms.write("time sharing"), titles.animate.set_opacity(0), run_time=0.8)
            self.wait(1.0)
            self.play(self.terms.dock_anim(), titles.animate.set_opacity(1), run_time=0.8)
            self.play(LaggedStart(*[Indicate(b, scale_factor=1.2, color=None) for b in tl.blocks_in(None)],
                                  lag_ratio=0.02, run_time=1.5))

        # S06.10
        jug, t = juggler()
        t.add_updater(lambda m, dt: m.increment_value(dt * 0.9))
        with self.narrate("It's like a juggler! Only one ball in the hand at a time, but they're all in the air."):
            self.add(t)
            self.play(stu.thinks(jug, expression="excited", max_width=2.2), run_time=0.9)
            self.wait(2.5)
        self.play(stu.remove_bubble(), stu.change("neutral"), run_time=0.6)
        jug[2].clear_updaters()
        self.remove(t)

        # S06.11
        gauges = d["gauges"]
        a_hl = VGroup(*[SurroundingRectangle(b, buff=0.02, color=COL["A"], stroke_width=3)
                        for b in tl.blocks_in("A") if b.state == "running"])
        a_lab = Text("A gets 1/3 of the time", font_size=22, color=COL["A"])
        a_lab.next_to(tl.grid, DOWN, buff=0.1).align_to(tl.grid, LEFT)
        targets = [g.value_targets(1 / 3, "~33%") for g in gauges]
        with self.narrate("Good picture. But notice the price. If three processes share one CPU, each one runs "
                          "slower than it would alone."):
            self.play(prof.change("explaining"), FadeIn(gauges), FadeOut(ms), run_time=0.8)
            self.wait(0.8)
            self.play(*[Transform(g.bar, bt) for g, (bt, lt) in zip(gauges, targets)],
                      *[Transform(g.label, lt) for g, (bt, lt) in zip(gauges, targets)], run_time=1.2)
            self.play(Create(a_hl), FadeIn(a_lab), run_time=0.8)

        # S06.12
        self.say("Time sharing trades performance for the illusion.", min_time=2.0)
        self.play(FadeOut(a_hl), FadeOut(a_lab), run_time=0.5)
        self.beat(0.5)
