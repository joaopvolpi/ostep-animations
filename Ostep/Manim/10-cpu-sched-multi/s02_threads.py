import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


class S02Threads(Ep10Scene):
    def construct(self):
        w = build_s01_end()
        lap, chips, a, sw, stu, prof, comp = (w[k] for k in ("lap", "chips", "a", "sw", "stu", "prof", "comp"))
        stu.set_expression("sad")
        cores = label("8 cores", 26)
        laptop = VGroup(lap, chips, a)
        cores.next_to(lap, UP, buff=0.15)
        self.add(laptop, cores, sw, stu, prof, comp)

        # S02.1  laptop moves up, program splits
        self.play(AnimationGroup(laptop.animate.scale(0.8).move_to(P3(0, 1.0)),
                                 cores.animate.move_to(P3(0, 2.3)),
                                 sw.animate.move_to(P3(4.3, 1.0)),
                                 FadeOut(comp), run_time=1.0))
        a_pos = chips[0].get_top()
        threads = [make_thread("", COL["A"], scale=0.4) for _ in range(8)]
        for t in threads:
            t.set_expression("ready")
            place_on(t, a_pos)
        sw2 = stopwatch("8×", 24).move_to(sw)
        lit = [mini_chip(True, size=0.32 * 0.8).move_to(c) for c in chips]
        hops = [hop_to(t, c.get_top() + DOWN * 0.04, height=0.5, run_time=0.8) for t, c in zip(threads, chips)]
        with self.narrate("To use eight cores, you'd have to rewrite it to run in parallel, perhaps using threads."):
            self.play(self.note("parallel"))
            self.play(FadeOut(a, run_time=0.01), *[FadeIn(t, run_time=0.2) for t in threads], run_time=0.3)
            self.play(LaggedStart(*hops, lag_ratio=0.15),
                      LaggedStart(*[Transform(c, l) for c, l in zip(chips, lit)], lag_ratio=0.15),
                      Succession(Wait(0.6), Transform(sw.txt, sw2.txt.move_to(sw.txt, aligned_edge=LEFT))),
                      run_time=2.2)
            self.play(self.note("threads"))

        # S02.2  counter cameo
        cell = Rectangle(width=0.9, height=0.7).set_fill(MEM_COLOR, 0.15).set_stroke(MEM_COLOR, 3)
        val = mono("5", 28)
        cap = label("counter", 20, DIM)
        cam = VGroup(cell, val.move_to(cell), cap.next_to(cell, DOWN, buff=0.1)).move_to(P3(0, -1.5))
        arr_l = VGroup(Arrow(P3(-2.4, -1.5), P3(-0.6, -1.5), buff=0, color=COL["A"]), mono("+1", 22, COL["A"]).move_to(P3(-1.5, -1.15)))
        arr_r = VGroup(Arrow(P3(2.4, -1.5), P3(0.6, -1.5), buff=0, color=COL["A"]), mono("+1", 22, COL["A"]).move_to(P3(1.5, -1.15)))
        with self.narrate("Remember the threads from the first episodes, the ones that fought over the shared counter?"):
            self.play(FadeIn(cam, shift=UP * 0.3), run_time=0.5)
            self.play(Create(arr_l[0]), Create(arr_r[0]), FadeIn(arr_l[1]), FadeIn(arr_r[1]), run_time=0.7)
            self.play(Transform(val, mono("6", 28).move_to(val)), Flash(cell, color=KERNEL_COLOR, run_time=0.6))
            self.play(FadeOut(VGroup(cam, arr_l, arr_r)), run_time=0.5)

        # S02.3
        self.say("Okay, so that's the programmer's problem. What does it have to do with the OS?",
                 stu.change("confused"))

        # S02.4  others arrive
        others = [proc(n, "ready", 0.4) for n in "BCDE"]
        pts = [P3(-3.9, -1.2), P3(-3.2, -1.2), P3(3.2, -1.2), P3(3.9, -1.2)]
        for p, pt in zip(others, pts):
            place_on(p, pt)
        self.say("Everything. Because the moment you do have eight busy threads, plus every other process on the machine",
                 prof.change("explaining"), stu.change("neutral"),
                 LaggedStart(*[FadeIn(p, shift=UP * 0.5) for p in others], lag_ratio=0.3))

        # S02.5  spotlight sweeps chips
        spot = Spotlight(height=1.0, spread=0.4)
        spot.move_beam_to(chips[0].get_center() + DOWN * 0.1)
        qs = VGroup(*[question_mark(0.3).move_to(c.get_center() + UP * 0.75) for c in chips])
        sweep = Succession(*[spot.animate.move_beam_to(c.get_center() + DOWN * 0.1) for c in chips[1:]])
        self.say("someone has to decide who runs on which core.",
                 FadeIn(spot), LaggedStart(*[FadeIn(q, scale=0.5) for q in qs], lag_ratio=0.1),
                 Succession(Wait(0.5), *[spot.animate(run_time=0.35).move_beam_to(c.get_center() + DOWN * 0.1) for c in chips[1:]]))

        # S02.6  narrow to chip 1
        self.say("And everything we learned about scheduling assumed exactly one CPU.",
                 spot.animate.move_beam_to(chips[0].get_center() + DOWN * 0.1),
                 FadeOut(qs),
                 VGroup(*chips[1:]).animate.set_opacity(0.5))
        self.beat(0.6)

        # S02.7  aside
        card = aside_card("advanced chapter: leans on concurrency (later in the series)", title="ASIDE",
                          width=3.8, font_size=22).move_to(P3(4.4, -0.2))
        self.say("Quick note. The book calls this an advanced chapter. It leans on ideas from concurrency, "
                 "which we haven't fully covered yet.",
                 FadeOut(spot), card.slide_in(RIGHT), prof.change("neutral"))
        # S02.8
        ep = ep_tag("→ Ep. 26-28").next_to(card, DOWN, buff=0.15)
        self.say("So we'll sketch those parts, and promise to come back to them later.",
                 FadeIn(ep, shift=UP * 0.1), Succession(Wait(2.8), AnimationGroup(card.slide_out(RIGHT), FadeOut(ep))))
