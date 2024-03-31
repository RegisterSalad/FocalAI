from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame, QSizePolicy
from PySide6.QtCore import Qt
from PySide6.QtWebEngineWidgets import QWebEngineView  # Import QWebEngineView
import markdown
import sys
import os

# Working dir imports
from model_player import ModelPlayer
from styler import Styler

# Calculate the path to the directory containing
module_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if module_dir not in sys.path:
    sys.path.append(module_dir)

# Project imports
from repo import Repository
from database import DatabaseManager

class ModelPage(QFrame):
    def __init__(self, styler: Styler):
        super().__init__()
        self.init_ui(styler)

    def init_ui(self, styler: Styler) -> None:
        self.styler = styler
        self.html_text: str | None = None
        self.css = self.styler.doc_css
        self.button1 = QPushButton("Model Player")
        self.button2 = QPushButton("Download Model")
        self.button3 = QPushButton("Famoose the Goose")
        self.textDisplay = QWebEngineView()  # Use QWebEngineView
        self.textDisplay.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.textDisplay.setZoomFactor(0.9)
        self.thumbnail = QLabel()
        self.thumbnail.setFixedSize(100, 100)

        mainLayout = QVBoxLayout()
        
        self.model_player = ModelPlayer()
        self.button1.clicked.connect(lambda: self.create_model_player())
        
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
        mainLayout.addWidget(self.textDisplay)

        self.setLayout(mainLayout)

        self.styler.register_component(self)
        self.styler.style_me()

    def display_pop_up(self):
        self.pop_up_window.show()
    
    def get_repo(self, repo_url: str) -> Repository:
        return Repository(repo_url)


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
    

    def update_content(self, repo_url: str | None)-> None:
        if repo_url is None:
            if self.html_text is None:
                self.html_text = markdown.markdown("  ", extensions=['tables', 'fenced_code', 'codehilite', 'extra'])
            
            self.html_text = f"<style>{self.css}</style>{self.html_text}"
            self.textDisplay.setHtml(self.html_text)  # Set HTML content
            return
        self.repository = self.get_repo(repo_url)
        install_commands = self.repository.install_commands

        if install_commands:
            markdown_text = install_commands
            self.html_text = markdown.markdown(markdown_text, extensions=['tables', 'fenced_code', 'codehilite', 'extra'])

            self.html_text = f"<style>{self.css}</style>{self.html_text}"
            
            self.textDisplay.setHtml(self.html_text)  # Set HTML content

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

class DownloadPlayer(QFrame):
    def __init__(self, styler, api_caller):
        super().__init__()
        self.init_ui(styler, api_caller)

    def init_ui(self, styler, api_caller) -> None:
        self.styler = styler
        self.html_text: str | None = None
        self.css = self.styler.doc_css
        self.caller = api_caller

        self.button1 = QPushButton("Model Player")
        self.button2 = QPushButton("Download Model")
        self.button3 = QPushButton("Famoose the Goose")
        self.textDisplay = QWebEngineView()  # Use QWebEngineView
        self.textDisplay.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.textDisplay.setZoomFactor(0.9)
        self.thumbnail = QLabel()
        self.thumbnail.setFixedSize(100, 100)

        mainLayout = QVBoxLayout()
        
        self.model_player = ModelPlayer()
        self.button1.clicked.connect(lambda: self.create_model_player())
        
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
        mainLayout.addWidget(self.textDisplay)

        self.setLayout(mainLayout)

        self.styler.register_component(self)
        self.styler.style_me()

    def display_pop_up(self):
        self.pop_up_window.show()
        
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
    

    def update_content(self, repo_url: str | None)-> None:
        if repo_url is None:
            if self.html_text is None:
                self.html_text = markdown.markdown("  ", extensions=['tables', 'fenced_code', 'codehilite', 'extra'])
            
            self.html_text = f"<style>{self.css}</style>{self.html_text}"
            self.textDisplay.setHtml(self.html_text)  # Set HTML content
            return

        readme = self.caller.get_readme_contents(repo_url=repo_url)

        if readme:
            markdown_text = readme
            self.html_text = markdown.markdown(markdown_text, extensions=['tables', 'fenced_code', 'codehilite', 'extra'])

            self.html_text = f"<style>{self.css}</style>{self.html_text}"
            
            self.textDisplay.setHtml(self.html_text)  # Set HTML content

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
