from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QLineEdit, QListWidget, QStackedWidget)

from PySide6.QtCore import Slot, QCoreApplication
import sys
from model_page import ModelPage
from styler import Styler
from vertical_menu import VerticalMenu

class MainWindow(QMainWindow):
    def __init__(self, styler):
        super().__init__()
        self.styler = styler
        self.setWindowTitle("Main Window with Menu and Details")

        # Central widget and layout
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        layout = QHBoxLayout()

        # List and search
        self.listWidget = QListWidget()
        self.searchBar = QLineEdit()
        self.searchBar.setPlaceholderText("Search...")
        self.searchBar.textChanged.connect(self.search_items)

        # Detail view
        self.detailView = QStackedWidget()

        # Populate list and setup detail view
        self.populate_list()
        self.setup_detail_views()

        # Layout for list and search bar
        listLayout = QVBoxLayout()
        listLayout.addWidget(self.searchBar)
        listLayout.addWidget(self.listWidget)
        layout.addLayout(listLayout)
        layout.addWidget(self.detailView)

        self.centralWidget.setLayout(layout)

        #Initialize at full screen windowed
        screen = QCoreApplication.instance().primaryScreen()
        self.setGeometry(screen.geometry())

        # Initialize menu
        self.menu = VerticalMenu(self, self.styler)

    def create_menus(self):
        self.menu.create_menus()

    def populate_list(self):
        for i in range(50):
            self.listWidget.addItem(f"Item {i}")
        self.listWidget.itemClicked.connect(self.display_item)

    def setup_detail_views(self):
        self.modelPage = ModelPage(self.styler)
        self.detailView.addWidget(self.modelPage)

    @Slot()
    def search_items(self, text):
        for i in range(self.listWidget.count()):
            item = self.listWidget.item(i)
            item.setHidden(text.lower() not in item.text().lower())

    @Slot()
    def display_item(self, item):
        item_id = self.listWidget.row(item)
        self.modelPage.update_content(item_id)
        self.detailView.setCurrentWidget(self.modelPage)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    styler = Styler()
    mainWindow = MainWindow(styler)
    mainWindow.show()
    sys.exit(app.exec())
