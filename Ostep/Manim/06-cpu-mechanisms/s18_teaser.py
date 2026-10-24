import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403
from s17_recap import build_end as s17_end  # noqa: E402


class S18Teaser(Ep06Scene):
    def construct(self):
        stu, prof = corner_chars(True, "neutral", "neutral")
        d = s17_end()
        recap = VGroup(d["header"], d["lines"], *d["icons"])
        self.add(recap, stu, prof)

        # S18.1
        sd = student_dialogue("curious")
        pd = prof_dialogue("neutral")
        q = Queue(label="Ready", center=P3(0, 0.3), slots=3, spacing=1.2)
        ps = [bottom_to(proc(n, "ready", scale=0.8), P3(0, 0)) for n in "ABC"]
        q.place(*ps)
        chip = CPU(1.0, label="CPU").move_to(P3(0, 2.7))
        self.say("So the OS can take the CPU back whenever it wants, and swap one process for another. Great. But "
                 "when should it? And who should it pick?",
                 AnimationGroup(FadeOut(recap), ReplacementTransform(stu, sd), ReplacementTransform(prof, pd), run_time=1.2),
                 Succession(Wait(1.5), AnimationGroup(FadeIn(q), *[FadeIn(p) for p in ps], FadeIn(chip))))

        # S18.2
        gears = GearPair(0.35).move_to(P3(-4.3, 0.8))
        make_translucent(gears, 0.5, 0.6)
        spot = Spotlight(height=2.2, spread=0.6).move_beam_to(P3(4.3, 0.3))
        self.say("Ah. That's no longer a mechanism question. That's a policy question.", pd.change("happy"),
                 AnimationGroup(FadeIn(gears), gears.spin(TAU, 3.0), FadeIn(spot)))

        # S18.3
        pts = [P3(p.get_center()[0], 0.3) for p in ps]
        dot = Dot(radius=0.1).set_fill(VIRT, 1)
        nxt = Text("Next: 07 · CPU Scheduling", font_size=40, color=TEXT)
        card = VGroup(dot, nxt).arrange(RIGHT, buff=0.25).move_to(ORIGIN)
        everything = Group(*self.mobjects)
        self.say("The machinery is done. Next time we meet the scheduler.",
                 Succession(spot.animate(run_time=0.8).move_beam_to(pts[0]), spot.animate(run_time=0.8).move_beam_to(pts[1]),
                            spot.animate(run_time=0.8).move_beam_to(pts[2]),
                            FadeOut(everything, run_time=0.5), FadeIn(card)))
