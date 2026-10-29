import pytest

from typing import NoReturn, Any, Callable
from unittest.mock import Mock, create_autospec

import src.case6.collatz_analyzer as collatz
from src.case6.collatz_analyzer import CollatzAnalyzer, Notifier, Repository


# --------------------------------------------------------------------
# Slide 4: Dummy and Stub
# --------------------------------------------------------------------
class DummyNotifier:                      # fails loudly if ever touched
    def __getattr__(self, name: str) -> NoReturn:
        raise AssertionError(f"dummy used: {name}")


class StubRepo:                           # returns a canned answer
    def __init__(self, canned: int | None = None) -> None:
        self.canned: int | None = canned

    def get(self, n: int) -> int | None:
        return self.canned

    def save(self, n: int, steps: int) -> None:
        pass


def test_invalid_input_needs_no_collaborators():
    analyzer = CollatzAnalyzer(repo=None, notifier=DummyNotifier())  # pyright: ignore[reportArgumentType]
    with pytest.raises(ValueError):
        analyzer.steps(0)


def test_cached_value_is_returned():
    analyzer = CollatzAnalyzer(StubRepo(canned=42), DummyNotifier())  # pyright: ignore[reportArgumentType]
    assert analyzer.steps(27) == 42       # 42 is not the real answer!


def test_cache_miss_computes():
    analyzer = CollatzAnalyzer(StubRepo(), DummyNotifier())  # pyright: ignore[reportArgumentType]
    assert analyzer.steps(6) == 8


# --------------------------------------------------------------------
# Slide 5: Spy: recording indirect outputs
# --------------------------------------------------------------------
class SpyNotifier:
    def __init__(self):
        self.calls: list[Any] = []

    def alert(self, n: int, steps: int):
        self.calls.append((n, steps))


def test_long_run_alerts():
    spy = SpyNotifier()
    system = CollatzAnalyzer(StubRepo(), spy)
    system.steps(27)   # 111 > 100
    assert spy.calls == [(27, 111)]


def test_short_run_silent():
    spy = SpyNotifier()
    system = CollatzAnalyzer(StubRepo(), spy)
    system.steps(6)    # 8 steps
    assert spy.calls == []


# --------------------------------------------------------------------
# Slide 6: Mock objects with unittest.mock
# --------------------------------------------------------------------
@pytest.fixture
def repo() -> Mock:
    r = Mock(spec=Repository)          # only Repository's attributes allowed
    r.get.return_value = None          # stub behaviour: cache miss
    return r


@pytest.fixture
def notifier() -> Mock:
    return Mock(spec=Notifier)


def test_result_is_saved_and_alerted(repo: Repository, notifier: Notifier):
    CollatzAnalyzer(repo, notifier).steps(27)
    repo.get.assert_called_once_with(27)             # pyright: ignore[reportAttributeAccessIssue]
    repo.save.assert_called_once_with(27, 111)       # pyright: ignore[reportAttributeAccessIssue]
    notifier.alert.assert_called_once_with(27, 111)  # pyright: ignore[reportAttributeAccessIssue]


def test_no_alert_below_threshold(repo: Repository, notifier: Notifier):
    CollatzAnalyzer(repo, notifier).steps(6)
    notifier.alert.assert_not_called()  # pyright: ignore[reportAttributeAccessIssue]


# --------------------------------------------------------------------
# Slide 7: Fake: a lightweight working implementation
# --------------------------------------------------------------------
class InMemoryRepo:  # no DB
    def __init__(self):
        self.data: dict[int, Any] = {}

    def get(self, n: int) -> int | None:
        print(f"get fake db: {n}, {self.data.get(n)}")
        return self.data.get(n)

    def save(self, n: int, steps: int):
        print(f"saving steps: {n},{steps}")
        self.data[n] = steps


def test_results_are_cached():
    repo = InMemoryRepo()
    system = CollatzAnalyzer(repo, Mock())
    print("call first begining")
    first: int = system.steps(27)
    print("call first ending")
    print("call second begining")
    second: int = system.steps(27)  # hit
    print("call second ending")
    assert first == second == 111
    assert repo.data == {27: 111}


# --------------------------------------------------------------------
# Slide 8: Patching: monkeypatch and pytest-mock
# --------------------------------------------------------------------
def next_value2(n: int = 0):
    print("next_value2")
    return 1


def test_step_function_stubbed(monkeypatch: pytest.MonkeyPatch):           # built-in fixture
    r: Callable[..., int] = lambda x: 1  # pyright: ignore[reportUnknownLambdaType, reportAssignmentType]
    monkeypatch.setattr(collatz, "next_value", r)
    analyzer = CollatzAnalyzer(InMemoryRepo(), Mock())
    assert analyzer.steps(10**9) == 1                               # one step, instantly
    monkeypatch.setattr(collatz, "next_value", next_value2)
    analyzer = CollatzAnalyzer(InMemoryRepo(), Mock())
    assert analyzer.steps(10**9) == 1


def test_second_call_does_not_recompute(mocker: Any):          # pip install pytest-mock
    spy = mocker.spy(collatz, "next_value")                    # real function still runs
    analyzer = CollatzAnalyzer(InMemoryRepo(), Mock())
    analyzer.steps(27)
    analyzer.steps(27)
    assert spy.call_count == 111                                    # not 222: cache hit


def test_patch_where_used(mocker: Any):
    fake_step = mocker.patch("src.case6.collatz_analyzer.next_value", side_effect=[4, 2, 1])
    assert CollatzAnalyzer(InMemoryRepo(), Mock()).steps(7) == 3
    assert fake_step.call_args_list[0].args == (7,)


# --------------------------------------------------------------------
# Slide 10: Pitfalls: doubles that lie
# --------------------------------------------------------------------
def test_plain_mock_hides_typos():
    n = Mock()
    n.alrt(27, 111)  # "works", alrt is not the alert function!
    n.alrt.assert_called_once()


def test_autospec_catches_typos():
    n: Any = create_autospec(Notifier, instance=True)
    with pytest.raises(AttributeError):
        n.alrt(27, 111)
    with pytest.raises(AttributeError):
        n.alrt(27)  # bad args


def test_unconfigured_mock():
    system = CollatzAnalyzer(Mock(), Mock())
    result: int = system.steps(27)  # get()->Mock
    assert result                   # passes!
    assert isinstance(result, Mock)


@pytest.mark.skip(reason="anti-pattern demo: would leak into other tests")
def test_leaky():  # BAD
    collatz.next_value = lambda x: 1
    ...                    # never restored
