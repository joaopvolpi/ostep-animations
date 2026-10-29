import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


class S02Machinery(Ep11Scene):
    def construct(self):
        self.world(stu="neutral", prof="happy", mode="dlg")
        stu, prof = self.stu, self.prof
        prof.set_look(stu)      # as S01 ends: the Professor still looks at the Student
        panels = build_panels()
        L, M, R = panels.left, panels.mid, panels.right
        bd, p_user = L.bd, L.proc
        cpu, pa, clock = M.cpu, M.proc, M.clock
        slot, ra, rb = R.slot, R.pa, R.pb

        # S02.1
        glide = AnimationGroup(stu.animate.scale(CHAR_SCALE).move_to(STUDENT_CORNER),
                               prof.animate.scale(CHAR_SCALE).move_to(PROF_CORNER), run_time=0.8)
        self.say("First, how the OS virtualizes the CPU.",
                 Succession(glide, stu.change("curious")),
                 Succession(Wait(0.8), AnimationGroup(GrowFromCenter(cpu), FadeIn(pa, shift=DOWN * 0.2))))

        # S02.2
        self.say("There were a bunch of important mechanisms:", self.term("mechanisms", at=P3(0, -0.6)))
        gear = GearPair(radius=0.28).move_to(P3(-1.2, 0.5))
        self.play(FadeIn(gear), run_time=0.3)
        self.play(gear.spin(angle=TAU, run_time=0.9))
        self.play(FadeOut(gear), run_time=0.3)

        # S02.3
        trap_lbl = label("trap handler", 18, KERNEL_COLOR).move_to(P3(PX[0] + 0.3, PANEL_Y - 1.1))
        home = p_user.get_center().copy()
        down = P3(PX[0] + 0.5, PANEL_Y - 0.6)
        self.say("traps and trap handlers,",
                 bd.draw(1.2), FadeIn(p_user),
                 Succession(Wait(1.3), bd.cross(p_user, down, run_time=0.8), FadeIn(trap_lbl),
                            p_user.animate(run_time=0.6).move_to(home)))

        # S02.4
        timer_ring = Circle(radius=0.38, color=KERNEL_COLOR).set_stroke(KERNEL_COLOR, 5).move_to(clock)
        off = P3(PX[1] - 1.05, PANEL_Y - 0.45)
        self.say("timer interrupts,",
                 FadeIn(clock),
                 Succession(clock.spin(turns=1, run_time=0.8), Create(timer_ring), FadeOut(timer_ring),
                            hop_to(pa, off, run_time=0.5)))

        # S02.5
        regs_a = VGroup(*[Square(0.12).set_fill(COL["A"], 1).set_stroke(width=0) for _ in range(3)]).arrange(RIGHT, buff=0.05)
        regs_b = VGroup(*[Square(0.12).set_fill(COL["B"], 1).set_stroke(width=0) for _ in range(3)]).arrange(RIGHT, buff=0.05)
        regs_a.move_to(off + UP * 0.5)
        regs_b.move_to(slot)
        tag_arrow = DoubleArrow(P3(PX[2] - 0.45, PANEL_Y - 0.95), P3(PX[2] + 0.45, PANEL_Y - 0.95), buff=0, tip_length=0.12)
        tag_arrow.set_stroke(DIM, 3)
        tag_txt = label("save / restore", 18, DIM).next_to(tag_arrow, DOWN, buff=0.08)
        self.add(regs_a)
        self.say("and how the OS and the hardware carefully save and restore state when switching between processes.",
                 Succession(AnimationGroup(FadeIn(slot), FadeIn(ra), FadeIn(rb), run_time=0.5),
                            regs_a.animate(run_time=0.6).move_to(slot).set_opacity(0.0),
                            AnimationGroup(FadeIn(regs_b), run_time=0.2),
                            regs_b.animate(run_time=0.6).move_to(cpu.slot_point() + UP * 0.3),
                            FadeOut(regs_b, run_time=0.2),
                            hop_to(rb, cpu.slot_point(), run_time=0.5),
                            AnimationGroup(Create(tag_arrow), FadeIn(tag_txt))),
                 min_time=7.0)
        self.remove(regs_a, regs_b)
        # regroup the loose parts into the panels group (so S03 can move them as one)
        self.remove(bd, p_user, cpu, pa, clock, slot, ra, rb, tag_arrow, tag_txt, trap_lbl)
        L.add(trap_lbl)
        R.add(tag_arrow, tag_txt)
        self.add(panels)

        # S02.6
        self.say("Good, good!", prof.change("happy"), Indicate(panels, scale_factor=1.05), min_time=2.0)
        self.beat(0.5)
