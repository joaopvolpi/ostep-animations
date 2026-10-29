import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


class S18Teaser(Ep08Scene):
    def construct(self):
        # starts with the recap faded; characters glide to dialogue mode
        stu, prof = student_corner("neutral"), prof_corner("neutral")
        self.add(stu, prof)
        self.stu, self.prof = stu, prof
        panel = SliderPanel(["queues", "time slice", "allotment", "boost"], width=2.2, font_size=18).move_to(P3(0, 1.0))
        panel.set_opacity(0)

        # S18.1
        self.say("MLFQ is clever. But it has so many knobs, and the rules keep patching each other. Isn't there a simpler way to share the CPU fairly?",
                 stu.animate.scale(1 / CHAR_SCALE).move_to(STUDENT_DLG), prof.animate.scale(1 / CHAR_SCALE).move_to(PROF_DLG),
                 after(1.0, FadeIn(panel.set_opacity(1)), Wait(0.6), FadeOut(panel)))
        self.play(stu.change("curious"), run_time=0.5)

        # S18.2
        drum = RaffleDrum(1.5).move_to(P3(0, 0.8))
        pie = mini_pie([(0.75, COL["A"]), (0.25, COL["B"])], 0.35).move_to(P3(0, 2.15))
        shares = label("shares", 20, DIM).next_to(pie, RIGHT, buff=0.25)
        tickets = [Ticket(COL["A"]) for _ in range(3)] + [Ticket(COL["B"])]
        for k, t in enumerate(tickets):
            t.move_to(P3(-2.2 + 0.5 * k, 2.0))
        ins = [Succession(FadeIn(t, shift=DOWN * 0.2), t.animate(run_time=0.6).move_to(drum.cage_center()).scale(0.4).set_opacity(0)) for t in tickets]
        self.say("There is. Forget turnaround and response for a moment. What if we just promised each job a share of the CPU, and picked the next one by drawing a ticket from a raffle drum?",
                 prof.change("happy"), FadeIn(drum), FadeIn(pie, scale=0.6), FadeIn(shares),
                 after(3.0, LaggedStart(*ins, lag_ratio=0.4)), after(5.0, drum.spin(1, run_time=2.0)))

        # S18.3
        tk = Ticket(COL["A"], label="A", width=0.7, height=0.4).move_to(drum.chute_point())
        hand = hand_icon(0.45).move_to(drum.chute_point() + RIGHT * 0.9 + UP * 0.3)
        self.say("The scheduler gambles?", stu.change("surprised"), FadeIn(tk, scale=0.4), FadeIn(hand),
                 hand.animate(run_time=1.2).move_to(tk.get_right() + RIGHT * 0.3), after(1.0, tk.animate(run_time=1.0).move_to(P3(1.8, 0.3))))

        # S18.4
        self.say("Next time.", prof.change("proud"), min_time=1.0)
        everything = Group(*self.mobjects)
        self.play(FadeOut(everything), run_time=0.5)
        dot = Dot(radius=0.1, color=VIRT)
        nxt = label("Next: 09 · Lottery Scheduling", 40, TEXT)
        grp = VGroup(dot, nxt).arrange(RIGHT, buff=0.25).move_to(ORIGIN)
        self.play(FadeIn(grp), run_time=0.8)
        self.beat(2.0)
