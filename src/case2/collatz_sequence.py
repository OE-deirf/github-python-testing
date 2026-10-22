from typing import Annotated
from pydantic import ConfigDict, Field, validate_call

PositiveInt = Annotated[int, Field(gt=0)]
STRICT = ConfigDict(strict=True)


class CollatzSequence:
    @validate_call(config=STRICT)
    def __init__(self, start: PositiveInt):
        "Simple init"
        self.start: PositiveInt = start
        self.values: list[PositiveInt] = self._generate()

    def _generate(self) -> list[PositiveInt]:
        "Generate values"
        n = self.start
        values: list[PositiveInt] = [self.start]
        while n != 1:
            n: PositiveInt = n // 2 if n % 2 == 0 else 3 * n + 1
            values.append(n)
        return values

    @property
    def steps(self) -> PositiveInt:
        "Calculate step length"
        return len(self.values) - 1

    @property
    def peak(self) -> PositiveInt:
        "Calculate peak value"
        return max(self.values)
