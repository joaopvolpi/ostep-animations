import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


class S05FIFO(Ep07Scene):
    def construct(self):
        self.world(term="turnaround time", stu="curious", prof="explaining")
        stu, prof = self.stu, self.prof
        sp = FIG["fifo"]
        tl = make_gantt(12, 10)
        self.add(tl)
        decor = Chart("fifo")          # only its brackets / markers / readout are used
        ro = decor.ro
        ro.shown = VGroup()            # nothing revealed yet

        # S05.1
        title = policy_title("FIFO")
        fcfs = Text("= FCFS", font_size=22, color=DIM).next_to(title, RIGHT, buff=0.2)
        self.say("The simplest policy imaginable: First In, First Out, FIFO, also called First Come, First Served.",
                 Write(title), self.term("FIFO", hold=0.6), after(2.5, FadeIn(fcfs)))

        # S05.2
        queue = Queue(label=None, center=(4.0, 1.95), slots=3, spacing=0.8)
        qs = [proc(n, scale=0.38) for n in "ABC"]
        queue.place(*qs)
        front = Arrow(P3(2.4, 2.3), P3(2.8, 2.3), buff=0, stroke_width=4, tip_length=0.15, color=TEXT)
        self.say("Whoever arrives first runs first.",
                 FadeIn(queue), *[FadeIn(q, shift=DOWN * 0.2) for q in qs], FadeIn(front))

        # S05.3
        simple = VGroup(tick_mark(0.28), Text("simple", font_size=22, color=PERS)).arrange(RIGHT, buff=0.12)
        simple.next_to(title, LEFT, buff=0.9)
        self.say("It's simple, so it's easy to build, and with our assumptions it works pretty well.",
                 FadeIn(simple, shift=RIGHT * 0.2))

        # S05.4
        arrows = [tl.arrival_marker(r, 0, dx=0.1 * k) for k, r in enumerate("ABC")]
        self.say("Three jobs, A, B and C. They all arrive together, but A arrived a hair before B, "
                 "and B a hair before C.",
                 LaggedStart(*[FadeIn(a, shift=DOWN * 0.2) for a in arrows], lag_ratio=0.6, run_time=2.5))

        # S05.5
        ten = tl.bracket("A", 0, 1, "10 s").shift(UP * 0.4)
        self.say("Each needs ten seconds.", Create(ten.line), FadeIn(ten.caps), FadeIn(ten.label))
        self.play(FadeOut(ten), run_time=0.4)

        # S05.6 - S05.8
        spot = Spotlight(height=0.9, spread=0.35)
        spot.move_beam_to(queue.slot_point(0) + DOWN * 0.12)
        self.add(spot)
        names = "ABC"
        lines = ["A finishes at ten.", "B at twenty.", "C at thirty."]
        for k in range(3):
            j = names[k]
            anims = cell_anims(tl, sp["run"], {}, k + 1)
            anims += [FadeIn(decor.mk[j], shift=DOWN * 0.4), Create(decor.br[j].line), FadeIn(decor.br[j].caps),
                      FadeIn(decor.br[j].label), *ro.reveal_term(k)]
            if k == 0:
                anims.append(FadeIn(spot))
            else:
                anims.append(spot.animate.move_beam_to(queue.slot_point(k) + DOWN * 0.12))
                anims.append(qs[k - 1].animate.set_opacity(0.3))
            self.say(lines[k], *anims, min_time=2.0)

        # S05.9
        self.say("Average turnaround time: ten plus twenty plus thirty, over three. Twenty seconds.",
                 *ro.reveal_value(run_time=1.2),
                 Succession(*[Indicate(decor.br[j], scale_factor=1.1, run_time=0.8) for j in "ABC"]),
                 stu.change("curious"))
        self.play(*ro.frame_value(True))
        self.beat(0.8)
        self.play(FadeOut(VGroup(spot, queue, front, *qs, simple, fcfs)), run_time=0.6)
