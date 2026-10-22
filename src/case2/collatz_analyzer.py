from typing import Annotated
from pydantic import ConfigDict, Field, validate_call

from src.case2.collatz_sequence import CollatzSequence

PositiveInt = Annotated[int, Field(gt=0)]
STRICT = ConfigDict(strict=True)


class CollatzAnalyzer:
    "input: lower: int, upper:int limit"
    @validate_call(config=STRICT)
    def __init__(self, lower: PositiveInt, upper: Annotated[int, Field(gt=0, le=1_000_000)]):
        if lower > upper:
            raise ValueError("lower must lower than upper")
        self.lower: PositiveInt = lower
        self.upper: PositiveInt = upper
        self.sequences: list[CollatzSequence] = [CollatzSequence(n) for n in range(lower, upper + 1)]

    def longest(self) -> CollatzSequence:
        "check the longest run"
        return max(self.sequences, key=lambda s: s.steps)

    def highest_peak(self) -> CollatzSequence:
        "check the highest peak run"
        return max(self.sequences, key=lambda s: s.peak)
