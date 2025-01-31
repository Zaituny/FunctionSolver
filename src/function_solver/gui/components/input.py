from typing import Dict, List

from PySide2.QtWidgets import (QFrame, QVBoxLayout, QLabel, QLineEdit,
                               QPushButton, QMessageBox)
from PySide2.QtCore import Signal
from src.function_solver.core.expression_parser import ExpressionParser


class InputWidget(QFrame):
    """
        A custom widget for inputting and validating mathematical functions. This widget provides
        input fields for two functions, validates them using the `ExpressionParser`, and emits
        a signal when the functions are valid and ready to be processed.

        Attributes:
            functions_updated (Signal): A PySide2 signal that emits the validated function strings.
    """
    functions_updated = Signal(str, str)  # Signal for function1, function2

    def __init__(self):
        """
            Initializes the InputWidget. This sets up the user interface and initializes the expression parser.
        """
        super().__init__()
        self.setup_ui()
        self.parser = ExpressionParser()

    def setup_ui(self):
        """
            Sets up the user interface for the InputWidget. This includes creating input fields for
            two functions, a button to trigger validation, and labels for displaying errors.
        """
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        # Title
        input_label = QLabel("Input Functions")
        input_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #2c3e50;")
        layout.addWidget(input_label)

        # Function 1 input
        self.func1_frame = self.create_function_input("Function 1:", "e.g., x^2")
        layout.addWidget(self.func1_frame)

        # Function 2 input
        self.func2_frame = self.create_function_input("Function 2:", "e.g., log(x)")
        layout.addWidget(self.func2_frame)

        # Plot button
        self.plot_button = QPushButton("Plot Functions")
        self.plot_button.clicked.connect(self.validate_and_emit)
        layout.addWidget(self.plot_button)
        layout.addStretch()

    @staticmethod
    def create_function_input(label_text: str,
                              placeholder: str
                              ) -> QFrame:
        """
            Creates a frame containing an input field for a function, along with a label and an error message label.

            :param label_text: The text to display as the label for the input field.
            :param placeholder: The placeholder text to display in the input field.
            :return: A QFrame containing the input field, label, and error message label.
        """
        frame = QFrame()
        frame.setStyleSheet("background-color: #f8f9fa; padding: 10px;")
        layout = QVBoxLayout(frame)

        layout.addWidget(QLabel(label_text))
        input_field = QLineEdit()
        input_field.setPlaceholderText(placeholder)
        layout.addWidget(input_field)

        error_label = QLabel()
        error_label.setStyleSheet("color: #dc3545; font-size: 12px;")
        error_label.hide()
        layout.addWidget(error_label)

        return frame

    def validate_and_emit(self):
        """
            Validates the input functions and emits the `functions_updated` signal if they are valid.
            If the functions are invalid, an error message is displayed.
        """
        f1_text = self.func1_frame.findChild(QLineEdit).text().strip()
        f2_text = self.func2_frame.findChild(QLineEdit).text().strip()

        if not f1_text or not f2_text:
            QMessageBox.critical(self, "Input Error", "Please enter both functions.")
            return

        f1_validation = self.parser.validate(f1_text)
        f2_validation = self.parser.validate(f2_text)

        if f1_validation['is_valid'] and f2_validation['is_valid']:
            self.functions_updated.emit(f1_text, f2_text)
        else:
            self.show_validation_errors(f1_validation, f2_validation)

    def show_validation_errors(self,
                               f1_validation: Dict[str, any],
                               f2_validation: Dict[str, any]
                               ) -> None:
        """
            Displays validation errors for the input functions.

            :param f1_validation: The validation result for function 1.
            :param f2_validation: The validation result for function 2.
        """
        error_messages = []
        if not f1_validation['is_valid']:
            error_messages.append(f"Function 1: {self.format_error_message(f1_validation['errors'])}")
        if not f2_validation['is_valid']:
            error_messages.append(f"Function 2: {self.format_error_message(f2_validation['errors'])}")
        QMessageBox.critical(self, "Validation Error", "\n\n".join(error_messages))
    @staticmethod
    def format_error_message(errors: List[str]
                             ) -> str:
        """
            Formats error messages for display in the UI.

            :param errors: A list of error messages to format.
            :return: A formatted string containing the error messages.
        """
        if not errors:
            return ""

        error_translations = {
            "Invalid character": "contains an invalid character",
            "Syntax error at end": "is incomplete",
            "Syntax error at": "has a syntax error near"
        }

        formatted_errors = []
        for error in errors:
            for key, value in error_translations.items():
                if key in error:
                    if "'" in error:
                        problematic_part = error.split("'")[1]
                        formatted_errors.append(f"Expression {value} '{problematic_part}'")
                    else:
                        formatted_errors.append(f"Expression {value}")
                    break
            else:
                formatted_errors.append(error)

        return "\n".join(formatted_errors)