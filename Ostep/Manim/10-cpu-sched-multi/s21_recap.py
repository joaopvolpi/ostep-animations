import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common_more import *  # noqa: E402,F401,F403
from s20_big_picture import mini_q  # noqa: E402

ITEMS = [
    ("One-CPU programs don't speed up on many CPUs", None),
    ("Caches use locality; hardware keeps them coherent\nby bus snooping", None),
    ("Shared data needs locks, which slow down\nas CPUs grow", None),
    ("Cache affinity: keep a job on the same CPU", None),
    ("SQMS: simple, but no scale, no affinity.\nMQMS: load imbalance, fixed by migration\nand work stealing", None),
]
ITEM_Y = [1.55, 0.7, -0.15, -0.9, -1.75]


def icons():
    row = VGroup(*[mini_chip(i == 0, 0.3) for i in range(5)]).arrange(RIGHT, buff=0.1)
    cache = VGroup(CacheCPU("", size=1.2).scale(0.3), EyeIcon(0.3)).arrange(RIGHT, buff=0.15)
    pad = VGroup(Padlock(0.4), mini_clock(0.1), mini_clock(0.1)).arrange(RIGHT, buff=0.12)
    warm = VGroup(flame_icon(0.4), pin_icon(0.4)).arrange(RIGHT, buff=0.15)
    qs = VGroup(mini_q(0, 0, 2), suitcase_icon(0.3)).arrange(RIGHT, buff=0.2)
    return [row, cache, pad, warm, qs]


class S21Recap(Ep10Scene):
    def construct(self):
        self.world(strip=0, stu="neutral", prof="proud")
        stu, prof = self.stu, self.prof
        head = label("Recap", 36, VIRT).move_to(P3(-4.0, 2.25))
        texts = []
        for (s, _), y in zip(ITEMS, ITEM_Y):
            t = Text(s, font_size=24, color=TEXT, line_spacing=0.8)
            t.move_to(P3(-4.6, y), aligned_edge=LEFT)
            texts.append(t)
        icos = icons()
        for ic, y in zip(icos, ITEM_Y):
            ic.move_to(P3(4.2, y))

        self.say("So, today:", FadeIn(head, shift=DOWN * 0.2))
        lines = [
            "Programs that use one CPU don't speed up on many.",
            "Caches use locality to speed things up; with several CPUs, hardware keeps them coherent by bus snooping.",
            "Shared data still needs locks, which slow down as CPUs grow.",
            "Cache affinity: keep a job on the same CPU when you can.",
            "SQMS is simple but doesn't scale or keep affinity. MQMS scales, but suffers load imbalance, "
            "fixed by migration and work stealing.",
        ]
        for i, (ln, t, ic) in enumerate(zip(lines, texts, icos)):
            self.say(ln, FadeIn(t, shift=RIGHT * 0.3), FadeIn(ic, shift=LEFT * 0.3))
        self.beat(1.5)
        self.play(FadeOut(self.badge), run_time=0.6)
