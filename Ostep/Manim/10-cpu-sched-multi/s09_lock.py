import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from race import *  # noqa: E402,F401,F403


class S09Lock(Ep10Scene):
    def construct(self):
        self.world(strip=1, term="bus snooping", stu="frustrated", prof="happy")
        stu, prof = self.stu, self.prof
        st = build_race_stage()
        code, nodes, null, arrows, hv, chips, threads = (st[k] for k in ("code", "nodes", "null", "arrows", "hv", "chips", "threads"))
        # state at the end of S08: head moved on, node 5 gone, double free label
        hv.next_to(nodes[1], UP, buff=0.05)
        boom = label("double free!", 40, KERNEL_COLOR).move_to(P3(3.0, -2.5))
        comp = Computer("error").scale(0.55).move_to(P3(-1.5, -2.2))
        self.add(code, nodes[1], nodes[2], null, arrows[1], arrows[2], hv, *chips, *threads, boom, comp)

        # S09.1
        pad = Padlock(0.6, opened=True).move_to(P3(-0.45, 0.3))
        code2 = CodeWalker(POP_LOCK_SRC, font_size=20)
        code2.code.move_to(code.code)
        for m in (code2.code,):
            m.align_to(code.code, UP)
        self.say("The solution, as you may remember from the first episodes, is mutual exclusion: "
                 "wrap the routine in a lock.",
                 FadeOut(boom), FadeOut(comp), FadeIn(nodes[0]), FadeIn(arrows[0]),
                 hv.animate.next_to(nodes[0], UP, buff=0.05),
                 FadeOut(code.code), FadeIn(code2.code), self.note("lock"),
                 Succession(Wait(1.5), FadeIn(pad, scale=0.5)), stu.change("neutral"), prof.change("explaining"))

        old_code, code = code, code2

        # S09.2
        tmp1, tmp2 = tmp_chip(TC[0]).move_to(P3(CHIP_XS[0], 0.25)), tmp_chip(TC[1]).move_to(P3(CHIP_XS[1], 0.25))
        clock = mini_clock(0.16).next_to(threads[1], RIGHT, buff=0.15).shift(UP * 0.3)
        glow = SurroundingRectangle(code.code, color=KERNEL_COLOR, buff=0.08, stroke_width=4)
        b1 = code.add_bar(TC[0], 3)
        b2 = code.add_bar(TC[1], 3)
        b2.set_opacity(0)
        with self.narrate("Lock at the top, unlock at the end, and only one CPU at a time is inside."):
            self.play(pad.close(), Create(glow), FadeIn(b1), FadeIn(tmp1), FadeIn(clock), run_time=0.8)
            self.play(code.move_bar(0, 5), FadeOut(nodes[0], scale=1.5), FadeOut(arrows[0]),
                      hv.animate.next_to(nodes[1], UP, buff=0.05), run_time=0.8)
            self.play(code.move_bar(0, 7), run_time=0.5)
            self.play(pad.open(), FadeOut(glow), FadeOut(b1), FadeOut(tmp1), FadeOut(clock), run_time=0.7)
            self.play(pad.close(), Create(glow), b2.animate.set_opacity(0.25), FadeIn(tmp2), run_time=0.7)
            self.play(code.move_bar(1, 5), FadeOut(nodes[1], scale=1.5), FadeOut(arrows[1]),
                      hv.animate.next_to(nodes[2], UP, buff=0.05), run_time=0.8)
            self.play(pad.open(), FadeOut(glow), FadeOut(b2), FadeOut(tmp2), run_time=0.6)
            ok = tick_mark(0.5).move_to(P3(-0.45, 1.3))
            self.play(FadeIn(ok, scale=1.5), run_time=0.4)
            self.play(FadeOut(ok), run_time=0.3)

        # S09.3
        ep = ep_tag("→ Ep. 26-28").next_to(pad, DOWN, buff=0.25)
        self.say("We won't get into the details here. They're the subject of the whole concurrency section.",
                 FadeIn(ep, shift=UP * 0.1))

        # S09.4
        sw = stopwatch("", 20, radius=0.3).next_to(pad, UP, buff=0.35)
        self.say("But hold on to one fact: locks have a cost.",
                 FadeOut(ep), FadeIn(sw, scale=0.6), pad.pulse(), prof.change("neutral"))

        # S09.5
        row = VGroup()
        for i in range(8):
            ch = CPU(size=0.4, label=None, pins=2).move_to(P3(-3.4 + 0.7 * i, -2.5))
            th = Process("ready", color=COL["A"], label=None).scale(0.22)
            place_on(th, ch.slot_point())
            ck = mini_clock(0.1).next_to(ch, DOWN, buff=0.08)
            row.add(VGroup(ch, th, ck))
        wait_t = label("waiting…", 22, KERNEL_COLOR).next_to(sw, RIGHT, buff=0.15)
        self.say("As the number of CPUs grows, accessing a shared, locked data structure gets slow.",
                 pad.close(), FadeIn(wait_t),
                 Succession(Wait(0.5), LaggedStart(*[FadeIn(r, shift=LEFT * 0.4) for r in row], lag_ratio=0.35)),
                 stu.change("frustrated"))

        # S09.6
        card = aside_card("lock-free structures: complex, rare", title="ASIDE", width=3.8, font_size=22).move_to(P3(4.6, 2.0))
        self.say("There are also lock-free structures that avoid locks, but they are complicated, and used only on occasion.",
                 Succession(card.slide_in(RIGHT), Wait(2.5), card.slide_out(RIGHT)), stu.change("neutral"))

        # transition: everything but the padlock fades; it shrinks to the corner
        rest = VGroup(code.code, nodes[2], null, arrows[2], hv, *chips, *threads, sw, wait_t, row)
        self.play(FadeOut(rest), pad.animate.scale(0.7).move_to(P3(6.2, 2.1)), run_time=1.0)
