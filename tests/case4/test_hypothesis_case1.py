import pytest
from hypothesis import given, strategies as st

from src.case1.collatz_sequence import CollatzSequence


@given(st.integers(min_value=1, max_value=100_000))
def test_sequence_properties(start: int):
    seq = CollatzSequence(start)
    assert seq.values[0] == start
    assert seq.values[-1] == 1
    assert seq.peak >= start
    assert seq.steps == len(seq.values) - 1


@given(st.integers(max_value=0))
def test_non_positive_int_rejected(start: int):
    with pytest.raises(ValueError):
        CollatzSequence(start)


@given(st.one_of(st.text(), st.booleans(), st.none()))
def test_non_int_rejected(value: int):
    with pytest.raises((TypeError, ValueError)):
        CollatzSequence(value)


@given(st.floats(min_value=-1, max_value=100_000))
def test_non_positive_float_rejected(start: int):
    with pytest.raises(ValueError):
        CollatzSequence(start)
