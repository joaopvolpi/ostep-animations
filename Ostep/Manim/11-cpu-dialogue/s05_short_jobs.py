import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


class S05ShortJobs(Ep11Scene):
    def construct(self):
        self.world(stu="curious", prof="proud", mode="corner", term="resource manager")
        stu, prof = self.stu, self.prof
        bd, gauge, stack, procs, puzzle = build_s04_end()
        self.add(bd, gauge, stack, procs, puzzle)

        q, A, B = make_checkout_queue()
        counter = make_counter()
        spot = Spotlight(height=1.4, spread=0.5).move_to(P3(0.6, 1.9))
        which = label("which?", 20, DIM).next_to(spot, RIGHT, buff=0.15).shift(UP * 0.3)
        tl = make_mini_timeline()

        # S05.1
        self.say("And the policies on top of those mechanisms? Any lessons there?",
                 FadeOut(bd), FadeOut(gauge), FadeOut(stack), FadeOut(procs), FadeOut(puzzle),
                 FadeIn(spot), FadeIn(which), prof.change("explaining"), min_time=3.5)

        # S05.2
        self.say("Bumping short jobs to the front of the queue.",
                 FadeIn(q), FadeIn(A), FadeIn(B), FadeIn(counter), FadeIn(tl), min_time=2.0)
        q.items = [B, A]
        self.play(q.pack(), spot.animate.move_beam_to(B[0].get_center()), FadeOut(which), run_time=0.9)

        # S05.3
        gum = Text("gum", font_size=20, color=TEXT).move_to(B[1])
        gum.next_to(B[0], UP, buff=0.05)
        self.say("I knew that was a good idea the day I was buying gum...",
                 stu.thinks("gum"), Transform(B[1], gum), min_time=3.5)

        # S05.4
        short = label("short", 20, DIM).next_to(B[0], UP, buff=0.05)
        q.items = [A, B]
        x_mark_ = x_mark(0.35).move_to(counter[1].get_top() + UP * 0.5)
        clk = ClockIcon(radius=0.18).next_to(A[0], UP, buff=0.35)
        a_at = P3(-2.5, COUNTER_AT[1] - 0.0)
        q.remove_item(A)
        self.say("...and the guy ahead of me had a credit card that wouldn't work.",
                 stu.remove_bubble(), Transform(B[1], short),
                 Succession(AnimationGroup(hop_to(A, a_at + (A.get_center() - A.get_bottom()), anchor="center", run_time=0.7),
                                           q.pack()),
                            AnimationGroup(FadeIn(x_mark_), A[0].change("blocked"), FadeIn(clk)),
                            clk.spin(turns=2, run_time=1.0), FadeOut(x_mark_)),
                 Succession(Wait(2.0), tl.fill(0, 0, "running"), tl.fill(1, 0, "ready"),
                            tl.fill(0, 1, "running"), tl.fill(1, 1, "ready"), tl.fill(0, 2, "running")),
                 min_time=5.0)

        # S05.5
        self.say("He was no short job, let me tell you.", stu.change("frustrated"),
                 Succession(tl.fill(0, 3, "running"), tl.fill(1, 2, "ready"), tl.fill(0, 4, "running"),
                            tl.fill(1, 3, "ready"), tl.fill(0, 5, "running"), tl.fill(1, 4, "ready")))
        self.beat(0.5)

        # S06
        self.say("That sounds oddly rude to that poor fellow. What else?", prof.change("worried"),
                 Indicate(A[0], scale_factor=1.1), spot.animate.set_opacity(0.3), min_time=3.0)
        self.beat(0.5)
