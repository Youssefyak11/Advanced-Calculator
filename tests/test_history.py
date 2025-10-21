from datetime import datetime
import pytest
from app.history import History
from app.calculation import Calculation
from app.exceptions import HistoryError

def _calc(i):
    return Calculation("add", float(i), float(i), float(2*i), datetime.now())

def test_add_undo_redo_and_rollover():
    h = History(max_size=2)
    h.add(_calc(1))
    h.add(_calc(2))
    assert len(h.list()) == 2
    h.add(_calc(3))
    assert len(h.list()) == 2
    assert h.list()[0].a == 2.0
    h.undo()
    assert len(h.list()) == 2
    h.redo()
    assert len(h.list()) == 2

def test_undo_redo_empty_errors():
    h = History()
    with pytest.raises(HistoryError):
        h.undo()
    with pytest.raises(HistoryError):
        h.redo()
