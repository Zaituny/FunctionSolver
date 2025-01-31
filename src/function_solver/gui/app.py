from PySide2.QtWidgets import QMainWindow, QWidget, QHBoxLayout
from pathlib import Path
from .components.input import InputWidget
from .components.plotter import PlotterWidget
from ..utils.resources_utils import ResourceUtils


class FunctionSolverWindow(QMainWindow):
    """
        The main application window for the Function Plotter application. This window integrates
        the input widget and the plotter widget, allowing users to input mathematical functions
        and visualize their plots and intersection points.

        Attributes:
            input_widget (InputWidget): The widget for inputting mathematical functions.
            plot_widget (PlotterWidget): The widget for plotting the functions and displaying their intersection points.
    """
    def __init__(self):
        """
            Initializes the FunctionSolverWindow. This sets up the user interface, loads the application styles,
            and sets the window icon.
        """
        super().__init__()
        self.setWindowTitle("Function Plotter")
        self.setup_ui()
        self.load_styles()
        self.setup_window_icon()

    def setup_ui(self):
        """
            Sets up the user interface for the main window. This includes creating the input widget,
            the plotter widget, and connecting their signals and slots.
        """
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

        self.input_widget = InputWidget()
        self.plot_widget = PlotterWidget()

        # Connect signals
        self.input_widget.functions_updated.connect(self.plot_widget.plot_functions)

        main_layout.addWidget(self.input_widget, 1)
        main_layout.addWidget(self.plot_widget, 2)
        self.setMinimumSize(800, 600)

    def load_styles(self):
        """
            Loads the application styles from a QSS (Qt Style Sheet) file and applies them to the window.
        """
        style_file_path = Path(__file__).parent.parent / "gui/styles/main.qss"
        with open(style_file_path, 'r') as f:
            self.setStyleSheet(f.read())

    def setup_window_icon(self):
        """
            Sets the window icon using an image loaded from the application's resources.
        """
        app_icon = ResourceUtils.load_icon('main_icon.png')
        self.setWindowIcon(app_icon)
