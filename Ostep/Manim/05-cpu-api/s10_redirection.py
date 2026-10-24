import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


class S10Redirection(Ep05Scene):
    def construct(self):
        d = build_s09_end()
        old_term, loop, sh, gap_sh = d["term"], d["loop"], d["sh"], d["gap_sh"]
        self.add_badge()
        self.add_docked_term("shell")
        stu, prof = self.add_corner_chars("frustrated", "proud")
        self.add(old_term, loop, sh, gap_sh)
        shop, shop_anim = loop.workshop()
        finish_now(shop_anim)
        gap_anim, gap_lab = loop.highlight_gap()
        finish_now(gap_anim)
        self.add(gap_lab)
        ut = tagged("user program", USER_COLOR, 18, USER_COLOR).move_to(P3(1.6, 1.75))
        run0 = program_chip('run("wc")', DIM, 24).scale(0.6).move_to(P3(-5.6, 2.75)).set_opacity(0.4)
        self.add(shop, ut, run0)

        fd = FdTable(center=(0, -0.2))
        clone = proc(CHI, "ready", scale=0.55, label="sh")
        bottom_to(clone, fd.panel.get_top() + UP * 0.0)
        term = mk_term(5.0, 2, 18).move_to(P3(-3.6, 2.3))
        step_names = ["close(1)", "open(file)", "exec(wc)"]
        chips = VGroup(*[program_chip(n, DIM, 20) for n in step_names]).arrange(RIGHT, buff=0.5).move_to(P3(0, -2.6))
        chips.set_opacity(0.4)
        f_icon = FileIcon("newfile.txt", width=0.45, font_size=14).move_to(P3(4.6, -0.2))

        def light(i):
            return chips[i].animate.set_opacity(1).set_stroke(CPU_COLOR, 3)

        # S10.1
        cmd = "wc p3.c > newfile.txt"
        with self.narrate("Let's use the gap. You type: wc p3.c > newfile.txt."):
            self.play(FadeOut(loop), FadeOut(sh), FadeOut(old_term), FadeOut(shop), FadeOut(gap_lab), FadeOut(ut), FadeOut(run0), stu.change("curious"), run_time=0.8)
            self.play(gap_sh.animate.scale(0.55 / 0.4).move_to(clone.get_center()), FadeIn(fd), FadeIn(chips), run_time=1.0)
            self.remove(gap_sh)
            self.add(clone)
            self.play(FadeIn(term), run_time=0.3)
            self.play(term.type(cmd))
            line = term.lines[-1][-1]
            cw = Text("0", font=MONO_FONT, font_size=18).width
            gt = min(line, key=lambda m: abs(m.get_center()[0] - (line.get_left()[0] + (cmd.index(">") + 0.5) * cw)))
            gt.set_color(VIRT)

        # S10.2
        ghost = DashedVMobject(CubicBezier(P3(0.1, -0.45), P3(0.5, -1.0), P3(4.4, -1.0), P3(4.5, -0.55)), num_dashes=24)
        ghost.set_stroke(DIM, 3)
        with self.narrate("The > sign means the output of wc should go into a file, not the screen."):
            self.play(Indicate(gt, scale_factor=1.8, color=VIRT), run_time=0.8)
            self.play(FadeIn(f_icon, shift=LEFT * 0.3), Create(ghost), run_time=0.8)
            self.wait(1.0)

        # S10.3
        self.say("This is redirection.", self.terms.show("redirection", hold=0.5))

        # S10.4
        glow = DashedVMobject(Circle(radius=0.85).move_to(clone), num_dashes=30).set_stroke(CPU_COLOR, 3)
        with self.narrate("The shell does it in the gap."):
            self.play(Create(glow), run_time=0.8)
            self.wait(0.6)

        # S10.5
        with self.narrate("In the child, before exec(), it closes standard output, then opens the file."):
            self.play(light(0), fd.cut(1))
            self.wait(1.0)

        # S10.6
        scan, marks = fd.scan_free(taken=(0,), free=1)
        tag = tagged("lowest free = 1", CPU_COLOR, 18, CPU_COLOR).move_to(P3(-2.2, 0.3))
        with self.narrate("UNIX always hands out the lowest free file descriptor. Remember our three plugs, 0, 1, 2? "
                          "Plug zero is taken, plug one was just freed, so the file takes plug number one."):
            self.play(light(1), FadeOut(ghost), run_time=0.4)
            self.play(scan)
            self.play(FadeIn(tag), run_time=0.4)
            anim, plug, cable = fd.plug_into(1, f_icon, below=0.8)
            self.play(anim)
            self.wait(1.0)
            self.play(FadeOut(marks), FadeOut(tag), run_time=0.4)

        # S10.7
        wc_new = proc(CHI, "ready", scale=0.55, label="wc")
        wc_new.move_to(clone)
        with self.narrate("And open files stay open across exec()."):
            self.play(light(2), FadeOut(glow), run_time=0.4)
            self.play(FadeOut(clone), FadeIn(wc_new), run_time=0.8)
            self.play(Indicate(fd.plugs, color=CPU_COLOR, scale_factor=1.1), Indicate(fd.cables, color=CPU_COLOR),
                      run_time=1.0)

        # S10.8
        toks = [mono("29  107  1030 p3.c", 14, CPU_COLOR)]
        out = mono("29  107  1030 p3.c", 14, TEXT)
        with self.narrate('So when wc later prints, it prints "to the screen", exactly as always, '
                          "and the text lands in the file instead."):
            self.play(wc_new.change("running"), run_time=0.5)
            for t in toks:
                t.move_to(fd.slot_point(1) + DOWN * 0.3)
                self.play(FadeIn(t, scale=0.6), run_time=0.3)
                self.play(t.animate.move_to(f_icon.get_center()).scale(0.5).set_opacity(0), run_time=1.0)
                self.remove(t)
            f_icon.label.next_to(f_icon.page, RIGHT, buff=0.1)
            out.next_to(f_icon, LEFT, buff=0.15)
            self.play(FadeIn(out, shift=LEFT * 0.2), run_time=0.5)
            self.wait(1.0)

        # S10.9
        self.add(stu)
        with self.narrate("And wc doesn't even know!"):
            self.play(stu.change("excited"), run_time=0.5)
            self.play(stu.thinks("I just print to stdout…", max_width=3.5, font_size=24), run_time=0.8)
            self.wait(1.0)
            self.play(stu.remove_bubble())

        # S10.10
        with self.narrate("And the proof is easy. Run the command, and the screen stays empty. Then read the file, "
                          "and all the expected output is there."):
            self.play(prof.change("happy"), run_time=0.5)
            self.play(term.type("wc p3.c > newfile.txt"))
            self.play(term.prompt_line())
            self.wait(1.0)
            self.play(term.type("cat newfile.txt"))
            self.play(term.print("29  107  1030 p3.c"))
            self.wait(1.0)

        # transition: everything fades except the Terminal
        self.play(*[FadeOut(m) for m in (fd, wc_new, f_icon, out, plug, cable, chips, term)], run_time=0.8)
