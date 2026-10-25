import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


class S20Sleeper(Ep09Scene):
    def construct(self):
        self.world(stu="curious", prof="explaining")
        stu = self.stu
        mA = VruntimeMeter(COL["A"], height=2.0, width=0.5, max_value=20.0).move_to(P3(-2.4, -0.2))
        mB = VruntimeMeter(COL["B"], height=2.0, width=0.5, max_value=20.0).move_to(P3(2.4, -0.2))
        a = proc("A", scale=0.5).next_to(mA, DOWN, buff=0.1)
        b = proc("B", scale=0.5).next_to(mB, DOWN, buff=0.1)
        cpu = CPU(size=0.8, label="CPU").move_to(P3(0, 1.3))
        clock = ClockIcon(0.4, color=TEXT).move_to(P3(0, -1.1))
        ruler = Line(P3(-3.0, -2.55), P3(3.0, -2.55)).set_stroke(DIM, 2)
        r0 = Text("0 s", font_size=18, color=DIM).next_to(ruler.get_start(), DOWN, buff=0.08)
        r10 = Text("10 s", font_size=18, color=DIM).next_to(ruler.get_end(), DOWN, buff=0.08)
        prog = Line(P3(-3.0, -2.55), P3(-2.99, -2.55)).set_stroke(CPU_COLOR, 5)

        self.play(*[FadeIn(x) for x in (mA, mB, a, b, cpu, clock, ruler, r0, r10)], run_time=0.7)

        # S20.1
        self.say("One last trap. A runs all the time.",
                 hop_to(a, cpu.slot_point(), run_time=0.8), mA.set_level(0.3, run_time=3.0))

        # S20.2
        zz = zz_glyph(0.3).next_to(b, UP, buff=0.0)
        def grow(m, al):
            m.put_start_and_end_on(P3(-3.0, -2.55), P3(-3.0 + 6.0 * max(al, 0.002), -2.55))
        self.add(prog)
        self.say("B sleeps for ten seconds.", b.change("blocked"), FadeIn(zz),
                 UpdateFromAlphaFunc(prog, grow, run_time=3.0, rate_func=linear),
                 Succession(Wait(0.5), mA.set_level(0.9, run_time=2.5)))

        # S20.3
        gap = mA.gap_to(mB, label="10 s")
        self.say("When B wakes, its vruntime is ten seconds behind A's.",
                 b.change("ready"), FadeOut(zz), FadeIn(gap))

        # S20.4
        starve = Text("starved", font_size=22, color=KERNEL_COLOR).move_to(mA.get_bottom() + DOWN * 0.4)
        longbar = Rectangle(width=5.0, height=0.3).set_fill(COL["B"], 1).set_stroke(TEXT, 1).move_to(P3(0, -2.3))
        lb = Text("B runs 10 s in a row", font_size=18, color=INK_DARK).move_to(longbar)
        self.say("So B hogs the CPU for ten seconds while A starves!",
                 stu.change("surprised"), FadeOut(gap),
                 Succession(Wait(0.5), GrowFromEdge(longbar, LEFT), FadeIn(lb), FadeIn(starve)))
        self.play(FadeOut(VGroup(longbar, lb, starve)), stu.change("neutral"), run_time=0.7)

        # S20.5
        tree_icon = VGroup(Circle(radius=0.15).set_fill(RBTree.BLK, 1).set_stroke(TEXT, 2),
                           Circle(radius=0.12).set_fill(RBTree.RED, 1).set_stroke(TEXT, 2).shift(DL * 0.35),
                           Circle(radius=0.12).set_fill(RBTree.RED, 1).set_stroke(TEXT, 2).shift(DR * 0.35))
        tmin = Text("min", font_size=20, color=CPU_COLOR).next_to(tree_icon, DOWN, buff=0.1)
        tg = VGroup(tree_icon, tmin).move_to(P3(5.6, 2.0))
        self.say("It would. So when a job wakes, CFS sets its vruntime to the minimum in the tree.",
                 mB.set_level(0.9, run_time=1.2), FadeIn(tg),
                 Succession(Wait(1.5), Indicate(mB, color=CPU_COLOR)))

        # S20.6
        tl = Timeline(["CPU"], ticks=8, x_range=(-1.6, 1.6), top=-1.9, row_height=0.32, row_kinds=["cpu"],
                      tick_labels=False, label_font=16)
        tagb = Text("frequent short sleeps → lose their share", font_size=20, color=DIM).move_to(P3(3.3, -1.2))
        zz2 = zz_glyph(0.3).next_to(b, RIGHT, buff=0.1)
        self.say("No monopoly. The price: jobs that sleep for short periods, again and again, never get their fair share.",
                 FadeOut(VGroup(ruler, r0, r10, prog)), FadeIn(tl), FadeIn(tagb), FadeIn(zz2),
                 Succession(Wait(0.5), *[tl.fill("CPU", t, "running", color=COL["AB"[t % 2]], run_time=0.25) for t in range(1, 9)]))
        self.beat(0.6)
        self.fade_stage()
