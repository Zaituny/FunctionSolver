from typing import List, Union, Dict

from PySide2.QtWidgets import QFrame, QVBoxLayout
from matplotlib.backend_bases import MouseEvent
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.collections import PathCollection
from matplotlib.figure import Figure
import numpy as np
from src.function_solver.core.solver import Solver
from src.function_solver.utils.math_utils import MathUtils


class PlotterWidget(QFrame):
    """
        A custom widget for plotting mathematical functions. This widget uses Matplotlib to plot
        two functions, find their intersection points, and display annotations when hovering over
        the intersection points.

        Attributes:
            points (matplotlib.collections.PathCollection): The scatter plot points representing the solutions.
            annotation (matplotlib.text.Annotation): The annotation displayed when hovering over a solution point.
    """
    def __init__(self):
        """
            Initializes the PlotterWidget. This sets up the user interface and initializes the Matplotlib figure and canvas.
        """
        super().__init__()
        self.setup_ui()
        self.points = None
        self.annotation = None

    def setup_ui(self) -> None:
        """
            Sets up the user interface for the PlotterWidget. This includes creating a Matplotlib figure and canvas,
            and configuring the layout.
        """
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        self.figure = Figure(facecolor='#f8f9fa')
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.create_axis()
        self.canvas.mpl_connect('motion_notify_event', self.hover)
        self.create_annotation()

    def create_axis(self) -> None:
        """
            Creates the Matplotlib axis for the plot. This configures the grid, labels, and visibility of the axis spines.
        """
        self.ax = self.figure.add_subplot(111)
        self.ax.grid(True, linestyle='--', alpha=0.7)
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('y')
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)

    def create_annotation(self) -> None:
        """
            Creates an annotation for displaying coordinates when hovering over solution points.
            The annotation is initially hidden.
        """
        if self.ax is None:
            return

        self.annotation = self.ax.annotate(
            '',
            xy=(0, 0),
            xytext=(20, 20),
            textcoords='offset points',
            bbox=dict(boxstyle='round', fc='white', ec='black', alpha=0.8),
            arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.5', color='black')
        )
        self.annotation.set_visible(False)
        self.canvas.draw_idle()

    def plot_functions(self,
                       f1_text: str,
                       f2_text: str
                       ) -> None:
        """
            Plots two mathematical functions on the same graph and highlights their intersection points.

            :param f1_text: A string representing the first mathematical function (e.g., "x^2 + 3*x + 2").
            :param f2_text: A string representing the second mathematical function (e.g., "2*x + 1").
        """
        self.figure.clear()
        self.create_axis()
        self.create_annotation()

        try:
            solutions = Solver.solve(f1_text, f2_text)
            f1_text = f1_text.replace("^", "**")
            f2_text = f2_text.replace("^", "**")

            center = MathUtils.find_solution_center(solutions)
            min_x, max_x = MathUtils.get_plot_range(center, solutions)
            x = np.linspace(min_x, max_x, 1000)
            # set y limits
            self.ax.set_xlim(min_x, max_x)
            # Plot functions
            y1 = eval(MathUtils.prepare_expression(f1_text))
            self.ax.plot(x, y1, '-', color='#007bff', label=f'f1(x) = {f1_text}', zorder=1)

            y2 = eval(MathUtils.prepare_expression(f2_text))
            self.ax.plot(x, y2, '-', color='#dc3545', label=f'f2(x) = {f2_text}', zorder=2)

            # Plot solutions
            numeric_solutions = [complex(sol).real for sol in solutions if complex(sol).imag == 0]
            self.annotate_solutions(numeric_solutions, f1_text)

            self.ax.legend(loc="upper right")
            self.canvas.draw()

        except Exception as e:
            print(f"Error plotting functions: {e}")

    def annotate_solutions(self,
                           solutions: List,
                           function: str
                           ) -> Union[PathCollection, None]:
        """
            Annotates the intersection points (solutions) on the plot.

            :param solutions: A list of x-values representing the intersection points.
            :param function: The function to evaluate at the intersection points to get the y-values.
            :return: The scatter plot points representing the solutions.
        """
        if not solutions:
            return None

        y_vals = []
        for sol in solutions:
            try:
                y_val = Solver.evaluate(function, sol)
                y_vals.append(y_val)
            except Exception as e:
                print(f"Error evaluating function at {sol}: {e}")
                return None

        self.points = self.ax.scatter(solutions, y_vals,
                                      color='black',
                                      s=50,
                                      zorder=5,
                                      picker=5)
        return self.points

    def update_annot(self,
                     ind: Dict[str, any]
                     ) -> None:
        """
            Updates the annotation text and position when hovering over a solution point.

            :param ind: The index of the point being hovered over.
        """
        pos = self.points.get_offsets()[ind["ind"][0]]
        self.annotation.xy = pos
        text = f'({pos[0]:.4f}, {pos[1]:.4f})'
        self.annotation.set_text(text)
        self.annotation.set_visible(True)

    def hover(self,
              event: MouseEvent
              ) -> None:
        """
            Handles the hover event for the solution points. Displays an annotation when hovering over a point.

            :param event: The Matplotlib event containing information about the mouse movement.
        """
        if not self.points or not self.annotation:
            return

        if event.inaxes != self.ax:
            if self.annotation.get_visible():
                self.annotation.set_visible(False)
                self.canvas.draw_idle()
            return

        cont, ind = self.points.contains(event)
        if cont:
            self.update_annot(ind)
            self.canvas.draw_idle()
        elif self.annotation.get_visible():
            self.annotation.set_visible(False)
            self.canvas.draw_idle()