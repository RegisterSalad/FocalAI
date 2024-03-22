import sys
from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget, QTextEdit, QLineEdit
from PySide6.QtCore import Qt, QProcess, QByteArray

class TerminalWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.output_textedit = QTextEdit()
        self.output_textedit.setReadOnly(True)
        layout.addWidget(self.output_textedit)

        self.input_lineedit = QLineEdit()
        self.input_lineedit.returnPressed.connect(self.execute_command)
        layout.addWidget(self.input_lineedit)

        self.setLayout(layout)

        # Start the shell process
        self.process = QProcess()
        self.process.readyReadStandardOutput.connect(self.read_output)
        self.start_shell()

    def start_shell(self):
        # Start a Bash shell process
        self.process.start("bash")

    def execute_command(self):
        # Get the command from the input line
        command = self.input_lineedit.text()

        # Send the command to the shell process
        self.process.write(f"{command}\n".encode())
        self.process.waitForBytesWritten()

        # Clear the input line
        self.input_lineedit.clear()

    def read_output(self):
        # Read the output from the shell process
        output = self.process.readAllStandardOutput().data().decode()

        # Append the output to the output text area
        self.output_textedit.moveCursor(QTextCursor.End)
        self.output_textedit.insertPlainText(output)

