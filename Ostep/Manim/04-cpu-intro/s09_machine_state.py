import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


def pointer_tag(name, color, y, mem):
    x0 = mem.cells.get_right()[0]
    arr = Arrow(P3(x0 + 0.85, y), P3(x0 + 0.05, y), buff=0, stroke_width=4, tip_length=0.18,
                max_tip_length_to_length_ratio=0.4, color=color)
    t = Text(name, font=MONO_FONT, font_size=22, color=color, weight="BOLD").next_to(arr, RIGHT, buff=0.08)
    return VGroup(arr, t)


class S09MachineState(Ep04Scene):
    def construct(self):
        self.add_badge()
        self.add_docked_term("modularity")
        stu, prof = self.add_corner_chars()
        cpu = CPU(CPU_SIZE).move_to(CPU_HOME)
        a = proc("A", "running")
        seat(a, cpu)
        self.add(cpu, a)

        # S09.1
        world = VGroup(cpu, a)
        self.say("“A running program” is a nice slogan. But if the OS is going to stop a process and resume "
                 "it later, it needs to know exactly what a process is.",
                 world.animate(run_time=1.2).shift(S09_CPU_POS - CPU_HOME),
                 Succession(Wait(1.4), Wiggle(a, scale_value=1.05, rotation_angle=0.02, run_time=1.2)))

        # S09.2 freeze
        overlay = Rectangle(width=16, height=9).set_fill(BG, 0.45).set_stroke(width=0)
        pause = PauseGlyph(0.5).move_to(a.get_center() + UP * 0.1)
        flash = Rectangle(width=16, height=9).set_fill(WHITE, 0.6).set_stroke(width=0)
        with self.narrate("Here's a good way to think about it. Suppose we freeze a process mid-step."):
            self.wait(1.6)
            self.add(flash)
            a.set_expression("ready")
            self.play(FadeOut(flash, run_time=0.25))
            self.add(overlay, stu, prof, self.badge, self.terms.docked)
            self.play(FadeIn(pause, scale=1.4), run_time=0.5)

        # S09.3
        pad = Notepad("To resume A:", lines=3, width=3.6, font_size=22).move_to(P3(0, -2.45))
        self.say("What would we have to write down to bring it back perfectly?",
                 FadeIn(pad, shift=UP * 0.3, run_time=0.8))

        # S09.4
        self.say("In other words: what parts of the machine can this program read or change? "
                 "That's its machine state.",
                 prof.change("explaining", look_at=a),
                 Succession(Wait(2.4), self.term("machine state")))

        # S09.5
        mem = s09_memory(colored=False)
        link = DashedLine(cpu.get_left(), mem.cells.get_right(), dash_length=0.1).set_stroke(COL["A"], 2)
        with self.narrate("First, memory. The instructions live in memory. So does the data the program reads "
                          "and writes."):
            self.play(Create(mem.cells), FadeIn(mem.texts), FadeIn(mem.addresses), run_time=1.2)
            self.play(*[mem.fill_cell(n, COL["A"], 0.35) for n in ("code", "static data", "heap", "stack")],
                      *[mem.region(n).animate.set_stroke(COL["A"], 3) for n in ("code", "static data")],
                      Create(link), run_time=1.0)

        # S09.6
        aspace = DashedVMobject(SurroundingRectangle(mem.cells, buff=0.1, corner_radius=0.08),
                                num_dashes=44).set_stroke(COL["A"], 3)
        l1 = pad.line_text(0, "memory (address space)")
        with self.narrate("The memory a process can address is its address space."):
            self.play(Create(aspace), run_time=0.8)
            self.play(self.term("address space"))
            self.play(Write(l1), run_time=0.8)

        # S09.7
        regs = s09_registers()
        self.say("Second, registers. Lots of instructions read and update them directly.",
                 Succession(FadeIn(regs, shift=LEFT * 0.3, run_time=0.8), regs.flicker(rounds=4, step=0.3)))

        # S09.8
        code = mem.region("code")
        hl = Rectangle(width=code.width * 0.8, height=0.14).set_fill(CPU_COLOR, 0.9).set_stroke(width=0)
        hl.move_to(code.get_center() + DOWN * code.height * 0.28)
        pc_tag = pointer_tag("PC", CPU_COLOR, hl.get_y(), mem)
        with self.narrate("A few are special. The program counter, sometimes called the instruction pointer, "
                          "says which instruction runs next."):
            self.play(regs.highlight("PC", CPU_COLOR), run_time=0.6)
            self.play(self.term("program counter (PC)", size=44))
            self.play(TransformFromCopy(regs.name_texts["PC"], pc_tag[1]), GrowArrow(pc_tag[0]),
                      FadeIn(hl), run_time=0.9)

        # S09.9
        q = Text("?", font_size=40, color=TEXT, weight="BOLD").next_to(code, RIGHT, buff=0.15).shift(UP * 0.15)
        with self.narrate("Lose it and the process forgets where it was."):
            self.play(FadeOut(pc_tag), FadeOut(hl), FadeIn(q, scale=1.5), run_time=0.3)
            self.wait(0.8)
            self.play(FadeIn(pc_tag), FadeIn(hl), FadeOut(q), run_time=0.4)

        # S09.10
        stack = mem.region("stack")
        st_text = mem.texts[mem.index_of("stack")]
        fh = stack.height / 3.4
        frames = VGroup()
        for k, lab in enumerate(("ret addr", "locals", "params")):
            r = Rectangle(width=stack.width * 0.86, height=fh).set_fill(COL["A"], 0.6).set_stroke(TEXT, 1)
            r.move_to(stack.get_bottom() + UP * (fh * (k + 0.5) + 0.04))
            t = Text(lab, font_size=15, color=TEXT).move_to(r)
            frames.add(VGroup(r, t))
        sp_tag = pointer_tag("SP", MEM_COLOR, frames[2].get_top()[1], mem)
        fp_tag = pointer_tag("FP", USER_COLOR, frames[1].get_top()[1] - 0.02, mem)
        fp_tag.shift(DOWN * 0.0)
        l2 = pad.line_text(1, "registers (PC, SP, FP…)")
        with self.narrate("The stack pointer and frame pointer keep track of the stack: function parameters, "
                          "local variables, return addresses."):
            self.play(regs.highlight("SP", MEM_COLOR), regs.highlight("FP", USER_COLOR),
                      self.terms.write("stack pointer & frame pointer", size=40), run_time=0.8)
            self.play(FadeOut(st_text), LaggedStart(*[FadeIn(f, shift=DOWN * 0.2) for f in frames], lag_ratio=0.4),
                      run_time=1.4)
            self.play(TransformFromCopy(regs.name_texts["SP"], sp_tag[1]), GrowArrow(sp_tag[0]),
                      TransformFromCopy(regs.name_texts["FP"], fp_tag[1]), GrowArrow(fp_tag[0]), run_time=0.9)
            self.play(self.terms.dock_anim(), Write(l2), run_time=0.8)

        # S09.11
        files = s09_files()
        l3 = pad.line_text(2, "open files")
        with self.narrate("Third, I/O information. Programs talk to storage, so the process includes things like "
                          "the list of files it currently has open."):
            self.play(FadeIn(files[:2], shift=LEFT * 0.3), run_time=0.6)
            self.play(LaggedStart(*[FadeIn(r) for r in files.rows], lag_ratio=0.3), run_time=1.2)
            self.play(Write(l3), run_time=0.6)

        # S09.12
        panels = [VGroup(mem.cells, aspace), regs, files]
        outlines = VGroup(*[SurroundingRectangle(p, buff=0.12, corner_radius=0.1).set_stroke(VIRT, 3) for p in panels])
        ms_label = Text("machine state", font_size=30, color=VIRT, weight="BOLD").move_to(P3(-0.5, 2.75))
        slot = save_slot(1.1).move_to(pad)
        with self.narrate("So a process is a snapshot: memory, registers, open files. Save those and you can "
                          "pause it like a video game!"):
            self.play(stu.change("excited", look_at=a), run_time=0.6)
            self.play(LaggedStart(*[Create(o) for o in outlines], lag_ratio=0.3), FadeIn(ms_label), run_time=1.4)
            self.play(FadeOut(VGroup(l1, l2, l3)), ReplacementTransform(pad, slot), run_time=1.0)

        # S09.13
        docked = docked_save_slot()
        with self.narrate("Exactly the right instinct. Hold on to it. It's the heart of the context switch."):
            self.play(prof.change("happy", look_at=stu), run_time=0.6)
            self.play(Transform(slot, docked), FadeOut(outlines), FadeOut(ms_label), run_time=1.0)
            a.set_expression("running")
            self.play(FadeOut(overlay), FadeOut(pause), run_time=0.8)
        self.wait(0.3)
