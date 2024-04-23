from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton, QFileDialog, QMessageBox, QLabel
from PySide6.QtCore import QFile, QIODevice, QTextStream, QRegularExpression
from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
import os
import sys
import subprocess

module_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if module_dir not in sys.path:
    sys.path.append(module_dir)

from conda_env import CondaEnvironment
from install_page import run_environment_command
from directories import RUN_LOG_DIR, DB_PATH

class PythonSyntaxHighlighter(QSyntaxHighlighter):
    """
    A syntax highlighter for Python source code in a QTextDocument. This class configures and applies
    syntax highlighting rules to enhance the readability of Python code within a text-editing component.

    Attributes:
        document (QTextDocument): The document object where the syntax highlighting is applied.
    """

    
    def __init__(self, document):
        """
        Initializes the PythonSyntaxHighlighter with a QTextDocument to apply syntax highlighting.

        Args:
            document (QTextDocument): The document to which the syntax highlighting will be applied.
        """
        
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
        """
        Applies syntax highlighting to the given block of text using the defined rules and formats. 
        This method is automatically called by the QSyntaxHighlighter to format text as it's entered or edited.

        Args:
            text (str): The text block within the document to apply syntax highlighting.
        """

        for pattern, format in self.highlightRules:
            iterator = pattern.globalMatch(text)
            while iterator.hasNext():
                match = iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), format)
        self.setCurrentBlockState(0)


class ScriptBuilder(QWidget):
    """
    A widget designed to facilitate the creation and execution of scripts in a specified Conda environment. It provides a text editor for writing scripts, options to save and run them, and integrates environment-specific paths to enhance script functionality.

    Attributes:
        parent (QWidget): The parent widget that this ScriptBuilder is attached to.
        running_env (CondaEnvironment): The Conda environment context in which the scripts will be executed, providing necessary paths and settings.
        repository (Repository): The repository associated with the current environment, containing model-specific data.
        model_type (str): The type of model that the script is intended to interact with.
        defaultText (str): The default script template provided in the editor upon initialization.
    """
    
    def __init__(self, parent, running_env: CondaEnvironment):
        super().__init__(parent)
        self.running_env = running_env
        self.repository = self.running_env.repository
        self.model_type = self.repository.model_type
        current_working_dir = os.getcwd()
        primary_path = current_working_dir + "/src"
        secondary_path = current_working_dir + "/src/frontend_build"
        self.defaultText: str = f"""
# import <model> # Import model specific packages
# Adapter import
import sys

sys.path.append("{primary_path}")
sys.path.append("{secondary_path}")
from adapter import Adapter
from PySide6.QtWidgets import QApplication

# Initialize your model here  


def process_model_input(model_input: str): # Only runs when the app receives valid input from user
    '''
       model_input is the input received from the application  
    '''
    # Compute result based on model_input
    # Ex: result = model(model_input)
    adapter.display_output(result) # Display model results

if __name__ == "__main__":
    app = QApplication(sys.argv)  # Create an application object for PyQt
    adapter = Adapter("{self.repository.model_type}") # name automatically set from rest of app
    adapter.inputReady.connect(process_model_input)  # Connect the signal to processing function
    adapter.show()
    sys.exit(app.exec())  # Start the event loop and exit the application appropriately
"""
        self.initUI()

    def initUI(self):
        """
        Sets up the user interface components for the ScriptBuilder. This includes creating and configuring the text editor 
        for script input, a button for saving and executing scripts, and a label for the widget. It also applies syntax 
        highlighting to the text editor and sets the overall styling for the widget.
        """
        self.textEdit = QTextEdit()
        self.textEdit.setPlainText(self.defaultText)
        self.saveButton = QPushButton("Save and Run")
        
        # Connect the save button to the save method
        self.saveButton.clicked.connect(self.saveAndRunFile)
        self.label = QLabel("Script Builder")
        font = QFont('Arial', 18) 
        font.setBold(True)  # Make the font bold

        # Apply the font to the label
        self.label.setFont(font)
        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
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
        """
        Handles the action of saving the script entered in the text editor to a file and executing it. 
        This method also handles file dialog interactions, file writing, and script execution logging. 
        It provides user feedback about the success or failure of the script execution.

         Uses:
        - QDateTime to format the current date and time for unique logging.
        - QFile and QTextStream for file operations.
        - QMessageBox for user feedback.
        """       

        
        import datetime
        now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
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
            logging_directory = RUN_LOG_DIR
            log_file_name = os.path.join(RUN_LOG_DIR, f"log_{now}.log")  # You can also make this more dynamic or user-defined

            command = f"python {fileName}"
            call_tuple = self.running_env(command)
            script_run_successful = run_environment_command(self.parent(), worker_name="call" ,command=call_tuple[0], error_message=call_tuple[1])

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
