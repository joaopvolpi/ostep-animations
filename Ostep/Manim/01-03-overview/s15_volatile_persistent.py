import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from manim import *  # noqa: E402,F403
from ostep_lib import *  # noqa: E402,F403
from common import *  # noqa: E402,F403


class S15VolatilePersistent(NarratedScene):
    def construct(self):
        stu, prof = make_hosts("corner", stu_expr="frustrated", prof_expr="explaining")
        th = terms(PERS)
        bdg = badge(CONC)
        self.add(stu, prof, bdg)

        mem = s15_memory()
        disk, files = s15_disk()
        dram = mem.title
        mem.remove(dram)

        # S15.1
        self.say("Third piece: persistence.", bdg.recolor(PERS), FadeIn(VGroup(mem, disk, files)),
                 late(0.3, th.show("persistence", hold=0.8)), stu.change("curious"))

        # S15.2
        self.say("Memory, the DRAM in your computer, is volatile.",
                 FadeIn(dram, shift=DOWN * 0.1), late(0.6, th.note("volatile")))

        # S15.3 power off
        sw = PowerSwitch(0.9).move_to(S15_SWITCH_POS)
        dim = Rectangle(width=16, height=10).set_fill(BG, 0.55).set_stroke(width=0)
        crisp = VGroup(disk, files)
        with self.narrate("Cut the power, or crash, and everything in it is gone."):
            self.play(FadeIn(sw), run_time=0.4)
            self.play(sw.flip(False))
            self.add(dim)
            self.bring_to_front(crisp, sw)
            self.play(FadeIn(dim), run_time=0.4)
            for i in range(6):
                self.play(mem.set_content(i, "", run_time=0.25))
        # S15.4 power back
        glow = VGroup(*[f.page.copy().set_fill(opacity=0).set_stroke(PERS, 8, opacity=0.5) for f in files])
        self.say("So we need hardware and software that store data persistently.",
                 Succession(sw.flip(True), FadeOut(dim, run_time=0.5), FadeIn(glow, run_time=0.5),
                            FadeOut(glow, run_time=0.6)))

        # S15.5 HDD + SSD
        hdd, ssd, fs = s15_extras(disk)
        self.say("The hardware is some kind of I/O device: a hard drive, or more and more often a solid-state drive.",
                 FadeIn(hdd), Succession(Wait(1.2), FadeIn(ssd, shift=LEFT * 0.6)),
                 late(2.0, th.note("I/O device")))

        # S15.6 file system layer
        self.say("The software is the file system. It stores the files you create, reliably and efficiently.",
                 FadeIn(fs, shift=DOWN * 0.3), late(0.6, th.note("file system")))
        self.beat(0.5)
