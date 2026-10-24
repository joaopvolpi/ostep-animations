import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from manim import *  # noqa: E402,F403
from ostep_lib import *  # noqa: E402,F403
from common import *  # noqa: E402,F403


class S02ThreePieces(NarratedScene):
    def construct(self):
        stu, prof = make_hosts("dialog", stu_expr="excited", prof_expr="happy")
        title, credit = make_title()
        self.add(stu, prof, title, credit)

        # S02.1
        small = small_title(title)
        self.say("First question: why three easy pieces?",
                 Succession(AnimationGroup(Transform(title, small), FadeOut(credit), stu.change("curious"),
                                           run_time=0.9),
                            Indicate(title[1], color=INTRO, run_time=0.9)))

        # S02.2
        six = book_icon("Six Easy", "Pieces", color="#6FA8F7").move_to([-1.2, 1.4, 0])
        six_lab = Text("Six Easy Pieces · Feynman", font_size=24, color=TEXT).next_to(six, DOWN, buff=0.15)
        six_g = VGroup(six, six_lab)
        self.say("Richard Feynman gave famous lectures on physics, and some of the basics were collected "
                 "in a book called Six Easy Pieces.",
                 prof.change("explaining"), FadeIn(six_g, shift=UP * 0.2, run_time=0.8))

        # S02.3
        three = book_icon("Three Easy", "Pieces", color=VIRT).move_to([1.6, 1.4, 0])
        three_lab = Text("Three Easy Pieces · OS", font_size=24, color=TEXT).next_to(three, DOWN, buff=0.15)
        three_g = VGroup(three, three_lab)
        self.say("We're doing three easy pieces on operating systems.",
                 six_g.animate.shift(LEFT * 1.6).set_opacity(0.4),
                 FadeIn(three_g, shift=LEFT * 0.3))

        # S02.4
        with self.narrate("Which is fitting, since operating systems are about half as hard as physics."):
            self.play(Indicate(three_g, color=VIRT, scale_factor=1.08), run_time=1.0)
            self.wait(2.0)
            self.play(FadeOut(six_g), FadeOut(three_g), run_time=0.6)

        # S02.5
        self.say("So what are the pieces?", stu.change("curious"), prof.change("neutral"), min_time=1.4)

        cards = piece_cards(with_icons=False)
        # S02.6-8
        self.say("Virtualization.", GrowFromCenter(cards[0], run_time=0.6), min_time=1.1)
        self.say("Concurrency.", GrowFromCenter(cards[1], run_time=0.6), min_time=1.1)
        self.say("Persistence. Learn those three ideas, and you learn how an operating system works.",
                 GrowFromCenter(cards[2], run_time=0.6), prof.change("proud"))

        # S02.9
        cpu_i = mini_cpu_icon().move_to(icon_slot(cards[0], 0, 2))
        proc = cpu_i[1]
        with self.narrate("How it decides what program runs next on a CPU."):
            self.play(FadeIn(cpu_i, scale=0.4), run_time=0.5)
            top = cpu_i[0].slot_point()
            for dx in (0.25, 0.0):
                self.play(hop_to(proc, top + RIGHT * dx, run_time=0.4))
        # S02.10
        mem_i = mini_mem_icon().move_to(icon_slot(cards[0], 1, 2))
        self.say("How it copes when memory overflows.",
                 Succession(FadeIn(mem_i[0], scale=0.4, run_time=0.4),
                            LaggedStart(*[FadeIn(s, shift=UP * 0.15) for s in mem_i[1]], lag_ratio=0.5,
                                        run_time=0.6)))
        # S02.11 concurrency
        conc_i = mini_conc_icon().move_to(icon_slot(cards[1]))
        self.say("How it keeps many things happening at once from tripping over each other.",
                 FadeIn(conc_i[0], scale=0.4, run_time=0.5), FadeIn(conc_i[2], scale=0.4, run_time=0.5),
                 late(0.5, Create(conc_i[1], run_time=0.5)))
        # S02.12
        disk_i = mini_disk_icon().move_to(icon_slot(cards[2]))
        self.say("And how it stores information on disks.", FadeIn(disk_i, scale=0.4, run_time=0.5),
                 disk_i.spin(1, run_time=1.0))
        cards[0].icons.add(cpu_i, mem_i)
        cards[1].icons.add(conc_i)
        cards[2].icons.add(disk_i)

        # S02.13
        q = question_mark(0.8, CPU_COLOR).move_to([0, 2.45, 0])
        self.say("I have no idea what you're talking about, really.",
                 stu.change("confused"), FadeIn(q, scale=0.4))
        # S02.14
        self.say("Good! That means you're in the right place.",
                 prof.change("happy"), FadeOut(q, scale=1.6))
        self.beat(0.6)
