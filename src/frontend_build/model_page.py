from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QLineEdit, QListWidget, QPushButton,
                               QLabel, QStackedWidget, QFrame, QSizePolicy, QMenu, QTextBrowser, QTextEdit)
from PySide6.QtGui import QAction, QGuiApplication, QPalette, QColor
from PySide6.QtCore import Slot, Qt, QCoreApplication
import sys
import markdown


class ModelPage(QFrame):
    def __init__(self, styler):
        super().__init__()
        self.styler = styler

        # Initialize all components used in update_style before registering with the styler
        self.button1 = QPushButton("Button 1")
        self.button2 = QPushButton("Button 2")
        self.button3 = QPushButton("Button 3")
        self.textDisplay = QTextBrowser()
        self.textDisplay.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.thumbnail = QLabel()
        self.thumbnail.setFixedSize(100, 100)

        mainLayout = QVBoxLayout()

        # Buttons layout
        buttonsLayout = QVBoxLayout()
        buttonsLayout.setAlignment(Qt.AlignRight | Qt.AlignTop)
        buttonsLayout.addWidget(self.button1)
        buttonsLayout.addWidget(self.button2)
        buttonsLayout.addWidget(self.button3)

        # Configure layouts and components
        buttonsWrapperLayout = QHBoxLayout()
        buttonsWrapperLayout.addLayout(buttonsLayout)
        buttonsWrapperLayout.addStretch()

        mainLayout.addWidget(self.thumbnail)
        mainLayout.addLayout(buttonsWrapperLayout)
        mainLayout.addWidget(self.textDisplay)

        self.setLayout(mainLayout)

        # Now that all attributes are defined, register this component with the styler
        self.styler.register_component(self)

    def update_content(self, item_id):
        def read_file(file_path):
            try:
                with open(file_path, 'r') as file:
                    content = file.read()
                    return content
            except FileNotFoundError:
                print("File not found.")
                return None

        file_path = "../../_assets/test_readme.md"
        file_content = read_file(file_path)

        markdownText = f"**Item {item_id}:**\n{file_content}"
        htmlText = markdown.markdown(markdownText, extensions=['tables'])
        self.textDisplay.setHtml(htmlText)

    def update_style(self):
        if self.styler.dark_mode_enabled:
            self.setStyleSheet("background-color: #333333; color: white;")
            self.textDisplay.setStyleSheet("""
                QTextBrowser { background-color: #333333; color: white; }
                a { color: red; }
            """)
            self.thumbnail.setStyleSheet("background-color: gray;")
        else:
            self.setStyleSheet("background-color: lightgray; color: black;")
            self.textDisplay.setStyleSheet("""
                QTextBrowser { background-color: lightgray; color: black; }
                a { color: red; }
            """)
            self.thumbnail.setStyleSheet("background-color: lightgray;")