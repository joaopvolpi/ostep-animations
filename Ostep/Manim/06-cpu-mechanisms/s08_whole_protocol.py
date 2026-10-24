import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403

OS, HW, PR = 0, 1, 2


class S08WholeProtocol(Ep06Scene):
    def construct(self):
        self.add_badge()
        self.add_docked_term("protection")
        stu, prof = corner_chars(True, "neutral", "neutral")
        chart = ProtocolChart(["OS (kernel mode)", "Hardware", "Program (user mode)"],
                              colors=[KERNEL_COLOR, CPU_COLOR, USER_COLOR], col_x=[-4.4, 0.0, 4.4], col_width=4.2,
                              top=2.5, bottom=-1.95, row_h=0.4, font_size=20, header_size=24)
        thumb = LDEThumb().move_to(P3(3.6, -2.75))
        self.add(stu, prof, chart.rows_group, chart.cursor, chart.arrows)
        W_ = chart.write_row

        # S08.1
        self.say("Let's put it together. Limited direct execution has two phases.",
                 Succession(chart.draw(1.2), chart.section("OS @ boot (kernel mode)", VIRT)))
        self.play(FadeIn(thumb), run_time=0.5)

        # S08.2
        self.say("At boot, in kernel mode, the OS initializes the trap table, and the hardware remembers the "
                 "system-call handler.",
                 Succession(W_(OS, "initialize trap table", bold=True, run_time=1.2),
                            W_(HW, "remember address of syscall handler", run_time=1.2),
                            Indicate(thumb.kst, color=KERNEL_COLOR)))

        # S08.3
        self.say("Then, to run a process, the OS creates the entry, allocates memory, loads the program, sets up the stack.",
                 Succession(chart.section("OS @ run (kernel mode)", VIRT, run_time=0.8),
                            W_(OS, "Create entry for process list", run_time=0.9),
                            W_(OS, "Allocate memory for program", run_time=0.9),
                            W_(OS, "Load program into memory", run_time=0.9),
                            W_(OS, "Setup user stack with argv", run_time=0.9)))

        # S08.4
        self.say("It fills the kernel stack with the starting registers, and executes a return-from-trap.",
                 Succession(W_(OS, "Fill kernel stack with reg/PC", run_time=1.0),
                            AnimationGroup(W_(OS, "return-from-trap", bold=True, run_time=1.0), thumb.packet())))

        # S08.5
        q = Text("?", font_size=44, color=CPU_COLOR, weight=BOLD).move_to(chart.row_text(9).get_right() + RIGHT * 0.3)
        self.say("A return? From a trap that never happened?", stu.change("surprised"), FadeIn(q, scale=1.6))

        # S08.6
        tg = ep_tag("→ Ep. 06").move_to(P3(-6.2, 3.0))
        chk = tick_mark(0.3).move_to(chart.row_text(9).get_left() + LEFT * 0.4)
        self.say("A pretend return. That's the special mechanism I promised in episode four, the one that jumps "
                 "to main().", prof.change("proud"),
                 Succession(FadeOut(q), FadeIn(tg),
                            PacketFly(tg, chart.row_text(9).get_left() + LEFT * 0.9, arc=0.5, run_time=1.5),
                            ReplacementTransform(tg, chk), Wait(0.5), FadeOut(chk)))

        # S08.7
        self.say("The hardware restores the registers, moves to user mode, and jumps in.",
                 Succession(W_(HW, "restore regs (from kernel stack)", run_time=1.0), W_(HW, "move to user mode", run_time=0.8),
                            AnimationGroup(W_(HW, "jump to main", run_time=0.8), thumb.ride("user")),
                            W_(PR, "Run main()", run_time=0.8)))

        # S08.8
        self.say("The program runs. When it needs a service, it traps: registers saved, kernel mode, trap handler.",
                 Succession(W_(PR, "Call system call", run_time=0.8), W_(PR, "trap into OS", bold=True, run_time=0.8),
                            W_(HW, "save regs (to kernel stack)", run_time=0.8),
                            AnimationGroup(W_(HW, "move to kernel mode", run_time=0.8), thumb.ride("kernel")),
                            W_(HW, "jump to trap handler", run_time=0.8)))

        # S08.9
        self.say("The OS does the work, and returns from the trap.",
                 Succession(W_(OS, "Handle trap", run_time=0.8), W_(OS, "Do work of syscall", run_time=0.8),
                            W_(OS, "return-from-trap", bold=True, run_time=0.8)))

        # S08.10
        self.say("The registers come back, user mode returns, and the program continues right after the trap.",
                 Succession(W_(HW, "restore regs (from kernel stack)", run_time=0.9),
                            AnimationGroup(W_(HW, "move to user mode", run_time=0.9), thumb.ride("user")),
                            W_(HW, "jump to PC after trap", run_time=0.9), W_(PR, "...", run_time=0.6)))

        # S08.11
        self.say("Finally main() returns into exit(), one more system call, and the OS cleans up.",
                 Succession(W_(PR, "return from main", run_time=0.8), W_(PR, "trap (via exit())", bold=True, run_time=0.8),
                            W_(OS, "Free memory of process", run_time=0.8), W_(OS, "Remove from process list", run_time=0.8)))

        # S08.12
        bar = chart.sweep(PR)
        leg = chart_legend()
        self.say("The program ran directly on the CPU nearly the whole time.",
                 Succession(FadeIn(bar), Wait(1.5), FadeOut(bar),
                            AnimationGroup(ReplacementTransform(chart, leg), FadeOut(thumb), run_time=1.2)))
