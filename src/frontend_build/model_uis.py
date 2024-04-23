from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame, QWidget, QSizePolicy, QListWidget, QTextEdit, QLineEdit, QApplication
from PySide6.QtCore import Qt, QThread, QEventLoop, QObject, Signal
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtGui import QPixmap, QImage
import sys
import os
from PySide6.QtGui import QIcon
from typing import Callable
import subprocess
import shutil


DRAG_N_DROP_DIR = os.getcwd() + "/app/temp/drag_n_drop"

# Used for UI 
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



class LLMPlayer(QWidget):
    """
    A graphical user interface component that serves as a chat interface for interacting with a language model (LLM).
    It allows for sending prompts to the LLM and displays the model's responses.

    Attributes:
        chatDisplay (QTextEdit): Displays the chat history and responses from the LLM.
        textEntry (QLineEdit): Allows the user to type and send messages to the LLM.
    """
    def __init__(self):
        """
        Initializes the LLMPlayer by setting up the UI components and layout.
        """
        super().__init__()
        self.initUI()

    def initUI(self):
        """
        Sets up the user interface of the LLMPlayer, including the chat display area and text entry field. 
        Configures the layout and styles necessary for the interface.
        """
        
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
        """
        Captures text from the text entry field when the user presses Enter, sends it to the LLM, and displays the response.
        Clears the text entry field after sending the message.
        """
        userText = self.textEntry.text()
        self.displayMessage(userText, "user")
        self.textEntry.clear()

        # Send prompt to LLM and get response
        llmResponse = "Just need to connect the LLM now"
        self.displayMessage(llmResponse, "llm")

    def displayMessage(self, message, sender):
        """
        Formats and displays a message in the chat display area with a specific style based on the sender.

        Args:
            message (str): The message text to display.
            sender (str): The sender of the message, which can be either 'user' or 'llm'. This parameter affects the styling of the message.
        """
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

class FileDropWidget(QWidget):
    """
    A widget that allows files to be dragged and dropped onto it, handling file input operations dynamically.

    Attributes:
        filesDropped (Signal): A signal emitted when a file is successfully dropped onto the widget.
    """
    filesDropped = Signal(str)
    def __init__(self):
        """
        Initializes the user interface of the file drop widget, including setting up styles and dimensions.
        """
        super().__init__()
        self.setAcceptDrops(True)
        self.init_ui()
        self.stored_files_folder = DRAG_N_DROP_DIR
        os.makedirs(self.stored_files_folder, exist_ok=True)

    def init_ui(self):
        """
        Sets up the user interface elements of the FileDropWidget, including the layout and styling. It configures a label to indicate that files can be dragged and dropped here.
        """
        
        self.setMinimumSize(400, 200)
        self.setStyleSheet(global_style)
        layout = QVBoxLayout()
        self.label = QLabel("Drag and drop files here")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("color: #888888; font-style: italic;")
        layout.addWidget(self.label)
        layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(layout)

    def dragEnterEvent(self, event):
        """
        Handles the event where a drag operation enters the widget area. If the event contains URLs (files), it accepts the drag operation to allow for a drop.

        Args:
            event (QDragEnterEvent): The event triggered by dragging something into the widget.
        """
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.label.setStyleSheet("color: #555555; font-style: normal;")

    def dropEvent(self, event):
        """
        Handles the event where files are dropped onto the widget. It processes the first file dropped, copies it to a designated folder, and emits a signal with the file's destination path.

        Args:
            event (QDropEvent): The event triggered by dropping files onto the widget.

        Emits:
            filesDropped: Signal emitted with the path of the file successfully dropped and copied.
        """
        
        mime_data = event.mimeData()
        if mime_data.hasUrls():
            first_file_url = mime_data.urls()[0]
            if first_file_url.isLocalFile():
                src_path = first_file_url.toLocalFile()
                if os.path.isfile(src_path):
                    file_name = os.path.basename(src_path)
                    dest_path = os.path.join(self.stored_files_folder, file_name)
                    try:
                        shutil.rmtree(self.stored_files_folder)
                        os.makedirs(self.stored_files_folder, exist_ok=True)
                        shutil.copy(src_path, dest_path)
                        self.label.setText(file_name)
                        self.label.setStyleSheet("color: #000000; font-style: normal;")
                        self.filesDropped.emit(dest_path)
                    except Exception as e:
                        self.error_message(f"Could not copy file: {e}")

    def error_message(self, message):
        """
        Displays an error message on the widget and prints the error to the console.

        Args:
            message (str): The error message to display and log.
        """
        
        self.label.setText("Error occurred! Check console.")
        self.label.setStyleSheet("color: #ff0000; font-style: normal;")
        print(message)

