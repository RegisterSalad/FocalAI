from PySide6.QtWidgets import (QWidget, QVBoxLayout, QApplication,
                               QHBoxLayout, QLabel, QFrame, QSizePolicy, QTextEdit, QLineEdit)
from PySide6.QtCore import QObject, Signal, Qt 
from PySide6.QtGui import QFont
from file_drop_widget import FileDropWidget
from file_list_widget import FileListWidget
from menu_bar import MenuBar
from terminal_widget import TerminalWidget
import os
import sys

module_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if module_dir not in sys.path:
    sys.path.append(module_dir)

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


class ModelPlayer(QWidget):
    def __init__(self, model_type: str):
        super().__init__()
        self.model_type: str = model_type
        self.setWindowTitle("Model Player")
        self.init_styles()  # Initialize styles for the window
        self.file_list_widget = FileListWidget()
        self.file_drop_widget = FileDropWidget()
        self.input_path: str | None = None
        self.init_ui()  # Setup the UI components

    def init_styles(self):
        self.setStyleSheet("""
            QWidget {
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
            }
            QFrame {
                background-color: #F0F0F0;
                border-radius: 10px;
            }
            QLineEdit, QListWidget {
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
                display: inline-block;
                font-size: 14px;
                margin: 4px 2px;
                cursor: pointer;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)  # Add margins for padding around the layout
        layout.setSpacing(10)  # Add some spacing between widgets
        # Adding a menu bar
        self.menu_bar = MenuBar(self)
        self.menu_bar.setStyleSheet("""
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

        layout.setMenuBar(self.menu_bar)
        self.init_top_section(layout)
        self.init_bottom_section(layout)

        self.setLayout(layout)
        self.setGeometry(100, 100, 800, 600)  # Set the window geometry

    def init_top_section(self, main_layout):
        top_frame = QFrame()
        left_top_frame = QFrame()
        right_top_frame = QFrame()

        top_layout = QHBoxLayout()
        top_layout.setSpacing(10)  # Add spacing between left and right sections

        # Ensure this connection is correct, using file_drop_widget and file_list_widget
        self.file_drop_widget.filesDropped.connect(self.file_list_widget.update_file_list)
        self.file_drop_widget.filesDropped.connect(self.get_user_input)

        # Set the size policy and layout for the drop widget and list widget
        self.file_drop_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.file_drop_widget.setMaximumHeight(200)
        self.file_list_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        left_top_layout = QVBoxLayout(left_top_frame)
        left_top_layout.addWidget(self.file_drop_widget)
        left_top_layout.addWidget(self.file_list_widget)

        # Assuming self.list_widget is your QListWidget instance
        #file_list_widget.clear()

        # Terminal widget with minimum size policy
        terminal_widget = TerminalWidget()
        terminal_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        terminal_widget.setMinimumSize(200, 150)  # Set a minimum size for the terminal widget

        right_top_layout = QVBoxLayout(right_top_frame)
        right_top_layout.addWidget(terminal_widget)

        # Add left and right sections to the top layout
        top_layout.addWidget(left_top_frame)
        top_layout.addWidget(right_top_frame)
        top_frame.setLayout(top_layout)
        main_layout.addWidget(top_frame)
    
    def get_user_input(self, input_path: str) -> None:
        self.input_path = input_path

    def init_bottom_section(self, main_layout):
        bottom_frame = QFrame()
        bottom_layout = QVBoxLayout()

        # Bottom widget with minimum size policy
        bottom_widget = QLabel("This is the bottom frame")
        bottom_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        bottom_widget.setMinimumHeight(100)  # Set a minimum height for the bottom widget
        bottom_widget.setAlignment(Qt.AlignCenter)

        bottom_layout.addWidget(bottom_widget)
        bottom_frame.setLayout(bottom_layout)

        # Set the size policy for the bottom frame to expand
        bottom_frame.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        main_layout.addWidget(bottom_frame)


class LLMPlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.llm = LLM()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("LLM Player")
        
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
                display: inline-block;
                font-size: 14px;
                margin: 4px 2px;
                cursor: pointer;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

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





if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    player = LLMPlayer()
    player.show()
    sys.exit(app.exec())