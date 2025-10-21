from datetime import datetime
from .operations import get_operation
from .calculation import Calculation
from .history import History

class Calculator:
    def __init__(self):
        self.history = History()

    def calculate(self, op_name, a, b):
        op = get_operation(op_name)
        result = op.execute(float(a), float(b))
        calc = Calculation(op_name, float(a), float(b), result, datetime.now())
        self.history.add(calc)
        return result
