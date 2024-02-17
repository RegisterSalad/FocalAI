import subprocess
import os

class CondaEnvironment:
    """
    Represents an Anaconda environment
    Attributes:
        python_version (str): The Python version of the conda environment
        is_created (bool): A result of the check that finds if the environment is already part of the system
        pip_list_directory (str): The location of the pip requirements
        models (str | list[str]): The names of the models currently installed
        repository_name (str): Name of the repository, will be the name of the associated conda environment
        logging_directory (str): Directory where logging files are create and stored.
    """
    def __init__(self, python_version: str, models: str | list[str], repository_name: str, pip_list_directory: str = "../pip_reqs", logging_directory: str = "../logging") -> None:
        self.python_version = python_version
        self.is_created = False
        self.pip_list_directory = pip_list_directory
        self.models = models
        self.env_name = repository_name
        self.logging_directory = logging_directory
        self.bash_scipt_dir = os.path.abspath("bash_scripts")

    def create(self) -> None:
        """
        Creates the Anaconda environment if it does not exist already.
        """
        if self.is_created:
            return

        args = ['conda', 'create', '-n', self.env_name, '-y', f'python={self.python_version}']
        error_message = f"Error occurred while creating environment '{self.env_name}'"
        self.run_subprocess_with_logging(args, error_message, self.logging_directory, "create_log.log")
        self.is_created = True

    def delete(self) -> None:
        """
        Deletes the Anaconda environment.
        """
        args = ['conda', 'env', 'remove', '-n', self.env_name, '-y']
        error_message = f"Error occurred while deleting environment '{self.env_name}'"
        self.run_subprocess_with_logging(args, error_message, self.logging_directory, "delete_log.log")
        self.is_created = False

    def conda_init(self) -> None:
        """
        Initializes Anaconda
        """
        args = ['conda', 'init']
        error_message = f"Error occurred while running 'conda init'"
        self.run_subprocess_with_logging(args, error_message, self.logging_directory, "init_log.log")

    def activate(self) -> None:
        raise NotImplemented

    def activate_by_name(self, env_name: str) -> None:
        """
        Activates the Anaconda environment using a bash script.

        Args:
            env_name (str): Name of the Anaconda environment to be activated
        """
        if not self.is_created:
            return

        activate_script_path = self.bash_scipt_dir + "/activate_conda_env.sh"
        args = ['bash', activate_script_path, env_name]
        error_message = f"Error occurred while activating environment '{env_name}'"
        self.run_subprocess_with_logging(args, error_message, self.logging_directory, "activate_log.log")

    def install_all_requirements(self) -> None:
        """
        Installs all pip requirements through pip within the conda environment using 'conda run',
        leveraging the dedicated subprocess function for execution and logging.
        """
        if not self.is_created:
            print("Environment is not created. Please create the environment before installing requirements.")
            return

        # Construct the command to run 'pip install' within the conda environment
        args = ['conda', 'run', '-n', self.env_name, 'pip', 'install', '-r', self.pip_list_directory]
        error_message = f"Error occurred while installing pip requirements from '{self.pip_list_directory}'"

        # Use the dedicated subprocess function for execution and logging
        self.run_subprocess_with_logging(args, error_message, self.logging_directory, "pip_log.log")

    def __str__(self) -> str:
        if not self.is_created:
            return "Conda env not created"
        """
        Provides a string representation of the CondaEnvironment object
        Returns:
            str: A summary of the environment's characteristics.
        """
        str_attributes: list = [
            f"Environment Name: {self.env_name}",
            f"Python Version: {self.python_version}",
            f"Is Created: {self.is_created}",
            f"PIP List Directory: {self.pip_list_directory}",
            f"Models: {self.models}" 
        ]

        return "\n".join(str_attributes)
    
    def test_environment(self) -> bool:
        """
        Tests if running commands in the conda environment is successful by executing a simple command.
        Returns True if the command executes successfully and False otherwise.
        """
        if not self.is_created:
            print("Environment is not created. Please create the environment before testing.")
            return False

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

    def run_subprocess_with_logging(self, args: str, error_message: str, logging_directory: str, log_file_name: str) -> None:
        """
        Runs a subprocess with the given arguments and logs the output and any errors encountered.

        Args:
            args (list[str]): The list of arguments to pass to the subprocess.
            error_message (str): The error message to display if the subprocess encounters an error.
            logging_directory (str): The directory to store logging information.
        """
        try:
            log_file_path = os.path.join(logging_directory, log_file_name)
            with open(log_file_path, 'w') as log_file:
                command = " ".join(args)
                print(f"Tried: {command}")
                subprocess.run(command, check=True, stdout=log_file, stderr=subprocess.STDOUT,  shell=True)
        except subprocess.CalledProcessError as e:
            print(f"{error_message}: {e}")

    def find_installed_environments(self, logging_directory="../logging") -> list[str]:
        """
        Finds all of the installed Anaconda environments and returns a list of their names using the dedicated
        subprocess function with logging.

        Args:
            logging_directory (str): The directory where the log file will be saved.
        """
        log_file_name = "env_list_log.log"
        args = ['conda', 'env', 'list']

        # Execute the command and log its output
        self.run_subprocess_with_logging(args, "Error finding installed environments", logging_directory, log_file_name)

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

if __name__ == "__main__":
    # Get the absolute path of the logging directory
    logging_directory = os.path.abspath("../logging")
    requirements_directory = os.path.abspath("../pip_reqs")
    log_file_name = "logfile.log"


    # Create a CondaEnvironment instance
    env = CondaEnvironment(
        python_version="3.11.5",
        pip_list_directory=os.path.join(requirements_directory, "requirements.txt"),
        models=[],
        logging_directory=logging_directory,
        repository_name="TestRepo"
    )

    # Test your methods
    env.create()
    env.install_all_requirements()
    env.test_environment()
    print(env)
    # env.delete()
    # print(env)