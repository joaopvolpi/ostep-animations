import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common_more import *  # noqa: E402,F401,F403


class S05Locality(Ep10Scene):
    def construct(self):
        self.world(strip=1, term="hardware cache", stu="curious", prof="neutral")
        stu, prof = self.stu, self.prof
        w = build_s04_end()
        cc, mem, ro1, ro2 = w["cc"], w["mem"], w["ro1"], w["ro2"]
        self.add(cc, mem, ro1, ro2)

        # S05.1 : readouts shrink to the right, cpu + cache to top-center, memory away
        cache_target = P3(0, 1.75)
        ro = VGroup(ro1, ro2)
        self.play(
            ro.animate.scale(0.55).move_to(P3(5.2, 2.0)),
            FadeOut(mem),
            cc.animate.scale(0.6, about_point=cc.cpu.get_center()).shift(cache_target - cc.cpu.get_center()),
            run_time=1.2)
        for i in range(3):          # start with an empty cache for the demos
            cc.cells[i].set_fill(BG, 1).set_stroke(DIM, 1.5)
            cc.texts[i].become(Text("", font=MONO_FONT, font_size=10, color=TEXT).move_to(cc.cells[i]))
        cc.used = 0
        q = question_mark(0.45).next_to(cc.strip, RIGHT, buff=0.3)
        self.say("But the cache is tiny. How does it know what to keep?",
                 FadeIn(q, scale=0.5), stu.change("curious"))

        # S05.2 : panels
        left = MemoryStrip(n=8, cell_width=0.55, cell_height=0.5, show_addresses=False,
                           values=["", "", "", "", "", "", "", ""]).move_to(P3(-3.3, 0.0))
        right = MemoryStrip(n=8, cell_width=0.55, cell_height=0.5, show_addresses=False,
                            values=[str(i) for i in range(8)]).move_to(P3(3.3, 0.0))
        t_l = label("temporal", 26, DIM).move_to(P3(-3.3, -0.75))
        t_r = label("spatial", 26, DIM).move_to(P3(3.3, -0.75))
        self.say("It guesses, and the guess works because of locality.",
                 FadeOut(q), self.note("locality"),
                 Succession(Wait(0.4), AnimationGroup(Create(left), Create(right), FadeIn(t_l), FadeIn(t_r))))

        # S05.3 : temporal
        t_l2 = label("temporal locality", 26, TEXT).move_to(t_l)
        box = VGroup(RoundedRectangle(width=1.8, height=0.5, corner_radius=0.1).set_fill(CARD_FILL, 1).set_stroke(DIM, 2),
                     mono("for(i…)", 20)).move_to(P3(-3.3, -1.55))
        box[1].move_to(box[0])
        loop = loop_arrow(0.3, color=VIRT).next_to(box, RIGHT, buff=0.2)
        c0 = left.cells[2]
        with self.narrate("Temporal locality: data you just used is likely to be used again soon…"):
            self.play(Transform(t_l, t_l2), FadeIn(box, shift=UP * 0.2), FadeIn(loop), run_time=0.8)
            self.play(left.color_cell(2, COL["A"], 0.8), run_time=0.4)
            self.play(left.pulse(2), run_time=0.5)
            self.play(left.pulse(2), run_time=0.5)
            self.play(left.pulse(2), cc.store("", COL["A"], run_time=0.5), run_time=0.6)

        # S05.4
        lc = label("loop code", 20, DIM).next_to(left.cells[5], UP, buff=0.1)
        self.say("…like a loop counter, or the instructions of the loop itself.",
                 left.color_cell(5, COL["B"], 0.8), FadeIn(lc), cc.store("", COL["B"]))

        # S05.5 : spatial
        t_r2 = label("spatial locality", 26, TEXT).move_to(t_r)
        br = Brace(VGroup(*right.cells[3:6]), UP, buff=0.08, color=MEM_COLOR)
        with self.narrate("Spatial locality: if you touch address x, you will probably touch the neighbors soon…"):
            self.play(Transform(t_r, t_r2), right.color_cell(3, COL["C"], 0.8), run_time=0.7)
            self.play(GrowFromCenter(br), run_time=0.5)
            self.play(br.animate.move_to(cc.strip.get_bottom() + DOWN * 0.1).scale(0.5).set_opacity(0),
                      cc.warmth(3, MEM_COLOR), *[right.color_cell(i, COL["C"], 0.4) for i in (4, 5)], run_time=1.2)

        # S05.6 : cursor walks
        cur = cursor_icon(0.4).move_to(right.cells[3].get_center() + DOWN * 0.55)
        hit_marks = []
        walk = [cur.animate.move_to(right.cells[i].get_center() + DOWN * 0.55) for i in (4, 5)]
        self.add(cur)
        miss = x_mark(0.3).move_to(right.cells[6].get_center() + UP * 0.55)
        with self.narrate("…like a program walking through an array."):
            for i in (3, 4, 5):
                tk = tick_mark(0.25).move_to(right.cells[i].get_center() + UP * 0.55)
                self.play(cur.animate.move_to(right.cells[i].get_center() + DOWN * 0.55), FadeIn(tk, scale=1.4),
                          run_time=0.5)
                self.play(FadeOut(tk), run_time=0.15)
            self.play(cur.animate.move_to(right.cells[6].get_center() + DOWN * 0.55), FadeIn(miss, scale=1.4), run_time=0.5)
            self.play(right.color_cell(6, COL["C"], 0.8), FadeOut(miss), run_time=0.5)

        # S05.7
        self.say("Programs show both kinds all the time, so caches work well.",
                 left.pulse(2), right.pulse(4), FadeOut(cur), stu.change("neutral"))

        # S05.8
        pin = pin_icon(0.6).move_to(cc.strip.get_right() + RIGHT * 0.1 + UP * 0.1)
        self.say("Keep this in mind. It is the whole reason the rest of the episode matters.",
                 FadeIn(pin, shift=DOWN * 0.8),
                 VGroup(left, right, t_l, t_r, box, loop, lc).animate.set_opacity(0.35))
        self.beat(0.6)
