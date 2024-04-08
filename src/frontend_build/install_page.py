from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame, QWidget, QSizePolicy, QListWidget
from PySide6.QtCore import Qt, QThread
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
from worker import Worker
# Calculate the path to the directory containing
module_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if module_dir not in sys.path:
    sys.path.append(module_dir)

# Project imports
from conda_env import CondaEnvironment
from repo import Repository
from database import DatabaseManager

class InstallPage(QFrame):
    def __init__(self, styler, model_page, new_env: CondaEnvironment):
            super().__init__()
            self.model_page = model_page
            self.styler = styler
            self.new_env: CondaEnvironment = new_env
            self.install_commands_list = self.new_env.repository.install_commands
            self.db = DatabaseManager("databases/conda_environments.db")
            print(self.install_commands_list)
            self.command_count = len(self.install_commands_list)
            self.commands_to_run_set = set()  # It seems you wanted to use a set, but it's not used later in your code.
            self.commands_to_run_list = []  # Initialize the list for commands to run.
            self.init_ui()

    def run_conda_command(self, command_name, *args):
        """
        Args:
        - command_name: Is the name of the subprocess method that the worker will wrap around
            valid options are:
                - __call__(command: str) -> bool: Executes a given command within the conda environment.
                - __str__() -> str: Returns a string representation of the CondaEnvironment object.
                - create() -> bool: Creates the conda environment based on the provided specifications.
                - delete() -> bool: Deletes the specified conda environment.
                - conda_init() -> bool: Initializes the conda command line environment setup.

        - *args: Any arguments for the method
        """
        # Create a worker and thread
        self.thread = QThread()
        self.worker = Worker(self.new_env, command_name, *args)
        
        # Move the worker to the thread and connect signals
        self.worker.moveToThread(self.thread)
        self.worker.finished.connect(self.thread.quit)
        self.worker.output.connect(self.update_progress_widget)
        
        # Start the thread
        self.thread.started.connect(self.worker.run)
        self.thread.start()

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
        print(f"Running {self.commands_to_run_list}")
        formatted_command = " && ".join(self.commands_to_run_list)
        if not self.new_env.create(): # This is using __create__ modify accordingly
            print("Env Creation failed")
        if self.new_env(formatted_command): # This runs the commands with logging, this is using __call__, modify accordingly
            self.db.insert_environment(self.new_env)
        else:
            print(f"Environment Deleted: {self.new_env.delete()}")

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

# This is NOT the main application