from app.calculator_config import load_config

def test_auto_save_false_true(tmp_path, monkeypatch):
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(tmp_path/"logs"))
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path/"hist"))

    monkeypatch.setenv("CALCULATOR_AUTO_SAVE", "false")
    cfg = load_config()
    assert cfg.auto_save is False

    monkeypatch.setenv("CALCULATOR_AUTO_SAVE", "YES")
    cfg2 = load_config()
    assert cfg2.auto_save is True
