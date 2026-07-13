from typing import Any
class MacroDefined_t(Any):
    """
    Type indicating a value defined by a macro.

    examples:

    `PI: int = MacroDefined`

    `SQRT: Callable[[int], int] = MacroDefined`
    """

class Uint_t(int):
    """
    Type for unsigned integers of size
    """

class Uint8_t(Uint_t):
    """
    Type for unsigned char
    """
    @staticmethod
    def convert(num): return num % (1 << 8)

class Uint16_t(Uint_t):
    """
    Type for unsigned word
    """
    @staticmethod
    def convert(num): return num % (1 << 16)

MacroDefined: MacroDefined_t = MacroDefined_t()
