import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from manim import *  # noqa: E402,F403
from ostep_lib import *  # noqa: E402,F403
from common import *  # noqa: E402,F403
from s12_same_address import top_strip, phys_strip, DIV_Y  # noqa: E402

THREADS_C = r'''volatile int counter = 0;
void *worker(void *arg) {
    for (i = 0; i < loops; i++)
        counter++;
}
// main: create 2 threads, join both, print counter'''
CODE_POS = np.array([-3.3, 0.4, 0])
CELL_POS = np.array([3.2, 1.2, 0])
T_POS = (np.array([1.6, -1.05, 0]), np.array([4.8, -1.05, 0]))   # base points
TERM_POS = np.array([2.4, -2.5, 0])


def counter_cell(value="0", color=TEXT):
    box = RoundedRectangle(width=1.9, height=1.0, corner_radius=0.1).set_fill(MEM_COLOR, 0.2).set_stroke(MEM_COLOR, 4)
    box.move_to(CELL_POS)
    lab = Text("counter", font=MONO_FONT, font_size=22, color=MEM_COLOR).next_to(box, UP, buff=0.1)
    val = Text(str(value), font=MONO_FONT, font_size=36, color=color, weight=BOLD).move_to(box)
    g = VGroup(box, lab, val)
    g.box, g.lab, g.val = box, lab, val
    return g


def threads_code():
    c = code_block(THREADS_C, 15).move_to(CODE_POS)
    return c, code_title(c, "threads.c")


def threads_terminal():
    return Terminal(width=4.6, height=1.5, font_size=16).move_to(TERM_POS)


def placed_threads():
    t1 = make_thread("T1", T1_COLOR)
    t2 = make_thread("T2", T2_COLOR)
    place_on(t1, T_POS[0])
    place_on(t2, T_POS[1])
    return t1, t2


def s13_end():
    code, title = threads_code()
    cell = counter_cell("137298", BAD)
    t1, t2 = placed_threads()
    links = VGroup(*[DashedLine(t.get_top(), cell.box.get_bottom(), dash_length=0.1).set_stroke(DIM, 2) for t in (t1, t2)])
    term = threads_terminal()
    term.type("./threads 100000")
    term.print("Final value : 137298   // what the??")
    return code, title, cell, t1, t2, links, term


