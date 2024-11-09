import pytest
from prefix_to_infix.base import prefix_to_infix

@pytest.mark.parametrize("expression, expected", [
    ("+ 1 2", "(1 + 2)"),
    ("- 10 3", "(10 - 3)"),
    ("* 5 5", "(5 * 5)"),
    ("/ 16 4", "(16 / 4)"),
    ("+ 5 * 4 45", "(5 + (4 * 45))"),
])

def test_prefix_to_infix(expression, expected):
    assert prefix_to_infix(expression) == expected

@pytest.mark.parametrize("expression", [
    "+ 123",
    "* 56 y",
    "- 5 12 4",
    "- + *"
])

def test_prefix_to_infix_errors(expression):
    with pytest.raises(ValueError):
        prefix_to_infix(expression)