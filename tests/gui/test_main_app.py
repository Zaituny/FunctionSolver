import pytest
import threading
from PySide2.QtCore import Qt
from PySide2.QtTest import QTest
from PySide2.QtWidgets import QLineEdit, QApplication, QMessageBox
from PySide2 import QtCore
from matplotlib.backend_bases import MouseEvent
import numpy as np
from src.function_solver.gui.app import FunctionSolverWindow


@pytest.fixture
def app(qtbot):
    window = FunctionSolverWindow()
    qtbot.addWidget(window)
    return window


def close_window():
    message = QApplication.activeWindow()
    if isinstance(message, QMessageBox):
        closeButton = message.defaultButton()
        QTest.mouseClick(closeButton, Qt.LeftButton)


def test_initial_window_state(app):
    # test that the main app was initialized correctly
    assert app.input_widget is not None
    assert app.plot_widget is not None
    assert app.input_widget.func1_frame is not None
    assert app.input_widget.func2_frame is not None
    assert app.plot_widget.ax is not None
    assert app.plot_widget.canvas is not None


def test_plot_button_enabled(app):
    # test that the plot button is enabled by default
    assert app.input_widget.plot_button.isEnabled()


def test_input_fields(app, qtbot):
    # test that the input fields are empty by default
    assert app.input_widget.func1_frame.findChild(QLineEdit).text() == ""


def test_inputing_into_input_fields(app, qtbot):
    # test that the input fields can be typed into
    app.input_widget.func1_frame.findChild(QLineEdit).setText("x^2")
    app.input_widget.func2_frame.findChild(QLineEdit).setText("2*x")

    assert app.input_widget.func1_frame.findChild(QLineEdit).text() == "x^2"
    assert app.input_widget.func2_frame.findChild(QLineEdit).text() == "2*x"


def test_plot_functions(app, qtbot):
    # Enter valid functions
    app.input_widget.func1_frame.findChild(QLineEdit).setText("x^2")
    app.input_widget.func2_frame.findChild(QLineEdit).setText("2*x")

    # Click plot button
    qtbot.mouseClick(app.input_widget.plot_button, Qt.LeftButton)

    # Verify that the plot is created
    assert app.plot_widget.ax is not None
    assert len(app.plot_widget.ax.lines) == 2  # Two functions plotted


def test_plot_invalid_functions(app, qtbot):
    # Enter invalid functions
    app.input_widget.func1_frame.findChild(QLineEdit).setText("x^")
    app.input_widget.func2_frame.findChild(QLineEdit).setText("2*/x")

    # Click plot button
    qtbot.mouseClick(app.input_widget.plot_button, Qt.LeftButton)

    # Verify that no plot is created for invalid functions
    assert len(app.plot_widget.ax.lines) == 0


def move_mouse_to_data_point(canvas, ax, x, y):
    """
    Move mouse to a specific data point on a matplotlib canvas

    Args:
        canvas (FigureCanvas): The matplotlib canvas
        ax (Axes): The matplotlib axes
        x (float): x-coordinate of the data point
        y (float): y-coordinate of the data point
    """
    # get global coordinates of the data point
    x_px, y_px = ax.transData.transform([x, y]).ravel()
    # get bottom-left corner of the canvas
    # move mouse to the data point
    return QtCore.QPoint(x_px, canvas.height() - y_px)




# create end-to-end test for the app
def test_solving_and_plotting_and_showing_annotation(app, qtbot):
    # launch the app
    app.show()

    # Enter invalid functions with qtbot
    qtbot.keyClicks(app.input_widget.func1_frame.findChild(QLineEdit), "x^")
    qtbot.keyClicks(app.input_widget.func2_frame.findChild(QLineEdit), "2*/x")

    # schedule closing the message box
    threading.Timer(0.5, close_window).start()

    # Click plot button
    qtbot.mouseClick(app.input_widget.plot_button, Qt.LeftButton)

    # Verify that no plot is created for invalid functions
    assert len(app.plot_widget.ax.lines) == 0

    # clear the input fields
    app.input_widget.func1_frame.findChild(QLineEdit).clear()
    app.input_widget.func2_frame.findChild(QLineEdit).clear()

    # Enter valid functions
    qtbot.keyClicks(app.input_widget.func1_frame.findChild(QLineEdit), "x^2")
    qtbot.keyClicks(app.input_widget.func2_frame.findChild(QLineEdit), "2*x")

    # Click plot button
    qtbot.mouseClick(app.input_widget.plot_button, Qt.LeftButton)

    # Verify that the plot is created
    assert app.plot_widget.ax is not None
    assert len(app.plot_widget.ax.lines) == 2  # Two functions plotted

    qtbot.waitExposed(app.plot_widget.canvas)

    # hover over the point (0, 0) in FigureCanvas
    pos = move_mouse_to_data_point(app.plot_widget.canvas, app.plot_widget.ax, 0, 0)
    qtbot.mouseMove(app.plot_widget.canvas,
                     pos=pos)
    # send a mouse event to the canvas with hovering position
    event = MouseEvent(name='motion_notify_event',
                       canvas=app.plot_widget.canvas,
                       x=pos.x(),
                       y=app.plot_widget.canvas.height() - pos.y())
    app.plot_widget.canvas.callbacks.process('motion_notify_event', event)
    assert app.plot_widget.annotation is not None
    assert app.plot_widget.annotation.get_text() == "(0.0000, 0.0000)"
    assert app.plot_widget.annotation.get_visible()
    assert np.array_equal(app.plot_widget.annotation.xy, [0, 0])
    # hover over the point (2, 4) in FigureCanvas
    pos = move_mouse_to_data_point(app.plot_widget.canvas, app.plot_widget.ax, 2, 4)
    qtbot.mouseMove(app.plot_widget.canvas,
                     pos=pos)
    # send a mouse event to the canvas with hovering position
    event = MouseEvent(name='motion_notify_event',
                       canvas=app.plot_widget.canvas,
                       x=pos.x(),
                       y=app.plot_widget.canvas.height() - pos.y())
    app.plot_widget.canvas.callbacks.process('motion_notify_event', event)
    assert app.plot_widget.annotation is not None
    assert app.plot_widget.annotation.get_text() == "(2.0000, 4.0000)"
    assert app.plot_widget.annotation.get_visible()
    assert np.array_equal(app.plot_widget.annotation.xy, [2, 4])

