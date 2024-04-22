import os
import sys
import shutil
from PySide6.QtWidgets import QListWidget, QMessageBox

# Remove for final build
module_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if module_dir not in sys.path:
    sys.path.append(module_dir)

from directories import DRAG_N_DROP_DIR

class FileListWidget(QListWidget):
    """
    A widget that displays a list of files from a specified directory, allowing for file management within the widget.

    Attributes:
        folder_path (str): Path to the directory whose files are to be displayed and managed.
    """
    def __init__(self, parent=None):
        """
        Initializes the FileListWidget with a specific parent and sets up the directory from which files will be managed.

        Args:
            parent (QWidget, optional): Parent widget. Defaults to None.
        """
        super().__init__(parent)
        self.folder_path = DRAG_N_DROP_DIR
        self.ensure_folder_exists(self.folder_path)
        self.populate_initial_list()

    def ensure_folder_exists(self, folder_path):
        """
        Ensures that the specified folder exists. If it doesn't, the folder is created.

        Args:
            folder_path (str): Path to the directory to check and create if necessary.
        """
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

    def add_file(self, file_path):
        """
        Adds a file to the folder and the list widget if it does not already exist in the folder.

        Args:
            file_path (str): The path of the file to be added to the directory and list.

        Shows a warning if the file already exists and an error if the file could not be added.
        """
        basename = os.path.basename(file_path)
        dest_path = os.path.join(self.folder_path, basename)
        if os.path.exists(dest_path):
            QMessageBox.warning(self, "File Exists", f"A file named {basename} already exists.")
            return  # Exit the method to avoid overwriting the file and causing an error.
        try:
            shutil.copy(file_path, dest_path)
            self.addItem(basename)  # Changed to add just the file name, not the full path.
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not add file: {e}")


    def populate_initial_list(self):
        """
        Populates the list widget with file names from the directory.
        This method is called on initialization and when the list is refreshed.
        """
        for file_name in os.listdir(self.folder_path):
            self.addItem(os.path.join(self.folder_path, file_name))
        # In FileListWidget class

    def update_file_list(self, file_paths):
        """
        Updates the file list by adding new files from a list of file paths.

        Args:
            file_paths (list of str): Paths of the files to be added.
        """
        for file_path in file_paths:
            self.add_file(file_path)  # Assuming add_file is your method for adding items

    def refresh_list(self):
        """
        Clears and repopulates the file list to reflect the current state of the folder.
        """
        self.clear()  # Clear the current list
        self.populate_initial_list()  # Repopulate list based on the current folder content
