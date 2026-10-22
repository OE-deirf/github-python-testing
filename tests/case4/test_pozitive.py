import pytest

from src.case4.collatz_analyzer import CollatzAnalyzer
from src.case4.collatz_sequence import CollatzSequence


class TestCollatzSequence:
    def test_start_one_has_zero_steps(self):
        seq = CollatzSequence(1)
        assert seq.values == [1]
        assert seq.steps == 0
        assert seq.peak == 1

    def test_known_sequence_for_six(self):
        seq = CollatzSequence(6)
        assert seq.values == [6, 3, 10, 5, 16, 8, 4, 2, 1]
        assert seq.steps == 8
        assert seq.peak == 16

    def test_famous_case_27(self):
        seq = CollatzSequence(27)
        assert seq.steps == 111
        assert seq.peak == 9232

    @pytest.mark.parametrize("start", [1, 2, 3, 7, 19, 97, 871])
    def test_sequence_starts_with_start_and_ends_with_one(self, start: int):
        seq = CollatzSequence(start)
        assert seq.values[0] == start
        assert seq.values[-1] == 1

    @pytest.mark.parametrize("start", [3, 7, 27, 97])
    def test_each_step_follows_the_rule(self, start: int):
        values: list[int] = CollatzSequence(start).values
        for current, following in zip(values, values[1:]):
            expected: int = current // 2 if current % 2 == 0 else 3 * current + 1
            assert following == expected


class TestCollatzAnalyzer:
    def test_longest_in_small_range(self):
        best: CollatzSequence = CollatzAnalyzer(1, 10).longest()
        assert best.start == 9
        assert best.steps == 19

    def test_longest_up_to_hundred(self):
        best: CollatzSequence = CollatzAnalyzer(1, 100).longest()
        assert best.start == 97
        assert best.steps == 118

    def test_highest_peak_up_to_hundred(self):
        assert CollatzAnalyzer(1, 100).highest_peak().peak == 9232

    def test_single_element_range(self):
        analyzer = CollatzAnalyzer(5, 5)
        assert len(analyzer.sequences) == 1
        assert analyzer.longest().start == 5