class S13TwoThreads(NarratedScene):
    def construct(self):
        stu, prof = make_hosts("corner", stu_expr="confused", prof_expr="worried")
        th = terms(CONC)
        bdg = badge(VIRT)
        left, right = top_strip(-2.75), top_strip(2.75)
        phys = phys_strip()
        split = IllusionSplit("what each process sees", "what really happens", orientation="horizontal", at=DIV_Y,
                              top_y=3.15, title_size=22)
        self.add(stu, prof, bdg, left, right, phys, split, set_docked(th, "virtualizing memory"))

        # S13.1
        card = piece_card(1).move_to([0, 2.0, 0])
        with self.narrate("Second piece: concurrency."):
            self.play(FadeOut(VGroup(left, right, phys, split)), bdg.recolor(CONC), run_time=0.7)
            self.play(FadeIn(card, scale=0.8), run_time=0.4)
            self.play(Indicate(card, color=CONC), run_time=0.6)
            self.play(FadeOut(card), run_time=0.3)
            self.play(th.show("concurrency", hold=0.8))

        # S13.2 callback: the OS juggles too
        cpu = CPU(size=0.9).move_to([0, 0.9, 0])
        ps = VGroup()
        for i, x in enumerate((-1.5, -0.5, 0.5, 1.5)):
            p = Process(color=ABCD_COLORS[i], label="ABCD"[i]).scale(0.5)
            place_on(p, [x, -0.6, 0])
            ps.add(p)
        homes = [base_point(p).copy() for p in ps]
        jl = Text("the OS juggles too", font_size=24, color=DIM).next_to(cpu, UP, buff=0.4)
        with self.narrate("That's the name for a host of problems that show up when you work on many things at "
                          "once. The OS itself ran into them first. It's juggling processes, after all."):
            self.play(FadeIn(cpu), FadeIn(ps), FadeIn(jl), run_time=0.6)
            for k in (0, 1, 3, 2, 0, 1):
                self.play(hop_to(ps[k], cpu.slot_point(), run_time=0.35))
                self.play(hop_to(ps[k], homes[k], run_time=0.3))
            self.play(FadeOut(VGroup(cpu, ps, jl)), run_time=0.5)

        # S13.3
        self.say("Today, any multi-threaded program meets them too.", th.show("multi-threaded", hold=0.8))

        # S13.4 thread: two blobs inside one program
        outline = DashedVMobject(RoundedRectangle(width=4.6, height=2.4, corner_radius=0.3), num_dashes=50)
        outline.set_stroke(TEXT, 3).move_to([3.2, -0.1, 0])
        o_lab = Text("one program · one memory", font_size=22, color=TEXT).next_to(outline, UP, buff=0.1)
        t1, t2 = placed_threads()
        t1.move_to(outline.get_center() + LEFT * 0.8)
        t2.move_to(outline.get_center() + RIGHT * 0.8)
        self.say("A thread is like a function running in the same memory as other functions, with more than "
                 "one active at a time.",
                 Create(outline, run_time=0.8), FadeIn(o_lab), FadeIn(t1, scale=0.5), FadeIn(t2, scale=0.5),
                 Succession(Wait(1.0), th.show("thread", hold=0.8)))

        # S13.5 code, threads to positions, taps
        code, title = threads_code()
        cell = counter_cell("0")
        links = VGroup(*[DashedLine(base_point(t) * 0 + p + UP * 0.95, cell.box.get_bottom(), dash_length=0.1)
                         .set_stroke(DIM, 2) for t, p in ((t1, T_POS[0]), (t2, T_POS[1]))])
        with self.narrate("This program creates two threads. Each one adds one to a shared counter, over and over, "
                          "loops times."):
            self.play(FadeIn(code.background), Write(code.code_lines), FadeIn(title), run_time=1.4)
            self.play(FadeOut(outline), FadeOut(o_lab), hop_to(t1, T_POS[0], run_time=0.6),
                      hop_to(t2, T_POS[1], run_time=0.6))
            self.play(FadeIn(cell), Create(links), run_time=0.6)
            for k, t in enumerate((t1, t2, t1, t2)):
                plus = Text("+1", font_size=24, color=(T1_COLOR, T2_COLOR)[k % 2], weight=BOLD)
                plus.move_to(links[k % 2].get_center())
                new = Text(str(k + 1), font=MONO_FONT, font_size=36, color=TEXT, weight=BOLD).move_to(cell.box)
                self.play(FadeIn(plus, shift=UP * 0.3), Transform(cell.val, new), run_time=0.4)
                self.play(FadeOut(plus, shift=UP * 0.3), run_time=0.2)

        # S13.6
        term = threads_terminal()
        tr = ValueTracker(4)
        spin_val = always_redraw(lambda: Text(f"{int(tr.get_value())}", font=MONO_FONT, font_size=36, color=TEXT,
                                              weight=BOLD).move_to(cell.box))
        with self.narrate("Loops equals a thousand. Two threads, a thousand each. The final value?"):
            self.play(FadeIn(term), run_time=0.4)
            self.play(term.type("./threads 1000"))
            self.remove(cell.val)
            self.add(spin_val)
            self.play(tr.animate.set_value(1700), run_time=2.0, rate_func=linear)

        # S13.7
        self.say("Two thousand!", stu.change("excited"), tr.animate(run_time=1.0, rate_func=linear).set_value(1990),
                 min_time=1.2)

        # S13.8
        ok = tick_mark(0.35).next_to(cell.box, RIGHT, buff=0.2)
        with self.narrate("Two thousand. Correct."):
            self.play(tr.animate.set_value(2000), run_time=0.3)
            self.remove(spin_val)
            cell.val = Text("2000", font=MONO_FONT, font_size=36, color=GOOD, weight=BOLD).move_to(cell.box)
            self.add(cell.val)
            self.play(Create(ok), term.print("Final value : 2000"), run_time=0.5)

        # S13.9
        exp = Text("expected: 200000", font_size=20, color=DIM).next_to(cell.lab, UP, buff=0.12)
        tr.set_value(0)
        with self.narrate("Now loops equals a hundred thousand. We expect two hundred thousand…"):
            self.play(FadeOut(ok), term.type("./threads 100000"), run_time=0.9)
            self.play(FadeIn(exp, shift=RIGHT * 0.2), run_time=0.4)
            self.remove(cell.val)
            self.add(spin_val)
            self.play(tr.animate.set_value(130000), run_time=1.8, rate_func=linear)

        # S13.10
        with self.narrate("and we get 143,012."):
            self.play(tr.animate.set_value(143012), run_time=0.5)
            self.remove(spin_val)
            cell.val = Text("143012", font=MONO_FONT, font_size=36, color=BAD, weight=BOLD).move_to(cell.box)
            self.add(cell.val)
            self.play(Wiggle(VGroup(cell.box, cell.val), scale_value=1.08, rotation_angle=0.05),
                      term.print("Final value : 143012   // huh??"), run_time=0.8)

        # S13.11
        tr.set_value(0)
        with self.narrate("Run it again: 137,298. Wrong, and wrong differently."):
            self.play(term.type("./threads 100000"), run_time=0.8)
            self.remove(cell.val)
            self.add(spin_val)
            self.play(tr.animate.set_value(137298), run_time=1.4, rate_func=smooth)
            self.remove(spin_val)
            cell.val = Text("137298", font=MONO_FONT, font_size=36, color=BAD, weight=BOLD).move_to(cell.box)
            self.add(cell.val)
            self.play(Wiggle(VGroup(cell.box, cell.val), scale_value=1.08, rotation_angle=0.05),
                      term.print("Final value : 137298   // what the??"), run_time=0.8)

        # S13.12
        self.say("Huh?? It's the same program!", stu.change("frustrated"), FadeOut(exp))
        self.beat(0.6)
