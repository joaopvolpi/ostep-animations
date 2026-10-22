import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403

ITEMS = [
    "1.  fork() clones a process",
    "2.  scheduler picks the order; wait() waits",
    "3.  exec() becomes another program",
    "4.  fork and exec apart: redirection, pipes",
    "5.  signals, users, root: who controls what",
]
YS = [1.9, 0.95, 0.0, -0.95, -1.9]


def icons():
    a = VGroup(proc(PAR, "ready", 0.35), proc(CHI, "ready", 0.35)).arrange(RIGHT, buff=0.15)
    b = VGroup(ClockIcon(0.25), zombie_mini(0.3)).arrange(RIGHT, buff=0.2)
    c = VGroup(FileIcon("wc", width=0.4, color=SKY), proc(CHI, "running", 0.35)).arrange(RIGHT, buff=0.25)
    d = VGroup(*[plug_glyph(str(i), TEXT, 14) for i in range(3)]).arrange(RIGHT, buff=0.1).scale(0.9)
    e = VGroup(bolt_glyph(0.6, CPU_COLOR), crown_tag("root", 18)).arrange(RIGHT, buff=0.3)
    return [a, b, c, d, e]


class S17Recap(Ep05Scene):
    def construct(self):
        self.add_badge()
        stu, prof = self.add_corner_chars("neutral", "happy")
        header = Text("Recap", font_size=44, color=VIRT, weight="BOLD").move_to(P3(-6.0, 2.85), aligned_edge=LEFT)
        lines = VGroup(*[Text(s, font_size=28, color=TEXT) for s in ITEMS])
        for ln, y in zip(lines, YS):
            ln.move_to(P3(-5.8, y), aligned_edge=LEFT)
        ics = icons()
        for ic, y in zip(ics, YS):
            ic.move_to(P3(4.6, y))
        self.say("So, today:", Write(header))
        texts = [
            "fork() creates a new process: a nearly exact copy. The parent gets the child's PID, and the child gets zero.",
            "The order is up to the scheduler, so output is non-deterministic. wait() makes the parent wait for its child.",
            "exec() turns the current process into a different program, without creating a new one.",
            "Keeping fork() and exec() apart lets the shell set up redirection and pipes in between.",
            "Signals, users and the superuser control who can do what to which process.",
        ]
        for i, (t, ln, ic) in enumerate(zip(texts, lines, ics)):
            self.say(t, FadeIn(ln, shift=RIGHT * 0.3), FadeIn(ic, scale=0.6), min_time=0.0)
        self.beat(1.5)
        self.play(FadeOut(self.badge), run_time=0.6)
