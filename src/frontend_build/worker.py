from PySide6.QtCore import QObject, Signal, Slot
import os
import sys

# Calculate the path to the directory containing
module_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if module_dir not in sys.path:
    sys.path.append(module_dir)

from directories import LOG_DIR
from conda_env import run_subprocess_with_logging

class Worker(QObject):
    output = Signal(str)  # Signal to emit output lines
    finished = Signal(bool)  # Signal to emit on process completion, with success status

    def __init__(self, name: str, command: str, error_message: str):
        super().__init__()
        self.name = name
        self.command = command
        self.error_message = error_message
        self.success = False  # Track the success of the command execution

    @Slot()
    def run_command(self):
        log_path = os.path.join(LOG_DIR, f"{self.name}.log") 
        try:
            for line in run_subprocess_with_logging(self.command, self.error_message, log_file_dir=log_path):
                self.output.emit(line)  # Emit each line of the subprocess output
            self.success = True  # If execution reaches here, no exceptions were raised
        except Exception as e:
            self.output.emit(str(e))  # Optionally emit the error
            self.success = False
        finally:
            self.finished.emit(self.success)  # Emit the finished signal with the success flag