from __future__ import annotations
import os
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv

@dataclass(frozen=True)
class Config:
    log_dir: Path
    history_dir: Path
    log_file: Path
    history_file: Path
    max_history_size: int
    auto_save: bool
    precision: int
    max_input_value: float
    default_encoding: str

def _as_bool(v: str | None, default: bool) -> bool:
    if v is None:
        return default
    return v.strip().lower() in {"1","true","y","yes","on"}

def load_config() -> Config:
    load_dotenv()
    log_dir = Path(os.getenv("CALCULATOR_LOG_DIR", "./logs")).resolve()
    history_dir = Path(os.getenv("CALCULATOR_HISTORY_DIR", "./history")).resolve()
    log_dir.mkdir(parents=True, exist_ok=True)
    history_dir.mkdir(parents=True, exist_ok=True)
    return Config(
        log_dir=log_dir,
        history_dir=history_dir,
        log_file=log_dir / os.getenv("CALCULATOR_LOG_FILE", "calculator.log"),
        history_file=history_dir / os.getenv("CALCULATOR_HISTORY_FILE", "history.csv"),
        max_history_size=int(os.getenv("CALCULATOR_MAX_HISTORY_SIZE", "100")),
        auto_save=_as_bool(os.getenv("CALCULATOR_AUTO_SAVE"), True),
        precision=int(os.getenv("CALCULATOR_PRECISION", "6")),
        max_input_value=float(os.getenv("CALCULATOR_MAX_INPUT_VALUE", "1e9")),
        default_encoding=os.getenv("CALCULATOR_DEFAULT_ENCODING", "utf-8"),
    )
