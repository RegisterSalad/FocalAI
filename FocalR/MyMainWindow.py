# This Python file uses the following encoding: utf-8
"""
from PyQt6 import QtCore
from PyQt6 import QtWidgets
from PyQt6 import QtQuick
import sys


class MyMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        #Load the UI File
        self.ui_file_path = 'path
"""
# python_script.py
import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.uic import loadUi  # Import the loadUi function from PyQt6.uic

class MyMainWindow(QMainWindow):
    def __init__(self, ui_file_path):
        super().__init__()

        # Load the UI file
        self.ui_file_path = ui_file_path
        self.load_ui()

    def load_ui(self):
        # Load the UI file using PyQt6
        loadUi(self.ui_file_path, self)

        # Connect widgets to functions
        self.addLineEdit.textChanged.connect(self.calculate_sum)

    def calculate_sum(self, text):
        # Get values from input line edits
        add_value = int(text) if text.isdigit() else 0

        # Perform addition
        result = add_value + 10  # Example addition, modify as needed

        # Update the output line edit
        self.sumLineEdit.setText(str(result))

if __name__ == "__main__":
    # Get the current directory of the Python script
    script_directory = os.path.dirname(os.path.abspath(__file__))

    # Specify the name of your UI file
    ui_file_name = 'mainwindow.ui'  # Replace with the actual name of your UI file

    # Join the script directory and the UI file name to get the full path
    ui_file_path = os.path.join(script_directory, ui_file_name)

    # Create the application and main window with the dynamically determined UI file path
    app = QApplication(sys.argv)
    main_window = MyMainWindow(ui_file_path)
    main_window.show()
    sys.exit(app.exec())
