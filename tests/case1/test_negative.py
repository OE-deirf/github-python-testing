import pytest

from src.case1.collatz_analyzer import CollatzAnalyzer
from src.case1.collatz_sequence import CollatzSequence


class TestHandledInvalidInput:
    @pytest.mark.parametrize("start", [0, -1, -100])
    def test_non_positive_start_rejected(self, start: int):
        with pytest.raises(ValueError, match="Needs positive int!"):
            CollatzSequence(start)

    def test_analyzer_range_including_zero_rejected(self):
        with pytest.raises(ValueError):
            CollatzAnalyzer(0, 10)


class TestUnvalidatedInput:
    def test_string_start_rejected_with_clear_message(self):
        # TypeError by`"27" < 1`
        with pytest.raises(TypeError):
            CollatzSequence("27")  # pyright: ignore[reportArgumentType]

    # failed
    def test_float_start_rejected(self):
        # floats
        with pytest.raises((TypeError, ValueError)):
            CollatzSequence(27.0)  # pyright: ignore[reportArgumentType]

    # failed
    def test_bool_start_rejected(self):
        # bool -> int conversion (True == 1)
        with pytest.raises((TypeError, ValueError)):
            CollatzSequence(True)

    # failed
    def test_reversed_range_rejected(self):
        # Reverse bounds
        with pytest.raises(ValueError):
            CollatzAnalyzer(50, 10)
