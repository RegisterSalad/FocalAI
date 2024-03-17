# This Python file uses the following encoding: utf-8

# Importing necessary modules
import sys  # Importing sys module for system-related functionalities
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QFileDialog  # Importing necessary PySide6 modules
from PySide6 import *
from ui_form import Ui_MainWindow  # Importing the user interface class
import os

# Calculate the path to the directory containing database.py
module_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if module_dir not in sys.path:
    sys.path.append(module_dir)

# Defining the main window class
class MainWindow(QMainWindow):
    fname = None
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()  # Creating an instance of the user interface class
        self.ui.setupUi(self)  # Setting up the user interface in the main window

        # Connecting button clicks to respective functions
        self.ui.pushButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))  # Connecting pushButton click to switch_to_page1 function
        self.ui.pushButton_2.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))  # Connecting pushButton_2 click to switch_to_page2 function
        self.ui.pushButton_3.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(2))  # Connecting pushButton_3 click to switch_to_page3 function
        self.ui.pushButton_5.clicked.connect(self.nothing)
        self.ui.fileList.findChild(QLabel, "fileList")


        self.ui.actionOpen_Dock.triggered.connect(lambda: self.ui.dockWidget.show())

    def nothing(self):
        pass

    def list_file(self, fname):
        fName = QFileDialog.getOpenFileName(self, "File Opener", "", "All Files (*)") #(self, title, specify starting directory, filter file formats) [ex: any(*);;python(*.py)]
        if fName:
            self.ui.fileList.setText(str(fName))


# Entry point of the program
if __name__ == "__main__":
    app = QApplication(sys.argv)  # Creating an instance of QApplication
    widget = MainWindow()  # Creating an instance of MainWindow class
    widget.show()  # Displaying the main window
    sys.exit(app.exec())  # Executing the application and exiting when done
