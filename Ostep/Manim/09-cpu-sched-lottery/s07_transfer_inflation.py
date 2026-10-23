import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403
from s06_ticket_currency import tag_row  # noqa: E402


class S07TransferInflation(Ep09Scene):
    def construct(self):
        self.world(stu="neutral", prof="neutral")
        stu, prof = self.stu, self.prof
        tags = tag_row(1)
        self.add(tags)
        div = DashedLine(P3(0, 2.0), P3(0, -2.2), color=DIM, dash_length=0.1, stroke_width=2)

        client = proc("A", scale=0.6, label="client").move_to(P3(-5.0, 0.2))
        server = proc("C", scale=0.6, label="server").move_to(P3(-1.8, 0.2))
        cst = TicketStack(50, COL["A"]).move_to(P3(-5.0, 1.5))
        sst = TicketStack(50, COL["C"]).move_to(P3(-1.8, 1.5))
        p1 = proc("A", scale=0.6).move_to(P3(2.0, 0.2))
        p2 = proc("B", scale=0.6, color=DIM, label="greedy").move_to(P3(5.0, 0.2))
        st1 = TicketStack(50, COL["A"]).move_to(P3(2.0, 1.5))
        st2 = TicketStack(50, DIM).move_to(P3(5.0, 1.5))

        # S07.1
        req = Dot(radius=0.1, color=CPU_COLOR).move_to(client.get_center() + RIGHT * 0.5)
        self.say("Ticket transfer. A client asks a server for help, and lends it its tickets while the server works.",
                 self.term("ticket transfer"), FadeIn(div),
                 FadeIn(client), FadeIn(server), FadeIn(cst), FadeIn(sst))
        self.add(req)
        self.play(glide(req, server.get_center() + LEFT * 0.5, 0.7))
        self.play(FadeOut(req), cst.hop_to(P3(-3.4, 1.5), run_time=0.8), sst.set_count(100, run_time=0.8))

        # S07.2
        ok = tick_mark(0.35).move_to(P3(-3.4, 2.1))
        self.say("The server hands them back when it's done.",
                 cst.hop_to(P3(-5.0, 1.5), run_time=0.8), sst.set_count(50, run_time=0.8),
                 Succession(Wait(0.9), FadeIn(ok)))

        # S07.3
        self.say("Ticket inflation. A process raises or lowers its own ticket count.",
                 self.term("ticket inflation"), FadeIn(p1), FadeIn(st1), FadeOut(ok))
        self.play(st1.set_count(80), run_time=0.6)
        self.play(st1.set_count(50), run_time=0.6)

        # S07.4
        eks = x_mark(0.4).move_to(P3(5.0, 2.3))
        self.say("Among strangers that's useless, since a greedy process would print tickets and take over.",
                 FadeIn(p2), FadeIn(st2),
                 Succession(Wait(1.0), st2.set_count(1000000, run_time=1.2), FadeIn(eks)))

        # S07.5
        self.play(FadeOut(VGroup(p2, st2, eks)), run_time=0.5)
        hs = handshake_icon(0.8).move_to(P3(3.5, 0.9))
        f2 = proc("D", scale=0.6, label="friend").move_to(P3(5.0, 0.2))
        ok2 = tick_mark(0.35).move_to(P3(5.0, 2.0))
        self.say("Among friends, a process that needs the CPU can just say so.",
                 FadeIn(f2), FadeIn(hs), Succession(Wait(1.0), st1.set_count(60), FadeIn(ok2)))

        # S07.6
        self.say("So a ticket is a unit of ownership.", stu.change("curious"))

        # S07.7
        mem = Memory(cells=4, width=0.7, height=1.0, addresses=False).move_to(P3(-0.8, -1.7))
        cp = CPU(size=0.6, label="").move_to(P3(0.6, -1.7))
        tk = Ticket(COL["A"]).scale(1.6).move_to(P3(-0.1, -0.9))
        hint = Text("hypervisor memory share", font_size=18, color=DIM).move_to(P3(0, -2.5))
        self.say("Exactly. Need to represent a proportion of anything? Try a ticket.",
                 prof.change("proud"), FadeIn(mem), FadeIn(cp), FadeIn(tk), FadeIn(hint))
        self.play(FadeOut(VGroup(mem, cp, tk, hint)), run_time=0.8)
        self.play(FadeOut(VGroup(tags, div, client, server, cst, sst, p1, st1, f2, hs, ok2)), run_time=0.8)
