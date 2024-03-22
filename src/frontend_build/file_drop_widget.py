from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QLineEdit, QListWidget, QPushButton,
                               QLabel, QStackedWidget, QFrame, QSizePolicy, QMenu, QTextBrowser, QTextEdit)
from PySide6.QtGui import QAction, QGuiApplication, QPalette, QColor
from PySide6.QtCore import Slot, Qt, QCoreApplication, Signal



class FileDropWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)  # Enable drag and drop functionality
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.label = QLabel("Drag and drop files here")
        layout.addWidget(self.label)
        self.setLayout(layout)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        mime_data = event.mimeData()
        if mime_data.hasUrls():
            file_paths = [url.toLocalFile() for url in mime_data.urls()]
            file_names = [path.split('/')[-1] for path in file_paths]  # Extract file names
            self.label.setText("\n".join(file_names))  # Display file names in the label

        
