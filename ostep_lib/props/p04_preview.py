"""Preview sheet for the episode-04 props.

    python -m manim -ql -s ostep_lib/props/p04_preview.py P04PropSheet
    python -m manim -ql -s ostep_lib/props/p04_preview.py P04IconSheet
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from manim import *  # noqa: E402,F401
from ostep_lib import *  # noqa: E402,F401
from ostep_lib.props.p04_timeline import Timeline  # noqa: E402
from ostep_lib.props.p04_queue import Queue  # noqa: E402
from ostep_lib.props.p04_state_diagram import StateDiagram  # noqa: E402
from ostep_lib.props.p04_pcb import PCBCard  # noqa: E402
from ostep_lib.props.p04_registers import RegisterBank  # noqa: E402
from ostep_lib.props.p04_bus import Bus  # noqa: E402
from ostep_lib.props.p04_icons import *  # noqa: E402,F401


def caption(text, mob, direction=DOWN):
    return Text(text, font_size=18, color=DIM).next_to(mob, direction, buff=0.12)


class P04PropSheet(Scene):
    def construct(self):
        apply_style(self)
        c0, c1, c2 = PROCESS_COLORS[:3]

        # Timeline: every state
        tl = Timeline(["P0", "P1"], ticks=10, colors=[c0, c1], x_range=(-6.0, -0.6), top=3.2,
                      row_height=0.38, row_step=0.5, cpu_row=True, label_font=20, tick_font=16)
        seq0 = ["running"] * 3 + ["blocked"] * 3 + ["ready"] * 2 + ["running"] * 2
        seq1 = ["ready"] * 3 + ["running"] * 5 + [None, None]
        for t in range(1, 11):
            tl.set_block("P0", t, seq0[t - 1])
            if seq1[t - 1]:
                tl.set_block("P1", t, seq1[t - 1])
            tl.set_block("CPU", t, "idle" if t == 10 else "busy")
        self.add(tl, caption("Timeline (Fig 4.4; tick 10 CPU idle for demo)", tl))

        # State diagram
        chip = Square(0.7).set_fill(CPU_COLOR, 1).set_stroke(TEXT, 2)
        sd = StateDiagram(running_icon=chip)
        sd.scale(0.5).move_to(RIGHT * 3.6 + UP * 2.3)
        for z in ("descheduled", "scheduled", "io_initiate", "io_done"):
            pass
        d0 = sd.make_dot(c0, label="0")
        d1 = sd.make_dot(c1, label="1")
        d2 = sd.make_dot(c2)
        sd.place_dot(d0, "running").place_dot(d1, "ready").place_dot(d2, "ready")
        self.add(sd, caption("StateDiagram (+ tracking dots)", sd))

        # Queue with processes
        q = Queue(label="Ready", center=(-3.8, -0.4), slots=3, spacing=1.0)
        ps = [Process(color=c, label=l).scale(0.8) for c, l in zip((c0, c1, c2), "ABC")]
        q.place(*ps)
        self.add(q, *ps)

        # PCB cards
        card = PCBCard("A", c0, [("pid", "1"), ("state", "running"), ("mem", "0x40"), ("files", "3")],
                       col_widths=(0.42, 0.58))
        card2 = PCBCard("C", c2, [("pid", "3"), ("state", "blocked"), ("wait", "disk"), ("files", "4")],
                        col_widths=(0.42, 0.58))
        cards = VGroup(card, card2).arrange(DOWN, buff=0.2).move_to(RIGHT * 0.3 + DOWN * 0.6)
        self.add(cards, caption("PCBCard", cards))

        # Register bank
        regs = RegisterBank([("PC", "0x40"), ("SP", "0xff8"), ("FP", "0xffc"), ("eax", "42"),
                             ("ebx", "7"), ("ecx", "0"), ("edx", "13"), ("esi", "99")], cols=2,
                            title="registers")
        regs.move_to(RIGHT * 4.9 + DOWN * 0.7)
        regs.boxes["PC"].set_stroke(CPU_COLOR, 3).set_fill(CPU_COLOR, 0.25)
        regs.name_texts["PC"].set_color(CPU_COLOR)
        self.add(regs)

        # Bus
        bus = Bus(y=-3.0, x_range=(-6.2, -1.2), taps=[(-5, -2.4), (-2.6, -2.4), (-3.8, -3.5)])
        self.add(bus, caption("Bus", bus, UP).shift(UP * 0.0 + RIGHT * 0.0))

        # Small icons strip
        icons = VGroup(save_slot(0.8), Notepad("To resume A:", 3, width=2.4, font_size=16),
                       whistle_icon(0.6), RoboticArm(l1=0.6, l2=0.5).scale(0.9))
        icons.arrange(RIGHT, buff=0.35).move_to(RIGHT * 2.6 + DOWN * 2.95)
        self.add(icons)


class P04IconSheet(Scene):
    def construct(self):
        apply_style(self)
        items = [
            ("browser", browser_icon()), ("music", music_icon()), ("chat", chat_icon()),
            ("gamepad", gamepad_icon()), ("envelope", envelope_icon()), ("sheet", sheet_music()),
            ("zZ", zz_glyph()), ("bars", mini_bar_chart()), ("tag", tag_icon()), ("dial", dial_icon()),
            ("gauge", SpeedGauge(0.33)), ("save slot", save_slot(0.8)), ("cursor", cursor_icon()),
            ("puff", puff(0.35)), ("info", info_tag("running · 3.2 s")), ("ring", progress_ring(value=0.6)),
            ("keyboard", keyboard_icon()), ("plug", plug_glyph("0 stdin")), ("whistle", whistle_icon()),
            ("exit 0", exit_tag(0)), ("exit 1", exit_tag(1)), ("clock", mini_clock(0.25)),
            ("idle", hatch_rect(0.8, 0.4)), ("check", check_mark()), ("cross", cross_mark()),
            ("ep tag", ep_tag("→ Ep. 06")), ("arm", RoboticArm(l1=0.6, l2=0.5)),
        ]
        cells = VGroup()
        for name, m in items:
            if m.width > 1.6:
                m.scale_to_fit_width(1.6)
            if m.height > 1.1:
                m.scale_to_fit_height(1.1)
            lab = Text(name, font_size=16, color=DIM).next_to(m, DOWN, buff=0.1)
            cells.add(VGroup(m, lab))
        cells.arrange_in_grid(cols=7, buff=(0.35, 0.4)).move_to(DOWN * 0.6)
        menu = MenuCard("Process API", ["Create", "Destroy", "Wait", "Misc. control", "Status"],
                        width=2.6, height=3.0, font_size=20)
        menu.to_corner(UR, buff=0.2)
        cells.scale_to_fit_width(10.5).to_edge(LEFT, buff=0.4)
        self.add(cells, menu, menu.row_highlight(2))
