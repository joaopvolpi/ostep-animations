import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from manim import *  # noqa: E402,F403
from ostep_lib import *  # noqa: E402,F403
from common import *  # noqa: E402,F403

S16_DISK = np.array([0, -2.0, 0])
S16_XS = (-4, 0, 4)
S16_BASE_Y = 0.75
NAMES = ("emacs", "gcc", "./main")


def s16_actors():
    disk = Disk(width=1.8, height=1.5).move_to(S16_DISK)
    ps = VGroup()
    for i, (x, n) in enumerate(zip(S16_XS, NAMES)):
        p = Process(color=PROCESS_COLORS[(i + 1) % 6]).scale(0.7)
        place_on(p, [x, S16_BASE_Y, 0])
        tag = Text(n, font=MONO_FONT, font_size=22, color=TEXT).next_to(p, DOWN, buff=0.1)
        p.tag = tag
        ps.add(VGroup(p, tag))
    links = VGroup(*[Line(p.get_bottom() + DOWN * 0.05, disk.top.get_center(), buff=0.1).set_stroke(DIM, 2)
                     for p in ps])
    links.set_z_index(-1)
    return disk, ps, links


def disk_slot(disk, k):
    return disk.top.get_center() + RIGHT * (k - 0.5) * 0.85 + UP * 0.28


class S16FilesShared(NarratedScene):
    def construct(self):
        stu, prof = make_hosts("corner", stu_expr="curious", prof_expr="explaining")
        th = terms(PERS)
        bdg = badge(PERS)
        mem = s15_memory(values=False)
        disk0, files0 = s15_disk()
        hdd, ssd, fs = s15_extras(disk0)
        self.add(stu, prof, bdg, mem, disk0, files0, hdd, ssd, fs, set_docked(th, "file system"))

        disk, ps, links = s16_actors()
        # S16.1
        ghosts = VGroup()
        for p in ps:
            g = Disk(width=0.7, height=0.6).move_to(p.get_bottom() + DOWN * 0.5)
            make_translucent(g, 0.3, 0.6)
            lab = Text("private disk?", font_size=16, color=DIM).next_to(g, RIGHT, buff=0.08)
            ghosts.add(VGroup(g, lab))
        crosses = VGroup(*[x_mark(0.25).move_to(g[0]) for g in ghosts])
        with self.narrate("Unlike the CPU and memory, the OS does not give each program a private virtual disk."):
            self.play(FadeOut(VGroup(mem, files0, hdd, ssd, fs)), ReplacementTransform(disk0, disk), run_time=0.9)
            self.play(LaggedStart(*[FadeIn(p, shift=DOWN * 0.3) for p in ps], lag_ratio=0.2), run_time=0.9)
            self.play(FadeIn(ghosts), run_time=0.5)
            self.play(Create(crosses), run_time=0.6)
            self.play(FadeOut(ghosts), FadeOut(crosses), run_time=0.5)

        # S16.2
        self.say("Files are meant to be shared.", LaggedStart(*[Create(l) for l in links], lag_ratio=0.2, run_time=1.0),
                 Succession(Wait(0.5), th.show("shared", size=44, hold=0.8)))

        # S16.3 emacs writes main.c
        mainc = FileIcon("main.c", color=TEXT, width=0.45, font_size=14).move_to(ps[0].get_center())
        note = Text("(the book insists on Emacs)", font_size=16, color=DIM).next_to(ps[0], DOWN, buff=0.1)
        with self.narrate("You write main.c in an editor."):
            self.play(FadeIn(mainc, scale=0.3), mainc.animate.shift(RIGHT * 0.9), FadeIn(note), run_time=0.6)
            self.play(mainc.animate.move_to(disk_slot(disk, 0)), run_time=0.9)

        # S16.4 gcc reads, writes main
        exe = FileIcon("main", color=CPU_COLOR, width=0.45, font_size=14).move_to(ps[1].get_center())
        with self.narrate("The compiler reads it and writes an executable."):
            ghost_c = mainc.copy()
            self.play(ghost_c.animate.move_to(ps[1].get_center()).scale(0.6).set_opacity(0), run_time=0.8)
            self.play(Indicate(ps[1][0], color=TEXT, scale_factor=1.08), run_time=0.5)
            self.play(FadeIn(exe, scale=0.3), run_time=0.3)
            self.play(exe.animate.move_to(disk_slot(disk, 1)), run_time=0.8)

        # S16.5 ./main runs; relay arcs
        arcs = VGroup(ArcBetweenPoints(ps[0].get_top() + UP * 0.1, ps[1].get_top() + UP * 0.1, angle=-PI / 4),
                      ArcBetweenPoints(ps[1].get_top() + UP * 0.1, ps[2].get_top() + UP * 0.1, angle=-PI / 4))
        for a in arcs:
            a.set_stroke(PERS, 4)
            a.add_tip(tip_length=0.18)
        with self.narrate("Then you run that. Three programs, passing files along like a relay."):
            ghost_e = exe.copy()
            self.play(ghost_e.animate.move_to(ps[2].get_center()).scale(0.6).set_opacity(0), run_time=0.8)
            self.play(ps[2][0].change("running"), run_time=0.4)
            self.play(Create(arcs[0]), run_time=0.6)
            self.play(Create(arcs[1]), run_time=0.6)
        self.play(FadeOut(arcs), FadeOut(note), run_time=0.4)
        self.beat(0.4)
