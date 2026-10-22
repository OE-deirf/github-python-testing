import pytest

from src.case4.collatz_analyzer import CollatzAnalyzer
from src.case4.collatz_sequence import CollatzSequence


class TestHandledInvalidInput:
    @pytest.mark.parametrize("start", [0, -1, -100])
    def test_non_positive_start_rejected(self, start: int):
        with pytest.raises(ValueError, match="Input should be greater than 0"):
            CollatzSequence(start)

    def test_analyzer_range_including_zero_rejected(self):
        with pytest.raises(ValueError):
            CollatzAnalyzer(0, 10)

    def test_string_start_rejected_with_clear_message(self):
        # TypeError by`"27" < 1`
        with pytest.raises(ValueError, match="Input should be a valid integer"):
            CollatzSequence("27")  # pyright: ignore[reportArgumentType]

    def test_float_start_rejected(self):
        # floats
        with pytest.raises((TypeError, ValueError)):
            CollatzSequence(27.0)  # pyright: ignore[reportArgumentType]

    def test_bool_start_rejected(self):
        # bool -> int conversion (True == 1)
        with pytest.raises((TypeError, ValueError)):
            CollatzSequence(True)

    def test_reversed_range_rejected(self):
        # Reverse bounds
        with pytest.raises(ValueError):
            CollatzAnalyzer(50, 10)
