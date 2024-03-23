import re
import sys
from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget, QTextEdit, QLineEdit
from PySide6.QtCore import Qt, QProcess, QByteArray
from PySide6.QtGui import QTextCursor

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

        layout = QVBoxLayout()
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
        if self.process.state() != QProcess.NotRunning:
            self.process.terminate()  # Politely ask the process to terminate
            self.process.waitForFinished(2000)  # Wait up to 2000 ms for the process to terminate
            self.process.kill()  # Forcefully kill the process if it didn't terminate
        event.accept()  # Accept the close event




# class TerminalWidget(QWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.init_ui()

#     def init_ui(self):
#         layout = QVBoxLayout()

#         self.output_textedit = QTextEdit()
#         self.output_textedit.setReadOnly(True)
#         layout.addWidget(self.output_textedit)

#         self.input_lineedit = QLineEdit()
#         self.input_lineedit.returnPressed.connect(self.execute_command)
#         layout.addWidget(self.input_lineedit)

#         self.setLayout(layout)

#         # Start the shell process
#         self.process = QProcess()
#         self.process.readyReadStandardOutput.connect(self.read_output)
#         self.start_shell()

#     def start_shell(self):
#         # # Start a Bash shell process
#         # self.process.start("bash")
    
#     def execute_command(self):
#         # Get the command from the input line
#         command = self.input_lineedit.text()

#         # Send the command to the shell process
#         self.process.write(f"{command}\n".encode())
#         self.process.waitForBytesWritten()

#         # Clear the input line
#         self.input_lineedit.clear()

#     def read_output(self):
#         # Read the output from the shell process
#         output = self.process.readAllStandardOutput().data().decode()

#         # Append the output to the output text area
#         self.output_textedit.moveCursor(QTextCursor.End)
#         self.output_textedit.insertPlainText(output)

