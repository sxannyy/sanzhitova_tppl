import pytest
from res.ploc import Ploc
from res.token import Token, TokenType
from res.ast import Number, Condition
from res.ploc import operator

@pytest.fixture
def ploc_instance():
    return Ploc({
        "key1": 10,
        "key2": 20,
        "key3": 30,
        "key4": 40,
    })

def test_operator_equal():
    token_10 = Token(TokenType.NUMBER, '10')
    token_20 = Token(TokenType.NUMBER, '20')

    cond_10 = Condition(Token(TokenType.EQUAL, '='), Number(token_10))
    cond_20 = Condition(Token(TokenType.EQUAL, '='), Number(token_20))

    assert operator(cond_10, token_10) is True
    assert operator(cond_20, token_10) is False

def test_operator_more():
    token_10 = Token(TokenType.NUMBER, '10')
    token_20 = Token(TokenType.NUMBER, '20')

    cond_10 = Condition(Token(TokenType.MORE, '>'), Number(token_10))
    cond_20 = Condition(Token(TokenType.MORE, '>'), Number(token_20))

    assert operator(cond_10, token_20) is True
    assert operator(cond_20, token_10) is False

def test_getitem_invalid_type(ploc_instance):
    with pytest.raises(TypeError):
        ploc_instance.getitem(123)

def test_getitem_empty_condition(ploc_instance):
    result = ploc_instance.getitem('')
    assert result == {}

def test_getitem_no_match(ploc_instance):
    result = ploc_instance.getitem('key1 > 100')
    assert result == {}

def test_ploc_init_empty():
    ploc_empty = Ploc({})
    assert len(ploc_empty) == 0