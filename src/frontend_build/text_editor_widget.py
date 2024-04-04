from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton, QFileDialog, QMessageBox
from PySide6.QtCore import QFile, QIODevice, QTextStream

class TextEditorWidget(QWidget):
    def __init__(self, parent=None):
        super(TextEditorWidget, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.textEdit = QTextEdit()
        self.saveButton = QPushButton("Save")
        
        # Connect the save button to the save method
        self.saveButton.clicked.connect(self.saveFile)
        
        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.textEdit)
        layout.addWidget(self.saveButton)
        self.setLayout(layout)
        
        # Styling
        self.setStyleSheet("""
            QWidget {
                border-radius: 5px;
            }
            QTextEdit, QLineEdit {
                border-radius: 15px;
                background-color: #f0f0f0;
            }
            """)

    def saveFile(self):
        fileName, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt);;All Files (*)")
        if fileName:
            file = QFile(fileName)
            if not file.open(QIODevice.WriteOnly | QIODevice.Text):
                QMessageBox.warning(self, "Error", "Cannot save file: {}".format(file.errorString()))
                return
            out = QTextStream(file)
            out << self.textEdit.toPlainText()
            file.close()