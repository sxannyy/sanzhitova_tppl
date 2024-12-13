from res.token import Token, TokenType

def test_token_str():
    token = Token(TokenType.NUMBER, "5")
    assert str(token) == "The token is (TokenType.NUMBER, 5)"