import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403

S4_A = P3(-1.3, -1.0)       # bottom of A
S4_DISK = P3(4.2, -0.8)
S4_BOOTH = P3(1.6, -0.6)
S4_GLYPH = P3(3.8, 1.9)


def build_end():
    """S04 end: crux strip, Disk, A, the CPU glyph with its lock."""
    st = strip(CRUX_Q2)
    disk = Disk().move_to(S4_DISK)
    a = bottom_to(proc("A", "ready", scale=0.9), S4_A)
    glyph = CPU(0.8, label=None, pins=3).move_to(P3(0, 0.8))
    lock = padlock_icon(0.35, KERNEL_COLOR).move_to(glyph.get_center())
    return dict(strip=st, disk=disk, a=a, glyph=glyph, lock=lock)


class S04RestrictedOperations(Ep06Scene):
    def construct(self):
        self.add_badge()
        self.add_docked_term("limited direct execution")
        stu, prof = corner_chars(True, "curious", "worried")
        d = build_s03_end()
        chart, fast, n1, n2, extras = d["chart"], d["fast"], d["n1"], d["n2"], d["extras"]
        old = strip(CRUX_Q1)
        self.add(stu, prof, chart, fast, n1, n2, extras, old)

        # S04.1 (transition + crux strip)
        grp = VGroup(chart, fast)
        new = strip(CRUX_Q2)
        disk = Disk().move_to(S4_DISK)
        a = bottom_to(proc("A", "ready", scale=0.9), S4_A)
        arrow = Arrow(a.get_right() + UP * 0.1, S4_DISK + LEFT * 1.0 + UP * 0.1, buff=0, stroke_width=5, color=COL["A"])
        rd = Text("read", font=MONO_FONT, font_size=22, color=COL["A"]).next_to(arrow, UP, buff=0.1)
        self.say("Which gives us the first question to answer: How to perform restricted operations?",
                 AnimationGroup(chart.animate.scale(0.4).move_to(P3(-4.4, 1.4)).set_opacity(0.3),
                                fast.animate.scale(0.6).move_to(P3(-4.4, 2.75)),
                                n1.animate.move_to(P3(-6.3, 1.4)), FadeOut(n2), FadeOut(extras),
                                ReplacementTransform(old, new), run_time=1.5))
        self.say("Problem number one. What if the process wants to do something restricted, like reading from the disk?",
                 Succession(AnimationGroup(FadeIn(disk), FadeIn(a)), Wait(1.0),
                            AnimationGroup(GrowArrow(arrow), FadeIn(rd))))

        # S04.2
        data = [Square(0.16).set_fill(DISK_COLOR, 1).set_stroke(TEXT, 1).move_to(disk.get_left()) for _ in range(3)]
        self.say("So just let it. It's its program.", stu.change("curious"),
                 Succession(Wait(0.3), LaggedStart(*[PacketFly(s, a.get_right() + UP * 0.1, arc=0.2, fade=True, run_time=1.0)
                                                    for s in data], lag_ratio=0.3)))

        # S04.3
        booth = booth_gate(1.3).move_to(S4_BOOTH)
        badge_tag = tag("A's file", COL["A"], 16).next_to(booth, UP, buff=0.15)
        chk = tick_mark(0.25).next_to(badge_tag, RIGHT, buff=0.1)
        self.say("A file system checks permissions before it opens a file.", prof.change("worried"),
                 Succession(FadeOut(VGroup(arrow, rd), shift=LEFT * 0.4), FadeIn(booth, scale=0.8), FadeIn(badge_tag),
                            FadeIn(chk, scale=1.5), Rotate(booth.bar, 1.0, about_point=booth.bar.get_left(), run_time=0.6)))

        # S04.4
        arc = CurvedArrow(a.get_top() + RIGHT * 0.3, S4_DISK + UP * 0.7 + LEFT * 0.5, angle=-1.1, color=RED_BAD)
        self.say("If any process could talk to the disk directly, it would skip the check…",
                 AnimationGroup(FadeOut(badge_tag), FadeOut(chk), Create(arc, run_time=1.5)))

        # S04.5
        files = VGroup(*[FileIcon(None, width=0.3) for _ in range(3)]).arrange(RIGHT, buff=0.15).next_to(disk, UP, buff=0.25)
        lock = padlock_icon(0.4, KERNEL_COLOR).next_to(booth, UP, buff=0.1)
        self.say("…and read or write the whole disk. All protection gone.",
                 Succession(FadeIn(files), AnimationGroup(*[f.animate.set_color(RED_BAD) for f in files]),
                            FadeIn(lock), AnimationGroup(Rotate(lock, 0.9, about_point=lock.get_bottom()), run_time=0.5),
                            AnimationGroup(lock.animate.shift(DOWN * 0.6).set_opacity(0), FadeIn(x_mark(0.3).move_to(lock)), run_time=0.8)))

        # S04.6
        names = ["mov", "add", "ld", "st", "cmp", "jmp"]
        row = VGroup(*[snippet(n, 18, pad=0.1) for n in names]).arrange(RIGHT, buff=0.15).move_to(P3(-1.5, 1.9))
        glyph = CPU(0.8, label=None, pins=3).move_to(S4_GLYPH)
        mag = magnifier_icon(0.9).move_to(P3(-1.0, 1.35))
        self.say("Then let the OS inspect every instruction before it runs.", stu.change("confused"),
                 Succession(AnimationGroup(FadeIn(row), FadeIn(glyph), FadeIn(mag), FadeOut(arc), FadeOut(files)),
                            row.animate(run_time=3.0, rate_func=linear).shift(RIGHT * 1.6)))

        # S04.7
        slow = tag("SLOW", RED_BAD, 24).move_to(fast)
        self.say("Safe, and slow. We'd throw away the point of direct execution.", prof.change("thinking"),
                 AnimationGroup(row.animate(run_time=3.0, rate_func=rush_from).shift(RIGHT * 0.5),
                                ReplacementTransform(fast, slow), mag.animate.shift(RIGHT * 0.5)))

        # S04.8
        lk = padlock_icon(0.35, KERNEL_COLOR).move_to(glyph.get_center())
        self.say("We want the hardware to help.",
                 AnimationGroup(FadeOut(mag), FadeOut(row), FadeOut(booth), FadeOut(lock), FadeOut(chart), FadeOut(slow),
                                FadeOut(n1), glyph.animate.move_to(P3(0, 0.8)), run_time=1.0),
                 Succession(Wait(1.0), FadeIn(lk.move_to(P3(0, 0.8)), scale=1.5), Indicate(glyph, scale_factor=1.15)))
