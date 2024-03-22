from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QLineEdit, QListWidget, QPushButton,
                               QLabel, QStackedWidget, QFrame, QSizePolicy, QMenu, QTextBrowser, QTextEdit)
from PySide6.QtGui import QAction, QGuiApplication, QPalette, QColor
from PySide6.QtCore import Slot, Qt, QCoreApplication, QObject

from new_window import NewWindow

class NewWindowManager(QObject):
    def __init__(self):
        super().__init__()

    @Slot(str)
    def handle_content_change(self, content):
        # Extract the model name from the file path or content (or pass it separately)
        model_name = "Model Name"  # Example model name

        # Create and show the new window with the model name
        new_window = NewWindow(content)  # Pass the model name and content to the NewWindow constructor
        new_window.show()
