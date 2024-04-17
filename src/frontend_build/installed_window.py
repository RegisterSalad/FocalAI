import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QLineEdit, QListWidget, QStackedWidget, QListWidgetItem, QLabel)

from PySide6.QtCore import Slot, QCoreApplication
import sys

#Local Imports
from model_page import ModelPage
from styler import Styler
from vertical_menu import VerticalMenu
from FocalAI import RepoWidget
from database import DatabaseManager

module_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if module_dir not in sys.path:
    sys.path.append(module_dir)

from directories import DB_PATH
from conda_env import CondaEnvironment
from repo import Repository


from api_caller import APIManager

class InstalledWindow(QWidget):
    def __init__(self, styler: Styler) -> None:
        super().__init__()
        self.init_ui(styler=styler)
        self.db = DatabaseManager(DB_PATH)

    def init_ui(self, styler: Styler) -> None:
        self.styler = styler
        self.styler.register_component(self)
        self.styler.style_me()
        self.caller = APIManager()
        self.setWindowTitle("Installed Models Window with Menu and Details")

        # Central widget and layout
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        layout = QHBoxLayout()

        # List and search
        self.list_widget = QListWidget()
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search...")

        self.search_bar.returnPressed.connect(self.trigger_search)  # Connect to returnPressed signal

        # Detail view
        self.detail_view = QStackedWidget()

        self.setup_detail_views()

        # Layout for list and search bar
        list_layout = QVBoxLayout()
        list_layout.addWidget(self.search_bar)
        list_layout.addWidget(self.list_widget)
        layout.addLayout(list_layout)
        layout.addWidget(self.detail_view)

        self.list_widget.itemClicked.connect(self.display_item)

        self.repos = []  # List to store repo objects
        self.centralWidget.setLayout(layout)

        #Initialize at full screen windowed
        screen = QCoreApplication.instance().primaryScreen()
        self.setGeometry(screen.geometry())

        # Initialize menu
        self.menu = VerticalMenu(self, self.styler)


    def create_menus(self):
        self.menu.create_menus()

    def setup_detail_views(self):
        self.model_page = ModelPage(self.styler)
        self.detail_view.addWidget(self.model_page)

    @Slot()
    def trigger_search(self):
        # Get text from searchBar and initiate search
        searchText = self.search_bar.text()
        if searchText:  # Only search if there's text
            self.search_items(searchText)

    def search_items(self, text: str):
        self.list_widget.clear()  # Clear current items
        self.repos.clear()  # Clear the repository list
        found_repos: CondaEnvironment = self.db.get_environment_by_name(text)

        for repo in found_repos:
            env: CondaEnvironment = repo
            self.repos.append(env.repository)  # Add the repo object to the list
            repo_widget = RepoWidget(repo)
            item = QListWidgetItem()
            item.setSizeHint(repo_widget.sizeHint())
            self.list_widget.addItem(item)
            self.list_widget.setItemWidget(item, repo_widget)

    def update_style(self) -> None:
        """
        Function from styler, is not applicable to main window
        """
        pass

    @Slot()
    def display_item(self):
        current_row = self.list_widget.currentRow()  # Get the currently selected item's row
        if 0 <= current_row < len(self.repos):
            repo = self.repos[current_row]
            if self.model_page.install_page:
                self.model_page.install_page.change_to_main_model_page() # Ensure that main model page is displayed
                
            self.model_page.update_content(repo_entry = repo)
            self.detail_view.setCurrentWidget(self.model_page)