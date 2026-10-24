import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from manim import *  # noqa: E402,F403
from ostep_lib import *  # noqa: E402,F403
from common import *  # noqa: E402,F403
from s16_files_shared import s16_actors, disk_slot  # noqa: E402

IO_C = r'''int fd = open("/tmp/file", O_WRONLY | O_CREAT | O_TRUNC, S_IRWXU);
write(fd, "hello world\n", 12);
close(fd);'''
PROG_BASE = np.array([-4.6, 1.15, 0])
BAND_Y = 0.0
DISK_POS = np.array([2.5, -2.3, 0])
COMP_POS = np.array([-3.3, -2.55, 0])   # spec (-5.4, -2.6) would sit on the Student


def s17_world():
    prog = Process(color=A_COLOR, label="A").scale(0.65)
    place_on(prog, PROG_BASE)
    code = code_block(IO_C, 13).move_to([1.1, 1.95, 0])
    band = RoundedRectangle(width=11.4, height=1.4, corner_radius=0.15).set_fill(KERNEL_COLOR, 0.2)
    band.set_stroke(KERNEL_COLOR, 3).move_to([0.4, BAND_Y, 0])
    band_lab = Text("Operating System", font_size=18, color=TEXT).move_to([-4.25, BAND_Y - 0.3, 0])
    door = RoundedRectangle(width=0.95, height=0.34, corner_radius=0.08).set_fill(BG, 1).set_stroke(KERNEL_COLOR, 2.5)
    door.move_to([PROG_BASE[0], band.get_top()[1], 0])
    door_lab = Text("syscall", font=MONO_FONT, font_size=14, color=TEXT).move_to(door)
    fsb = RoundedRectangle(width=3.4, height=1.1, corner_radius=0.1).set_fill(CARD_FILL, 1).set_stroke(PERS, 3)
    fsb.move_to([-1.3, BAND_Y, 0])
    fs_lab = Text("file system", font_size=20, color=PERS).move_to(fsb.get_corner(UL) + np.array([0.75, -0.2, 0]))
    blocks = VGroup(*[Square(0.18).set_fill(DISK_COLOR, 0.15).set_stroke(DISK_COLOR, 1.5) for _ in range(10)])
    blocks.arrange_in_grid(rows=2, buff=0.05).move_to(fsb.get_center() + np.array([-0.55, -0.15, 0]))
    ledger = journal_icon(0.5).move_to(fsb.get_center() + np.array([1.1, -0.1, 0]))
    drv = RoundedRectangle(width=2.6, height=1.1, corner_radius=0.1).set_fill(CARD_FILL, 1).set_stroke(TEXT, 3)
    drv.move_to([DISK_POS[0], BAND_Y, 0])
    drv_lab = Text("device driver", font_size=20, color=TEXT).move_to(drv)
    disk = Disk(width=1.6, height=1.3).move_to(DISK_POS)
    cable = DashedLine(drv.get_bottom(), disk.top.get_top(), dash_length=0.08).set_stroke(DIM, 2.5)
    dblocks = VGroup(*[Rectangle(width=0.5, height=0.35).set_fill(DISK_COLOR, 0.12).set_stroke(DISK_COLOR, 2)
                       for _ in range(4)]).arrange(RIGHT, buff=0.04).next_to(disk, LEFT, buff=0.35).shift(DOWN * 0.2)
    return dict(prog=prog, code=code, band=band, band_lab=band_lab, door=VGroup(door, door_lab), fsb=fsb,
                fs_lab=fs_lab, blocks=blocks, ledger=ledger, drv=VGroup(drv, drv_lab), disk=disk, cable=cable,
                dblocks=dblocks)


S17_CRUX_Q = "How to store data persistently?"
S17_CRUX_SUB = "Correctly, fast, and reliably, even when hardware and software fail."


