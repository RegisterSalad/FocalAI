from PySide6.QtWidgets import QListWidget, QAbstractItemView, QFileDialog
from PySide6.QtCore import Qt, Signal


class FileListWidget(QListWidget):
    fileOpened = Signal(str)

    def __init__(self):
        super().__init__()
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.itemDoubleClicked.connect(self.open_file)

    def add_file(self, file_path):
        self.addItem(file_path)

    def open_file(self, item):
        file_path = item.text()
        self.fileOpened.emit(file_path)

    def open_file(self, item):
        file_path = item.text()
        self.fileOpened.emit(file_path)

    """
    def sizeHint(self):
        return QSize(100, 100)  # Set an initial size hint

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Adjust the size of the list widget to match its parent frame
        self.setMinimumSize(event.size())
        self.setMaximumSize(event.size())
    """
