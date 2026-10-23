import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


class S06Allotment(Ep08Scene):
    def construct(self):
        s05_end(self, stu="neutral", prof="explaining")
        lad, cpu, board = self.ladder, self.cpu, self.board
        A, B = self.jobs["A"], self.jobs["B"]
        tl = make_tl(20)

        # S06.1
        self.play(FadeOut(VGroup(A, B)), run_time=0.5)
        lad.release(A); lad.release(B)
        self.add(tl)
        self.say("To turn this into rules, we need one new concept: the allotment.",
                 self.term("allotment"), FadeIn(tl, shift=UP * 0.8))

        # S06.2
        A2 = job("A", lad.job_scale, "running")
        place_on(A2, cpu.slot_point())
        g = self.attach_gauge(A2, 1.0, 1.0)
        lab = label("allotment", 18, DIM).next_to(g, LEFT, buff=0.15)
        darr = Arrow(g.get_left() + LEFT * 0.1 + DOWN * 0.1, g.get_left() + LEFT * 0.1 + DOWN * 0.7, buff=0, color=KERNEL_COLOR, stroke_width=5)
        self.say("It's the amount of time a job can spend at a given priority level before the scheduler lowers its priority.",
                 FadeIn(A2, shift=DOWN * 0.3), FadeIn(g), Succession(Wait(1.0), FadeIn(lab)),
                 Succession(Wait(2.5), g.drain(1.0, run_time=1.5)), Succession(Wait(5.0), FadeIn(darr, shift=DOWN * 0.2)))
        self.play(FadeOut(darr), FadeOut(lab), run_time=0.4)

        # S06.3
        tag = label("allotment = 1 time slice\n= 10 ms", 18, CPU_COLOR, line_spacing=0.8).move_to(P3(1.7, -0.15))
        br = tl.bracket("Q2", 0, 1, "10 ms")
        self.say("To keep things simple, we'll say for now that the allotment is exactly one time slice.",
                 FadeIn(tag), g.reset(), Succession(Wait(1.0), Create(br.line), FadeIn(br.caps), FadeIn(br.label)))
        self.play(FadeOut(VGroup(A2, g)), run_time=0.4)

        # S06.4
        B.set_expression("ready")
        B.move_to(lad.lane_point(2, 0))
        lad.register(B, 2, 0)
        self.say("Rule three: when a job enters the system, it starts at the highest priority, the topmost queue.",
                 board.add_rule("R3", RULES["R3"]), FadeIn(B, shift=DOWN * 0.8))

        # S06.5
        gB = self.attach_gauge(B, 1.0, 1.0)
        self.say("Rule four, part A: if a job uses up its allotment while running, it moves down one queue.",
                 board.add_rule("R4a", RULES["R4a"]),
                 Succession(self.to_cpu(B), FadeIn(gB), gB.drain(1.0, run_time=1.4), self.to_lane(B, 1, 0, "ready"), gB.reset(0.4)))

        # S06.6
        clk = ClockIcon(0.3, color=TEXT).move_to(BLOCK_AT)
        self.say("Rule four, part B: if a job gives up the CPU, for example for an I/O, before its allotment is up, it stays where it is, and its allotment is reset.",
                 board.add_rule("R4b", RULES["R4b"]),
                 Succession(self.to_cpu(B), gB.drain(0.5, run_time=1.0),
                            Succession(SetExpr(B, "blocked"), hop_to(B, BLOCK_SPOT, run_time=0.5), FadeIn(clk), clk.spin(1, run_time=1.2)),
                            FadeOut(clk), gB.reset(0.5), self.to_lane(B, 1, 0, "ready")))

        # S06.7
        yd = board.row_y("R4a"); yr = board.row_y("R4b")
        dn = Arrow(P3(6.2, yd + 0.15), P3(6.2, yd - 0.15), buff=0, color=KERNEL_COLOR, stroke_width=4, tip_length=0.12)
        rs = loop_arrow(0.12, color=PERS).move_to(P3(6.2, yr))
        self.say("So a job that keeps the CPU too long gets punished, and a job that's polite gets to stay?",
                 self.stu.change("curious"), FadeIn(dn), FadeIn(rs))

        # S06.8
        self.say("Exactly. Let's watch it work.", self.prof.change("happy"), FadeOut(VGroup(B, gB, br)), FadeOut(tag))

        # S06.9
        st = label("slice = 10 ms", 20, CPU_COLOR).move_to(P3(1.7, -0.15))
        self.say("From now on we use three queues, which the book calls Q2, Q1 and Q0, and a ten-millisecond time slice.",
                 *[Indicate(lad.labels[k], color=CPU_COLOR) for k in (2, 1, 0)], FadeIn(st))
        self.beat(0.5)
