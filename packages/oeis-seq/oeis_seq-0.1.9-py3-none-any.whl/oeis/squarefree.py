from itertools import count
from typing import Iterable

from oeis.registry import registry
from oeis.utils import prime_factors


@registry.register("A005117")
def squarefree() -> Iterable[int]:
    """
    Square-free numbers.

        Square-free numbers are integers that are divisible by no square number other
        than 1.
    """
    for n in count(start=1):  # pragma: no branch
        if len(prime_factors(n)) == len(set(prime_factors(n))):
            yield n
