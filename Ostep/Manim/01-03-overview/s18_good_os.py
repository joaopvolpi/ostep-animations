import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from manim import *  # noqa: E402,F403
from ostep_lib import *  # noqa: E402,F403
from common import *  # noqa: E402,F403
from s17_syscalls_crash import s17_world, s17_end_world  # noqa: E402

BADGE_XS = (-4.8, -1.6, 1.6, 4.8)
BADGE_Y = 0.4
GOALS = ("Abstraction", "Performance", "Protection", "Reliability")


def goal_frame(i, size=2.6):
    r = RoundedRectangle(width=size, height=size, corner_radius=0.25).set_fill(CARD_FILL, 1).set_stroke(INTRO, 3)
    r.move_to([BADGE_XS[i], BADGE_Y, 0])
    lab = Text(GOALS[i], font_size=24, color=TEXT).move_to(r.get_bottom() + UP * 0.35)
    return VGroup(r, lab)


def icon_center(i):
    return np.array([BADGE_XS[i], BADGE_Y + 0.25, 0])


def goal_icons():
    """The four badge icons (final look)."""
    ab = layers_icon(1.2).move_to(icon_center(0))
    sw = stopwatch_icon(0.38).move_to(icon_center(1) + LEFT * 0.55)
    bars = VGroup()
    for k, name in enumerate(("time", "space")):
        b = Rectangle(width=0.28, height=0.9).set_fill(USER_COLOR, 0.8).set_stroke(width=0)
        o = Rectangle(width=0.28, height=0.12).set_fill(BAD, 0.9).set_stroke(width=0).next_to(b, UP, buff=0)
        t = Text(name, font_size=14, color=DIM).next_to(b, DOWN, buff=0.06)
        bars.add(VGroup(b, o, t))
    bars.arrange(RIGHT, buff=0.18, aligned_edge=DOWN).move_to(icon_center(1) + RIGHT * 0.55)
    prot = VGroup()
    ps = VGroup(*[Process(color=ABCD_COLORS[k]).scale(0.3) for k in range(3)])
    walls = walls_icon(2, 0.75)
    row = VGroup(ps[0], walls[0], ps[1], walls[1], ps[2]).arrange(RIGHT, buff=0.08).move_to(icon_center(2))
    prot.add(ps, walls)
    prot.procs, prot.walls = ps, walls
    ecg = ecg_icon(1.9).move_to(icon_center(3))
    return ab, VGroup(sw, bars), prot, ecg


def extras_row():
    items = [(leaf_icon(0.45), "energy"), (padlock_icon(0.35), "security"), (phone_icon(0.5), "mobility")]
    g = VGroup()
    for k, (ic, name) in enumerate(items):
        r = RoundedRectangle(width=1.4, height=1.0, corner_radius=0.15).set_fill(CARD_FILL, 1).set_stroke(DIM, 2)
        r.move_to([(k - 1) * 1.7, -2.0, 0])
        ic.move_to(r.get_center() + UP * 0.12)
        t = Text(name, font_size=16, color=TEXT).move_to(r.get_bottom() + UP * 0.17)
        g.add(VGroup(r, ic, t))
    return g


def s18_end_extras(icons):
    """What S18 leaves on screen beyond frames/icons/extras row (S19's start): the angry process
    (replaces the middle protection process), the wall glow, the wish-list scroll and title."""
    prot = icons[2]
    ps, walls = prot.procs, prot.walls
    angry = Process(color=BAD).scale(0.3).move_to(ps[1])
    ps.remove(ps[1])
    glow = VGroup(*[w_.copy().set_fill(opacity=0).set_stroke(CPU_COLOR, 6, opacity=0.6) for w_ in walls])
    scroll = scroll_icon(13.6, 4.3)
    scroll[0].set_fill(opacity=0.12)
    scroll[1].set_fill(opacity=0.5)
    scroll.move_to([0, -0.25, 0]).set_z_index(-2)
    wl = Text("wish list", font_size=26, color=INTRO).move_to([0, 2.15, 0])
    return VGroup(angry, glow, scroll, wl)


