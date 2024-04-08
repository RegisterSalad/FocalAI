from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame, QSizePolicy, QWidget, QListWidget, QListWidgetItem, QToolTip
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

# Calculate the path to the directory containing
module_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if module_dir not in sys.path:
    sys.path.append(module_dir)

# Project imports
from repo import Repository
from database import DatabaseManager
from conda_env import CondaEnvironment

class ModelPage(QFrame):
    def __init__(self, styler: Styler):
        super().__init__()
        self.install_page: InstallPage | None = None
        self.running_env: CondaEnvironment | None
        self.db = DatabaseManager("databases/conda_environments.db")
        self.styler = styler
        self.init_ui()

    def init_ui(self) -> None:
        self.html_text: str | None = None
        self.css = self.styler.doc_css
        self.button1 = QPushButton("Model Player")
        self.button2 = QPushButton("Download Model")
        self.button3 = QPushButton("Famoose the Goose")
        self.text_display = QWebEngineView()  # Use QWebEngineView
        self.text_display.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.text_display.setZoomFactor(0.9)
        self.thumbnail = QLabel()
        self.thumbnail.setFixedSize(100, 100)
        
        mainLayout = QVBoxLayout()
        
        self.button1.clicked.connect(lambda: self.create_model_player())
        self.button2.clicked.connect(lambda: self.change_to_install_page())
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

    def create_model_player(self):
        self.model_player = ModelPlayer(self) # Model Player is inited here because it needs a repo before initialization
        # Set the window to always stay on top when it's first opened
        self.model_player.setWindowFlags(self.model_player.windowFlags() | Qt.WindowStaysOnTopHint)
        self.model_player.show()
        self.model_player.raise_()
        self.model_player.activateWindow()
        # Remove the always-on-top flag after it's displayed and focused
        self.model_player.setWindowFlags(self.model_player.windowFlags() & ~Qt.WindowStaysOnTopHint)
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
        self.button1.show()
        self.button2.show()
        self.button3.show()   
        layout = self.layout()  # Get the layout of the frame
        if layout is not None:
            for i in range(layout.count()):  
                item = layout.itemAt(i)
                widget = item.widget()
                if widget is not None:  # Check if the item is a widget
                    widget.setEnabled(True)
                    widget.show()  # Show the widget

        if self.install_page.success:
            self.env = self.get_conda_env()

    def change_to_install_page(self):
        self.hide_all()
        self.install_page = InstallPage(self.styler, self, self.running_env)
        self.layout().addWidget(self.install_page)
        self.install_page.show_all()

    def convert_to_markdown(self, name: str) -> str:
        content = getattr(self.running_env.repository, name, None)
        
        if content:
            markdown_text = content
            self.html_text = markdown.markdown(markdown_text, extensions=['tables', 'fenced_code', 'codehilite', 'extra'])

            self.html_text = f"<style>{self.css}</style>{self.html_text}"
            
            return self.html_text

    def update_content(self, repo_entry) -> None:
        # Show buttons when content is updated
        if repo_entry is None:
            if self.html_text is None:
                self.html_text = markdown.markdown("  ", extensions=['tables', 'fenced_code', 'codehilite', 'extra'])
            
            self.html_text = f"<style>{self.css}</style>{self.html_text}"
            self.text_display.setHtml(self.html_text)  # Set HTML content
            return
            
        self.button1.show()
        self.button2.show()
        self.button3.show()
        self.running_env = CondaEnvironment(python_version="3.10.0",
                                            description=repo_entry.description,  
                                            repository_url=repo_entry.url)
        
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
        self.update_content(repo_entry=None)
