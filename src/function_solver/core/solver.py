from typing import List
import sympy


class Solver:
    """
        A class for solving and evaluating mathematical functions. This class uses the SymPy library
        to perform symbolic mathematics, including solving equations and evaluating functions at specific points.
    """
    @staticmethod
    def solve(function1: str,
              function2: str
              ) -> List:
        """
            Solves the equation `function1 = function2` for the variable `x`.

            This method takes two mathematical functions as strings, converts them into SymPy expressions,
            and then solves the equation formed by setting the two functions equal to each other.

            :param function1: A string representing the first mathematical function (e.g., "x**2 + 3*x + 2").
            :param function2: A string representing the second mathematical function (e.g., "2*x + 1").
            :return: A list of solutions for the variable `x`. If no solution is found or if the equation
                     cannot be solved, an empty list is returned.
        """
        # Convert the input strings into SymPy expressions
        function1_sympified = sympy.sympify(function1)
        function2_sympified = sympy.sympify(function2)
        try:
            # Solve the equation `function1 = function2` for `x`
            return sympy.solve(sympy.Eq(function1_sympified,
                                        function2_sympified),
                               sympy.symbols('x'))
        except NotImplementedError as e:
            print(e)
            return []

    @staticmethod
    def evaluate(function: str,
                 value: float
                 ) -> float:
        """
                Evaluates a mathematical function at a specific value of `x`.

                This method takes a mathematical function as a string and evaluates it at the given value of `x`.

                :param function: A string representing the mathematical function (e.g., "x**2 + 3*x + 2").
                :param value: The value of `x` at which the function should be evaluated.
                :return: The result of evaluating the function at the given value of `x`.
                """
        function_sympified = sympy.sympify(function)
        # Substitute `x` with the given value and evaluate the expression
        return function_sympified.subs(sympy.symbols('x'), value)

