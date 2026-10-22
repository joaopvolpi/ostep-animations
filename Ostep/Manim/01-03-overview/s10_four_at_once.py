import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from manim import *  # noqa: E402,F403
from ostep_lib import *  # noqa: E402,F403
from common import *  # noqa: E402,F403

S10_CPU = np.array([3.2, 1.0, 0])
S10_XS = (1.7, 2.7, 3.7, 4.7)
S10_ROW_Y = -1.3          # base y of the process row (centers ~ -0.8)
S10_TERM = np.array([-3.6, 0.6, 0])
TL = dict(x0=0.8, x1=4.9, y=-2.25, n=9, h=0.36)


def s10_world():
    cpu = CPU(size=1.2).move_to(S10_CPU)
    procs = VGroup()
    for i, x in enumerate(S10_XS):
        p = Process(color=ABCD_COLORS[i], label="ABCD"[i]).scale(0.6)
        place_on(p, [x, S10_ROW_Y, 0])
        procs.add(p)
    tl = mini_timeline(**TL)
    return cpu, procs, tl


class S10FourAtOnce(NarratedScene):
    def construct(self):
        stu, prof = make_hosts("corner", stu_expr="bored", prof_expr="happy")
        code, title = s09_code()
        term = s09_terminal()
        th = terms(VIRT)
        th.at = np.array([-2.4, 3.0, 0])
        th.size = 44
        bdg = badge(VIRT)
        self.add(stu, prof, bdg, code, title, term, set_docked(th, "virtual"))

        cpu, procs, tl = s10_world()
        times = Text("×1", font_size=26, color=CPU_COLOR, weight=BOLD).next_to(cpu, LEFT, buff=0.25)

        # S10.1
        self.play(FadeOut(VGroup(code, title)), term.animate.scale(5 / 5.6).move_to(S10_TERM), run_time=0.8)
        with self.narrate("Now let's run four of them at once: A, B, C and D."):
            self.play(term.pop(), run_time=0.1)
            self.play(term.type("./cpu A & ./cpu B & ./cpu C & ./cpu D &", run_time=1.4))
            for i in range(4):
                self.play(term.print(f"[{i + 1}] {7353 + i}", color=DIM), FadeIn(procs[i], shift=UP * 0.3, scale=0.6),
                          run_time=0.35)

        # S10.2
        self.say("One processor.", GrowFromCenter(cpu), FadeIn(times), min_time=1.4)

        # S10.3 A B D C A B D C A
        self.add(tl)
        slots = VGroup()
        homes = [base_point(p).copy() for p in procs]
        on_cpu = None
        with self.narrate("And yet: A, B, D, C, A, B, D, C…"):
            for k, letter in enumerate(CPU_ORDER):
                i = "ABCD".index(letter)
                rt = 0.8 if k < 4 else 0.45
                anims = []
                if on_cpu is not None:
                    anims.append(hop_to(procs[on_cpu], homes[on_cpu], run_time=rt * 0.45))
                self.play(*anims, hop_to(procs[i], cpu.slot_point(), run_time=rt * 0.45)) if anims else \
                    self.play(hop_to(procs[i], cpu.slot_point(), run_time=rt * 0.45))
                if on_cpu is not None:
                    procs[on_cpu].set_expression("ready")
                procs[i].set_expression("running")
                s = timeline_slot(tl, k, ABCD_COLORS[i])
                slots.add(s)
                self.play(term.print(letter), FadeIn(s, shift=RIGHT * 0.1), run_time=rt * 0.55)
                on_cpu = i
            # A goes back down at the end
            self.play(hop_to(procs[on_cpu], homes[on_cpu], run_time=0.3))
            procs[on_cpu].set_expression("ready")

        # S10.4
        self.say("All four seem to be running at the same time.", stu.change("surprised", look_at=cpu))
        self.say("Wait. One CPU, four programs, all running?", min_time=2.0)

        # S10.5 peach callback
        pch = Peach().scale(0.9).move_to(cpu)
        with self.narrate("That's the peach, for real."):
            self.play(FadeIn(pch, scale=0.6), run_time=0.3)
            self.wait(0.5)
            self.play(FadeOut(pch, scale=1.3), run_time=0.3)

        # S10.6 illusion: virtual CPUs
        vcs = VGroup(*[CPU(size=0.55, label=None).virtual_copy(0.3, 0.7).move_to([x, 2.55, 0]) for x in S10_XS])
        field = VGroup()
        for r, y in enumerate((2.95, 2.25)):
            for x in np.arange(1.0, 5.6, 0.42):
                field.add(CPU(size=0.3, label=None, pins=2).virtual_copy(0.12, 0.25).move_to([x + 0.2 * r, y, 0]))
        field.set_z_index(-1)
        with self.narrate("The OS, with some help from the hardware, creates an illusion: that the system has "
                          "a very large number of virtual CPUs."):
            self.play(LaggedStart(*[FadeIn(v, shift=DOWN * 0.2) for v in vcs], lag_ratio=0.2), run_time=1.0)
            self.play(FadeIn(field, lag_ratio=0.02), run_time=1.4)
            self.play(th.show("illusion", hold=1.0))

        # S10.7
        tag = next_tag("→ Ep. 04–10", 18).next_to(cpu, RIGHT, buff=0.3)
        self.say("This is virtualizing the CPU, and it's the subject of the next several episodes.",
                 th.show("virtualizing the CPU", hold=1.0), FadeIn(tag, shift=LEFT * 0.2))

        # S10.8 B and C bump
        q = question_mark(0.5).next_to(cpu, UP, buff=0.1).shift(LEFT * 0.0)
        bpos, cpos = base_point(procs[1]).copy(), base_point(procs[2]).copy()
        mid = (bpos + cpos) / 2 + UP * 0.9
        with self.narrate("It also raises new questions. If two programs both want to run right now, which one should?"):
            self.play(FadeOut(VGroup(vcs, field)), run_time=0.5)
            self.play(procs[1].animate.move_to(procs[1].get_center() + (mid - bpos) * 0.75 + RIGHT * 0.0),
                      procs[2].animate.move_to(procs[2].get_center() + (mid - cpos) * 0.75), run_time=0.6)
            self.play(Wiggle(VGroup(procs[1], procs[2]), scale_value=1.05, rotation_angle=0.05), FadeIn(q, scale=0.5),
                      run_time=0.6)

        # S10.9 policy: spotlight picks C
        spot = Spotlight(height=2.2, spread=0.45).move_beam_to(base_point(procs[2]))
        with self.narrate("Questions like that are answered by a policy."):
            self.play(th.show("policy", hold=0.8))
            self.play(FadeIn(spot), FadeOut(q), run_time=0.5)
            self.play(hop_to(procs[1], bpos, run_time=0.45))
            self.play(hop_to(procs[2], cpu.slot_point(), run_time=0.5),
                      spot.animate(run_time=0.5).move_beam_to(cpu.slot_point()))
            self.play(procs[2].change("running"), FadeOut(spot), run_time=0.4)

        # S10.10 tiny OS band
        band = RoundedRectangle(width=4.1, height=0.42, corner_radius=0.08).set_fill(KERNEL_COLOR, 0.25)
        band.set_stroke(KERNEL_COLOR, 2.5).move_to([2.85, -2.95, 0])
        band_lab = Text("resource manager", font_size=20, color=TEXT).move_to(band)
        self.say("Deciding them is the OS's job as resource manager.",
                 FadeIn(VGroup(band, band_lab), shift=UP * 0.3))
        self.beat(0.8)
