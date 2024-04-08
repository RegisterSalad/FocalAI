import subprocess
import os
from repo import Repository

general_logging_dir: str = os.path.expanduser("~/FocalAI/logs/")

def run_subprocess_with_logging(args: list[str], error_message: str, logging_directory: str, log_file_name: str) -> bool:
    """
    Runs a subprocess with the given arguments and logs the output and any errors encountered.

    Args:
        args (list[str]): The list of arguments to pass to the subprocess.
        error_message (str): The error message to display if the subprocess encounters an error.
        logging_directory (str): The directory to store logging information.
        log_file_name (str): The name of the log file.
    """
    try:
        # Ensure the logging directory exists
        os.makedirs(logging_directory, exist_ok=True)
        
        log_file_path = os.path.join(logging_directory, log_file_name)
        
        with open(log_file_path, 'w') as log_file:
            command = " ".join(args)
            print(f"Tried: {command} at {log_file_path}")
            subprocess.run(command, check=True, stdout=log_file, stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"{error_message}: {e}")
        return False
    except OSError as e:
        print(f"OS error occurred, possibly due to a missing executable or insufficient permissions.\n{e}")
        return False
    return True

def check_if_exists(env_name: str) -> bool:
    args = ['conda', 'env', 'list']
    error_message = "Error finding installed environments"
    log_file_name = "env_list_log.log"
    run_subprocess_with_logging(args, error_message, general_logging_dir, log_file_name)

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
    """
    Represents an Anaconda environment
    Attributes:
        env_id (int | None): Primary key for database lookup
        description (str) : Description of the installed repository provided by paperswithcode
        python_version (str): The Python version of the conda environment
        pip_list_directory (str): The location of the pip requirements
        installed_models (list[str] | None): The names of the models currently installed
        repository (Repository): Repository Object containing all information about repository as well as formatted readme
        env_name (str): Name conda environment
        logging_directory (str): Directory where logging files are create and stored.
    """
    def __init__(self, python_version: str, repository_url: str = "", description: str = "", pip_list_directory: str = "../pip_reqs", logging_directory: str = general_logging_dir, env_id: int | None = None) -> None:
        self.env_id = env_id
        self.python_version = python_version
        self.description = description
        self.pip_list_directory = pip_list_directory
        self.installed_models = None
        self.repository = Repository(repository_url)
        self.env_name = self.repository.repo_name
        self.logging_directory = logging_directory

    def __call__(self, command: str) -> bool:
        """
        Allows the CondaEnvironment instance to be called directly to run a command within the environment.

        Args:
            command (str): The command to run.
        """
        # Ensure the environment is activated before running the command
        args = ['conda', 'run', '-n', self.env_name, '--no-capture-output', 'bash', '-c', '"'+command+'"']
        error_message = f"Error occurred while running command in environment '{self.env_name}'"
        log_file_name = "run_command_log.log"
        return run_subprocess_with_logging(args, error_message, self.logging_directory, log_file_name)
    
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
    
    def create(self) -> bool:
        """
        Creates the Anaconda environment if it does not exist already.
        """
        if self.is_created:
            return

        args = ['conda', 'create', '-n', self.env_name, '-y', f'python={self.python_version}']
        error_message = f"Error occurred while creating environment '{self.env_name}'"
        return run_subprocess_with_logging(args, error_message, self.logging_directory, "create_log.log")

    def delete(self) -> bool:
        """
        Deletes the Anaconda environment.
        """
        args = ['conda', 'env', 'remove', '-n', self.env_name, '-y', '&&', 'conda', 'clean', '--all', '-y']
        error_message = f"Error occurred while deleting environment '{self.env_name}'"
        return run_subprocess_with_logging(args, error_message, self.logging_directory, "delete_log.log")

    def conda_init(self) -> bool:
        """
        Initializes Anaconda
        """
        args = ['conda', 'init']
        error_message = f"Error occurred while running 'conda init'"
        return run_subprocess_with_logging(args, error_message, self.logging_directory, "init_log.log")

    def activate_by_name(self, env_name: str) -> bool:
        """
        Activates the Anaconda environment using a bash script.

        Args:
            env_name (str): Name of the Anaconda environment to be activated
        """

        activate_script_path = self.bash_scipt_dir + "/activate_conda_env.sh"
        args = ['bash', activate_script_path, env_name]
        error_message = f"Error occurred while activating environment '{env_name}'"
        return run_subprocess_with_logging(args, error_message, self.logging_directory, "activate_log.log")

    def install_all_requirements(self) -> bool:
        """
        Installs all pip requirements through pip within the conda environment using 'conda run',
        leveraging the dedicated subprocess function for execution and logging.
        """

        # Construct the command to run 'pip install' within the conda environment
        args = ['conda', 'run', '-n', self.env_name, 'pip', 'install', '-r', self.pip_list_directory]
        error_message = f"Error occurred while installing pip requirements from '{self.pip_list_directory}'"

        # Use the dedicated subprocess function for execution and logging
        return run_subprocess_with_logging(args, error_message, self.logging_directory, "pip_log.log")

    def test_environment(self) -> bool:
        """
        Tests if running commands in the conda environment is successful by executing a simple command.
        Returns True if the command executes successfully and False otherwise.
        """

        # Use a simple command that provides predictable output, like checking the Python version
        args = ['conda', 'run', '-n', self.env_name, 'python', '--version']
        try:
            # Execute the command and capture the output
            result = subprocess.run(args, capture_output=True, text=True, check=True)
            # Optionally, check the output for expected content (e.g., Python version)
            expected_output_part = self.python_version.split('.')[0]  # Just check major version part for simplicity
            if expected_output_part in result.stdout or expected_output_part in result.stderr:
                print(f"Test successful: {result.stdout}")
                return True
            else:
                print(f"Test failed: Python version mismatch or unexpected output: {result.stdout}")
                return False
        except subprocess.CalledProcessError as e:
            print(f"An error occurred during the environment test: {e}")
            return False

    def find_installed_environments(self) -> list[str] | None:
        """
        Finds all of the installed Anaconda environments and returns a list of their names using the dedicated
        subprocess function with logging.

        Args:
            logging_directory (str): The directory where the log file will be saved.
        """
        log_file_name = "env_list_log.log"
        args = ['conda', 'env', 'list']

        # Execute the command and log its output
        if not run_subprocess_with_logging(args, "Error finding installed environments", self.logging_directory, log_file_name):
            print("Returning None")
            return None

        # Path to the log file where the command output is saved
        log_file_path = os.path.join(logging_directory, log_file_name)

        try:
            # Read the log file to process the output
            with open(log_file_path, 'r') as log_file:
                output_lines = log_file.readlines()

            # Extract environment names from the output
            env_names = [line.split()[0] for line in output_lines if not line.startswith('#') and line.strip()]
            return env_names
        except Exception as e:
            print(f"An error occurred while processing environments list: {e}")
            return []
        
    @property
    def is_created(self) -> bool:
        check_if_exists(self.env_name)


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