import pytest
import sys
sys.path.append("..")
from interpreter.interpreter import Interpreter
from interpreter.lexer import Lexer
from interpreter.parser import Parser
from interpreter.ast import BinOp, Number, UnaryOp, Variable, Assignment, Semicolon
from interpreter.token import Token, TokenType

@pytest.fixture
def interpreter():
    return Interpreter()

class TestInterpreter:
    def test_invalid_syntax(self, interpreter):
        with pytest.raises(SyntaxError):
            interpreter.eval("1+=-2")
        with pytest.raises(SyntaxError):
            interpreter.eval("(1+2")

    def test_binop_invalid_operator(self, interpreter):
        invalid_op = BinOp(Number(Token(TokenType.NUMBER, "2")), Token(TokenType.OPERATOR, "^"), Number(Token(TokenType.NUMBER, "3")))
        with pytest.raises(RuntimeError, match="Invalid operator"):
            interpreter._visit_binop(invalid_op)

    def test_unaryop(self, interpreter):
        assert interpreter.eval("BEGIN x:=1++++1 END.") == {"x":2}
        assert interpreter.eval("BEGIN x:=1----1 END.") == {"x":2}

    def test_bad_unaryop(self, interpreter):
        with pytest.raises(RuntimeError):
            interpreter._visit_unaryop(UnaryOp(Token(TokenType.OPERATOR, "^"), Number(Token(TokenType.NUMBER, 3))))

    def test_variable_assignment(self, interpreter):
        assert interpreter.eval("BEGIN x := 5; y := x + 1; END.") == {"x": 5.0, "y": 6.0}

    def test_undefined_variable(self, interpreter):
        with pytest.raises(ValueError, match="Variable 'y' is not defined"):
            interpreter.eval("BEGIN x := 1; z := y; END.")

    def test_empty_program(self, interpreter):
        assert interpreter.eval("BEGIN END.") == {}

    def test_complex_expression(self, interpreter):
        result = interpreter.eval("BEGIN x := 2 + 3 * (2 + 3); y := (x - 5) / 2; END.")
        assert result == {"x": 17.0, "y": 6.0}

    def test_nested_statements(self, interpreter):
        result = interpreter.eval(
            "BEGIN a := 1; b := 2; BEGIN c := a + b; d := c * 2; END; e := d - 1; END."
        )
        assert result == {"a": 1.0, "b": 2.0, "c": 3.0, "d": 6.0, "e": 5.0}

    def test_assignment_order(self, interpreter):
        with pytest.raises(SyntaxError):
            interpreter.eval("BEGIN 1 := x; END.")

    def test_semicolon_handling(self, interpreter):
        result = interpreter.eval("BEGIN x := 1; y := 2; z := x + y; END.")
        assert result == {"x": 1.0, "y": 2.0, "z": 3.0}

    def test_eval(self, interpreter):
        result = interpreter.eval("BEGIN x := 1 + 1; END.")
        assert result == {"x": 2}
        result = interpreter.eval("BEGIN x := -2 + 3; END.")
        assert result == {"x": 1}
        with pytest.raises(SyntaxError):
            interpreter.eval("BEGIN x := 1 +; END.")

    def test_empty_code(self, interpreter):
        assert interpreter.eval("BEGIN END.") == {}

    def test_easy_code(self, interpreter):
        assert interpreter.eval("BEGIN x:= 2 + 3 * (2 + 3); y:= 2 / 2 - 2 + 3 * ((1 + 1) + (1 + 1)); END.") == {'x': 17.0, 'y': 11.0}

    def test_medium_code(self, interpreter):
        assert interpreter.eval("BEGIN y:= 2; BEGIN a := 3; a := a; b := 10 + a + 10 * y / 4; c := a - b; END; x := 11; END.") == {'x': 11.0, 'y': 2.0, 'a': 3.0, 'b': 18.0, 'c': -15.0}
    
@pytest.fixture
def lexer():
    return Lexer()

class TestLexer:
    def test_create_var(self, lexer):
        with pytest.raises(SyntaxError):
            lexer._Lexer__variable()

    def test_assignment_bad_token(self, lexer):
        lexer.init("  :-")
        with pytest.raises(SyntaxError):
            lexer._Lexer__assignment()

    def test_next(self, lexer):
        lexer.init("BEGIN x:=10; END.")
        assert str(lexer.next()) == str(Token(TokenType.BEGIN, "BEGIN"))
        assert str(lexer.next()) == str(Token(TokenType.IDENTIFIER, "x"))
        assert str(lexer.next()) == str(Token(TokenType.ASSIGNMENT, ":="))
        assert str(lexer.next()) == str(Token(TokenType.NUMBER, "10"))
        assert str(lexer.next()) == str(Token(TokenType.SEMICOLON, ";"))
        assert str(lexer.next()) == str(Token(TokenType.END, "END"))
        assert str(lexer.next()) == str(Token(TokenType.DOT, "."))

    def test_next_bad_token(self, lexer):
        lexer.init("BEGIN ^")
        assert str(lexer.next()) == str(Token(TokenType.BEGIN, "BEGIN"))
        with pytest.raises(SyntaxError):
            lexer.next()

@pytest.fixture
def parser():
    return Parser()

class TestParser:
    def test_check_token(self, parser):
        with pytest.raises(SyntaxError):
            parser._Parser__check_token(Token(TokenType.NUMBER, "True"))

class TestAst:
    def test_number_str(self):
        token = Token(TokenType.NUMBER, "1")
        number_node = Number(token)
        assert str(number_node) == "Number (Token(TokenType.NUMBER, 1))"

    def test_binop_str(self):
        left = Number(Token(TokenType.NUMBER, "1"))
        right = Number(Token(TokenType.NUMBER, "2"))
        operator = Token(TokenType.OPERATOR, "+")
        binop_node = BinOp(left, operator, right)
        assert str(binop_node) == "BinOp + (Number (Token(TokenType.NUMBER, 1)), Number (Token(TokenType.NUMBER, 2)))"

    def test_unary_op_str(self):
        token = Token(TokenType.OPERATOR, "-")
        number_node = Number(Token(TokenType.NUMBER, "3"))
        unary_node = UnaryOp(token, number_node)
        assert str(unary_node) == "UnaryOp-Number (Token(TokenType.NUMBER, 3))"

    def test_variable_str(self):
        variable_node = Variable("x")
        assert str(variable_node) == "Variable(x)"

    def test_assignment_str(self):
        variable_node = Variable("x")
        number_node = Number(Token(TokenType.NUMBER, "5"))
        assignment_node = Assignment(variable_node, number_node)
        assert str(assignment_node) == "AssignmentVariable(x):=Number (Token(TokenType.NUMBER, 5))"

    def test_semicolon_str(self):
        left_node = Variable("x")
        right_node = Variable("y")
        semicolon_node = Semicolon(left_node, right_node)
        assert str(semicolon_node) == "Semicolon(Variable(x), Variable(y))"
