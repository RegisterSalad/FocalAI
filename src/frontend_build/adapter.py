from typing import Callable
from model_player import ModelPlayer
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

from database import DatabaseManager
from conda_env import CondaEnvironment
    
class Adapter(QWidget):
    """
    This adapter will speak to the pages in order to pass the AI model input and get display the AI model output
    """
    def __init__(self, name: str = "") -> None:
        self.db = DatabaseManager("databases/conda_environments.db")
        self.running_env = self.db.get_environment_by_name
    
    def get_model_input(self, model_type: str | None = None) -> Callable:
        """
        Configures the model_page to the right model type and makes the input of the model come from the drag on drop

        Args:
            - model_type: str | None ; Model type string. Options are "ASR", "OBJ", and "LLM"
        
        Returns:
            - False if model_type is not supported
            - True if pipe is successful
        """

        if model_type == "ASR":
            return self._asr_inteface() 
        elif model_type == "OBJ":
            return self._obj_interface()
        elif model_type == "LLM":
            return self._llm_interface()            
        else:
            return self._default_interface()
        
    def _asr_interface(self) -> str | None:
        """
        Fetches the file from the drag-and-drop, checks its type to make sure
        it is a valid audio file, and returns the path if valid.

        Returns:
            str | None: Path of the input audio file (from drag-and-drop) if valid,
                        None otherwise.
        """
        result_path: str = self.parent_page.input_path
        valid_extensions = ('.mp3', '.wav', '.aac', '.flac')

        # Check if result_path has a valid audio file extension
        if result_path.endswith(valid_extensions):
            return result_path  # Return path if it's a valid audio file
        
        return None  # Return None if the file is not a valid audio file
    
    def _obj_interface(self) -> str | None: # Utilizes ModelPlayer
        """
        Fetches the file from the drag-and-drop, checks its type to make sure
        it is a valid image file, and returns the path if valid.

        Returns:
            str | None: Path of the input image file (from drag-and-drop) if valid,
                        None otherwise.
        """
        result_path: str = self.parent_page.input_path
        valid_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')

        # Check if result_path has a valid image file extension
        if result_path.endswith(valid_extensions):
            return result_path  # Return path if it's a valid image file
        
        return None  # Return None if the file is not a valid image file

    def _llm_interface(self):
        pass

    def show(self) -> None:
        pass