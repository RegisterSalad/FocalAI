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
    """
    A window in the GUI that displays installed models, offering functionality for searching and viewing details.

    Attributes:
        styler (Styler): An instance of Styler used for applying styles to components.
        db (DatabaseManager): Manages interactions with the database storing environment and repository data.
    """
    def __init__(self, styler: Styler) -> None:
        """
        Initializes the InstalledWindow with a specific styler.

        Args:
          styler (Styler): The styler object to apply UI styles.
        """
        super().__init__()
        self.init_ui(styler=styler)
        self.db = DatabaseManager(DB_PATH)

    def init_ui(self, styler: Styler) -> None:
        """
        Sets up the user interface components of the window.

        Args:
        styler (Styler): The styler object to apply UI styles to the window's components.
        """
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
        """
        Creates the menus for the window using a vertical menu layout. This function may define and add specific menu items.
        """
        self.menu.create_menus()

    def setup_detail_views(self):
        """
        Sets up the detail views that display information about the selected models or repositories. This is where individual model pages are initialized and added to the stack.
        """
        self.model_page = ModelPage(self.styler)
        self.detail_view.addWidget(self.model_page)

    @Slot()
    def trigger_search(self):
        """
        Triggers a search operation based on the text entered into the search bar. 
        This function connects directly to the returnPressed signal of the search bar.
        """
        # Get text from searchBar and initiate search
        searchText = self.search_bar.text()
        if searchText:  # Only search if there's text
            self.search_items(searchText)

    def search_items(self, text: str):
        """
        Searches for repository items based on the given text and updates the list widget with the results.

        Args:
          text (str): The text to search for within the repository names.
        """
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
        """
        Displays the detailed information of the selected repository item in the detail view when a list item is clicked.
        """
        current_row = self.list_widget.currentRow()  # Get the currently selected item's row
        if 0 <= current_row < len(self.repos):
            repo = self.repos[current_row]
            if self.model_page.install_page:
                self.model_page.install_page.change_to_main_model_page() # Ensure that main model page is displayed
                
            self.model_page.update_content(repo_entry = repo)
            self.detail_view.setCurrentWidget(self.model_page)