def s17_end_world():
    """Exact S17 end state (S18's start): returns (w, extras, strip, blk_point).
    ``w`` is s17_world() with its end-of-scene fills; ``extras`` the later additions."""
    w = s17_world()
    w["blocks"][6].set_fill(DISK_COLOR, 0.9)
    tick = tick_mark(0.2).move_to(w["ledger"].get_corner(UR))
    for a in (w["disk"].spin(1.5, run_time=0.8), w["disk"].spin(0.7, run_time=0.6)):
        finish_now(a)
    hello = Text("hello world", font=MONO_FONT, font_size=11, color=INK)
    hello.scale_to_fit_width(w["dblocks"][1].width * 0.85).move_to(w["dblocks"][1])
    w["dblocks"][1].set_fill(DISK_COLOR, 0.95)
    comp = Computer("idle").scale(0.6).move_to(COMP_POS)
    blk = w["dblocks"][2]
    half_g = Rectangle(width=0.25, height=0.35).set_fill(DISK_COLOR, 0.95).set_stroke(width=0)
    half_r = Rectangle(width=0.25, height=0.35).set_fill(BAD, 0.9).set_stroke(width=0)
    half_g.move_to(blk.get_center() + LEFT * 0.125)
    half_r.move_to(blk.get_center() + RIGHT * 0.125)
    j = journal_icon(0.5).move_to([3.75, -1.15, 0])
    cw = cow_icon(0.5).move_to([5.0, -1.15, 0])
    jl = VGroup(Text("journal", font_size=14, color=DIM), Text("→ Ep. 42", font_size=14, color=DIM)).arrange(DOWN, buff=0.04)
    cl = VGroup(Text("copy-on-write", font_size=14, color=DIM), Text("→ Ep. 42", font_size=14, color=DIM)).arrange(DOWN, buff=0.04)
    jl.next_to(j, DOWN, buff=0.08)
    cl.next_to(cw, DOWN, buff=0.08)
    note = sticky_note("later!", 0.6).next_to(blk, UP, buff=0.05)
    strip = CruxCard(S17_CRUX_Q, S17_CRUX_SUB, accent=PERS).strip()
    extras = VGroup(tick, hello, comp, half_g, half_r, j, jl, cw, cl, note)
    return w, extras, strip, blk.get_center()


