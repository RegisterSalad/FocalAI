from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame, QSizePolicy
from PySide6.QtCore import Qt
from PySide6.QtWebEngineWidgets import QWebEngineView  # Import QWebEngineView
import markdown
from paperswithcode.models.repository import Repository
from pygments.formatters import HtmlFormatter
from pop_up import PopupWindow

class ModelPage(QFrame):
    def __init__(self, styler, api_caller):
        super().__init__()
        self.styler = styler
        self.html_text: str | None = None
        self.css = self.styler.doc_css
        self.caller = api_caller

        self.button1 = QPushButton("Button 1")
        self.button2 = QPushButton("Button 2")
        self.button3 = QPushButton("Button 3")
        self.textDisplay = QWebEngineView()  # Use QWebEngineView
        self.textDisplay.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.textDisplay.setZoomFactor(0.9)
        self.thumbnail = QLabel()
        self.thumbnail.setFixedSize(100, 100)

        mainLayout = QVBoxLayout()

        # Connect the button1 click signal to the method to open the popup
        # self.pop_up_window = PopupWindow(self.styler)
        # self.button1.clicked.connect(lambda: self.display_pop_up())
        
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

    def display_pop_up(self):
        self.pop_up_window.show()

    #def create_model_player(self):
        

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