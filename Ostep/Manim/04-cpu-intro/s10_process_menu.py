import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


class S10ProcessMenu(Ep04Scene):
    def construct(self):
        self.add_badge()
        self.add_docked_term("stack pointer & frame pointer")
        stu, prof = self.add_corner_chars("excited", "happy")
        w = build_s09_end()
        cpu, a, panels, slot = w["cpu"], w["a"], w["panels"], w["slot"]
        self.add(panels, cpu, a, slot)

        # S10.1
        menu = MenuCard("Process API", ["Create", "Destroy", "Wait", "Misc. control", "Status"],
                        width=4.0, height=4.4, font_size=28)
        menu.move_to(P3(-3.6, 0.35))
        tag = ep_tag("→ Ep. 05").scale(0.85).next_to(menu.card, RIGHT, buff=0.2, aligned_edge=UP).shift(DOWN * 0.1)
        glow = Circle(radius=0.6).set_fill(COL["A"], 0.4).set_stroke(width=0).move_to(a)
        world = VGroup(cpu, a)
        with self.narrate("Now that we know what a process is, what can the OS actually do with one?"):
            self.play(Transform(panels, glow), stu.change("neutral"), prof.change("neutral"), run_time=1.2)
            self.play(FadeOut(panels), world.animate.shift(S10_CPU - cpu.get_center()), run_time=1.0)
        with self.narrate("It turns out to be a short menu of actions. We'll meet the real API in the next "
                          "episode, but any operating system offers something like this."):
            self.play(FadeIn(menu, shift=RIGHT * 0.3), FadeIn(tag), run_time=0.8)

        hl = [None]

        def pick(i):
            new = menu.row_highlight(i)
            if hl[0] is None:
                hl[0] = new
                return FadeIn(new)
            return Transform(hl[0], new)

        # S10.2 create
        icon = browser_icon(0.5).move_to(P3(4.3, 2.0))
        cursor = cursor_icon(0.35).move_to(icon.get_center() + P3(0.6, -0.5))
        b = proc("B").move_to(S10_SIDE)
        with self.narrate("Create: you double-click an icon or type a command, and a new process is born."):
            self.play(pick(0), FadeIn(icon), FadeIn(cursor), run_time=0.6)
            self.play(cursor.animate.move_to(icon.get_center() + P3(0.12, -0.15)), run_time=0.5)
            for _ in range(2):
                self.play(cursor.animate(rate_func=there_and_back).scale(0.8), run_time=0.2)
            self.play(GrowFromPoint(b, icon.get_center()), FadeOut(cursor), run_time=0.7)
            self.play(b.animate(rate_func=there_and_back).shift(UP * 0.2), run_time=0.4)

        # S10.3 destroy
        x = cross_mark(0.45, KERNEL_COLOR, 9).move_to(b)
        poof = puff(0.55).move_to(b)
        with self.narrate("Destroy: most processes exit on their own, but a runaway one can be killed."):
            self.play(pick(1), FadeOut(icon), run_time=0.5)
            self.play(Rotate(b, TAU * 2, run_time=1.0, rate_func=smooth))
            self.play(FadeIn(x, scale=2.0), run_time=0.3)
            self.play(FadeOut(b, scale=0.1), FadeOut(x), FadeIn(poof, scale=0.3), run_time=0.5)
            self.play(FadeOut(poof, scale=1.6), run_time=0.4)

        # S10.4 wait
        c = proc("C", "running").move_to(S10_SIDE)
        ring = progress_ring(0.28, CPU_COLOR, 0.0).next_to(c, UP, buff=0.15)
        prog = ValueTracker(0.0)
        ring.add_updater(lambda m: m[1].become(
            Arc(radius=0.28, start_angle=PI / 2, angle=-TAU * max(prog.get_value(), 1e-3),
                arc_center=m[0].get_center()).set_stroke(CPU_COLOR, 5)))
        with self.narrate("Wait: pause until some process finishes."):
            self.play(pick(2), GrowFromCenter(c), FadeIn(ring), a.change("blocked"), run_time=0.7)
            self.play(prog.animate.set_value(1.0), run_time=1.6, rate_func=linear)
            ring.clear_updaters()
            self.play(a.change("ready"), FadeOut(ring), run_time=0.5)

        # S10.5 misc control
        pz = PauseGlyph(0.35).move_to(c.get_center() + UP * 0.1)
        pl = PlayGlyph(0.35).move_to(pz)
        with self.narrate("Miscellaneous control: for example, suspend a process for a while, then resume it."):
            self.play(pick(3), run_time=0.4)
            self.play(FadeIn(pz, scale=1.4), c.animate.set_opacity(0.4), run_time=0.5)
            self.wait(0.8)
            self.play(ReplacementTransform(pz, pl), c.animate.set_opacity(1.0), run_time=0.5)
            self.play(FadeOut(pl), run_time=0.4)

        # S10.6 status
        info = info_tag("running · 3.2 s", font_size=22).next_to(a, UP, buff=0.2)
        with self.narrate("And status: how long has it run, and what state is it in?"):
            self.play(pick(4), a.change("running"), run_time=0.5)
            self.play(GrowFromPoint(info, a.get_top()), run_time=0.6)

        # S10.7
        self.say("That's… a menu.", stu.change("bored", look_at=menu), min_time=1.5)

        # S10.8
        with self.narrate("A very powerful menu. Next episode, we order from it."):
            self.play(prof.change("happy", look_at=menu), run_time=0.6)
            self.play(Wiggle(VGroup(menu, tag, hl[0]), scale_value=1.04, rotation_angle=0.05, n_wiggles=4), run_time=1.0)
        self.beat(0.6)

        # transition: menu and C fade
        self.play(FadeOut(VGroup(menu, tag, hl[0], info)), FadeOut(c), stu.change("neutral"), run_time=0.8)
