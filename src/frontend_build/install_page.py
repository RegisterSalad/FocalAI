from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame, QWidget, QSizePolicy, QListWidget, QTextEdit, QMessageBox
from PySide6.QtCore import Qt, QThread, QEventLoop
from PySide6.QtWebEngineWidgets import QWebEngineView  # Import QWebEngineView
import markdown
import sys
import os
from PySide6.QtGui import QIcon
from typing import Callable
import subprocess
import json

# Working dir imports
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

def run_environment_command(widget, worker_name, command: str, error_message: str) -> bool:
        # Create the worker and thread
        worker = Worker(worker_name, command, error_message)
        thread = QThread()
        loop = QEventLoop()  # Event loop to wait for completion

        # Move the worker to the thread and connect signals
        worker.moveToThread(thread)
        worker.output.connect(widget.update_progress_widget)
        thread.started.connect(worker.run_command)

        # Use the finished signal to quit the loop and capture the success flag
        success_flag = [False]  # Use a mutable type to capture the success flag

        def on_finished(success):
            success_flag[0] = success
            loop.quit()

        worker.finished.connect(on_finished)

        # Cleanup
        worker.finished.connect(thread.quit)
        worker.finished.connect(worker.deleteLater)
        thread.finished.connect(thread.deleteLater)

        # Start the thread and the event loop
        thread.start()
        loop.exec()  # This will block until the worker emits `finished`

        # Keep a reference to avoid premature garbage collection
        widget._thread = thread
        widget._worker = worker

        return success_flag[0]

class InstallPage(QFrame):
    def __init__(self, styler, model_page, new_env: CondaEnvironment):
            super().__init__()
            self.model_page = model_page
            self.styler = styler
            self.new_env: CondaEnvironment = new_env
            self.install_commands_list = self.new_env.repository.install_commands
            self.db = self.model_page.db
            print(f"Old DB size: {self.db.count}")
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

        # Progress Widget initialization
        self.progress_widget = QTextEdit(self)
        self.progress_widget.setReadOnly(True)  # Make the progress widget read-only
        self.progress_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)  # Adjust size policy

        # Add the progress widget to the layout
        self.layout.addWidget(self.progress_widget)
        self.layout.addLayout(list_layout)
        self.layout.addWidget(self.run_button)
        self.layout.addLayout(button_layout)

        # Set the style as provided
        self.setStyleSheet("""
            QWidget {
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
            }
            QFrame {
                background-color: #F0F0F0;
                border-radius: 10px;
            }
            QLineEdit, QTextEdit {
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
        self.commands_to_run_list.append("pip install pyside6 pypandoc pdflatex pydantic")
        formatted_command = " && ".join(self.commands_to_run_list)

        # Environment creation (blocking)
        create_tuple = self.new_env.create()
        creation_success = run_environment_command(self, worker_name="create",command=create_tuple[0], error_message=create_tuple[1])
        if not creation_success:
            print("Env Creation failed")
            return  # Stop further execution if environment creation fails

        # Execute other commands (asynchronously or with a blocking pattern if necessary)
        call_tuple = self.new_env(formatted_command)
        print(call_tuple)
        if run_environment_command(self, worker_name="call" ,command=call_tuple[0], error_message=call_tuple[1]):
            self.new_env.is_installed = True
            QMessageBox.information(self, "Success", f"Installation of {self.new_env.repository.repo_name} Successful!\nCheck log for details.")
            self.install_store()
                
            if not self.db.insert_environment(self.new_env):
                QMessageBox.warning(self, f"Failure", "Installation failed, aborting.")
                self._premature_delete()
        else:
            self._premature_delete()
        print(f"New DB size: {self.db.count}")

    def _premature_delete(self) -> None:

        delete_tuple = self.new_env.delete()
        print(f"Environment Deleted: {run_environment_command(self, worker_name="delete", command=delete_tuple[0], error_message=delete_tuple[1])}")

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

    def update_progress_widget(self, text: str):
            # Append text to the progress_widget, ensuring thread safety
        self.progress_widget.append(text)
    
    def install_store(self):
        #stores the all model information like description, name, url, model type in a .JSON
        repo: Repository = self.new_env.repository
        file = f"{repo.repo_name}.json"
        modelInfo = {
            "name":repo.repo_name,
            "url":repo.repo_url,
            "Model type": repo.get_model_type()
        }
        with open(file, "w") as outfile:
            json.dump(modelInfo, outfile)

    def remove_json(self):
        jsonfile = f"{self.new_env.repository.repo_name}.json"
        os.remove(jsonfile)
