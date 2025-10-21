import pytest
from app.operations import get_operation

@pytest.mark.parametrize("name,a,b,expected", [
    ("add", 2, 3, 5),
    ("subtract", 5, 3, 2),
    ("multiply", 2, 4, 8),
    ("divide", 8, 2, 4),
    ("power", 2, 3, 8),
    ("root", 27, 3, 3),
    ("modulus", 7, 3, 1),
    ("int_divide", 7, 3, 2),
    ("percent", 2, 8, 25),
    ("abs_diff", -5, 3, 8),
])
def test_ops(name, a, b, expected):
    op = get_operation(name)
    assert op.execute(a, b) == expected

def test_unknown_operation():
    with pytest.raises(Exception):
        get_operation("does_not_exist")
