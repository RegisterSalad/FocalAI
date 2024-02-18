# This Python file uses the following encoding: utf-8
import sys

from PySide6.QtWidgets import QApplication, QMainWindow


# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.switch_to_page1)
        self.ui.pushButton_2.clicked.connect(self.switch_to_page2)
        self.ui.pushButton_3.clicked.connect(self.switch_to_page3)

    def switch_to_page1(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def switch_to_page2(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def switch_to_page3(self):
        self.ui.stackedWidget.setCurrentIndex(2)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
