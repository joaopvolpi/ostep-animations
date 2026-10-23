import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common_more import *  # noqa: E402,F401,F403


class S07Snooping(Ep10Scene):
    def construct(self):
        self.world(strip=1, term="cache coherence", stu="surprised", prof="worried")
        stu, prof = self.stu, self.prof
        w = build_s06_end()
        c1, c2, mem, bus, bus_lab, a, neq, stale, stale_t = (
            w[k] for k in ("c1", "c2", "mem", "bus", "bus_lab", "a", "neq", "stale", "stale_t"))
        comp = Computer("error").scale(0.6).move_to(P3(3.7, -2.4))
        self.add(c1, c2, mem, bus, bus_lab, a, neq, stale, stale_t, comp)

        # S07.1  rewind
        self.say("The fix is the hardware's job. And the basic idea is delightfully nosy.",
                 FadeOut(neq), FadeOut(stale), FadeOut(stale_t), FadeOut(comp),
                 c2.clear(), hop_to(a, c1.slot_point(), run_time=1.0, height=1.0),
                 prof.change("neutral"), stu.change("neutral"))

        # S07.2
        e1 = EyeIcon(0.5, opened=False).move_to(c1.strip.get_right() + RIGHT * 0.35)
        e2 = EyeIcon(0.5, opened=False).move_to(c2.strip.get_right() + RIGHT * 0.35)
        look1, look2 = P3(c1.strip.get_center()[0], BUS_Y), P3(c2.strip.get_center()[0], BUS_Y)
        self.add(e1, e2)
        self.say("Every cache watches the bus, the wire connecting everything to memory. This is bus snooping.",
                 self.note("bus snooping"), e1.open_lids(), e2.open_lids())
        self.play(e1.look_at(look1), e2.look_at(look2), run_time=0.5)

        # S07.3
        self.play(c2.store("7", COL["A"], run_time=0.4), run_time=0.4)
        pulse = bus_pulse(bus, c1.cache_bottom(), c2.cache_bottom(), color=COL["A"], run_time=2.0)
        self.say("When a cache sees an update for data it holds, it reacts in one of two ways.",
                 pulse, Succession(Wait(0.6), e2.look_at(P3(0, BUS_Y))),
                 Indicate(c1.cells[0], color=TEXT, scale_factor=1.3))

        # S07.4
        lab = label("invalidate", 24, KERNEL_COLOR).move_to(P3(2.8, -1.45))
        self.say("It can invalidate: throw its own copy away, so the next read has to fetch the fresh value.",
                 self.note("invalidate"), c2.invalidate(0, run_time=1.2), FadeIn(lab, shift=UP * 0.1))

        # S07.5
        lab2 = label("update", 24, GREEN_OK).move_to(lab)
        pulse2 = bus_pulse(bus, c1.cache_bottom(), c2.cache_bottom(), color=COL["A"], run_time=1.6)
        with self.narrate("Or it can update: put the new value into its own cache too."):
            self.play(c2.store("7", COL["A"], cell=0, run_time=0.3), Transform(lab, lab2), run_time=0.5)
            self.play(pulse2, self.note("update"))
            self.play(c2.set_value(0, "9", color=COL["A"]), run_time=0.5)

        # S07.6
        okt = tick_mark(0.6).move_to(P3(0, 1.3))
        lazy = DashedVMobject(bus.path(c1.cache_bottom(), mem.get_top()).set_stroke(DIM, 2), num_dashes=24)
        self.say("Either way, the one shared memory stays one shared memory.",
                 FadeIn(okt, scale=0.5), Create(lazy), mem.set_content(0, "9"), FadeOut(lab))

        # S07.7
        card = aside_card("write-back caches: trickier", title="ASIDE", width=3.8, font_size=22).move_to(P3(4.6, 2.0))
        self.say("Write-back caches, like our example, make this trickier, because the write to memory isn't "
                 "visible until later. But you can imagine how the basic scheme works.",
                 Succession(card.slide_in(RIGHT), Wait(1.5), card.slide_out(RIGHT)), FadeOut(lazy))

        # S07.8
        self.say("So the hardware makes sure the program sees the right value, no matter which CPU it's on. "
                 "Then we're done!",
                 stu.change("excited"), okt.animate.scale(1.5))

        # S07.9
        hand = hand_up_icon(0.7).move_to(P3(0, 2.0))
        shade = scrim(0.25)
        self.say("Hold that thought.",
                 prof.change("happy"), FadeIn(hand, shift=DOWN * 0.3), FadeIn(shade))
        self.beat(0.3)
