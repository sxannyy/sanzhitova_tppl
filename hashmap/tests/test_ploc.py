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
        "(key1, key2)": 50,
        "(key5)": 60,
    })

def test_operator_equal():
    token_10 = Token(TokenType.NUMBER, '10')
    token_20 = Token(TokenType.NUMBER, '20')

    cond_10 = Condition(Token(TokenType.EQUAL, '='), Number(token_10))
    cond_20 = Condition(Token(TokenType.EQUAL, '='), Number(token_20))

    assert operator(cond_10, token_10) is True
    assert operator(cond_20, token_10) is False

def test_operators():
    token_10 = Token(TokenType.NUMBER, '10')
    token_20 = Token(TokenType.NUMBER, '20')

    cond_20 = Condition(Token(TokenType.MORE, '>'), Number(token_10))
    assert operator(cond_20, token_10) is False

    cond_20 = Condition(Token(TokenType.MOREEQUAL, '>='), Number(token_20))
    assert operator(cond_20, token_10) is False

    cond_20 = Condition(Token(TokenType.LESS, '<'), Number(token_20))
    assert operator(cond_20, token_10) is True

    cond_20 = Condition(Token(TokenType.LESSEQUAL, '<='), Number(token_20))
    assert operator(cond_20, token_10) is True

    cond_20 = Condition(Token(TokenType.UNEQUAL, '<>'), Number(token_20))
    assert operator(cond_20, token_10) is True

    with pytest.raises(SyntaxError):
        cond_20 = Condition(Token(TokenType.UNEQUAL, '<<<'), Number(token_20))
        assert operator(cond_20, token_10) is True

def test_getitem_invalid_type(ploc_instance):
    with pytest.raises(TypeError):
        ploc_instance[123]

def test_getitem_empty_condition(ploc_instance):
    result = ploc_instance['']
    assert result == {}

def test_getitem_no_match(ploc_instance):
    result = ploc_instance['key1 > 100']
    assert result == {}

def test_ploc_init_empty():
    ploc_empty = Ploc({})
    assert len(ploc_empty) == 0
    
def test_getitem_brackets(ploc_instance):
    result = ploc_instance['>=1']
    assert result == {'(key5)': 60}