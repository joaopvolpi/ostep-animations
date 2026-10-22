import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


class S03Crux(Ep04Scene):
    def construct(self):
        w = build_s02_end()
        board, cpu, vcpus, counter, stu, prof, comp = (w[k] for k in
                                                       ("board", "cpu", "vcpus", "counter", "stu", "prof", "comp"))
        self.add(board, vcpus, counter, cpu, stu, prof, comp)

        # S03.1 (transition)
        badge = make_badge()
        self.play(
            FadeOut(board), FadeOut(vcpus), FadeOut(counter),
            Transform(cpu, badge.dot),
            FadeIn(badge.text, shift=RIGHT * 0.2),
            FadeOut(comp, shift=DOWN * 1.5),
            stu.animate.scale(CHAR_SCALE).move_to(STUDENT_CORNER),
            prof.animate.scale(CHAR_SCALE).move_to(PROF_CORNER),
            run_time=1.6,
        )
        self.remove(cpu)
        self.add(badge)
        self.play(stu.change("neutral"), prof.change("neutral"), run_time=0.5)

        # S03.2 (card appears)
        card = CruxCard(CRUX_Q, CRUX_SUB, accent=VIRT)
        card.move_to(P3(0, 0.6))
        card.subtitle.set_opacity(0)
        self.play(FadeIn(card.frame, scale=0.92), Write(card.header), run_time=0.8)
        self.play(Write(card.question), stu.look_at(card), run_time=1.4)
        self.beat(0.8)

        # S03.3
        term = terminal_thumb(width=6.4, height=1.25)
        term.move_to(P3(0, -2.55))
        cmd = Text("prompt> ./cpu A & ./cpu B & ./cpu C & ./cpu D &", font=MONO_FONT, font_size=17, color=TEXT)
        cmd.move_to(term.frame.get_left() + RIGHT * 0.2 + UP * 0.15, aligned_edge=LEFT)
        out_line = Text("A B D C A B D C A B D C", font=MONO_FONT, font_size=22, color=CPU_COLOR)
        out_line.next_to(cmd, DOWN, buff=0.15, aligned_edge=LEFT)
        with self.narrate("Last time, we watched the OS pull off this trick with four copies of a tiny "
                          "program, printing A, B, C and D."):
            self.play(FadeIn(term, shift=UP * 0.4), FadeIn(cmd), run_time=0.7)
            self.play(AddTextLetterByLetter(out_line, run_time=2.4, rate_func=linear))

        # S03.4
        with self.narrate("Today we find out what it's actually juggling."):
            self.play(FadeOut(VGroup(term, cmd, out_line), run_time=0.6))
            self.play(card.subtitle.animate(run_time=1.0).set_opacity(1))
        self.beat(1.5)

        # S03.5
        # Work-around: CruxCard.dock collapses the subtitle into a leftover dot,
        # so fade the subtitle separately and dock an empty placeholder instead.
        strip = card.strip((0, 3.2, 0), 24)
        self.say("Answering this question introduces the most fundamental idea the operating "
                 "system gives us.",
                 ReplacementTransform(card.frame, strip[0], run_time=1.2),
                 ReplacementTransform(card.question, strip[2], run_time=1.2),
                 FadeOut(card.header, run_time=0.5), FadeOut(card.subtitle, run_time=0.6),
                 stu.look_at(P3(0, 3.2)))
        self.beat(0.3)
