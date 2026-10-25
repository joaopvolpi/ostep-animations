import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


def mini_tl(x0, x1, y, ticks=10):
    return Timeline(["CPU"], ticks=ticks, x_range=(x0, x1), top=y, row_height=0.34, row_kinds=["cpu"],
                    tick_labels=False, label_font=16)


class S13WhyKeepLottery(Ep09Scene):
    def construct(self):
        self.world(stu="surprised", prof="proud")
        stu, prof = self.stu, self.prof
        lf = card_rect(5.8, 3.6, DIM).move_to(P3(-3.4, 0.5))
        rf = card_rect(5.8, 3.6, DIM).move_to(P3(3.4, 0.5))
        lt = Text("Stride", font_size=26, color=VIRT).move_to(P3(-3.4, 2.0))
        rt = Text("Lottery", font_size=26, color=VIRT).move_to(P3(3.4, 2.0))
        xs_l, xs_r = (-5.2, -4.0, -2.8), (1.6, 2.8, 4.0)
        lp = {n: proc(n, scale=0.5).move_to(P3(x, 0.5)) for n, x in zip("ABC", xs_l)}
        rp = {n: proc(n, scale=0.5).move_to(P3(x, 0.5)) for n, x in zip("ABC", xs_r)}
        dl = proc("D", scale=0.5).move_to(P3(-1.0, 1.6))
        dr = proc("D", scale=0.5).move_to(P3(5.3, 1.6))

        # S13.1
        self.say("Then stride beats lottery, right? Why did we bother with lottery?",
                 stu.change("curious"), FadeIn(lf), FadeIn(rf), FadeIn(lt), FadeIn(rt),
                 *[FadeIn(p) for p in (*lp.values(), *rp.values(), dl, dr)])

        # S13.2
        flags = VGroup(*[token("pass 200", COL[n], size=18).next_to(lp[n], DOWN, buff=0.12) for n in "ABC"])
        stacks = {n: TicketStack(t, COL[n], scale=0.6).next_to(rp[n], UP, buff=0.15)
                  for n, t in zip("ABC", (100, 50, 250))}
        nostate = Text("no per-process state", font_size=20, color=GREEN_OK).move_to(P3(3.4, -0.45))
        self.say("One good reason. Lottery has no global state.",
                 prof.change("explaining"), FadeIn(flags), *[FadeIn(s) for s in stacks.values()], FadeIn(nostate))

        # S13.3
        dpos = P3(-1.4, 0.5)
        q = token("pass = ?", CPU_COLOR, size=20).move_to(P3(-1.4, 1.5))
        self.say("In the middle of our stride example, a new job shows up. What should its pass value be?",
                 hop_bottom(dl, dpos + DOWN * 0.1, run_time=0.9), Succession(Wait(1.5), FadeIn(q)))

        # S13.4
        tl = mini_tl(-5.0, -0.9, -0.85)
        zero = token("pass 0", COL["D"], size=18).next_to(dl, DOWN, buff=0.12)
        banner = Text("monopoly", font_size=24, color=KERNEL_COLOR, weight=BOLD).move_to(P3(-3.4, -1.95))
        self.say("Zero? Then it's far below everyone and monopolizes the CPU until it catches up.",
                 Transform(q, zero), FadeIn(tl),
                 Succession(Wait(1.2), *[tl.fill("CPU", t, "running", color=COL["D"], run_time=0.25) for t in range(1, 9)],
                            FadeIn(banner)))

        # S13.5
        ghosts = [token(s, DIM, size=18).move_to(zero) for s in ("50", "120", "200", "?")]
        self.say("Anything else? You have to decide what.",
                 Succession(*[Transform(q, g.copy(), run_time=0.5) for g in ghosts]), FadeOut(banner))
        self.play(FadeOut(tl), FadeOut(VGroup(*[b for b in tl.blocks])), run_time=0.3)

        # S13.6
        tot = Text("total: 400", font_size=22, color=TEXT).move_to(P3(3.4, -0.45))
        tot2 = Text("total: 450", font_size=22, color=TEXT).move_to(tot)
        sd = TicketStack(50, COL["D"], scale=0.6).move_to(stacks["C"].get_center() + RIGHT * 1.0).align_to(stacks["C"], DOWN)
        tl2 = mini_tl(1.6, 5.8, -0.95)
        seq = "ABCDABCDAD"
        self.say("With lottery, a new job just arrives with its tickets. Add them to one global total, and go.",
                 FadeOut(nostate), FadeIn(tot),
                 hop_bottom(dr, P3(5.0, 0.5) + DOWN * 0.1, run_time=0.9), FadeIn(sd), FadeIn(tl2),
                 Succession(Wait(2.0), Transform(tot, tot2, run_time=0.6),
                            *[tl2.fill("CPU", i + 1, "running", color=COL[c], run_time=0.25) for i, c in enumerate(seq)]))

        # S13.7
        l_lab = Text("exact, fussy", font_size=24, color=DIM).move_to(P3(-3.0, -1.95))
        r_lab = Text("flexible, approximate", font_size=24, color=DIM).move_to(P3(3.0, -1.95))
        self.say("Lottery is sloppy but flexible. Stride is exact but fussy.",
                 stu.change("excited"), FadeIn(l_lab), FadeIn(r_lab))

        # S13.8
        self.say("That's the trade.", prof.change("happy"))
        self.beat(1.0)
        self.fade_stage()
