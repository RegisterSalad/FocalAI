from PySide6.QtWidgets import QMenu
from PySide6.QtGui import QAction

import os
import sys
# Calculate the path to the directory containing database.py
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

        for i in range(1, 5):
            menu = self.parent.menuBar().addMenu(f"Menu {i}")
            action = QAction(f"Option {i}", self.parent)
            menu.addAction(action)

    def update_style(self) -> None:
        """
        Function from styler, is not applicable to main window
        """
        pass