import pytest
from src.function_solver.core.solver import Solver

def test_solve_linear_equation():
    # Test solving a linear equation
    function1 = "x+2"
    function2 = "3*x-1"
    solutions = Solver.solve(function1, function2)
    assert len(solutions) == 1
    assert float(solutions[0]) == pytest.approx(1.5)

def test_solve_quadratic_equation():
    # Test solving a quadratic equation
    function1 = "x ^ 2 - 4"
    function2 = "0"
    solutions = Solver.solve(function1, function2)
    assert len(solutions) == 2
    assert [float(sol) for sol in solutions] == pytest.approx([-2.0, 2.0])

def test_solve_no_solution():
    # Test no solution case
    function1 = "x + 2"
    function2 = "x + 3"
    solutions = Solver.solve(function1, function2)
    assert not len(solutions)

def test_evaluate_function():
    # Test evaluating a function
    function = "x^2 + 3*x + 2"
    value = 2
    result = Solver.evaluate(function, value)
    assert result == pytest.approx(12.0)