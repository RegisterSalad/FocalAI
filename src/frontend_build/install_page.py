from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame, QWidget, QSizePolicy, QListWidget
from PySide6.QtCore import Qt
from PySide6.QtWebEngineWidgets import QWebEngineView  # Import QWebEngineView
import markdown
import sys
import os
from PySide6.QtGui import QIcon
from typing import Callable
import subprocess



# Working dir imports
from model_player import ModelPlayer
from styler import Styler

# Calculate the path to the directory containing
module_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if module_dir not in sys.path:
    sys.path.append(module_dir)

# Project imports
from conda_env import CondaEnvironment
from repo import Repository
from database import DatabaseManager

class InstallPage(QFrame):
    def __init__(self, styler, model_page, install_commands: list[str]):
            super().__init__()
            self.model_page = model_page
            self.styler = styler
            self.install_commands_list = install_commands
            print(self.install_commands_list)
            self.command_count = len(self.install_commands_list)
            self.commands_to_run_set = set()  # It seems you wanted to use a set, but it's not used later in your code.
            self.commands_to_run_list = []  # Initialize the list for commands to run.
            self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)

        # Install Commands List
        self.install_commands_widget = QListWidget()
        self.install_commands_widget.addItems(self.install_commands_list)

        # Commands to Run List
        self.commands_to_run_widget = QListWidget()

        # Horizontal layout for buttons
        button_layout = QHBoxLayout()
        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.change_to_main_model_page)
        button_layout.addWidget(self.back_button)

        # Add the button layout to the main layout
        
        # Buttons for adding/removing commands
        self.add_button = QPushButton("Add >>")
        self.add_button.clicked.connect(self.add_command_to_run)
        self.run_button = QPushButton("Run Selected Commands")
        self.run_button.clicked.connect(self.run_selected_commands)

        # Layout for lists and buttons
        list_layout = QHBoxLayout()
        list_layout.addWidget(self.install_commands_widget)
        list_layout.addWidget(self.add_button)
        list_layout.addWidget(self.commands_to_run_widget)

        self.layout.addLayout(list_layout)
        self.layout.addWidget(self.run_button)
        self.layout.addLayout(button_layout)

    def add_command_to_run(self):
        selected_items = self.install_commands_widget.selectedItems()
        if not selected_items:
            return
        for item in selected_items:
            # Avoid adding duplicates
            if item.text() not in self.commands_to_run_list:
                self.commands_to_run_list.append(item.text())
                self.commands_to_run_widget.addItem(item.text())

    def run_selected_commands(self):
        # for command in self.commands_to_run_list:
        # # Prepend the command with 'bash -c' to ensure it runs in bash
        #     bash_command = f"bash -c \"{command}\""
        #     try:
        #         # Use shell=True to run the command through the shell
        #         subprocess.run(bash_command, shell=True, check=True)
        #     except subprocess.CalledProcessError as e:
        #         print(f"Error running command '{command}': {e}")
        print("Commands to run:", self.commands_to_run_list)

    
    def hide_all(self) -> None:
        # Hide all child widgets
        for i in range(self.layout.count()):
            item = self.layout.itemAt(i)
            widget = item.widget()
            if widget is not None:
                widget.hide()

    # Hide the frame itself
        self.hide()

    def show_all(self) -> None:
        # Show all child widgets
        for i in range(self.layout.count()):
            item = self.layout.itemAt(i)
            widget = item.widget()
            if widget is not None:
                widget.show()

        # Show the frame itself
        self.show()

    

    def change_to_main_model_page(self):
        self.hide_all()
        self.model_page.show_all()














