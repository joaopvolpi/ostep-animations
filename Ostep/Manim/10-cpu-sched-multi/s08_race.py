import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from race import *  # noqa: E402,F401,F403


class S08Race(Ep10Scene):
    def construct(self):
        self.world(strip=1, term="bus snooping", stu="excited", prof="happy")
        stu, prof = self.stu, self.prof
        w = build_s06_end()
        c1, c2, mem, bus, bus_lab = (w[k] for k in ("c1", "c2", "mem", "bus", "bus_lab"))
        cache_with(c1, 0, "9", COL["A"])
        cache_with(c2, 0, "9", COL["A"])
        hw = VGroup(c1, c2, mem, bus, bus_lab)
        okt = tick_mark(0.9).move_to(P3(0, 1.6))
        shade = scrim(0.25)
        self.add(hw, okt, shade)

        # S08.1
        same = label("same view", 22, GREEN_OK).move_to(P3(1.3, 1.6))
        hw_small = hw.copy().scale(0.55).move_to(P3(0, -0.7)).set_opacity(0.3)
        self.say("Coherent caches guarantee that every CPU sees the same memory.",
                 FadeOut(shade), Transform(hw, hw_small), FadeIn(same),
                 prof.change("neutral"), stu.change("neutral"))

        # S08.2
        order = label("order", 22, KERNEL_COLOR).move_to(same)
        qm = question_mark(0.8).move_to(okt)
        self.say("They don't guarantee that two CPUs will modify it in a sensible order.",
                 Transform(okt, qm), Transform(same, order))

        # S08.3
        st = build_race_stage()
        code, nodes, null, arrows, hv, chips, threads = (st[k] for k in ("code", "nodes", "null", "arrows", "hv", "chips", "threads"))
        small_tick = VGroup(tick_mark(0.35), label("coherent", 18, GREEN_OK).shift(DOWN * 0.8)).move_to(P3(6.0, 0.3))
        self.say("Here is a shared linked list, and the routine that removes the head from it.",
                 FadeOut(hw), FadeOut(okt), FadeOut(same), FadeIn(small_tick),
                 LaggedStart(*[Create(n) for n in nodes], FadeIn(null), Create(arrows), FadeIn(hv), lag_ratio=0.2),
                 Succession(Wait(0.8), FadeIn(code.code)),
                 Succession(Wait(1.5), AnimationGroup(*[FadeIn(c) for c in chips], *[FadeIn(t) for t in threads])))

        # S08.4
        bar1 = code.add_bar(COL["A"], 2)
        tmp1 = tmp_chip(COL["A"]).move_to(P3(CHIP_XS[0], 0.25))
        a_tmp1 = Arrow(tmp1.get_top(), nodes[0].get_bottom() + DOWN * 0.02, buff=0.05, stroke_width=3, color=COL["A"], tip_length=0.15)
        vbox = VGroup(RoundedRectangle(width=1.4, height=0.4, corner_radius=0.1).set_fill(CARD_FILL, 1).set_stroke(DIM, 2),
                      label("value", 16, DIM).shift(LEFT * 0.3), mono("5", 20)).move_to(P3(2.9, 0.2))
        vbox[2].move_to(vbox.get_center() + RIGHT * 0.35)
        self.say("Read the head into a temporary variable. Remember its value.",
                 FadeIn(bar1), FadeIn(tmp1, shift=UP * 0.2), Succession(Wait(0.8), Create(a_tmp1)),
                 Succession(Wait(1.8), AnimationGroup(code.move_bar(0, 3), FadeIn(vbox, shift=RIGHT * 0.2))))

        # S08.5
        puff_n = nodes[0]
        with self.narrate("Move the head forward. Free the old head. Return the value."):
            self.play(code.move_bar(0, 4), hv.animate.next_to(nodes[1], UP, buff=0.05), run_time=0.8)
            self.play(code.move_bar(0, 5), FadeOut(puff_n, scale=1.6), FadeOut(arrows[0]), FadeOut(a_tmp1), run_time=0.8)
            self.play(code.move_bar(0, 6), FadeOut(vbox, shift=RIGHT * 0.5), run_time=0.8)

        # S08.6 rewind
        bar2 = code.add_bar(COL["D"], 2)
        self.say("Now imagine threads on two CPUs both run the first line at the same time.",
                 FadeIn(nodes[0]), FadeIn(arrows[0]), hv.animate.next_to(nodes[0], UP, buff=0.05),
                 code.move_bar(0, 2), FadeIn(bar2), FadeOut(tmp1))

        # S08.7
        tmps = [tmp_chip(c).move_to(P3(x, 0.25)) for c, x in zip(TC, CHIP_XS)]
        tabs = [label("stack", 16, DIM).move_to(P3(x, -0.05)) for x in CHIP_XS]
        arr = [Arrow(t.get_top(), nodes[0].get_bottom() + DOWN * 0.02, buff=0.05, stroke_width=3, color=c, tip_length=0.15)
               for t, c in zip(tmps, TC)]
        self.say("Each has its own private temporary, because that lives on its own stack.",
                 *[FadeIn(t, shift=UP * 0.2) for t in tmps], *[FadeIn(t) for t in tabs],
                 Succession(Wait(1.0), AnimationGroup(*[Create(a) for a in arr])))

        # S08.8
        boom = label("double free!", 40, KERNEL_COLOR).move_to(P3(3.0, -2.5))
        comp = Computer("error").scale(0.55).move_to(P3(-1.5, -2.2))
        with self.narrate("Both point to the same head. So both remove the same element, both free it, "
                          "and the program frees memory twice."):
            self.play(code.move_bar(0, 4), code.move_bar(1, 4), hv.animate.next_to(nodes[1], UP, buff=0.05), run_time=0.8)
            self.play(code.move_bar(0, 5), code.move_bar(1, 5), FadeOut(nodes[0], scale=1.6), FadeOut(arrows[0]),
                      run_time=0.8)
            self.play(FadeIn(boom, scale=1.5), Flash(boom, color=KERNEL_COLOR, flash_radius=0.8), FadeIn(comp, scale=0.7),
                      stu.change("frustrated"), run_time=0.8)

        # S08.9
        cross = VGroup(Circle(radius=0.55).set_stroke(KERNEL_COLOR, 5),
                       Line(UL * 0.39, DR * 0.39).set_stroke(KERNEL_COLOR, 5)).move_to(small_tick[0])
        self.say("Even with perfect cache coherence.", Create(cross))
        self.beat(1.0)
