import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403
from s16_baby_proofing import build_end as s16_end  # noqa: E402

RECAP = [
    "1.  Limited direct execution: run programs directly for speed, within limits set up by the OS and the hardware.",
    "2.  User and kernel mode protect the machine. Programs reach the kernel only through system calls: trap in, "
    "return-from-trap out.",
    "3.  The trap table, installed at boot, is the only place a trap can go.",
    "4.  The timer interrupt lets the OS regain control, even from a process that never cooperates.",
    "5.  A context switch saves one process's registers and restores another's.",
]
SAY = [
    "Limited direct execution: run programs directly for speed, within limits set up by the OS and the hardware.",
    "User and kernel mode protect the machine. Programs reach the kernel only through system calls: trap in, "
    "return-from-trap out.",
    "The trap table, installed at boot, is the only place a trap can go.",
    "The timer interrupt lets the OS regain control, even from a process that never cooperates.",
    "A context switch saves one process's registers and restores another's.",
]


def recap_lines():
    lines = VGroup(*[Text(wrap_text(s, 8.0, 24), font_size=24, color=TEXT, line_spacing=0.75) for s in RECAP])
    lines.arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to(P3(-6.2, 2.4), aligned_edge=UL)
    if lines.get_bottom()[1] < -3.3:
        lines.scale_to_fit_height(5.6).move_to(P3(-6.2, 2.4), aligned_edge=UL)
    return lines


def recap_header():
    return Text("Recap", font_size=44, color=VIRT, weight=BOLD).move_to(P3(-6.2, 3.0), aligned_edge=LEFT)


def icons_for(lines):
    ic = []
    chip = CPU(0.55, label=None, pins=2)
    fence = fence_glyph(0.9).next_to(chip, DOWN, buff=0.08)
    ic.append(VGroup(chip, fence))
    dl = DashedLine(P3(-0.7, 0), P3(0.7, 0), dash_length=0.1).set_stroke(TEXT, 2)
    ar1 = Arrow(P3(-0.3, 0.4), P3(-0.3, -0.4), buff=0, color=KERNEL_COLOR, stroke_width=4, tip_length=0.15)
    ar2 = Arrow(P3(0.3, -0.4), P3(0.3, 0.4), buff=0, color=USER_COLOR, stroke_width=4, tip_length=0.15)
    ic.append(VGroup(dl, ar1, ar2))
    tt = TrapTable(filled=3, width=3.4, height=1.6).scale(0.42)
    lk = padlock_icon(0.3, KERNEL_COLOR).move_to(tt.get_corner(UR))
    ic.append(VGroup(tt, lk))
    clk = AlarmClock(0.3, boxed=False)
    pr = proc("A", "running", scale=0.3, label=None).next_to(clk, RIGHT, buff=0.3)
    ic.append(VGroup(clk, pr))
    sl = save_slot(0.55)
    sa = Arrow(sl.get_left() + LEFT * 0.7, sl.get_left() + LEFT * 0.1, buff=0, color=COL["A"], stroke_width=4, tip_length=0.14)
    sb = Arrow(sl.get_right() + RIGHT * 0.1, sl.get_right() + RIGHT * 0.7, buff=0, color=COL["B"], stroke_width=4, tip_length=0.14)
    ic.append(VGroup(sa, sl, sb))
    for g, l in zip(ic, lines):
        g.move_to(P3(4.6, l.get_center()[1]))
    return ic


def build_end():
    lines = recap_lines()
    return dict(header=recap_header(), lines=lines, icons=icons_for(lines))


class S17Recap(Ep06Scene):
    def construct(self):
        self.add_badge()
        stu, prof = corner_chars(True, "neutral", "neutral")
        d = s16_end()
        r, m = d["r"], d["m"]
        term = self.add_docked_term("limited direct execution")
        self.add(m, *r.values(), stu, prof)
        header = recap_header()
        lines = recap_lines()
        icons = icons_for(lines)

        # S17.1
        self.say("So, today:",
                 AnimationGroup(FadeOut(VGroup(m, *r.values()), run_time=1.0), FadeIn(header, shift=RIGHT * 0.3)))
        for i in range(5):
            if i == 4:
                self.say(SAY[i], Succession(FadeIn(lines[i], shift=RIGHT * 0.3), FadeIn(icons[i], scale=1.3)))
            else:
                self.say(SAY[i], Succession(FadeIn(lines[i], shift=RIGHT * 0.3), FadeIn(icons[i], scale=1.3)))
        self.beat(1.5)
        self.play(FadeOut(self.badge), FadeOut(term))
