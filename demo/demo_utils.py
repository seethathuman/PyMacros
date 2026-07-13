##ifndef PM_IMPLEMENTATION
##define PM_IMPLEMENTATION 1

# Utility functions for demo

##ifdef 0
from collections.abc import Callable
from pymacros.types import *
to_int: Callable[[int, int], int]
##endif

##define to_int(uint, size) int.from_bytes(uint.to_bytes(size), signed=1)

##endif