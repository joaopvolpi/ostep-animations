import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403
from s22_recap import LINES, icon  # noqa: E402,F401


class S23Teaser(Ep09Scene):
    def construct(self):
        head = Text("Recap", font_size=44, color=VIRT, weight=BOLD).move_to(P3(-6.2, 2.3), aligned_edge=LEFT)
        lines = VGroup(*[Text(wrap_text(s, 8.8, 24), font_size=24, color=TEXT, line_spacing=0.75) for s in LINES])
        lines.arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(P3(-6.2, 1.8), aligned_edge=UL)
        icons = [icon(i).move_to(P3(5.0, lines[i].get_center()[1])) for i in range(5)]
        self.add(head, lines, *icons)
        stu = Student("neutral").move_to(STU_DIALOGUE)
        prof = Professor("neutral").flip().move_to(PROF_DIALOGUE)
        cpu = CPU(size=0.8, label="CPU").move_to(P3(0, 1.7))
        q = Queue(label="Ready", center=(0, 0.3), slots=4, spacing=0.9, font_size=18)
        ps = [proc(n, scale=0.4) for n in "ABCD"]
        q.place(*ps)

        # S23.1
        self.say("Everything so far has been about one CPU. My laptop has eight. What changes?",
                 FadeOut(VGroup(head, lines, *icons)), FadeIn(stu), FadeIn(prof), FadeIn(cpu), FadeIn(q), *[FadeIn(p) for p in ps])
        self.play(stu.change("curious"), run_time=0.5)

        # S23.2
        chips = [CPU(size=0.8, label="CPU" if k == 3 else "").move_to(cpu) for k in range(4)]
        self.add(*chips)
        self.remove(cpu)
        arrows = VGroup(*[Arrow(P3(x, 1.3), P3(x * 0.4, 0.8), buff=0.05, stroke_width=3, color=DIM,
                                max_tip_length_to_length_ratio=0.2) for x in (-3.0, -1.0, 1.0, 3.0)])
        sparks = VGroup(*[Dot(P3(0.9 * k - 1.35, 0.85), radius=0.06, color=CPU_COLOR) for k in range(4)])
        self.say("Quite a lot, I'm afraid. Caches, locks, and one queue that eight CPUs all want to touch at once…",
                 prof.change("worried"),
                 AnimationGroup(*[glide(c, P3(x, 1.7), 1.4) for c, x in zip(chips, (-3.0, -1.0, 1.0, 3.0))]),
                 Succession(Wait(2.5), Create(arrows), FadeIn(sparks), Indicate(sparks, color=CPU_COLOR, scale_factor=2.0)))

        # S23.3
        shake = Succession(*[q.animate(run_time=0.1).shift(RIGHT * 0.1 * s) for s in (1, -2, 2, -1)])
        self.say("Uh oh.", stu.change("surprised"), shake)

        # S23.4
        self.play(FadeOut(*self.mobjects), run_time=0.5)
        dot = Dot(radius=0.1, color=VIRT)
        nxt = Text("Next: 10 · Multi-CPU Scheduling", font_size=40, color=TEXT)
        card = VGroup(dot, nxt).arrange(RIGHT, buff=0.3).move_to(ORIGIN)
        self.play(FadeIn(card), run_time=0.8)
        self.wait(2.0)
