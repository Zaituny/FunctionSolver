from typing import Tuple, List

from src.function_solver.core.solver import Solver


class MathUtils:
    """
        A utility class for performing mathematical operations and transformations.
        This class provides methods for preparing mathematical expressions, finding the center of solutions,
        and determining the appropriate plot range for visualizing functions.
    """
    @staticmethod
    def prepare_expression(text: str) -> str:
        """
            Prepares a mathematical expression for evaluation by replacing certain operators and functions
            with their equivalents in Python's syntax.

            :param text: The input mathematical expression as a string (e.g., "x^2 + log(x)").
            :return: The transformed expression ready for evaluation (e.g., "x^2 + np.log(x)").
        """
        replacement_dict = {
            'log': 'np.log',
            'sqrt': 'np.sqrt'
        }
        for key, value in replacement_dict.items():
            text = text.replace(key, value)
        return text

    @staticmethod
    def find_solution_center(solutions: List) -> float:
        """
            Finds the center of a list of solutions. The center is calculated as the average of the real parts
            of the solutions, ignoring any complex solutions.

            :param solutions: A list of solutions, which may include complex numbers.
            :return: The center of the solutions as a float. If no valid solutions are found, returns 0.
        """
        if not solutions:
            return 0
        numeric_solutions = [complex(sol).real for sol in solutions if complex(sol).imag == 0]
        if not numeric_solutions:
            return 0
        return float(sum(numeric_solutions) / len(numeric_solutions))

    @staticmethod
    def get_plot_range(center: float,
                       solutions: List,
                       ) -> Tuple[float, float]:
        """
            Determines the appropriate x-axis range for plotting based on the solutions of a function.
            The range is calculated to include all solutions with some padding.

            :param center: The center of the solutions, typically calculated using `find_solution_center`.
            :param solutions: A list of solutions, which may include complex numbers.
            :return: A tuple containing the minimum and maximum x-axis values for the plot.
                     If no valid solutions are found, returns a default range around the center.
        """
        if not solutions:
            return center - 5, center + 5

        numeric_solutions = [float(complex(sol).real) for sol in solutions if complex(sol).imag == 0]
        if not numeric_solutions:
            return center - 5, center + 5

        min_sol = min(numeric_solutions)
        max_sol = max(numeric_solutions)

        domain_size = max_sol - min_sol
        x_padding = max(domain_size * 0.2, 1)
        return min_sol - x_padding, max_sol + x_padding
