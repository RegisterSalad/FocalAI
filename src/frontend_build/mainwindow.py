import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QLineEdit, QListWidget, QStackedWidget, QListWidgetItem, QLabel)

from PySide6.QtCore import Slot, QCoreApplication
import sys

#Local Imports
from model_page import ModelPage
from styler import Styler
from vertical_menu import VerticalMenu

# Calculate the path to the directory containing database.py
module_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if module_dir not in sys.path:
    sys.path.append(module_dir)

from api_caller import APICaller

class RepoWidget(QWidget):
    def __init__(self, repo_info, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()

        # Create labels for each piece of repo info
        # self.id_label = QLabel(f"ID: [{repo_info['id']}]")
        self.name_label = QLabel(f"Name: {repo_info.name}")
        self.owner_label = QLabel(f"Owner: {repo_info.owner}")
        self.description_label = QLabel(f"Description: {repo_info.description}")
        self.url_label = QLabel(f"URL: {repo_info.url}")
        self.url_label.setOpenExternalLinks(True)  # Make the URL clickable

        # Add labels to the layout
        # layout.addWidget(self.id_label)
        layout.addWidget(self.name_label)
        layout.addWidget(self.owner_label)
        layout.addWidget(self.description_label)
        layout.addWidget(self.url_label)

        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self, styler: Styler):
        super().__init__()
        self.styler = styler
        self.styler.register_component(self)
        self.styler.style_me()
        self.caller = APICaller()
        self.setWindowTitle("Main Window with Menu and Details")

        # Central widget and layout
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        layout = QHBoxLayout()

        # List and search
        self.listWidget = QListWidget()
        self.searchBar = QLineEdit()
        self.searchBar.setPlaceholderText("Search...")

        self.searchBar.returnPressed.connect(self.trigger_search)  # Connect to returnPressed signal

        # Detail view
        self.detailView = QStackedWidget()

        self.setup_detail_views()

        # Layout for list and search bar
        listLayout = QVBoxLayout()
        listLayout.addWidget(self.searchBar)
        listLayout.addWidget(self.listWidget)
        layout.addLayout(listLayout)
        layout.addWidget(self.detailView)

        self.listWidget.itemClicked.connect(self.display_item)

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
        self.modelPage = ModelPage(self.styler, self.caller)
        self.detailView.addWidget(self.modelPage)

    @Slot()
    def trigger_search(self):
        # Get text from searchBar and initiate search
        searchText = self.searchBar.text()
        if searchText:  # Only search if there's text
            self.search_items(searchText)

    def search_items(self, text):
        self.listWidget.clear()  # Clear current items
        self.repos.clear()  # Clear the repository list
        found_repos = self.caller.get_repo_list(text.lower())

        for repo in found_repos.results:
            self.repos.append(repo)  # Add the repo object to the list
            repo_widget = RepoWidget(repo)
            item = QListWidgetItem()
            item.setSizeHint(repo_widget.sizeHint())
            self.listWidget.addItem(item)
            self.listWidget.setItemWidget(item, repo_widget)

    def update_style(self) -> None:
        """
        Function from styler, is not applicable to main window
        """
        pass

    @Slot()
    def display_item(self):
        current_row = self.listWidget.currentRow()  # Get the currently selected item's row
        if 0 <= current_row < len(self.repos):
            repo = self.repos[current_row]
            self.modelPage.update_content(repo_url=repo.url)
            self.detailView.setCurrentWidget(self.modelPage)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    styler = Styler()
    mainWindow = MainWindow(styler)
    mainWindow.show()
    sys.exit(app.exec())
