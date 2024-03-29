from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QLineEdit, QListWidget, QPushButton,
                               QLabel, QStackedWidget, QFrame, QSizePolicy, QMenu, QTextBrowser, QTextEdit)
from PySide6.QtGui import QAction, QGuiApplication, QPalette, QColor
from PySide6.QtCore import Slot, Qt, QCoreApplication
from pygments.formatters import HtmlFormatter

class Styler:
    def __init__(self):
        self.dark_mode_enabled = False
        self.components = []

    def style_me(self) -> None:
        for component in self.components:
            component.setStyleSheet(
                """
                QWidget {
                    border-radius: 5px;
                }
                QTextEdit, QLineEdit {
                    border-radius: 15px;
                    background-color: #f0f0f0;
                }"""
                                    )

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
    

    @property
    def doc_css(self) -> HtmlFormatter:
        # Common CSS for both dark and light modes
        css = HtmlFormatter().get_style_defs('.codehilite')
        css += """
        table {
            border-collapse: collapse;
            width: 100%;
        }
        th, td {
            border: 1px solid #dddddd;
            text-align: left;
            padding: 8px;
        }
        img {
            max-width: 50%;
            height: auto;
        }
        """
        
        # Conditional CSS for dark and light modes
        if self.dark_mode_enabled:  # Dark mode settings
            css += """
        body {
            background-color: #1e1e1e;
            color: white;
        }
        tr:nth-child(even) {
            background-color: #262626;
        }
        a {
            color: #add8e6;  # Light blue for better visibility in dark mode
        }
        pre {
            border: 1px solid #000000;
            color: #ffffff;
            font-size: 15px;
            line-height: 1.6;
            background-color: #181818
        }
            """
        else:  # Light mode settings
            css += """
        body {
            background-color: #f0f0f0;
            color: #333;
        }
        tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        a {
            color: purple;  # Default purple color for hyperlinks in light mode
        }
        pre {
            border: 1px solid #ffffff;
            color: #000000;
            font-size: 15px;
            line-height: 1.6;
        }
            """
        return css
