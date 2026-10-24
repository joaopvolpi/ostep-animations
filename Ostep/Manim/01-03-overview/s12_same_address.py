import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from manim import *  # noqa: E402,F403
from ostep_lib import *  # noqa: E402,F403
from common import *  # noqa: E402,F403

DIV_Y = 0.55
PHYS_Y = -1.1
PHYS_IDX = (3, 11)


def top_strip(x):
    return MemoryStrip(n=5, cell_width=0.9, cell_height=0.7, values=["", "0", "", "", ""]).move_to([x, 2.2, 0])


def phys_strip():
    return MemoryStrip(n=16, cell_width=0.7, cell_height=0.6, addresses=[f"0x{4 * i:02X}" for i in range(16)],
                       font_size=20, address_size=12).move_to([0, PHYS_Y, 0])


def s12_end_world():
    """Exact S12 end state (for S13's start): dict of mobjects."""
    tag = next_tag("./mem & ./mem &", 22, TEXT)
    tag[1].become(Text("./mem & ./mem &", font=MONO_FONT, font_size=22, color=TEXT).move_to(tag[1]))
    tag.move_to([0, 3.25, 0])
    left, right = top_strip(-2.75), top_strip(2.75)
    p1 = pid_process(24113, PID1_COLOR)
    p2 = pid_process(24114, PID2_COLOR)
    place_on(p1, [-5.85, 1.85, 0])
    place_on(p2, [5.85, 1.85, 0])
    p2.flip()
    cards = VGroup()
    for p, s, col in ((p1, left, PID1_COLOR), (p2, right, PID2_COLOR)):
        c = Text("p = 0x200000", font=MONO_FONT, font_size=16, color=col)
        box = SurroundingRectangle(c, buff=0.08, corner_radius=0.05).set_fill(CARD_FILL, 1).set_stroke(col, 2)
        card = VGroup(box, c).next_to(p, DOWN, buff=0.12)
        if card.get_left()[0] < -6.6:
            card.shift(RIGHT * (-6.6 - card.get_left()[0]))
        if card.get_right()[0] > 6.6:
            card.shift(LEFT * (card.get_right()[0] - 6.6))
        cards.add(card)
    left.color_cell(1, PID1_COLOR)
    right.color_cell(1, PID2_COLOR)
    left.cell(1).set_fill(PID1_COLOR, 0.55).set_stroke(PID1_COLOR)
    right.cell(1).set_fill(PID2_COLOR, 0.55).set_stroke(PID2_COLOR)
    left.set_value(1, "5")
    right.set_value(1, "5")
    log_box = RoundedRectangle(width=2.0, height=0.95, corner_radius=0.08).set_fill(TERM_FILL, 1).set_stroke(DIM, 1.5)
    log_box.move_to([0, 1.15, 0])
    la = Text("(24113) p: 3", font=MONO_FONT, font_size=15, color=PID1_COLOR).move_to(log_box.get_center() + UP * 0.2)
    lb = Text("(24114) p: 3", font=MONO_FONT, font_size=15, color=PID2_COLOR).move_to(log_box.get_center() + DOWN * 0.2)
    split = IllusionSplit("what each process sees", "what really happens", orientation="horizontal",
                          at=DIV_Y, top_y=3.15, title_size=22)
    split.left_title.move_to([-6.6, 3.22, 0], aligned_edge=LEFT)
    split.right_title.move_to([-6.6, DIV_Y - 0.3, 0], aligned_edge=LEFT)
    phys = phys_strip()
    phys_lab = Text("physical memory", font_size=22, color=MEM_COLOR).move_to([4.6, DIV_Y - 0.3, 0])
    outlines = VGroup(*[DashedVMobject(SurroundingRectangle(s.cells, buff=0.1, corner_radius=0.08), num_dashes=40)
                        .set_stroke(col, 3) for s, col in ((left, PID1_COLOR), (right, PID2_COLOR))])
    vas = VGroup(*[Text("virtual address space", font_size=18, color=col).next_to(o, UP, buff=0.05)
                   for o, col in zip(outlines, (PID1_COLOR, PID2_COLOR))])
    arrows = MappingArrows([(left.cell(1), phys.cell(PHYS_IDX[0]), PID1_COLOR),
                            (right.cell(1), phys.cell(PHYS_IDX[1]), PID2_COLOR)], angle=0.3)
    phys.cell(PHYS_IDX[0]).set_fill(PID1_COLOR, 0.55).set_stroke(PID1_COLOR)
    phys.cell(PHYS_IDX[1]).set_fill(PID2_COLOR, 0.55).set_stroke(PID2_COLOR)
    phys.set_value(PHYS_IDX[0], "5")
    phys.set_value(PHYS_IDX[1], "5")
    return dict(all=VGroup(tag, left, right, p1, p2, cards, log_box, la, lb, split, phys, phys_lab, outlines,
                           vas, arrows),
                left=left, right=right, phys=phys, split=split)


