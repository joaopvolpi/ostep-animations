import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


class S15UsefulTools(Ep05Scene):
    def construct(self):
        self.add_badge()
        self.add_docked_term("superuser (root)")
        stu, prof = self.add_corner_chars("curious", "worried")
        term = Terminal(width=7.0, height=3.4, font_size=18).move_to(P3(-1.2, 0.6))

        # S15.1
        dots = VGroup()
        with self.narrate("To see all this in practice, some tools help. ps lists the processes running on your system."):
            self.play(FadeIn(term), run_time=0.5)
            self.play(term.type("ps"))
            rows = ["    PID    CMD", "    29146  p1", "    29147  p1", "    29150  sh", "    29151  ps"]
            for r in rows:
                self.play(term.print(r, run_time=0.3))
            for line, col in zip(list(term.lines)[-4:-1], (PAR, CHI, SHC)):
                dots.add(Dot(radius=0.07, color=col).move_to(line.get_left() + RIGHT * 0.15))
            self.play(FadeIn(dots), run_time=0.5)
            self.wait(1.0)

        # S15.2
        top_rows = ["top", "p1", "sh", "ps"]
        widths = [2.2, 1.5, 0.8, 0.4]
        with self.narrate("top shows which of them are using the most CPU."):
            self.play(FadeOut(dots), term.clear())
            self.play(term.type("top"))
            bars = VGroup()
            for r, wd in zip(top_rows, widths):
                self.play(term.print(f"  {r}", run_time=0.2))
                ln = term.lines[-1]
                bar = Rectangle(width=wd, height=0.16).set_fill(CPU_COLOR, 0.9).set_stroke(width=0)
                bar.move_to(P3(ln.get_left()[0] + 1.5, ln.get_y()), aligned_edge=LEFT)
                bar.align_to(P3(ln.get_left()[0] + 1.5, 0), LEFT)
                bars.add(bar)
            self.play(*[GrowFromEdge(b, LEFT) for b in bars], run_time=0.8)
            self.play(*[b.animate.stretch(1.2 if i % 2 else 0.85, 0, about_edge=LEFT) for i, b in enumerate(bars)],
                      run_time=1.0)

        # S15.3
        with self.narrate("Humorously, top often claims that top is the top resource hog."):
            self.play(Indicate(term.lines[-4], color=CPU_COLOR), Indicate(bars[0], color=CPU_COLOR), run_time=1.2)
            self.wait(0.8)

        # S15.4
        win = desktop_icon(1.0).move_to(P3(4.2, 1.4))
        with self.narrate("And kill and killall send signals. Use them carefully, or you could kill your window manager."):
            self.play(FadeOut(bars), term.clear())
            self.play(term.type("killall -9 wm"))
            self.play(FadeIn(win, scale=0.5), run_time=0.5)
            self.wait(0.5)
            xm = x_mark(0.5).move_to(win)
            self.play(FadeIn(xm, scale=2.0), run_time=0.3)
            self.play(FadeOut(win, scale=0.2), FadeOut(xm), run_time=0.5)

        # S15.5
        self.say("Is there a manual for every flag?", stu.change("bored"))

        # S15.6
        aside = AsideCard("RTFM: read the man pages", title="RTFM", width=3.4, font_size=22, icon=book_icon())
        aside.move_to(P3(4.6, -0.2))
        with self.narrate("There is. They're the man pages. When someone replies, \"RTFM\", they mean you should "
                          "go read them."):
            self.play(prof.change("happy"), self.terms.note("man pages"))
            self.play(term.clear())
            self.play(term.type("man ps"))
            self.play(term.print("PS(1)            User Commands            PS(1)"))
            self.play(aside.slide_in(RIGHT), run_time=0.8)
            self.wait(1.5)
            self.play(aside.slide_out(RIGHT), run_time=0.6)
        self.beat(0.5)

        self.play(*[FadeOut(m) for m in (term,)], run_time=0.8)
