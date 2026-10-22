import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


def code_word(code, line, word):
    """Glyphs of ``word`` in a Code line (Code drops spaces from its glyph list)."""
    s = code.code_lines[line]
    src = XV6_ENUM.split("\n")[line].replace(" ", "")
    i = src.find(word)
    return s[i:i + len(word)]


class S19Zombies(Ep04Scene):
    def construct(self):
        self.add_badge()
        self.add_docked_term("register context")
        stu, prof = self.add_corner_chars("excited", "proud")
        code = code_block(XV6_PROC, font_size=20).move_to(P3(-0.8, 0.35))
        cbar = code_line_bar(code, 7, color=CPU_COLOR, opacity=0.45)
        cap = Text("xv6 (Figure 4.5, simplified)", font_size=20, color=DIM).next_to(code, DOWN, buff=0.15)
        cpu = CPU(1.2).move_to(P3(4.4, -0.7))
        tag = ep_tag("context switch → Ep. 06").scale(0.85).next_to(cpu, DOWN, buff=0.25)
        self.add(code, cbar, cap, cpu, tag)

        enum = code_block(XV6_ENUM, font_size=18).move_to(P3(-3.4, 2.1))
        parent_pos, child_pos = P3(-1.5, -0.6), P3(1.5, -0.6)

        # S19.1
        emb, zom = code_word(enum, 0, "EMBRYO"), code_word(enum, 1, "ZOMBIE")
        with self.narrate("Real systems also have a couple more states."):
            self.play(ReplacementTransform(VGroup(code, cbar), enum), FadeOut(cap), FadeOut(cpu), FadeOut(tag),
                      stu.change("neutral"), prof.change("neutral"), run_time=1.2)
            self.play(emb.animate.set_color(VIRT), zom.animate.set_color(VIRT), run_time=0.4)
            self.play(Indicate(emb, color=VIRT, scale_factor=1.3), Indicate(zom, color=VIRT, scale_factor=1.3),
                      run_time=0.8)

        # S19.2
        child = proc("D", "ready", label="child").move_to(child_pos)
        make_translucent(child, 0.4, 0.5)
        frags = VGroup(*[Square(0.12).set_fill(COL["D"], 0.8).set_stroke(width=0)
                         .move_to(child_pos + P3(np.cos(a) * 1.6, np.sin(a) * 1.3)) for a in np.linspace(0, TAU, 9)[:-1]])
        with self.narrate("There's an initial state while a process is being created."):
            self.play(self.term("initial", hold=0.7))
            self.play(FadeIn(frags), run_time=0.3)
            self.play(*[f.animate.move_to(child_pos).scale(0.3) for f in frags], run_time=0.8)
            self.play(FadeOut(frags), FadeIn(child, scale=0.6), run_time=0.5)

        # S19.3
        with self.narrate("And there's a final state, where a process has exited but hasn't been cleaned up yet. "
                          "On UNIX that's called the zombie state."):
            self.play(child.animate.set_opacity(1), run_time=0.4)
            self.play(child.change("done"), run_time=0.7)
            self.wait(1.2)
            self.play(child.change("zombie"), run_time=0.9)
            self.play(self.term("zombie", hold=0.7))

        # S19.4
        parent = proc("A", "ready", label="parent").move_to(parent_pos)
        link = Line(parent.get_right() + RIGHT * 0.1, child.get_left() + LEFT * 0.1).set_stroke(DIM, 2)
        llab = Text("parent of", font_size=20, color=DIM).next_to(link, UP, buff=0.08)
        with self.narrate("It sounds spooky, but it's useful. It lets the process's parent, the process that created it…"):
            self.wait(1.2)
            self.play(FadeIn(parent, shift=RIGHT * 0.3), run_time=0.6)
            self.play(Create(link), FadeIn(llab), run_time=0.6)
            self.play(self.term("parent", hold=0.6))

        # S19.5
        ok = exit_tag(0).next_to(child, DOWN, buff=0.15)
        bad = exit_tag(1).move_to(ok)
        with self.narrate("…check its return code. Zero usually means success, anything else means something went wrong."):
            self.play(FadeIn(ok, shift=DOWN * 0.2), run_time=0.5)
            self.wait(1.0)
            self.play(ReplacementTransform(ok, bad), run_time=0.4)
            self.wait(0.8)
            ok2 = exit_tag(0).move_to(bad)
            self.play(ReplacementTransform(bad, ok2), run_time=0.4)

        # S19.6
        with self.narrate("The parent calls wait(), reads the result, and the OS cleans up."):
            self.play(parent.says(Text("wait()", font=MONO_FONT, font_size=28, color=TEXT)), run_time=0.7)
            self.play(ok2.animate.next_to(parent, DOWN, buff=0.15), run_time=0.8)
            self.play(FadeOut(child, scale=0.3), FadeOut(link), FadeOut(llab), run_time=0.8)
            self.play(parent.remove_bubble(), FadeOut(ok2), run_time=0.5)

        # S19.7
        self.say("Zombies. In my operating system.", stu.change("surprised", look_at=parent), min_time=2.0)

        # S19.8
        self.say("Relatively easy to kill, too. Different techniques are recommended, though.",
                 prof.change("happy", look_at=stu))
        self.beat(0.8)

        # transition: everything fades (badge stays)
        self.play(FadeOut(VGroup(parent, enum)), FadeOut(self.terms.docked),
                  FadeOut(stu), FadeOut(prof), run_time=0.8)
