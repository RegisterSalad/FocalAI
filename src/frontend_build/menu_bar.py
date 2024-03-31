from PySide6.QtWidgets import QMenuBar
import sys
import os
import shutil
from PySide6.QtWidgets import QMenuBar, QMessageBox

module_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if module_dir not in sys.path:
    sys.path.append(module_dir)

class MenuBar(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        #self.file_list_widget = parent.file_list_widget  # Assuming the parent passes a reference to the FileListWidget
        self.init_ui()

    def init_ui(self):
        # Terminal selection menu
        terminal_menu = self.addMenu("Terminal Selection")
        terminal_menu.addAction("Bash")
        terminal_menu.addAction("Zsh")
        terminal_menu.addAction("PowerShell")
        terminal_menu.addAction("Anaconda Prompt")

        # File list widget options menu
        file_menu = self.addMenu("File List Options")
        clear_action = file_menu.addAction("Clear stored_files folder")
        clear_action.triggered.connect(self.clear_stored_files_folder)

    def clear_stored_files_folder(self):
        stored_files_folder = os.path.join(os.getcwd(), 'stored_files')  # Adjust path as necessary

        # Confirm action
        reply = QMessageBox.question(self, 'Clear Folder', 'Are you sure you want to clear all files in the stored_files folder?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            for filename in os.listdir(stored_files_folder):
                file_path = os.path.join(stored_files_folder, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    QMessageBox.critical(self, 'Error', f'Failed to delete {filename}: {e}')
                    return

            # Update the FileListWidget if available
            if self.file_list_widget:
                self.file_list_widget.clear()  # Clear the list in the UI

