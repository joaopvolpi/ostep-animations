import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


class S17ProcessList(Ep04Scene):
    def construct(self):
        self.add_badge()
        self.add_docked_term("scheduler")
        stu, prof = self.add_corner_chars()
        slot = docked_save_slot()
        w = build_s17_end()
        sd, ps, os_box, os_lab, cards_end = (w[k] for k in ("sd", "ps", "os_box", "os_lab", "cards"))
        self.add(slot, sd)
        k = S17_SD_SCALE

        # start-of-scene positions: A running, B and D ready, C blocked
        a, b, c, d = ps["A"], ps["B"], ps["C"], ps["D"]
        rp2 = sd.zone_points("ready", 2, spacing=sd.radius * 0.62)
        bottom_to(b, rp2[0])
        bottom_to(d, rp2[1])
        c.set_expression("blocked")
        bottom_to(c, sd.zone_points("blocked", 1)[0])

        # S17.1
        with self.narrate("One last question. How does the OS remember all this? It's a program too, and like "
                          "any program, it keeps data structures."):
            self.play(LaggedStart(*[GrowFromCenter(m) for m in (a, b, d, c)], lag_ratio=0.2), run_time=1.2)
            self.play(Create(os_box), Write(os_lab), run_time=1.2)

        cards = {n: pcb_for(n, st, pid, extra) for n, st, pid, extra in
                 (("A", "running", 1, None), ("B", "ready", 2, None), ("D", "ready", 4, None),
                  ("C", "blocked", 3, ("wait", "disk")))}
        for (n, card), y in zip(cards.items(), PCB_YS):
            card.move_to(P3(PCB_X, y))

        # S17.2 + S17.3
        with self.narrate("For each process, it keeps a record. That record is called a Process Control Block, "
                          "or PCB (sometimes a process descriptor)."):
            self.play(GrowFromPoint(cards["A"], a.get_center()), run_time=0.9)
            self.play(self.term("Process Control Block (PCB)", hold=1.4))

        # S17.4
        brace, blab = s17_brace(cards)
        with self.narrate("All of those records together form the process list, also called the task list."):
            self.play(LaggedStart(*[GrowFromPoint(cards[n], ps[n].get_center()) for n in ("B", "D", "C")],
                                  lag_ratio=0.35), run_time=1.5)
            self.play(GrowFromCenter(brace), FadeIn(blab), run_time=0.6)
            self.play(self.note("process list"))

        # S17.5
        with self.narrate("It's the OS's roll call of every process: who's ready, who's running, who's blocked "
                          "and waiting on what,"):
            self.play(cards["B"].indicate_field("state"), cards["D"].indicate_field("state"), run_time=0.8)
            self.play(cards["A"].indicate_field("state"), run_time=0.8)
            self.play(cards["C"].indicate_field("state"), run_time=0.8)
            self.play(cards["C"].indicate_field("wait"), run_time=0.8)

        # S17.6
        disk = Disk(width=0.7, height=0.6).move_to(P3(0.45, -2.6))
        packet = Square(0.14).set_fill(CPU_COLOR, 1).set_stroke(TEXT, 1).move_to(disk.top_point())
        hl = SurroundingRectangle(cards["C"], buff=0.06, corner_radius=0.1).set_stroke(CPU_COLOR, 4)
        rp3 = sd.zone_points("ready", 3, spacing=sd.radius * 0.62)
        with self.narrate("so the right one can be woken when its I/O completes."):
            self.play(FadeIn(disk), FadeIn(packet), run_time=0.4)
            self.play(packet.animate.move_to(os_box.get_left() + DOWN * 1.6), run_time=0.6)
            self.play(Create(hl), FadeOut(packet), run_time=0.5)
            c.set_expression("ready")
            self.play(hop_bottom(c, rp3[2], run_time=0.8),
                      b.animate.shift(rp3[0] - b.get_bottom()), d.animate.shift(rp3[1] - d.get_bottom()),
                      cards["C"].set_field("state", "ready"), cards["C"].set_field("wait", "—"))
            self.play(FadeOut(hl), FadeOut(disk), run_time=0.5)
        self.beat(0.6)
