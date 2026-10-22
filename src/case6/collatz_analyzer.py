from typing import Protocol


def next_value(n: int) -> int:
    return n // 2 if n % 2 == 0 else 3 * n + 1


class Repository(Protocol):
    def get(self, n: int) -> int | None: ...
    def save(self, n: int, steps: int) -> None: ...


class Notifier(Protocol):
    def alert(self, n: int, steps: int) -> None: ...


class CollatzAnalyzer:
    def __init__(self, repo: Repository, notifier: Notifier, threshold: int = 100):
        self.repo: Repository = repo
        self.notifier: Notifier = notifier
        self.threshold: int = threshold

    def steps(self, n: int) -> int:
        if n < 1:
            raise ValueError("n < 1")
        cached: int | None = self.repo.get(n)
        if cached is not None:
            return cached
        count: int = 0
        x: int = n
        while x != 1:
            x: int = next_value(x)
            count += 1
        self.repo.save(n, count)
        if count > self.threshold:
            self.notifier.alert(n, count)
        return count
