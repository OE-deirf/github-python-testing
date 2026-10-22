class CollatzSequence:
    def __init__(self, start: int):
        "Simple init"
        if start < 1:
            raise ValueError("Needs positive int!")
        self.start: int = start
        self.values: list[int] = self._generate()

    def _generate(self) -> list[int]:
        "Generate values"
        n: int = self.start
        values: list[int] = [self.start]
        while n != 1:
            n = n // 2 if n % 2 == 0 else 3 * n + 1
            values.append(n)
        return values

    @property
    def steps(self) -> int:
        "Calculate step length"
        return len(self.values) - 1

    @property
    def peak(self) -> int:
        "Calculate peak value"
        return max(self.values)
