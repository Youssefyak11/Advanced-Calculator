import pytest
from app.calculator import Calculator
from app.exceptions import OperationError

def test_calculate_tracks_history_and_result():
    c = Calculator()
    r1 = c.calculate("add", 2, 3)
    r2 = c.calculate("multiply", 2, 4)
    assert (r1, r2) == (5, 8)
    hist = c.history.list()
    assert len(hist) == 2
    assert hist[0].operation == "add"
    assert hist[1].operation == "multiply"

def test_calculator_handles_unknown_operation():
    c = Calculator()
    with pytest.raises(OperationError):
        c.calculate("not_an_op", 1, 2)
