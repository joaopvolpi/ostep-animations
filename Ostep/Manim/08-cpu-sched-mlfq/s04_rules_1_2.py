import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


class S04Rules12(Ep08Scene):
    def construct(self):
        card = s03_end(self)
        lad, cpu, board = self.ladder, self.cpu, self.board
        spot = Spotlight(height=0.7, spread=0.3)
        spot.move_beam_to(lad.lane_point(8, 3))
        lad.lane_rect(8).set_stroke(CPU_COLOR, 3.5).set_fill(CPU_COLOR, 0.12)
        self.add(spot)
        A, B, C, D = (self.jobs[n] for n in "ABCD")
        self.play(card.slide_out(DOWN), run_time=0.7)

        # S04.1
        nope = VGroup(x_mark(0.22), label("not now", 18, KERNEL_COLOR)).arrange(RIGHT, buff=0.08).next_to(C, RIGHT, buff=0.1)
        self.say("Rule one: if the priority of A is greater than the priority of B, A runs, and B doesn't.",
                 board.add_rule("R1", RULES["R1"]), self.to_cpu(A),
                 after(1.5, AnimationGroup(Wiggle(C, scale_value=1.2, run_time=0.8), FadeIn(nope))))
        self.play(FadeOut(nope), run_time=0.4)

        # S04.2
        ring = rr_ring(0.2).move_to(lad.lane_point(8, 2.1))
        self.say("Rule two: if A and B have the same priority, they take turns, round robin.",
                 board.add_rule("R2", RULES["R2"]),
                 Succession(self.to_lane(A, 8, 0), self.to_cpu(B), self.to_lane(B, 8, 1), self.to_cpu(A)), after(2.5, FadeIn(ring)))

        # S04.3
        rr_tag = label("RR · time slice", 18, TEXT)
        ep = ep_tag("← Ep. 07")
        chip = VGroup(rr_tag, ep).arrange(RIGHT, buff=0.12).move_to(lad.lane_point(8, 5.2) + LEFT * 0.2 + DOWN * 0.08)
        self.say("That's the same time-slice rotation we already know.", FadeIn(chip, shift=LEFT * 0.3))

        # S04.4
        tl = Timeline(["CPU"], ticks=8, colors=[CPU_COLOR], x_range=TL_X, top=-2.0, row_height=0.4, tick_labels=False, label_font=20)
        self.add(tl)
        self.play(FadeIn(tl), run_time=0.5)
        anims = []
        for t in range(1, 9):
            name = "A" if t % 2 else "B"
            anims.append(Succession(*([Wait(0.0)]), tl.fill("CPU", t, "running", color=COL[name], run_time=0.3), Wait(0.0)))
        seq = []
        cur = A
        for t in range(1, 9):
            name = "A" if t % 2 else "B"
            seq.append(tl.fill("CPU", t, "running", color=COL[name], run_time=0.35))
        self.say("So with this picture, A and B alternate forever.", Succession(*seq))

        # S04.5
        zA = zz_glyph(0.22).next_to(C, RIGHT, buff=0.05)
        zB = zz_glyph(0.22).next_to(D, RIGHT, buff=0.05)
        self.say("And C and D?", Indicate(C, scale_factor=1.6), after(0.9, Indicate(D, scale_factor=1.6)),
                 after(0.4, FadeIn(zA), FadeIn(zB)))

        # S04.6
        st = label("starved?", 44, KERNEL_COLOR, weight=BOLD).move_to(P3(-2.5, -0.1))
        self.say("They never run! That's an outrage.", self.stu.change("frustrated"),
                 Succession(FadeIn(st, scale=1.4), Wait(1.0), FadeOut(st)))

        # S04.7
        bm = bookmark_glyph(0.4).move_to(P3(3.6, -1.4))
        bmt = label("starvation: later", 16, DIM).next_to(bm, RIGHT, buff=0.1)
        self.say("It is, and we'll come back to it.", self.prof.change("worried"), self.stu.change("neutral"),
                 FadeIn(bm, scale=1.4), FadeIn(bmt))

        # S04.8
        q = question_mark(0.8).move_to(P3(-2.5, 0.2))
        self.say("But first: with priorities this rigid, everything depends on where each job sits. So who decides that?",
                 FadeIn(q, scale=1.4), Indicate(lad.arrows.up, color=CPU_COLOR), after(0.5, Indicate(lad.arrows.down, color=CPU_COLOR)),
                 after(1.5, Indicate(q)))
        self.beat(1.0)
