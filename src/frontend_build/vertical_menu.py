from PySide6.QtWidgets import QMenu, QListWidget, QWidget, QVBoxLayout
from PySide6.QtGui import QAction

import os
import sys
import json

from view_models_widget import JSONCaller


module_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if module_dir not in sys.path:
    sys.path.append(module_dir)
    
class VerticalMenu:
    def __init__(self, parent, styler):
        self.parent = parent
        self.styler = styler
        self.styler.register_component(self)
        # self.styler.style_me()
        self.create_menus()

    def create_menus(self):
        editMenu = self.parent.menuBar().addMenu("&Edit")
        preferencesMenu = QMenu("Preferences", self.parent)
        darkModeAction = preferencesMenu.addAction("Dark Mode")
        darkModeAction.setCheckable(True)
        darkModeAction.toggled.connect(self.styler.toggle_dark_mode)
        editMenu.addMenu(preferencesMenu)

        menu = self.parent.menuBar().addMenu(f"My Models")
        action = QAction(f"View my Models", self.parent)
        menu.addAction(action)
        # action.toggled.connect(self.open_model_list)


    def update_style(self) -> None:
        """
        Function from styler, is not applicable to main window
        """
        pass

    def open_model_list(self):
        print("showing downloaded models")
        self.model_list = viewModel_widget()
        print("init successful")
        # self.model_list.show()




class viewModel_widget(QWidget):

    def __init__(self):
        super().__init__()
        self.JSON = JSONCaller()
        self.initUI()


    def initUI(self):
        print("init UI")
        self.setWindowTitle("View My Models")
        
        # Set the style as provided
        # Updated style settings without 'display' and 'cursor' properties
        self.setStyleSheet("""
            QWidget {
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
            }
            QFrame {
                background-color: #F0F0F0;
                border-radius: 10px;
            }
            """)
        print("init UI pt2")
        list_widget = QListWidget()
        layout = QVBoxLayout()
        layout.addWidget(list_widget)
        self.setLayout(layout)

        