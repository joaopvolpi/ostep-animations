import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


class S04CellDivides(Ep05Scene):
    def construct(self):
        w = build_s03_end()
        self.add_badge()
        self.add(crux_strip())
        self.add_docked_term("fork()")
        stu, prof = self.add_corner_chars("curious", "explaining")
        old = VGroup(w["cpu"], w["par"], w["bd"], w["gauge"], w["packet"], w["code"], w["code_bar"], w["mt"])
        self.add(old)

        # S04.1
        pw = ProcessWorld(PAR, PID_P).place(P3(0, -0.1))
        pause = PauseGlyph(0.4).move_to(pw.creature.get_center() + RIGHT * 0.75 + UP * 0.25)
        with self.narrate("And what the OS does is create a new process."):
            self.play(FadeOut(old), run_time=0.8)
            self.play(pw.assemble(1.4))
            self.play(FadeIn(pause, scale=1.4), run_time=0.4)

        # S04.2
        almost = Text("almost\nexact copy", font_size=30, color=TEXT, line_spacing=0.8).move_to(P3(0, -1.95))
        delta = WORLD_L - pw.panels.get_center()
        other, peel, cascade = pw.clone_stages(WORLD_R, CHI, PID_C)
        with self.narrate("Not an empty one. An almost exact copy of the caller."):
            self.play(Write(almost), run_time=0.8)
            self.play(*[p.animate.shift(delta) for p in pw.parts()], pause.animate.shift(delta),
                      almost.animate.move_to(P3(0, 0.45)), run_time=0.8)
            self.play(peel)

        # S04.3
        t_as = Text("address space", font_size=16, color=DIM)
        t_rg = Text("registers", font_size=16, color=DIM)
        t_pc = Text("PC", font_size=16, color=CPU_COLOR)
        with self.narrate("Same code. Its own copy of the address space, its own registers, its own program counter."):
            self.play(cascade)
            t_as.next_to(other.memory, DOWN, buff=0.1)
            t_rg.next_to(other.regs, UP, buff=0.08)
            t_pc.next_to(other.regs.boxes["PC"], RIGHT, buff=0.1)
            self.play(LaggedStart(FadeIn(t_as), FadeIn(t_rg), FadeIn(t_pc), lag_ratio=0.4), run_time=1.0)
            self.play(other.set_pid(PID_C))
            self.play(other.creature.blink())
        cw = other

        # S04.4
        braces, blabs = [], []
        for wld in (pw, cw):
            br = Brace(wld.panels, DOWN, color=DIM, buff=0.08)
            bl = Text("machine state", font_size=20, color=DIM).next_to(br, DOWN, buff=0.08)
            braces.append(br)
            blabs.append(bl)
        slot = save_slot(0.7).move_to(P3(0, -0.45))
        with self.narrate("Remember our freeze-frame from last time, memory, registers, open files? "
                          "The OS just copied all of it."):
            self.play(FadeOut(almost), FadeOut(t_as), FadeOut(t_rg), FadeOut(t_pc), run_time=0.5)
            self.play(*[Create(b) for b in braces], *[FadeIn(b) for b in blabs], FadeIn(slot), run_time=0.8)
            self.play(Indicate(slot, scale_factor=1.25), run_time=0.8)
            self.wait(1.6)

        # S04.5
        lab_p = Text("parent", font_size=26, color=PAR, weight="BOLD").next_to(pw.creature, LEFT, buff=0.35)
        lab_c = Text("child", font_size=26, color=CHI, weight="BOLD").next_to(cw.creature, RIGHT, buff=0.35)
        with self.narrate("The creator is the parent. The new process is the child."):
            self.play(*[FadeOut(b) for b in braces + blabs], FadeOut(slot), run_time=0.4)
            self.play(Write(lab_p), self.terms.note("parent", run_time=0.6))
            self.play(Write(lab_c), self.terms.note("child", run_time=0.6))

        # S04.6
        flag = program_chip("main()", CPU_COLOR, 18)
        flag.move_to(cw.memory.get_left() + LEFT * (0.1 + flag.width / 2) + UP * 0.9)
        q = question_mark(0.4).next_to(flag, UP, buff=0.05)
        with self.narrate("So the child starts again from the top, at main()?"):
            self.play(stu.change("curious", look_at=flag), FadeIn(flag, scale=0.5), FadeIn(q), run_time=0.8)

        # S04.7
        mt = mk_term(4.4, 1, 18).move_to(S4_TERM_AT)
        xm = x_mark(0.4).move_to(flag)
        with self.narrate('No, and that\'s the odd part. Notice "hello" printed only once.'):
            self.play(prof.change("explaining", look_at=flag), FadeIn(xm, scale=2.0), run_time=0.5)
            self.play(FadeOut(flag), FadeOut(xm), FadeOut(q), FadeIn(mt), run_time=0.5)
            self.play(mt.print("hello (pid:29146)"))

        # S04.8
        pm, cm = pw.pc_marker(PAR), cw.pc_marker(CHI)
        b1, b2 = s4_bubbles()
        with self.narrate("The child never ran that line. It simply comes to life inside the call to fork(), "
                          "as if it had called it itself."):
            self.play(FadeIn(pm, scale=2.0), FadeIn(cm, scale=2.0), run_time=0.6)
            self.play(FadeIn(b1, shift=UP * 0.1), FadeIn(b2, shift=UP * 0.1), run_time=0.6)
            self.play(FadeOut(pause), run_time=0.7)
            self.wait(1.5)

        # S04.9
        with self.narrate("Two processes, both about to return from the same call."):
            self.play(Indicate(pm, scale_factor=1.8), Indicate(cm, scale_factor=1.8), run_time=1.0)
        self.beat(1.0)

        # S04.10
        self.say("The book warns you that fork() is the strangest routine you'll ever call. It's right.",
                 prof.change("happy"), stu.change("surprised"))
        self.beat(0.8)
