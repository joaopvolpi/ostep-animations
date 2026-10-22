import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403

# S20's final timeline (see SCHEDULE in s20): per tick, the running process and the blocked set
S20_TICKS = [("A", "D"), ("B", "D"), ("C", "D"), ("D", ""), ("A", ""), ("B", "A"), ("C", "A"), ("D", ""),
             ("A", ""), ("B", "")]


def build_s20_end():
    w = build_s20_world()
    ps, cpu, q, cards, tl = w["ps"], w["cpu"], w["q"], w["cards"], w["tl"]
    for n in "ABCD":
        ps[n].set_expression("ready")
    ps["B"].set_expression("running")
    seat(ps["B"], cpu)
    q.items = []
    q.place(ps["C"], ps["D"], ps["A"])
    for n, st in zip("ABCD", ("ready", "running", "ready", "ready")):
        cards[n].set_field_now("state", st)
    for k, (run, blk) in enumerate(S20_TICKS, start=1):
        for n in "ABCD":
            tl.set_block(n, k, "running" if n == run else "blocked" if n in blk else "ready")
    laptop = w["laptop"]
    laptop.lid.set_fill(TEXT, 0.1)
    gears = GearPair(radius=0.22).move_to(cpu.get_right() + RIGHT * 0.55 + UP * 0.1)
    spot = Spotlight(height=1.1, spread=0.32).move_beam_to(q.slot_point(1) + UP * 0.02)
    glow = Circle(radius=0.75).move_to(cpu).set_fill(CPU_COLOR, 0.18).set_stroke(CPU_COLOR, 3, opacity=0.6)
    world = VGroup(glow, laptop, w["counter"], cpu, q, w["disk"], *ps.values(), *cards.values(), w["list_lab"],
                   w["brace"], tl, gears, spot)
    return world


class S21Recap(Ep04Scene):
    def construct(self):
        self.add_badge()
        world = build_s20_end()
        self.add(world)

        # S21.1
        header = Text("Recap", font_size=44, color=VIRT, weight="BOLD").move_to(P3(-6.0, 2.85), aligned_edge=LEFT)
        self.say("So, today:", FadeOut(world, run_time=0.8), Succession(Wait(0.4), Write(header, run_time=0.6)),
                 min_time=1.6)

        items = [
            "1.  A process is a running program.",
            "2.  Time sharing the CPU creates the illusion of many CPUs, at the cost of performance.",
            "3.  Mechanisms answer how; policies answer which.",
            "4.  A process is its machine state: address space, registers, open files.",
            "5.  Processes move between running, ready and blocked, and the OS tracks them all in the process list.",
        ]
        lines = VGroup()
        for s in items:
            wrapped = wrap_text(s, 7.6, 28)
            t = Text(wrapped, font_size=28, color=TEXT, line_spacing=0.75)
            lines.add(t)
        lines.arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to(P3(-6.0, 2.3), aligned_edge=UL)
        if lines.get_bottom()[1] < -3.3:
            lines.scale_to_fit_height(5.5).move_to(P3(-6.0, 2.3), aligned_edge=UL)

        ix = 4.6

        def at_line(m, i):
            m.move_to(P3(ix, lines[i].get_y()))
            return m

        # icons
        f = FileIcon(width=0.45).move_to(P3(ix - 0.6, 0))
        p = proc("A", scale=0.5)
        ic1 = VGroup(f, p)
        f.move_to(P3(ix - 0.5, lines[0].get_y()))
        p.move_to(P3(ix + 0.5, lines[0].get_y()))
        arrow1 = Arrow(f.get_right(), p.get_left(), buff=0.1, stroke_width=3, color=DIM,
                       max_tip_length_to_length_ratio=0.3)
        mini_tl = Timeline(["A", "B", "C"], ticks=6, colors=[COL[n] for n in "ABC"], x_range=(ix - 1.0, ix + 1.0),
                           top=lines[1].get_y() + 0.22, row_height=0.14, row_step=0.22, tick_labels=False,
                           label_font=12)
        for t in range(1, 7):
            for r, n in enumerate("ABC"):
                mini_tl.set_block(n, t, "running" if (t - 1) % 3 == r else "ready")
        gear = GearPair(radius=0.25)
        spot = Spotlight(height=0.7, spread=0.25)
        ic3 = VGroup(gear, spot).arrange(RIGHT, buff=0.4)
        at_line(ic3, 2)
        ic4 = at_line(save_slot(0.6), 3)
        sd = make_state_diagram()
        sd.scale(0.2)
        card = PCBCard("A", COL["A"], [("state", "ready")], width=1.5, height=0.42, cols=1, font_size=12,
                       header_width=0.3, title_font=16)
        ic5 = VGroup(sd, card).arrange(RIGHT, buff=0.25)
        at_line(ic5, 4)

        # S21.2
        with self.narrate("A process is a running program. The OS brings a lifeless program to life."):
            self.play(Write(lines[0]), run_time=1.0)
            self.play(FadeIn(f), run_time=0.3)
            self.play(GrowArrow(arrow1), TransformFromCopy(f, p), run_time=0.8)

        # S21.3
        self.say("Time sharing the CPU creates the illusion of many CPUs, at the cost of performance.",
                 Write(lines[1], run_time=1.4), FadeIn(mini_tl, run_time=1.0))

        # S21.4
        self.say("Mechanisms answer how; policies answer which.",
                 Write(lines[2], run_time=1.0), FadeIn(ic3, run_time=0.8))

        # S21.5
        self.say("A process is its machine state: address space, registers, open files.",
                 Write(lines[3], run_time=1.2), FadeIn(ic4, run_time=0.8))

        # S21.6
        self.say("Processes move between running, ready and blocked, and the OS tracks them all in the process list.",
                 Write(lines[4], run_time=1.6), FadeIn(ic5, run_time=0.8))
        self.beat(1.5)
        self.play(FadeOut(self.badge), run_time=0.6)
