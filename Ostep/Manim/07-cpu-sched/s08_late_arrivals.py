import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


class S08LateArrivals(Ep07Scene):
    def construct(self):
        self.world(opened=(0,), term="SJF", stu="neutral", prof="happy")
        stu, prof, strip = self.stu, self.prof, self.strip
        sj = Chart("sjf")
        bars = bars_labelled()
        title = policy_title("SJF")
        self.add(sj.group(), bars, title)
        tl = sj.tl
        late = Chart("late")
        run, arr = late.sp["run"], late.sp["arrive"]
        ro = late.ro
        ro.shown = VGroup()
        sp = late.sp
        formula = turn_brackets(tl, sp, labels={"A": "100", "B": "110 − 10", "C": "120 − 10"})

        # S08.1
        old = VGroup(*sj.br.values(), *sj.mk.values(), sj.ro.shown)
        self.say("Right. The second assumption goes next.",
                 stu.change("curious"), strip.locks[1].open(), tl.clear_blocks(0.9), FadeOut(old))
        tl.purge()

        # S08.2
        a_arr = tl.arrival_marker("A", 0, "arrives", dx=0.05)
        self.say("Now A arrives at time zero and needs a hundred seconds.",
                 FadeIn(a_arr, shift=DOWN * 0.2), Indicate(bars[0], scale_factor=1.05))

        # S08.3
        b_arr = tl.arrival_marker("B", 1, "[B, C arrive]", label_side=LEFT)
        c_arr = tl.arrival_marker("C", 1)
        self.say("B and C arrive at time ten, and each needs ten.",
                 FadeIn(b_arr, shift=DOWN * 0.2), FadeIn(c_arr, shift=DOWN * 0.2),
                 Indicate(bars[1], scale_factor=1.2), Indicate(bars[2], scale_factor=1.2))

        # S08.4
        self.say("SJF starts A, the only job it has.", *cell_anims(tl, run, arr, 1, run_time=0.8))

        # S08.5
        stop = Line(P3(GX[0] + 2 * CELL10, tl.row_y("A") + 0.2), P3(GX[0] + 2 * CELL10, tl.row_y("A") - 0.2))
        stop.set_stroke(KERNEL_COLOR, 6)
        nolab = Text("no interrupt", font_size=20, color=KERNEL_COLOR).next_to(stop, UP, buff=0.55).shift(RIGHT * 0.5)
        self.say("When B and C show up, A is already running, and SJF never interrupts.",
                 *cell_anims(tl, run, arr, 2, run_time=0.8),
                 after(1.0, AnimationGroup(Create(stop), FadeIn(nolab)),
                            Indicate(tl.blocks_in("A"), scale_factor=1.05, run_time=1.0)))

        # S08.6
        with self.narrate("So they wait until A finishes at a hundred."):
            for t in range(3, 11):
                self.play(*cell_anims(tl, run, arr, t, run_time=0.2), run_time=0.2)
            self.play(FadeOut(VGroup(stop, nolab)), run_time=0.4)

        # S08.7
        anims = []
        for t in (11, 12):
            anims += cell_anims(tl, run, arr, t, run_time=0.5)
        anims += [FadeIn(m, shift=DOWN * 0.4) for m in late.mk.values()]
        self.say("B finishes at a hundred and ten, and C at a hundred and twenty.", *anims)

        # S08.8
        anims = []
        for j in "ABC":
            b = formula[j]
            anims += [Create(b.line), FadeIn(b.caps), FadeIn(b.label)]
        self.say("But their turnaround counts from their arrival at ten.", *anims,
                 after(1.0, Indicate(VGroup(b_arr.arrow, c_arr.arrow), scale_factor=1.6)))

        # S08.9
        self.say("So that's a hundred, a hundred, and a hundred and ten.",
                 *[Transform(formula[j], late.br[j]) for j in "ABC"])

        # S08.10
        self.say("Average: a hundred and three point three three seconds. The convoy is back.",
                 *ro.reveal_numerator(run_time=1.4))
        self.play(*ro.reveal_value(), run_time=0.8)
        self.play(*ro.frame_value(False), run_time=0.6)

        # S08.11
        self.say("The problem is that SJF is non-preemptive: it runs each job to completion before it even "
                 "considers another.",
                 prof.change("worried"), self.term("non-preemptive", hold=0.8))
