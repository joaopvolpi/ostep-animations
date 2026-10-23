import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403
from s09_recap import build_recap  # noqa: E402


class S10Teaser(Ep11Scene):
    def construct(self):
        self.world(stu="neutral", prof="proud", mode="corner")
        stu, prof = self.stu, self.prof
        head, lines, icons = build_recap()
        self.add(head, lines, icons)

        # S10.1
        self.say("So the CPU is sorted out.", FadeOut(VGroup(head, lines, icons)),
                 Succession(AnimationGroup(stu.animate.scale(1 / CHAR_SCALE).move_to(STUDENT_DLG),
                                           prof.animate.scale(1 / CHAR_SCALE).move_to(PROF_DLG), run_time=0.8),
                            stu.change("curious")), min_time=2.5)

        # S10.2
        split = IllusionSplit()
        procs = [proc(n, "ready", scale=0.45, label=None) for n in "ABC"]
        boxes = VGroup()
        for p, x in zip(procs, (-5.0, -3.6, -2.2)):
            box = RoundedRectangle(width=1.0, height=1.5, corner_radius=0.1).set_fill(MEM_COLOR, 0.35).set_stroke(MEM_COLOR, 2)
            box.move_to(P3(x, 1.0))
            place_on(p, box.get_bottom() + UP * 0.08)
            boxes.add(box)
        mem = Memory(regions=["code", "heap", "stack"], width=1.3, height=1.5, addresses=False).move_to(P3(3.3, 1.0))
        q = question_mark(0.45).next_to(stu, UP, buff=0.1)
        with self.narrate("What about memory? Does every process get its own, too?", min_time=5.0):
            self.play(split.draw(), run_time=1.0)
            self.play(FadeIn(boxes), *[FadeIn(p) for p in procs], FadeIn(mem), GrowFromCenter(q), run_time=0.8)
            for _ in range(2):
                self.play(boxes.animate.set_fill(MEM_COLOR, 0.7), run_time=0.4)
                self.play(boxes.animate.set_fill(MEM_COLOR, 0.35), run_time=0.4)

        # S10.3
        chip = CPU(size=0.7).move_to(P3(5.2, 1.0))
        peach = Peach(0.3).move_to(P3(0, 1.0))
        self.say("The same trick, on a different resource.", prof.change("happy"), FadeOut(q),
                 Succession(FadeIn(chip), Wait(0.8), FadeOut(chip), FadeIn(peach), Wait(0.8), FadeOut(peach)), min_time=3.5)

        # S10.4
        self.say("Next time.", FadeOut(*[m for m in self.mobjects]), min_time=0.8)
        dot = Dot(radius=0.1, color=VIRT)
        nxt = Text("Next: 12 · Dialogue on Memory Virtualization", font_size=40, color=TEXT)
        card = VGroup(dot, nxt).arrange(RIGHT, buff=0.3).move_to(ORIGIN)
        self.play(FadeIn(card), run_time=0.8)
        self.wait(2.0)
