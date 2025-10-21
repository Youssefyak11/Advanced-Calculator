import pytest
from app.operations import list_operations, get_operation
from app.exceptions import OperationError

def test_list_operations_contains_core():
    ops = list_operations()
    for name in ["add","subtract","multiply","divide","power","root","modulus","int_divide","percent","abs_diff"]:
        assert name in ops

def test_execute_handles_zero_division():
    with pytest.raises(OperationError):
        get_operation("divide").execute(1, 0)
