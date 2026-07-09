from collections.abc import Callable
from pymacros import *

assert (
    ##include ensure_pm.py
)

##define PI 3.14159
##define SQR(x) ((x)*(x))
##define ADD(a,b) ((a)+(b))
##define uint8(num) num % 256
##define log print
##define DEBUG_MODE True
##define string "Hello World"

##ifdef 0
PI: int = MacroDefined
SQR: Callable[[int], int] = MacroDefined
ADD: Callable[[int, int], int] = MacroDefined
log: Callable[[int], int] = MacroDefined
DEBUG_MODE: bool = MacroDefined
string: str = MacroDefined
uint8: Callable[[int], int] = MacroDefined
##endif

##ifdef DEBUG_MODE
log(string)
##endif

log(PI)
log(SQR(4))
log(ADD(1+2, SQR(3)))

a = uint8(523 * 212)
log(a)