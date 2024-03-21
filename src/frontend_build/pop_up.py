from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QApplication
from PySide6.QtCore import Qt

class PopupWindow(QWidget):
    def __init__(self, styler):
        super().__init__()
        self.styler = styler
        # Optionally use the styler to apply initial styles if needed
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Popup Window')
        self.setGeometry(100, 100, 200, 100)  # Modify as needed
        self.styler.register_component(self)  # Ensure the popup gets styled too
        # Additional UI setup can go here

    def update_style(self):
        # This method can be implemented to react to style changes if needed
        pass