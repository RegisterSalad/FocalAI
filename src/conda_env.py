import subprocess
import os
from repo import Repository

general_logging_dir: str = os.path.expanduser("~/FocalAI/logs/")

def run_subprocess_with_logging(command: str, error_message: str, log_file_name: str, logging_directory: str = general_logging_dir):
    """
    Runs a subprocess with the given arguments and logs the output and any errors encountered.

    Args:
        command (str): The arguments to pass to the subprocess.
        error_message (str): The error message to display if the subprocess encounters an error.
        logging_directory (str): The directory to store logging information.
        log_file_name (str): The name of the log file.
    """
    os.makedirs(logging_directory, exist_ok=True)
    log_file_path = os.path.join(logging_directory, log_file_name)

    try:
        with open(log_file_path, 'w') as log_file:
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
    log_file_name = "env_list_log.log"
    run_subprocess_with_logging(command, error_message, general_logging_dir, log_file_name)

    log_file_path = os.path.join(general_logging_dir, log_file_name)
    try:
        with open(log_file_path, 'r') as log_file:
            environments = log_file.readlines()
        for env in environments:
            if env_name in env:
                return True
        return False
    except Exception as e:
        print(f"An error occurred while processing environments list: {e}")
        return False
        
class CondaEnvironment:
    def __init__(self, python_version: str, repository_url: str = "", description: str = "", pip_list_directory: str = "../pip_reqs", logging_directory: str = general_logging_dir, env_id: int | None = None) -> None:
        self.env_id = env_id
        self.python_version = python_version
        self.description = description
        self.pip_list_directory = pip_list_directory
        self.installed_models = None
        self.repository = Repository(repository_url)
        self.env_name = self.repository.repo_name
        self.logging_directory = logging_directory

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
            f"PIP List Directory: {self.pip_list_directory}",
            f"Models: {self.installed_models}", 
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


if __name__ == "__main__":
    # Get the absolute path of the logging directory
    logging_directory = os.path.abspath("../logging") # Values for testing
    requirements_directory = os.path.abspath("../pip_reqs")
    log_file_name = "logfile.log"

    # Create a CondaEnvironment instance
    env = CondaEnvironment(
        python_version="3.11.5",
        pip_list_directory=os.path.join(requirements_directory, "requirements.txt"),
        logging_directory=logging_directory,
    )

    # Test your methods
    env.install_all_requirements()
    env.test_environment()
    print(env)
    # env.delete()
    # print(env)