class S12SameAddress(NarratedScene):
    def construct(self):
        stu, prof = make_hosts("corner", stu_expr="neutral", prof_expr="happy")
        th = terms(VIRT)
        bdg = badge(VIRT)
        strip = s11_strip()
        strip.cell(1).set_fill(PID1_COLOR, 0.55).set_stroke(PID1_COLOR)
        strip.values.submobjects[1] = strip._val("4", strip.cell(1))
        p_lab = Text("p", font=MONO_FONT, font_size=24, color=PID1_COLOR, weight=BOLD).next_to(strip.cell(1), UP, buff=0.1)
        code, title = s11_code()
        term = s11_terminal()
        term.type("./mem")
        for line in ["(2134) address pointed to by p: 0x200000"] + [f"(2134) p: {v}" for v in range(1, 5)]:
            term.print(line)
        pid = pid_process(2134, PID1_COLOR)
        place_on(pid, S11_PID_POS)
        self.add(stu, prof, bdg, strip, p_lab, code, title, term, pid, set_docked(th, "process identifier (PID)"))

        # S12.1
        tag = next_tag("./mem & ./mem &", 22, TEXT)
        tag[1].become(Text("./mem & ./mem &", font=MONO_FONT, font_size=22, color=TEXT).move_to(tag[1]))
        tag.move_to([0, 3.25, 0])
        left, right = top_strip(-2.75), top_strip(2.75)
        p1 = pid_process(24113, PID1_COLOR)
        p2 = pid_process(24114, PID2_COLOR)
        place_on(p1, [-5.85, 1.85, 0])
        place_on(p2, [5.85, 1.85, 0])
        p2.flip()
        with self.narrate("Now run two copies at once."):
            self.play(ReplacementTransform(VGroup(code, title, term), tag), FadeOut(p_lab),
                      ReplacementTransform(strip, VGroup(left, right)), run_time=1.2)
            self.play(ReplacementTransform(pid, p1), FadeIn(p2, shift=LEFT * 0.4), run_time=0.8)

        # S12.2 same address
        cards = VGroup()
        for p, s, col in ((p1, left, PID1_COLOR), (p2, right, PID2_COLOR)):
            c = Text("p = 0x200000", font=MONO_FONT, font_size=16, color=col)
            box = SurroundingRectangle(c, buff=0.08, corner_radius=0.05).set_fill(CARD_FILL, 1).set_stroke(col, 2)
            card = VGroup(box, c).next_to(p, DOWN, buff=0.12)
            if card.get_left()[0] < -6.6:
                card.shift(RIGHT * (-6.6 - card.get_left()[0]))
            if card.get_right()[0] > 6.6:
                card.shift(LEFT * (card.get_right()[0] - 6.6))
            cards.add(card)
        with self.narrate("Look at the addresses. Both say 0x200000. The same address!"):
            self.play(left.color_cell(1, PID1_COLOR), right.color_cell(1, PID2_COLOR),
                      FadeIn(cards, shift=UP * 0.1), run_time=0.7)
            self.wait(1.0)
            self.play(*[Indicate(c, color=CPU_COLOR) for c in cards], run_time=0.8)
            self.wait(0.6)

        # S12.3 alternate counting with a log
        log = VGroup()
        log_box = RoundedRectangle(width=2.0, height=0.95, corner_radius=0.08).set_fill(TERM_FILL, 1).set_stroke(DIM, 1.5)
        log_box.move_to([0, 1.15, 0])

        def log_line(text, col):
            return Text(text, font=MONO_FONT, font_size=15, color=col)

        with self.narrate("And yet each one counts up on its own: 1, 1, 2, 2, 3, 3."):
            self.play(FadeIn(log_box), run_time=0.3)
            for v in (1, 2, 3):
                for p_, s_, col, pidn in ((p1, left, PID1_COLOR, 24113), (p2, right, PID2_COLOR, 24114)):
                    ln = log_line(f"({pidn}) p: {v}", col)
                    anims = [s_.set_value(1, str(v))]
                    if len(log) == 2:
                        old = log[0]
                        log.remove(old)
                        anims += [FadeOut(old), log[0].animate.move_to(log_box.get_center() + UP * 0.2)]
                    ln.move_to(log_box.get_center() + (UP * 0.2 if len(log) == 0 else DOWN * 0.2))
                    log.add(ln)
                    anims.append(FadeIn(ln))
                    self.play(*anims, run_time=0.45)

        # S12.4
        self.say("They never interfere.", min_time=1.6)
        # S12.5
        self.say("How can two programs use the same address without overwriting each other?",
                 stu.change("confused"))

        # S12.6 divider + physical strip
        split = IllusionSplit("what each process sees", "what really happens", orientation="horizontal",
                              at=DIV_Y, top_y=3.15, title_size=22)
        split.left_title.move_to([-6.6, 3.22, 0], aligned_edge=LEFT)
        split.right_title.move_to([-6.6, DIV_Y - 0.3, 0], aligned_edge=LEFT)
        phys = phys_strip()
        phys_lab = Text("physical memory", font_size=22, color=MEM_COLOR).move_to([4.6, DIV_Y - 0.3, 0])
        self.say("Because \"the same address\" isn't the same place.",
                 prof.change("proud"), split.draw(), Succession(Wait(0.6), FadeIn(phys), FadeIn(phys_lab)))

        # S12.7 virtual address spaces
        outlines = VGroup(*[DashedVMobject(SurroundingRectangle(s.cells, buff=0.1, corner_radius=0.08), num_dashes=40)
                            .set_stroke(col, 3) for s, col in ((left, PID1_COLOR), (right, PID2_COLOR))])
        vas = VGroup(*[Text("virtual address space", font_size=18, color=col).next_to(o, UP, buff=0.05)
                       for o, col in zip(outlines, (PID1_COLOR, PID2_COLOR))])
        self.say("Each process gets its own private virtual address space,",
                 Create(outlines, run_time=1.0), FadeIn(vas),
                 late(0.6, th.note("virtual address space")))

        # S12.8 mapping arrows
        arrows = MappingArrows([(left.cell(1), phys.cell(PHYS_IDX[0]), PID1_COLOR),
                                (right.cell(1), phys.cell(PHYS_IDX[1]), PID2_COLOR)], angle=0.3)
        with self.narrate("and the OS maps it onto the real, physical memory."):
            self.play(arrows.create(), run_time=1.2)
            self.play(phys.color_cell(PHYS_IDX[0], PID1_COLOR), phys.color_cell(PHYS_IDX[1], PID2_COLOR),
                      phys.set_value(PHYS_IDX[0], "3"), phys.set_value(PHYS_IDX[1], "3"), run_time=0.6)
            for v in (4, 5):
                self.play(left.set_value(1, str(v)), phys.set_value(PHYS_IDX[0], str(v)), run_time=0.4)
                self.play(right.set_value(1, str(v)), phys.set_value(PHYS_IDX[1], str(v)), run_time=0.4)

        # S12.9
        self.say("Same address on the outside, different bytes underneath. That's virtualizing memory.",
                 arrows.pulse(), late(0.8, th.note("virtualizing memory")))

        self.beat(0.5)
