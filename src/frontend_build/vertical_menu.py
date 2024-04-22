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
    """
    Represents a vertical menu system associated with a parent GUI component. This class manages the creation and 
    behavior of menus, integrating with a styling system to provide theme toggling capabilities.

    Attributes:
        parent (QWidget): The parent widget to which the menu is attached, typically a main window.
        styler (Styler): A styling manager used to apply themes and styles to the menu and other components.
    """
    def __init__(self, parent, styler):
        """
        Initializes a new instance of the VerticalMenu with the specified parent and styler.

        Args:
            parent (QWidget): The parent widget that this menu is part of.
            styler (Styler): The styling manager that will be used to apply themes and styles to this menu.
        """
        self.parent = parent
        self.styler = styler
        self.styler.register_component(self)
        # self.styler.style_me()
        self.create_menus()

    def create_menus(self):
        """
        Sets up the menus within the parent's menu bar. This method adds an 'Edit' menu with a 'Preferences' submenu 
        for toggling dark mode, and a 'My Models' menu with actions related to model management.
        """
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
        """
        Opens a list of downloaded models. This method is responsible for initializing and displaying a widget 
        that lists all models currently available to the user.
        """
        print("showing downloaded models")
        self.model_list = viewModel_widget()
        print("init successful")
        # self.model_list.show()




class viewModel_widget(QWidget):
     """
    A widget designed to display a list of models that a user has access to, pulling information from a JSON source. 
    This class initializes the user interface elements necessary to list models in an easily navigable format.

    Attributes:
        QWidget
    """
    def __init__(self):
        """
        Initializes the viewModel_widget instance, setting up the JSON data handler and initializing the user interface.
        """
        super().__init__()
        self.JSON = JSONCaller()
        self.initUI()


    def initUI(self):
        """
        Configures the initial user interface for the viewModel_widget, setting up the layout and style of the widget.
        This includes creating a list widget for displaying model information and applying basic styling to the widget.
        """
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

        
