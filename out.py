#[0] from collections.abc import Callable
from collections.abc import Callable
#[1] from pymacros import *
from pymacros import*
#[2] 
#[3] assert (
#[4] ##include ensure_pm.py
#[5] ), "Compile this file with pymacros!"
assert(
1),"Compile this file with pymacros!"
#[6] 
#[7] ###define ( [
###define ( [
#[8] ###define ) ]
###define ) ]
#[9] ##define PI 3.14159
#[10] ##define SQR(x) ((x)*(x))
#[11] ##define ADD(a,b) ((a)+(b))
#[12] ##define uint8(num) num % 256
#[13] ##define log print
#[14] ##define DEBUG_MODE True
#[15] ##define string "Hello World"
#[16] 
#[17] ##ifdef 0
#[18] PI: int = MacroDefined
#[19] SQR: Callable[[int], int] = MacroDefined
#[20] ADD: Callable[[int, int], int] = MacroDefined
#[21] log: Callable[[int], int] = MacroDefined
#[22] DEBUG_MODE: bool = MacroDefined
#[23] string: str = MacroDefined
#[24] uint8: Callable[[int], int] = MacroDefined
#[25] ##endif
#[26] 
#[27] ##ifdef DEBUG_MODE
#[28] log(string)
print("Hello World")
#[29] ##endif
#[30] 
#[31] log(PI)
print(3.14159)
#[32] log(SQR(4))
print(((4)*(4)))
#[33] log(ADD(1+2, SQR(3)))
print(((1+2)+(((3)*(3)))))
#[34] 
#[35] a = uint8(523 * 212)
a=523*212%256
#[36] log(a)
print(a)
