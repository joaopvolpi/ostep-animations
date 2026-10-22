import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403
from s01_just_run_it import build_end as s01_end  # noqa: E402


def slices_strip(y=2.2, n=6, w=6.0):
    cols = [COL["A"], COL["B"], COL["C"]]
    cell = w / n
    g = VGroup(*[Rectangle(width=cell, height=0.35).set_fill(cols[i % 3], 1).set_stroke(TEXT, 1) for i in range(n)])
    g.arrange(RIGHT, buff=0).move_to(P3(0, y))
    return g


def build_end():
    """S02 end: badge, crux strip, docked term."""
    return dict(strip=strip(CRUX_Q1))


class S02TheCrux(Ep06Scene):
    def construct(self):
        d = s01_end()
        stage = [d[k] for k in ("cpu", "a", "mem", "scr", "disk", "book", "comp", "loop")]
        stu, prof = d["stu"], d["prof"]
        self.add(*stage, stu, prof)
        cs, cp = corner_chars(False, "neutral", "explaining")

        # S02.1
        crux = CruxCard(CRUX_Q1, CRUX_SUB1, accent=VIRT).move_to(P3(0, 0.4))
        self.play(FadeOut(VGroup(*stage), run_time=0.8), AnimationGroup(
            stu.animate.scale(0.75).move_to(cs.get_center()), prof.animate.scale(0.75).move_to(cp.get_center())),
            run_time=1.0)
        self.play(crux.write())
        self.beat(3.0)

        # S02.2
        sl = slices_strip()
        self.say("To virtualize the CPU, the OS has to share it among many processes by time sharing.",
                 crux.dock((0, 3.2, 0), 22), Succession(Wait(1.0), FadeIn(sl, lag_ratio=0.15, run_time=1.5)))

        # S02.3
        p = proc("A", "ready", scale=1.1).move_to(P3(0, 0.0))
        sw = stopwatch_icon(0.45).move_to(P3(-3.6, 0.3))
        sw_l = Text("performance", font_size=26, color=CPU_COLOR).next_to(sw, DOWN, buff=0.15)
        wl = walls_icon(2, 1.0).move_to(P3(3.6, 0.3))
        wl_l = Text("control", font_size=26, color=KERNEL_COLOR).next_to(wl, DOWN, buff=0.15)
        al = Arrow(p.get_left() + LEFT * 0.1, sw.get_right() + RIGHT * 0.2, buff=0, color=CPU_COLOR, stroke_width=6)
        ar = Arrow(p.get_right() + RIGHT * 0.1, wl.get_left() + LEFT * 0.2, buff=0, color=KERNEL_COLOR, stroke_width=6)
        self.say("That raises two challenges, pulling in opposite directions.",
                 AnimationGroup(FadeIn(p), FadeIn(sw), FadeIn(sw_l), FadeIn(wl), FadeIn(wl_l), run_time=1.0),
                 Succession(Wait(1.0), AnimationGroup(GrowArrow(al), GrowArrow(ar))))

        # S02.4
        self.say("The first is performance: no excessive overhead.",
                 Indicate(sw, scale_factor=1.25), Rotate(p, 0.18, about_point=p.get_bottom()))

        # S02.5
        self.say("The second is control: processes must not be able to run forever, or touch what they shouldn't.",
                 Indicate(wl, scale_factor=1.25), Rotate(p, -0.36, about_point=p.get_bottom()))

        # S02.6
        line = Line(P3(-1.2, 0.3), P3(1.2, 0.3)).set_stroke(VIRT, 8)
        self.say("The answer is a technique with a long name: limited direct execution.",
                 AnimationGroup(ReplacementTransform(VGroup(al, ar), line), Rotate(p, 0.18, about_point=p.get_bottom()),
                                FadeOut(sw), FadeOut(wl), FadeOut(sw_l), FadeOut(wl_l)),
                 Succession(Wait(1.0), self.term("limited direct execution", hold=1.0)))

        # S02.7
        direct = Text("direct", font_size=48, color=TEXT).move_to(P3(-2.2, 0.9))
        limited = Text("limited", font_size=48, color=TEXT).move_to(P3(2.2, 0.9))
        cg = CPU(0.6, label=None, pins=2).next_to(direct, DOWN, buff=0.3)
        fg = fence_glyph(1.0).next_to(limited, DOWN, buff=0.3)
        badge = SectionBadge(BADGE_TEXT, accent=VIRT)
        self.say("Direct: run the program on the CPU itself. Limited: the guard rails we build now.",
                 Succession(AnimationGroup(FadeOut(line), FadeIn(direct), FadeIn(cg)),
                            direct.animate.set_color(VIRT), Wait(0.8),
                            AnimationGroup(FadeIn(limited), FadeIn(fg)), limited.animate.set_color(VIRT), Wait(0.8),
                            FadeIn(badge, shift=RIGHT * 0.3)),
                 stu.change("curious"))
        self.play(FadeOut(VGroup(direct, limited, cg, fg, p, sl)), run_time=0.8)
