from dataclasses import dataclass
from typing import Callable, Dict
from .exceptions import OperationError

@dataclass(frozen=True)
class Operation:
    name: str
    func: Callable[[float, float], float]
    def execute(self, a: float, b: float) -> float:
        try:
            return self.func(a, b)
        except ZeroDivisionError as e:
            raise OperationError("Division by zero") from e

_registry: Dict[str, Operation] = {}
def register_operation(name, func):
    _registry[name] = Operation(name, func)
def get_operation(name):
    if name not in _registry:
        raise OperationError(f"Unknown op: {name}")
    return _registry[name]

# Register basic operations
register_operation("add", lambda a,b: a+b)
register_operation("subtract", lambda a,b: a-b)
register_operation("multiply", lambda a,b: a*b)
register_operation("divide", lambda a,b: a/b)
register_operation("power", lambda a,b: a**b)
register_operation("root", lambda a,b: a**(1/b))
register_operation("modulus", lambda a,b: a % b)
register_operation("int_divide", lambda a,b: a // b)
register_operation("percent", lambda a,b: (a/b)*100)
register_operation("abs_diff", lambda a,b: abs(a-b))
