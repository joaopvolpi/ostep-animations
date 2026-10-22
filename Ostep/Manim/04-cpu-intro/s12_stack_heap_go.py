import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


def terminal_icon(w=0.8, h=0.55):
    fr = RoundedRectangle(width=w, height=h, corner_radius=0.06).set_fill("#101010", 1).set_stroke(TEXT, 2.5)
    pr = Text(">_", font=MONO_FONT, font_size=18, color=GREEN_OK).move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.1)
    return VGroup(fr, pr)


class S12StackHeapGo(Ep04Scene):
    def construct(self):
        self.add_badge()
        self.add_docked_term("lazily")
        stu, prof = self.add_corner_chars()
        slot = docked_save_slot()
        w = build_s11_end()
        cpu, mem, disk, bus, outline, olab, tag, file = (w[k] for k in
                                                         ("cpu", "mem", "disk", "bus", "outline", "olab", "tag", "file"))
        self.add(slot, cpu, mem, disk, bus, outline, olab, tag, file)
        D = COL["D"]

        def new_tag(i, name):
            return Transform(tag, step_tag(i, name), run_time=0.5)

        def fill_region(name):
            i = mem.index_of(name)
            return AnimationGroup(mem.region(name).animate.set_fill(D, 0.6),
                                  mem.texts[i].animate.set_opacity(1), run_time=0.6)

        # S12.1
        with self.narrate("Step two: the stack. C programs use it for local variables, function parameters "
                          "and return addresses."):
            self.play(new_tag(2, "stack"), fill_region("stack"))
            self.play(self.term("stack", size=40, at=S11_TERM_AT, hold=0.8))

        # S12.2
        st = mem.region("stack")
        st_text = mem.texts[mem.index_of("stack")]
        cells = VGroup(*[Rectangle(width=st.width * 0.9, height=st.height * 0.3).set_fill(BG, 0.6).set_stroke(TEXT, 1)
                         for _ in range(2)]).arrange(DOWN, buff=0.03)
        cells.move_to(st.get_top() + DOWN * (cells.height / 2 + 0.04))
        argc = Text("argc = 2", font=MONO_FONT, font_size=13, color=TEXT).move_to(cells[0])
        argv = Text('argv → ["./d","x"]', font=MONO_FONT, font_size=11, color=TEXT).move_to(cells[1])
        argv.scale_to_fit_width(min(argv.width, cells[1].width * 0.92))
        with self.narrate("The OS sets aside memory for it, and fills in the arguments to main(): argc and the argv array."):
            self.play(st_text.animate.scale(0.8).move_to(st.get_bottom() + UP * 0.1), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(VGroup(c, t), shift=DOWN * 0.3) for c, t in zip(cells, (argc, argv))],
                                  lag_ratio=0.4), run_time=1.0)

        # S12.3
        heap = mem.region("heap")
        mal = Text("malloc()", font=MONO_FONT, font_size=20, color=TEXT).next_to(mem.cells, LEFT, buff=0.35).set_y(heap.get_y() + 0.15)
        fre = Text("free()", font=MONO_FONT, font_size=20, color=TEXT).next_to(mem.cells, LEFT, buff=0.35).set_y(heap.get_y() - 0.25)
        blk = Square(0.16).set_fill(D, 1).set_stroke(TEXT, 1).next_to(mal, RIGHT, buff=0.05)
        with self.narrate("Step three, maybe: a heap. That's for data the program asks for while it runs, with "
                          "malloc(), and gives back with free()."):
            self.play(new_tag(3, "heap"), fill_region("heap"))
            self.play(self.term("heap", size=40, at=S11_TERM_AT, hold=0.6))
            self.play(FadeIn(mal), run_time=0.3)
            self.play(blk.animate.move_to(heap.get_center() + RIGHT * 0.45), run_time=0.6)
            self.play(FadeIn(fre), run_time=0.3)
            self.play(blk.animate.next_to(fre, LEFT, buff=0.1).set_opacity(0), run_time=0.6)

        # S12.4
        free = mem.region("free")
        h_text = mem.texts[mem.index_of("heap")]
        nodes = VGroup(*[Circle(radius=0.06).set_fill(TEXT, 1).set_stroke(width=0) for _ in range(3)]).arrange(RIGHT, buff=0.22)
        links = VGroup(*[Arrow(nodes[k].get_right(), nodes[k + 1].get_left(), buff=0.02, stroke_width=2,
                               tip_length=0.08, max_tip_length_to_length_ratio=0.5, color=TEXT) for k in range(2)])
        ll = VGroup(nodes, links)
        grow = 0.35
        new_heap = heap.copy().stretch_to_fit_height(heap.height + grow).align_to(heap, UP)
        new_free = free.copy().stretch_to_fit_height(free.height - grow).align_to(free, DOWN)
        with self.narrate("Linked lists, hash tables, trees. It starts small, and the OS can grow it on request."):
            self.play(h_text.animate.scale(0.8).move_to(heap.get_top() + DOWN * 0.13),
                      FadeIn(ll.move_to(heap.get_center() + DOWN * 0.08)), run_time=0.8)
            self.play(Transform(heap, new_heap), Transform(free, new_free),
                      ll.animate.shift(DOWN * grow / 2), FadeOut(mal), FadeOut(fre), run_time=1.0)

        # S12.5
        x0 = mem.cells.get_right()[0] + 0.25
        plugs = VGroup(*[plug_glyph(s, font_size=16) for s in ("0 stdin", "1 stdout", "2 stderr")])
        for k, p in enumerate(plugs):
            p.move_to(P3(0, 2.15 - 0.55 * k), aligned_edge=ORIGIN)
            p.shift(RIGHT * (x0 - p.get_left()[0]))
        kb = keyboard_icon(0.85).move_to(P3(5.55, 2.15))
        term_ic = terminal_icon().move_to(P3(5.55, 1.05))
        cables = VGroup(
            Line(plugs[0].get_right(), kb.get_left()),
            Line(plugs[1].get_right(), term_ic.get_left() + UP * 0.1),
            Line(plugs[2].get_right(), term_ic.get_left() + DOWN * 0.1),
        ).set_stroke(DIM, 2)
        with self.narrate("Step four: I/O setup. On UNIX, every process starts with three open file descriptors: "
                          "standard input, standard output, and standard error. That's how a program can read "
                          "your keyboard and print to your terminal from line one."):
            self.play(new_tag(4, "I/O"))
            self.play(LaggedStart(*[FadeIn(p, shift=LEFT * 0.3) for p in plugs], lag_ratio=0.3), run_time=1.2)
            self.play(self.term("file descriptors", size=36, at=S11_TERM_AT, hold=0.8))
            self.play(FadeIn(kb), FadeIn(term_ic), Create(cables), run_time=1.0)

        # S12.6
        code = mem.region("code")
        c_text = mem.texts[mem.index_of("code")]
        main_bar = Rectangle(width=code.width * 0.86, height=code.height * 0.42).set_fill(CPU_COLOR, 0.9).set_stroke(width=0)
        main_bar.move_to(code.get_bottom() + UP * (code.height * 0.27))
        main_t = Text("main()", font=MONO_FONT, font_size=16, color=BG, weight="BOLD").move_to(main_bar)
        jump = CurvedArrow(cpu.get_right() + RIGHT * 0.15 + UP * 0.2, main_bar.get_left() + LEFT * 0.05,
                           angle=-0.5, tip_length=0.2, stroke_width=5, color=CPU_COLOR)
        ep = ep_tag("→ Ep. 06").scale(0.8).move_to(P3(-0.1, 1.25))
        with self.narrate("And finally, the OS jumps to the entry point, main(), using a special mechanism "
                          "we'll see soon…"):
            self.play(new_tag(5, "run"), c_text.animate.scale(0.8).move_to(code.get_top() + DOWN * 0.13))
            self.play(FadeIn(main_bar), FadeIn(main_t), run_time=0.4)
            self.play(Create(jump), run_time=0.8)
            self.play(FadeIn(ep, scale=1.3), run_time=0.4)

        # S12.7
        d_proc = proc("D", scale=0.7).move_to(mem.cells.get_center())
        seat_pt = cpu.slot_point() + UP * 0.02
        comp = Computer("idle").scale(0.6).move_to(P3(-3.0, -2.45))
        with self.narrate("…and hands the CPU over to the new process. The performance begins."):
            self.play(ReplacementTransform(outline.copy(), d_proc), FadeOut(olab), FadeOut(ep), run_time=1.0)
            self.play(d_proc.blink(), run_time=0.4)
            d_proc.set_expression("running")
            self.play(hop_to(d_proc, feet_for_bottom(d_proc, seat_pt), run_time=0.8), FadeOut(jump))
            self.play(FadeIn(comp, shift=UP * 0.4), run_time=0.5)
            self.play(comp.change("happy"), run_time=0.6)
        self.beat(0.8)

        # transition to S13: everything except D fades; D goes to center, ready
        keep = (d_proc, self.badge, self.terms.docked, stu, prof, slot)
        others = [m for m in self.mobjects if m not in keep]
        self.play(*[FadeOut(m) for m in others], run_time=0.8)
        target = proc("D", "ready").move_to(P3(0, 0.2))
        d_proc.set_expression("ready")
        self.play(Transform(d_proc, target), run_time=0.8)
