from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Protocol, List
import pandas as pd
from colorama import Fore, Style, init as colorama_init
from .operations import get_operation, list_operations
from .calculation import Calculation
from .history import History
from .calculator_config import load_config
from .logger import logger

colorama_init(autoreset=True)

# --- Observers ---
class Observer(Protocol):
    def on_calculation(self, calc: Calculation) -> None: ...

class LoggingObserver:
    def on_calculation(self, calc: Calculation) -> None:
        logger.info(
            "op=%s a=%s b=%s result=%s ts=%s",
            calc.operation, calc.a, calc.b, calc.result, calc.timestamp.isoformat()
        )

class AutoSaveObserver:
    def __init__(self, path, encoding: str):
        self.path = path
        self.encoding = encoding
    def on_calculation(self, calc: Calculation) -> None:
        # No per-event action; save is called centrally after calculate().
        pass  # pragma: no cover

# --- Decorator for dynamic help ---
@dataclass
class HelpDecorator:
    def build_help(self) -> str:
        ops = ", ".join(list_operations().keys())
        return "Commands: " + ops + ", history, clear, undo, redo, save, load, help, exit"

# --- Calculator orchestration ---
class Calculator:
    def __init__(self):
        self.config = load_config()
        self.history = History(max_size=self.config.max_history_size)
        self.observers: List[Observer] = [LoggingObserver()]
        if self.config.auto_save:
            self.observers.append(AutoSaveObserver(self.config.history_file, self.config.default_encoding))
        self.helper = HelpDecorator()

    def _notify(self, calc: Calculation) -> None:
        for obs in self.observers:
            obs.on_calculation(calc)

    def _coerce(self, v):
        f = float(v)
        if abs(f) > self.config.max_input_value:
            raise ValueError(f"Input {f} exceeds allowed magnitude {self.config.max_input_value}")
        return f

    def calculate(self, op_name: str, a, b) -> float:
        op = get_operation(op_name)
        fa, fb = self._coerce(a), self._coerce(b)
        result = round(op.execute(fa, fb), self.config.precision)
        calc = Calculation(op_name, fa, fb, result, datetime.now())
        self.history.add(calc)
        self._notify(calc)
        if self.config.auto_save:
            self.save_history()
        return result

    # --- Persistence via pandas ---
    def save_history(self) -> None:
        df = self.history.to_dataframe()
        df.to_csv(self.config.history_file, index=False, encoding=self.config.default_encoding)

    def load_history(self) -> None:
        try:
            df = pd.read_csv(self.config.history_file, encoding=self.config.default_encoding)
        except FileNotFoundError:
            self.history = History(max_size=self.config.max_history_size)
            return
        self.history = self.history.from_dataframe(df, max_size=self.config.max_history_size)

    # --- Helpers for colored output ---
    @staticmethod
    def ok(msg: str) -> str:      # pragma: no cover
        return f"{Fore.GREEN}{msg}{Style.RESET_ALL}"
    @staticmethod
    def warn(msg: str) -> str:    # pragma: no cover
        return f"{Fore.YELLOW}{msg}{Style.RESET_ALL}"
    @staticmethod
    def err(msg: str) -> str:     # pragma: no cover
        return f"{Fore.RED}{msg}{Style.RESET_ALL}"

    def help_text(self) -> str:
        return self.helper.build_help()
