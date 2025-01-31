import sys
from PySide2.QtWidgets import QApplication
from src.function_solver.gui.app import FunctionSolverWindow


def main():
    app = QApplication(sys.argv)
    window = FunctionSolverWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
