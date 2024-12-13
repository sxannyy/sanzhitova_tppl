import pytest
from res.lexer import Lexer
from res.token import TokenType
from res.parser import Parser

def test_lexer_init():
    lexer = Lexer()
    lexer.init("5 > 3")
    assert lexer._current_char == "5"

def test_check_token_valid():
    lexer = Lexer()
    lexer.init("5>3")
    parser = Parser()
    parser._lexer = lexer
    parser._current_token = lexer.next()
    parser.check_token(TokenType.NUMBER)
    assert parser._current_token.type_ == TokenType.MORE
    
def test_check_token_invalid():
    lexer = Lexer()
    lexer.init("5>3")
    parser = Parser()
    parser._lexer = lexer
    parser._current_token = lexer.next()
    with pytest.raises(SyntaxError, match="Invalid token order"):
        parser.check_token(TokenType.LESS)

def test_lexer_number():
    lexer = Lexer()
    lexer.init("123.45")
    token = lexer.number()
    assert token == "123.45"

def test_lexer_operators():
    lexer = Lexer()
    lexer.init(">=")
    token = lexer.operators()
    assert token.type_ == TokenType.MOREEQUAL
    assert token.value == ">="

    lexer.init("<=")
    token = lexer.operators()
    assert token.type_ == TokenType.LESSEQUAL
    assert token.value == "<="

def test_lexer_next():
    lexer = Lexer()
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

def test_invalid_operator():
    lexer = Lexer()
    lexer.init("*")
    with pytest.raises(SyntaxError, match="Not a valid condition"):
        lexer.operators()