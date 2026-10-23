import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


class S03Tickets(Ep09Scene):
    def construct(self):
        self.world(term="proportional share", pie=True, stu="neutral", prof="neutral")
        stu, prof = self.stu, self.prof
        W = build_s03_world()
        cpu, drum, a, b, sa, sb, strip = (W[k] for k in ("cpu", "drum", "a", "b", "sa", "sb", "strip"))

        # S03.1
        paper = paper_chip("Waldspurger & Weihl, 1994").move_to(P3(0, 2.0))
        self.say("Here's the idea, from a paper by Waldspurger and Weihl.",
                 FadeIn(paper, shift=UP * 0.2),
                 Succession(Wait(1.6), paper.animate(run_time=1.0).scale(0.75).move_to(P3(-4.4, 2.1))))

        # S03.2
        self.add(cpu)
        ball, anim = drum.draw(42, CPU_COLOR)
        self.add(drum)
        self.say("Every so often, hold a lottery to decide who runs next.",
                 FadeIn(cpu), FadeIn(drum), Succession(Wait(0.4), drum.spin(1, run_time=1.5), anim))
        self.play(FadeOut(ball), run_time=0.4)

        # S03.3
        sa_empty = TicketStack(75, COL["A"], show_count=False).move_to(sa)
        sb_empty = TicketStack(25, COL["B"], show_count=False).move_to(sb)
        self.add(a, b)
        a.set_opacity(0)
        b.set_opacity(0)
        self.say("Processes that deserve more of the CPU get more chances to win. That's lottery scheduling.",
                 self.term("lottery scheduling", hold=1.0),
                 a.animate.set_opacity(1), b.animate.set_opacity(1), FadeIn(sa_empty), FadeIn(sb_empty))

        # S03.4
        t = Ticket(COL["A"]).move_to(sa_empty.get_center())
        self.add(t)
        self.say("The thing you hold is a ticket.",
                 self.term("ticket", hold=0.8),
                 Succession(Wait(0.5), glide(t, P3(0, -2.0), 0.8),
                            Wait(0.3), AnimationGroup(FadeOut(t))))

        # S03.5
        cap = caption_at("tickets = share", y=-2.45, size=26)
        self.say("Tickets represent a share. The percent of the tickets you own is the percent of the resource you should get.",
                 FadeIn(cap), FadeOut(sa_empty), FadeOut(sb_empty), FadeIn(sa), FadeIn(sb))

        # S03.6
        labs = strip_labels(strip)
        total = Text("total: 100", font_size=20, color=DIM).move_to(P3(5.75, STRIP3_Y - 0.42))
        for n in strip.order:
            strip.segs[n].set_opacity(0)
            strip.seg_labels[n].set_opacity(0)
        self.add(strip)
        self.say("Say process A holds seventy-five tickets and process B holds twenty-five. A hundred in total, "
                 "numbered zero to ninety-nine.",
                 Create(strip.line),
                 Succession(Wait(1.0), AnimationGroup(*[strip.segs[n].animate(run_time=1.2).set_opacity(0.9) for n in strip.order],
                                                       *[strip.seg_labels[n].animate(run_time=1.2).set_opacity(1) for n in strip.order]),
                            AnimationGroup(FadeIn(labs), FadeIn(total))))

        # S03.7
        ball, anim = drum.draw(63, COL["A"])
        mk = strip.marker_at(63)
        with self.narrate("Each time slice, the scheduler picks a winning number, finds its owner, and runs that process."):
            self.play(anim)
            self.play(glide(ball, mk.get_center() + UP * 0.1, 0.6))
            self.play(FadeOut(ball), FadeIn(mk), Indicate(strip.segs["A"], color=COL["A"], scale_factor=1.05))
            self.play(hop_to(a, cpu.slot_point(), run_time=0.8))
        a.set_expression("running")
        self.beat(1.0)

        # S03.8
        self.say("A raffle! Draw a ticket, run the winner!", stu.change("excited"))
        self.beat(0.5)
