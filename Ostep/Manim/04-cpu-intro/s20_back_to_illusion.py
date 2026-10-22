import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *  # noqa: E402,F401,F403

# tick -> (runner, process that blocks at the END of this tick or None, process whose I/O completes at the end)
SCHEDULE = [("A", None, None), ("B", None, None), ("C", None, "D"), ("D", None, None), ("A", "A", None),
            ("B", None, None), ("C", None, "A"), ("D", None, None), ("A", None, None), ("B", None, None)]


class S20BackToIllusion(Ep04Scene):
    def construct(self):
        self.add_badge()
        w = build_s20_world()
        laptop, counter, cpu, q, disk, ps, cards, list_lab, brace, tl = (w[k] for k in (
            "laptop", "counter", "cpu", "q", "disk", "ps", "cards", "list_lab", "brace", "tl"))

        # S20.1
        self.say("Let's go back to that laptop with a hundred programs and one CPU.",
                 Create(laptop, run_time=1.5), FadeIn(counter, run_time=1.0))

        # S20.2
        self.say("Now we can see the trick.",
                 laptop.lid.animate(run_time=0.8).set_fill(TEXT, 0.1),
                 laptop.screen.animate(run_time=0.8).set_fill(BG, 0.0), FadeIn(cpu), FadeIn(q), FadeIn(disk))

        # S20.3
        with self.narrate("Each program is a process: memory, registers, open files, written down in a PCB."):
            self.play(LaggedStart(*[GrowFromCenter(ps[n]) for n in "ABCD"], lag_ratio=0.2), run_time=1.0)
            self.play(LaggedStart(*[GrowFromPoint(cards[n], ps[n].get_center()) for n in "ABCD"], lag_ratio=0.25),
                      run_time=1.6)

        # S20.4
        self.say("The OS keeps them all on a list.", GrowFromCenter(brace, run_time=0.6), FadeIn(list_lab, run_time=0.6))

        # S20.5
        state = dict(w["states"])
        queue = ["B", "C"]
        runner = "A"
        blocked = {"D"}

        def spots():
            pts = {runner: cpu.slot_point() + UP * 0.02} if runner else {}
            for i, n in enumerate(queue):
                pts[n] = q.slot_point(i)
            for n in blocked:
                pts[n] = S20_BLOCK_SPOT
            return pts

        with self.narrate("It hands the CPU to one, then another, quickly, sliding each between running, ready "
                          "and blocked."):
            self.play(FadeIn(tl), run_time=0.4)
            for k, (run, blocks, wakes) in enumerate(SCHEDULE, start=1):
                prev = runner
                if run in queue:
                    queue.remove(run)
                if prev and prev != run:
                    queue.append(prev)
                runner = run
                new_state = {n: ("running" if n == runner else "blocked" if n in blocked else "ready") for n in "ABCD"}
                anims = []
                for n, pt in spots().items():
                    if np.linalg.norm(ps[n].get_bottom() - pt) > 1e-3 or new_state[n] != state[n]:
                        ps[n].set_expression(new_state[n])
                        anims.append(hop_bottom(ps[n], pt, run_time=0.35))
                for n in "ABCD":
                    if new_state[n] != state[n]:
                        anims.append(cards[n].set_field("state", new_state[n], run_time=0.35))
                state = new_state
                if anims:
                    self.play(*anims, run_time=0.35)
                else:
                    self.wait(0.35)
                self.play(tl.fill_column(k, {n: state[n] for n in "ABCD"}, run_time=0.25))
                # end-of-tick events
                if blocks:
                    runner = None
                    queue_ = queue
                    blocked.add(blocks)
                    state_b = dict(state)
                    state_b[blocks] = "blocked"
                    ps[blocks].set_expression("blocked")
                    self.play(hop_bottom(ps[blocks], S20_BLOCK_SPOT, run_time=0.3),
                              cards[blocks].set_field("state", "blocked", run_time=0.3))
                    state = state_b
                if wakes:
                    blocked.discard(wakes)
                    queue.append(wakes)
                    ps[wakes].set_expression("ready")
                    state[wakes] = "ready"
                    self.play(hop_bottom(ps[wakes], q.slot_point(len(queue) - 1), run_time=0.3),
                              cards[wakes].set_field("state", "ready", run_time=0.3))
                for n, pt in spots().items():      # keep everyone exactly on their spot
                    bottom_to(ps[n], pt)

        # S20.6
        gears = GearPair(radius=0.22).move_to(cpu.get_right() + RIGHT * 0.55 + UP * 0.1)
        spot = Spotlight(height=1.1, spread=0.32).move_beam_to(q.slot_point(0) + UP * 0.02)
        with self.narrate("A low-level mechanism does the switching. A policy decides who goes next."):
            self.play(FadeIn(gears, scale=0.5), run_time=0.5)
            self.play(gears.spin(PI, run_time=1.0))
            self.play(FadeIn(spot), run_time=0.6)
            self.play(spot.animate.move_beam_to(q.slot_point(1) + UP * 0.02), run_time=0.6)

        # S20.7
        vcpus = virtual_cpu_row(xs=np.linspace(-3.4, 2.2, 5), y=2.75, size=0.45)
        with self.narrate("Many virtual CPUs. One real one."):
            self.play(LaggedStart(*[FadeIn(v, shift=DOWN * 0.2) for v in vcpus], lag_ratio=0.12), run_time=1.0)
            self.play(*[Transform(v, cpu.copy().set_opacity(0.6)) for v in vcpus], run_time=1.2)
            self.remove(*vcpus)
            glow = Circle(radius=0.75).move_to(cpu).set_fill(CPU_COLOR, 0.18).set_stroke(CPU_COLOR, 3, opacity=0.6)
            glow.set_opacity(0)
            self.add(glow)
            self.bring_to_back(glow)
            glow.set_fill(CPU_COLOR, 0.18).set_stroke(CPU_COLOR, 3, opacity=0.6)
            glow.save_state()
            glow.scale(0.6).set_opacity(0)
            self.play(Flash(cpu, color=CPU_COLOR, line_length=0.3, flash_radius=0.7),
                      Restore(glow), run_time=0.6)
        self.beat(1.5)
