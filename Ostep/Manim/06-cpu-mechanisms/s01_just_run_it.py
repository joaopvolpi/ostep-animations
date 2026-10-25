import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403

S1_CPU = P3(0, 0.7)
S1_MEM = P3(-4.6, 0.7)
S1_DISK = P3(4.6, 0.6)
S1_OS = P3(0, -1.3)


def mem_scribbles(mem):
    rng = np.random.default_rng(6)
    g = VGroup()
    for c in mem.cells:
        cx, cy = c.get_center()[:2]
        for _ in range(2):
            x0, x1 = rng.uniform(-0.5, 0.5, 2)
            y0, y1 = rng.uniform(-0.12, 0.12, 2)
            g.add(Line(P3(cx + x0, cy + y0), P3(cx + x1, cy + y1)).set_stroke(COL["A"], 4))
    return g


def build_end():
    """S01 end state."""
    cpu = CPU(1.4).move_to(S1_CPU)
    a = proc("A", "running", scale=1.0)
    bottom_to(a, cpu.slot_point() + UP * 0.12)
    mem = Memory(cells=8, width=1.2, height=3.2).move_to(S1_MEM)
    scr = mem_scribbles(mem)
    disk = Disk().move_to(S1_DISK)
    book = book_icon("library", width=0.9, height=1.1, font_size=16).move_to(S1_OS)
    comp = Computer("overwhelmed").scale(0.6).move_to(P3(0, -2.9))
    loop = loop_arrow(0.4).move_to(a.get_top() + UP * 0.3)
    stu = student_dialogue("sad")
    prof = prof_dialogue("thinking")
    return dict(cpu=cpu, a=a, mem=mem, scr=scr, disk=disk, book=book, comp=comp, loop=loop, stu=stu, prof=prof)


class S01JustRunIt(Ep06Scene):
    def construct(self):
        stu = student_dialogue("curious")
        prof = prof_dialogue("neutral")
        cpu = CPU(1.4).move_to(S1_CPU)
        a = proc("A", "ready", scale=1.0)
        bottom_to(a, P3(-2.4, 0.2))
        main_lab = Text("main()", font=MONO_FONT, font_size=26, color=TEXT).move_to(P3(-3.6, 1.9))
        main_arr = Arrow(main_lab.get_bottom() + DOWN * 0.05, a.get_top() + UP * 0.05, buff=0, stroke_width=4,
                         tip_length=0.18, color=TEXT)

        # S01.1
        self.say("Last time I asked how the OS ever gets control back once my program is on the CPU. "
                 "So let's start simple. What is the simplest way to run a program? "
                 "Load it, jump to main(), and get out of the way?",
                 Succession(AnimationGroup(FadeIn(stu, shift=RIGHT * 0.6), FadeIn(prof, shift=LEFT * 0.6)),
                            Wait(1.0), FadeIn(cpu), Wait(5.5),
                            AnimationGroup(FadeIn(a, shift=DOWN * 0.3), FadeIn(main_lab), run_time=0.8),
                            GrowArrow(main_arr), Wait(2.0),
                            AnimationGroup(FadeOut(main_arr), FadeOut(main_lab),
                                           hop_bottom(a, cpu.slot_point() + UP * 0.12, run_time=0.8))))
        a.set_expression("running")

        # S01.2
        gauge = SpeedGauge(0.02, width=1.4, color=GREEN_OK).move_to(P3(2.3, 1.1))
        bar, lab = gauge.value_targets(1.0, "FAST")
        lab.set_color(GREEN_OK)
        self.say("That's called direct execution, and it has one huge advantage. It's fast. No middleman.",
                 prof.change("explaining"),
                 Succession(FadeIn(gauge), Wait(1.0), AnimationGroup(Transform(gauge.bar, bar), Transform(gauge.label, lab), run_time=1.5)))

        # S01.3
        lines = VGroup(*[Line(P3(-0.9, 1.6 + k * 0.3), P3(-0.5 - 0.3 * (k % 2), 1.6 + k * 0.3)).set_stroke(CPU_COLOR, 3, opacity=0.7)
                         for k in range(3)])
        self.say("The program runs natively on the hardware.",
                 Succession(FadeIn(lines, shift=RIGHT * 0.3), Wait(0.6), FadeOut(lines)))

        # S01.4
        self.say("Great. Ship it.", stu.change("excited"))
        self.beat(0.5)

        # S01.5
        disk = Disk().move_to(S1_DISK)
        arm = Line(a.get_right() + UP * 0.2, disk.top_point()).set_stroke(COL["A"], 4)
        files = [FileIcon(None, width=0.4).move_to(disk.top_point() + UP * 0.2) for _ in range(3)]
        self.say("Now the program decides to read every file on the disk.",
                 prof.change("worried"),
                 Succession(FadeIn(disk), Create(arm),
                            LaggedStart(*[PacketFly(f, a.get_center(), arc=0.5, end_scale=0.4, fade=True, run_time=0.9)
                                          for f in files], lag_ratio=0.35)))
        self.remove(*files)

        # S01.6
        mem = Memory(cells=8, width=1.2, height=3.2).move_to(S1_MEM)
        arm2 = Line(a.get_left() + UP * 0.2, mem.cells.get_right()).set_stroke(COL["A"], 4)
        scr = mem_scribbles(mem)
        self.say("Or to scribble over memory that isn't its own.",
                 Succession(AnimationGroup(FadeOut(arm), FadeIn(mem)), Create(arm2),
                            LaggedStart(*[Create(l) for l in scr], lag_ratio=0.1, run_time=2.0)))

        # S01.7
        loop = loop_arrow(0.4).move_to(a.get_top() + UP * 0.3)
        comp = Computer("overwhelmed").scale(0.6).move_to(P3(0, -2.9))
        self.say("Or just to run while (1) until the sun burns out.",
                 Succession(AnimationGroup(Rotate(a, TAU, about_point=a.get_center(), run_time=1.5), FadeIn(loop), FadeOut(arm2)),
                            FadeIn(comp, scale=0.5)))

        # S01.8
        os_box = KernelToken(scale=1.0).move_to(S1_OS)
        wall = Rectangle(width=3.0, height=0.12).set_fill(USER_COLOR, 0.25).set_stroke(USER_COLOR, 2, opacity=0.6)
        wall.move_to(P3(0, -0.55))
        self.say("And the OS does… what, exactly?",
                 stu.change("confused"),
                 Succession(FadeIn(os_box), FadeIn(wall), os_box.reach(P3(0, -0.62), run_time=0.5),
                            Flash(P3(0, -0.55), color=USER_COLOR, flash_radius=0.3, run_time=0.4), os_box.retract(run_time=0.4)))

        # S01.9
        glow = SurroundingRectangle(cpu, color=CPU_COLOR, buff=0.12, corner_radius=0.15)
        self.say("Nothing. The OS isn't running. The program is. The OS can only watch from the sidelines.",
                 os_box.dim_to(0.3), Succession(Wait(1.0), Create(glow)))
        self.beat(1.0)

        # S01.10
        book = book_icon("library", width=0.9, height=1.1, font_size=16).move_to(S1_OS)
        self.say("An operating system with no control over anything is just a library. "
                 "A very sad state of affairs for an aspiring operating system.",
                 prof.change("thinking"),
                 Succession(Wait(2.0), AnimationGroup(ReplacementTransform(os_box, book), FadeOut(wall), FadeOut(glow), FadeOut(gauge),
                                                      run_time=1.0), stu.change("sad")))
