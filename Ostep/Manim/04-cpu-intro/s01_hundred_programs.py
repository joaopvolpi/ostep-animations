import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


class S01HundredPrograms(Ep04Scene):
    def construct(self):
        laptop = Laptop(width=5).move_to(P3(0, 0.3))
        icons = app_icons()
        for ic, p in zip(icons, APP_SPOTS):
            ic.move_to(p)
        src = laptop.screen_center()

        # S01.1
        self.say("Look at your computer right now.", Create(laptop, run_time=1.5))
        self.beat(0.6)

        # S01.2
        self.say("A web browser.", GrowFromPoint(icons[0], src, run_time=0.8))

        # S01.3
        notes = VGroup(*[eighth_note(0.16).move_to(APP_SPOTS[1] + P3(0.3 + 0.22 * k, 0.15 + 0.1 * k))
                         for k in range(3)])
        with self.narrate("Music playing."):
            self.play(GrowFromPoint(icons[1], src, run_time=0.7))
            self.play(LaggedStart(*[FadeIn(n, shift=UP * 0.4) for n in notes], lag_ratio=0.3, run_time=0.8))
            self.play(FadeOut(notes, shift=UP * 0.3, run_time=0.4))

        # S01.4
        self.say("A chat app, a game in the background, maybe a mail client.",
                 LaggedStart(*[GrowFromPoint(icons[i], src) for i in (2, 3, 4)],
                             lag_ratio=0.45, run_time=1.8))
        self.beat(0.8)

        # S01.5
        tm = TaskManager(width=laptop.screen.width * 0.92, height=laptop.screen.height * 0.9)
        tm.move_to(laptop.screen_center())
        counter, num, _ = counter_group(12)
        tm.start_scrolling(0.25)
        self.say("Open a task manager…", FadeIn(tm, shift=UP * 0.6, run_time=0.8),
                 FadeIn(counter, run_time=0.8), min_time=1.4)

        # S01.6
        speed = ValueTracker(0.25)
        tm.add_updater(lambda m: setattr(m, "speed", speed.get_value()))
        self.say("…and you'll find tens, maybe hundreds of programs…",
                 speed.animate(run_time=1.5).set_value(2.5),
                 ChangeDecimalToValue(num, 137, run_time=1.5), min_time=2.6)

        # S01.7
        self.say("…all running at the same time.",
                 LaggedStart(*[Indicate(ic, scale_factor=1.25, color=None) for ic in icons],
                             lag_ratio=0.1, run_time=1.2))
        self.beat(0.5)

        # S01.8
        stu = student_dialogue("curious", STUDENT_SIDE)
        stu.set_look(laptop)
        stu.shift(LEFT * 4)
        with self.narrate("Okay, sure. That's just… what computers do."):
            self.play(stu.animate(run_time=0.8).shift(RIGHT * 4))
            self.play(stu.animate(rate_func=there_and_back, run_time=0.5).shift(UP * 0.15))
            self.play(stu.blink())
        self.wait(0.5)
