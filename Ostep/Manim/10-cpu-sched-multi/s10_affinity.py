import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common_more import *  # noqa: E402,F401,F403

XA, XB = -2.5, 2.5


def build_affinity_stage():
    c1, c2 = cpu_at(XA, 1.3, "CPU 1"), cpu_at(XB, 1.3, "CPU 2")
    mem = Memory(cells=4, contents=["7", "3", "5", "1"], width=1.2, height=1.6, addresses=False, font_size=20).move_to(P3(0, -2.2))
    bus = Bus(y=BUS_Y, x_range=(-4.4, 4.4), taps=[c1.cache_bottom(), c2.cache_bottom(), mem.get_top()])
    return c1, c2, mem, bus


class S10Affinity(Ep10Scene):
    def construct(self):
        self.world(strip=1, stu="curious", prof="neutral")
        stu, prof = self.stu, self.prof
        pad = Padlock(0.42).move_to(P3(6.2, 2.1))
        pad.scale(1.0)
        c1, c2, mem, bus = build_affinity_stage()
        a = proc("A", "running", 0.5)
        place_on(a, c1.slot_point())
        self.add(pad, c1, c2, mem, bus, a)
        A = COL["A"]

        # S10.1
        self.say("When a process runs on a CPU, it gradually fills that CPU's caches…",
                 c1.warmth(3, A, run_time=2.4), stu.look_at(c1.strip))

        # S10.2
        tlb = ep_tag("TLB → Ep. 19", color=DIM).move_to(P3(-5.0, 0.2))
        self.say("…and its TLBs, which we'll meet in the memory episodes…", FadeIn(tlb, shift=RIGHT * 0.2))

        # S10.3 key term
        warm = VGroup(flame_icon(0.45), label("warm", 24, CPU_COLOR)).arrange(RIGHT, buff=0.12).move_to(P3(-0.1, 0.2))
        with self.narrate("It builds up state. This is called cache affinity: the CPU is warm for that process."):
            self.play(self.term("cache affinity"))
            self.play(FadeIn(warm, shift=LEFT * 0.2), Indicate(c1.strip, color=A, scale_factor=1.1), prof.change("explaining"),
                      FadeOut(tlb), run_time=1.0)

        # S10.4
        fast = stopwatch("fast", 24, CPU_COLOR).move_to(P3(0, 1.5))
        spot_off = P3(-5.0, 0.0)
        with self.narrate("The next time that process runs, it runs faster on the same CPU…"):
            self.play(hop_to(a, spot_off, run_time=0.7), run_time=0.7)
            self.play(a.change("ready"), run_time=0.4)
            self.play(hop_to(a, c1.slot_point(), run_time=0.7), FadeIn(fast, shift=DOWN * 0.2), run_time=0.7)
            self.play(a.change("running"), run_time=0.4)

        # S10.5
        slow = stopwatch("slow", 24, KERNEL_COLOR).move_to(fast)
        with self.narrate("Put it on a different CPU, and it must reload everything, slowly."):
            self.play(hop_to(a, c2.slot_point(), run_time=1.0, height=1.2), FadeOut(warm), run_time=1.0)
            self.play(Transform(fast, slow), run_time=0.5)
            for i in range(3):
                self.play(bus_pulse(bus, mem.get_top(), c2.cache_bottom(), color=A, run_time=0.9),
                          Succession(Wait(0.7), c2.warmth(i + 1, A, run_time=0.3)), run_time=1.0)

        # S10.6
        ok = VGroup(tick_mark(0.3), label("correct", 20, GREEN_OK)).arrange(RIGHT, buff=0.1).move_to(P3(4.7, 0.2))
        gauge = SpeedGauge(0.3, width=1.4, color=KERNEL_COLOR).move_to(P3(4.9, 1.3))
        self.say("It still runs correctly, thanks to coherence, just slower.",
                 FadeIn(ok, shift=LEFT * 0.2), FadeIn(gauge, shift=LEFT * 0.2))

        # S10.7
        pin = pin_icon(0.55).move_to(c1.cpu.get_corner(UL) + P3(0.0, 0.3))
        self.say("So a multiprocessor scheduler should consider cache affinity. When possible, keep a process on the same CPU.",
                 hop_to(a, c1.slot_point(), run_time=1.0, height=1.2), c2.clear(), FadeOut(ok), FadeOut(gauge),
                 FadeOut(fast), Succession(Wait(1.4), FadeIn(pin, shift=DOWN * 0.5)), prof.change("explaining"))
        self.play(a.change("running"), run_time=0.4)
        self.beat(0.4)
