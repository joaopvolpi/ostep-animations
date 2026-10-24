import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403


class S04SheetMusic(Ep04Scene):
    def construct(self):
        self.add_badge()
        strip = crux_strip()
        stu, prof = self.add_corner_chars()
        self.add(strip)

        # S04.1
        disk = Disk().move_to(S04_DISK)
        file = s04_file(disk)
        self.say("To get there, first a distinction. A program is a lifeless thing.",
                 FadeOut(strip, run_time=0.6), FadeIn(disk, run_time=0.8), FadeIn(file, shift=DOWN * 0.3, run_time=0.8))

        # S04.2
        lines = VGroup(*[Text(s, font=MONO_FONT, font_size=18, color=DIM)
                         for s in ("load  r1, x", "add   r1, 1", "store r1, x", "jump  loop")])
        lines.arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        data = VGroup(RoundedRectangle(width=0.9, height=0.35, corner_radius=0.05).set_stroke(DIM, 2),
                      Text("data", font_size=18, color=DIM))
        data[1].move_to(data[0])
        body = VGroup(lines, data).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        pop = RoundedRectangle(width=body.width + 0.4, height=body.height + 0.35, corner_radius=0.1)
        pop.set_fill(CARD_FILL, 1).set_stroke(DIM, 2)
        popup = VGroup(pop, body.move_to(pop))
        popup.next_to(file, RIGHT, buff=0.35).shift(UP * 0.5)
        self.say("It's a file on your disk, a bunch of instructions and maybe some static data.",
                 GrowFromPoint(popup, file.get_right(), run_time=0.8))

        # S04.3
        zz = zz_glyph(0.35, DIM).next_to(file, UP, buff=0.1).shift(RIGHT * 0.25)
        self.say("It just sits there, waiting to spring into action.",
                 FadeOut(popup, run_time=0.6), FadeIn(zz, shift=UP * 0.2, run_time=0.8))
        self.beat(1.0)

        # S04.4
        sheet = sheet_music(0.75, 0.95).move_to(file.page)
        self.say("Think of sheet music. Sheet music is not a song.",
                 FadeOut(zz, run_time=0.4), ReplacementTransform(file, sheet, run_time=1.0))

        # S04.5
        flying = VGroup(*[eighth_note(0.2, c) for c in PROCESS_COLORS[:5]])
        for n, src in zip(flying, sheet.notes):
            n.move_to(src).set_color(DIM)
        targets = [S04_A + P3(-1.2 + 0.6 * k, 0.4 + 0.3 * np.sin(k)) for k in range(5)]
        self.say("Nothing happens until someone performs it.",
                 LaggedStart(*[n.animate(path_arc=-0.8).move_to(t).set_color(c)
                               for n, t, c in zip(flying, targets, PROCESS_COLORS[:5])],
                             lag_ratio=0.15, run_time=1.8))

        # S04.6
        file = s04_file(disk)
        a = proc("A", label="browser").move_to(S04_A)
        copy = file.copy()
        with self.narrate("The operating system is the performer. It takes those bytes and brings them to life."):
            self.play(ReplacementTransform(sheet, file), FadeOut(flying, scale=0.5), run_time=0.8)
            self.add(copy)
            self.play(copy.animate(path_arc=-0.6).move_to(S04_A), run_time=1.0)
            self.play(ReplacementTransform(copy, a), run_time=0.8)
            self.play(a.blink())
        self.beat(0.6)
        # S04.7
        self.say("That living, running program has a name: a process.",
                 self.term("process"), min_time=3.2)

        # S04.8
        defn = Text("process = a running program", font_size=30, color=TEXT)
        defn.next_to(a, DOWN, buff=0.35).set_x(1.6)
        self.say("Informally, that's the whole definition. A process is a running program.",
                 Write(defn, run_time=1.5))
        self.beat(0.5)

        # S04.9
        with self.narrate("So if I open two browser windows…"):
            self.play(stu.change("curious", look_at=file))
            self.play(Indicate(file, color=CPU_COLOR, scale_factor=1.3))

        # S04.10
        b = proc("B", label="browser").move_to(S04_B)
        copy2 = file.copy()
        brace, blab = s04_brace(a, b)
        with self.narrate("One program, two performances. Two processes."):
            self.add(copy2)
            self.play(copy2.animate(path_arc=-0.5).move_to(S04_B), FadeOut(defn), run_time=1.0)
            self.play(ReplacementTransform(copy2, b), prof.change("happy"), run_time=0.8)
            self.play(GrowFromCenter(brace), FadeIn(blab, shift=UP * 0.2), run_time=0.8)
        self.beat(1.0)
