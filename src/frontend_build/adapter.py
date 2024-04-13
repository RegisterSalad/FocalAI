import os
import sys
module_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if module_dir not in sys.path:
    sys.path.append(module_dir)

from typing import Callable
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QApplication,
                               QHBoxLayout, QLabel, QFrame, QSizePolicy, QTextEdit, QLineEdit)
from PySide6.QtCore import QObject, Signal, QCoreApplication
from PySide6.QtGui import QFont
from menu_bar import MenuBar

from model_uis import LLMPlayer, DragAndDropPlayer, DefaultPlayer # Implemented elsewhere assume they only return values when the receive them from their user interaction widgets via a slot

from database import DatabaseManager
from conda_env import CondaEnvironment

class Adapter(QWidget):
    inputReady = Signal(str)  # Defines a signal to emit when input is ready

    def __init__(self, name: str | None = None) -> None:
        super().__init__()  # Initialize the QWidget base class
        db_path = os.path.abspath("databases/conda_environments.db")
        
        self.db = DatabaseManager(db_path)
        if not isinstance(name, str):
            raise TypeError(f"Adapter incorrectly initialized: Name cannot be of type [{type(name)}]")

        self.running_env = self.db.get_environment_by_name(name)
        if not isinstance(self.running_env, CondaEnvironment):
            raise TypeError(f"Environment fetching unsuccessful, perhaps the name is incorrect? Name used for fetching: [{name}]")

        self.model_type = self.running_env.repository.model_type
        self.init_UI()

    def init_UI(self) -> None:
        self.model_input_widget_dict = {
            "ASR": DragAndDropPlayer(self.model_type),
            "OBJ": DragAndDropPlayer(self.model_type),
            "LLM": LLMPlayer(),
        }
        self.player = self.model_input_widget_dict.get(self.model_type, DefaultPlayer())
        self.mainLayout = QHBoxLayout()  # Correctly create an instance of QHBoxLayout
        if not isinstance(self.player, QWidget):
            raise TypeError("Model Player incorrectly initialized")
        self.player.inputReceived.connect(self.handle_input)
        self.mainLayout.addWidget(self.player)
        self.setLayout(self.mainLayout)  # Set the layout to the widget

    def handle_input(self, input_data):
        """Slot to handle input data from the player."""
        if isinstance(input_data, str):
            self.inputReady.emit(input_data)  # Emit the signal with the input data

    def display_output(self, output) -> None:
        self.player.displayOutput(output)


if __name__ == "__main__":
    app = QApplication(sys.argv)  # Create an application object for PyQt
    adapter_name = "whisper"  # You would replace this with a valid environment name
    adapter = Adapter(adapter_name)  # Create an instance of the Adapter with a specific name
    adapter.inputReady.connect(lambda x: print(f"Input received: {x}"))  # Connect to the inputReady signal
    x = None
    def remake_x(data):
        x = data
        adapter.display_output(x)  # Optionally, display some output

    sys.exit(app.exec())  # Start the event loop and exit the application appropriately