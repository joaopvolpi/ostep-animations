import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403

EXEC_SRC = ('char *myargs[3] = {"wc", "p3.c", NULL};\n'
            'execvp(myargs[0], myargs);\n'
            'printf("this shouldn\'t print out");')


class S08Exec(Ep05Scene):
    def construct(self):
        self.add_badge()
        self.add(crux_strip())
        stu, prof = self.add_corner_chars("neutral", "happy")

        # S08.1
        chi = proc(CHI, "ready", scale=0.8, label=f"PID {PID_C}").move_to(P3(-4.7, 1.0))
        mem = Memory(regions=["code", "static data", ("heap", 0.8), ("free", 1.0), "stack"], width=1.3, height=3.4,
                     addresses=False, font_size=15).move_to(P3(-2.6, 0.6))
        for n in ("code", "static data", "heap", "stack"):
            mem.region(n).set_fill(CHI, 0.35).set_stroke(CHI, 3)
        mem.region("free").set_fill(BG, 0).set_stroke(MEM_COLOR, 2)
        for t in (mem.texts[mem.index_of("code")], mem.texts[mem.index_of("static data")]):
            t.set_opacity(0)
        chip = program_chip("p3", DIM, 18).move_to(mem.region("code").get_center())
        chip2 = program_chip("p3", DIM, 18).move_to(mem.region("static data").get_center())
        twin = proc(PAR, "ready", scale=0.8, label=f"PID {PID_P}").move_to(P3(0.6, 0.9))
        twin_chip = program_chip("p3", DIM, 18).next_to(twin, DOWN, buff=0.12)
        with self.narrate("fork() alone is a bit limited. It only gives us copies of the same program."):
            self.play(FadeIn(chi), FadeIn(mem), FadeIn(chip), FadeIn(chip2), run_time=0.9)
            self.play(FadeIn(twin), FadeIn(twin_chip), run_time=0.6)
            self.wait(1.0)
            self.play(FadeOut(twin), FadeOut(twin_chip), run_time=0.6)

        # S08.2
        q = question_mark(0.45).next_to(mem.region("code"), RIGHT, buff=0.15)
        with self.narrate("What if the child should run something different? That's the third call: exec()."):
            self.play(self.terms.show("exec()"), run_time=2.8)
            self.play(FadeIn(q, scale=0.5), Indicate(chip, color=CPU_COLOR), run_time=0.8)

        # S08.3
        code = CodeWalker(EXEC_SRC, font_size=15).move_to(P3(3.4, 2.0))
        disk = Disk(width=1.4, height=1.1).move_to(P3(3.2, -1.0))
        wc_file = FileIcon("wc", width=0.5, color=SKY).move_to(disk.top_point() + UP * 0.75)
        arg_file = FileIcon("p3.c", width=0.4).move_to(P3(4.7, -0.1))
        b1 = code.add_bar(CPU_COLOR, 1)
        b2 = code.add_bar(CPU_COLOR, 2)
        with self.narrate("In our next example, the child calls a variant of exec() to run wc, the word-counting "
                          "program, on the file p3.c."):
            self.play(FadeOut(q), FadeIn(code, shift=LEFT * 0.4), run_time=0.8)
            self.play(FadeIn(b1), FadeIn(b2), run_time=0.4)
            self.play(FadeIn(disk, shift=UP * 0.5), FadeIn(wc_file, shift=UP * 0.5), run_time=0.8)
            self.play(FadeIn(arg_file, shift=LEFT * 0.3), run_time=0.5)
            self.wait(1.5)

        # S08.4
        term = mk_term(6.0, 3, 16).move_to(P3(0.8, -2.4))
        out_txt = "29  107  1030 p3.c"
        with self.narrate("And the output shows the counts: 29 lines, 107 words, 1,030 bytes."):
            self.play(FadeIn(term), run_time=0.4)
            self.play(term.type("./p3"))
            self.play(term.print(out_txt, color=TEXT))
            line = term.lines[-1]
            cw = Text("0", font=MONO_FONT, font_size=16).width
            x0 = line.get_left()[0]
            labs = VGroup()
            for idx, ln, name in ((0, 2, "lines"), (4, 3, "words"), (9, 4, "bytes")):
                t = Text(name, font_size=14, color=CPU_COLOR)
                t.move_to(P3(x0 + (idx + ln / 2) * cw, line.get_y() - 0.27))
                labs.add(t)
            for t in labs:
                self.play(FadeIn(t, shift=UP * 0.1), run_time=0.5)
            self.wait(0.3)
            self.play(term.animate.set_opacity(0.45), FadeOut(labs), FadeOut(arg_file), run_time=0.6)

        # S08.5
        self.say("Let's look inside.", min_time=0.8)

        # S08.6
        pkt = program_chip("exec()", CPU_COLOR, 18).move_to(P3(0.6, 1.0))
        a1 = CurvedArrow(wc_file.get_left() + LEFT * 0.1, mem.region("code").get_right() + RIGHT * 0.05,
                         angle=-0.5, color=SKY, stroke_width=4)
        a2 = CurvedArrow(wc_file.get_left() + LEFT * 0.1 + DOWN * 0.2, mem.region("static data").get_right() + RIGHT * 0.05,
                         angle=-0.4, color=SKY, stroke_width=4)
        with self.narrate("Given the name of an executable and some arguments, exec() loads code and static data "
                          "from that file…"):
            self.play(FadeIn(pkt, scale=0.5), run_time=0.4)
            self.play(pkt.animate.move_to(chi.get_center() + RIGHT * 0.9), run_time=0.9)
            self.play(FadeOut(pkt), Create(a1), Create(a2), run_time=1.0)
            self.wait(1.0)

        # S08.7
        rng = np.random.default_rng(5)
        frags = VGroup()
        for n in ("code", "static data"):
            r = mem.region(n)
            for _ in range(7):
                f = Square(0.13).set_fill(CHI, 0.8).set_stroke(TEXT, 1)
                f.move_to(r.get_center() + P3(rng.uniform(-0.5, 0.5), rng.uniform(-0.25, 0.25)))
                f.rotate(rng.uniform(0, 3))
                frags.add(f)
        wc_chip = program_chip("wc", SKY, 18).move_to(chip)
        wc_chip2 = program_chip("wc", SKY, 18).move_to(chip2)
        with self.narrate("…and overwrites the process's current code segment and static data with it."):
            self.play(FadeIn(frags), FadeOut(chip), FadeOut(chip2), run_time=0.3)
            self.play(*[f.animate.shift(DOWN * rng.uniform(0.6, 1.4) + RIGHT * rng.uniform(-0.3, 0.3)).set_opacity(0)
                        for f in frags], run_time=1.2)
            self.play(mem.region("code").animate.set_fill(SKY, 0.5).set_stroke(SKY, 3),
                      mem.region("static data").animate.set_fill(SKY, 0.5).set_stroke(SKY, 3),
                      FadeIn(wc_chip), FadeIn(wc_chip2), run_time=0.8)
            self.play(FadeOut(a1), FadeOut(a2), run_time=0.4)
            self.remove(frags)

        # S08.8
        argv = tagged("argv: wc p3.c", TEXT, 14, DIM)
        argv.scale_to_fit_width(min(argv.width, 1.15))
        argv.move_to(mem.region("stack").get_center() + UP * 0.05)
        with self.narrate("The heap and the stack are re-initialized."):
            self.play(Indicate(mem.region("heap"), color=CPU_COLOR, scale_factor=1.05),
                      Indicate(mem.region("stack"), color=CPU_COLOR, scale_factor=1.05), run_time=0.8)
            self.play(mem.region("heap").animate.set_fill(CHI, 0.08), mem.region("stack").animate.set_fill(CHI, 0.08),
                      run_time=0.5)
            self.play(FadeIn(argv, shift=DOWN * 0.1), run_time=0.5)

        # S08.9
        pc = Triangle().rotate(-PI / 2).scale(0.1).set_fill(CPU_COLOR, 1).set_stroke(TEXT, 1.5)
        pc.move_to(mem.region("code").get_left() + LEFT * 0.17 + UP * 0.25)
        with self.narrate("Then the OS runs the new program, passing the arguments as its argv."):
            self.play(chi.change("running"), FadeIn(pc, shift=RIGHT * 0.3), run_time=0.7)
            self.play(Indicate(chi, scale_factor=1.05, color=TEXT), run_time=0.8)

        # S08.10
        note = tagged("← Ep. 04: load", DIM, 18, DIM).next_to(disk, UP, buff=0.05).shift(LEFT * 1.0 + UP * 0.9)
        with self.narrate("Sound familiar? It's the loading step from last episode, applied to a process "
                          "that already exists."):
            self.play(FadeIn(note, shift=RIGHT * 0.2), run_time=0.5)
            self.wait(1.5)
            self.play(FadeOut(note), run_time=0.4)

        # S08.11
        self.say("So it makes a new process?", stu.change("surprised"))

        # S08.12
        same = Text("same process\nnew program", font_size=28, color=TEXT, line_spacing=0.8).move_to(P3(0.4, 0.4))
        with self.narrate("No, and that's the key point. exec() creates no process. The same process, "
                          "same PID, becomes a different program."):
            self.play(prof.change("explaining"), Write(same), run_time=1.2)
            self.play(Indicate(chi, scale_factor=1.0, color=CPU_COLOR), Indicate(wc_chip, color=CPU_COLOR), run_time=1.0)
            self.wait(1.5)

        # S08.13
        noway = Arrow(P3(-0.6, -0.1), chi.get_right() + DOWN * 0.1, buff=0.1, color=KERNEL_COLOR, stroke_width=6)
        nw_lab = Text("no way back", font_size=22, color=KERNEL_COLOR).next_to(noway, DOWN, buff=0.1)
        l3 = code.line_mob(3)
        strike = Line(l3.get_left(), l3.get_right()).set_stroke(KERNEL_COLOR, 3)
        with self.narrate("If it works, exec() never returns. The code that came after it is gone."):
            self.play(FadeOut(same), GrowArrow(noway), FadeIn(nw_lab), run_time=0.8)
            self.play(l3.animate.set_opacity(0.35), Create(strike), run_time=0.8)
            self.wait(1.0)

        # S08.14
        xm = x_mark(0.35).move_to(l3.get_right() + RIGHT * 0.35)
        with self.narrate('In our example, the line "this shouldn\'t print out" never prints.'):
            self.play(FadeIn(xm, scale=2.0), run_time=0.4)
            self.play(FadeOut(xm), FadeOut(noway), FadeOut(nw_lab), run_time=0.8)
            self.wait(1.0)

        # S08.15
        names = ["execl", "execlp", "execle", "execv", "execvp", "execvpe"]
        chips = VGroup(*[program_chip(n, DIM, 16) for n in names])
        r1 = VGroup(*chips[:3]).arrange(RIGHT, buff=0.15)
        r2 = VGroup(*chips[3:]).arrange(RIGHT, buff=0.15)
        grid = VGroup(r1, r2).arrange(DOWN, buff=0.15).move_to(P3(1.3, -0.1))
        one = program_chip("exec()", CPU_COLOR, 20).move_to(grid)
        with self.narrate("On Linux there are six variants of exec(), with different ways of passing the arguments, "
                          "but they do the same thing."):
            self.play(FadeOut(disk), FadeOut(wc_file), FadeIn(grid), run_time=0.8)
            self.wait(1.8)
            self.play(Transform(chips, one), run_time=0.8)
        self.beat(0.5)
