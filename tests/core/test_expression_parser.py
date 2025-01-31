import pytest
from src.function_solver.core.expression_parser import ExpressionParser

@pytest.fixture
def parser():
    return ExpressionParser()

def test_valid_expression(parser):
    # Test valid expression
    expression = "x + 3 * (y - 2) / 4 ^ 2"
    validation = parser.validate(expression)
    assert validation['is_valid'] == True
    assert validation['errors'] == []

def test_invalid_expression(parser):
    # Test invalid expression
    expression = "x + 3 * (y - 2 / 4 ^ 2"  # Missing closing parenthesis
    validation = parser.validate(expression)
    assert validation['is_valid'] == False
    assert "Syntax error at end of expression" in validation['errors']

def test_log_function(parser):
    # Test log function
    expression = "log(x + 1)"
    validation = parser.validate(expression)
    assert validation['is_valid'] == True
    assert validation['errors'] == []