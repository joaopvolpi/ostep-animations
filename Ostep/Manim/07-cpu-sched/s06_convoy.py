import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


class S06Convoy(Ep07Scene):
    def construct(self):
        self.world(term="FIFO", stu="curious", prof="neutral")
        stu, prof, strip = self.stu, self.prof, self.strip
        fifo = Chart("fifo")
        title = policy_title("FIFO")
        self.add(fifo.group(), title)
        tl = fifo.tl
        cv = Chart("convoy")
        run = cv.sp["run"]
        ro = cv.ro
        ro.shown = VGroup()
        bars = convoy_bars(("A", "B", "C"))

        # S06.1
        self.say("Okay, but I bet there's a catch. What if the jobs aren't all the same length?",
                 stu.change("curious"), strip.locks[0].shake(run_time=1.2))

        # S06.2
        old = VGroup(*fifo.br.values(), *fifo.mk.values(), fifo.ro.shown)
        self.say("That's the first assumption going away.",
                 strip.locks[0].open(), tl.clear_blocks(0.9), FadeOut(old),
                 after(0.8, LaggedStart(*[FadeIn(b, shift=DOWN * 0.2) for b in bars], lag_ratio=0.4)))
        tl.purge()

        # S06.3
        labs = ["100 s", "10 s", "10 s"]
        self.say("Same three jobs, but now A needs a hundred seconds, and B and C need ten each.",
                 *[Transform(b.txt, Text(t, font_size=18, color=INK_DARK).move_to(b.rect)) for b, t in zip(bars, labs)])

        # S06.4
        with self.narrate("A is first in line, so A runs for a full hundred seconds."):
            for t in range(1, 11):
                rt = max(0.12, 0.5 - 0.04 * t)
                self.play(*cell_anims(tl, run, {}, t, run_time=rt), run_time=rt)

        # S06.5
        anims = []
        for t in (11, 12):
            anims += cell_anims(tl, run, {}, t, run_time=0.5)
        anims += [FadeIn(m, shift=DOWN * 0.4) for m in cv.mk.values()]
        for b in cv.br.values():
            anims += [Create(b.line), FadeIn(b.caps), FadeIn(b.label)]
        self.say("Then B finishes at a hundred and ten. C at a hundred and twenty.", *anims)

        # S06.6
        self.say("The average: a hundred and ten seconds. Ouch.",
                 *ro.reveal_numerator(), stu.change("surprised"))
        self.play(*ro.reveal_value(), run_time=0.8)
        self.play(*ro.frame_value(False), run_time=0.6)
        self.play(Wiggle(ro.value_mob, scale_value=1.2, rotation_angle=0.04 * TAU), run_time=0.8)

        # S06.7
        red = []
        for j in "BC":
            i = tl.row_index(j)
            for t in range(1, 11):
                if (i, t) in tl.block_at:
                    red.append(tl.block_at[(i, t)].animate.set_stroke(KERNEL_COLOR, 3.5))
        self.say("This is the convoy effect: short consumers of a resource get stuck behind a heavyweight one.",
                 self.term("convoy effect", hold=0.8), after(1.5, AnimationGroup(*red)),
                 after(2.5, Indicate(tl.blocks_in("A"), scale_factor=1.05, run_time=1.5)))

        # S06.8
        cg = VGroup(tl, *cv.br.values(), *cv.mk.values(), ro.shown)
        cg.save_state()
        tray, ps, extras = shopper_line()
        self.say("It's your supermarket line again.",
                 cg.animate.scale(0.5).move_to(P3(3.3, -0.3)),
                 after(0.8, AnimationGroup(FadeIn(tray, shift=RIGHT * 0.5),
                                                      *[FadeIn(p, shift=RIGHT * 0.5) for p in ps], FadeIn(extras))))
        self.beat(0.6)
        self.play(FadeOut(VGroup(tray, *ps, extras), shift=LEFT * 0.5), Restore(cg), run_time=1.2)

        # S06.9
        self.say("Just let B and C go first!", stu.change("excited"))

        # S06.10
        self.say("Hold that thought.", prof.change("happy"))
        self.beat(0.8)
