import os
import sys
import json
from dataclasses import dataclass
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QLineEdit, QListWidget, QStackedWidget, QListWidgetItem, QLabel, QPushButton)

from PySide6.QtCore import Slot, QCoreApplication
from PySide6.QtGui import QFont
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

#Local Imports
from model_page import ModelPage
from styler import Styler
from vertical_menu import VerticalMenu
from repo import Repository
from directories import REPO_JSONS_DIR

module_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if module_dir not in sys.path:
    sys.path.append(module_dir)

from api_caller import APIManager

class RepoWidget(QWidget):
    def __init__(self, repo_info, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()

        # Create labels for each piece of repo info
        name_label = QLabel(f"Name: {repo_info.name}")
        owner_label = QLabel(f"Owner: {repo_info.owner}")
        description_label = QLabel(f"Description: {repo_info.description}")
        url_label = QLabel(f"URL: {repo_info.url}")
        url_label.setOpenExternalLinks(True)  # Make the URL clickable
        
        # Add labels to the layout
        layout.addWidget(name_label)
        layout.addWidget(owner_label)
        layout.addWidget(description_label)
        layout.addWidget(url_label)
        
        # Check if 'online' attribute exists and create a label accordingly
        if hasattr(repo_info, 'is_installed') and repo_info.is_installed:
            is_downloaded = QLabel("Locally Available")
            font = QFont("Arial", 12)
            font.setItalic(True)
            is_downloaded.setFont(font)
            is_downloaded.setStyleSheet("color: green;")
        else:
            is_downloaded = QLabel("Not Locally Available")
            font = QFont("Arial", 12)
            font.setItalic(False)
            is_downloaded.setFont(font)
            is_downloaded.setStyleSheet("color: red;")  # Use red for better visibility on negative status

        # Add 'is_downloaded' label to the layout
        layout.addWidget(is_downloaded)
        
        # Apply layout to the widget
        self.setLayout(layout)

class RepoTempObj:
    name: str
    owner: str
    description: str
    url: str
    is_installed: bool

    def __init__(self, entry_dict) -> None:
        self.url = entry_dict["url"]
        self.name = Repository.parse_name(self.url)
        self.owner = entry_dict["owner"]
        self.description = entry_dict["description"]
        self.is_installed = True

    def __str__(self) -> str:
        res = [
        f"name: {self.name}",
        f"owner: {self.owner}",
        f"url: {self.url}",
        f"description: {self.description}"
        ]
        
        return "\n".join(res)

class MainWindow(QMainWindow):
    def __init__(self, styler: Styler) -> None:
        super().__init__()

        self.init_ui(styler=styler)

    def init_ui(self, styler: Styler) -> None:
        self.styler = styler
        self.styler.register_component(self)
        self.styler.style_me()
        self.caller = APIManager()
        self.setWindowTitle("Main Window with Menu and Details")

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
        
        
        self.view_downloads_button = QPushButton("Toggle Downloaded Models View")
        self.viewFont = QFont("Arial", 18)
        self.viewFont.bold()
        self.view_downloads_button.setFont(self.viewFont)
        self.view_downloads_button.clicked.connect(self.display_downloads)
        # Layout for list and search bar
        list_layout = QVBoxLayout()
        list_layout.addWidget(self.view_downloads_button)
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
        self.display_downloads() # Function to display all downloaded models as widgets. This must run as it is the inital state of the application
    
    def display_downloads(self):
        """
        Populates the list widget with downloaded repository information.
        This method is called on application initialization and potentially
        after refreshing the list of downloads.
        """
        # Clear the current items in the list widget to refresh the display
        self.list_widget.clear()
        
        # Retrieve the list of installed repositories using the provided method
        installed_models_list = self.process_json_files(REPO_JSONS_DIR)
        self.repos = []
        
        # Iterate over each repository info dictionary and create a repository widget for it
        for repo_dict in installed_models_list:
            # Create a temporary repository object from dictionary
            repo_entry = RepoTempObj(repo_dict)
            print(repo_entry)
            # Append to the list of repository objects
            self.repos.append(repo_entry)
            
            # Create the custom widget to display the repository information
            repo_widget = RepoWidget(repo_entry)
            
            # Create a QListWidgetItem and set its size hint to the size of the repo widget
            item = QListWidgetItem()
            item.setSizeHint(repo_widget.sizeHint())
            
            # Add the item to the list widget and set the custom widget to be displayed in the list item
            self.list_widget.addItem(item)
            self.list_widget.setItemWidget(item, repo_widget)
        

    def create_menus(self):
        self.menu.create_menus()

    def setup_detail_views(self):
        self.model_page = ModelPage(self.styler, self)
        self.detail_view.addWidget(self.model_page)

    @Slot()
    def trigger_search(self):
        # Get text from searchBar and initiate search
        searchText = self.search_bar.text()
        if searchText:  # Only search if there's text
            self.search_items(searchText)

    def process_json_files(self, directory: str) -> list[dict]:
        """
        Processes all JSON files within a specified directory.

        Args:
        directory (str): The path to the directory containing the JSON files.

        Returns:
        None
        """
        installed_list: list[dict] = []
        # Iterate over each file in the directory
        for filename in os.listdir(directory):

            # Check if the file is a JSON file
            if filename.endswith('.json'):
                # Construct the full file path
                filepath = os.path.join(directory, filename)
                # Open and read the JSON file
                with open(filepath, 'r') as file:
                    data: dict = json.load(file)
                    # Process the data (for demonstration, we'll just print it)
                    installed_list.append(data)

        return installed_list

    def search_items(self, text: str):
        self.list_widget.clear()  # Clear current items
        self.repos.clear()  # Clear the repository list
        found_repos = self.caller.get_repo_list(text.lower().replace(" ", "-"))
        
        # Add functionality for searching through the installed repos


        resulting_repos: list = found_repos.results
        
        for repo in resulting_repos:
            self.repos.append(repo)  # Add the repo object to the list
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
        print("displaying item")
        current_row = self.list_widget.currentRow()  # Get the currently selected item's row
        print(current_row)
        if 0 <= current_row < len(self.repos):
            repo = self.repos[current_row]
            if self.model_page.install_page:
                self.model_page.install_page.change_to_main_model_page() # Ensure that main model page is displayed
                
            self.model_page.update_content(repo_entry = repo)
            self.detail_view.setCurrentWidget(self.model_page)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    styler = Styler()
    mainWindow = MainWindow(styler)
    mainWindow.show()
    sys.exit(app.exec())
