# This Python file uses the following encoding: utf-8

# Importing necessary modules
import sys  # Importing sys module for system-related functionalities
from PySide6.QtWidgets import QApplication, QMainWindow  # Importing necessary PySide6 modules
from ui_form import Ui_MainWindow  # Importing the user interface class
import os

# Calculate the path to the directory containing database.py
module_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if module_dir not in sys.path:
    sys.path.append(module_dir)

# Defining the main window class
class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()  # Creating an instance of the user interface class
        self.ui.setupUi(self)  # Setting up the user interface in the main window

        # Connecting button clicks to respective functions
        self.ui.pushButton.clicked.connect(self.switch_to_page1)  # Connecting pushButton click to switch_to_page1 function
        self.ui.pushButton_2.clicked.connect(self.switch_to_page2)  # Connecting pushButton_2 click to switch_to_page2 function
        self.ui.pushButton_3.clicked.connect(self.switch_to_page3)  # Connecting pushButton_3 click to switch_to_page3 function

        self.ui.actionOpen_Dock.triggered.connect(self.openDock)

    def openDock(self):
        self.ui.dockWidget.show()

    # Function to switch to page 1
    def switch_to_page1(self):
        self.ui.stackedWidget.setCurrentIndex(0)  # Setting the index of stackedWidget to 0 (page 1)

    # Function to switch to page 2
    def switch_to_page2(self):
        self.ui.stackedWidget.setCurrentIndex(1)  # Setting the index of stackedWidget to 1 (page 2)

    # Function to switch to page 3
    def switch_to_page3(self):
        self.ui.stackedWidget.setCurrentIndex(2)  # Setting the index of stackedWidget to 2 (page 3)



# Entry point of the program
if __name__ == "__main__":
    app = QApplication(sys.argv)  # Creating an instance of QApplication
    widget = MainWindow()  # Creating an instance of MainWindow class
    widget.show()  # Displaying the main window
    sys.exit(app.exec())  # Executing the application and exiting when done
