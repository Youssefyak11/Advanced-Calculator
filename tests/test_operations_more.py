import pytest
from app.operations import get_operation

def test_divide_by_zero_maps_to_operationerror():
    div = get_operation("divide")
    with pytest.raises(Exception):
        div.execute(1, 0)

@pytest.mark.parametrize("name,a,b,expected", [
    ("power", 2, -1, 0.5),
    ("abs_diff", 10, 3, 7),
    ("root", 16, 2, 4),
    ("modulus", 10, 4, 2),
    ("int_divide", 10, 4, 2),
])
def test_edge_ops(name, a, b, expected):
    op = get_operation(name)
    assert op.execute(a, b) == expected