class S17SyscallsCrash(NarratedScene):
    def construct(self):
        stu, prof = make_hosts("corner", stu_expr="curious", prof_expr="explaining")
        th = terms(PERS)
        th.at = np.array([-2.6, 3.0, 0])
        th.size = 44
        bdg = badge(PERS)
        disk0, ps, links = s16_actors()
        ps[2][0].set_expression("running")   # S16 ends with ./main running
        f1 = FileIcon("main.c", color=TEXT, width=0.45, font_size=14).move_to(disk_slot(disk0, 0))
        f2 = FileIcon("main", color=CPU_COLOR, width=0.45, font_size=14).move_to(disk_slot(disk0, 1))
        self.add(stu, prof, bdg, disk0, ps, links, f1, f2, set_docked(th, "shared"))

        w = s17_world()
        prog, code, band, door, disk = w["prog"], w["code"], w["band"], w["door"], w["disk"]
        world = VGroup(band, w["band_lab"], door, w["fsb"], w["fs_lab"], w["blocks"], w["ledger"], w["drv"],
                       w["cable"], w["dblocks"])

        # S17.1
        bars = [line_bar(code, i, PERS, 0.3) for i in range(3)]

        def envelope_drop():
            env = letter_icon(0.4).move_to(prog.get_center() + RIGHT * 0.5)
            return env, Succession(FadeIn(env, run_time=0.2),
                                   env.animate(run_time=0.5).move_to(door.get_center()),
                                   env.animate(run_time=0.5).move_to(w["fsb"].get_center() + UP * 0.2),
                                   FadeOut(env, run_time=0.2))

        with self.narrate("In code, writing \"hello world\" to a file is three system calls: open(), write(), close()."):
            self.play(FadeOut(VGroup(ps, links, f1, f2)), ReplacementTransform(disk0, disk), FadeIn(prog),
                      FadeIn(code.background), Write(code.code_lines), run_time=1.2)
            self.play(FadeIn(world, shift=LEFT * 0.5), run_time=0.8)
            for b in bars:
                env, anim = envelope_drop()
                self.play(FadeIn(b, run_time=0.2))
                self.play(anim)
                self.play(FadeOut(b, run_time=0.2))

        # S17.2 bookkeeping
        chosen = w["blocks"][6]
        with self.narrate("Behind them, the file system figures out where on disk the data goes, keeps its own bookkeeping,"):
            for k in (2, 8, 6):
                self.play(w["blocks"][k].animate.set_fill(CPU_COLOR, 0.6), run_time=0.25)
                if k != 6:
                    self.play(w["blocks"][k].animate.set_fill(DISK_COLOR, 0.15), run_time=0.2)
            self.play(chosen.animate.set_fill(DISK_COLOR, 0.9), run_time=0.3)
            tick = tick_mark(0.2).move_to(w["ledger"].get_corner(UR))
            self.play(Indicate(w["ledger"], color=PERS), Create(tick), run_time=0.6)

        # S17.3 driver -> disk
        req = letter_icon(0.35).move_to(w["fsb"].get_center())
        hello = Text("hello world", font=MONO_FONT, font_size=11, color=INK)
        hello.scale_to_fit_width(w["dblocks"][1].width * 0.85).move_to(w["dblocks"][1])
        with self.narrate("and talks to the device through a device driver."):
            self.play(FadeIn(req), run_time=0.2)
            self.play(req.animate.move_to(w["drv"].get_center()), run_time=0.6)
            self.play(req.animate.move_to(disk.top.get_center()), disk.spin(1.5, run_time=0.8))
            self.play(FadeOut(req), w["dblocks"][1].animate.set_fill(DISK_COLOR, 0.95), FadeIn(hello), run_time=0.5)
            self.play(th.note("device driver"))

        # S17.4 crash mid-write
        comp = Computer("busy").scale(0.6).move_to(COMP_POS)
        half_g = Rectangle(width=0.25, height=0.35).set_fill(DISK_COLOR, 0.95).set_stroke(width=0)
        half_r = Rectangle(width=0.25, height=0.35).set_fill(BAD, 0.9).set_stroke(width=0)
        blk = w["dblocks"][2]
        half_g.move_to(blk.get_center() + LEFT * 0.125)
        half_r.move_to(blk.get_center() + RIGHT * 0.125)
        with self.narrate("And it has to survive a crash in the middle of all that,"):
            self.play(FadeIn(comp, shift=UP * 0.3), run_time=0.4)
            req2 = letter_icon(0.35).move_to(w["drv"].get_center())
            self.play(req2.animate.move_to(disk.top.get_center()), disk.spin(0.7, run_time=0.6))
            self.play(FadeIn(half_g), comp.change("error"), FadeOut(req2), run_time=0.4)
            self.play(FadeIn(half_r, run_time=0.3))
            # a blue-screen-of-death style crash screen, then back to the scene
            bsod = Rectangle(width=16, height=10).set_fill("#1F5FBF", 1).set_stroke(width=0)
            sad = Text(":(", font=MONO_FONT, font_size=120, color="#FFFFFF", weight=BOLD)
            msg = VGroup(*[Text(t, font=MONO_FONT, font_size=26, color="#FFFFFF") for t in (
                "Your computer ran into a problem", "while writing to the disk.",
                "Some of your data may be lost.")]).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
            screen = VGroup(sad, msg).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to([-0.8, 0.2, 0])
            blue = VGroup(bsod, screen).set_z_index(60)
            self.add(blue)
            self.wait(1.6)
            self.play(FadeOut(blue, run_time=0.3))

        # S17.5 journaling / copy-on-write
        j = journal_icon(0.5).move_to([3.75, -1.15, 0])
        cw = cow_icon(0.5).move_to([5.0, -1.15, 0])
        jl = VGroup(Text("journal", font_size=14, color=DIM), Text("→ Ep. 42", font_size=14, color=DIM)).arrange(DOWN, buff=0.04)
        cl = VGroup(Text("copy-on-write", font_size=14, color=DIM), Text("→ Ep. 42", font_size=14, color=DIM)).arrange(DOWN, buff=0.04)
        jl.next_to(j, DOWN, buff=0.08)
        cl.next_to(cw, DOWN, buff=0.08)
        self.say("using tricks like journaling or copy-on-write.",
                 FadeIn(VGroup(j, jl), shift=UP * 0.2), FadeIn(VGroup(cw, cl), shift=UP * 0.2),
                 late(0.4, th.note("journaling · copy-on-write")))

        self.beat(1.5)

        # S17.6 crux
        crux = CruxCard(S17_CRUX_Q, S17_CRUX_SUB, accent=PERS).move_to([0, 0.5, 0])
        self.say_crux(crux, dock=True, run_time=0.9)

        # S17.7
        self.say("So what happens to my file if it crashes halfway?",
                 stu.change("surprised", look_at=blk), Indicate(VGroup(half_g, half_r), color=BAD))

        # S17.8
        note = sticky_note("later!", 0.6).next_to(blk, UP, buff=0.05)
        self.say("Hold that thought for the whole third part of the series.",
                 prof.change("happy"), FadeIn(note, shift=DOWN * 0.3), comp.change("idle"))
        self.beat(0.6)
