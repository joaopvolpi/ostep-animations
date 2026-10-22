import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403

LINE = {"mem": 1, "state": 3, "pid": 4, "parent": 5, "ofile": 6, "context": 7}


class S18Xv6PCB(Ep04Scene):
    def construct(self):
        self.add_badge()
        self.add_docked_term("process list")
        stu, prof = self.add_corner_chars()
        slot = docked_save_slot()
        w = build_s17_end()
        sd, ps, os_box, os_lab, cards, brace, blab = (w[k] for k in
                                                      ("sd", "ps", "os_box", "os_lab", "cards", "brace", "blab"))
        rest = VGroup(sd, *ps.values(), os_box, os_lab, brace, blab, *[cards[n] for n in ("B", "D", "C")])
        self.add(slot, rest, cards["A"])

        code = code_block(XV6_PROC, font_size=20)
        code.move_to(P3(-0.8, 0.35))
        cap = Text("xv6 (Figure 4.5, simplified)", font_size=20, color=DIM).next_to(code, DOWN, buff=0.15)

        # S18.1
        with self.narrate("Here's a real one, from a small teaching operating system called xv6."):
            veil = Rectangle(width=16, height=9).set_fill(BG, 0.8).set_stroke(width=0)
            self.add(veil, cards["A"], stu, prof, self.badge, self.terms.docked, slot)
            self.play(FadeIn(veil), run_time=0.6)
            self.play(ReplacementTransform(cards["A"], code), run_time=1.2)
            self.play(FadeIn(cap), run_time=0.4)

        # S18.2
        bar = code_line_bar(code, LINE["pid"], color=TEXT, opacity=0.15)
        with self.narrate("Each process has an ID, a state, a pointer to its memory, its open files, its parent."):
            self.play(FadeIn(bar), run_time=0.3)
            for name in ("state", "mem", "ofile", "parent"):
                self.wait(0.35)
                self.play(bar.animate.move_to(code_line_bar(code, LINE[name])), run_time=0.4)

        # S18.3
        cbar = code_line_bar(code, LINE["context"], color=CPU_COLOR, opacity=0.3)
        with self.narrate("And look at this field: the register context."):
            self.play(ReplacementTransform(bar, cbar), run_time=0.5)
            self.play(self.term("register context", size=44, at=P3(-0.8, 2.95)))

        # S18.4
        land = cbar.get_right() + LEFT * 0.45
        regs = RegisterBank([("eip", "40"), ("esp", "ff8"), ("ebx", "7"), ("ebp", "ffc")], cols=2,
                            box_width=1.15, box_height=0.38, font_size=18, title="registers")
        regs.move_to(P3(4.2, 1.75))
        with self.narrate("When a process is stopped, its registers get saved right here."):
            self.play(slot.animate.scale(1.3).move_to(land), run_time=1.0)
            self.play(FadeIn(regs, shift=LEFT * 0.2), FadeOut(rest), FadeOut(veil), run_time=0.6)
            dots = VGroup(*[Dot(radius=0.06, color=CPU_COLOR).move_to(regs.boxes[n]) for n in regs.names])
            self.play(LaggedStart(*[d.animate.move_to(slot) for d in dots], lag_ratio=0.2), run_time=1.2)
            self.remove(dots)

        # S18.5
        cpu = CPU(1.2).move_to(P3(4.4, -0.7))
        with self.narrate("To resume it, the OS loads them back into the real CPU."):
            self.play(FadeIn(cpu), run_time=0.6)
            dots = VGroup(*[Dot(radius=0.06, color=CPU_COLOR).move_to(slot) for _ in range(4)])
            self.add(dots)
            self.play(LaggedStart(*[d.animate.move_to(cpu.die) for d in dots], lag_ratio=0.2), run_time=1.2)
            self.play(FadeOut(dots), Indicate(cpu, color=CPU_COLOR), run_time=0.6)

        # S18.6
        self.say("That's the video-game save slot!", stu.change("excited", look_at=slot), min_time=1.8)

        # S18.7
        tag = ep_tag("context switch → Ep. 06").scale(0.85).next_to(cpu, DOWN, buff=0.25)
        with self.narrate("That's the one. Restoring it is the context switch."):
            self.play(prof.change("proud", look_at=stu), FadeIn(tag, scale=1.2), run_time=0.7)
            self.play(FadeOut(slot, scale=0.4), FadeOut(regs), cbar.animate.set_fill(CPU_COLOR, 0.45), run_time=0.8)
        self.beat(0.8)
