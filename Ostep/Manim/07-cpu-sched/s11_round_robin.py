import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


class S11RoundRobin(Ep07Scene):
    def construct(self):
        self.world(opened=(0, 1, 2, 3)[:3], term="response time", stu="sad", prof="explaining")
        stu, prof = self.stu, self.prof
        sj = Chart("sjf5", brackets="resp", markers=False)
        title = policy_title("SJF")
        sb1 = scoreboard_at([("SJF · STCF", True, False)], y=2.5)
        self.add(sj.group(), title, sb1)
        tl = sj.tl
        rr = Chart("rr", brackets="resp", markers=False)
        run = rr.sp["run"]
        ro = rr.ro
        ro.shown = VGroup()
        sb2 = scoreboard_at([("SJF · STCF", True, False), ("RR", None, True)])
        clk = ClockIcon(0.3, color=CPU_COLOR).move_to(CLOCK_AT)
        clklab = Text("1 s", font_size=24, color=CPU_COLOR).next_to(clk, RIGHT, buff=0.12)

        # S11.1
        self.say("Here's the idea. Instead of running jobs to completion, run one for a short time slice…",
                 Transform(title, policy_title("RR")), self.term("time slice", hold=0.8),
                 Succession(Wait(2.0), AnimationGroup(FadeIn(clk, scale=1.3), FadeIn(clklab), clk.spin(1, run_time=1.5))),
                 stu.change("curious"))

        # S11.2
        alias = Text("= scheduling quantum", font_size=20, color=DIM).next_to(title, RIGHT, buff=0.2)
        self.say("…(the book also calls it a scheduling quantum)…", FadeIn(alias, shift=LEFT * 0.2))

        # S11.3
        queue = Queue(label="Run queue", center=(3.6, 2.2), slots=3, spacing=0.8, font_size=18)
        ps = [proc(n, scale=0.38) for n in "ABC"]
        queue.place(*ps)
        spot = Spotlight(height=0.8, spread=0.3)
        spot.move_beam_to(queue.slot_point(0))
        loop = loop_arrow(0.28, color=TEXT).move_to(P3(5.35, 2.4))
        sweep = Succession(*[spot.animate(run_time=0.7).move_beam_to(queue.slot_point(k % 3)) for k in (1, 2, 0)])
        self.say("…then switch to the next job in the queue, and the next, round and round until every job is done. "
                 "This is Round Robin.",
                 FadeIn(queue), *[FadeIn(p, shift=DOWN * 0.2) for p in ps], FadeIn(spot),
                 Succession(Wait(1.5), sweep, FadeIn(loop)), self.term("Round Robin", hold=0.8))

        # S11.4
        old = VGroup(*sj.br.values(), sj.ro.shown, spot, loop)
        self.play(tl.clear_blocks(0.8), FadeOut(old), run_time=0.8)
        tl.purge()
        with self.narrate("Same three five-second jobs, with a one-second slice. A, B, C, A, B, C."):
            for t in range(1, 16):
                rt = 0.45 if t <= 6 else 0.18
                self.play(*cell_anims(tl, run, {}, t, run_time=rt), run_time=rt)

        # S11.5
        anims = []
        for j in "ABC":
            b = rr.br[j]
            anims += [Create(b.line), FadeIn(b.caps), FadeIn(b.label)]
        flash = [Indicate(tl.blocks_in(None, ticks=[1, 2, 3]), scale_factor=1.15, run_time=1.2)]
        self.say("A runs first, B second, C third, all within three seconds.", *anims, *flash)

        # S11.6
        self.say("Response times: zero, one, and two. Average: one second. Down from five.",
                 *ro.reveal_numerator(run_time=1.2), prof.change("happy"))
        self.play(*ro.reveal_value(), run_time=0.7)
        self.play(*ro.strike("5"), run_time=0.8)
        self.play(*ro.frame_value(True), FadeOut(sb1), FadeIn(sb2), run_time=0.8)
        self.beat(0.6)
