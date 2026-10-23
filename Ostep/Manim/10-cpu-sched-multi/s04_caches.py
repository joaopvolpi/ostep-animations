import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common_more import *  # noqa: E402,F401,F403


class S04Caches(Ep10Scene):
    def construct(self):
        self.world(strip=1, stu="curious", prof="neutral")
        stu, prof = self.stu, self.prof
        cc = cpu_at(S04_X, S04_CHIP_Y, "CPU")
        cache_parts = VGroup(cc.link, cc.strip, cc.cache_label, *cc.cells, *cc.texts)
        a = proc("A", "running", 0.5)

        # S04.1
        place_on(a, cc.cpu.slot_point())
        self.say("Here is the single CPU we've been using all along.",
                 GrowFromCenter(cc.cpu), Succession(Wait(0.6), FadeIn(a, shift=DOWN * 0.3)), stu.look_at(cc.cpu))

        # S04.2
        with self.narrate("And now, a detail we've been hiding: the cache."):
            self.play(FadeIn(cache_parts, shift=DOWN * 0.3), stu.look_at(cc.strip), run_time=0.8)
            self.play(self.note("hardware cache"))

        # S04.3
        mem = make_main_memory(S04_X)
        slow = VGroup(stopwatch_icon(radius=0.28), mono("~100 ns", 26, KERNEL_COLOR)).arrange(RIGHT, buff=0.2)
        slow.move_to(P3(3.4, READ_MEM_Y))
        trail = DashedLine(cc.cache_bottom(), mem.get_top(), dash_length=0.12).set_stroke(DIM, 3)
        self.say("Main memory holds all the data, but it's slow. Tens of nanoseconds, maybe hundreds.",
                 FadeIn(mem, shift=UP * 0.3), Succession(Wait(0.8), Create(trail)),
                 Succession(Wait(1.4), FadeIn(slow, shift=LEFT * 0.3)))

        # S04.4
        sf = label("small · fast", 22, MEM_COLOR).next_to(cc.strip, RIGHT, buff=0.3)
        self.say("So the CPU keeps a small, fast memory right next to it. It holds copies of popular data.",
                 cc.pulse(), FadeIn(sf, shift=LEFT * 0.2))

        # S04.5
        desk = desk_icon(1.0).next_to(cc.strip, LEFT, buff=0.5)
        lib = library_icon(1.4).next_to(mem, LEFT, buff=0.5)
        self.say("Think of the books on your desk versus the ones in the library across town.",
                 Succession(FadeIn(desk, shift=RIGHT * 0.3), Wait(1.4), FadeOut(desk)),
                 Succession(Wait(2.4), FadeIn(lib, shift=RIGHT * 0.3), Wait(1.4), FadeOut(lib)), FadeOut(sf))

        # S04.6  first load: miss
        dot = Dot(cc.cpu.get_center(), radius=0.1, color=TEXT)
        miss = x_mark(0.3).move_to(cc.strip.get_center() + RIGHT * 1.2)
        self.add(dot)
        with self.narrate("The first time the program loads a value, the CPU has to go all the way to memory."):
            self.play(dot.animate.move_to(cc.strip.get_center()), run_time=0.7)
            self.play(FadeIn(miss, scale=1.5), run_time=0.3)
            self.play(dot.animate.move_to(mem.cell(0).get_center()), FadeOut(miss), run_time=1.6)
            self.play(Indicate(slow, color=KERNEL_COLOR, scale_factor=1.15), run_time=0.9)

        # S04.7
        val = VGroup(Square(0.3).set_fill(COL["A"], 0.9).set_stroke(outline_of(COL["A"]), 2), mono("7", 18, INK))
        val[1].move_to(val[0])
        val.move_to(mem.cell(0).get_center())
        self.say("It copies the value into the cache on the way back.",
                 FadeOut(dot, run_time=0.2),
                 Succession(FadeIn(val, run_time=0.2), val.animate.move_to(cc.cell_point(0)),
                            AnimationGroup(FadeOut(val, run_time=0.2), cc.store("7", COL["A"], run_time=0.4))))

        # S04.8  second load: hit
        dot2 = Dot(cc.cpu.get_center(), radius=0.1, color=TEXT)
        hit = tick_mark(0.3).move_to(cc.strip.get_center() + RIGHT * 1.2)
        fast = VGroup(stopwatch_icon(radius=0.28), mono("~few ns", 26, CPU_COLOR)).arrange(RIGHT, buff=0.2)
        fast.move_to(P3(3.4, READ_CACHE_Y))
        self.add(dot2)
        self.say("The next time, it finds the value in the cache, and gets it in just a few nanoseconds.",
                 dot2.animate.move_to(cc.strip.get_center()),
                 Succession(Wait(0.8), AnimationGroup(FadeIn(hit, scale=1.5), FadeIn(fast, shift=LEFT * 0.3))),
                 Succession(Wait(1.6), Indicate(fast, color=CPU_COLOR, scale_factor=1.15)))
        self.play(FadeOut(dot2), FadeOut(hit), run_time=0.3)

        # S04.9
        r_mem, r_cache = readout_group("mem").move_to(slow), readout_group("cache").move_to(fast)
        self.say("The large slow memory suddenly looks like a fast one.",
                 Transform(slow, r_mem), Transform(fast, r_cache), stu.look_at(cc.strip))
        self.beat(0.6)
