from pymacros.ensure_pm import PYMACROS
##include pymacros.ensure_pm

##ifndef PYMACROS
# Extra code to handle pure python, exit here for demo.
assert PYMACROS, "Compile this file with pymacros!"
##endif

# Basic includes with ##include and ##import
##include pymacros.builtin
##import demo_utils


##ifdef 0
# Type hints for editors and static analysis.

from pymacros.types import *
from collections.abc import Callable

PI: float = MacroDefined
SQR: Callable[[int], int] = MacroDefined
ADD: Callable[[int, int], int] = MacroDefined
uint8: Callable[[int], int] = MacroDefined

log: Callable[..., None] = MacroDefined
DEBUG_MODE: bool = MacroDefined
string: str = MacroDefined
##endif


# Macro definitions
##define PI 3.14159
##define SQR(x) ((x) * (x))
##define ADD(a, b) ((a) + (b))
##define uint8(x) ((x) % 256)
##define log print
##define DEBUG_MODE True
##define string "Hello World"

# Demo code
##ifdef DEBUG_MODE
log(string)
##endif

log(f"PI = {PI}")
log(f"SQR(4) = {SQR(4)}")
log(f"ADD(1 + 2, SQR(3)) = {ADD(1 + 2, SQR(3))}")

value = uint8(523 * 212)
log(f"uint8(523 * 212) = {value}")