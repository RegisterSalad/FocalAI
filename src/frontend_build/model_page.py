from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame, QSizePolicy, QWidget, QListWidget, QListWidgetItem, QToolTip, QTextEdit, QLineEdit, QInputDialog
from PySide6.QtCore import Qt
from PySide6.QtWebEngineWidgets import QWebEngineView  # Import QWebEngineView
import markdown
import sys
import os
from PySide6.QtGui import QIcon

# Working dir imports
from model_player import ModelPlayer
from styler import Styler
from install_page import InstallPage
from GPT_caller import GPTCaller

# Calculate the path to the directory containing
module_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if module_dir not in sys.path:
    sys.path.append(module_dir)

# Project imports
from repo import Repository
from database import DatabaseManager

class GPTPlayer(QWidget):
    def __init__(self, documentation):
        super().__init__()
        self.GPT = GPTCaller(documentation)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("ChatGPT Assisstant")
        
        # Set the style as provided
        # Updated style settings without 'display' and 'cursor' properties
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
                background-color: #700F2A;
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
                background-color: #700F5A;
            }
        """)

        # Chat display area
        self.chatDisplay = QTextEdit()
        self.chatDisplay.setReadOnly(True)

        # Layout for chat display
        layout = QVBoxLayout()
        layout.addWidget(self.chatDisplay)

        # Creating and adding buttons dynamically
        buttonLabels = ['Make Sample Code', 'Find The Models Parameters', 'Find The Models Datasets', 'Find Additional Model Content', 'Write A Report On The Model', 'Delete Current API Key']
        self.buttonsLayout = QVBoxLayout()  # Layout for buttons

        for label in buttonLabels:
            button = QPushButton(label)
            button.clicked.connect(self.buttonClicked)  # Connect the clicked signal to a slot
            self.buttonsLayout.addWidget(button)

        layout.addLayout(self.buttonsLayout)  # Add the buttons layout to the main layout
        
        self.setLayout(layout)
        self.displayMessage("Please Note: the API calls may take a few seconds to respond", "GPT")

    def buttonClicked(self):
        sender = self.sender()
        response: str
        
        if sender.text() == 'Make Sample Code':
            response = self.GPT.make_sample_code()

        elif sender.text() == 'Find The Models Parameters':
            response = self.GPT.find_model_parameters()

        elif sender.text() == 'Find The Models Datasets':
            response = self.GPT.find_model_datasets()

        elif sender.text() == 'Find Additional Model Content':
            response = self.GPT.find_model_content()

        elif sender.text() == 'Write A Report On The Model':
            response = self.GPT.write_model_report()

        elif sender.text() == 'Delete Current API Key':
            response = self.GPT.delete_api_key()

        self.displayMessage(response, sender)


    def displayMessage(self, message, sender):
        # Check the sender and format the message accordingly
        if sender == "user":
            message_html = f"""
            <div style='margin: 10px; padding: 10px; border-radius: 10px; border-top: 1px solid #ddd; border-bottom: 1px solid #ddd;'>
                <b style='color: #007ACC;'>User:</b>
                <p style='color: #333;'>{message}</p>
            </div>
            """
        else:  # sender is gpt response
            message_html = f"""
            <div style='margin: 10px; padding: 10px; border-radius: 10px; border-top: 1px solid #ddd; border-bottom: 1px solid #ddd;'>
                <b style='color: #CC7A00; font-family: Consolas;'>GPT:</b>
                <p style='color: #333; font-family: Consolas;'>{message}</p>
            </div>
            """

        # Insert the formatted message HTML
        self.chatDisplay.insertHtml(message_html)
        self.chatDisplay.insertPlainText("\n\n")  # Ensure there's a double new line after the div
        self.chatDisplay.ensureCursorVisible()  # Auto-scroll to the latest message

class ModelPage(QFrame):
    def __init__(self, styler: Styler):
        super().__init__()
        self.install_page: InstallPage | None = None
        self.styler = styler
        self.init_ui()

    def init_ui(self) -> None:
        self.html_text: str | None = None
        self.css = self.styler.doc_css
        self.button1 = QPushButton("Model Player")
        self.button2 = QPushButton("Download Model")
        self.button3 = QPushButton("ChatGPT Window")
        self.text_display = QWebEngineView()  # Use QWebEngineView
        self.text_display.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.text_display.setZoomFactor(0.9)
        self.thumbnail = QLabel()
        self.thumbnail.setFixedSize(100, 100)
        
        mainLayout = QVBoxLayout()
        
        self.model_player = ModelPlayer()
        self.button1.clicked.connect(lambda: self.create_model_player())
        
        self.button2.clicked.connect(lambda: self.change_to_install_page())

        self.button3.clicked.connect(lambda: self.create_GPT_interface())
        
        buttonsLayout = QVBoxLayout()
        buttonsLayout.setAlignment(Qt.AlignRight | Qt.AlignTop)
        buttonsLayout.addWidget(self.button1)
        buttonsLayout.addWidget(self.button2)
        buttonsLayout.addWidget(self.button3)

        buttonsWrapperLayout = QHBoxLayout()
        buttonsWrapperLayout.addLayout(buttonsLayout)
        buttonsWrapperLayout.addStretch()

        mainLayout.addWidget(self.thumbnail)
        mainLayout.addLayout(buttonsWrapperLayout)
        mainLayout.addWidget(self.text_display)

        self.setLayout(mainLayout)

        self.styler.register_component(self)
        self.styler.style_me()

        # Initially hide buttons
        self.button1.hide()
        self.button2.hide()
        self.button3.hide()
        

    def display_pop_up(self):
        self.pop_up_window.show()
    
    def get_repo(self, repo_url: str) -> Repository:
        return Repository(repo_url)
    
    def create_GPT_interface(self):
        print("GPT window")
        self.GPT_Window = GPTPlayer(self.repository.repo_url)
        self.GPT_Window.show()


    def create_model_player(self):
        print("Creating New Window")
        # Set the window to always stay on top when it's first opened
        self.model_player.setWindowFlags(self.model_player.windowFlags() | Qt.WindowStaysOnTopHint)
        self.model_player.show()
        self.model_player.raise_()
        self.model_player.activateWindow()
        # Remove the always-on-top flag after it's displayed and focused
        self.model_player.setWindowFlags(self.model_player.windowFlags() & ~Qt.WindowStaysOnTopHint)
        # You need to call show() again after changing window flags
        self.model_player.show()
    
    def hide_all(self) -> None:
        layout = self.layout()  # Get the layout of the frame
        self.button1.hide()
        self.button2.hide()
        self.button3.hide()
        if layout is not None:
            for i in range(layout.count()):  
                item = layout.itemAt(i)
                widget = item.widget()
                if widget is not None and widget != self.install_page:  # Check if the widget is not self.install_page
                    widget.setDisabled(True)
                    widget.hide()  # Hide the widget

    def show_all(self) -> None:
        layout = self.layout()  # Get the layout of the frame
        if layout is not None:
            for i in range(layout.count()):  
                item = layout.itemAt(i)
                widget = item.widget()
                if widget is not None:  # Check if the item is a widget
                    widget.setEnabled(True)
                    widget.show()  # Show the widget

    def change_to_install_page(self):
        self.hide_all()
        self.install_page = InstallPage(self.styler, self, self.repository.install_commands)
        self.layout().addWidget(self.install_page)
        self.install_page.show_all()

    def convert_to_markdown(self, name: str) -> str:
        content = getattr(self.repository, name, None)
        
        if content:
            markdown_text = content
            self.html_text = markdown.markdown(markdown_text, extensions=['tables', 'fenced_code', 'codehilite', 'extra'])

            self.html_text = f"<style>{self.css}</style>{self.html_text}"
            
            return self.html_text

    def update_content(self, repo_url: str | None) -> None:
        # Show buttons when content is updated
        if repo_url is None:
            if self.html_text is None:
                self.html_text = markdown.markdown("  ", extensions=['tables', 'fenced_code', 'codehilite', 'extra'])
            
            self.html_text = f"<style>{self.css}</style>{self.html_text}"
            self.text_display.setHtml(self.html_text)  # Set HTML content
            return
            
        self.button1.show()
        self.button2.show()
        self.button3.show()    
        self.repository = self.get_repo(repo_url)
        self.text_display.setHtml(self.convert_to_markdown('readme_content'))  # Set HTML content

    def update_style(self):
        if self.styler.dark_mode_enabled:
            self.setStyleSheet("background-color: #333333; color: white;")
            # Update styles for QWebEngineView if necessary
            self.thumbnail.setStyleSheet("background-color: gray;")
        else:
            self.setStyleSheet("background-color: lightgray; color: black;")
            # Update styles for QWebEngineView if necessary
            self.thumbnail.setStyleSheet("background-color: lightgray;")
        self.css = self.styler.doc_css
        self.update_content(repo_url=None)
