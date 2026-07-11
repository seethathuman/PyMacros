#[0] from ensure_pm import PYMACROS
#[1] ##include ensure_pm.py
#[0] PYMACROS: bool = False
PYMACROS:bool=False
#[1] ##define PYMACROS True
#[2] 
#[3] ##ifdef PYMACROS
#[4] ##include pymacros.py
#[0] ##ifndef PM_IMPLEMENTATION
#[1] ##define PM_IMPLEMENTATION 1
#[2] from typing import Any
from typing import Any
#[3] class MacroDefined_t(Any):
class MacroDefined_t(Any):
#[4] """
#[5] Type indicating a value defined by a macro.
#[6] #[7] examples:
#[8] #[9] `PI: int = MacroDefined`
#[10] #[11] `SQRT: Callable[[int], int] = MacroDefined`
#[12] """
    """
    Type indicating a value defined by a macro.

    examples:

    `PI: int = MacroDefined`

    `SQRT: Callable[[int], int] = MacroDefined`
    """
#[13] def __init__(self, *args, **kwargs): pass
    def __init__(self,*args,**kwargs):pass
#[14] 
#[15] class Uint_t(int):
class Uint_t(int):
#[16] """
#[17] Type for unsigned integers of size
#[18] """
    """
    Type for unsigned integers of size
    """
#[19] 
#[20] class Uint8_t(Uint_t):
class Uint8_t(Uint_t):
#[21] """
#[22] Type for unsigned char
#[23] """
    """
    Type for unsigned char
    """
#[24] @staticmethod
    @staticmethod
#[25] def convert(num): return num % (1 << 8)
    def convert(num):return num%(1<<8)
#[26] 
#[27] class Uint16_t(Uint_t):
class Uint16_t(Uint_t):
#[28] """
#[29] Type for unsigned word
#[30] """
    """
    Type for unsigned word
    """
#[31] @staticmethod
    @staticmethod
#[32] def convert(num): return num % (1 << 16)
    def convert(num):return num%(1<<16)
#[33] 
#[34] MacroDefined: MacroDefined_t = MacroDefined_t()
MacroDefined:MacroDefined_t=MacroDefined_t()
#[35] ##endif
#[5] ##else
#[6] ##BREAKPOINT
#[7] from pymacros import *
#[8] ##endif
#[9] 
#[10] assert PYMACROS, "Compile this file with pymacros!"
assert True,"Compile this file with pymacros!"
#[11] 
#[12] ##ifdef 0
#[13] from collections.abc import Callable
#[14] PI: int = MacroDefined
#[15] SQR: Callable[[int], int] = MacroDefined
#[16] ADD: Callable[[int, int], int] = MacroDefined
#[17] log: Callable[[int], int] = MacroDefined
#[18] DEBUG_MODE: bool = MacroDefined
#[19] string: str = MacroDefined
#[20] uint8: Callable[[int], int] = MacroDefined
#[21] ##endif
#[22] 
#[23] ##define PI 3.14159
#[24] ##define SQR(x) ((x)*(x))
#[25] ##define ADD(a,b) ((a)+(b))
#[26] ##define uint8(num) num % 256
#[27] ##define log print
#[28] ##define DEBUG_MODE True
#[29] ##define string "Hello World"
#[30] 
#[31] ##ifdef DEBUG_MODE
#[32] log(string)
print("Hello World")
#[33] ##endif
#[34] 
#[35] log(PI)
print(3.14159)
#[36] log(SQR(4))
print(((4)*(4)))
#[37] log(ADD(1+2, SQR(3)))
print(((1+2)+(((3)*(3)))))
#[38] 
#[39] a = uint8(523 * 212)
a=523*212%256
#[40] log(a)
print(a)
