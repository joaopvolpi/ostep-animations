"""Series palette and style constants for the OSTEP video series."""
from manim import YELLOW, BLUE, GREEN, RED_C, BLUE_C, Text, MarkupText, Paragraph

# --- Typography ---------------------------------------------------------------
# Computer Modern (CMU Serif), the TeX font family used by 3Blue1Brown.
# Installed per-user from MiKTeX's cm-unicode package. Text, MarkupText and
# Paragraph default to it as soon as ostep_lib is imported.
FONT = "CMU Serif"
MONO_FONT = "CMU Typewriter Text"   # code blocks, terminals, addresses

for _cls in (Text, MarkupText, Paragraph):
    _cls.set_default(font=FONT)

# --- Background / text -----------------------------------------------------
BG = "#1C1C1C"
TEXT = "#ECECEC"
DIM = "#8A8A8A"

# --- Section accents (from the OSTEP website) ------------------------------
VIRT = "#F88017"   # virtualization (orange)
CONC = "#00AACC"   # concurrency (cyan)
PERS = "#4CC417"   # persistence (green)
SEC = "#3EA99F"    # security (teal)
INTRO = "#E8E2D0"  # intro / overview episodes (warm off-white)

# --- Concept colors ---------------------------------------------------------
CPU_COLOR = YELLOW
MEM_COLOR = BLUE
DISK_COLOR = GREEN
KERNEL_COLOR = RED_C
USER_COLOR = BLUE_C

# --- Character colors -------------------------------------------------------
PROFESSOR_COLOR = "#A48BD6"   # soft lavender
STUDENT_COLOR = "#F4A3B5"     # warm rose
COMPUTER_COLOR = "#D9CCAE"    # retro beige casing

# Distinct colors for process creatures (cycled by Process when no color given)
PROCESS_COLORS = [
    "#F4845F",  # coral
    "#5FC6A8",  # mint
    "#F2CC5B",  # gold
    "#6FA8F7",  # sky
    "#C792EA",  # lilac
    "#F7A1C4",  # pink
]


def apply_style(scene):
    """Apply the series look to a scene (currently: the background color)."""
    scene.camera.background_color = BG
    return scene


__all__ = [
    "FONT", "MONO_FONT",
    "BG", "TEXT", "DIM", "VIRT", "CONC", "PERS", "SEC", "INTRO",
    "CPU_COLOR", "MEM_COLOR", "DISK_COLOR", "KERNEL_COLOR", "USER_COLOR",
    "PROFESSOR_COLOR", "STUDENT_COLOR", "COMPUTER_COLOR", "PROCESS_COLORS",
    "apply_style",
]
