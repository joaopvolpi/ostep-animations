import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


class S08LightingFires(Ep11Scene):
    def construct(self):
        self.world(stu="neutral", prof="explaining", mode="corner")
        stu, prof = self.stu, self.prof
        old = build_s07_end()
        self.add(old)

        ladder = make_ladder()
        B = proc("B", "running", scale=0.6, label=None)
        shades = put_shades(B)
        gamer = VGroup(B, shades)
        D = proc("D", "ready", scale=0.6, label=None)
        ladder.place(D, 0)
        ladder.place(B, 2)
        shades.move_to(B.get_center() + UP * 0.12 * B.get_height())
        t_gamer = label("the gamer", 18, DIM).move_to(P3(1.5, ladder.lane_y(2)))
        t_neigh = label("gullible neighbor", 18, DIM).move_to(P3(1.9, ladder.lane_y(0)))
        rack = VGroup(server_rack_icon(0.7, 1.1), label("EC2", 22, TEXT)).arrange(DOWN, buff=0.1).move_to(P3(4.6, 1.5))

        # S08.1
        self.say("Anything else that caught your fancy?", FadeOut(old), FadeIn(ladder),
                 prof.change("neutral", look_at=stu), min_time=2.5)

        # S08.2
        self.say("Gaming the scheduler!", stu.change("excited"), Indicate(ladder, scale_factor=1.02),
                 FadeIn(D), FadeIn(gamer), FadeIn(t_gamer), FadeIn(t_neigh), min_time=2.5)

        # S08.3
        self.say("I might try it next time I run a job on Amazon's EC2.", FadeIn(rack, shift=LEFT * 0.5),
                 Succession(Wait(1.5), Flash(shades.get_center(), color=TEXT, line_length=0.15, flash_radius=0.2, run_time=0.5)),
                 min_time=3.5)

        # S08.4
        disk = Disk(width=0.5, height=0.42).move_to(P3(-0.5, ladder.lane_y(2)))
        coin = Circle(radius=0.12).set_fill(CPU_COLOR, 1).set_stroke(outline_of(CPU_COLOR), 2).move_to(D.get_center() + UP * 0.3)
        tear = Dot(radius=0.05, color=USER_COLOR).move_to(D.get_center() + LEFT * 0.12)
        with self.narrate("Steal some cycles from some unsuspecting, and more importantly OS-ignorant, customer.", min_time=7.0):
            for _ in range(2):
                self.play(FadeIn(disk), disk.spin(turns=1, run_time=0.6))
                self.play(FadeOut(disk), ladder.promote(B, 1, run_time=0.4) if False else Indicate(gamer, scale_factor=1.1), run_time=0.5)
            self.play(coin.animate(run_time=1.2).move_to(B.get_center() + UP * 0.3).shift(RIGHT * 0.0), FadeIn(coin), D.change("blocked"), run_time=1.2)
            self.play(FadeIn(tear), run_time=0.3)
            self.play(FadeOut(coin), FadeOut(tear), run_time=0.4)

        # S08.5
        monster = proc("A", "zombie", scale=0.9, color="#8C9A8E", label=None).move_to(P3(3.0, -0.2))
        bolts = neck_bolts(0.7).scale(0.9).move_to(monster.get_center() + DOWN * 0.1)
        mon = VGroup(monster, bolts)
        self.say("I might have created a monster.", prof.change("surprised"), FadeIn(mon, shift=LEFT * 0.8), min_time=2.5)

        # S08.6
        tagf = name_tag("Prof. Frankenstein", 20).move_to(P3(5.2, -0.6))
        self.say("Professor Frankenstein is not what I'd like to be called.",
                 prof.change("worried"), Succession(Indicate(mon, scale_factor=1.15), FadeIn(tagf, shift=DOWN * 0.4)), min_time=4.0)

        # S08.7
        flame = Flame(0.8).move_to(stu.get_top() + UP * 0.55)
        flame.flicker()
        self.say("But isn't that the idea? To get us excited enough to look into it on our own? Lighting fires and all that?",
                 FadeOut(mon), FadeOut(tagf), stu.change("curious"), Succession(Wait(3.0), GrowFromCenter(flame)), min_time=6.5)

        # S08.8
        self.say("I guess so. But I didn't think it would work!", prof.change("happy"), min_time=3.5)
        self.beat(1.0)
