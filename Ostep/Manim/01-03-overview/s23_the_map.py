import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from manim import *  # noqa: E402,F403
from ostep_lib import *  # noqa: E402,F403
from common import *  # noqa: E402,F403
from s22_pc_today import PC_POS  # noqa: E402

MAP_CARD_Y = 2.4
GOAL_NAMES = ("abstraction", "performance", "protection", "reliability")


def thumb_virt():
    letters = VGroup(*[Text(c, font=MONO_FONT, font_size=22, color=ABCD_COLORS["ABCD".index(c)], weight=BOLD)
                       for c in "ABDC"]).arrange(RIGHT, buff=0.08)
    cells = VGroup()
    for col in (PID1_COLOR, PID2_COLOR):
        c = Rectangle(width=0.32, height=0.22).set_fill(col, 0.7).set_stroke(MEM_COLOR, 1.5)
        lab = Text("0x200000", font=MONO_FONT, font_size=10, color=col)
        ar = Arrow(UP * 0.28, ORIGIN, buff=0, stroke_width=2.5, tip_length=0.08).set_color(col)
        g = VGroup(lab, ar, c).arrange(DOWN, buff=0.03)
        cells.add(g)
    cells.arrange(RIGHT, buff=0.12)
    return VGroup(letters, cells).arrange(RIGHT, buff=0.35)


def thumb_conc():
    t1 = make_thread("T1", T1_COLOR, 0.26)
    t2 = make_thread("T2", T2_COLOR, 0.26)
    bad = Text("143012", font=MONO_FONT, font_size=16, color=BAD)
    cross = Line(bad.get_left(), bad.get_right()).set_stroke(BAD, 2.5)
    good = VGroup(Text("200000", font=MONO_FONT, font_size=16, color=GOOD), tick_mark(0.14, GOOD, 4)).arrange(RIGHT, buff=0.06)
    nums = VGroup(VGroup(bad, cross), good).arrange(DOWN, buff=0.06)
    return VGroup(t1, t2, nums).arrange(RIGHT, buff=0.15)


def thumb_pers():
    f = FileIcon(None, color=TEXT, width=0.3)
    d = Disk(width=0.55, height=0.48)
    sw = PowerSwitch(0.45)
    sw.remove(sw.on_lab, sw.off_lab)
    return VGroup(f, d, sw).arrange(RIGHT, buff=0.2)


def map_cards():
    cards = VGroup(*[piece_card(i).move_to([x, MAP_CARD_Y, 0]) for i, x in enumerate(CARD_XS)])
    thumbs = [thumb_virt(), thumb_conc(), thumb_pers()]
    for c, t in zip(cards, thumbs):
        if t.width > CARD_W - 0.4:
            t.scale_to_fit_width(CARD_W - 0.4)
        t.move_to(c.frame.get_center() + DOWN * 0.3)
        c.icons.add(t)
    return cards


def map_stack():
    st = make_stack().scale(0.9, about_point=ORIGIN)
    procs = stack_programs().scale(0.9, about_point=ORIGIN)
    return st, procs


def mini_goals():
    g = VGroup()
    for n in GOAL_NAMES:
        t = Text(n, font_size=16, color=TEXT)
        r = RoundedRectangle(width=t.width + 0.3, height=0.42, corner_radius=0.1).set_fill(CARD_FILL, 1).set_stroke(INTRO, 2)
        g.add(VGroup(r, t.move_to(r)))
    return g.arrange(RIGHT, buff=0.2).move_to([0, -3.3, 0])


def uk_line(stack):
    y = stack.band.get_top()[1] + 0.12
    return DashedLine([-5.0, y, 0], [5.0, y, 0], dash_length=0.18).set_stroke(TEXT, 3)


