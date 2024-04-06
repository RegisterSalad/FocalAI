from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton, QFileDialog, QMessageBox
from PySide6.QtCore import QFile, QIODevice, QTextStream, QRegularExpression
from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont

class PythonSyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)
        self.highlightRules = []

        keywordFormat = QTextCharFormat()
        keywordFormat.setForeground(QColor(88, 124, 255))  # Blue color for keywords
        keywordFormat.setFontWeight(QFont.Bold)
        keywords = [
            '\\bclass\\b', '\\bdef\\b', '\\bfrom\\b', '\\bimport\\b',
            '\\bas\\b', '\\breturn\\b', '\\bif\\b', '\\belse\\b', '\\belif\\b',
            '\\bwhile\\b', '\\bfor\\b', '\\bin\\b', '\\bnot\\b', '\\band\\b',
            '\\bor\\b', '\\bpass\\b', '\\bbreak\\b', '\\bcontinue\\b'
        ]
        for pattern in keywords:
            self.highlightRules.append((QRegularExpression(pattern), keywordFormat))


        stringFormat = QTextCharFormat()
        stringFormat.setForeground(QColor(207, 106, 50))  # Orange color for strings
        self.highlightRules.append((QRegularExpression('".*?"'), stringFormat))
        self.highlightRules.append((QRegularExpression("'.*?'"), stringFormat))

        functionCallFormat = QTextCharFormat()
        functionCallFormat.setForeground(QColor(0, 160, 0))  # Dark green color for function calls
        self.highlightRules.append((QRegularExpression('\\b[A-Za-z_][A-Za-z0-9_]*(?=\\()'), functionCallFormat))

        commentFormat = QTextCharFormat()
        commentFormat.setForeground(QColor(150, 150, 150))  # Gray color for comments
        self.highlightRules.append((QRegularExpression('#[^\n]*'), commentFormat))

    def highlightBlock(self, text):
        for pattern, format in self.highlightRules:
            iterator = pattern.globalMatch(text)
            while iterator.hasNext():
                match = iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), format)

class ScriptBuilder(QWidget):
    def __init__(self, parent=None):
        super(ScriptBuilder, self).__init__(parent)
        try:
            self.model_type = self.parent.repository.model_type
        except:
            self.model_type = "N/A" 
        self.defaultText: str = f"""
        # import <model> # Import model specific package
        from adapter_util import Adapter
        from typing import Callable

        # Model Initialization and configuration  



        # Initialize the adapter and set up pipes into and out of it
        adapter = Adapter()
        model_type: str = {self.model_type} # "ASR", "OBJ", or "LLM"

        get_model_input: Callable = adapter.get_input_method(model_type) # This tells the adapter to return the str of the path of the audio that was drag-and-dropped
        model_input = get_model_input()

        # Compute result based on model_input
        # Ex: result = model(model_input)

        adapter.set_model_output(result) # Method that displays the output to the user
        """
        self.initUI()

    def initUI(self):
        self.textEdit = QTextEdit()
        self.textEdit.setPlainText(self.defaultText)
        self.saveButton = QPushButton("Save")
        
        # Connect the save button to the save method
        self.saveButton.clicked.connect(self.saveFile)
        
        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.textEdit)
        layout.addWidget(self.saveButton)
        self.setLayout(layout)
        
        # Apply Python syntax highlighter to the text edit
        self.highlighter = PythonSyntaxHighlighter(self.textEdit.document())
        
        # Styling
        self.setStyleSheet("""
            QWidget {
                border-radius: 5px;
            }
            QTextEdit, QPushButton {
                border-radius: 15px;
                background-color: #f0f0f0;
            }
            """)

    def saveFile(self):
        fileName, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Python Files (*.py);;All Files (*)")
        if fileName:
            file = QFile(fileName)
            if not file.open(QIODevice.WriteOnly | QIODevice.Text):
                QMessageBox.warning(self, "Error", "Cannot save file: {}".format(file.errorString()))
                return
            out = QTextStream(file)
            out << self.textEdit.toPlainText()
            file.close()

if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    editor = ScriptBuilder()
    editor.show()
    sys.exit(app.exec())
