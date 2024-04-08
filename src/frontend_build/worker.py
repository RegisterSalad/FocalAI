from PySide6.QtCore import QObject, Signal, Slot
import os
import sys
import subprocess
# Calculate the path to the directory containing
module_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if module_dir not in sys.path:
    sys.path.append(module_dir)

from conda_env import run_subprocess_with_logging

class Worker(QObject):
    finished = Signal()  # Signal to indicate the process has finished
    output = Signal(str)  # Signal to emit live output for GUI updates

    def __init__(self, conda_env, command_method_name, *args):
        super().__init__()
        self.conda_env = conda_env
        self.command_method_name = command_method_name
        self.args = args

    def run(self):
        # Get the method based on its name
        method = getattr(self.conda_env, self.command_method_name)
        
        # Ensure logging directory exists
        os.makedirs(self.conda_env.logging_directory, exist_ok=True)

        # Determine the log file path
        log_file_name = f"{self.command_method_name}_log.log"
        log_file_path = os.path.join(self.conda_env.logging_directory, log_file_name)
        
        try:
            with open(log_file_path, 'w') as log_file:
                # Format command for subprocess
                command = method(*self.args)
                if not command:  # If the method does not return a command, it's a signal that something went wrong
                    self.output.emit("Error: Command generation failed.")
                    return
                
                process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, shell=True)
                
                # Read and emit output live, while also writing to the log file
                for line in process.stdout:
                    log_file.write(line)
                    self.output.emit(line)  # Emit line for real-time GUI update
                
                process.stdout.close()
                return_code = process.wait()
                if return_code:
                    raise subprocess.CalledProcessError(return_code, command)
        except subprocess.CalledProcessError as e:
            error_message = f"Error occurred: {e}"
            self.output.emit(error_message)
            with open(log_file_path, 'a') as log_file:  # Append error message to the log file
                log_file.write(error_message)
        except OSError as e:
            error_message = f"OS error occurred: {e}"
            self.output.emit(error_message)
            with open(log_file_path, 'a') as log_file:  # Append error message to the log file
                log_file.write(error_message)
        
        self.finished.emit()
