import os
from pathlib import Path
import pytest
from app.calculator import Calculator

def test_help_text_lists_ops():
    c = Calculator()
    h = c.help_text()
    assert "add" in h and "history" in h and "exit" in h

def test_autosave_creates_csv(tmp_path, monkeypatch):
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(tmp_path/"logs"))
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path/"hist"))
    monkeypatch.setenv("CALCULATOR_AUTO_SAVE", "true")
    c = Calculator()
    c.calculate("add", 2, 3)
    f = c.config.history_file
    assert f.exists(), f"Expected file at {f}"

def test_value_coercion_limit_raises(tmp_path, monkeypatch):
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(tmp_path/"logs"))
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path/"hist"))
    monkeypatch.setenv("CALCULATOR_MAX_INPUT_VALUE", "5")
    c = Calculator()
    with pytest.raises(Exception):
        c.calculate("add", 10, 1)  # exceeds limit

def test_load_history_when_missing(tmp_path, monkeypatch):
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(tmp_path/"logs"))
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path/"hist"))
    # ensure no CSV exists
    c = Calculator()
    c.load_history()  # should not raise
    assert len(c.history.list()) == 0
