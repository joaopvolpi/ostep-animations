import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from manim import *  # noqa: E402,F403
from ostep_lib import *  # noqa: E402,F403
from common import *  # noqa: E402,F403


class S03HearSeeDo(NarratedScene):
    def construct(self):
        stu, prof = make_hosts("dialog", stu_expr="confused", prof_expr="happy")
        title = small_title(make_title()[0])
        cards = piece_cards()
        self.add(stu, prof, title, cards)

        # S03.1
        self.say("And what's the best way to learn this stuff?",
                 stu.change("curious"), Transform(cards, card_strip(cards), run_time=1.0),
                 FadeOut(title, run_time=0.6))

        # S03.2
        ed = editor_icon(1.8).move_to([0, 1.0, 0])
        cursor = ed[-1]
        with self.narrate("Watch, think, and then do. Write real code that solves real problems."):
            self.play(prof.change("explaining"), FadeIn(ed, scale=0.8), run_time=0.7)
            for _ in range(3):
                self.play(cursor.animate.set_opacity(0), run_time=0.3)
                self.play(cursor.animate.set_opacity(1), run_time=0.3)
            self.play(FadeOut(ed), run_time=0.5)

        # S03.3
        self.say("As Confucius said…", prof.says("As Confucius said…", font_size=26, max_width=3.2),
                 min_time=1.6)

        lines = motto_lines()
        # S03.4 (the Student cuts in: the Professor's bubble gives way)
        self.say("\"I hear and I forget.\"", stu.change("excited"), prof.remove_bubble(),
                 Write(lines[0], run_time=0.9), min_time=1.6)
        # S03.5
        glow = glow_for(lines[1])
        self.say("\"I see and I remember.\"", Write(lines[1], run_time=0.9), min_time=1.6)
        self.play(FadeIn(glow), lines[1].animate.set_color(INTRO), run_time=0.6)
        # S03.6
        self.say("\"I do and I understand.\" Or something like that.", Write(lines[2], run_time=0.9))

        # S03.7
        self.say("How did you know what I was going to say?!", prof.change("surprised"))

        # S03.8
        note = Text("attributed to Confucius; closer to Xunzi", font_size=20, color=DIM)
        note.next_to(lines, DOWN, buff=0.3).shift(LEFT * 0.4)
        self.say("It seemed to follow. Also, the philosopher Xunzi is actually a better source for that quote.",
                 stu.change("neutral"), FadeIn(note, shift=LEFT * 0.5, run_time=0.7))

        # S03.9
        self.say("Well. I think we're going to get along just fine.", prof.change("happy"))
        self.beat(1.0)
