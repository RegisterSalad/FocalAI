from PySide6.QtWidgets import (QWidget, QVBoxLayout, QApplication,
                               QHBoxLayout, QLabel, QFrame, QSizePolicy, QTextEdit, QLineEdit)
from PySide6.QtCore import QObject, Signal, QCoreApplication
from PySide6.QtGui import QFont
from menu_bar import MenuBar
import os
import sys

module_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if module_dir not in sys.path:
    sys.path.append(module_dir)

from file_list_widget import FileListWidget
from file_drop_widget import FileDropWidget
from terminal_widget import TerminalWidget
from script_builder import ScriptBuilder

class ModelPlayer(QWidget):
    def __init__(self, parent=None):  # Changed parent default value to None
        super().__init__()
        self.model_type: str | None = None
        self.setWindowTitle("Model Player")
        self.file_list_widget = FileListWidget(parent=self)
        self.file_drop_widget = FileDropWidget()
        self.script_builder = ScriptBuilder(parent=self, running_env = parent.running_env)
        self.input_path: str | None = None
        self.init_styles()
        self.init_ui()

    def init_styles(self):
        self.setStyleSheet("""
            QWidget {
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
            }
            QFrame {
                background-color: #F0F0F0;
                border-radius: 10px;
            }
            QLineEdit, QListWidget {
                border: 2px solid #CCCCCC;
                border-radius: 5px;
                padding: 5px;
                background-color: white;
            }
            QLabel {
                color: #333333;
            }
            QPushButton {
                background-color: #4CAF50;
                border: none;
                color: white;
                padding: 10px 24px;
                text-align: center;
                text-decoration: none;
                font-size: 14px;
                margin: 4px 2px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

    def init_ui(self):
        main_layout = QHBoxLayout()  # Changed to QHBoxLayout
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)
        
        self.menu_bar = MenuBar(self)
        main_layout.setMenuBar(self.menu_bar)
        
        # Create a container for left side widgets
        left_side_layout = QVBoxLayout()
        self.init_left_section(left_side_layout)
        
        
        # Add left_side_layout and ScriptBuilder to the main layout
        left_side_container = QWidget()
        left_side_container.setLayout(left_side_layout)
        main_layout.addWidget(left_side_container)
        main_layout.addWidget(self.script_builder)
        
        self.setLayout(main_layout)
        #Initialize at full screen windowed
        screen = QCoreApplication.instance().primaryScreen()
        self.setGeometry(screen.geometry())

    def init_left_section(self, main_layout):
        left_section_layout = QVBoxLayout()
        
        # Combine file_drop_widget and file_list_widget into a vertical layout
        self.file_drop_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.file_drop_widget.setMaximumHeight(200)
        self.file_list_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        # Connect the file_drop_widget to the file_list_widget
        self.file_drop_widget.filesDropped.connect(self.file_list_widget.update_file_list)
        self.file_drop_widget.filesDropped.connect(self.get_user_input)

        # left_section_layout.addWidget(self.file_drop_widget)
        # left_section_layout.addWidget(self.file_list_widget)

        # Add the terminal_widget to the vertical layout
        terminal_widget = TerminalWidget()
        terminal_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        terminal_widget.setMinimumSize(200, 150)
        left_section_layout.addWidget(terminal_widget)


        # Progress Widget initialization
        self.progress_widget = QTextEdit(self)
        self.progress_widget.setReadOnly(True)  # Make the progress widget read-only
        self.progress_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)  # Adjust size policy

        # Add the progress widget to the layout
        left_section_layout.addWidget(self.progress_widget)

        left_section_container = QWidget()
        left_section_container.setLayout(left_section_layout)
        main_layout.addWidget(left_section_container)


    def get_user_input(self, input_path: str) -> None:
        self.input_path = input_path

    def update_progress_widget(self, text: str):
        # Append text to the progress_widget, ensuring thread safety
        self.progress_widget.append(text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = ModelPlayer()
    main_window.show()
    sys.exit(app.exec())