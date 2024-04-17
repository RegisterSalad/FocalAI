import subprocess
import os
from repo import Repository
from directories import LOG_DIR, ENV_LIST_LOG
general_logging_dir: str = os.path.expanduser("~/FocalAI/logs/")

def run_subprocess_with_logging(command: str, error_message: str, log_file_dir: str):
    """
    Runs a subprocess with the given arguments and logs the output and any errors encountered.

    Args:
        command (str): The arguments to pass to the subprocess.
        error_message (str): The error message to display if the subprocess encounters an error.
        logging_directory (str): The directory to store logging information.
        log_file_name (str): The name of the log file.
    """

    try:
        with open(log_file_dir, 'w') as log_file:
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

            # Read output live and yield lines
            for line in process.stdout:
                log_file.write(line)
                log_file.flush()
                yield line
            
            process.stdout.close()
            return_code = process.wait()
            if return_code:
                raise subprocess.CalledProcessError(return_code, command)
    except subprocess.CalledProcessError as e:
        print(f"{error_message}: {e}")
        yield error_message
    except OSError as e:
        print(f"OS error occurred, possibly due to a missing executable or insufficient permissions.\n{e}")
        yield "OS error occurred, check permissions or executable."

def check_if_exists(env_name: str) -> bool:
    command = "conda env list"
    error_message = "Error finding installed environments"

    run_subprocess_with_logging(command, error_message, ENV_LIST_LOG)

    try:
        with open(ENV_LIST_LOG, 'r') as log_file:
            environments = log_file.readlines()
        for env in environments:
            if env_name in env:
                return True
        return False
    except Exception as e:
        print(f"An error occurred while processing environments list: {e}")
        return False
        
class CondaEnvironment:
    def __init__(self, python_version: str, repository_url: str = "", description: str = "",env_id: int | None = None) -> None:
        self.env_id = env_id
        self.python_version = python_version
        self.repository = Repository(repository_url, description)
        self.env_name = self.repository.repo_name
        self.is_installed: bool = False

    def __call__(self, command: str) -> tuple[str, str]:
        """
        Prepares a command string to be run within the environment along with an error message.

        Args:
            command (str): The command to run.

        Returns:
            tuple[str, str]: The command string and an error message.
        """
        args = f"conda run -n {self.env_name} --no-capture-output bash -c \"{command}\""
        error_message = f"Error occurred while running command in environment '{self.env_name}'"
        return (args, error_message)
    
    def __str__(self) -> str:
        """
        Provides a string representation of the CondaEnvironment object
        Returns:
            str: A summary of the environment's characteristics.
        """
        str_attributes: list = [
            f"Environment Name: {self.env_name}",
            f"Python Version: {self.python_version}",
            f"Repository: {self.repository}"
        ]

        return "\n".join(str_attributes)
    
    def create(self) -> tuple[str, str]:
        """
        Prepares the command to create the Anaconda environment.
        
        Returns:
            tuple[str, str]: Command string and error message.
        """
        command = f"conda create -n {self.env_name} -y python={self.python_version}"
        error_message = f"Error occurred while creating environment '{self.env_name}'"
        return (command, error_message)

    def delete(self) -> tuple[str, str]:
        """
        Prepares the command to delete the Anaconda environment.

        Returns:
            tuple[str, str]: Command string and error message.
        """
        command = f"conda env remove -n {self.env_name} -y && conda clean --all -y"
        error_message = f"Error occurred while deleting environment '{self.env_name}'"
        return (command, error_message)
    
    def conda_init(self) -> bool:
        """
        Initializes Anaconda
        """
        command = "conda init"
        error_message = f"Error occurred while running 'conda init'"
        return (command, error_message)

        
    @property
    def is_created(self) -> bool:
        check_if_exists(self.env_name) # Separate function, no need for live capture
