from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class Calculation:
    operation: str
    a: float
    b: float
    result: float
    timestamp: datetime
