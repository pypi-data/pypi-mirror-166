from itertools import count
from math import floor, isqrt
from typing import Iterable

from oeis.registry import registry


def k1(n: int) -> int:
    """Determine a(k+1) in the sequence."""
    return floor(isqrt(n)) if n % 2 == 0 else floor(n ** (3 / 2))


@registry.register("A094683")
def juggler() -> Iterable[int]:
    """Jugglers sequence."""
    yield 0
    for n in count(start=1):  # pragma: no branch
        yield k1(n)
