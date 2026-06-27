from typing import Any

class MacroDefined_t(Any):
    """
    Type indicating a value defined by a macro.

    examples:

    `PI: int = MacroDefined`

    `SQRT: Callable[[int], int] = MacroDefined`
    """
    pass

MacroDefined: MacroDefined_t = MacroDefined_t()