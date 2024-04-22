from PySide6.QtWidgets import QMenuBar
import sys
import os
import shutil
from PySide6.QtWidgets import QMenuBar, QMessageBox
import textwrap
import os
import subprocess
from pathlib import Path
import pypandoc
#from pypandoc.pandoc_download import download_pandoc
import pdflatex

module_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if module_dir not in sys.path:
    sys.path.append(module_dir)

from directories import DRAG_N_DROP_DIR, REPORTS_DIR

class Logger:
    """
    A utility class for converting documents from one format to another using the Pandoc library.
    """
    def convert_md_to_pdf(self,input_file, output_file):
        """
        Converts a Markdown file to a PDF file using Pandoc.

        Args:
            input_file (str): The path to the Markdown file to be converted.
            output_file (str): The path where the resulting PDF file should be saved.

        Raises:
            RuntimeError: If the conversion fails due to an issue within Pandoc or the environment setup.
        """
       
        try:
            # Specify 'markdown' as the input format
            output = pypandoc.convert_file(input_file, 'pdf', format='markdown', outputfile=output_file)
            assert output == ""  # Output should be empty for PDF conversions
            print(f"Conversion successful: {input_file} to {output_file}")

        except RuntimeError as e:
            print(f"Error during conversion: {e}")

class MenuBar(QMenuBar):
    """
    Custom menu bar for an application that provides various menu items for terminal selection and file management.

    Attributes:
        file_list_widget (FileListWidget): A reference to a file list widget which can be used for updating or interacting with files.
    """
    def __init__(self, parent=None):
        """
        Initializes the menu bar with a parent widget.

        Args:
            parent (QWidget, optional): The parent widget to which this menu bar will belong.
        """
        super().__init__(parent)
        self.file_list_widget = parent.file_list_widget  # Assuming the parent passes a reference to the FileListWidget
        self.init_ui()

    def init_ui(self):
        """
        Initializes the user interface components of the menu bar, adding specific menus and configuring styles.
        """
        self.setStyleSheet("""
                QMenuBar {
                    background-color: #f0f0f0;
                    color: #333333;
                    border: 1px solid #cccccc;
                    border-radius: 10px;  /* Rounded corners for the menu bar */
                    padding: 2px;  /* Padding to ensure the border does not cut into the items */
                }
                QMenuBar::item {
                    background-color: #f0f0f0;
                    padding: 5px 10px;
                    border-radius: 5px;  /* Rounded corners for each menu item */
                }
                QMenuBar::item:selected { /* When selected using mouse or keyboard */
                    background-color: #a8a8a8;
                    border-radius: 5px;  /* Maintain rounded corners on selection */
                }
                QMenuBar::item:pressed {
                    background-color: #888888;
                    border-radius: 5px;  /* Maintain rounded corners when pressed */
                }
                QMenu {
                    background-color: #f0f0f0;
                    border: 1px solid #cccccc;
                    margin: 2px;  /* Some spacing around the menu */
                    border-radius: 5px;  /* Rounded corners for the dropdowns */
                }
                QMenu::item {
                    padding: 5px 25px;
                    border-radius: 5px;  /* Rounded corners for each menu item */
                }
                QMenu::item:selected {
                    background-color: #a8a8a8;
                    border-radius: 5px;  /* Maintain rounded corners on selection */
                }
            """)
        # Terminal selection menu
        terminal_menu = self.addMenu("Terminal Selection")
        terminal_menu.addAction("Bash")
        # terminal_menu.addAction("Zsh")
        # terminal_menu.addAction("PowerShell")
        terminal_menu.addAction("Anaconda Prompt")

        # File list widget options menu
        file_menu = self.addMenu("File List Options")
        clear_action = file_menu.addAction("Clear stored_files folder")
        clear_action.triggered.connect(self.clear_stored_files_folder)

    def clear_stored_files_folder(self):
        """
        Clears all files in the 'stored_files' folder, which is specified by the DRAG_N_DROP_DIR directory constant.
        This method includes a confirmation dialog and error handling for file deletions.
        """
        stored_files_folder = DRAG_N_DROP_DIR

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
                    return  # Exit if there's an error

            # Update the FileListWidget if available
            if self.file_list_widget:
                self.file_list_widget.refresh_list()  # Refresh the list in the UI to reflect the cleared folder

    def clip_my_output_placeholder(self):
        """
         convert an output log file from text to PDF
        
        """
        input_txt = "run_command_log_test.txt"
        output_pdf = "command_log.pdf"

        logger = Logger()
        logger.convert_md_to_pdf(input_txt , output_pdf)


