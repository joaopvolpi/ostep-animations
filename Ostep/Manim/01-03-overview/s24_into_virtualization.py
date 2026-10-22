import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from manim import *  # noqa: E402,F403
from ostep_lib import *  # noqa: E402,F403
from common import *  # noqa: E402,F403
from s23_the_map import map_stack, map_cards, mini_goals, uk_line  # noqa: E402

BIG_CARD = np.array([0, 2.2, 0])


class S24IntoVirtualization(NarratedScene):
    def construct(self):
        stu, prof = make_hosts("corner", stu_expr="curious", prof_expr="happy")
        th = terms(VIRT)
        th.at = np.array([-4.6, 1.9, 0])
        th.size = 44
        bdg = badge(INTRO)
        st, procs = map_stack()
        cards = map_cards()
        goals = mini_goals()
        ukl = uk_line(st)
        tags = VGroup(*[Text(t, font_size=20, color=DIM) for t in ("networking", "graphics")]).arrange(DOWN, buff=0.12)
        note = Text("(other courses)", font_size=16, color=DIM).next_to(tags, DOWN, buff=0.1)
        out = VGroup(tags, note).move_to([5.6, 0.7, 0]).set_opacity(0.3)
        sec = VGroup(padlock_icon(0.4), Text("security", font_size=20, color=SEC)).arrange(RIGHT, buff=0.12).move_to([-5.6, 0.7, 0])
        self.add(stu, prof, bdg, st, procs, cards, goals, ukl, out, sec)

        vcard = cards[0]
        # S24.1
        self.say("And so we reach the first of our three pieces: virtualization.",
                 FadeOut(VGroup(st, procs, cards[1], cards[2], goals, ukl, out, sec)), FadeOut(vcard.icons),
                 vcard[:2].animate(run_time=1.2).scale(1.5).move_to(BIG_CARD), bdg.recolor(VIRT),
                 *mode_anims(stu, prof, "dialog", run_time=1.2))
        self.play(prof.change("happy"), run_time=0.5)

        frame = vcard.frame
        slot = frame.get_center() + DOWN * 0.55
        # S24.2 peach
        peach = Peach(0.36).move_to(slot)
        self.say("The peach thing! Tell me more. How does it actually work?",
                 stu.change("excited"), FadeIn(peach, scale=0.3))

        # S24.3
        self.say("In time, young student, in good time.", prof.change("thinking"), min_time=2.2)

        # S24.4 peach -> CPU
        cpu = CPU(size=0.7).move_to(slot)
        self.say("We'll start with the most basic illusion of all: the CPU.", ReplacementTransform(peach, cpu, run_time=1.0))

        # S24.5 process A hops onto the CPU
        a = Process(color=A_COLOR, label="A").scale(0.42)
        place_on(a, frame.get_corner(DR) + LEFT * 0.5)
        with self.narrate("And the thing the OS creates to pull it off: the process."):
            self.play(FadeIn(a, scale=0.5), run_time=0.4)
            self.play(hop_to(a, cpu.slot_point(), run_time=0.6))
            self.play(a.change("running"), run_time=0.4)
            self.play(th.show("process", hold=0.8))

        # S24.6 the peach peeks in
        peek = Peach(0.55).move_to([0.9, -4.6, 0])
        self.say("I'm a little worried you're going to start talking about peaches again.",
                 stu.change("sad"), peek.animate(run_time=0.8).move_to([0.9, -3.6, 0]))

        # S24.7 the peach rolls away
        with self.narrate("Don't worry too much. I don't even like peaches."):
            self.play(prof.change("happy"), run_time=0.5)
            self.play(peek.animate.move_to([3.0, -3.45, 0]), run_time=0.4)
            self.play(Rotate(peek, -2 * TAU, about_point=peek.get_center()), peek.animate.shift(RIGHT * 5.5),
                      run_time=1.4, rate_func=rush_into) if False else \
                self.play(MoveAlongPath(peek, Line(peek.get_center(), [8.5, -3.45, 0])),
                          Rotate(peek, -2.5 * TAU), run_time=1.4, rate_func=rush_into)

        # S24.8 end card
        fill = frame.copy().set_fill(VIRT, 1).set_stroke(VIRT)
        dot = Dot(radius=0.12).set_fill(VIRT, 1)
        end = Text("Next: 04 · The Process", font_size=40, color=TEXT)
        endg = VGroup(dot, end).arrange(RIGHT, buff=0.25).move_to(ORIGIN)
        self.play(FadeIn(fill), run_time=0.3)
        self.add(fill)
        self.bring_to_front(fill)
        self.play(fill.animate.scale(6).move_to(ORIGIN), run_time=1.0)
        everything = [m for m in self.mobjects if m is not fill]
        self.remove(*everything)
        self.play(FadeOut(fill), run_time=0.8)
        self.play(FadeIn(endg, shift=UP * 0.2), run_time=0.7)
        self.beat(2.0)
