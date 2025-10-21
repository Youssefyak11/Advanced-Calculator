import logging
from logging.handlers import RotatingFileHandler
from .calculator_config import load_config

_cfg = load_config()
logger = logging.getLogger("calculator")
logger.setLevel(logging.INFO)

handler = RotatingFileHandler(_cfg.log_file, maxBytes=512_000, backupCount=3)
fmt = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    "%Y-%m-%d %H:%M:%S",
)
handler.setFormatter(fmt)
if not logger.handlers:
    logger.addHandler(handler)
