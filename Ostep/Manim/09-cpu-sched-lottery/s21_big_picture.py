import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403

CX = (-4.4, 0.0, 4.4)


def share_strip(x, y):
    """A tiny 75/25 strip standing for a filled Timeline."""
    segs = VGroup(*[Rectangle(width=0.3, height=0.25).set_fill(COL["B" if k in (3, 7) else "A"], 1).set_stroke(TEXT, 0.8)
                    for k in range(10)]).arrange(RIGHT, buff=0)
    return segs.move_to(P3(x, y))


def tree_icon():
    g = VGroup(Circle(radius=0.17).set_fill(RBTree.BLK, 1).set_stroke(TEXT, 2).move_to(P3(0, 0.3)),
               Circle(radius=0.14).set_fill(RBTree.RED, 1).set_stroke(TEXT, 2).move_to(P3(-0.35, -0.1)),
               Circle(radius=0.14).set_fill(RBTree.RED, 1).set_stroke(TEXT, 2).move_to(P3(0.35, -0.1)))
    g.add(Line(g[0].get_center(), g[1].get_center()).set_stroke(DIM, 2).set_z_index(-1),
          Line(g[0].get_center(), g[2].get_center()).set_stroke(DIM, 2).set_z_index(-1))
    return g


def runners_icon():
    g = VGroup()
    for k, c in enumerate((COL["A"], COL["B"], COL["C"])):
        g.add(Line(P3(-0.6, -0.3 * k), P3(0.6, -0.3 * k)).set_stroke(DIM, 2))
        g.add(Dot(P3(-0.6 + 0.35 * (k + 1), -0.3 * k), radius=0.09, color=c))
    return g.move_to(ORIGIN)


class S21BigPicture(Ep09Scene):
    def construct(self):
        self.world(stu="neutral", prof="neutral")
        stu, prof = self.stu, self.prof
        icons = [RaffleDrum(0.8).move_to(P3(CX[0], 1.5)), runners_icon().move_to(P3(CX[1], 1.5)), tree_icon().move_to(P3(CX[2], 1.5))]
        words = [Text(w, font_size=26, color=VIRT).move_to(P3(x, 0.6)) for w, x in zip(("random", "deterministic", "efficient"), CX)]
        subs = [Text(w, font_size=20, color=DIM).move_to(P3(x, 0.15)) for w, x in zip(("tickets", "pass", "vruntime"), CX)]
        strips = [share_strip(x, -0.45) for x in CX]

        # S21.1
        sentence_anims = []
        for i in range(3):
            sentence_anims.append(Succession(Wait(3.0 * i), AnimationGroup(FadeIn(icons[i]), FadeIn(words[i]), FadeIn(subs[i]),
                                                                           FadeIn(strips[i]))))
        self.say("Let's step back. Lottery shares the CPU by random draw. Stride does it deterministically. CFS does it with "
                 "vruntime, weights and a tree, built for efficiency at scale.", *sentence_anims)

        # S21.2
        mlfq = sched_chip("MLFQ", 0.95, 0.46).move_to(P3(8.0, -1.1))
        self.say("So these are the best schedulers? Why did we bother with MLFQ?",
                 stu.change("confused"), glide(mlfq, P3(5.6, -1.1), 1.2))

        # S21.3
        sleeper = proc("B", expr="blocked", scale=0.4, label="").move_to(P3(-3.4, -1.5))
        share = Rectangle(width=2.0, height=0.25).set_fill(opacity=0).set_stroke(COL["B"], 2).move_to(P3(-1.4, -1.5))
        half = Rectangle(width=0.8, height=0.25).set_fill(COL["B"], 0.9).set_stroke(width=0).align_to(share, LEFT).match_y(share)
        self.say("No scheduler is a panacea. These don't mesh well with I/O: a job that sleeps often misses its share.",
                 prof.change("worried"), FadeIn(sleeper), FadeIn(share), FadeIn(half))

        # S21.4
        qcard = VGroup(card_rect(3.2, 1.3, DIM), text_editor_icon(0.8), Text("nice ?", font_size=22, color=TEXT),
                       Text("tickets ?", font_size=22, color=TEXT))
        qcard[1].move_to(qcard[0].get_center() + LEFT * 0.95)
        qcard[2].move_to(qcard[0].get_center() + RIGHT * 0.6 + UP * 0.25)
        qcard[3].move_to(qcard[0].get_center() + RIGHT * 0.6 + DOWN * 0.25)
        qcard.move_to(P3(0.6, -1.8))
        self.say("And they leave a hard question open: how many tickets, or which nice value, should your text editor get?",
                 FadeOut(VGroup(sleeper, share, half)), FadeIn(qcard, shift=UP * 0.2))

        # S21.5
        ok = tick_mark(0.35).next_to(mlfq, UP, buff=0.1)
        strike = Line(qcard.get_corner(DL), qcard.get_corner(UR)).set_stroke(KERNEL_COLOR, 4)
        self.say("MLFQ-style schedulers handle that automatically.",
                 Indicate(mlfq, color=CPU_COLOR), FadeIn(ok), Create(strike))

        # S21.6
        pie = TargetPie((0.75, 0.25), radius=0.45, label=None).move_to(P3(5.4, -1.7))
        self.say("Still, in many domains that isn't the main worry.",
                 qcard.animate.shift(LEFT * 9), strike.animate.shift(LEFT * 9), FadeOut(mlfq), FadeOut(ok), FadeIn(pie))
        self.remove(qcard, strike)

        # S21.7
        cloud = cloud_icon(1.6).move_to(P3(-2.6, -1.5))
        rack = server_rack_icon(0.6, 1.0).scale(0.7).move_to(cloud.get_center() + DOWN * 0.05)
        win = vm_window("Windows", COL["B"], 1.5, 0.9, "25%").move_to(P3(0.0, -1.6))
        lin = vm_window("Linux", COL["A"], 1.5, 0.9, "75%").move_to(P3(2.0, -1.6))
        self.say("In a cloud data center, you might give a quarter of the CPU to a Windows VM and the rest to your Linux install.",
                 FadeIn(cloud), FadeIn(rack), FadeIn(win), FadeIn(lin))

        # S21.8
        ok2 = tick_mark(0.35).next_to(pie, UP, buff=0.1)
        self.say("Proportional share is simple and effective there.", pie.pulse(), FadeIn(ok2))

        # S21.9
        eev = token("EEVDF", VIRT, size=22).move_to(P3(CX[2], 1.5))
        tag = Text("Linux 6.6 → EEVDF", font_size=20, color=VIRT).move_to(P3(CX[2], 2.35))
        self.say("And Linux keeps changing: since version 6.6, its default is a scheduler called EEVDF. Just when you thought "
                 "you were done.",
                 Transform(icons[2], eev), FadeIn(tag), stu.change("surprised"),
                 Succession(Wait(3.0), prof.change("happy")))
        self.beat(0.8)
        self.play(FadeOut(VGroup(*icons, *words, *subs, *strips, tag, cloud, rack, win, lin, pie, ok2)), run_time=0.8)
