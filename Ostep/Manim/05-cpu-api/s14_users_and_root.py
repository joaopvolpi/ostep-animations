import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


class S14UsersAndRoot(Ep05Scene):
    def construct(self):
        self.add_badge()
        self.add_docked_term("signal")
        stu, prof = self.add_corner_chars("neutral", "neutral")

        coral = proc(PAR, "ready", scale=0.8, label="A")
        gold = proc(SHC, "ready", scale=0.8, label="B")
        VGroup(coral, gold).arrange(RIGHT, buff=0.5).move_to(P3(-3.6, 0.8))
        sky = proc(SKY, "ready", scale=0.8, label="C").move_to(P3(3.6, 0.8))
        box_l = RoundedRectangle(width=3.4, height=2.2, corner_radius=0.2).set_stroke(DIM, 2.5).move_to(P3(-3.6, 0.8))
        box_r = RoundedRectangle(width=2.2, height=2.2, corner_radius=0.2).set_stroke(DIM, 2.5).move_to(P3(3.6, 0.8))
        tag_l = name_tag("you", 20).scale(0.7).next_to(box_l, UP, buff=0.12)
        tag_r = name_tag("roommate", 20).scale(0.7).next_to(box_r, UP, buff=0.12)
        shield = shield_arc(1.7, LEFT, PI * 0.8, USER_COLOR, center=P3(3.6, 0.8))

        # S14.1
        bolt = bolt_glyph(0.6, CPU_COLOR).move_to(P3(-2.2, 1.0))
        with self.narrate("Wait. Then can I kill anyone's process? Say, the one my roommate started on the same machine?"):
            self.play(stu.change("curious"), FadeIn(VGroup(coral, gold, sky, box_l, box_r)), run_time=0.8)
            self.play(FadeIn(shield), FadeIn(bolt), run_time=0.5)
            self.play(bolt.animate(run_time=1.0).move_to(P3(1.9, 1.0)))
            self.play(bolt.animate(run_time=0.5).shift(LEFT * 1.0).set_opacity(0))
            self.remove(bolt)

        # S14.2
        bolt = bolt_glyph(0.6, CPU_COLOR).move_to(P3(-2.2, 0.0))
        with self.narrate("That's why systems have users. You log in, and you can control your own processes. "
                          "Not anybody else's."):
            self.play(prof.change("explaining"), self.terms.note("user"))
            self.play(FadeIn(tag_l), FadeIn(tag_r), run_time=0.6)
            self.play(FadeIn(bolt), run_time=0.2)
            self.play(bolt.animate(run_time=0.7).move_to(coral.get_center() + RIGHT * 0.5))
            self.play(Indicate(coral, scale_factor=1.1, color=KERNEL_COLOR), FadeOut(bolt, scale=0.3), run_time=0.6)
            b2 = bolt_glyph(0.6, CPU_COLOR).move_to(gold.get_right() + RIGHT * 0.3)
            self.play(FadeIn(b2), run_time=0.2)
            self.play(b2.animate(run_time=0.8).move_to(P3(1.9, 0.9)))
            self.play(b2.animate(run_time=0.4).shift(LEFT * 1.0).set_opacity(0))
            self.remove(b2)

        # S14.3
        lock = padlock_icon(0.5).move_to(P3(1.8, 0.8))
        with self.narrate("Sharing the machine safely needs that rule."):
            self.play(FadeIn(lock, scale=0.5), run_time=0.6)
            self.wait(1.4)

        # S14.4
        root = proc(VIO, "ready", scale=0.6).move_to(P3(0, 1.6))
        crown = crown_tag("root").move_to(P3(0, 2.8))
        bolt = bolt_glyph(0.6, CPU_COLOR).move_to(P3(0.7, 1.7))
        with self.narrate("There's one exception: the superuser, or root."):
            self.play(self.terms.note("superuser (root)"), FadeIn(root, shift=DOWN * 0.5), FadeIn(crown, shift=DOWN * 0.3))
            self.play(FadeIn(bolt), run_time=0.2)
            self.play(bolt.animate(run_time=1.0).move_to(sky.get_center() + LEFT * 0.6))
            self.play(Indicate(sky, scale_factor=1.1, color=KERNEL_COLOR), FadeOut(bolt, scale=0.3), run_time=0.6)

        # S14.5
        warn = VGroup(Polygon(P3(-0.3, -0.25), P3(0.3, -0.25), P3(0, 0.3)).set_fill(CPU_COLOR, 1).set_stroke(TEXT, 2),
                      Text("!", font_size=24, color=BG, weight="BOLD").move_to(P3(0, -0.07)))
        sd = VGroup(warn, program_chip("shutdown", KERNEL_COLOR, 20)).arrange(RIGHT, buff=0.15).move_to(P3(0, -0.9))
        with self.narrate("They can administer the system and control any process. Powerful, and dangerous. Use it rarely."):
            self.play(Indicate(crown, scale_factor=1.2), run_time=0.8)
            self.play(FadeIn(sd, scale=0.7), run_time=0.5)
            self.wait(1.5)
            self.play(FadeOut(sd), run_time=0.4)

        # S14.6
        aside = AsideCard("With great power comes great responsibility.", title="THE SUPERUSER", width=4.4, font_size=24)
        aside.move_to(P3(0, -1.5))
        with self.narrate("With great power comes great responsibility. The French Revolution said it first, apparently."):
            self.play(prof.change("worried"), aside.slide_in(RIGHT), run_time=0.8)
            self.wait(3.0)
            self.play(aside.slide_out(RIGHT), run_time=0.6)
        self.beat(0.5)

        self.play(*[FadeOut(m) for m in (coral, gold, sky, box_l, box_r, tag_l, tag_r, shield, lock, root, crown)], run_time=0.8)