class S18GoodOS(NarratedScene):
    def construct(self):
        stu, prof = make_hosts("corner", stu_expr="surprised", prof_expr="happy")
        th = terms(PERS)
        th.at = np.array([0, 2.3, 0])
        bdg = badge(PERS)
        w, extras, crux_strip, blk_pt = s17_end_world()
        old = VGroup(*w.values(), extras, crux_strip)
        stu.set_look(blk_pt)
        self.add(stu, prof, bdg, old, set_docked(th, "journaling · copy-on-write"))
        th.set_accent(INTRO)

        # S18.1 pieces flash, dock as strip
        cards = piece_cards()
        strip = card_strip(cards).move_to([0, 3.3, 0])
        with self.narrate("So an OS virtualizes resources, handles concurrency, and stores files persistently. "
                          "If we're going to build one, what should we aim for?"):
            self.play(FadeOut(old), bdg.recolor(INTRO), stu.change("curious"), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(c, scale=0.8) for c in cards], lag_ratio=0.3), run_time=1.2)
            self.wait(1.0)
            self.play(Transform(cards, strip), run_time=1.0)

        # S18.2
        self.say("First, abstractions that make the system easy to use. Abstraction is how we build anything "
                 "big in computing.", th.show("abstraction", hold=1.0))

        # S18.3 tower
        names = ["transistors", "logic gates", "assembly", "C", "programs"]
        layers = VGroup()
        for k, n in enumerate(names):
            r = RoundedRectangle(width=4, height=0.62, corner_radius=0.1).set_fill(mix_layer(k), 1).set_stroke(INTRO, 2)
            t = Text(n, font_size=24, color=TEXT).move_to(r)
            layers.add(VGroup(r, t))
        layers.arrange(UP, buff=0.08).move_to([0, 0.0, 0])
        with self.narrate("We write C without thinking about assembly,"):
            self.play(LaggedStart(*[FadeIn(l, shift=DOWN * 0.3) for l in layers], lag_ratio=0.25), run_time=1.6)
            self.play(layers[2].animate.set_opacity(0.3), run_time=0.4)
        # S18.4
        with self.narrate("assembly without thinking about logic gates, gates without thinking about transistors."):
            self.wait(0.6)
            self.play(layers[1].animate.set_opacity(0.3), run_time=0.4)
            self.wait(1.2)
            self.play(layers[0].animate.set_opacity(0.3), run_time=0.4)

        # S18.5 collapse into badge 1
        frames = [goal_frame(i) for i in range(4)]
        ab, perf, prot, ecg = goal_icons()
        self.play(FadeIn(frames[0]), run_time=0.3)
        self.play(ReplacementTransform(layers, ab), run_time=1.0)
        self.beat(0.4)

        # S18.6-7 performance
        sw, bars = perf
        self.say("Second, performance.", FadeIn(frames[1]), FadeIn(sw), th.show("performance", hold=0.8), min_time=2.0)
        with self.narrate("Virtualization is worth it, but not at any cost. We want to minimize the overheads, in "
                          "extra time and in extra space."):
            for b in bars:
                b[1].stretch(3, 1, about_edge=DOWN)
            self.play(FadeIn(bars), Rotate(sw.hand, -TAU, about_point=sw[0].get_center()), run_time=1.0)
            self.wait(1.0)
            self.play(*[b[1].animate.stretch(1 / 3, 1, about_edge=DOWN) for b in bars], run_time=1.0)
            self.play(th.show("minimize overheads", size=40, hold=0.8))

        # S18.8 protection
        ps, walls = prot.procs, prot.walls
        angry = Process(color=BAD).scale(0.3).move_to(ps[1])
        with self.narrate("Third, protection. One misbehaving program, malicious or just buggy, must not harm the "
                          "others, or the OS itself."):
            self.play(FadeIn(frames[2]), FadeIn(prot), run_time=0.6)
            self.play(th.show("protection", hold=0.8))
            self.play(ReplacementTransform(ps[1], angry), run_time=0.5)
            for d in (LEFT, RIGHT, LEFT):
                self.play(angry.animate.shift(d * 0.08), Indicate(walls[0 if d[0] < 0 else 1], color=TEXT,
                                                                   scale_factor=1.05), run_time=0.3)
                self.play(angry.animate.shift(-d * 0.08), run_time=0.2)

        # S18.9 isolation
        glow = VGroup(*[w_.copy().set_fill(opacity=0).set_stroke(CPU_COLOR, 6, opacity=0.6) for w_ in walls])
        self.say("The principle behind that is isolation.", FadeIn(glow), th.show("isolation", hold=0.8))

        # S18.10 reliability
        line = ecg[0]
        with self.narrate("Fourth, reliability. If the OS fails, everything fails, so it has to keep running."):
            self.play(FadeIn(frames[3]), Create(ecg), run_time=0.8)
            self.play(th.show("reliability", hold=0.8))
            for _ in range(2):
                self.play(ShowPassingFlash(line.copy().set_stroke(GOOD, 7), time_width=0.4), run_time=0.8)

        # S18.11 extras + wish list
        ex = extras_row()
        scroll = scroll_icon(13.6, 4.3)
        scroll[0].set_fill(opacity=0.12)
        scroll[1].set_fill(opacity=0.5)
        scroll.move_to([0, -0.25, 0]).set_z_index(-2)
        wl = Text("wish list", font_size=26, color=INTRO).move_to([0, 2.15, 0])
        self.say("Add energy efficiency, security and mobility, and you have a long wish list.",
                 LaggedStart(*[FadeIn(e, shift=UP * 0.2) for e in ex], lag_ratio=0.3, run_time=1.2),
                 Succession(Wait(1.6), AnimationGroup(GrowFromEdge(scroll, UP), FadeIn(wl), run_time=0.9)))
        self.beat(0.6)


def mix_layer(k):
    from ostep_lib.characters.base import mix
    return mix(INTRO, BG, 0.88 - 0.06 * k)
