from src.case1.collatz_sequence import CollatzSequence


class CollatzAnalyzer:
    "input: lower: int, upper:int limit"
    def __init__(self, lower: int, upper: int):
        self.sequences: list[CollatzSequence] = [CollatzSequence(n) for n in range(lower, upper + 1)]

    def longest(self) -> CollatzSequence:
        "check the longest run"
        return max(self.sequences, key=lambda s: s.steps)

    def highest_peak(self) -> CollatzSequence:
        "check the highest peak run"
        return max(self.sequences, key=lambda s: s.peak)
