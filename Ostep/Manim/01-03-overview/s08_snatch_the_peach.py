import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from manim import *  # noqa: E402,F403
from ostep_lib import *  # noqa: E402,F403
from common import *  # noqa: E402,F403

# right half of the split (S08.6+)
R_CPU = np.array([3.5, 0.9, 0])
R_XS = (1.9, 3.0, 4.1, 5.2)
R_BASE_Y = -1.2
L_POS = [(-5.0, 0.9), (-2.4, 0.9), (-5.0, -1.4), (-2.4, -1.4)]   # left half: eater base points


def split_world():
    """S08 end state pieces: split, left eaters+peaches, right CPU + A-D."""
    split = IllusionSplit("what each eater sees", "what really happens")
    left = VGroup()
    for i, (x, y) in enumerate(L_POS):
        e = Process(color=ABCD_COLORS[i]).scale(0.65)
        place_on(e, [x, y, 0])
        pch = Peach().scale(0.5).next_to(e, RIGHT, buff=0.12).align_to(e, DOWN).shift(UP * 0.35)
        e.set_look(pch)
        left.add(VGroup(e, pch))
    cpu = CPU(size=1.2).move_to(R_CPU)
    procs = VGroup()
    for i, x in enumerate(R_XS):
        p = Process(color=ABCD_COLORS[i], label="ABCD"[i]).scale(0.65)
        place_on(p, [x, R_BASE_Y, 0])
        procs.add(p)
    return split, left, cpu, procs


class S08SnatchThePeach(NarratedScene):
    def construct(self):
        stu, prof = peach_hosts()
        stu.set_expression("curious")
        prof.set_expression("explaining")
        w = peach_world_s07_end()
        table, peach, phys, eaters, vps, vtags, cones = (w[k] for k in
                                                          ("table", "peach", "phys", "eaters", "vps", "vtags", "cones"))
        th = terms(VIRT)
        bdg = badge(VIRT)
        self.add(stu, prof, bdg, table, peach, phys, eaters, vps, vtags, cones, set_docked(th, "virtual"))

        # S08.1-2
        self.say("So you're sharing the peach, and they don't even know it?", stu.change("curious"))
        self.say("Exactly.", prof.change("happy"), min_time=1.2)

        # S08.3 virtual peaches flicker
        with self.narrate("But there's only one peach. If I were sharing a peach, I think I'd notice."):
            self.play(stu.change("frustrated"), run_time=0.5)
            for _ in range(3):
                self.play(vps.animate.set_opacity(0.1), run_time=0.25)
                self.play(vps.animate.set_opacity(0.35), run_time=0.25)

        # S08.4 nap
        self.say("Ah, but most of the time eaters are napping, or doing something else.",
                 prof.change("proud"), FadeOut(cones), *[eaters[i].change("blocked") for i in (1, 2, 3)])

        # S08.5 snatch and hop
        def spot(i):
            e = eaters[i]
            side = RIGHT if EATER_XS[i] < 0 else LEFT
            return np.array([EATER_XS[i], TABLE_Y, 0]) + side * 0.75

        order = [0, 2, 1, 3, 0, 2, 1]
        with self.narrate("So you snatch the peach away and give it to someone else for a while."):
            self.play(peach.animate.set_opacity(1), run_time=0.3)
            prev = None
            for k, i in enumerate(order):
                fast = k >= 4
                rt = 0.35 if fast else 0.6
                anims = [hop_to(peach, spot(i), height=0.8, run_time=rt)]
                if prev is not None and prev != i:
                    anims.append(eaters[prev].change("blocked", run_time=rt))
                if k > 0:
                    anims.append(eaters[i].change("ready", run_time=rt))
                self.play(*anims)
                self.play(eaters[i].change("running", run_time=0.25 if fast else 0.35),
                          Indicate(peach, scale_factor=0.9, color=PEACH_COLOR, run_time=0.25 if fast else 0.35))
                prev = i

        # S08.6 pull back: illusion split
        split, left, cpu, procs = split_world()
        r_eaters = VGroup()
        for i, x in enumerate(R_XS):
            e = Process(color=ABCD_COLORS[i]).scale(0.65)
            place_on(e, [x, R_BASE_Y, 0])
            e.set_expression("blocked" if i != 1 else "running")
            r_eaters.add(e)
        r_peach = Peach().scale(0.6).move_to(R_CPU)
        world = VGroup(table, peach, phys, eaters, vps, vtags)
        with self.narrate("And so we create the illusion of many virtual peaches: one for each person!"):
            self.play(*mode_anims(stu, prof, "corner", run_time=1.0),
                      FadeOut(VGroup(table, phys, vps, vtags)),
                      ReplacementTransform(eaters, r_eaters), ReplacementTransform(peach, r_peach), run_time=1.0)
            self.play(split.draw(), FadeIn(left, lag_ratio=0.15), run_time=1.4)
            for i in (2, 0, 3, 1):
                self.play(hop_to(r_peach, r_eaters[i].get_top() + UP * 0.15, height=0.6, run_time=0.45))
            self.play(hop_to(r_peach, R_CPU + DOWN * r_peach.height / 2, height=0.6, run_time=0.45))

        # S08.7 campaign poster
        poster = poster_frame(width=5.6).move_to([-3.6, -0.2, 0])
        with self.narrate("Sounds like a bad campaign slogan."):
            self.play(stu.change("bored"), FadeIn(poster, scale=1.2), run_time=0.6)
            self.wait(1.2)
            self.play(FadeOut(poster), run_time=0.5)

        # S08.8
        self.say("You're talking about computers, right?", min_time=1.6)

        # S08.9 peach -> CPU, eaters -> A-D
        self.say("Right. Let's take a real one.",
                 prof.change("happy"), ReplacementTransform(r_peach, cpu, run_time=1.0),
                 ReplacementTransform(r_eaters, procs, run_time=1.0))
        self.beat(1.0)
