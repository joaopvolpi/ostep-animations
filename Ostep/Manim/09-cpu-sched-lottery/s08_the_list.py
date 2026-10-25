import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from lottery_world import *  # noqa: E402,F401,F403


class S08TheList(Ep09Scene):
    def construct(self):
        self.world(stu="curious", prof="proud")
        W = build_s08()
        cw, jl, bars, total, drum, dlab, cpu = (W[k] for k in ("cw", "jl", "bars", "total", "drum", "dlab", "cpu"))

        # S08.1
        for i in range(4, 10):
            cw.line_mob(i).set_opacity(0.35)
        self.say("How hard is it to build? Barely.", FadeIn(cw), FadeIn(cpu))

        # S08.2
        bar = cw.add_bar(CPU_COLOR, line=2)
        node_anims = [FadeIn(jl.head), FadeIn(jl.head_arrow)]
        for i in range(3):
            node_anims += [FadeIn(jl.nodes[i], scale=0.6), Create(jl.arrows[i])]
        node_anims.append(FadeIn(jl.null))
        self.say("You need a good random number generator, a list of processes, and the total number of tickets.",
                 FadeIn(drum), FadeIn(dlab), FadeIn(bar),
                 Succession(Wait(1.5), LaggedStart(*node_anims, lag_ratio=0.15, run_time=2.5), FadeIn(total)))

        # S08.3
        self.say("Three jobs. A has a hundred tickets, B has fifty, C has two hundred and fifty. Four hundred in total.",
                 LaggedStart(*[FadeIn(c) for c in jl.captions], lag_ratio=0.5, run_time=2.0),
                 Succession(Wait(1.5), LaggedStart(*[GrowFromEdge(b, LEFT) for b in bars], lag_ratio=0.4, run_time=2.0)))

        # S08.4
        win = winner_text("?")
        self.add(win)
        ball, anim = drum.draw(300, CPU_COLOR, run_time=0.9)
        ball[0].scale(1.5)   # three digits fit inside the small ball
        ball[1].scale(0.85)
        with self.narrate("Say the random number comes out as three hundred."):
            self.play(FadeIn(win), drum.spin(1, run_time=1.0))
            self.play(anim)
            self.play(glide(ball, win.get_left() + LEFT * 0.5, 0.6))
            self.play(FadeOut(ball), Transform(win, winner_text(300)))

        # S08.5
        for i in range(4, 10):
            cw.line_mob(i).set_opacity(1.0)
        cnt = counter_text(0)
        ptr = jl.pointer(0)
        self.add(ptr)
        ptr.set_opacity(0)
        self.say("Walk the list with a counter. Start at zero.",
                 FadeIn(cnt), ptr.animate.set_opacity(1),
                 Succession(cw.move_bar(0, 3, run_time=0.6), cw.move_bar(0, 4, run_time=0.6)))

        # S08.6
        bubble = Text("100 > 300? no", font_size=22, color=TEXT, font=MONO_FONT).move_to(P3(2.0, -2.0), aligned_edge=LEFT)
        nx = x_mark(0.3).next_to(bubble, RIGHT, buff=0.15)
        self.say("A adds a hundred: the counter is a hundred. Is that more than three hundred? No, keep going.",
                 Succession(cw.move_bar(0, 5, run_time=0.5), Transform(cnt, counter_text(100), run_time=0.7),
                            cw.move_bar(0, 6, run_time=0.6), AnimationGroup(FadeIn(bubble), FadeIn(nx))))

        # S08.7
        bubble2 = Text("150 > 300? no", font_size=22, color=TEXT, font=MONO_FONT).move_to(bubble, aligned_edge=LEFT)
        dx = jl.node_center(1) - jl.node_center(0)
        self.say("B adds fifty: a hundred and fifty. Still no.",
                 Succession(AnimationGroup(FadeOut(bubble), FadeOut(nx), glide(ptr, ptr.get_center() + dx, 0.7)),
                            cw.move_bar(0, 5, run_time=0.4), Transform(cnt, counter_text(150), run_time=0.5),
                            cw.move_bar(0, 6, run_time=0.4), FadeIn(bubble2)))

        # S08.8
        bubble3 = Text("400 > 300? yes", font_size=22, color=TEXT, font=MONO_FONT).move_to(bubble, aligned_edge=LEFT)
        ok = tick_mark(0.3).next_to(bubble3, RIGHT, buff=0.15)
        ring = Circle(radius=jl.nodes[2][0].width / 2).set_fill(opacity=0).set_stroke(CPU_COLOR, 5).move_to(jl.node_center(2))
        pc = proc("C", scale=0.4, label="").move_to(jl.node_center(2) + UP * 0.85)
        self.add(pc)
        pc.set_opacity(0)
        self.say("C adds two hundred and fifty: four hundred. Now it's more than three hundred. Stop. C wins.",
                 Succession(AnimationGroup(FadeOut(bubble2), glide(ptr, ptr.get_center() + dx, 0.7)),
                            cw.move_bar(0, 5, run_time=0.4), Transform(cnt, counter_text(400), run_time=0.5),
                            cw.move_bar(0, 6, run_time=0.4), AnimationGroup(FadeIn(bubble3), FadeIn(ok)),
                            cw.move_bar(0, 7, run_time=0.5),
                            AnimationGroup(FadeIn(ring), pc.animate.set_opacity(1)),
                            hop_to(pc, cpu.slot_point(), run_time=0.9)))
        self.beat(0.5)
