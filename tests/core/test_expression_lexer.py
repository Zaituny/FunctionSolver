import pytest
from src.function_solver.core.expression_lexer import ExpressionLexer

@pytest.fixture
def lexer():
    return ExpressionLexer()

def test_valid_tokens(lexer):
    # Test valid tokens
    input_text = "x + 3 * (y - 2) / 4 ^ 2"
    tokens, errors = lexer.tokenize(input_text)
    assert errors == []
    assert tokens == ['VARIABLE', 'PLUS', 'NUMBER', 'TIMES', 'LPAREN', 'VARIABLE', 'MINUS', 'NUMBER', 'RPAREN', 'DIVIDE', 'NUMBER', 'POWER', 'NUMBER']

def test_invalid_tokens(lexer):
    # Test invalid tokens
    input_text = "x + 3 * @"
    tokens, errors = lexer.tokenize(input_text)
    assert errors == ["Invalid character '@'"]
    assert tokens == ['VARIABLE', 'PLUS', 'NUMBER', 'TIMES']

def test_log_token(lexer):
    # Test 'log' token
    input_text = "log(x)"
    tokens, errors = lexer.tokenize(input_text)
    assert errors == []
    assert tokens == ['LOG', 'LPAREN', 'VARIABLE', 'RPAREN']