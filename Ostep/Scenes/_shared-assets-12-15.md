# Shared assets for episodes 12–15 (memory virtualization)

Same rules as `_shared-assets-05-11.md`: build each asset **once**, under the canonical name, in
its owner's `ostep_lib/props/pNN_*.py`. Later episodes import it.

## New props (one owner each)

| Canonical | Owner | Used by | Spec |
|---|---|---|---|
| **`address_space_16kb()`** ("AS16") | 13 (`p13_addrspace.py`) | 12 (same region order, no addresses), 13, 14, 15 | `Memory(regions=["code","heap",("free",6),"stack"], addresses=["0KB","1KB","2KB","15KB","16KB"])`, with a "not to scale" break mark on free, `.grow_heap(k)`, `.grow_stack(k)`, `.region_arrows()`, `.set_owner(color)`. Full spec: `13-vm-intro.md`, "New assets needed". |
| **`physical_512kb()`**, `memory_copy_fly()` | 13 | 13, 15 | Fig 13.2 physical column (OS / free / C / B / free / A / free); `.slice_of(name)`, `.land(copy, name)`; a translucent AS16 copy flies onto a slice. |
| **`MMU`**, `AddressChip`, `TranslationStage` | 15 (`p15_*.py`) | 15, later VM episodes (16+) | Base and bounds cells, comparator, adder; `translate(chip, va, base, bounds, ok)`. See `15-vm-mechanism.md`. |
| Heap helpers (`heap_block`, `free_block`, `pointer_arrow`, `ErrorChip`, break marker, `GarbageCollector`) | 14 (`p14_heap.py`) | 14, likely 17 (free space) | See `14-vm-api.md`. |

Already existing and reused: `EyeIcon` (p10), `Padlock` (p07), `KernelToken`, `TrapTable`,
`ProtocolChart` (p06), `RegisterBank`, `PCBCard` (p04), `CodeWalker` (p05), `Terminal`,
`MappingArrows` (ov), `IllusionSplit` (titles now at y = 2.25).

## Continuity decisions
- **Colors:** A coral, B mint, C gold (as in 05–11).
- **Unveiled terms:**
  - 12 has none (notes only).
  - 13: *address space*, *virtual address*, *virtualizing memory*.
  - 14: *heap*, *malloc()*, *buffer overflow*, *memory leak*.
  - 15: *address translation*, *dynamic relocation*, *MMU*, *internal fragmentation*.
- **Handoffs:**
  - 11 → 12: 11's teaser leads into 12.
  - 12 → 13: 12's teaser asks what a private memory looks like, and 13's B01 calls back to "every address is virtual".
  - 13 → 14: 13's teaser is the `malloc(?)` bubble.
  - 14 → 15: 14's S18 calls back to `va.c`, and 15's B01 picks up "every printed address is virtual".
  - 15 → 16: the teaser points to segmentation.
