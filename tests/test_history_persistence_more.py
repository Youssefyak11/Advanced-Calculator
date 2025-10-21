from datetime import datetime
import pandas as pd
from app.history import History
from app.calculation import Calculation

def test_to_dataframe_empty_has_columns():
    h = History()
    df = h.to_dataframe()
    assert list(df.columns) == ["operation","a","b","result","timestamp"]
    assert df.empty

def test_roundtrip_via_dataframe():
    h = History()
    h.add(Calculation("add", 1.0, 2.0, 3.0, datetime.now()))
    df = h.to_dataframe()
    h2 = History.from_dataframe(df, max_size=10)
    items = h2.list()
    assert len(items) == 1
    c = items[0]
    assert c.operation == "add" and c.a == 1.0 and c.b == 2.0 and c.result == 3.0

def test_clear_history():
    h = History()
    h.add(Calculation("add", 1, 1, 2, datetime.now()))
    h.clear()
    assert len(h.list()) == 0
