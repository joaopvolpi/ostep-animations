import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


def chip_under(p, size=0.55):
    c = CPU(size=size, label=None, pins=2)
    c.next_to(p, DOWN, buff=0.05)
    return c


class S05MoreCPUs(Ep04Scene):
    def construct(self):
        self.add_badge()
        self.add_docked_term("process")
        stu, prof = self.add_corner_chars("curious", "happy")
        w = build_s04_end()
        a0, b0 = w["a"], w["b"]
        self.add(w["disk"], w["file"], a0, b0, w["brace"], w["blab"])

        # S05.1
        spots = row_positions()
        a = proc("A").move_to(a0)
        b = proc("B").move_to(b0)
        c = proc("C").move_to(P3(7.5, -0.9))
        cpu = CPU(CPU_SIZE).move_to(CPU_HOME)
        with self.narrate("So we have a hundred processes and one CPU. Easy: just buy more CPUs."):
            self.play(FadeOut(VGroup(w["disk"], w["file"], w["brace"], w["blab"])),
                      ReplacementTransform(a0, a), ReplacementTransform(b0, b), run_time=0.8)
            self.play(a.animate.move_to(spots[0]), b.animate.move_to(spots[1]),
                      hop_to(c, base_point(c) + (spots[2] - c.get_center()), run_time=0.8),
                      GrowFromCenter(cpu), run_time=1.0)
            self.play(stu.change("excited", look_at=cpu))
        self.beat(0.8)

        # S05.2
        spread = [P3(-3, -0.7), P3(0, -0.7), P3(3, -0.7)]
        chips = VGroup()
        extras = VGroup()
        for n, p in zip((a, b, c), spread):
            target = n.copy().move_to(p)
            chips.add(chip_under(target))
        extra_spots = [P3(-4.6, 1.7), P3(4.6, 1.7), P3(-5.3, -0.4), P3(5.3, -0.4), P3(-2.6, 1.9), P3(2.6, 1.9)]
        enter_from = [P3(-8, 1.7), P3(8, 1.7), P3(-8, -0.4), P3(8, -0.4), P3(-8, 2.5), P3(8, 2.5)]
        for k, (sp, src) in enumerate(zip(extra_spots, enter_from)):
            e = Process("ready", color=PROCESS_COLORS[(k + 3) % 6]).scale(0.55).move_to(src)
            ch = chip_under(e.copy().move_to(sp), 0.4)
            extras.add(VGroup(e, ch))
        counter = VGroup(Text("CPUs needed:", font_size=28, color=CPU_COLOR),
                         Integer(3, font_size=34, color=CPU_COLOR)).arrange(RIGHT, buff=0.15, aligned_edge=DOWN)
        counter.move_to(P3(0, 2.45))
        num = counter[1]
        with self.narrate("One CPU per process? We'd need a hundred chips…"):
            self.play(prof.change("worried", look_at=cpu),
                      a.animate.move_to(spread[0]), b.animate.move_to(spread[1]), c.animate.move_to(spread[2]),
                      cpu.animate.move_to(P3(0, 1.0)).scale(0.7),
                      run_time=0.8)
            self.play(LaggedStart(*[GrowFromCenter(ch) for ch in chips], lag_ratio=0.2), FadeIn(counter), run_time=0.8)
            anims = []
            for (e, ch), sp in zip(extras, extra_spots):
                anims.append(Succession(e.animate(run_time=0.5).move_to(sp), GrowFromCenter(ch, run_time=0.3)))
            self.play(LaggedStart(*anims, lag_ratio=0.15),
                      ChangeDecimalToValue(num, 100, run_time=1.8), run_time=1.8)
        self.beat(1.0)

        # S05.3
        times = Text("×1000", font_size=40, color=KERNEL_COLOR, weight="BOLD").next_to(counter, RIGHT, buff=0.3)
        swarm = VGroup(chips, extras)
        with self.narrate("…then a thousand when you open more tabs. That doesn't scale."):
            num.set_color(KERNEL_COLOR)
            self.play(ChangeDecimalToValue(num, 1000, run_time=1.4), counter[0].animate(run_time=1.4).set_color(KERNEL_COLOR))
            self.play(Indicate(counter, color=KERNEL_COLOR), run_time=0.8)
            self.play(swarm.animate(run_time=0.6).scale(0.8, about_point=P3(0, 0.3)))
            self.play(FadeOut(swarm, scale=0.5, shift=DOWN * 1.0), FadeOut(counter),
                      cpu.animate.scale(1 / 0.7).move_to(CPU_HOME),
                      a.animate.move_to(spots[0]), b.animate.move_to(spots[1]), c.animate.move_to(spots[2]),
                      run_time=1.0)
            self.play(stu.change("sad", look_at=cpu), prof.change("neutral"))
        self.beat(1.8)
