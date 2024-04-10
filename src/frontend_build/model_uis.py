from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame, QWidget, QSizePolicy, QListWidget, QTextEdit, QLineEdit
from PySide6.QtCore import Qt, QThread, QEventLoop, QObject, Signal
from PySide6.QtWebEngineWidgets import QWebEngineView  # Import QWebEngineView
import markdown
import sys
import os
from PySide6.QtGui import QIcon
from typing import Callable
import subprocess
import shutil

module_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if module_dir not in sys.path:
    sys.path.append(module_dir)

from database import DatabaseManager
from conda_env import CondaEnvironment
    
class Adapter(QWidget):
    """
    This adapter will interface with the pages to pass AI model input and display the AI model output.
    """
    # Signal to emit when the model output is ready to be displayed
    modelOutputReady = Signal(str)

    def __init__(self, model_type: str = "ASR", parent=None) -> None:
        super().__init__(parent=parent)
        self.model_type = model_type
        self.init_ui()

    def init_ui(self):
        """
        Initialize the UI based on the model type.
        """
        self.layout = QVBoxLayout()

        if self.model_type == "ASR":
            self.fileDropWidget = FileDropWidget()
            self.layout.addWidget(self.fileDropWidget)
            self.fileDropWidget.filesDropped.connect(self.set_model_output)
        elif self.model_type == "LLM":
            self.llmPlayer = LLMPlayer(self)
            self.layout.addWidget(self.llmPlayer)
            self.modelOutputReady.connect(self.llmPlayer.displayMessage)
        # Add additional UI initializations for other model types here

        self.setLayout(self.layout)

    def get_input_method(self, model_type: str) -> callable:
        """
        Return a callable based on the model type that gets the path of the audio file dropped.
        """
        if model_type == "ASR":
            return lambda: self.fileDropWidget.stored_files_folder
        # Define methods for other model types as needed

    def set_model_output(self, result: str) -> None:
        """
        Display the output from the AI model in the UI.
        """
        if self.model_type == "ASR":
            # For ASR, assume result is text to be displayed in a text widget
            print(result)  # Or update a UI element
        elif self.model_type == "LLM":
            self.modelOutputReady.emit(result)
        # Handle other model types as needed

global_style = """
            QWidget {
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
            }
            QMainWindow {
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
        """

class LLM(QObject):
    # Define a signal that can carry string messages
    sendMessage = Signal(str)

    def __init__(self):
        super().__init__()

    def process_request(self, request: str):
        # Dummy processing method
        print(f"Processing: {request}")
        # Emit a signal when processing is done
        self.sendMessage.emit(f"Processed: {request}")

class LLMPlayer(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent_widget = parent
        self.llm = LLM
        self.initUI()

    def initUI(self):
        self.setWindowTitle("LLM Player")
        
        # Set the style as provided
        self.setStyleSheet(global_style)

        # Chat display area
        self.chatDisplay = QTextEdit()
        self.chatDisplay.setReadOnly(True)

        # Text entry area
        self.textEntry = QLineEdit()
        self.textEntry.setPlaceholderText("Type your message...")
        self.textEntry.returnPressed.connect(self.sendPrompt)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.chatDisplay)
        layout.addWidget(self.textEntry)

        self.setLayout(layout)

    def sendPrompt(self):
        userText = self.textEntry.text()
        self.displayMessage(userText, "user")
        self.textEntry.clear()

        # Send prompt to LLM and get response
        llmResponse = "Just need to connect the LLM now"
        self.displayMessage(llmResponse, "llm")

    def displayMessage(self, message, sender):
        # Check the sender and format the message accordingly
        if sender == "user":
            message_html = f"""
            <div style='margin: 10px; padding: 10px; border-radius: 10px; border-top: 1px solid #ddd; border-bottom: 1px solid #ddd;'>
                <b style='color: #007ACC;'>User:</b>
                <p style='color: #333;'>{message}</p>
            </div>
            """
        else:  # sender is "llm"
            message_html = f"""
            <div style='margin: 10px; padding: 10px; border-radius: 10px; border-top: 1px solid #ddd; border-bottom: 1px solid #ddd;'>
                <b style='color: #CC7A00; font-family: Consolas;'>LLM:</b>
                <p style='color: #333; font-family: Consolas;'>{message}</p>
            </div>
            """

        # Insert the formatted message HTML
        self.chatDisplay.insertHtml(message_html)
        self.chatDisplay.insertPlainText("\n\n")  # Ensure there's a double new line after the div
        self.chatDisplay.ensureCursorVisible()  # Auto-scroll to the latest message

class Model(QObject):

    def __init__(self, model_type: str):
        self.type = model_type 
        super().__init__()

    def process_request(self, request: str):
        # Dummy processing method
        print(f"Processing: {request}")
        # Emit a signal when processing is done
        self.sendMessage.emit(f"Processed: {request}")

class DragAndDropPlayer(QWidget):
    def __init__(self, model_type: str):
        self.model_type = model_type
        # self.model = model
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("LLM Player")
        self.setStyleSheet(global_style)

        self.mainlayout = QVBoxLayout() 
        self.textOutput = QWidget(self)
        self.imgOutput = QWidget(self)

        # Progress Widget initialization
        self.progress_widget = QTextEdit(self)
        self.progress_widget.setReadOnly(True)  # Make the progress widget read-only
        self.progress_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)  # Adjust size policy

        ui_selector_dict = {"ASR": self.textOutput, "OBJ": self.imgOutput, "N/A": self.progress_widget }

        try:
            self.mainlayout.addWidget(ui_selector_dict[self.model.type])
        except Exception as e:
            print("Model object incorrect attribution")

class FileDropWidget(QWidget):
    filesDropped = Signal(str)  # Signal to emit when files have been dropped

    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.init_ui()
        self.stored_files_folder = os.path.join(os.getcwd(), 'stored_files')  # Path to the folder
        os.makedirs(self.stored_files_folder, exist_ok=True)  # Ensure the folder exists

    def init_ui(self):
        self.setMinimumSize(400, 200)
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
                border: 2px dashed #cccccc;
                border-radius: 10px;
            }
        """)

        layout = QVBoxLayout()
        self.label = QLabel("Drag and drop files here")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("color: #888888; font-style: italic;")
        layout.addWidget(self.label)
        layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(layout)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.label.setStyleSheet("color: #555555; font-style: normal;")

    def dropEvent(self, event):
        mime_data = event.mimeData()
        if mime_data.hasUrls():
            # Consider only the first file from the drop
            first_file_url = mime_data.urls()[0]
            if first_file_url.isLocalFile():
                src_path = first_file_url.toLocalFile()
                if os.path.isfile(src_path):  # Check if it's a file not a directory
                    file_name = os.path.basename(src_path)
                    dest_path = os.path.join(self.stored_files_folder, file_name)

                    # Clear existing files in the directory
                    for existing_file in os.listdir(self.stored_files_folder):
                        os.remove(os.path.join(self.stored_files_folder, existing_file))

                    # Copy the new file
                    try:
                        shutil.copy(src_path, dest_path)
                        self.label.setText(file_name)  # Update label to show copied file
                        self.label.setStyleSheet("color: #000000; font-style: normal;")
                        self.filesDropped.emit(dest_path)  # Emit signal with path of copied file
                    except Exception as e:
                        print(f"Could not copy file {src_path} to {dest_path}: {e}")
