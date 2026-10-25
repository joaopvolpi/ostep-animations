import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from s12_sqms_affinity import make_grid, BOOK_TABLE  # noqa: E402
from common_more import *  # noqa: E402,F401,F403

PIN_TABLE = ["AEAAA", "BBEBB", "CCCEC", "DDDDE"]


class S13Patch(Ep10Scene):
    def construct(self):
        self.world(strip=1, term="scalability", stu="neutral", prof="worried")
        stu, prof = self.stu, self.prof
        cpus = four_cpus()
        grid = make_grid(repeat=True)
        for r in range(4):
            grid.set_row(r, BOOK_TABLE[r])
        self.add(*cpus, grid)

        # S13.1
        pins = [pin_icon(0.5).move_to(c.cpu.get_corner(UL) + P3(0.05, 0.25)) for c in cpus]
        self.say("Real SQMS schedulers add an affinity mechanism.",
                 grid.clear(), prof.change("explaining"),
                 Succession(Wait(0.8), LaggedStart(*[FadeIn(p, shift=DOWN * 0.4) for p in pins], lag_ratio=0.3)))

        # S13.2
        self.say("Let some jobs stay put, and move others around to balance the load.",
                 LaggedStart(*[Indicate(p, color=KERNEL_COLOR, scale_factor=1.4) for p in pins], lag_ratio=0.3))

        # S13.3
        warm = [c.warmth(3, COL["ABCD"[i]]) for i, c in enumerate(cpus)]
        self.say("For our five jobs: A, B, C and D each stay on their own CPU.",
                 AnimationGroup(*[grid.fill_row(r, PIN_TABLE[r], run_time=0.3, lag=0.4) for r in range(4)]),
                 *warm)

        # S13.4
        e_cells = [(0, 1), (1, 2), (2, 3), (3, 4)]
        arrows = [Arrow(grid.cell_center(*a), grid.cell_center(*b), buff=0.28, stroke_width=3, color=COL["E"], tip_length=0.14)
                  for a, b in zip(e_cells, e_cells[1:])]
        suit = suitcase_icon(0.4).move_to(grid.cell_center(0, 1) + UP * 0.45)
        self.say("Only job E migrates, from CPU to CPU, so the load stays fair.",
                 grid.highlight_job("E"), FadeIn(suit, shift=DOWN * 0.2), self.note("migration"),
                 Succession(Wait(1.2), LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.8)),
                 Succession(Wait(1.2), suit.animate.move_to(grid.cell_center(3, 4) + UP * 0.45)))

        # S13.5
        nxt = tag("next round: another job", 18).next_to(grid, DOWN, buff=0.2)
        self.say("A different job could take the migrating role the next time round, if you want fairness among the others too.",
                 grid.unhighlight(), FadeOut(VGroup(*arrows)),
                 suit.animate.move_to(grid.repeat.get_bottom() + DOWN * 0.3), FadeIn(nxt))

        # S13.6
        gear = GearPair(0.28)
        cx = tag("complex", 20, KERNEL_COLOR)
        gc = VGroup(gear, cx).arrange(RIGHT, buff=0.2).move_to(P3(4.4, -1.7))
        self.say("It works. But it's complex to build.",
                 FadeIn(gc, shift=LEFT * 0.2), gear.spin(angle=TAU, run_time=2.0), FadeOut(nxt), FadeOut(suit))

        # S13.7
        def item(txt, ok):
            return VGroup(label(txt, 24), (tick_mark(0.25) if ok else x_mark(0.25))).arrange(RIGHT, buff=0.12)
        verdict = VGroup(item("simple", True), item("scales", False), item("affinity (patchable)", False)).arrange(RIGHT, buff=0.7)
        verdict.move_to(P3(0, -3.3))
        self.say("So SQMS is easy to write, and doesn't scale or preserve affinity well.",
                 LaggedStart(*[FadeIn(v, shift=UP * 0.2) for v in verdict], lag_ratio=0.7))
        self.beat(0.5)

        # transition: everything fades except badge and strip
        self.play(FadeOut(VGroup(*cpus, grid, gc, verdict, *pins)), run_time=0.8)
