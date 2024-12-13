from enum import Enum, auto

class TokenType(Enum):
    MORE = auto()
    LESS = auto()
    MOREEQUAL = auto()
    LESSEQUAL = auto()
    EQUAL = auto()
    UNEQUAL = auto()
    NUMBER = auto()

class Token:
    def __init__(self, type_: TokenType, value: str):
        self.type_ = type_
        self.value = value

    def __str__(self):
        return f"The token is ({self.type_}, {self.value})"