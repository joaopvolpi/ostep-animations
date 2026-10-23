import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common_more import *  # noqa: E402,F401,F403

class S06Stale(Ep10Scene):
    def construct(self):
        self.world(strip=1, term="locality", stu="neutral", prof="neutral")
        stu, prof = self.stu, self.prof
        c1, c2, mem, bus, bus_lab = two_cpu_stage()
        # starting state: one CPU with an empty cache top-center (end of S05)
        start = cpu_at(0, 1.75, "CPU")
        start.scale(0.6, about_point=start.cpu.get_center())
        self.add(start)

        # S06.1
        tgt = c1.copy()
        self.say("Now the tricky part. Add a second CPU.",
                 Transform(start, tgt), Succession(Wait(0.6), GrowFromCenter(c2)))
        self.remove(start)
        self.add(c1)

        # S06.2
        self.say("Each CPU has its own cache, and both share one main memory, connected by a bus.",
                 FadeIn(mem, shift=UP * 0.3), Succession(Wait(0.8), Create(bus), FadeIn(bus_lab)),
                 self.note("bus"))

        # S06.3
        self.say("Memory holds a value at some address.",
                 Circumscribe(mem.cell(0), color=CPU_COLOR, run_time=1.5), Indicate(mem.texts[0], color=TEXT, scale_factor=1.4))

        # S06.4
        a = proc("A", "ready", 0.5)
        place_on(a, c1.slot_point() + LEFT * 1.6)
        self.add(a)
        dot = Dot(c1.cpu.get_center(), radius=0.1, color=TEXT)
        self.add(dot)
        self.say("The program, on CPU one, reads it.",
                 hop_to(a, c1.slot_point(), run_time=0.7),
                 Succession(Wait(0.9), dot.animate.move_to(c1.cache_bottom())))
        self.play(a.change("running"), run_time=0.4)
        # S06.5
        miss = x_mark(0.28).move_to(c1.strip.get_right() + RIGHT * 0.35)
        path = bus.path(c1.cache_bottom(), mem.get_top())
        back = bus.path(mem.get_top(), c1.cache_bottom())
        val = VGroup(Square(0.3).set_fill(COL["A"], 0.9).set_stroke(outline_of(COL["A"]), 2), mono("7", 18, INK))
        val[1].move_to(val[0])
        val.move_to(mem.get_top())
        with self.narrate("It's not in CPU one's cache, so it's fetched from memory: the value is seven."):
            self.play(FadeIn(miss, scale=1.4), run_time=0.3)
            self.play(MoveAlongPath(dot, path), FadeOut(miss), run_time=1.3)
            self.play(FadeOut(dot, run_time=0.1), FadeIn(val, run_time=0.1))
            self.play(MoveAlongPath(val, back), run_time=1.3)
            self.play(FadeOut(val, run_time=0.2), c1.store("7", COL["A"], run_time=0.4))

        # S06.6
        stale = DashedVMobject(Rectangle(width=1.3, height=0.5).move_to(mem.cell(0)).set_stroke(KERNEL_COLOR, 4))
        stale_t = label("stale!", 22, KERNEL_COLOR).next_to(mem.cell(0), RIGHT, buff=0.55)
        self.say("The program then changes it to nine.",
                 c1.set_value(0, "9", color=COL["A"]), Indicate(c1.cells[0], color=TEXT, scale_factor=1.3),
                 Succession(Wait(1.2), AnimationGroup(Create(stale), FadeIn(stale_t))))

        # S06.7
        wb = VGroup(mini_clock(0.14), label("write-back later", 20, DIM)).arrange(RIGHT, buff=0.12)
        wb.move_to(P3(-3.2, -1.5))
        dotted = DashedVMobject(path.copy().set_stroke(DIM, 3), num_dashes=30)
        self.say("But writing all the way back to slow main memory takes a while, so the system, usually, "
                 "just updates the cache and does the write to memory later.",
                 FadeIn(wb, shift=UP * 0.2), Succession(Wait(1.0), Create(dotted)))

        # S06.8
        self.say("Now the OS stops the program and moves it to CPU two.",
                 hop_to(a, c2.slot_point(), run_time=1.0, height=1.0))
        self.play(a.change("running"), run_time=0.4)

        # S06.9
        book = label("book: D → D'", 18, DIM).next_to(mem, DOWN, buff=0.12)
        self.say("The book's example calls the old value D and the new one D-prime.", FadeIn(book))

        # S06.10
        dot2 = Dot(c2.cpu.get_center(), radius=0.1, color=TEXT)
        miss2 = x_mark(0.28).move_to(c2.strip.get_left() + LEFT * 0.35)
        self.add(dot2)
        self.say("The program reads the same address again. CPU two's cache has nothing.",
                 dot2.animate.move_to(c2.strip.get_center()), Succession(Wait(1.0), FadeIn(miss2, scale=1.4)))

        # S06.11
        path2 = bus.path(c2.cache_bottom(), mem.get_top())
        back2 = bus.path(mem.get_top(), c2.cache_bottom())
        val2 = VGroup(Square(0.3).set_fill(COL["A"], 0.9).set_stroke(outline_of(COL["A"]), 2), mono("7", 18, INK))
        val2[1].move_to(val2[0])
        val2.move_to(mem.get_top())
        neq = MathTex(r"7\neq 9", color=KERNEL_COLOR).scale(1.8).move_to(P3(0, 1.3))
        with self.narrate("So it fetches from main memory, which still holds the old value. Seven. Not nine."):
            self.play(MoveAlongPath(dot2, bus.path(c2.cache_bottom(), mem.get_top())), FadeOut(miss2), run_time=1.3)
            self.play(FadeOut(dot2, run_time=0.1), FadeIn(val2, run_time=0.1))
            self.play(MoveAlongPath(val2, back2), run_time=1.3)
            self.play(FadeOut(val2, run_time=0.2), c2.store("7", COL["A"], run_time=0.4))
            self.play(FadeIn(neq, scale=0.6), a.says("7?", font_size=28, max_width=1.4), run_time=0.8)

        # S06.12
        comp = Computer("error").scale(0.6).move_to(P3(3.7, -2.4))
        self.say("The program just read stale data. The wrong answer, from the right address!",
                 stu.change("surprised"), FadeIn(comp, scale=0.7))

        # S06.13 key term
        self.play(prof.change("worried"), a.remove_bubble(), run_time=0.5)
        with self.narrate("This is the problem of cache coherence. Each cache has its own view of the "
                          "\"one\" shared memory, and the views disagree."):
            self.play(self.term("cache coherence"))

        # S06.14
        ctag = tag("→ computer architecture course", 20).move_to(P3(4.0, 2.2))
        books = VGroup(*[Rectangle(width=0.7 - 0.05 * i, height=0.16).set_fill(c, 1).set_stroke(INK, 1.5)
                         for i, c in enumerate(("#E06C75", "#61AFEF", "#98C379"))]).arrange(DOWN, buff=0.0)
        books.move_to(P3(4.0, 1.5))
        self.say("Research on it fills libraries. We'll skip the nuance, and take a computer architecture course for that.",
                 FadeIn(ctag, shift=LEFT * 0.2), Succession(Wait(0.6), FadeIn(books, shift=UP * 0.2), Wait(2.0), FadeOut(books)),
                 Succession(Wait(4.5), FadeOut(ctag)))
        self.beat(0.3)
