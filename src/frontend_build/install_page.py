from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame, QWidget, QSizePolicy, QListWidget, QTextEdit, QMessageBox
from PySide6.QtCore import Qt, QThread, QEventLoop
from PySide6.QtWebEngineWidgets import QWebEngineView  # Import QWebEngineView
import markdown
import sys
import os
from PySide6.QtGui import QIcon, QFont
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
from directories import REPO_JSONS_DIR
from conda_env import CondaEnvironment
from repo import Repository

def run_environment_command(widget, worker_name, command: str, error_message: str) -> bool:
    """
    Executes a specified command in a separate thread and updates the widget based on the command's success or failure.

    Args:
        widget (QWidget): The widget that will display progress and receive updates.
        worker_name (str): A name identifier for the worker thread.
        command (str): The command to be executed by the worker.
        error_message (str): A message to display if the command execution fails.

    Returns:
        bool: True if the command execution was successful, False otherwise.
    """
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
    """
    A page in the GUI that handles the installation of a new conda environment and the management of installation commands.

    Attributes:
        styler (Styler): An instance of the Styler class used to apply UI styles.
        parent (QWidget): The parent widget, typically the main model page.
        new_env (CondaEnvironment): An instance representing the new conda environment being managed.
    """
    
    def __init__(self, styler, parent, new_env: CondaEnvironment):

            """
        Initialize the InstallPage with the parent widget, the styler, and the new environment.

        Args:
            styler (Styler): The styler object to apply UI styles.
            parent (QWidget): The parent widget.
            new_env (CondaEnvironment): The new conda environment to be installed.
        """
            super().__init__(parent)
            self.model_page = parent
            self.styler = styler
            self.new_env: CondaEnvironment = new_env
            self.install_commands_list = self.new_env.repository.install_commands
            self.db = self.model_page.db
            print(f"Old DB size: {self.db.count}")
            self.command_count = len(self.install_commands_list)
            self.commands_to_run_set = set()  # It seems you wanted to use a set, but it's not used later in your code.
            self.commands_to_run_list = []  # Initialize the list for commands to run.
            self.new_env.is_installed = False
            self.init_ui()
            

    def init_ui(self):
        """Set up the user interface for the installation page."""
        self.layout = QVBoxLayout(self)

        # Install Commands List
        self.install_commands_subwidget = QListWidget()
        self.install_commands_subwidget.addItems(self.install_commands_list)

        # Commands to Run List
        self.commands_to_run_subwidget = QListWidget()


        # Horizontal layout for buttons
        button_subayout = QHBoxLayout()
        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.change_to_main_model_page)
        button_subayout.addWidget(self.back_button)

        # Create the labels for each section
        self.button_label = QLabel("Interaction Buttons")
        self.install_commands_label = QLabel("Install Commands")
        self.commands_to_run_label = QLabel("Commands to Run")

        font = QFont('Arial', 18)
        font.setBold(True)  # Make the font bold

        # Apply the font to the label
        self.button_label.setFont(font)
        self.install_commands_label.setFont(font)
        self.commands_to_run_label.setFont(font)

        # Create holder layouts for install commands and run commands to hold widget and label
        self.install_commands_main_layout = QVBoxLayout()
        self.commands_to_run_layout = QVBoxLayout()

        # Install and To run holder widgets
        self.install_commands_widget = QWidget()
        self.install_commands_widget.setLayout(self.install_commands_main_layout)
        self.commands_to_run_widget = QWidget()
        self.commands_to_run_widget.setLayout(self.commands_to_run_layout)

        # Add labels to widgets
        self.install_commands_main_layout.addWidget(self.install_commands_label)
        self.install_commands_main_layout.addWidget(self.install_commands_subwidget)

        self.commands_to_run_layout.addWidget(self.commands_to_run_label)
        self.commands_to_run_layout.addWidget(self.commands_to_run_subwidget)
        # Buttons for adding/removing commands
        self.add_button = QPushButton("Add >>")
        self.add_button.clicked.connect(self.add_command_to_run)
        self.run_button = QPushButton("Run Selected Commands")
        self.run_button.clicked.connect(self.run_selected_commands)

        self.clear_button = QPushButton("Clear Commands")
        self.clear_button.clicked.connect(self.clear_commands_to_run)

        buttons_main_layout = QVBoxLayout()
        buttons_main_layout.addWidget(self.button_label)
        buttons_main_layout.addWidget(self.add_button)
        buttons_main_layout.addWidget(self.clear_button) 

        # Layout for lists and buttons
        list_layout = QHBoxLayout()
        list_layout.addWidget(self.install_commands_widget)
        list_layout.addLayout(buttons_main_layout)
        list_layout.addWidget(self.commands_to_run_widget)

        # Progress Widget initialization
        self.progress_subwidget = QTextEdit(self)
        self.progress_subwidget.setPlaceholderText("Progress Display, Installation output will show up here")
        self.progress_subwidget.setReadOnly(True)  # Make the progress widget read-only
        self.progress_subwidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)  # Adjust size policy

        # Create a widget for the progress window and label
        self.progress_label = QLabel("Progress Window")
        self.progress_widget = QWidget()
        self.progress_holder_layout = QVBoxLayout()
        self.progress_holder_layout.addWidget(self.progress_label)
        self.progress_holder_layout.addWidget(self.progress_subwidget)
        self.progress_widget.setLayout(self.progress_holder_layout)

        # Add the progress widget to the layout
        self.layout.addWidget(self.progress_widget)
        self.layout.addLayout(list_layout)
        self.layout.addWidget(self.run_button)
        self.layout.addLayout(button_subayout)

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
        QListWidget {
            background-color: #FFFFFF;
            border: 2px solid #cccccc;
            border-radius: 10px;
            padding: 5px;
            color: #333333;
        }
    """)


    def add_command_to_run(self):
        """
        Add selected commands from the install commands list to the commands to run list.
        Ensures that no duplicates are added.
        """
        selected_items = self.install_commands_subwidget.selectedItems()
        if not selected_items:
            return
        for item in selected_items:
            # Avoid adding duplicates
            if item.text() not in self.commands_to_run_list:
                self.commands_to_run_list.append(item.text())
                self.commands_to_run_subwidget.addItem(item.text())

    def run_selected_commands(self):
        """
        Execute the selected commands necessary for installing the new environment.
        Handles command execution and updates the installation status.
        """
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
        """
        Deletes the currently managed conda environment prematurely if installation fails.
        This method handles the cleanup process by deleting the environment and outputs the success status.
        """
        delete_tuple = self.new_env.delete()
        delete_succes = run_environment_command(self, worker_name="delete", command=delete_tuple[0], error_message=delete_tuple[1])
        print(f"Environment Deleted: {delete_succes}")

    def clear_commands_to_run(self):
        """
        Clears all commands from the 'commands to run' list and the associated UI list widget.
        This method is used to reset the command selection interface.
        """

        self.commands_to_run_list.clear()
        self.commands_to_run_subwidget.clear()

    def hide_all(self) -> None:
        """
        Hides all child widgets and the frame itself. This method is useful for toggling the visibility of the entire installation interface.
        """
        # Hide all child widgets
        for i in range(self.layout.count()):
            item = self.layout.itemAt(i)
            widget = item.widget()
            if widget is not None:
                widget.hide()

        # Hide the frame itself
        self.hide()

    def show_all(self) -> None:
        """
        Shows all child widgets and the frame itself, restoring the visibility of the installation interface after being hidden.
        """
        # Show all child widgets
        for i in range(self.layout.count()):
            item = self.layout.itemAt(i)
            widget = item.widget()
            if widget is not None:
                widget.show()

        # Show the frame itself
        self.show()

    def change_to_main_model_page(self):
        """
        Transitions from the installation page back to the main model page.
        It hides the current installation UI and shows the main model management UI.
        """
        self.hide_all()
        self.remove_from_layout()
        #self.model_page.show_all()
        if self.model_page:
                self.model_page.show_all()  # Ensure model_page is visible

    def remove_from_layout(self):
        """
        Removes the widget from its parent's layout. This is typically called when the widget needs to be completely removed from view.
        This method also ensures that the widget is hidden after removal from the layout.
        """
        #print("Parent:", self.parent())
        #print("Parent's Layout:", self.parent().layout() if self.parent() else "No parent")
        if self.parent() and self.parent().layout():
            layout = self.parent().layout()
            layout.removeWidget(self)
            layout.update()

        self.hide()

    def set_new_environment(self, new_env):
        """
        Sets a new conda environment to be managed by this installation page.

        Args:
        new_env (CondaEnvironment): The new environment configuration to set.
        """
        self.new_env = new_env
        self.update_install_commands()

    def update_install_commands(self): 
        """
        Updates the list of install commands based on the new environment's configuration.
        This is particularly useful when switching to manage a different conda environment.
        """
        self.install_commands_subwidget.clear()
        self.install_commands_list = self.new_env.repository.install_commands
        self.install_commands_subwidget.addItems(self.install_commands_list)

    
    def update_progress_widget(self, text: str):
        """
        Appends text to the progress widget, which displays ongoing processes or results.

        Args:
        text (str): The text to be appended to the progress widget. This text typically includes command outputs or status updates.
        """
        
        # Append text to the progress_widget, ensuring thread safety
        self.progress_subwidget.append(text)
    
    def install_store(self):
        """
        Stores all relevant model information in a JSON file. This includes the model's description, name, URL, type, and owner.

        The stored JSON file facilitates later retrieval and management of installed models.
        """
        
        #stores the all model information like description, name, url, model type in a .JSON
        repo: Repository = self.new_env.repository
        file = os.path.join(REPO_JSONS_DIR, f"{repo.repo_name}.json")
        modelInfo = {
            "name":repo.repo_name,
            "url":repo.repo_url,
            "model_type": repo.model_type,
            "description": repo.description,
            "owner": repo.owner
        }
        with open(file, "w") as outfile:
            json.dump(modelInfo, outfile)

    def remove_json(self):
        """
        Attempts to remove the JSON file associated with the environment's repository.
        This method is typically called when uninstalling a model or cleaning up resources.
        """
        repo: Repository = self.new_env.repository
        file = os.path.join(REPO_JSONS_DIR, f"{repo.repo_name}.json")
        try:
            os.remove(file)
        except:
            print("Couldn't remove " + file)
