import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


class S07Wait(Ep05Scene):
    def construct(self):
        self.add_badge()
        strip = crux_strip()
        self.add(strip)
        self.add_docked_term("non-deterministic")
        stu, prof = self.add_corner_chars("frustrated", "worried")
        par = proc(PAR, "ready", scale=0.55, label=f"PID {PID_P}").move_to(P3(-4.6, 1.75))
        chi = proc(CHI, "ready", scale=0.55, label=f"PID {PID_C}").move_to(P3(-3.3, 1.75))
        self.add(par, chi)

        tl = Timeline(["parent", "child"], ticks=6, colors=[PAR, CHI], x_range=(-4.5, 2.5), top=0.5,
                      row_height=0.4, row_step=0.6, cpu_row=True, tick_labels=False, label_font=22)
        sd = StateDiagram(running_icon=CPU(size=0.75, label=None, pins=3), font_size=30, arrow_font=24)
        sd.set_legend((4.8, 1.8), 0.45)
        dp = sd.make_dot(PAR, label="P", radius=0.13)
        dc = sd.make_dot(CHI, label="C", radius=0.13)
        sd.place_dot(dp, "ready").place_dot(dc, "ready")
        mt = mk_term(5.6, 2, 16).move_to(P3(0, -2.4))

        # S07.1
        with self.narrate("Sometimes order matters. Suppose the parent wants to know that its child has "
                          "finished before it continues."):
            # the diagram and code live in the top band, so the crux strip steps out until the end
            self.play(Create(tl), FadeIn(sd), FadeOut(strip), run_time=1.5)
            self.play(stu.change("curious", look_at=tl), run_time=0.6)
            self.wait(2.0)

        # S07.2
        code = CodeWalker("int rc_wait = wait(NULL);", font_size=18).move_to(P3(-4.0, 2.6))
        with self.narrate("For that, there's wait()."):
            self.play(self.terms.note("wait()"), FadeIn(code, shift=RIGHT * 0.2))

        # S07.3a
        with self.narrate("The parent calls it, and from then on it can't move forward until one of its "
                          "children finishes. So the OS doesn't let it hold the CPU. It blocks the parent, "
                          "our old blocked state, and the CPU is free for the child."):
            self.play(Indicate(code, scale_factor=1.1, color=CPU_COLOR), run_time=1.0)
            self.wait(1.2)
            self.play(Indicate(par, scale_factor=1.15), run_time=1.0)
            self.wait(1.0)
            self.play(sd.glow_zone("blocked"))
            self.wait(1.2)
            self.play(sd.unglow_zone("blocked"), Indicate(chi, scale_factor=1.15), run_time=0.8)
            self.wait(0.5)

        # S07.3b
        zomb = zombie_mini(0.55, label="child").move_to(chi)
        self.say("Let's watch it, one step at a time. First, the parent runs, and calls wait().",
                 par.change("running"), sd.move_dot(dp, "running"), tl.fill("parent", 1, "running"),
                 tl.fill("child", 1, "ready"), tl.fill_cpu(1), min_time=4.5)
        self.beat(0.8)

        # S07.3c
        self.say("Right away, the parent is blocked. The child moves from ready to running, and gets the CPU.",
                 par.change("blocked"), sd.move_dot(dp, "blocked"), tl.fill("parent", 2, "blocked"),
                 chi.change("running"), sd.move_dot(dc, "running"), tl.fill("child", 2, "running"),
                 tl.fill_cpu(2), min_time=5.5)
        self.beat(0.8)

        # S07.3d
        self.say("The child keeps running, while the parent just waits.",
                 tl.fill("parent", 3, "blocked"), tl.fill("child", 3, "running"), tl.fill_cpu(3),
                 min_time=4.0)
        self.beat(0.8)

        # S07.3e
        self.say("Then the child exits.", Transform(chi, zomb), sd.move_dot(dc, "ready"), min_time=2.0)
        self.beat(0.6)

        # S07.4
        ret = tagged("returns 29147", CHI, 20, CHI).move_to(chi.get_center() + DOWN * 0.1)
        with self.narrate("Now wait() returns in the parent, and rc_wait holds the PID of the child that "
                          "finished. The parent goes from blocked, to ready, to running again."):
            self.play(FadeOut(chi), FadeIn(ret), run_time=0.6)
            self.wait(0.6)
            self.play(ret.animate.move_to(par.get_center() + RIGHT * 1.9), run_time=1.0)
            self.wait(0.8)
            self.play(par.change("ready"), sd.move_dot(dp, "ready"), run_time=0.8)
            self.wait(0.6)
            self.play(par.change("running"), sd.move_dot(dp, "running"), run_time=0.8)
            self.wait(0.6)
            self.play(FadeOut(ret), tl.clear_blocks(), run_time=0.7)
            self.wait(0.5)
        tl.purge()
        self.play(par.change("ready"), sd.move_dot(dp, "ready"), run_time=0.4)

        # S07.5
        ring = progress_ring(0.3, CPU_COLOR, 0.0).move_to(P3(0, -1.35))
        prog = ValueTracker(0.0)
        ring.add_updater(lambda m: m[1].become(
            Arc(radius=0.3, start_angle=PI / 2, angle=-TAU * max(prog.get_value(), 1e-3),
                arc_center=m[0].get_center()).set_stroke(CPU_COLOR, 5)))
        yt = Text("your turn", font_size=20, color=DIM).next_to(ring, RIGHT, buff=0.2)
        with self.narrate("Add one wait() to the parent's branch, and the output becomes deterministic. "
                          "Can you see why? Pause the video and think about it."):
            self.play(prof.change("thinking"), FadeIn(ring), FadeIn(yt), run_time=0.8)
            self.wait(2.5)
            self.play(prog.animate.set_value(1.0), run_time=3.0, rate_func=linear)
            ring.clear_updaters()
            self.play(FadeOut(ring), FadeOut(yt), run_time=0.4)

        # S07.6
        case1 = Text("case 1", font_size=26, color=CPU_COLOR, weight="BOLD").move_to(P3(-1.0, 1.55))
        z2 = zombie_mini(0.35).move_to(tl.cell_center("child", 3) + UP * 0.0)
        self.say("Here's the answer. Remember, after fork() it's the scheduler that decides who runs first, "
                 "the parent or the child, and we can't predict it. So there are two cases, and wait() "
                 "has to handle both.", prof.change("explaining"), sd.glow_zone("ready"))
        self.play(sd.unglow_zone("ready"), run_time=0.4)
        with self.narrate("Case one: the child happens to run first. It prints and exits, and when the parent "
                          "finally runs, wait() returns immediately."):
            self.play(FadeIn(case1), run_time=0.4)
            self.play(tl.fill("parent", 1, "ready"), tl.fill("child", 1, "running"), tl.fill_cpu(1))
            self.play(tl.fill("parent", 2, "ready"), tl.fill("child", 2, "running"), tl.fill_cpu(2),
                      FadeIn(mt), mt.type("./p1"))
            self.play(FadeIn(z2), mt.print("child (pid:29147)"))
            r1 = tagged("returns at once", PAR, 18, PAR).move_to(tl.cell_center("parent", 3) + UP * 0.55)
            self.play(tl.fill("parent", 3, "running"), tl.fill_cpu(3), FadeIn(r1))
            self.play(mt.print("parent of 29147 (rc_wait:29147)"))
            self.wait(0.8)

        # S07.7
        case2 = Text("case 2", font_size=26, color=CPU_COLOR, weight="BOLD").move_to(P3(-1.0, 1.55))
        wtag = mono("wait()", 18, PAR).move_to(tl.cell_center("parent", 1) + UP * 0.55)
        with self.narrate("Case two: the parent runs first. It calls wait() right away, blocks, and the CPU goes to the child."):
            self.play(tl.unfill_ticks([1, 2, 3], run_time=1.0), FadeOut(z2), FadeOut(r1), mt.clear(),
                      Transform(case1, case2))
            tl.purge()
            self.play(tl.fill("parent", 1, "running"), tl.fill("child", 1, "ready"), tl.fill_cpu(1), FadeIn(wtag))
            self.play(tl.fill("parent", 2, "blocked"), tl.fill("child", 2, "running"), tl.fill_cpu(2))
            self.play(tl.fill("parent", 3, "blocked"), tl.fill("child", 3, "running"), tl.fill_cpu(3))
            self.play(mt.print("child (pid:29147)"))

        # S07.8
        cap = Text("child always first", font_size=24, color=CPU_COLOR).move_to(P3(0.6, -1.42))
        with self.narrate("Only once the child has exited does the parent wake up. Either way, the child prints first."):
            self.play(tl.fill("parent", 4, "ready"), tl.fill("child", 4, "ready"), tl.fill_cpu(4, "busy"))
            self.play(tl.fill("parent", 5, "running"), tl.fill_cpu(5))
            self.play(mt.print("parent of 29147 (rc_wait:29147)"))
            tk = tick_mark(0.3).next_to(cap, LEFT, buff=0.15)
            self.play(FadeIn(cap), FadeIn(tk))

        # S07.9
        z3 = zombie_mini(0.35).move_to(tl.cell_center("child", 4))
        self.add(z3)
        with self.narrate("And the exited child waits for its parent in the zombie state!"):
            self.play(stu.change("excited"), Indicate(z3, scale_factor=1.5), run_time=0.9)
            self.play(Indicate(z3, scale_factor=1.5), run_time=0.8)

        # S07.10
        wp = mono("waitpid()", 20, DIM).next_to(code, RIGHT, buff=0.3)
        with self.narrate("The zombie finally has a job. There's a sibling call, waitpid(), with more control, "
                          "and rare cases where wait() returns early. But for us, this is the rule."):
            self.play(prof.change("happy"), Write(wp), run_time=0.8)
            self.wait(3.0)
            self.play(FadeOut(wp), run_time=0.4)
        self.fade_stage(stu, prof, self.badge)
        self.play(FadeIn(strip), run_time=0.6)
