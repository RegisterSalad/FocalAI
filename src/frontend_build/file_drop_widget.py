from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QLineEdit, QListWidget, QPushButton,
                               QLabel, QStackedWidget, QFrame, QSizePolicy, QMenu, QTextBrowser, QTextEdit)
from PySide6.QtGui import QAction, QGuiApplication, QPalette, QColor
from PySide6.QtCore import Slot, Qt, QCoreApplication, Signal



from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor

import os
import shutil
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QApplication
from PySide6.QtCore import Qt, QMimeData
from PySide6.QtGui import QDragEnterEvent, QDropEvent


class FileDropWidget(QWidget):
    filesDropped = Signal(list)  # Signal to emit when files have been dropped

    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.init_ui()
        self.stored_files_folder = os.path.join(os.getcwd(), 'stored_files')  # Path to the folder
        os.makedirs(self.stored_files_folder, exist_ok=True)  # Ensure the folder exists

    def init_ui(self):
        self.setMinimumSize(400, 200)
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
                border: 2px dashed #cccccc;
                border-radius: 10px;
            }
        """)

        layout = QVBoxLayout()
        self.label = QLabel("Drag and drop files here")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("color: #888888; font-style: italic;")
        layout.addWidget(self.label)
        layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(layout)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.label.setStyleSheet("color: #555555; font-style: normal;")

    def dropEvent(self, event):
        mime_data = event.mimeData()
        if mime_data.hasUrls():
            file_paths = [url.toLocalFile() for url in mime_data.urls()]  # Get the list of file paths
            copied_file_paths = []  # List to store paths of successfully copied files

            for src_path in file_paths:
                file_name = os.path.basename(src_path)
                dest_path = os.path.join(self.stored_files_folder, file_name)
                try:
                    shutil.copy(src_path, dest_path)  # Copy file to stored_files folder
                    copied_file_paths.append(dest_path)  # Add path of copied file
                except Exception as e:
                    print(f"Could not copy file {src_path} to {dest_path}: {e}")

            # Update label to show copied files and reset style
            self.label.setText("\n".join(os.path.basename(path) for path in copied_file_paths))
            self.label.setStyleSheet("color: #000000; font-style: normal;")
            self.filesDropped.emit(copied_file_paths)  # Emit signal with paths of copied files



# class FileDropWidget(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setAcceptDrops(True)  # Enable drag and drop functionality
#         self.init_ui()

#     def init_ui(self):
#         layout = QVBoxLayout()
#         self.label = QLabel("Drag and drop files here")
#         layout.addWidget(self.label)
#         self.setLayout(layout)

#     def dragEnterEvent(self, event):
#         if event.mimeData().hasUrls():
#             event.acceptProposedAction()

#     def dropEvent(self, event):
#         mime_data = event.mimeData()
#         if mime_data.hasUrls():
#             file_paths = [url.toLocalFile() for url in mime_data.urls()]
#             file_names = [path.split('/')[-1] for path in file_paths]  # Extract file names
#             self.label.setText("\n".join(file_names))  # Display file names in the label

        
