import pytest
import sys
sys.path.append("..")
from res.ast import Number, Condition
from res.token import Token, TokenType

def test_number_str():
    token = Token(TokenType.NUMBER, "5")
    number = Number(token)
    assert str(number) == "Number (The token is (TokenType.NUMBER, 5))"

def test_condition_str():
    token = Token(TokenType.MORE, ">")
    number = Number(Token(TokenType.NUMBER, "3"))
    condition = Condition(token, number)
    assert str(condition) == "Condition (The token is (TokenType.MORE, >)Number (The token is (TokenType.NUMBER, 3)))"