class S23TheMap(NarratedScene):
    def construct(self):
        stu, prof = make_hosts("corner", stu_expr="curious", prof_expr="happy")
        th = terms(INTRO)
        bdg = badge(INTRO)
        era = era_ribbon(4)
        pc = Computer("idle").scale(0.585).move_to([-4.6, 0.35, 0])
        mini2 = minicomputer_icon(1.1, 1.4).move_to([-0.9, 0.35, 0])
        phone = phone_icon(1.0).move_to([1.7, 0.35, 0])
        approx = MathTex(r"\approx", font_size=72, color=GOOD).move_to([0.45, 0.35, 0])
        neq = MathTex(r"\neq", font_size=72, color=BAD).move_to([-2.85, 0.35, 0])
        old = VGroup(era, pc, mini2, phone, approx, neq)
        self.add(stu, prof, bdg, old, set_docked(th, "personal computer"))

        st, procs = map_stack()
        cards = map_cards()

        # S23.1 rebuild the stack
        self.say("So, an operating system is the software that makes a computer easy to use, correctly "
                 "and efficiently.",
                 FadeOut(old), th.clear(),
                 late(1.0, LaggedStart(*[FadeIn(h, shift=UP * 0.3) for h in st.hardware], lag_ratio=0.2,
                                       run_time=0.8)))
        self.say("Here's our map.",
                 FadeIn(st.band, shift=RIGHT), FadeIn(st.band_label), 
                 late(0.5, LaggedStart(*[FadeIn(p, shift=DOWN * 0.3) for p in procs], lag_ratio=0.2, run_time=0.8)))

        # S23.2 virtualization
        vc = st.cpu.virtual_copy().shift(UP * 0.2 + RIGHT * 0.2)
        vm = make_translucent(st.memory.copy(), 0.3, 0.6).shift(UP * 0.2 + RIGHT * 0.2)
        with self.narrate("Virtualization: one physical CPU and one memory become many virtual ones."):
            self.play(FadeIn(cards[0], shift=DOWN * 0.8), run_time=0.8)
            self.wait(0.6)
            self.play(FadeIn(vc), FadeIn(vm), run_time=0.6)
            self.wait(0.8)
            self.play(FadeOut(vc), FadeOut(vm), run_time=0.6)

        # S23.3 concurrency
        self.say("Concurrency: doing many things at once, correctly.", FadeIn(cards[1], shift=DOWN * 0.8))

        # S23.4 persistence
        self.say("Persistence: data that survives power loss and crashes.", FadeIn(cards[2], shift=DOWN * 0.8))

        # S23.5 goals + user/kernel line
        goals = mini_goals()
        ukl = uk_line(st)
        with self.narrate("Along the way: abstraction, performance, protection and reliability, and the "
                          "user/kernel line that makes protection possible."):
            self.play(LaggedStart(*[FadeIn(g, shift=UP * 0.2) for g in goals], lag_ratio=0.3), run_time=1.6)
            self.wait(0.8)
            self.play(Create(ukl), run_time=1.0)
            for _ in range(2):
                self.play(Indicate(ukl, scale_factor=1.0, color=CPU_COLOR), run_time=0.6)

        # S23.6 out of scope
        tags = VGroup(*[Text(t, font_size=20, color=DIM) for t in ("networking", "graphics")]).arrange(DOWN, buff=0.12)
        note = Text("(other courses)", font_size=16, color=DIM).next_to(tags, DOWN, buff=0.1)
        out = VGroup(tags, note).move_to([5.6, 0.7, 0])
        self.say("We won't go deep into networking or graphics.",
                 Succession(FadeIn(out, shift=LEFT * 0.5), out.animate.set_opacity(0.3)))

        # S23.7 security
        lock = padlock_icon(0.4)
        sec = VGroup(lock, Text("security", font_size=20, color=SEC)).arrange(RIGHT, buff=0.12).move_to([-5.6, 0.7, 0])
        self.say("We'll touch on security where the OS must protect programs and files.", FadeIn(sec, scale=0.6))

        # S23.8
        self.say("But the three pieces are the core.",
                 *[Indicate(c, color=c.frame.get_stroke_color(), scale_factor=1.06) for c in cards], min_time=1.6)
        self.beat(1.5)
