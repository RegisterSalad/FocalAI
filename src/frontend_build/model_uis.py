from PySide6.QtWidgets import (QWidget, QVBoxLayout, QTextEdit, QLineEdit)
from PySide6.QtCore import QObject, Signal, QCoreApplication
from menu_bar import MenuBar
import os
import sys

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
        self.llm = None
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
                font-size: 14px;
                margin: 4px 2px;
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