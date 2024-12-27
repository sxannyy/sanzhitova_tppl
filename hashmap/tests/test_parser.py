import pytest
from res.parser import Parser
from res.ast import Condition

@pytest.fixture
def parser():
    return Parser()

def test_parser_parse(parser):
    result = parser.parse("5 > 3")
    assert isinstance(result, list)
    assert len(result) == 2
    assert isinstance(result[1], Condition) == True
    assert result[1].op.value == ">"

def test_parser_invalid_order(parser):
    with pytest.raises(SyntaxError):
        parser.parse("> >")

def test_parser_factor(parser):
    with pytest.raises(SyntaxError):
        parser.factor()