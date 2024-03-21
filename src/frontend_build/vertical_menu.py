from PySide6.QtWidgets import QMenu
from PySide6.QtGui import QAction

class VerticalMenu:
    def __init__(self, parent, styler):
        self.parent = parent
        self.styler = styler
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