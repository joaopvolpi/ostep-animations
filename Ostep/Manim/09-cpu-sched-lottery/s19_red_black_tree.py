import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403

VALS = [1, 5, 9, 10, 14, 17, 18, 21, 22, 24]


def list_node(v, x, y):
    c = Circle(radius=0.22).set_fill("#3A3A3A", 1).set_stroke(TEXT, 2)
    t = Text(str(v), font_size=16, color=TEXT, font=MONO_FONT).move_to(c)
    return VGroup(c, t).move_to(P3(x, y))


class S19RedBlackTree(Ep09Scene):
    def construct(self):
        self.world(stu="neutral", prof="neutral")
        stu, prof = self.stu, self.prof
        LY = 1.6
        xs = [-6.0 + 0.58 * i for i in range(10)]
        nodes = [list_node(v, x, LY) for v, x in zip(VALS, xs)]
        cpu = CPU(size=0.7, label="CPU").move_to(P3(-3.4, -0.4))

        # S19.1
        proc_ct = Text("processes: 1000s", font_size=22, color=TEXT).move_to(P3(0.0, 2.2))
        clk = ClockIcon(0.22, color=CPU_COLOR).move_to(P3(-1.7, 2.2))
        self.say("One more efficiency problem. 'Pick the lowest vruntime' sounds easy, but servers run thousands of "
                 "processes, and the choice happens every few milliseconds.",
                 FadeIn(proc_ct), FadeIn(clk), FadeIn(cpu),
                 Succession(clk.spin(2, run_time=3.0), clk.spin(4, run_time=3.0)))
        self.play(FadeOut(proc_ct), FadeOut(clk), run_time=0.4)

        # S19.2
        spot = Spotlight(height=0.7, spread=0.3)
        spot.move_beam_to(P3(xs[0], LY - 0.3))
        steps_l = Text("steps: 0", font_size=22, color=TEXT, font=MONO_FONT).move_to(P3(-3.4, -1.4))
        self.say("Keep a sorted list. The lowest is at the front.",
                 stu.change("curious"), LaggedStart(*[FadeIn(n, scale=0.6) for n in nodes], lag_ratio=0.1, run_time=1.8),
                 Succession(Wait(1.8), FadeIn(spot)), FadeIn(steps_l))

        # S19.3
        steps_1 = Text("steps: 1", font_size=22, color=TEXT, font=MONO_FONT).move_to(steps_l)
        first = nodes[0]
        self.say("Taking the first is quick.", FadeOut(spot),
                 glide(first, cpu.get_top() + UP * 0.25, 1.0), Transform(steps_l, steps_1))

        # S19.4
        newv = list_node(20, xs[0], LY)
        newv[0].set_stroke(CPU_COLOR, 3)
        ptr = Arrow(P3(xs[1], LY + 0.8), P3(xs[1], LY + 0.3), buff=0, color=CPU_COLOR, stroke_width=4,
                    max_tip_length_to_length_ratio=0.35)
        self.say("But after it runs, its vruntime grows, and it must be re-inserted in order.",
                 Transform(first, newv), FadeIn(ptr))
        with self.narrate(""):
            for k in range(2, 9):
                xi = xs[min(k, 9) - 0] if False else xs[k - 1 + 1 if k - 1 + 1 < 10 else 9]
                self.play(glide(ptr, P3(xs[k] if k < 10 else xs[9], LY + 0.55), 0.3),
                          Transform(steps_l, Text(f"steps: {k}", font_size=22, color=TEXT, font=MONO_FONT).move_to(steps_l)),
                          run_time=0.35)
        self.play(Transform(steps_l, Text("steps: 8", font_size=22, color=TEXT, font=MONO_FONT).move_to(steps_l)),
                  glide(first, P3((xs[6] + xs[7]) / 2, LY - 0.55), 0.6), run_time=0.7)

        # S19.5
        on = Text("O(n)", font_size=30, color=KERNEL_COLOR).move_to(P3(-3.4, 0.6))
        self.say("With vruntimes one, five, nine, ten, fourteen, eighteen, seventeen, twenty-one, twenty-two and "
                 "twenty-four, that means scanning the list: linear time.",
                 FadeOut(ptr), Succession(*[Indicate(n, color=CPU_COLOR, scale_factor=1.3, run_time=0.8) for n in nodes[1:]]),
                 Succession(Wait(6.0), FadeIn(on)))

        # S19.6
        tick = Text("1000 nodes → 1000 steps", font_size=22, color=KERNEL_COLOR).move_to(P3(-3.4, -0.2))
        flag = Polygon(P3(0, 0.3), P3(0.3, 0.2), P3(0, 0.1)).set_fill(KERNEL_COLOR, 1).set_stroke(width=0)
        self.say("Terrible at a thousand processes.", FadeOut(cpu), FadeIn(tick), FadeIn(flag.next_to(tick, LEFT, buff=0.1)))
        self.play(FadeOut(VGroup(tick, flag, on)), run_time=0.4)

        # S19.7
        tree = RBTree(at=(3.2, 1.3), dx=0.5, dy=0.62, radius=0.21)
        nxt = Text("next to run", font_size=18, color=CPU_COLOR).next_to(tree.node(1), LEFT, buff=0.12)
        self.say("CFS uses a red-black tree, ordered by vruntime.",
                 self.term("red-black tree"), Create(tree.edges), FadeIn(tree.stubs),
                 LaggedStart(*[FadeIn(tree.node(v), scale=0.6) for v in (14, 9, 18, 1, 10, 17, 22, 5, 21, 24)],
                             lag_ratio=0.2, run_time=3.0))
        self.play(tree.highlight_min(), FadeIn(nxt), run_time=0.8)

        # S19.8
        path = tree.insert_path(20)
        steps_t = Text("steps: 0", font_size=22, color=TEXT, font=MONO_FONT).move_to(P3(3.2, -1.1))
        tptr = Dot(radius=0.1, color=CPU_COLOR).move_to(tree.pos[path[0]] + UP * 0.45)
        olog = Text("O(log n)", font_size=30, color=PERS).move_to(P3(3.2, -1.7))
        self.add(steps_t)
        steps_t.set_opacity(0)
        self.say("It's balanced: it does a little extra work on each insert to stay shallow, so find, insert and delete "
                 "are all logarithmic.",
                 FadeOut(nxt), steps_t.animate.set_opacity(1), FadeIn(tptr))
        with self.narrate(""):
            for i, v in enumerate(path, 1):
                self.play(glide(tptr, tree.pos[v] + UP * 0.45, 0.6),
                          Transform(steps_t, Text(f"steps: {i}", font_size=22, color=TEXT, font=MONO_FONT).move_to(steps_t)),
                          run_time=0.7)
            self.play(Indicate(tree.node(22), color=CPU_COLOR), FadeIn(olog), FadeOut(tptr), run_time=0.8)

        # S19.9
        sleep_tag = Text("sleeping", font_size=18, color=DIM)
        sl = tree.node(10)
        sclk = mini_clock(0.12)
        self.say("And only runnable processes live in the tree. A sleeper is removed.",
                 glide(sl, P3(6.0, 0.4), 1.2), Succession(Wait(1.3), AnimationGroup(FadeIn(sleep_tag.next_to(P3(6.0, 0.4), DOWN, buff=0.3)),
                                                                                    FadeIn(sclk.move_to(P3(6.0, 0.9))))))

        # S19.10
        tip = VGroup(card_rect(6.6, 0.55, DIM), Text("TIP: use efficient data structures when appropriate", font_size=20, color=TEXT))
        tip[1].move_to(tip[0])
        tip.move_to(P3(0, -2.55))
        self.say("Knowing which data structure fits is a hallmark of good engineering. A list was fine once. At this "
                 "scale, it isn't.",
                 prof.change("explaining"), FadeIn(tip, shift=UP * 0.2))
        self.beat(0.8)
