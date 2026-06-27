from collections.abc import Callable
from pymacros import *

##define PI 3.14159
##define SQR(x) ((x)*(x))
##define ADD(a,b) ((a)+(b))
##define log print
##define DEBUG_MODE True
##define STRING "Hello World"

PI: int = MacroDefined
SQR: Callable[[int], int] = MacroDefined
ADD: Callable[[int, int], int] = MacroDefined
log: Callable[[int], int] = MacroDefined
DEBUG_MODE: bool = MacroDefined
string: str = MacroDefined


if DEBUG_MODE:
    log(string)
log(PI)
log(SQR(4))
log(ADD(1+2, SQR(3)))