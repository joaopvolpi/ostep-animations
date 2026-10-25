import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


class S10ResponseTime(Ep07Scene):
    def construct(self):
        self.world(opened=(0, 1, 2), term="STCF", stu="excited", prof="explaining")
        stu, prof, strip = self.stu, self.prof, self.strip
        st = Chart("stcf")
        title = policy_title("STCF")
        self.add(st.group(), title)
        cg = VGroup(st.tl, *st.br.values(), *st.mk.values(), st.ro.shown)

        # S10.1
        self.say("If all we cared about were batch jobs, we'd be done.",
                 cg.animate.scale(0.4).move_to(P3(4.2, 0.9)), prof.change("neutral"))

        # S10.2
        term = Terminal(width=4.4, height=2.0, font_size=20).move_to(P3(-3.4, 1.0))
        cursor = Rectangle(width=0.13, height=0.24).set_fill(TEXT, 1).set_stroke(width=0)
        cursor.move_to(term._slot(0) + RIGHT * 0.15)
        blink = Succession(*[Succession(FadeOut(cursor, run_time=0.25), FadeIn(cursor, run_time=0.25)) for _ in range(3)])
        self.say("But then came time-shared machines, and people sitting at terminals, typing.",
                 FadeIn(term, shift=RIGHT * 0.6), stu.change("curious", look_at=term), after(1.0, FadeIn(cursor), blink))

        # S10.3
        sw = stopwatch_icon(0.3).move_to(P3(-3.4, 2.6))
        key = VGroup(RoundedRectangle(width=0.5, height=0.5, corner_radius=0.08).set_fill(CARD_FILL, 1).set_stroke(TEXT, 2),
                     Text("a", font=MONO_FONT, font_size=26, color=TEXT)).move_to(P3(-4.6, -1.7))
        key[1].move_to(key[0])
        self.say("Now they care about something else: how long until the computer responds.",
                 after(0.8, FadeIn(key, scale=1.3), FadeOut(key, run_time=0.5, scale=0.8)),
                 after(1.5, FadeIn(sw), Rotate(sw.hand, -TAU * 0.6, about_point=sw[0].get_center(), run_time=2.0, rate_func=linear)))

        # S10.4
        ten = Text("10 s", font_size=24, color=KERNEL_COLOR).next_to(sw, RIGHT, buff=0.2)
        self.say("That's response time: the time from when a job arrives to the first time it runs.",
                 self.term("response time", hold=0.8),
                 after(1.2, AnimationGroup(Rotate(sw.hand, -TAU * 0.4, about_point=sw[0].get_center(), run_time=2.0, rate_func=linear))),
                 after(3.5, FadeOut(cursor, run_time=0.1), term.type("a"), FadeIn(ten), stu.change("frustrated")))

        # S10.5
        f = MathTex(r"T_{response}", "=", r"T_{firstrun}", "-", r"T_{arrival}", font_size=38).move_to(P3(0, -2.3))
        f[2].set_color(INTRO)
        ghost_f = MathTex(r"T_{turnaround} = T_{completion} - T_{arrival}", font_size=28, color=DIM).move_to(P3(0, -3.15))
        self.play(Write(f), FadeIn(ghost_f), run_time=1.6)

        # S10.6
        ch = Chart("sjf5", brackets="resp", markers=False)
        tl = ch.tl
        run = ch.sp["run"]
        arrows = [tl.arrival_marker(r, 0, dx=0.08 * k) for k, r in enumerate("ABC")]
        self.say("Look at SJF with three jobs of five seconds each.",
                 FadeOut(VGroup(term, sw, ten, cg, f, ghost_f, cursor), run_time=0.6),
                 Transform(title, policy_title("SJF")),
                 after(0.6, AnimationGroup(Create(tl.grid), FadeIn(tl.row_labels), FadeIn(tl.tick_labels))),
                 after(1.6, LaggedStart(*[FadeIn(a, shift=DOWN * 0.2) for a in arrows], lag_ratio=0.4)))

        # S10.7
        br = ch.br
        anims = []
        with self.narrate("A runs first and responds at zero."):
            for t in range(1, 6):
                self.play(*cell_anims(tl, run, {}, t, run_time=0.3), run_time=0.3)
            self.play(Create(br["A"].line), FadeIn(br["A"].caps), FadeIn(br["A"].label), run_time=0.6)

        # S10.8
        with self.narrate("B waits five. C waits ten."):
            self.play(Create(br["B"].line), FadeIn(br["B"].caps), FadeIn(br["B"].label), run_time=0.7)
            for t in range(6, 11):
                self.play(*cell_anims(tl, run, {}, t, run_time=0.15), run_time=0.15)
            self.play(Create(br["C"].line), FadeIn(br["C"].caps), FadeIn(br["C"].label), run_time=0.7)
            for t in range(11, 16):
                self.play(*cell_anims(tl, run, {}, t, run_time=0.15), run_time=0.15)

        # S10.9
        ro = ch.ro
        ro.shown = VGroup()
        self.say("Average response time: five seconds.", *ro.reveal_numerator(run_time=1.2))
        self.play(*ro.reveal_value(), run_time=0.8)
        self.play(*ro.frame_value(False), run_time=0.6)

        # S10.10
        mini = VGroup(RoundedRectangle(width=1.5, height=0.8, corner_radius=0.08).set_fill("#101010", 1).set_stroke(DIM, 2),
                      Text("a", font=MONO_FONT, font_size=22, color=TEXT))
        mini[1].move_to(mini[0])
        msw = stopwatch_icon(0.2).next_to(mini, RIGHT, buff=0.2)
        mlab = Text("10 s", font_size=22, color=KERNEL_COLOR).next_to(msw, RIGHT, buff=0.1)
        pop = VGroup(mini, msw, mlab).move_to(P3(4.4, 2.5))
        self.say("Imagine typing a character and waiting ten seconds because other jobs got in front.",
                 FadeIn(pop, scale=1.4))

        # S10.11
        self.say("That's a terrible terminal.", FadeOut(pop), stu.change("sad"))

        # S10.12
        sb = scoreboard_at([("SJF · STCF", True, False)], y=2.5)
        self.say("SJF, STCF, and their relatives are great for turnaround and bad for response. So we need a new policy.",
                 prof.change("explaining"), FadeIn(sb, shift=DOWN * 0.2))
