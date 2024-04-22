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
    """
    A widget that displays detailed information about a repository.

    This widget is designed to be used in a graphical user interface to present
    relevant information about a repository, such as its name, owner, description,
    and URL. It also indicates whether the repository is available locally.

    Attributes:
        repo_info (object): An object containing the repository information.
            It should have `name`, `owner`, `description`, `url`, and optionally `is_installed` attributes.
        parent (QWidget, optional): The parent widget. Defaults to None.
    """
    def __init__(self, repo_info, parent=None):
        """
        Initializes the RepoWidget with repository information and sets up the UI components.

        Args:
            repo_info (object): The repository information object with attributes necessary for display.
            parent (QWidget, optional): The parent widget. Defaults to None.

        The repo_info object must have the following attributes:
        - name: The name of the repository.
        - owner: The owner of the repository.
        - description: A brief description of the repository.
        - url: The URL to the repository.
        - is_installed (optional): A boolean indicating if the repository is locally available.
        """
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
    """
    A temporary object for holding repository information.

    This class is designed to act as a simple container for repository data,
    providing easy access and manipulation of its attributes in memory.

    Attributes:
        name (str): The name of the repository.
        owner (str): The owner of the repository.
        description (str): A description of the repository.
        url (str): The URL to the repository.
        is_installed (bool): Indicates whether the repository is locally installed.
    """
    name: str
    owner: str
    description: str
    url: str
    is_installed: bool

    def __init__(self, entry_dict) -> None:
        """
        Initializes the RepoTempObj instance with data from a dictionary.

        Args:
            entry_dict (dict): A dictionary containing repository data. 
            This dictionary must include 'url', 'owner', and 'description' keys.

        The 'url' key is used to extract the repository name using a static method `parse_name` from the `Repository` class.
        """
        self.url = entry_dict["url"]
        self.name = Repository.parse_name(self.url)
        self.owner = entry_dict["owner"]
        self.description = entry_dict["description"]
        self.is_installed = True

    def __str__(self) -> str:
        """
        Provides a string representation of the repository data.

        Returns:
            str: A formatted string displaying the attributes of the repository.
        """
        res = [
        f"name: {self.name}",
        f"owner: {self.owner}",
        f"url: {self.url}",
        f"description: {self.description}"
        ]
        
        return "\n".join(res)

class MainWindow(QMainWindow):
    """
    Main application window that hosts the user interface for interacting with repositories.

    Attributes:
        styler (Styler): A Styler object used for applying and managing styles across the application.
        centralWidget (QWidget): The central widget of the main window.
        list_widget (QListWidget): Widget displaying a list of repositories.
        search_bar (QLineEdit): Input field for searching repositories.
        detail_view (QStackedWidget): Widget that displays detailed views of the selected repository.
        menu (VerticalMenu): The application's menu system.
    """
    def __init__(self, styler: Styler) -> None:
        """
        Initializes the main window with a styler instance.

        Args:
            styler (Styler): A Styler object to apply consistent styles across the UI.
        """
        super().__init__()

        self.init_ui(styler=styler)

    def init_ui(self, styler: Styler) -> None:
        """
        Initializes the user interface elements of the main window.

        Args:
            styler (Styler): A Styler object for styling UI components.
        """
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
        Displays downloaded models in the list widget. It reads JSON data from a directory and populates the list.
        This method sets up initial view state of the application, displaying all downloaded models.
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
        """
        Configures the application's menus.
        """
        self.menu.create_menus()

    def setup_detail_views(self):
        """
        Sets up the detailed view components of the application.
        """
        self.model_page = ModelPage(self.styler, self)
        self.detail_view.addWidget(self.model_page)

    @Slot()
    def trigger_search(self):
        """
        Initiates a search based on the text in the search bar and updates the display accordingly.
        """
        # Get text from searchBar and initiate search
        searchText = self.search_bar.text()
        if searchText:  # Only search if there's text
            self.search_items(searchText)

    def process_json_files(self, directory: str) -> list[dict]:
        """
        Reads and processes JSON files from a specified directory to extract repository data.

        Args:
            directory (str): Path to the directory containing JSON files.

        Returns:
            list[dict]: A list of dictionaries containing repository data.
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
        """
        Filters repositories based on a search query and updates the list widget with the results.

        Args:
            text (str): The search query used to filter repository listings.
        """
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
        Updates the style of the main window, typically called after a style change.
        """
        pass

    @Slot()
    def display_item(self):
        """
        Displays details of the selected repository in the detail view when an item is selected from the list widget.
        """
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
