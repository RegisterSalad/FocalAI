from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QLineEdit, QListWidget, QPushButton,
                               QLabel, QStackedWidget, QFrame, QSizePolicy, QMenu, QTextBrowser, QTextEdit, QMenuBar)
from PySide6.QtWidgets import QMenu

from PySide6.QtGui import QAction, QGuiApplication, QPalette, QColor
from PySide6.QtCore import Slot, Qt, QCoreApplication
import sys

class MenuBar(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        terminal_menu = self.addMenu("Terminal Selection")
        bash_action = terminal_menu.addAction("Bash")
        zsh_action = terminal_menu.addAction("Zsh")
        powershell_action = terminal_menu.addAction("PowerShell")
        anaconda_action = terminal_menu.addAction("Anaconda Prompt")

        # Connect actions to slots if needed
