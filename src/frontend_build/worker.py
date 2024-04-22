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
    """
    A specialized QObject that runs a given command in a subprocess, emitting real-time output and completion status. 
    Designed to handle asynchronous command execution with signals for integrating into Qt event loops.

    Attributes:
        output (Signal): Emitted with a string payload containing output from the subprocess.
        finished (Signal): Emitted when the subprocess completes, with a boolean indicating success or failure.
        name (str): A unique identifier for the worker, used for logging purposes.
        command (str): The command line to be executed in the subprocess.
        error_message (str): The message to log or emit in case of an error during subprocess execution.
        success (bool): Indicates whether the command execution was successful.
    """
    output = Signal(str)  # Signal to emit output lines
    finished = Signal(bool)  # Signal to emit on process completion, with success status

    def __init__(self, name: str, command: str, error_message: str):
        """
        Initializes the Worker with necessary parameters for subprocess execution and logging.

        Args:
            name (str): The name of the worker, used as a label in logs.
            command (str): The complete shell command to be executed.
            error_message (str): A predefined error message to use if the command fails.
        """
        super().__init__()
        self.name = name
        self.command = command
        self.error_message = error_message
        self.success = False  # Track the success of the command execution

    @Slot()
    def run_command(self):
        """
        Executes the stored command in a subprocess, emitting output line by line, and then emits a finished signal 
        upon completion. This method is designed to be run in a separate thread to avoid blocking the GUI.

        Uses the `run_subprocess_with_logging` utility to execute the command with stdout and stderr redirected to both a log file and emitted via signals.
        """
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
