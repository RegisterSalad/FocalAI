from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton, QFileDialog, QMessageBox
from PySide6.QtCore import QFile, QIODevice, QTextStream, QRegularExpression
from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
import os
import sys
import subprocess
module_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if module_dir not in sys.path:
    sys.path.append(module_dir)

from conda_env import run_subprocess_with_logging

class PythonSyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)
        self.highlightRules = []

        # Formats
        keywordFormat = QTextCharFormat()
        keywordFormat.setForeground(QColor(88, 124, 255))  # Blue
        keywordFormat.setFontWeight(QFont.Bold)

        builtinFormat = QTextCharFormat()
        builtinFormat.setForeground(QColor(255, 120, 198))  # Pink

        decoratorFormat = QTextCharFormat()
        decoratorFormat.setForeground(QColor(255, 198, 109))  # Orange
        decoratorFormat.setFontWeight(QFont.Bold)

        classFunctionFormat = QTextCharFormat()
        classFunctionFormat.setForeground(QColor(102, 153, 255))  # Light Blue
        classFunctionFormat.setFontWeight(QFont.Bold)

        stringFormat = QTextCharFormat()
        stringFormat.setForeground(QColor(207, 106, 50))  # Orange

        commentFormat = QTextCharFormat()
        commentFormat.setForeground(QColor(150, 150, 150))  # Gray

        numberFormat = QTextCharFormat()
        numberFormat.setForeground(QColor(174, 129, 255))  # Purple

        selfFormat = QTextCharFormat()
        selfFormat.setForeground(QColor(255, 69, 0))  # Red

        functionCallFormat = QTextCharFormat()
        functionCallFormat.setForeground(QColor(0, 160, 0))  # Dark green color for function calls
        self.highlightRules.append((QRegularExpression('\\b[A-Za-z_][A-Za-z0-9_]*(?=\\()'), functionCallFormat))

        # Rules
        keywords = ['\\bclass\\b', '\\bdef\\b', '\\bfrom\\b', '\\bimport\\b',
                    '\\bas\\b', '\\breturn\\b', '\\bif\\b', '\\belse\\b', '\\belif\\b',
                    '\\bwhile\\b', '\\bfor\\b', '\\bin\\b', '\\bnot\\b', '\\band\\b',
                    '\\bor\\b', '\\bpass\\b', '\\bbreak\\b', '\\bcontinue\\b']
        for pattern in keywords:
            self.highlightRules.append((QRegularExpression(pattern), keywordFormat))

        builtins = ['\\bprint\\b', '\\brange\\b', '\\bstr\\b', '\\bint\\b', '\\bfloat\\b']
        for pattern in builtins:
            self.highlightRules.append((QRegularExpression(pattern), builtinFormat))

        decorators = ['@\\w+']
        for pattern in decorators:
            self.highlightRules.append((QRegularExpression(pattern), decoratorFormat))

        classFunctionNames = ['\\bclass\\s+\\w+', '\\bdef\\s+\\w+']
        for pattern in classFunctionNames:
            self.highlightRules.append((QRegularExpression(pattern), classFunctionFormat))

        self.highlightRules.append((QRegularExpression('".*?"'), stringFormat))  # Double-quoted string
        self.highlightRules.append((QRegularExpression("'.*?'"), stringFormat))  # Single-quoted string
        self.highlightRules.append((QRegularExpression("#[^\n]*"), commentFormat))  # Comment
        self.highlightRules.append((QRegularExpression("\\b\\d+\\.?\\d*"), numberFormat))  # Number

        specialMethods = ['\\b__\\w+__\\b']
        for pattern in specialMethods:
            self.highlightRules.append((QRegularExpression(pattern), selfFormat))

        # Highlight Block
    def highlightBlock(self, text):
        for pattern, format in self.highlightRules:
            iterator = pattern.globalMatch(text)
            while iterator.hasNext():
                match = iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), format)
        self.setCurrentBlockState(0)


class ScriptBuilder(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.repository = None
        self.repository = parent.repository
        self.model_type = self.repository.model_type
        self.defaultText: str = f"""
# import <model> # Import model specific package
from adapter_util import Adapter
from typing import Callable

# Model Initialization and configuration  



# Initialize the adapter and set up pipes into and out of it
adapter = Adapter({self.repository.repo_name})
model_type: str = "{self.model_type}" # "ASR", "OBJ", or "LLM"

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
        self.saveButton = QPushButton("Save and Run")
        
        # Connect the save button to the save method
        self.saveButton.clicked.connect(self.saveAndRunFile)
        
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
                font-size: 14px;
                margin: 4px 2px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

    def saveAndRunFile(self):
        fileName, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Python Files (*.py);;All Files (*)")
        if fileName:
            file = QFile(fileName)
            if not file.open(QIODevice.WriteOnly | QIODevice.Text):
                QMessageBox.warning(self, "Error", "Cannot save file: {}".format(file.errorString()))
                return
            out = QTextStream(file)
            out << self.textEdit.toPlainText()
            file.close()

            # Prepare to run the saved script as a subprocess
            logging_directory = "path/to/logging/directory"  # You can modify this path
            log_file_name = "script_run_log.txt"  # You can also make this more dynamic or user-defined

            # Check if the logging directory exists, if not create it
            if not os.path.exists(logging_directory):
                os.makedirs(logging_directory)

            # Now, run the subprocess with logging
            script_run_successful = run_subprocess_with_logging(
                args=[sys.executable, fileName],  # sys.executable ensures the same Python interpreter is used
                error_message=f"Error running {fileName}",
                logging_directory=logging_directory,
                log_file_name=log_file_name
            )

            if script_run_successful:
                QMessageBox.information(self, "Success", "Script ran successfully, check log for details.")
            else:
                QMessageBox.warning(self, "Failure", "Script failed to run, check log for details.")


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    editor = ScriptBuilder()
    editor.show()
    sys.exit(app.exec())