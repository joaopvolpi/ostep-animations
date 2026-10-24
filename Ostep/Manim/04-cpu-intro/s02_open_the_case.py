import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


def shimmer(vcpus):
    t = ValueTracker(0)

    def upd(g):
        for i, m in enumerate(g):
            m.set_opacity(0.6 + 0.2 * np.sin(2.4 * t.get_value() + 1.3 * i))
    vcpus.add_updater(upd)
    t.add_updater(lambda m, dt: m.increment_value(dt))
    return t


class S02OpenTheCase(Ep04Scene):
    def construct(self):
        w = build_s01_end()
        laptop, icons, tm, counter, num, stu = (w[k] for k in ("laptop", "icons", "tm", "counter", "num", "stu"))
        tm.start_scrolling(2.5)
        self.add(laptop, icons, tm, counter, stu)

        # S02.1
        prof = prof_dialogue("thinking", PROF_SIDE)
        prof.shift(RIGHT * 4)
        board = motherboard()
        with self.narrate("Is it? Let's open the case and count the CPUs."):
            self.play(prof.animate(run_time=0.8).shift(LEFT * 4), FadeOut(icons, run_time=0.8))
            tm.clear_updaters()
            self.play(VGroup(laptop, tm).animate(run_time=1.4).scale(4).set_opacity(0),
                      FadeIn(board, run_time=1.4))
            self.remove(laptop, tm)

        # S02.2
        cpu = CPU(CPU_SIZE).move_to(CPU_HOME)
        cg, _, cnum = counter_group(137, 1)
        crow = VGroup(cg[2], cg[3])
        self.say("We might have many things running at once, but inside the machine there's just one CPU.",
                 GrowFromCenter(cpu, run_time=0.8), FadeIn(crow, run_time=0.6))

        # S02.3
        ghosts = VGroup(*[cpu.virtual_copy().move_to(p) for p in (P3(-2.2, 0.6), P3(2.2, 0.6), P3(0, 2.0))])
        ghosts[2].scale(0.7)
        with self.narrate("Maybe four, or eight. Not a hundred."):
            self.play(LaggedStart(*[FadeIn(g, scale=0.8) for g in ghosts], lag_ratio=0.2, run_time=0.7))
            cnum.set_value(4)
            self.wait(0.5)
            cnum.set_value(8)
            self.wait(0.5)
            self.play(FadeOut(ghosts, run_time=0.6))
            cnum.set_value(1)

        # S02.4
        stream = Line(P3(-4.0, 0.6), cpu.body.get_left()).set_stroke(TEXT, 2.5)
        bit = Dot(radius=0.08, color=CPU_COLOR).move_to(stream.get_start())
        with self.narrate("Each CPU can only follow one stream of instructions at a time."):
            self.play(Create(stream, run_time=0.6))
            self.add(bit)
            for _ in range(2):
                bit.move_to(stream.get_start())
                self.play(MoveAlongPath(bit, stream, run_time=1.0, rate_func=linear))
            self.remove(bit)

        # S02.5
        vcpus = virtual_cpu_row(xs=np.linspace(-3.6, 2.4, 5))
        with self.narrate("And yet every one of those programs behaves as if it had a CPU all to itself."):
            self.play(LaggedStart(*[FadeIn(v, shift=DOWN * 0.2) for v in vcpus], lag_ratio=0.15, run_time=1.5))
            shimmer(vcpus)
            self.wait(1.0)

        # S02.6
        comp = Computer("idle").scale(0.7).move_to(P3(0, -2.6))
        with self.narrate("So… the computer is lying to us?"):
            self.play(stu.change("confused", look_at=cpu), FadeIn(comp, shift=UP * 0.5, run_time=0.7))
            self.play(comp.change("surprised"))

        # S02.7
        self.say("Beautifully. And today we learn how.", prof.change("proud"))
        self.beat(1.0)
