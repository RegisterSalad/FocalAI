import subprocess
import os

def find_installed_environments() -> list[str]:
    """
    Finds all of the installed Anaconda environments and returns a list of their names
    """
    try:
        result = subprocess.run(['conda', 'env', 'list'], capture_output=True, text=True)
        output_lines = result.stdout.split('\n')
        env_names = [line.split()[0] for line in output_lines if line.startswith('#')]
        return env_names
    except Exception as e:
        print(f"An error occurred while finding installed environments: {e}")
        return []


# Get the absolute path of the current script directory
script_directory = os.path.dirname(os.path.abspath(__file__))

def run_subprocess_with_logging(args: str, error_message: str, logging_directory: str, log_file_name: str) -> None:
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

    def create(self) -> None:
        """
        Creates the Anaconda environment if it does not exist already.
        """
        if self.is_created:
            return

        args = ['conda', 'create', '-n', self.env_name, '-y', f'python={self.python_version}']
        error_message = f"Error occurred while creating environment '{self.env_name}'"
        run_subprocess_with_logging(args, error_message, self.logging_directory, "create_log.log")
        self.is_created = True

    def delete(self) -> None:
        """
        Deletes the Anaconda environment.
        """
        args = ['conda', 'env', 'remove', '-n', self.env_name, '-y']
        error_message = f"Error occurred while deleting environment '{self.env_name}'"
        run_subprocess_with_logging(args, error_message, self.logging_directory, "delete_log.log")
        self.is_created = False

    def conda_init(self) -> None:
        """
        Initializes Anaconda
        """
        args = ['conda', 'init']
        error_message = f"Error occurred while running 'conda init'"
        run_subprocess_with_logging(args, error_message, self.logging_directory, "init_log.log")

    def activate(self) -> None:
        """
        Activates the Anaconda environment.
        """
        if not self.is_created:
            return
        # self.conda_init()
        args = ['source', '~/.bashrc', '&&', 'conda', 'activate', self.env_name]
        error_message = f"Error occurred while activating environment '{self.env_name}'"
        run_subprocess_with_logging(args, error_message, self.logging_directory, "activate_log.log")

    def activate_by_name(self, env_name: str) -> None:
        """
        Activates the passed conda environment by name
        """
        if not self.is_created:
            return
        # self.conda_init()
        args = ['conda', 'init', '&&', 'conda', 'activate', env_name]
        error_message = f"Error occurred while activating environment '{env_name}'"
        run_subprocess_with_logging(args, error_message, self.logging_directory, "activate_log.log")

    def install_all_requirements(self) -> None:
        """
        Installs all pip requirements through pip.
        """
        if not self.is_created:
            return

        self.activate()
        args = ['pip', 'install', '-r', self.pip_list_directory]
        error_message = f"Error occurred while installing pip requirements from '{self.pip_list_directory}'"
        run_subprocess_with_logging(args, error_message, self.logging_directory, "pip_log.log")


    def __str__(self) -> str:
        if not self.is_created:
            print("Conda env not created")
            return
        """
        Provides a string representation of the CondaEnvironment object
        Returns:
            str: A summary of the environment's characteristics.
        """
        str_attributes: list = [
            f"Environment Name: {self.env_name}\n",
            f"Python Version: {self.python_version}\n",
            f"Is Created: {self.is_created}\n",
            f"PIP List Directory: {self.pip_list_directory}\n",
            f"Models: {self.models}" 
        ]

        return "".join(str_attributes)
    
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
    print(env)
    env.install_all_requirements()
    env.delete()
    print(env)