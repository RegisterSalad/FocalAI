from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame, QWidget, QSizePolicy, QListWidget, QTextEdit, QLineEdit, QApplication
from PySide6.QtCore import Qt, QThread, QEventLoop, QObject, Signal
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtGui import QPixmap, QImage
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
    def __init__(self):
        super().__init__()
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

class FileDropWidget(QWidget):
    filesDropped = Signal(str)

    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.init_ui()
        self.stored_files_folder = os.path.join(os.getcwd(), 'stored_files')
        os.makedirs(self.stored_files_folder, exist_ok=True)

    def init_ui(self):
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
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.label.setStyleSheet("color: #555555; font-style: normal;")

    def dropEvent(self, event):
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
        self.label.setText("Error occurred! Check console.")
        self.label.setStyleSheet("color: #ff0000; font-style: normal;")
        print(message)

class DragAndDropPlayer(QWidget):
    def __init__(self, model_type: str):
        super().__init__()
        self.initUI()
        self.inputReceived = Signal(str)
        self.model_type = model_type

    def initUI(self):
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
        textOutput = QTextEdit()
        textOutput.setReadOnly(True)
        return textOutput

    def _get_image_output_widget(self):
        imgOutput = QLabel("Image will appear here")
        imgOutput.setAlignment(Qt.AlignmentFlag.AlignCenter)
        imgOutput.setStyleSheet("border: 1px solid black; min-height: 200px;")
        return imgOutput

class DefaultPlayer(QWidget):
    pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = DragAndDropPlayer(model_type="ASR")
    player.show()
    sys.exit(app.exec())

