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
        self.init_styles()  # Initialize styles for the window
        self.init_ui()  # Setup the UI components

    def init_styles(self):
        self.setStyleSheet("""
            QWidget {
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
            }
            QFrame {
                background-color: #F0F0F0;
                border-radius: 10px;
            }
            QLineEdit, QListWidget {
                border: 2px solid #CCCCCC;
                border-radius: 5px;
                padding: 5px;
                background-color: white;
            }
            QLabel {
                color: #333333;
            }
            QPushButton {
                background-color: #4CAF50;
                border: none;
                color: white;
                padding: 10px 24px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 14px;
                margin: 4px 2px;
                cursor: pointer;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)  # Add margins for padding around the layout
        layout.setSpacing(10)  # Add some spacing between widgets



        # Adding a menu bar
        self.menu_bar = MenuBar()
        self.menu_bar.setStyleSheet("""
                QMenuBar {
                    background-color: #f0f0f0;
                    color: #333333;
                    border: 1px solid #cccccc;
                    border-radius: 10px;  /* Rounded corners for the menu bar */
                    padding: 2px;  /* Padding to ensure the border does not cut into the items */
                }
                QMenuBar::item {
                    background-color: #f0f0f0;
                    padding: 5px 10px;
                    border-radius: 5px;  /* Rounded corners for each menu item */
                }
                QMenuBar::item:selected { /* When selected using mouse or keyboard */
                    background-color: #a8a8a8;
                    border-radius: 5px;  /* Maintain rounded corners on selection */
                }
                QMenuBar::item:pressed {
                    background-color: #888888;
                    border-radius: 5px;  /* Maintain rounded corners when pressed */
                }
                QMenu {
                    background-color: #f0f0f0;
                    border: 1px solid #cccccc;
                    margin: 2px;  /* Some spacing around the menu */
                    border-radius: 5px;  /* Rounded corners for the dropdowns */
                }
                QMenu::item {
                    padding: 5px 25px;
                    border-radius: 5px;  /* Rounded corners for each menu item */
                }
                QMenu::item:selected {
                    background-color: #a8a8a8;
                    border-radius: 5px;  /* Maintain rounded corners on selection */
                }
            """)

        layout.setMenuBar(self.menu_bar)
        self.init_top_section(layout)
        self.init_bottom_section(layout)

        self.setLayout(layout)
        self.setGeometry(100, 100, 800, 600)  # Set the window geometry

    def init_top_section(self, main_layout):
        top_frame = QFrame()
        left_top_frame = QFrame()
        right_top_frame = QFrame()

        top_layout = QHBoxLayout()
        top_layout.setSpacing(10)  # Add spacing between left and right sections

        # File drop and list widget
        drop_widget = FileDropWidget()
        file_list_widget = FileListWidget()  # Assuming this is a custom widget similar to QListWidget

        drop_widget.filesDropped.connect(file_list_widget.update_file_list)

        # Set the size policy for the top left widgets
        left_top_frame.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        drop_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        drop_widget.setMaximumHeight(200)  # Set a maximum height
        file_list_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        left_top_layout = QVBoxLayout(left_top_frame)
        left_top_layout.addWidget(drop_widget)
        left_top_layout.addWidget(file_list_widget)

        # Assuming self.list_widget is your QListWidget instance
        #file_list_widget.clear()

        # Terminal widget with minimum size policy
        terminal_widget = TerminalWidget()
        terminal_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        terminal_widget.setMinimumSize(200, 150)  # Set a minimum size for the terminal widget

        right_top_layout = QVBoxLayout(right_top_frame)
        right_top_layout.addWidget(terminal_widget)

        # Add left and right sections to the top layout
        top_layout.addWidget(left_top_frame)
        top_layout.addWidget(right_top_frame)
        top_frame.setLayout(top_layout)
        main_layout.addWidget(top_frame)

    def init_bottom_section(self, main_layout):
        bottom_frame = QFrame()
        bottom_layout = QVBoxLayout()

        # Bottom widget with minimum size policy
        bottom_widget = QLabel("This is the bottom frame")
        bottom_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        bottom_widget.setMinimumHeight(100)  # Set a minimum height for the bottom widget
        bottom_widget.setAlignment(Qt.AlignCenter)

        bottom_layout.addWidget(bottom_widget)
        bottom_frame.setLayout(bottom_layout)

        # Set the size policy for the bottom frame to expand
        bottom_frame.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        main_layout.addWidget(bottom_frame)



# class NewWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Model Player")
#         layout = QVBoxLayout()



#         # Create frames for top and bottom sections
#         self.topFrame = QFrame()
#         self.topFrame.setStyleSheet("background-color: white;  border: 2px solid black;")
#         self.bottomFrame = QFrame()
#         self.bottomFrame.setStyleSheet("background-color: lightGray;  border: 2px solid black;")

#         self.leftTopFrame = QFrame()
#         self.leftTopFrame.setStyleSheet("background-color: lightGray; border: 1px solid black;")
#         self.rightTopFrame = QFrame()
#         self.rightTopFrame.setStyleSheet("background-color: lightGray;  border: 1px solid black;")

#         self.left1TopFrame = QFrame()
#         self.left1TopFrame.setStyleSheet("background-color: lightGray;  border: 1px solid black;")
#         self.left2TopFrame = QFrame()
#         self.left2TopFrame.setStyleSheet("background-color: lightBlue;  border: 1px solid black;")

#         """
#         layout.addWidget(self.topFrame)
#         layout.addWidget(self.bottomFrame)
#         self.topFrame.addWidget(QHBoxLayout())
#         self.topFrame.addWidget(self.leftTopFrame)
#         self.topFrame.addWidget(self.rightTopFrame)
#         """

#         # Create layouts for top frame and left section of top frame
#         topLayout = QHBoxLayout(self.topFrame)
#         topleftLayout = QHBoxLayout(self.leftTopFrame)
#         #leftTopLayout = QHBoxLayout(self.leftTopFrame)

#         # Add left and right sections to the top layout
#         topLayout.addWidget(self.leftTopFrame)
#         topLayout.addWidget(self.rightTopFrame)
#         topleftLayout.addWidget(self.left1TopFrame)
#         topleftLayout.addWidget(self.left2TopFrame)

#         # Add frames to the main layout
#         layout.addWidget(self.topFrame)
#         layout.addWidget(self.bottomFrame)

#         """
#         #Adding a menu bar
#         # Adding a menu bar
#         self.menu_bar = QMenuBar()
#         terminal_menu = self.menu_bar.addMenu("Terminal Selection")
#         bash_action = terminal_menu.addAction("Bash")
#         zsh_action = terminal_menu.addAction("Zsh")
#         powershell_action = terminal_menu.addAction("PowerShell")
#         anaconda_action = terminal_menu.addAction("Anaconda Prompt")
#         bash_action.triggered.connect(lambda: self.handle_terminal_selection("Bash"))
#         zsh_action.triggered.connect(lambda: self.handle_terminal_selection("Zsh"))
#         powershell_action.triggered.connect(lambda: self.handle_terminal_selection("PowerShell"))
#         anaconda_action.triggered.connect(lambda: self.handle_terminal_selection("Anaconda Prompt"))

#         # Set the menu bar as the menu bar of the main window
#         layout.setMenuBar(self.menu_bar)
#         """
#         # Adding a menu bar
#         self.menu_bar = MenuBar()
#         layout.setMenuBar(self.menu_bar)

#         #File drop capbability
#         drop_widget = FileDropWidget()
#         leftTopLayout = QVBoxLayout(self.left1TopFrame)
#         leftTopLayout.addWidget(drop_widget)

#         #self.left2TopFrame.addWigdet(FileListWidget)

#         #Adding a terminal to the top right frame
#         terminal_widge = TerminalWidget()
#         rightTopLayout = QHBoxLayout(self.rightTopFrame)
#         rightTopLayout.addWidget(terminal_widge)


#         # Add a widget to the bottom frame
#         bottom_layout = QVBoxLayout(self.bottomFrame)
#         bottom_widget = QLabel("This is the bottom frame")
#         bottom_layout.addWidget(bottom_widget)

#         # List and search
#         self.listWidget = QListWidget()
#         self.searchBar = QLineEdit()
#         self.searchBar.setPlaceholderText("Search...")
#         #self.searchBar.textChanged.connect(self.search_items)

#         # Add search bar and list widget to left2TopFrame
#         listLayout = QVBoxLayout(self.left2TopFrame)
#         listLayout.addWidget(self.searchBar)  # Assuming searchBar is an existing widget
#         listLayout.addWidget(self.listWidget)  # Assuming listWidget is an existing widget

#         # Adjust size policies and size hints
#         self.searchBar.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
#         self.listWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
#         self.searchBar.setMinimumHeight(30)  # Adjust the minimum height of the search bar
#         self.listWidget.setSizeAdjustPolicy(QListWidget.AdjustToContents)  # Adjust list widget size policy

#         """
#         #Testing list Debug
#         # Create a placeholder widget to test the layout
#         placeholder_widget = QWidget()
#         placeholder_widget.setStyleSheet("background-color: lightGreen; border: 1px solid black;")

#         # Add the placeholder widget to left2TopFrame
#         left2TopLayout = QVBoxLayout(self.left2TopFrame)
#         left2TopLayout.addWidget(placeholder_widget)
#         """

#         # Set the size policy of the bottom frame
#         self.bottomFrame.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)


#         self.setLayout(layout)
#         self.setVisible(True)

#         self.resize(800, 600)  # Set your desired size here
#         #self.center_window()
#         self.setGeometry(100,100,100,100)

#     # def center_window(self):
#     #     screen = QDesktopWidget().screenGeometry()
#     #     self.setGeometry(screen.width() // 4, screen.height() // 4, screen.width() // 2, screen.height() // 2)

