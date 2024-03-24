from database_util import Database
from conda_env import CondaEnvironment, check_if_exists
import os
from typing import Any, Dict, Callable, Tuple

class DatabaseManager(Database):
    def __init__(self, db_path: str) -> None:
        """
        Initialize the DatabaseManager with error checking for database path.

        Ensures the directory for the database exists and is accessible. If the
        directory does not exist, it attempts to create it. Raises an exception
        if the directory cannot be created.

        Parameters:
        - db_path: The file system path to the SQLite database file.

        Raises:
        - Exception: If the directory does not exist and cannot be created.
        """
        # Convert the relative path to an absolute path to ensure correctness
        self.db_path = os.path.abspath(db_path)
        
        # Check if the database directory exists; if not, attempt to create it
        db_directory = os.path.dirname(self.db_path)
        if not os.path.exists(db_directory):
            try:
                os.makedirs(db_directory)
            except Exception as e:
                raise Exception(f"Failed to create the database directory: {e}")
        self.running_env: CondaEnvironment | None = None
        self.is_running = False
        # Proceed with the original initialization from the parent class
        super().__init__(self.db_path)

    def __call__(self) -> None:
        """
        Execute the main application loop.

        Continuously displays the main menu and processes user input until
        the application is terminated by setting `is_running` to False.
        """
        self.is_running = True
        while self.is_running:
            self.option_interactor(self.main_menu_options)

    def option_interactor(self, options: Dict[int, Tuple[str, Callable[..., Any]]]) -> None:
        """
        Interact with the user to select and execute an option.

        This method displays available options and prompts the user to select one.
        It validates the user's input and executes the corresponding function
        associated with the selected option.

        Args:
            options: A dictionary mapping option numbers to tuples of option description
                    and the function to execute.
        """
        print("\nAvailable Options:")
        for option_number, option_info in options.items():
            print(f"{option_number}: {option_info[0]}")

        try:
            option_number = int(input("Enter option number: "))
            if option_number in options:
                options[option_number][1]()
            else:
                print("Invalid option number.")
        except ValueError:
            print("Please enter a valid integer.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def fetch_env_to_run_cli(self) -> None:
        """
        Display all environments and allow selection for operation.

        This method displays all available environments and prompts the user
        to select one by entering its ID. It validates the input and sets the
        selected environment for further operations. If the database is empty,
        it notifies the user accordingly.

        Raises:
        - VauleError: if environment is not found or if invalid ID is entered
        """
        if self.row_count == 0:
            print("Database is empty, insert a CondaEnvironment before continuing")
            return

        print(self)
        while True:
            try:
                env_id = str(input("Enter the ID of the environment to fetch (-1 to exit): "))
                if env_id == -1:
                    break
                self.running_env = self.get_environment(env_id)
                if not isinstance(self.running_env, CondaEnvironment):
                    raise ValueError("Invalid environment ID.")
                self.running_env.env_id = env_id
                break
            except ValueError as e:
                print(e)

        self.option_interactor(self.selected_env_options)

    def run_command_cli(self) -> None:
        """
        Execute a command within the selected environment.

        Prompts the user for a command to run within the context of the currently
        selected environment. The command is executed, and its output is logged.
        """
        command = input(
            f"Working directory is: {os.getcwd()}\n"
            f"Input command to run in {self.running_env.env_name}:\n"
        )
        self.running_env(command) # This runs the command and logs output

    def run_command(self, input_command: str) -> bool:
        if not isinstance(self.running_env, CondaEnvironment):
            print("Error: No running environments")
            return
        return self.running_env(input_command) # This runs the command and logs output

    def exit_dbm(self) -> None:
        """
        Terminate the database manager.

        Stops the main application loop and closes the database connection.
        """
        self.is_running = False
        self.close()

    def create_environment_cli(self) -> None:
        """
        Captures user input to create a Conda environment with validation.

        Environment attributes are prompted for one by one:
        - python_version (str): The Python version of the conda environment
        - pip_list_directory (str): The location of the pip requirements
        - models (str | list[str]): The names of the models currently installed
        - repository_name (str): Name of the repository, will be the name of the associated conda environment
        - logging_directory (str): Directory where logging files are created and stored.
        """
        print("Enter the name of the repository (will also be the environment name):")
        repository_name = input()
        import re
        print("Enter Python version for the conda environment (e.g., 3.8):")
        while True:
            python_version = input()
            if re.match(r'^\d+(\.\d+){1,2}$', python_version):
                break
            print("Invalid Python version. Please use the format: major.minor[.micro]")

        print("Enter the directory for pip requirements (e.g., ./pip_reqs):")
        pip_list_directory = input()

        print("Enter the names of the models currently installed (comma separated for multiple, leave empty if none):")
        models_input = input()
        models = models_input.split(",") if models_input else []

        

        print("Enter the directory where logging files will be created and stored (e.g., ./logging):")
        logging_directory = input()

        # Create the environment using the collected information
        try:
            new_env = CondaEnvironment(
                python_version=python_version, 
                models=models, 
                repository_name=repository_name, 
                pip_list_directory=pip_list_directory, 
                logging_directory=logging_directory
            )
            self.insert_environment(new_env)
            print(f"Environment '{repository_name}' created and inserted successfully.")
        except Exception as e:
            print(f"Failed to create environment: {e}")

    def delete_running_env(self) -> bool:
        if not isinstance(self.running_env, CondaEnvironment):
            print("Error: No running environments")
            return
        self.running_env.delete() # Delete environment from system
        return super().delete_environment_by_id(self.running_env.env_id) # Delete environment from database

    @property
    def main_menu_options(self) -> Dict[int, Tuple[str, Callable[..., Any]]]:
        """
        Property of DatabaseManager, returns main menu options for printing and execution

        Returns:
            options (Dict[int, Tuple[str, Callable[..., Any]]]): Dict with options and associated methods 
        """
        options = {
            1: ("Create Environment", self.create_environment_cli),
            2: ("Display All Environments", lambda: print(self)),
            3: ("Select Environment", self.fetch_env_to_run_cli),
            4: ("Exit", self.exit_dbm),
            5: ("Cleanup", self.remove_duplicates) 
        }
        return options

    @property
    def selected_env_options(self) -> Dict[int, Tuple[str, Callable[..., Any]]]:
        """
        Returns the 'Selected Environment' sub-menu options as a dict

        Returns:
            options (Dict[int, Tuple[str, Callable[..., Any]]]): Dict with options and associated methods
        """
        options = {
            1: ("Delete Environment",  self.delete_environment_by_id),
            2: ("Run Command in Environment", self.run_command_cli),
            3: ("Print Environment Info", lambda: str(self.running_env)),
            4: ("Back to Main Menu", print(end=""))
        }
        return options

if __name__ == "__main__":
    db_path = os.path.abspath('../databases/conda_environments.db')
    db = DatabaseManager(db_path)
    db()