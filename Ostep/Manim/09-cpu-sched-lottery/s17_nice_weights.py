import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403

ROWS = [("-5", "3121"), ("-4", "2501"), ("-3", "1991"), ("...", "..."), ("0", "1024")]


def make_table():
    g = VGroup()
    hdr = VGroup(mono("nice", 18, DIM).move_to(P3(-0.6, 0)), mono("weight", 18, DIM).move_to(P3(0.7, 0)))
    g.add(hdr)
    rows = []
    for k, (x, w) in enumerate(ROWS):
        r = VGroup(mono(x, 20).move_to(P3(-0.6, -0.42 - 0.36 * k)), mono(w, 20).move_to(P3(0.7, -0.42 - 0.36 * k)))
        rows.append(r)
        g.add(r)
    g.rows = rows
    return g


class S17NiceWeights(Ep09Scene):
    def construct(self):
        self.world(stu="neutral", prof="neutral")
        stu = self.stu
        a = proc("A", scale=0.5).move_to(P3(-1.0, 0.75))
        b = proc("B", scale=0.5).move_to(P3(0.4, 0.75))

        # S17.1
        st = TicketStack(100, COL["A"], scale=0.8).next_to(a, UP, buff=0.15)
        cross = x_mark(0.35).move_to(st)
        notix = Text("no tickets in CFS", font_size=20, color=DIM).move_to(P3(1.4, 1.5), aligned_edge=LEFT)
        self.say("Can I tell CFS that one program matters more? With tickets, I can.",
                 stu.change("curious"), FadeIn(a),
                 Succession(Wait(1.0), FadeIn(st, scale=1.3), Wait(1.5), FadeIn(cross), FadeIn(notix)))

        # S17.2
        line = Line(P3(-6.2, 1.5), P3(-2.8, 1.5)).set_stroke(TEXT, 3)
        knob = Dot(radius=0.13, color=VIRT).move_to(P3(-6.2 + 3.4 * 20 / 39, 1.5))
        lab = VGroup(*[Text(t, font_size=18, color=DIM).move_to(P3(-6.2 + 3.4 * (v + 20) / 39, 1.15))
                       for t, v in (("-20", -20), ("0", 0), ("19", 19))])
        self.say("CFS doesn't use tickets. It uses an old UNIX mechanism called nice: a value from minus twenty to plus "
                 "nineteen, default zero.",
                 FadeOut(st), FadeOut(cross), FadeOut(notix), self.term("nice"),
                 Succession(Wait(1.5), Create(line), FadeIn(lab), FadeIn(knob)))

        # S17.3
        less = Text("less CPU", font_size=18, color=DIM).move_to(P3(-3.4, 0.7))
        more = Text("more CPU", font_size=18, color=DIM).move_to(P3(-5.6, 0.7))
        xr, xl = knob.get_center()[0], knob.get_center()[0]
        self.say("Positive means nicer, so you get less. Negative means higher priority.",
                 FadeIn(less), FadeIn(more),
                 Succession(glide(knob, P3(-3.4, 1.5), 1.2), glide(knob, P3(-5.6, 1.5), 1.6),
                            glide(knob, P3(-6.2 + 3.4 * 20 / 39, 1.5), 0.8)))

        # S17.4
        table = make_table().move_to(P3(4.5, 1.1))
        self.say("CFS maps each nice value to a weight with a lookup table.",
                 self.term("weight"), FadeOut(VGroup(less, more)), FadeIn(table))

        # S17.5
        h5 = SurroundingRectangle(table.rows[4], color=CPU_COLOR, buff=0.08)
        hm = SurroundingRectangle(table.rows[0], color=CPU_COLOR, buff=0.08)
        self.say("Nice zero is one thousand twenty-four. Nice minus five is three thousand one hundred twenty-one.",
                 Succession(Create(h5), Wait(1.5), FadeOut(h5), Create(hm)))
        self.play(FadeOut(hm), run_time=0.3)

        # S17.6
        eq = MathTex(r"\text{time\_slice}_k = \frac{\text{weight}_k}{\sum_i \text{weight}_i}\cdot \text{sched\_latency}",
                     font_size=32, color=TEXT).move_to(P3(0, -0.85))
        self.say("A process's time slice is its weight over the sum of all weights, times sched_latency.", Write(eq, run_time=3.0))

        # S17.7
        ta = token("nice -5", COL["A"], size=18).next_to(a, DOWN, buff=0.1)
        tb = token("nice 0", COL["B"], size=18).next_to(b, DOWN, buff=0.1)
        self.say("Try it. A has nice minus five, B has nice zero.", FadeIn(b), FadeIn(ta), FadeIn(tb))

        # S17.8
        eq2 = MathTex(r"\tfrac{3121}{3121+1024}\approx\tfrac34 \;\Rightarrow\; 36\ \text{ms}\qquad"
                      r"\tfrac14 \;\Rightarrow\; 12\ \text{ms}", font_size=30, color=TEXT).move_to(P3(0, -1.55))
        ba = Rectangle(width=6.0, height=0.4).set_fill(COL["A"], 1).set_stroke(TEXT, 1)
        bb = Rectangle(width=2.0, height=0.4).set_fill(COL["B"], 1).set_stroke(TEXT, 1)
        bars = VGroup(ba, bb).arrange(RIGHT, buff=0).move_to(P3(0, -2.25))
        la = Text("A: 36 ms", font_size=20, color=INK_DARK).move_to(ba)
        lb = Text("B: 12 ms", font_size=18, color=INK_DARK).move_to(bb)
        self.say("A gets about three quarters of forty-eight: thirty-six milliseconds. B gets twelve.",
                 Transform(eq, eq2), Succession(Wait(1.5), GrowFromEdge(ba, LEFT), GrowFromEdge(bb, LEFT), FadeIn(la), FadeIn(lb)))
        self.beat(0.8)
