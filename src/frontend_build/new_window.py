from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QLineEdit, QListWidget, QPushButton,
                               QLabel, QStackedWidget, QFrame, QSizePolicy, QMenu, QTextBrowser, QTextEdit, QMenuBar)
from PySide6.QtGui import QAction, QGuiApplication, QPalette, QColor
from PySide6.QtCore import Slot, Qt, QCoreApplication
from PySide6.QtWidgets import QMenu
import sys
from file_drop_widget import FileDropWidget
from file_list_widget import FileListWidget
from window_menu_widget import MenuBar
from terminal_widget import TerminalWidget

class NewWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Model Player")
        layout = QVBoxLayout()



        # Create frames for top and bottom sections
        self.topFrame = QFrame()
        self.topFrame.setStyleSheet("background-color: white;  border: 2px solid black;")
        self.bottomFrame = QFrame()
        self.bottomFrame.setStyleSheet("background-color: lightGray;  border: 2px solid black;")

        self.leftTopFrame = QFrame()
        self.leftTopFrame.setStyleSheet("background-color: lightGray; border: 1px solid black;")
        self.rightTopFrame = QFrame()
        self.rightTopFrame.setStyleSheet("background-color: lightGray;  border: 1px solid black;")

        self.left1TopFrame = QFrame()
        self.left1TopFrame.setStyleSheet("background-color: lightGray;  border: 1px solid black;")
        self.left2TopFrame = QFrame()
        self.left2TopFrame.setStyleSheet("background-color: lightBlue;  border: 1px solid black;")

        """
        layout.addWidget(self.topFrame)
        layout.addWidget(self.bottomFrame)
        self.topFrame.addWidget(QHBoxLayout())
        self.topFrame.addWidget(self.leftTopFrame)
        self.topFrame.addWidget(self.rightTopFrame)
        """

        # Create layouts for top frame and left section of top frame
        topLayout = QHBoxLayout(self.topFrame)
        topleftLayout = QHBoxLayout(self.leftTopFrame)
        #leftTopLayout = QHBoxLayout(self.leftTopFrame)

        # Add left and right sections to the top layout
        topLayout.addWidget(self.leftTopFrame)
        topLayout.addWidget(self.rightTopFrame)
        topleftLayout.addWidget(self.left1TopFrame)
        topleftLayout.addWidget(self.left2TopFrame)

        # Add frames to the main layout
        layout.addWidget(self.topFrame)
        layout.addWidget(self.bottomFrame)

        """
        #Adding a menu bar
        # Adding a menu bar
        self.menu_bar = QMenuBar()
        terminal_menu = self.menu_bar.addMenu("Terminal Selection")
        bash_action = terminal_menu.addAction("Bash")
        zsh_action = terminal_menu.addAction("Zsh")
        powershell_action = terminal_menu.addAction("PowerShell")
        anaconda_action = terminal_menu.addAction("Anaconda Prompt")
        bash_action.triggered.connect(lambda: self.handle_terminal_selection("Bash"))
        zsh_action.triggered.connect(lambda: self.handle_terminal_selection("Zsh"))
        powershell_action.triggered.connect(lambda: self.handle_terminal_selection("PowerShell"))
        anaconda_action.triggered.connect(lambda: self.handle_terminal_selection("Anaconda Prompt"))

        # Set the menu bar as the menu bar of the main window
        layout.setMenuBar(self.menu_bar)
        """
        # Adding a menu bar
        self.menu_bar = MenuBar()
        layout.setMenuBar(self.menu_bar)

        #File drop capbability
        drop_widget = FileDropWidget()
        leftTopLayout = QVBoxLayout(self.left1TopFrame)
        leftTopLayout.addWidget(drop_widget)

        #self.left2TopFrame.addWigdet(FileListWidget)

        #Adding a terminal to the top right frame
        terminal_widge = TerminalWidget()
        rightTopLayout = QHBoxLayout(self.rightTopFrame)
        rightTopLayout.addWidget(terminal_widge)


        # Add a widget to the bottom frame
        bottom_layout = QVBoxLayout(self.bottomFrame)
        bottom_widget = QLabel("This is the bottom frame")
        bottom_layout.addWidget(bottom_widget)

        # List and search
        self.listWidget = QListWidget()
        self.searchBar = QLineEdit()
        self.searchBar.setPlaceholderText("Search...")
        #self.searchBar.textChanged.connect(self.search_items)

        # Add search bar and list widget to left2TopFrame
        listLayout = QVBoxLayout(self.left2TopFrame)
        listLayout.addWidget(self.searchBar)  # Assuming searchBar is an existing widget
        listLayout.addWidget(self.listWidget)  # Assuming listWidget is an existing widget

        # Adjust size policies and size hints
        self.searchBar.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.listWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.searchBar.setMinimumHeight(30)  # Adjust the minimum height of the search bar
        self.listWidget.setSizeAdjustPolicy(QListWidget.AdjustToContents)  # Adjust list widget size policy

        """
        #Testing list Debug
        # Create a placeholder widget to test the layout
        placeholder_widget = QWidget()
        placeholder_widget.setStyleSheet("background-color: lightGreen; border: 1px solid black;")

        # Add the placeholder widget to left2TopFrame
        left2TopLayout = QVBoxLayout(self.left2TopFrame)
        left2TopLayout.addWidget(placeholder_widget)
        """

        # Set the size policy of the bottom frame
        self.bottomFrame.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)


        self.setLayout(layout)
        self.setVisible(True)

        self.resize(800, 600)  # Set your desired size here
        #self.center_window()
        self.setGeometry(20,20,20,20)

    # def center_window(self):
    #     screen = QDesktopWidget().screenGeometry()
    #     self.setGeometry(screen.width() // 4, screen.height() // 4, screen.width() // 2, screen.height() // 2)

