import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


class S15TraceJustWait(Ep04Scene):
    def construct(self):
        self.add_badge()
        self.add_docked_term("descheduled")
        stu, prof = self.add_corner_chars()
        slot = docked_save_slot()
        t = build_trace_world(8)
        cpu, p0, p1, tl, sd, d0, d1 = (t[k] for k in ("cpu", "p0", "p1", "tl", "sd", "d0", "d1"))
        self.add(slot, sd, cpu, p0, p1, tl)

        disk = trace_disk()
        bar = work_bar(P0_IO_BAR, COL["P0"]).next_to(p0, UP, buff=0.12)
        packet = Square(0.14).set_fill(CPU_COLOR, 1).set_stroke(TEXT, 1)

        # S15.1
        with self.narrate("Now make it interesting. Process zero runs for three ticks, then asks the disk for something."):
            self.play(tl.extend(10, x_range=trace_x_range(10)), FadeIn(disk, shift=UP * 0.3),
                      FadeIn(bar), run_time=1.0)
            p0.set_expression("running")
            self.play(hop_seat(p0, cpu, run_time=0.6), bar.animate.next_to(cpu, LEFT, buff=0.25).shift(UP * 0.9),
                      sd.move_dot(d0, "running"))
            for k in range(1, 4):
                self.play(tl.fill_column(k, {"P0": "running", "P1": "ready"}, cpu="busy", run_time=0.45),
                          bar.cells[k - 1].animate(run_time=0.45).set_fill(opacity=0.1))
            packet.move_to(p0.get_right())
            self.add(packet)
            self.play(packet.animate.move_to(disk.top_point() + RIGHT * 0.25), run_time=0.6)

        # S15.2
        tag = io_tag(disk)
        self.say("The I/O will take a few ticks.", FadeIn(tag, run_time=0.4), disk.spin(1.5, run_time=1.4))

        # S15.3
        banner = Text("WHAT IF", font_size=40, color=DIM, weight="BOLD").set_opacity(0.6).move_to(P3(0.9, 2.75))
        with self.narrate("So… we just wait?"):
            self.play(stu.change("curious", look_at=cpu), FadeIn(banner, scale=1.2), run_time=0.7)

        # S15.4
        comp = Computer("idle").scale(0.6).move_to(P3(2.75, 0.3))
        with self.narrate("We could. Watch what happens if we do: three ticks where the CPU does nothing."):
            p0.set_expression("blocked")
            self.play(sd.move_dot(d0, "blocked"), run_time=0.5)
            for k in range(4, 7):
                self.play(tl.fill_column(k, {"P0": "blocked", "P1": "ready"}, cpu="idle", run_time=0.55),
                          disk.spin(0.5, run_time=0.55))
            # S15.5 (Computer snores)
            self.play(FadeIn(comp, shift=UP * 0.3), run_time=0.5)
            self.play(comp.change("sleeping"), run_time=0.6)
            self.wait(1.0)


        # S15.6 (rewind)
        self.play(tl.unfill_ticks([4, 5, 6], run_time=0.8), FadeOut(banner), sd.move_dot(d0, "running"))
        p0.set_expression("running")
        self.play(comp.change("idle"), stu.change("neutral"), run_time=0.6)
        tl.purge()
        self.wait(0.4)
