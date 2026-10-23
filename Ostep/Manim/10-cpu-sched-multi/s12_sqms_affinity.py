import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common_more import *  # noqa: E402,F401,F403

GRID_AT = P3(-0.7, -1.7)
BOOK_TABLE = ["AEDCB", "BAEDC", "CBAED", "DCBAE"]


def make_grid(repeat=False):
    return ScheduleGrid(rows=4, columns=5, cell_w=0.8, cell_h=0.5, colors=grid_colors(), repeat_label=repeat).move_to(GRID_AT)


class S12SqmsAffinity(Ep10Scene):
    def construct(self):
        self.world(strip=1, term="scalability", stu="sad", prof="explaining")
        stu, prof = self.stu, self.prof
        cpus = four_cpus()
        q_old, ps_old = job_queue("E", center=(0, -1.15))
        on_chip = []
        for i, j in enumerate("ABCD"):
            p = proc(j, "running", 0.5)
            place_on(p, cpus[i].slot_point())
            on_chip.append(p)
        null = mono("NULL", 18, DIM).move_to(P3(3.3, -1.0))
        pad = Padlock(0.45).move_to(P3(-3.2, -1.0))
        self.add(*cpus, q_old, *ps_old, *on_chip, null, pad)

        # S12.1
        q, ps = job_queue("ABCDE", center=(4.2, -1.0), label_text="the queue", spacing=0.75, scale=0.35)
        grid = make_grid()
        cap = label("5 jobs · 4 CPUs", 22, DIM).move_to(P3(-0.7, -3.2))
        self.say("The second problem is cache affinity. Take five jobs, A through E, and four CPUs.",
                 FadeOut(VGroup(q_old, *ps_old, *on_chip, null, pad)), FadeIn(q), LaggedStart(*[FadeIn(p) for p in ps], lag_ratio=0.1),
                 FadeIn(grid), FadeIn(cap), stu.change("neutral"), prof.change("neutral"))

        # S12.2
        self.say("Each CPU simply takes the next job from the shared queue…",
                 grid.fill_column(0, "ABCD", run_time=0.5, lag=0.3), *[FadeOut(p, shift=UP * 0.5) for p in ps[:4]])

        # S12.3
        with self.narrate("…so over time the jobs bounce around."):
            for c in range(1, 5):
                self.play(grid.fill_column(c, [BOOK_TABLE[r][c] for r in range(4)], run_time=0.4, lag=0.15), run_time=0.8)

        # S12.4
        colds = [label("cold", 18, MEM_COLOR).move_to(cpus[i].cache_bottom() + DOWN * 0.18) for i in range(3)]
        self.say("A on CPU zero, then CPU one, then CPU two. Each time it lands on a cold cache.",
                 grid.highlight_job("A"),
                 Succession(*[AnimationGroup(FadeIn(c, scale=1.3), Indicate(cpus[i].strip, color=MEM_COLOR, scale_factor=1.1))
                              for i, c in enumerate(colds)]))

        # S12.5
        xm = x_mark(0.5).move_to(P3(2.2, -1.7))
        self.say("This is exactly the opposite of what affinity wants.",
                 FadeIn(xm, scale=1.5), prof.change("worried"))
        self.beat(0.5)
