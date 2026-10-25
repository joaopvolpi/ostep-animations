import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


def crown(size=0.3):
    pts = [[-1, -0.6, 0], [-1, 0.5, 0], [-0.5, 0, 0], [0, 0.7, 0], [0.5, 0, 0], [1, 0.5, 0], [1, -0.6, 0]]
    return Polygon(*[np.array(p) * size for p in pts]).set_fill(CPU_COLOR, 1).set_stroke(outline_of(CPU_COLOR), 2)


class S07SJF(Ep07Scene):
    def construct(self):
        self.world(opened=(0,), term="convoy effect", stu="excited", prof="happy")
        stu, prof, strip = self.stu, self.prof, self.strip
        cv = Chart("convoy")
        bars = bars_labelled()
        title = policy_title("FIFO")
        self.add(cv.group(), bars, title)
        tl = cv.tl
        for j in "BC":   # S06 ends with B and C's waiting cells outlined in red
            for t in range(1, 11):
                if (tl.row_index(j), t) in tl.block_at:
                    tl.block_at[(tl.row_index(j), t)].set_stroke(KERNEL_COLOR, 3.5)
        sj = Chart("sjf")
        ro = sj.ro
        ro.shown = VGroup()

        # S07.1
        self.say("That's exactly the next policy. Shortest Job First, SJF.",
                 Transform(title, policy_title("SJF")), self.term("SJF", hold=0.6), stu.change("neutral"))

        # S07.2
        spot = Spotlight(height=0.7, spread=0.3)
        spot.move_beam_to(bars[1].get_center() + DOWN * 0.3)
        order = [(1, "1st"), (2, "2nd"), (0, "3rd")]
        tags = VGroup(*[Text(t, font_size=20, color=DIM).next_to(bars[i], DOWN, buff=0.4) for i, t in order])
        sweep = []
        for k, (i, _) in enumerate(order):
            tgt = bars[i].get_center() + DOWN * 0.3
            if i == 0:
                tgt = P3(-3.0, tgt[1])
            sweep.append(spot.animate(run_time=0.8).move_beam_to(tgt))
        self.say("Run the shortest job first, then the next shortest, and so on.",
                 FadeIn(spot),
                 after(0.5, *[Succession(s, FadeIn(tags[k], run_time=0.3)) for k, s in enumerate(sweep)]))
        self.play(FadeOut(spot), FadeOut(tags), run_time=0.4)

        # S07.3
        anims = reshuffle(tl, cv.sp["run"], {}, sj.sp["run"], {}, run_time=1.4)
        for j in "ABC":
            anims.append(Transform(cv.mk[j], sj.mk[j], run_time=1.4))
            anims.append(Transform(cv.br[j], sj.br[j], run_time=1.4))
        self.say("Same three jobs. B finishes at ten. C at twenty. A at a hundred and twenty.", *anims)
        tl.purge()

        # S07.4
        with self.narrate("Average turnaround: fifty seconds."):
            self.play(FadeOut(cv.ro.shown), *ro.reveal_numerator(), run_time=1.0)
            self.play(Write(ro.eq), run_time=0.5)
            ro.shown.add(ro.eq)
            self.play(*strike_below(self, ro, "110"))
            self.play(ro.count_value(110, run_time=1.4))
            self.play(*ro.frame_value(True))

        # S07.5
        br = Brace(VGroup(ro.old_mob, ro.value_mob), RIGHT, color=PERS, buff=0.2)
        bt = Text("× 2.2 better", font_size=26, color=PERS).next_to(br, RIGHT, buff=0.15)
        self.say("Same jobs, same work, and we cut the average by more than half just by changing the order.",
                 FadeIn(br), FadeIn(bt, shift=LEFT * 0.2))

        # S07.6
        tag = VGroup(crown(0.18), Text("optimal", font_size=24, color=PERS)).arrange(RIGHT, buff=0.1).move_to(P3(1.7, 3.1))
        note = Text("assuming all arrive together", font_size=18, color=DIM).next_to(tag, RIGHT, buff=0.2)
        self.say("And if all jobs arrive together, SJF is provably optimal.",
                 prof.change("explaining"), FadeIn(tag, scale=1.3), FadeIn(note))

        # S07.7
        proof = proof_sheet(0.6).move_to(P3(-2.6, 3.05))
        xm = x_mark(0.4).move_to(proof)
        self.say("We're in a systems class, so we'll skip the proof.",
                 stu.change("bored"), FadeIn(proof), after(1.2, Create(xm)))

        # S07.8
        sign = VGroup(RoundedRectangle(width=3.2, height=0.5, corner_radius=0.08).set_fill("#2E6BC4", 1).set_stroke(TEXT, 2),
                      Text("10 ITEMS OR LESS", font_size=22, color=TEXT, weight=BOLD))
        sign[1].move_to(sign[0])
        mint, coral = proc("B", scale=0.3, label=None), proc("A", scale=0.3, label=None)
        lane = VGroup(mint, coral).arrange(LEFT, buff=0.6)
        head = Text("The principle of SJF", font_size=24, color=TEXT)
        body = VGroup(head, sign, lane).arrange(DOWN, buff=0.25)
        card = TipCard(body, title="TIP", width=4.8, height=3.7).move_to(P3(4.0, 0.1))
        # the chart leaves while the tip card is up (it would sit under the card), and comes back after
        ro.shown.remove(ro.old_mob, ro.old_strike)
        stage = VGroup(tl, *cv.mk.values(), *cv.br.values(), ro.shown)
        self.say("But the supermarket got there first: that's the 'ten items or less' lane.",
                 card.slide_in(RIGHT), FadeOut(stage),
                 FadeOut(VGroup(br, bt, ro.old_mob, ro.old_strike, tag, note)), after(2.0, mint.animate(run_time=1.0).shift(RIGHT * 0.45)))

        # S07.9
        self.beat(1.0)
        self.play(card.slide_out(RIGHT), FadeOut(VGroup(proof, xm)), FadeIn(stage),
                  stu.change("neutral"), prof.change("happy"), run_time=0.7)
