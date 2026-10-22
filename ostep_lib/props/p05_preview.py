"""Preview sheet for the episode 05 props.

    python -m manim -ql -s ostep_lib/props/p05_preview.py P05PropSheet
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from manim import *  # noqa: E402,F403
from ostep_lib import *  # noqa: E402,F403


def _cap(text, mob):
    t = Text(text, font_size=16, color=DIM).next_to(mob, DOWN, buff=0.08)
    return VGroup(mob, t)


class P05PropSheet(NarratedScene):
    def construct(self):
        # row 1: icons
        icons = VGroup(
            _cap("bolt", bolt_glyph(0.8, CPU_COLOR, "SIGINT")),
            _cap("keycap", VGroup(Keycap("ctrl"), Keycap("c")).arrange(RIGHT, buff=0.1)),
            _cap("handler", handler_box()),
            _cap("shield", shield_arc(0.6, LEFT)),
            _cap("crown", crown_tag()),
            _cap("wrench", wrench_glyph(0.7)),
            _cap("chip", VGroup(program_chip("p3"), program_chip("wc", PROCESS_COLORS[3])).arrange(RIGHT, buff=0.1)),
            _cap("zombie", zombie_mini(0.5)),
        ).arrange(RIGHT, buff=0.35)
        icons.move_to(UP * 3.0)
        icons.scale_to_fit_width(12.8) if icons.width > 12.8 else None
        # row 2: world, code, fd table
        world = ProcessWorld(PROCESS_COLORS[0]).scale(0.55).move_to(LEFT * 5.0 + UP * 0.2)
        cw = CodeWalker('int rc = fork();\nif (rc == 0) {\n  child();\n} else {\n  parent();\n}', font_size=16)
        cw.move_to(LEFT * 1.6 + UP * 0.9)
        b0 = cw.add_bar(PROCESS_COLORS[0], 4)
        b1 = cw.add_bar(PROCESS_COLORS[1], 4)
        fd = FdTable(center=(2.6, -0.2), spacing=0.9).scale(0.6).move_to(RIGHT * 3.0 + UP * 0.6)
        sl = ShellLoop(cx=5.0).scale(0.45).move_to(RIGHT * 5.0 + DOWN * 1.9)
        kp = KernelPipe(center=(0, 0), width=2.4).scale(0.6).move_to(LEFT * 1.0 + DOWN * 2.4)
        mc = MenuCardRows("Process API", ["create", "destroy", "wait", "misc.", "status"], width=2.6, height=2.6,
                          font_size=20).move_to(LEFT * 3.7 + DOWN * 2.0).scale(0.8)
        self.add(icons, world, cw, b0, b1, fd, sl, kp, mc)
        for n in ("exec", "wait"):
            pass
        self.wait(0.1)
