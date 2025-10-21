from datetime import datetime
from app.calculation import Calculation

def test_calculation_dataclass_fields():
    c = Calculation("add", 1.5, 2.5, 4.0, datetime.now())
    assert c.operation == "add"
    assert c.a == 1.5
    assert c.b == 2.5
    assert c.result == 4.0
