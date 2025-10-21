from typing import List
from copy import deepcopy
import pandas as pd
from .calculation import Calculation
from .exceptions import HistoryError

class History:
    def __init__(self, max_size=100):
        self._items: List[Calculation] = []
        self._undo: List[List[Calculation]] = []
        self._redo: List[List[Calculation]] = []
        self._max_size = max_size

    def _snapshot(self):
        return deepcopy(self._items)

    def add(self, calc: Calculation):
        self._undo.append(self._snapshot())
        self._redo.clear()
        self._items.append(calc)
        if len(self._items) > self._max_size:
            self._items.pop(0)

    def list(self) -> List[Calculation]:
        return list(self._items)

    def clear(self):
        self._items.clear()

    def undo(self):
        if not self._undo:
            raise HistoryError("Nothing to undo")
        self._redo.append(self._snapshot())
        self._items = self._undo.pop()

    def redo(self):
        if not self._redo:
            raise HistoryError("Nothing to redo")
        self._undo.append(self._snapshot())
        self._items = self._redo.pop()

    # --- pandas persistence ---
    def to_dataframe(self) -> pd.DataFrame:
        if not self._items:
            return pd.DataFrame(columns=["operation","a","b","result","timestamp"])
        return pd.DataFrame([{
            "operation": c.operation,
            "a": c.a,
            "b": c.b,
            "result": c.result,
            "timestamp": c.timestamp.isoformat(),
        } for c in self._items])

    @classmethod
    def from_dataframe(cls, df: pd.DataFrame, max_size: int) -> "History":
        h = cls(max_size=max_size)
        if df.empty:
            return h
        from datetime import datetime
        for _, row in df.iterrows():
            h._items.append(Calculation(
                operation=str(row["operation"]),
                a=float(row["a"]),
                b=float(row["b"]),
                result=float(row["result"]),
                timestamp=datetime.fromisoformat(str(row["timestamp"])),
            ))
        return h

