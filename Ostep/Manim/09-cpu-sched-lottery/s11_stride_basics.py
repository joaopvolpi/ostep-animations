import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403

LANE_Y = {"A": 1.2, "B": 0.2, "C": -0.8}
STRIDE = {"A": 100, "B": 200, "C": 40}
TIX = {"A": 100, "B": 50, "C": 250}


def make_lanes(x0=-5.2, scale=0.04):
    lanes = {n: PassLane(n, COL[n], STRIDE[n], LANE_Y[n], x0=x0, scale=scale, length=260) for n in "ABC"}
    procs = {n: proc(n, scale=0.5).move_to(P3(x0 - 0.75, LANE_Y[n] - 0.1)) for n in "ABC"}
    return lanes, procs


class S11StrideBasics(Ep09Scene):
    def construct(self):
        self.world(stu="neutral", prof="neutral")
        stu, prof = self.stu, self.prof

        # S11.1
        drum = RaffleDrum(1.2).move_to(P3(4.2, 0.0))
        cloud = bad_luck_cloud("4 / 20", 1.5).move_to(P3(4.2, 1.9))
        self.add(drum)
        drum.set_opacity(0)
        self.say("Why use randomness at all, then? Can't we get the proportions exactly right?",
                 stu.change("frustrated"), drum.animate.set_opacity(1),
                 Succession(Wait(1.0), Rotate(drum, angle=0.2, run_time=0.3), Rotate(drum, angle=-0.4, run_time=0.3),
                            Rotate(drum, angle=0.2, run_time=0.3), FadeIn(cloud, shift=DOWN * 0.2)))

        # S11.2
        lanes, procs = make_lanes()
        axis = Line(P3(-5.2, 2.15), P3(-5.2 + 260 * 0.04, 2.15)).set_stroke(DIM, 2)
        ax_labels = VGroup(*[Text(str(v), font_size=18, color=DIM).move_to(P3(-5.2 + v * 0.04, 1.9)) for v in (0, 100, 200)])
        self.say("Waldspurger asked the same question. His answer is stride scheduling: a deterministic fair-share scheduler.",
                 FadeOut(cloud), drum.animate(run_time=2.0).shift(RIGHT * 4), self.term("stride scheduling"),
                 FadeIn(axis), FadeIn(ax_labels),
                 *[FadeIn(lanes[n]) for n in "ABC"], *[FadeIn(procs[n]) for n in "ABC"])
        self.remove(drum)

        # S11.3
        cap = MathTex(r"\text{stride}\ \propto\ \frac{1}{\text{tickets}}", font_size=34, color=TEXT).move_to(P3(0, -1.9))
        self.say("Each job gets a stride, which is inversely proportional to its tickets.",
                 self.term("stride"), FadeIn(cap), stu.change("neutral"))

        # S11.4
        stacks = {n: TicketStack(TIX[n], COL[n], scale=0.7).move_to(P3(-3.6, LANE_Y[n] + 0.3)) for n in "ABC"}
        self.say("Take our three jobs: a hundred, fifty and two hundred and fifty tickets.",
                 *[FadeIn(stacks[n], shift=DOWN * 0.1) for n in "ABC"])

        # S11.5
        eqs = {n: MathTex(rf"\frac{{10000}}{{{TIX[n]}}}={STRIDE[n]}", font_size=28, color=COL[n]).move_to(P3(4.7, LANE_Y[n] + 0.25))
               for n in "ABC"}
        self.say("Divide ten thousand by each. A has a stride of one hundred. B, two hundred. C, forty.",
                 FadeOut(cap),
                 Succession(*[AnimationGroup(Write(eqs[n]), Succession(Wait(0.8), GrowFromEdge(lanes[n].stride_bar, LEFT)))
                              for n in "ABC"]))

        # S11.6
        pass_cap = Text("pass = 0 for everyone", font_size=24, color=TEXT).move_to(P3(0, -1.9))
        self.say("Each job also keeps a pass value, starting at zero.",
                 self.term("pass"), FadeIn(pass_cap), FadeOut(VGroup(*eqs.values())),
                 *[Indicate(lanes[n].flag, color=COL[n], scale_factor=1.4) for n in "ABC"])

        # S11.7
        spot = Spotlight(height=0.9, spread=0.35)
        spot.move_beam_to(P3(-5.2, LANE_Y["A"] + 0.0))
        rule = VGroup(Text("1. run the lowest pass", font_size=26, color=TEXT),
                      Text("2. pass += stride", font_size=26, color=TEXT)).arrange(RIGHT, buff=0.7).move_to(P3(0, -2.5))
        self.say("The rule is simple: run the job with the lowest pass. Then add its stride to its pass.",
                 FadeOut(pass_cap), FadeIn(spot), FadeIn(rule),
                 Succession(Wait(1.0), *[spot.animate(run_time=0.7).move_beam_to(P3(-5.2, LANE_Y[n])) for n in "BCA"]))
        self.beat(0.8)
