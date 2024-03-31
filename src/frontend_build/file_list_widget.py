import os
import shutil
from PySide6.QtWidgets import QListWidget, QMessageBox

class FileListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.folder_path = os.path.join(os.path.dirname(__file__), 'stored_files')
        self.ensure_folder_exists(self.folder_path)
        self.populate_initial_list()

    def ensure_folder_exists(self, folder_path):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

    def add_file(self, file_path):
        try:
            dest_path = os.path.join(self.folder_path, os.path.basename(file_path))
            shutil.copy(file_path, dest_path)
            self.addItem(dest_path)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not add file: {e}")

    def populate_initial_list(self):
        for file_name in os.listdir(self.folder_path):
            self.addItem(os.path.join(self.folder_path, file_name))
        # In FileListWidget class

    def update_file_list(self, file_paths):
        for file_path in file_paths:
            self.add_file(file_path)  # Assuming add_file is your method for adding items