class DragAndDropPlayer(QWidget):
    """
    A specialized widget designed to handle file drag-and-drop interactions for specific model types.
    This widget can process and display outputs based on the type of model specified (e.g., ASR for audio recognition, OBJ for object detection).

    Attributes:
        model_type (str): Indicates the type of model the player is intended to work with, such as 'ASR' or 'OBJ'.
        inputReceived (Signal): A signal emitted when a file is successfully dropped and processed, carrying the file's path as data.
    """

    inputReceived = Signal(str)
    def __init__(self, model_type: str):
        """
        Initializes the DragAndDropPlayer with a specified model type.

        Args:
            model_type (str): The type of model the player is designed to interact with.
        """
        
        super().__init__()
        self.model_type = model_type
        self.initUI()

    def initUI(self):
        """
        Sets up the user interface components, including a file drop widget, output display widget, and a progress widget.
        Configures the layout based on the specified model type.
        """
        
        self.setWindowTitle(f"{self.model_type} Player")
        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)

        self.fileDropWidget = FileDropWidget()
        self.fileDropWidget.filesDropped.connect(self.handleFileDropped)  # Connect the signal

        self.progressWidget = QTextEdit(readOnly=True)
        self.progressWidget.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)

        if self.model_type == "ASR":
            self.outputWidget = self._get_text_output_widget()
        elif self.model_type == "OBJ":
            self.outputWidget = self._get_image_output_widget()
        else:
            self.outputWidget = QLabel("No output available for this model type")
            self.outputWidget.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.mainLayout.addWidget(self.fileDropWidget)
        self.mainLayout.addWidget(self.outputWidget)
        self.mainLayout.addWidget(self.progressWidget)

    def handleFileDropped(self, file_path):
        """
        Processes the dropped file based on the model type. It checks the file extension to ensure it's appropriate for the model.

        Args:
            file_path (str): The path to the file that was dropped.
        """
        
        if self.model_type == "ASR":
            valid_extensions = ('.mp3', '.wav', '.aac', '.flac')

            # Check if result_path has a valid audio file extension
            if file_path.endswith(valid_extensions):
                self.inputReceived.emit(file_path)
        elif self.model_type == "OBJ":
            result_path: str = self.parent_page.input_path
            valid_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')

            # Check if result_path has a valid image file extension
            if result_path.endswith(valid_extensions):
                self.inputReceived.emit(file_path)

    def displayOutput(self, output) -> None:
        """
        Display output in the UI based on its type. It can either be raw text from an ASR classifier
        or image data from an OBJ classifier respectively.

        Parameters:
            output (str or QImage): The output from the classifier to be displayed. If the output is a string,
                                    it's treated as text from ASR. If it's a QImage, it's treated as image data from OBJ.
        """
        if isinstance(output, str):  # Check if the output is text
            self.outputWidget.setText(output)
            self.outputWidget.setReadOnly(True)  # Ensure the widget is read-only if it's a text widget
        elif isinstance(output, QImage):  # Check if the output is an image
            pixmap = QPixmap.fromImage(output)
            self.outputWidget.setPixmap(pixmap)  # Display the image in a QLabel
            self.outputWidget.setAlignment(Qt.AlignCenter)
        else:
            self.outputWidget.setText("Unsupported output type")

    def _get_text_output_widget(self):
        """
        Creates and returns a QTextEdit widget configured to display text output.

        Returns:
            QTextEdit: A read-only text editor widget for displaying text output.
        """
        
        textOutput = QTextEdit()
        textOutput.setReadOnly(True)
        return textOutput

    def _get_image_output_widget(self):

        """
        Creates and returns a QLabel widget configured to display image output.

        Returns:
            QLabel: A label widget configured to display images.
        """
        imgOutput = QLabel("Image will appear here")
        imgOutput.setAlignment(Qt.AlignmentFlag.AlignCenter)
        imgOutput.setStyleSheet("border: 1px solid black; min-height: 200px;")
        return imgOutput

class DefaultPlayer(QWidget):
    def __init__(self) -> None:
        raise NotImplementedError

class FileDropWidget(QWidget):
    """A widget that supports dragging and dropping files into it.
    
    Attributes:
        filesDropped (Signal): Custom signal that emits the path of the dropped file.
    """
    
    
    filesDropped = Signal(str)  # Signal to emit when files have been dropped

    def __init__(self):
        """Initialize the FileDropWidget with drag and drop enabled."""
        super().__init__()
        self.setAcceptDrops(True)
        self.init_ui()

    def init_ui(self):
        """Set up the user interface of the widget."""
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
        """Handle the event when a drag action enters the widget."""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.label.setStyleSheet("color: #555555; font-style: normal;")

    def dropEvent(self, event):
        """Handle the event when files are dropped onto the widget."""
        mime_data = event.mimeData()
        if mime_data.hasUrls():
            # Consider only the first file from the drop
            first_file_url = mime_data.urls()[0]
            if first_file_url.isLocalFile():
                src_path = first_file_url.toLocalFile()
                if os.path.isfile(src_path):  # Check if it's a file not a directory
                    file_name = os.path.basename(src_path)
                    dest_path = os.path.join(DRAG_N_DROP_DIR, file_name)

                    # Clear existing files in the directory
                    for existing_file in os.listdir(DRAG_N_DROP_DIR):
                        os.remove(os.path.join(DRAG_N_DROP_DIR, existing_file))

                    # Copy the new file
                    try:
                        shutil.copy(src_path, dest_path)
                        self.label.setText(file_name)  # Update label to show copied file
                        self.label.setStyleSheet("color: #000000; font-style: normal;")
                        self.filesDropped.emit(dest_path)  # Emit signal with path of copied file
                    except Exception as e:
                        print(f"Could not copy file {src_path} to {dest_path}: {e}")

