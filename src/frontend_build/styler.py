from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QLineEdit, QListWidget, QPushButton,
                               QLabel, QStackedWidget, QFrame, QSizePolicy, QMenu, QTextBrowser, QTextEdit)
from PySide6.QtGui import QAction, QGuiApplication, QPalette, QColor
from PySide6.QtCore import Slot, Qt, QCoreApplication

class Styler:
    def __init__(self):
        self.dark_mode_enabled = False
        self.components = []

    def register_component(self, component):
        self.components.append(component)
        component.update_style()

    def toggle_dark_mode(self):
        self.dark_mode_enabled = not self.dark_mode_enabled
        app = QApplication.instance()
        palette = QPalette()

        if self.dark_mode_enabled:
            # Configure palette for dark mode
            palette.setColor(QPalette.Window, QColor(53, 53, 53))
            palette.setColor(QPalette.WindowText, Qt.white)
            palette.setColor(QPalette.Base, QColor(25, 25, 25))
            palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
            palette.setColor(QPalette.Text, Qt.white)
            palette.setColor(QPalette.Button, QColor(53, 53, 53))
            palette.setColor(QPalette.ButtonText, Qt.white)
            palette.setColor(QPalette.Link, QColor(42, 130, 218))
            palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
            palette.setColor(QPalette.HighlightedText, Qt.black)
        else:
            # Reset to default palette
            palette = app.style().standardPalette()

        app.setPalette(palette)
        self.update_styles()

    def update_styles(self):
        for component in self.components:
            component.update_style()