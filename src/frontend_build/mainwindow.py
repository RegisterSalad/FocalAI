from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QLineEdit, QListWidget, QPushButton,
                               QLabel, QStackedWidget, QFrame, QSizePolicy)
from PySide6.QtGui import QAction
from PySide6.QtCore import Slot, Qt
import sys

class ModelPage(QFrame):
    def __init__(self):
        super().__init__()
        # Main vertical layout for the page
        mainLayout = QVBoxLayout()

        # Vertical layout for buttons to stack them vertically
        buttonsLayout = QVBoxLayout()
        buttonsLayout.setAlignment(Qt.AlignRight | Qt.AlignTop)  # Align the buttons layout to the left and top

        # Creating and configuring buttons
        self.button1 = QPushButton("Button 1")
        self.button2 = QPushButton("Button 2")
        self.button3 = QPushButton("Button 3")

        # Optional: Change the size of the buttons
        self.button1.setFixedSize(100, 30)  # Width, Height
        self.button2.setFixedSize(100, 30)
        self.button3.setFixedSize(100, 30)

        # Add buttons to the buttons layout
        buttonsLayout.addWidget(self.button1)
        buttonsLayout.addWidget(self.button2)
        buttonsLayout.addWidget(self.button3)

        # Text label for displaying the item description
        self.text = QLabel("Select an item from the list")
        self.text.setWordWrap(True)
        self.text.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)  # Allow the text to expand horizontally but limit vertically

        # Thumbnail label
        self.thumbnail = QLabel()
        self.thumbnail.setFixedSize(100, 100)
        self.thumbnail.setStyleSheet("background-color: gray;")  # Placeholder styling

        # Constructing the main layout
        # To align the vertically stacked buttons to the left, wrap them in a QHBoxLayout
        buttonsWrapperLayout = QHBoxLayout()
        buttonsWrapperLayout.addLayout(buttonsLayout)
        buttonsWrapperLayout.addStretch()  # This pushes the buttons to the left

        # Adding elements to the main layout
        mainLayout.addLayout(buttonsWrapperLayout)  # Add wrapped buttons layout
        mainLayout.addWidget(self.text)  # Then add the text
        mainLayout.addWidget(self.thumbnail)  # Finally, add the thumbnail

        self.setLayout(mainLayout)

    def update_content(self, item_id):
        self.text.setText(f"Item {item_id}: Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
                          "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
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

    def create_menus(self):
        for i in range(5):
            menu = self.menuBar.addMenu(f"Menu {i+1}")
            action = QAction(f"Option {i+1}", self)
            menu.addAction(action)

    def populate_list(self):
        for i in range(10):
            self.listWidget.addItem(f"Item {i}")

        self.listWidget.itemClicked.connect(self.display_item)

    def setup_detail_views(self):
        self.modelPage = ModelPage()
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
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
