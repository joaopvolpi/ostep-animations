import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


class S13Signals(Ep05Scene):
    def construct(self):
        self.add_badge()
        self.add_docked_term("pipe")
        stu, prof = student_corner("neutral"), prof_corner("neutral")   # S12 ended without hosts
        p = proc(PAR, "running").move_to(P3(0, 0.8))

        def hit(proc_, bolt, target_dx=-0.9):
            return bolt.animate(run_time=0.8, rate_func=rush_into).move_to(proc_.get_center() + RIGHT * target_dx)

        def squash(proc_):
            return proc_.animate(run_time=0.5, rate_func=there_and_back).stretch(1.2, 0).stretch(0.85, 1)

        # S13.1
        bolt = bolt_glyph(0.8, CPU_COLOR, "kill(pid, sig)").move_to(P3(-4.2, 2.8))
        with self.narrate("Back to the interface. Beyond those three calls, there are more. "
                          "In UNIX, kill() sends a signal to a process."):
            self.play(FadeIn(p, scale=0.6), FadeIn(stu), FadeIn(prof), self.terms.note("signal"))
            self.play(FadeIn(bolt, scale=0.5), run_time=0.4)
            self.play(hit(p, bolt))
            self.play(squash(p), FadeOut(bolt, scale=0.3), run_time=0.5)

        # S13.2
        bolt2 = bolt_glyph(0.5, CPU_COLOR).move_to(P3(-2.6, 2.4))
        chips = VGroup(PauseGlyph(0.4), x_mark(0.4), Text("...", font=MONO_FONT, font_size=40, color=TEXT))
        chips.arrange(RIGHT, buff=0.7).move_to(P3(0.2, 2.5))
        with self.narrate("A signal can tell the process to pause, to die, or other useful things."):
            self.play(FadeIn(bolt2), run_time=0.3)
            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.8) for c in chips], lag_ratio=0.4), run_time=1.5)
            self.wait(1.0)
            self.play(FadeOut(chips), FadeOut(bolt2), run_time=0.5)

        # S13.3
        kb = keyboard_icon(1.2).move_to(P3(-3.8, 0.0))
        caps = VGroup(Keycap("ctrl"), Keycap("c")).arrange(RIGHT, buff=0.12).move_to(P3(-3.8, -0.85))
        sig = bolt_glyph(0.6, CPU_COLOR, "SIGINT").move_to(kb.get_top() + UP * 0.5)
        pf = puff(0.5).move_to(p)
        with self.narrate("Your shell wires some to keystrokes: control-c sends an interrupt, which normally "
                          "terminates the process."):
            self.play(FadeIn(kb), FadeIn(caps), stu.change("curious", look_at=kb), run_time=0.7)
            self.play(caps[0].press(0.3), caps[1].press(0.3))
            self.play(FadeIn(sig, scale=0.5), run_time=0.3)
            self.play(sig.animate(run_time=0.9).move_to(p.get_center() + LEFT * 0.9 + UP * 0.2))
            self.play(p.change("done"), FadeOut(sig), run_time=0.5)
            self.play(FadeOut(p, scale=0.1), FadeIn(pf, scale=0.3), run_time=0.5)
            self.play(FadeOut(pf, scale=1.6), run_time=0.4)

        # S13.4
        p2 = proc(PAR, "running").move_to(P3(0, 0.8))
        caps2 = VGroup(Keycap("ctrl"), Keycap("z")).arrange(RIGHT, buff=0.12).move_to(caps)
        sig2 = bolt_glyph(0.6, CPU_COLOR, "SIGTSTP").move_to(sig)
        pz = PauseGlyph(0.5).move_to(p2.get_center() + UP * 0.1)
        term = mk_term(4.5, 1, 18).move_to(P3(0, -2.2))
        pl = PlayGlyph(0.5).move_to(pz)
        with self.narrate("Control-z sends a stop, which pauses it, and you can resume it later with fg."):
            self.play(FadeIn(p2, scale=0.6), Transform(caps, caps2), run_time=0.6)
            self.play(caps[0].press(0.3), caps[1].press(0.3))
            self.play(FadeIn(sig2, scale=0.5), run_time=0.3)
            self.play(sig2.animate(run_time=0.9).move_to(p2.get_center() + LEFT * 0.9 + UP * 0.2))
            self.play(FadeOut(sig2), p2.animate.set_opacity(0.4), FadeIn(pz, scale=1.4), run_time=0.5)
            self.wait(0.5)
            self.play(FadeIn(term), term.type("fg"))
            self.play(ReplacementTransform(pz, pl), p2.animate.set_opacity(1.0), run_time=0.5)
            self.play(FadeOut(pl), run_time=0.4)

        # S13.5
        pill = VGroup(info_tag("Misc. control", TEXT, 20, DIM), tick_mark(0.25)).arrange(RIGHT, buff=0.15)
        pill.move_to(P3(-4.6, 2.75))
        with self.narrate('That\'s the "suspend and resume" from our menu.'):
            self.play(stu.change("neutral"), FadeIn(pill, scale=0.7), run_time=0.6)
            self.wait(1.2)
            self.play(FadeOut(pill), run_time=0.4)

        # S13.6
        hb = handler_box("handler()").move_to(p2.get_center() + RIGHT * 1.5 + UP * 0.6)
        sig3 = bolt_glyph(0.5, CPU_COLOR).move_to(P3(-3.0, 2.4))
        with self.narrate("A process can also catch a signal with signal()…"):
            self.play(FadeIn(hb, shift=LEFT * 0.2), run_time=0.5)
            self.play(FadeIn(sig3), run_time=0.2)
            self.play(sig3.animate(run_time=1.2).move_to(hb.get_center() + UP * 0.1))
            self.play(Flash(hb.get_center(), color=CPU_COLOR, flash_radius=0.5), FadeOut(sig3, scale=0.2), run_time=0.5)

        # S13.7
        lines = VGroup(*[mono(s, 18, TEXT) for s in ("handler() {", "  ...", "}")]).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        lines.next_to(hb, DOWN, buff=0.2, aligned_edge=LEFT)
        with self.narrate("…run its own code when one arrives."):
            self.play(LaggedStart(*[FadeIn(l, shift=DOWN * 0.2) for l in lines], lag_ratio=0.4), run_time=1.5)
            self.wait(1.0)
        self.beat(0.5)

        # transition: everything fades
        self.play(*[FadeOut(m) for m in (p2, hb, lines, kb, caps, term)], run_time=0.8)
