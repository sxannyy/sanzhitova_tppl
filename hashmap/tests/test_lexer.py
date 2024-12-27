import pytest
from res.lexer import Lexer
from res.token import TokenType
from res.parser import Parser

@pytest.fixture
def lexer():
    return Lexer()

def test_lexer_init(lexer):
    lexer.init("5 > 3")
    assert lexer._current_char == "5"

def test_check_token_valid(lexer):
    lexer.init("5>3")
    parser = Parser()
    parser._lexer = lexer
    parser._current_token = lexer.next()
    parser.check_token(TokenType.NUMBER)
    assert parser._current_token.type_ == TokenType.MORE
    
def test_check_token_invalid(lexer):
    lexer.init("5>3")
    parser = Parser()
    parser._lexer = lexer
    parser._current_token = lexer.next()
    with pytest.raises(SyntaxError, match="Invalid token order"):
        parser.check_token(TokenType.LESS)

def test_lexer_number(lexer):
    lexer.init("123.45")
    token = lexer.number()
    assert token == "123.45"

def test_lexer_operators(lexer):
    lexer.init(">=")
    token = lexer.operators()
    assert token.type_ == TokenType.MOREEQUAL
    assert token.value == ">="

    lexer.init("<=")
    token = lexer.operators()
    assert token.type_ == TokenType.LESSEQUAL
    assert token.value == "<="

    lexer.init("<>")
    token = lexer.operators()
    assert token.type_ == TokenType.UNEQUAL
    assert token.value == "<>"

    lexer.init("<5")
    token = lexer.operators()
    assert token.type_ == TokenType.LESS
    assert token.value == "<"


def test_lexer_next_compare(lexer):
    lexer.init("5 >= 3")
    token = lexer.next()
    assert token.type_ == TokenType.NUMBER
    assert token.value == "5"
    
    token = lexer.next()
    assert token.type_ == TokenType.MOREEQUAL
    assert token.value == ">="
    
    token = lexer.next()
    assert token.type_ == TokenType.NUMBER
    assert token.value == "3"

def test_lexer_next_eq(lexer):
    lexer.init("4 = 4")
    token = lexer.next()
    assert token.type_ == TokenType.NUMBER
    assert token.value == "4"

    with pytest.raises(SyntaxError):
        token = lexer.next()

    token = lexer.next()
    assert token.type_ == TokenType.NUMBER
    assert token.value == "4"
    
def test_equal_token_with_digit(lexer):
    lexer.init("=1")
    token = lexer.next()
    assert token.type_ == TokenType.EQUAL
    assert token.value == '='