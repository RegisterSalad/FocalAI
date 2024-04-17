import re
import sys
import os
from PySide6.QtWidgets import QVBoxLayout, QWidget, QTextEdit, QLineEdit, QLabel
from PySide6.QtCore import QProcess
from PySide6.QtGui import QTextCursor, QFont

module_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if module_dir not in sys.path:
    sys.path.append(module_dir)

class TerminalWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("""
            QWidget {
                border-radius: 5px;
            }
            QTextEdit, QLineEdit {
                border-radius: 15px;
                background-color: #f0f0f0;
            }
            """)
        label = QLabel("Working Directory Terminal")
        font = QFont('Arial', 18)
        font.setBold(True)  # Make the font bold

        # Apply the font to the label
        label.setFont(font)
        layout = QVBoxLayout()
        layout.addWidget(label)
        
        layout.setContentsMargins(5, 5, 5, 5)  # Add some padding to see the rounded corners

        self.output_textedit = QTextEdit()
        self.output_textedit.setReadOnly(True)
        layout.addWidget(self.output_textedit)

        self.input_lineedit = QLineEdit()
        self.input_lineedit.returnPressed.connect(self.execute_command)
        layout.addWidget(self.input_lineedit)

        self.setLayout(layout)

        # Start the shell process
        self.process = QProcess()
        self.process.setProcessChannelMode(QProcess.MergedChannels)  # Combine stdout and stderr
        self.process.readyReadStandardOutput.connect(self.read_output)
        self.start_shell()

    def start_shell(self):
        # Start a Bash shell process with custom PS1 to include the directory
        self.process.start("bash", ["-i"])  # '-i' makes the shell interactive and ensures loading of .bashrc
        self.process.waitForStarted()
        self.process.write(b'export PS1="\\w $ "\n')

    def execute_command(self):
        # Get the command from the input line
        command = self.input_lineedit.text()

        # Check if the command is to exit, then close the process
        if command.strip().lower() == 'exit':
            self.process.close()
            return

        full_command = f'pwd; {command}; echo -e "\\033[0m"\n'  # echo resets text formatting
        self.process.write(full_command.encode())
        self.process.waitForBytesWritten()
        self.input_lineedit.clear()

    def read_output(self):
        # Regular expression to match ANSI escape sequences
        ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
        # Read the output from the shell process
        output = self.process.readAllStandardOutput().data().decode()
        # Remove ANSI escape sequences
        clean_output = ansi_escape.sub('', output)
        # Append the cleaned output to the output text area
        self.output_textedit.moveCursor(QTextCursor.End)
        self.output_textedit.insertPlainText(clean_output)

    def closeEvent(self, event):
        if self.process.state() == QProcess.Running:
            self.process.terminate()
            self.process.waitForFinished()  # Wait indefinitely for the process to finish
            if self.process.state() == QProcess.Running:
                self.process.kill()  # Forcefully kill the process if it's still running
        event.accept()  # Accept the close event



