# Shared assets for episodes 05–11

The scene files for 05–11 were written in parallel, so several of them ask for the same new
asset, sometimes under different names. Build each asset **once**, in `ostep_lib/props/`, under
the canonical name below. Then every episode uses it. Existing props are not repeated here (see
`ostep_lib/README.md`).

## Extensions to existing props

| Canonical | Requested by | Spec (merged) |
|---|---|---|
| **`Timeline` extensions** | 06 (OS row), 07 (colored CPU lane, disk lane, arrival/completion markers, turnaround/response brackets), 08 (ms tick labels, sub-tick "sliver" blocks for 1 ms bursts), 10 (`ScheduleGrid`: CPU × time-slice table colored by job) | Add to `p04_timeline.Timeline`, without breaking its API. Row kinds: `"process"` (default), `"cpu"` (cells take the running job's color), `"disk"`, `"os"` (`KERNEL_COLOR`). Add `arrival_marker(row, t)`, `completion_marker(row, t)`, `bracket(row, t0, t1, style="solid"\|"dashed")`, fractional ticks for slivers, and a `unit` label ("s"/"ms"). `ScheduleGrid` = a `Timeline` whose rows are CPUs and whose cells are colored by job letter. |
| **`clone_process`** | 04 (S22 teaser), 05 | A helper animation: a Process squashes and splits into two identical copies (mitosis), with an optional label change on the copy. |
| **`padlock` open/close** | 07 (five assumptions as padlocks), 06/10/11 (locks, icons) | Extend `ov_icons.padlock` with `.open()` / `.close()` animations (the shackle rotates). One padlock design for the whole series. |
| **`Bus.pulse`** | 10 | A signal dot traveling along `Bus.path`, used for snooping. |
| **`MenuCard` custom rows** | 05 (S16 callback to 04's menu) | Let `MenuCard` take row labels and right-aligned tags (e.g. "create → fork()"). |
| **`IllusionSplit` with Memory** | 11 (teaser) | No change needed: use `IllusionSplit` + `Memory`. |

## New props (one owner each)

| Canonical | Requested by | Notes |
|---|---|---|
| **`RaffleDrum`, `Ticket`, `TicketStack`** | 09 (main), 08 (teaser: "hat and ticket") | 08's teaser now uses the drum. Tickets are colored by process. |
| **`Seesaw`** | 09 (icon), 11 (turnaround vs response) | A beam on a pivot with a `tilt(angle)` animation and two pans for labels. |
| **`EyeIcon`** | 10 (`eye_icon`), 11 (paranoid-OS eye) | An eye with a pupil `look_at`. |
| **`MLFQLadder`** | 08 (main), 11 (mini "MLFQ stack"), 07 and 10 (tiny staircase hints) | Stacked lane `Queue`s with promote / demote / boost-all / collapse. The 07/10 hints can be `MLFQLadder(levels=3)` scaled down instead of ad-hoc bars. |
| **`RuleBoard`** | 08 | An accumulating rule panel (add, glow, merge 4a+4b → 4). It may be useful for other "rules" later. |
| **`AllotmentGauge`** | 08 | A drain/reset bar. Proposed as the recurring "allotment" icon. |
| **`CacheCPU`** | 10 | A `CPU` with a cache strip: `store`, `invalidate`, `set_value`, `warmth`, `cache_point`. Reused in the memory section (TLBs, 19). |
| **`ProtocolChart`** | 06 (Figures 6.1, 6.2; 2–3 columns) | A column-listing figure with a highlight row; reusable for later protocol figures. |
| **`KernelToken`**, `cpu_ride`, `RegPacket`, `KernelStack`, `TrapTable` | 06 | `KernelToken` is the red "OS" badge on the chip (proposed for the bible). `KernelStack` reuses the `Memory` look. |
| **`AlarmClock`** | 06 (timer interrupt) | Reuse it wherever timer interrupts appear (07 time slices, 08 allotment). |
| **`ProcessWorld`**, `CodeWalker`, `FdTable`, `ShellLoop`, `KernelPipe` | 05 | `CodeWalker` = `Code` + several colored highlight bars, and it is likely reused widely (06 `swtch`, 09 lottery code). Build it generically. |
| **`JobList`**, `NumberStrip`, `PassTable`, `VruntimeMeter`, `RBTree`, `FairnessPlot`, `TargetPie` | 09 | `RBTree` is generic (a tree with red/black nodes). |
| **`MetricReadout`** | 07 | A `MathTex` average builder with strike-out; reused in 08/09 for numbers. |
| **`CrystalBall`** | 07 (no-oracle) | `.crack()`. |
| Small icons | 05 (bolt, keycap, shield, crown "root" tag, glass pane), 06 (cabinet lock, socket cover, fence, magnifier, doorway, permission booth, bench), 07 (cart, checkout), 08 (dial (reuse `dial_icon`), slider panel, voodoo glyph, gamer sunglasses, mini pie, medal), 09 (cloud/VM window, coin/die, handshake, paper chip, bad-luck cloud), 10 (suitcase, pin), 11 (flame, puzzle piece, censor bar, neck bolts) | Put shared ones in a new `ostep_lib/props/icons_05_11.py`. The **gamer sunglasses** must be one glyph (08 and 11 both use it on Process B). |

## Cross-episode continuity decisions (from the consistency pass)
- **Colors:** A coral, B mint, C gold, D sky in every episode. In 07/08/11, A is the long job and
  B the short or interactive one. **B (mint) is the scheduler-gamer** in both 08 and 11.
- **08 → 09 handoff:** the teaser shows the `RaffleDrum` with 3 coral + 1 mint tickets (75/25), the
  split 09 opens with.
- **05 → 06 handoff:** 06's cold open picks up 05's teaser question ("how does the OS get control
  back?"), and 06 B03 names `exec()`.
- **End cards:** each episode's "Next:" card matches the following episode (checked 04 → 12).
