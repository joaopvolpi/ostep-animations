import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from manim import *  # noqa: E402,F403
from ostep_lib import *  # noqa: E402,F403
from common import *  # noqa: E402,F403


def virtual_copies(stack, procs):
    """Three translucent CPUs and memories above the programs (S05.7)."""
    vc, vm = VGroup(), VGroup()
    for p in procs:
        x = p.get_center()[0]
        c = CPU(size=0.6, label=None).virtual_copy(0.3, 0.7).move_to([x - 0.4, 2.0, 0])
        m = Memory(cells=4, width=0.42, height=0.75, addresses=False)
        make_translucent(m, 0.3, 0.7)
        m.move_to([x + 0.42, 2.0, 0])
        vc.add(c)
        vm.add(m)
    return vc, vm


class S05EnterOS(NarratedScene):
    def construct(self):
        stu, prof = make_hosts("corner", stu_expr="bored", prof_expr="thinking")
        cpu0, mem0, lists = s04_end_world()
        th = terms(INTRO)
        bdg = badge(INTRO)
        self.add(stu, prof, bdg, cpu0, mem0, lists, set_docked(th, "Von Neumann model"))

        stack = make_stack()
        procs = stack_programs()

        # S05.1
        with self.narrate("While a program runs, a lot of other things are going on, all with one goal: "
                          "making the system easy to use. There's a body of software in charge of that."):
            self.play(ReplacementTransform(cpu0, stack.cpu), ReplacementTransform(mem0, stack.memory),
                      FadeIn(stack.disk, shift=UP * 0.8),
                      *[ReplacementTransform(lists[k], procs[k + 1]) for k in range(2)],
                      FadeIn(procs[0], shift=DOWN * 0.3), run_time=1.6)
            self.play(th.show("easy to use", dock=False, hold=1.0))

        # S05.2
        with self.narrate("It lets you run programs, even many at once."):
            for p in procs:
                self.play(hop_to(p, base_point(p), height=0.4, run_time=0.45))

        # S05.3 tangled lines
        targets = [stack.memory, stack.disk, stack.memory, stack.disk, stack.memory, stack.disk]
        sources = [procs[2], procs[0], procs[0], procs[1], procs[1], procs[2]]
        tangled = VGroup()
        for s_, t_ in zip(sources, targets):
            ln = DashedLine(base_point(s_) + DOWN * 0.05, t_.get_top() + UP * 0.05, dash_length=0.1)
            ln.set_stroke(s_.base_color, 2.5)
            tangled.add(ln)
        self.say("It lets programs share memory and talk to devices.",
                 LaggedStart(*[Create(l) for l in tangled], lag_ratio=0.2, run_time=1.6))

        # S05.4 the OS band untangles
        routes = VGroup()
        for k, (s_, t_) in enumerate(zip(sources, targets)):
            off = (k % 2) * 0.25 - 0.12
            r = stack.route(base_point(s_) + DOWN * 0.05 + RIGHT * off, t_, color=s_.base_color)
            r[1].shift(RIGHT * off * 1.5)
            routes.add(r)
        with self.narrate("That software is the operating system, or OS."):
            self.play(FadeIn(stack.band, shift=RIGHT * 2), FadeIn(stack.band_label, shift=RIGHT * 2), run_time=0.9)
            self.play(Transform(tangled, routes), run_time=1.0)
            self.play(th.show("operating system (OS)", hold=1.0))

        # S05.5
        self.say("Its main technique is called virtualization.", th.show("virtualization", hold=1.0))

        # S05.6-7
        vc, vm = virtual_copies(stack, procs)
        phys = Text("physical", font_size=20, color=TEXT).next_to(stack.cpu, LEFT, buff=0.2)
        virt = Text("virtual", font_size=20, color=CPU_COLOR).next_to(vc[0], LEFT, buff=0.2)
        travel = stack.cpu.copy()
        with self.narrate("The OS takes a physical resource, like the processor, memory or a disk,"):
            self.play(FadeOut(tangled), FadeIn(phys, shift=RIGHT * 0.2), run_time=0.6)
            self.play(travel.animate.move_to(stack.band.get_center() + LEFT * 3).set_opacity(0.6), run_time=1.2)
        with self.narrate("and transforms it into a more general, more powerful, easier-to-use virtual form of itself."):
            self.play(ReplacementTransform(VGroup(travel, travel.copy(), travel.copy()), vc), run_time=1.0)
            self.play(FadeIn(virt), *[Indicate(c, color=CPU_COLOR, scale_factor=1.08) for c in vc], run_time=0.8)
            mt = stack.memory.copy()
            self.play(mt.animate.move_to(stack.band.get_center()).set_opacity(0.6), run_time=0.6)
            self.play(ReplacementTransform(VGroup(mt, mt.copy(), mt.copy()), vm), run_time=0.8)

        # S05.8
        with self.narrate("That's why the OS is sometimes called a virtual machine."):
            self.play(stack.relabel("Operating System · a virtual machine"), run_time=0.6)
            self.play(th.show("virtual machine", hold=1.0))
            self.play(stack.relabel("Operating System"), run_time=0.6)
        self.beat(0.6)
