import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


class S13States(Ep04Scene):
    def construct(self):
        self.add_badge()
        self.add_docked_term("file descriptors")
        stu, prof = self.add_corner_chars()
        slot = docked_save_slot()
        d = proc("D", "ready").move_to(P3(0, 0.2))
        self.add(slot, d)
        sd = make_state_diagram()
        for lab in sd.arrow_labels.values():
            lab.set_opacity(0)

        def to_zone(p, pt, expr=None, run_time=0.6, **kw):
            if expr:
                p.set_expression(expr)
            return hop_bottom(p, pt, run_time=run_time, **kw)

        def show_label(name):
            lab = sd.arrow_labels[name]
            lab.set_opacity(1)
            return Write(lab, run_time=0.7)

        run_pt = sd.zone_points("running", 1)[0]

        # S13.1
        with self.narrate("Once it's alive, a process is always in some state. In a simplified view, there are three."):
            self.play(self.term("process state"))
            self.play(Create(sd.zone_group), Write(sd.label_group), FadeIn(sd.deco), run_time=1.5)

        # S13.2
        with self.narrate("Running: it's on a processor, executing instructions."):
            self.play(d.animate.scale(SD_PROC_SCALE), run_time=0.4)
            self.play(to_zone(d, run_pt, "running", run_time=0.7))
            self.play(sd.glow_zone("running"), Create(sd.arrow_group), run_time=0.9)

        # S13.3
        a, b = sd_proc("A"), sd_proc("B")
        rp2 = sd.zone_points("ready", 2)
        bottom_to(a, rp2[0])
        bottom_to(b, rp2[1])
        with self.narrate("Ready: it could run right now, but the OS has chosen to run someone else for the moment."):
            self.play(GrowFromCenter(a), GrowFromCenter(b), run_time=0.6)
            self.play(a.animate(rate_func=there_and_back).shift(UP * 0.12),
                      b.animate(rate_func=there_and_back).shift(UP * 0.12), run_time=0.4)

        # S13.4
        self.say("Blocked: it did something that means it can't run until some event happens.",
                 Indicate(sd.zones["blocked"], color=DIM, scale_factor=1.08, run_time=1.0))

        # S13.5
        disk = Disk(width=0.9, height=0.75).move_to(P3(2.4, -2.6))
        self.say("The classic example is asking the disk for data and waiting for the answer.",
                 FadeIn(disk, shift=UP * 0.3, run_time=0.6))

        # S13.6 scheduled: D -> Ready (descheduled pulses faintly), A -> Running
        rp3 = sd.zone_points("ready", 3)
        with self.narrate("The OS moves processes between ready and running whenever it likes. "
                          "Moving from ready to running is being scheduled."):
            self.play(a.animate.shift(rp3[0] - a.get_bottom()), b.animate.shift(rp3[1] - b.get_bottom()), run_time=0.4)
            self.play(to_zone(d, rp3[2], "ready", run_time=0.8),
                      sd.arrows["descheduled"].animate(rate_func=there_and_back).set_stroke(opacity=0.4), run_time=0.8)
            self.play(to_zone(a, run_pt, "running", run_time=0.8), sd.pulse_arrow("scheduled", run_time=0.8))
            self.play(b.animate.shift(rp2[0] - b.get_bottom()), d.animate.shift(rp2[1] - d.get_bottom()),
                      show_label("scheduled"), run_time=0.7)
            self.play(self.term("scheduled", hold=0.8))

        # S13.7 descheduled: A -> Ready, then D scheduled again
        with self.narrate("Moving from running back to ready is being descheduled."):
            self.play(b.animate.shift(rp3[0] - b.get_bottom()), d.animate.shift(rp3[1] - d.get_bottom()), run_time=0.4)
            self.play(to_zone(a, rp3[2], "ready", run_time=0.8), sd.pulse_arrow("descheduled", run_time=0.8))
            self.play(show_label("descheduled"))
            self.play(self.term("descheduled", hold=0.8))
            self.play(to_zone(d, run_pt, "running", run_time=0.7))
            self.play(b.animate.shift(rp2[0] - b.get_bottom()), a.animate.shift(rp2[1] - a.get_bottom()), run_time=0.4)

        # S13.8 I/O initiate
        blk_pt = sd.zone_points("blocked", 1)[0]
        packet = Square(0.16).set_fill(CPU_COLOR, 1).set_stroke(TEXT, 1).move_to(d.get_right())
        with self.narrate("A running process that starts an I/O becomes blocked."):
            self.play(packet.animate.move_to(disk.top_point()), run_time=0.8)
            self.play(to_zone(d, blk_pt, "blocked", run_time=0.9), sd.pulse_arrow("io_initiate", run_time=0.9))
            self.play(show_label("io_initiate"), sd.unglow_zone("running"))

        # S13.9
        with self.narrate("It stays there until the I/O completes."):
            self.play(disk.spin(2, run_time=1.6), sd.clock.animate.rotate(-PI, about_point=sd.clock[0].get_center()),
                      run_time=1.6)

        # S13.10
        with self.narrate("Then it goes back to ready, and maybe straight to running again, if the OS decides so."):
            self.play(packet.animate.move_to(d.get_right() + RIGHT * 0.1), run_time=0.7)
            self.play(FadeOut(packet), show_label("io_done"), sd.pulse_arrow("io_done"), run_time=0.8)
            self.play(b.animate.shift(rp3[0] - b.get_bottom()), a.animate.shift(rp3[1] - a.get_bottom()), run_time=0.4)
            self.play(to_zone(d, rp3[2], "ready", run_time=0.9))

        # S13.11
        self.say("Why not just let it keep the CPU while it waits?", stu.change("curious", look_at=sd), min_time=2.2)

        # S13.12
        ghost = sd_proc("D", "blocked")
        bottom_to(ghost, run_pt)
        make_translucent(ghost, 0.35, 0.5)
        zz = zz_glyph(0.3, TEXT).next_to(ghost, RIGHT, buff=0.05).shift(UP * 0.2)
        cyc = Integer(0, font_size=30, color=CPU_COLOR, group_with_commas=True)
        cyc_lab = Text("cycles…", font_size=26, color=CPU_COLOR)
        cyc_g = VGroup(cyc, cyc_lab).arrange(RIGHT, buff=0.12).move_to(P3(-4.6, -0.45))
        cyc.add_updater(lambda m: m.next_to(cyc_lab, LEFT, buff=0.12))
        with self.narrate("Because waiting for a disk takes ages in CPU time. The CPU would sit there doing nothing."):
            self.play(prof.change("worried", look_at=sd), FadeIn(ghost), FadeIn(zz), FadeIn(cyc_g), run_time=0.7)
            self.play(ChangeDecimalToValue(cyc, 1000000, run_time=2.2, rate_func=rush_into))
            self.wait(0.8)
            cyc.clear_updaters()
            self.play(FadeOut(ghost), FadeOut(zz), FadeOut(cyc_g), run_time=0.6)
        # end state: A runs; B and D ready
        rp_end = sd.zone_points("ready", 2)
        self.play(to_zone(a, run_pt, "running", run_time=0.7),
                  b.animate.shift(rp_end[0] - b.get_bottom()), d.animate.shift(rp_end[1] - d.get_bottom()))
        self.play(sd.glow_zone("running"), run_time=0.4)
        self.wait(0.4)
