import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


def chunk(label, w=0.95, h=0.3, color=DIM):
    r = Rectangle(width=w, height=h).set_fill(color, 0.35).set_stroke(color, 2)
    t = Text(label, font_size=16, color=TEXT).move_to(r)
    return VGroup(r, t)


class S11Loading(Ep04Scene):
    def construct(self):
        self.add_badge()
        self.add_docked_term("stack pointer & frame pointer")
        stu, prof = self.add_corner_chars()
        slot = docked_save_slot()
        cpu = CPU(CPU_SIZE).move_to(S10_CPU)
        a = proc("A", "ready")
        seat(a, cpu)
        self.add(slot, cpu, a)

        mem = s11_memory()
        disk = Disk().move_to(S11_DISK_POS)
        cpu_t = cpu.copy().move_to(S11_CPU_POS)
        bus = s11_bus(cpu_t, mem, disk)
        file = s11_file()

        # S11.1
        with self.narrate("Okay, but “create” hides a lot. How does a file on disk actually become a running process?"):
            self.play(stu.change("curious", look_at=cpu), run_time=0.6)
            self.play(hop_to(a, base_point(a) + RIGHT * 2.2, run_time=0.6))
            self.play(a.animate.shift(RIGHT * 6), run_time=0.8)
            self.remove(a)
            self.play(cpu.animate.move_to(S11_CPU_POS), Create(mem.cells), FadeIn(mem.addresses),
                      Create(bus), FadeIn(disk, shift=UP * 1.5), FadeIn(file), run_time=1.4)

        # S11.2
        tag = step_tag(1, "load")
        code_c = chunk("code").next_to(file, RIGHT, buff=0.3).shift(UP * 0.22)
        data_c = chunk("static data").next_to(code_c, DOWN, buff=0.12)
        with self.narrate("Step one: load. Programs start out on disk, or on a flash-based SSD, in an executable format."):
            self.play(FadeIn(tag, shift=DOWN * 0.2), run_time=0.5)
            self.play(self.term("load", size=40, at=S11_TERM_AT, hold=0.6))
            self.play(GrowFromPoint(code_c, file.get_right()), GrowFromPoint(data_c, file.get_right()), run_time=0.6)
            self.play(self.terms.show("executable format", size=36, at=S11_TERM_AT, hold=0.6))

        # S11.3
        start = cpu.get_bottom() + LEFT * 0.4 + DOWN * 0.15
        end = disk.get_left() + UP * 0.2
        no = DashedLine(start, end, dash_length=0.12).set_stroke(TEXT, 2.5)
        no.add_tip(tip_length=0.18)
        x = cross_mark(0.3, KERNEL_COLOR, 8).move_to((start + end) / 2)
        self.say("The CPU can't run instructions sitting on disk.",
                 Succession(Create(no, run_time=0.8), FadeIn(x, scale=2, run_time=0.4)))

        # S11.4
        top_pt = disk.top_point()
        rc, rd = mem.region("code"), mem.region("static data")
        outline = DashedVMobject(SurroundingRectangle(mem.cells, buff=0.12, corner_radius=0.08),
                                 num_dashes=40).set_stroke(COL["D"], 3)
        olab = Text("address space of D", font_size=20, color=COL["D"]).next_to(outline, UP, buff=0.08)

        def load_anim(ch, region, run_time=1.6):
            p = bus.path(top_pt, region.get_center())
            return Succession(ch.animate(run_time=0.3).move_to(top_pt),
                              MoveAlongPath(ch, p, run_time=run_time, rate_func=smooth))

        def land(ch, region, name):
            i = mem.index_of(name)
            return AnimationGroup(FadeOut(ch), region.animate.set_fill(COL["D"], 0.6),
                                  mem.texts[i].animate.set_opacity(1), run_time=0.4)

        with self.narrate("So the OS reads the code and static data, like initialized variables, into memory, "
                          "into the new process's address space."):
            self.play(FadeOut(no), FadeOut(x), run_time=0.4)
            self.play(load_anim(code_c, rc), Succession(Wait(0.4), load_anim(data_c, rd)))
            self.play(land(code_c, rc, "code"), land(data_c, rd, "static data"))
            self.play(Create(outline), FadeIn(olab), run_time=0.8)

        def clear_loaded():
            return AnimationGroup(*[mem.region(n).animate.set_fill(MEM_COLOR, 0.18) for n in ("code", "static data")],
                                  *[mem.texts[mem.index_of(n)].animate.set_opacity(0) for n in ("code", "static data")],
                                  run_time=0.5)

        # S11.5 eager
        label_pos = P3(0.2, 0.35)
        eager = Text("eager", font_size=28, color=TEXT, weight="BOLD").move_to(label_pos)
        big = chunk("code + static data", w=1.3, h=0.62, color=COL["D"]).move_to(file.get_right() + RIGHT * 0.8)
        both = VGroup(rc, rd)
        with self.narrate("Early, simple systems did this eagerly: everything, all at once, before running."):
            self.play(clear_loaded(), FadeIn(eager))
            self.play(FadeIn(big), run_time=0.3)
            self.play(load_anim(big, both, run_time=1.2))
            self.play(FadeOut(big), *[mem.region(n).animate.set_fill(COL["D"], 0.6) for n in ("code", "static data")],
                      *[mem.texts[mem.index_of(n)].animate.set_opacity(1) for n in ("code", "static data")], run_time=0.4)
            self.play(self.term("eagerly", size=40, at=S11_TERM_AT, hold=0.6))

        # S11.6 lazy
        lazy = Text("lazy", font_size=28, color=TEXT, weight="BOLD").move_to(label_pos)
        slice1 = chunk("", w=0.9, h=0.1, color=COL["D"]).move_to(file.get_right() + RIGHT * 0.8)
        slice2 = slice1.copy()
        piece1 = Rectangle(width=rc.width, height=rc.height * 0.35).set_fill(COL["D"], 0.6).set_stroke(width=0)
        piece1.align_to(rc, UP).set_x(rc.get_x())
        piece2 = Rectangle(width=rd.width, height=rd.height * 0.35).set_fill(COL["D"], 0.6).set_stroke(width=0)
        piece2.move_to(rd)
        spark = Text("need this!", font_size=20, color=CPU_COLOR).next_to(rd, LEFT, buff=0.15)
        with self.narrate("Modern systems are lazy. They load pieces of code and data only when the program "
                          "actually needs them."):
            self.play(clear_loaded(), ReplacementTransform(eager, lazy))
            self.add(slice1)
            self.play(load_anim(slice1, piece1, run_time=1.0))
            self.play(FadeOut(slice1), FadeIn(piece1), run_time=0.3)
            self.play(FadeIn(spark, scale=1.4), run_time=0.4)
            self.add(slice2)
            self.play(load_anim(slice2, piece2, run_time=1.0), FadeOut(spark))
            self.play(FadeOut(slice2), FadeIn(piece2), run_time=0.3)
            self.play(self.term("lazily", size=40, at=S11_TERM_AT, hold=0.6))

        # S11.7
        ep = ep_tag("→ Ep. 18, 21").scale(0.85).next_to(lazy, DOWN, buff=0.12)
        self.say("How that works needs paging and swapping, which come later in the series.",
                 FadeIn(ep, scale=1.3, run_time=0.5))

        # S11.8
        with self.narrate("For now, just remember that the bits have to get from disk to memory."):
            self.play(FadeOut(VGroup(lazy, ep, piece1, piece2)),
                      *[mem.region(n).animate.set_fill(COL["D"], 0.6) for n in ("code", "static data")],
                      *[mem.texts[mem.index_of(n)].animate.set_opacity(1) for n in ("code", "static data")],
                      run_time=0.8)
        self.beat(0.8)
