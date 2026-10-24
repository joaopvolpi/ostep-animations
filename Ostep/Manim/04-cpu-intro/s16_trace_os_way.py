import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


def numbered_marker(tl, boundary, n, color=TEXT):
    m = tl.boundary_marker(boundary, None, color=color, extra=0.2)
    c = Circle(radius=0.18).set_fill(BG, 1).set_stroke(color, 2.5).next_to(m, UP, buff=0.05)
    t = Text(str(n), font_size=24, color=color, weight="BOLD").move_to(c)
    return VGroup(m, c, t)


class S16TraceOSWay(Ep04Scene):
    def construct(self):
        self.add_badge()
        self.add_docked_term("descheduled")
        stu, prof = self.add_corner_chars("neutral", "worried")
        slot = docked_save_slot()
        t = build_s15_end()
        cpu, p0, p1, tl, sd, d0, d1 = (t[k] for k in ("cpu", "p0", "p1", "tl", "sd", "d0", "d1"))
        disk, bar, packet, comp, iotag = (t[k] for k in ("disk", "bar", "packet", "comp", "iotag"))
        comp.move_to(P3(2.75, 0.3))
        self.add(slot, sd, cpu, p0, p1, tl, disk, bar, packet, comp, iotag)

        # S16.1
        with self.narrate("Instead, the OS notices that process zero is blocked and isn't using the CPU, "
                          "so it runs process one."):
            self.play(hop_bottom(p0, TRACE_BLOCK_SPOT, run_time=0.7), sd.move_dot(d0, "blocked"))
            self.play(p0.change("blocked"), run_time=0.3)
            p1.set_expression("running")
            self.play(hop_seat(p1, cpu, run_time=0.7), sd.move_dot(d1, "running"))

        # S16.2
        with self.narrate("Ticks four, five and six: process one runs while zero waits on the disk."):
            self.play(comp.change("busy"), run_time=0.4)
            for k in range(4, 7):
                self.play(tl.fill_column(k, {"P0": "blocked", "P1": "running"}, cpu="busy", run_time=0.55),
                          disk.spin(0.5, run_time=0.55))

        # S16.3
        with self.narrate("At tick seven the I/O completes, and process zero moves to ready."):
            self.play(packet.animate.move_to(p0.get_right()), run_time=0.6)
            p0.set_expression("ready")
            self.play(FadeOut(packet), FadeOut(iotag), hop_bottom(p0, TRACE_P0_SPOT, run_time=0.7),
                      sd.move_dot(d0, "ready"))
            self.play(tl.fill_column(7, {"P0": "ready", "P1": "running"}, cpu="busy", run_time=0.55))

        # S16.4
        with self.narrate("Process one finishes at tick eight."):
            self.play(tl.fill_column(8, {"P0": "ready", "P1": "running"}, cpu="busy", run_time=0.55),
                      comp.animate(rate_func=there_and_back).shift(UP * 0.15), run_time=0.55)
            p1.set_expression("done")
            self.play(hop_bottom(p1, TRACE_P1_SPOT, run_time=0.6), sd.remove_dot(d1))
            self.play(p1.animate.set_opacity(0.5), run_time=0.3)

        # S16.5
        busy = Text("CPU busy: 10 / 10", font_size=26, color=CPU_COLOR).next_to(tl.tick_labels, DOWN, buff=0.12)
        with self.narrate("Then process zero runs ticks nine and ten, and is done."):
            p0.set_expression("running")
            self.play(hop_seat(p0, cpu, run_time=0.6), sd.move_dot(d0, "running"))
            for k in (9, 10):
                self.play(tl.fill_column(k, {"P0": "running"}, cpu="busy", run_time=0.5),
                          bar.cells[k - 5].animate(run_time=0.5).set_fill(opacity=0.1))
            p0.set_expression("done")
            self.play(hop_bottom(p0, TRACE_P0_SPOT, run_time=0.6), sd.remove_dot(d0), FadeOut(bar))
            self.play(p0.animate.set_opacity(0.5), Write(busy),
                      comp.animate(rate_func=there_and_back).shift(UP * 0.2), run_time=0.7)

        # S16.6
        blocks = tl.blocks_in(None)
        m1 = numbered_marker(tl, 3, 1)
        m2 = numbered_marker(tl, 7, 2)
        self.say("Notice that the OS just made two decisions.",
                 blocks.animate(run_time=0.8).set_opacity(0.3), FadeIn(m1), FadeIn(m2))

        # S16.7
        chk = check_mark(0.4, GREEN_OK, 8).next_to(m1[1], RIGHT, buff=0.12)
        cpu_456 = tl.blocks_in("CPU", ticks=[4, 5, 6])
        self.say("First, it switched to process one during the I/O. That's clearly good: it kept the CPU busy.",
                 Succession(FadeIn(chk, scale=1.5, run_time=0.5),
                            cpu_456.animate(run_time=0.6).set_opacity(1),
                            Indicate(cpu_456, color=CPU_COLOR, scale_factor=1.15, run_time=0.8)))

        # S16.8
        qm = Text("?", font_size=56, color=TEXT, weight="BOLD").next_to(m2[1], LEFT, buff=0.2)
        self.say("Second, when the I/O finished, it did not switch back to process zero right away.",
                 FadeIn(qm, scale=1.6, run_time=0.6))

        # S16.9
        ghost = tl.ghost_blocks([("P0", 7, "running"), ("P0", 8, "running"), ("P1", 7, "ready"), ("P1", 8, "ready"),
                                 ("P1", 9, "running"), ("P1", 10, "running")], opacity=0.55)
        alt = Text("the other choice", font_size=20, color=DIM).next_to(ghost, UP, buff=0.5).shift(RIGHT * 0.9)
        with self.narrate("It let process one finish first. Was that a good choice?"):
            self.play(FadeIn(ghost), FadeIn(alt), run_time=0.7)
            self.wait(1.4)
            self.play(FadeOut(ghost), FadeOut(alt), run_time=0.6)

        # S16.10
        self.say("Uh… depends?", stu.change("confused", look_at=tl), min_time=1.6)

        # S16.11
        whistle = whistle_icon(0.75).move_to(P3(-4.85, 1.55))
        wlab = Text("scheduler", font_size=22, color=TEXT).next_to(whistle, DOWN, buff=0.08)
        with self.narrate("That's the right answer more often than you'd think. Decisions like these are made by "
                          "the OS's scheduler…"):
            self.play(prof.change("happy", look_at=stu), run_time=0.6)
            self.wait(1.4)
            self.play(self.note("scheduler"))
            self.play(FadeIn(whistle, scale=0.5), FadeIn(wlab), run_time=0.6)

        # S16.12
        ep = ep_tag("→ Ep. 07–10").scale(0.8).next_to(wlab, DOWN, buff=0.1)
        self.say("…and we'll spend several episodes on them.", FadeIn(ep, scale=1.3, run_time=0.5))

        # transition: everything fades except the state diagram, which moves to the S17 spot
        keep = (sd, self.badge, self.terms.docked, stu, prof, slot)
        others = [m for m in self.mobjects if m not in keep]
        target = make_state_diagram()
        target.arrow_label_group.set_opacity(1)
        target.scale(S17_SD_SCALE).move_to(S17_SD_POS)
        self.play(*[FadeOut(m) for m in others], run_time=0.8)
        self.play(Transform(sd, target), stu.change("neutral"), prof.change("neutral"), run_time=1.0)
        self.remove(sd)
        self.add(target)
        self.wait(0.3)
