import sqlite3
from conda_env import CondaEnvironment
import pickle
import os

class Database:
    """
    Represents a database connection to manage Conda environments. It provides functionality to interact with the
    database such as creating tables, inserting, deleting, and querying Conda environment records.

    Attributes:
        db_path (str): Path to the SQLite database file.
        connection (sqlite3.Connection): Database connection object.
        cursor (sqlite3.Cursor): Cursor object used to execute SQL commands.
    """

    def __init__(self, db_path: str) -> None:
        """
        Initializes the database connection and sets up the table for storing Conda environments.

        Args:
            db_path (str): Path to the SQLite database file.
        """
        self.db_path = db_path
        # Check if the database file exists, and print the appropriate message
        if not os.path.exists(db_path):
            print(f"Database file not found. Creating new database at: {db_path}")
        else:
            print(f"Connecting to existing database at: {db_path}")
            
        
        # Connect to the database (this will create the database file if it does not exist)
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self.create_table()
        self.str_limit = 10  # Default value for items to list in __str__
        print(f"Count: {self.count}")
    @property
    def count(self) -> int:
        """
        Retrieves the count of Conda environments currently stored in the database.

        Returns:
            int: Number of environments in the database.
        """
        try:
            self.cursor.execute("SELECT COUNT(*) FROM conda_environments")
            return self.cursor.fetchone()[0]
        except sqlite3.Error as e:
            print(f"Error counting environments: {e}")
            return 0

    def __str__(self) -> str:
        """
        Provides a string representation of the database showing a limited number of Conda environment entries.

        Returns:
            str: A string listing the environments in the database.
        """
        try:
            self.cursor.execute("SELECT * FROM conda_environments LIMIT ?", (self.str_limit,))
            environments = self.cursor.fetchall()
            env_strings = [f"ID: {env[0]}, Name: {env[1]}, Python Version: {env[2]}" for env in environments]
            return f"Conda Environments (first {self.str_limit}):\n" + "\n".join(env_strings)
        except sqlite3.Error as e:
            return f"Failed to retrieve environments: {e}"
        
    def create_table(self) -> bool:
        """
        Creates a table for storing Conda environments if it does not already exist.
        """
        
        try:
            if not self.check_for_table("conda_environments"):
                self.cursor.execute('''
                    CREATE TABLE conda_environments (
                        id INTEGER PRIMARY KEY,
                        env_name TEXT UNIQUE,
                        python_version TEXT,
                        model_type TEXT,
                        serialized_env BLOB
                    )
                ''')
                self.connection.commit()
            return True
        except sqlite3.Error:
            return False

    def check_for_table(self, table_name: str) -> bool:
        """Checks if a specified table exists."""
        try:
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (table_name,))
            return self.cursor.fetchone() is not None
        except sqlite3.Error:
            return False
    
    def create_environment(self, python_version: str, pip_list_directory: str,
                            repository_url: str, logging_directory: str) -> bool:
        """
        Creates a new CondaEnvironment and inserts it into the database.

        Args:
            python_version (str): The Python version for the new conda environment.
            pip_list_directory (str): The directory for pip requirements.
            repository_url (str): The repository url, used to create a Repository object after CondaEnvironment init.
            logging_directory (str): The directory where logging files are stored.

        Returns:
            bool: True if the environment was successfully created and inserted, False otherwise.
        """
        try:
            # Create a new CondaEnvironment object with the provided details
            new_env = CondaEnvironment(
                python_version=python_version,
                pip_list_directory=pip_list_directory,
                repository_url=repository_url,
                logging_directory=logging_directory
            )
            # Attempt to insert the new environment into the database
            return self.insert_environment(new_env)
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return False

    def insert_environment(self, environment: CondaEnvironment) -> bool:
        """
        Inserts a new Conda environment into the database.

        Args:
            environment (CondaEnvironment): The Conda environment to insert.

        Returns:
            bool: True if the insert was successful, False otherwise.
        """
        try:
            serialized_env = pickle.dumps(environment)
            self.cursor.execute('''
                INSERT INTO conda_environments (env_name, python_version, model_type, serialized_env)
                VALUES (?, ?, ?, ?)
            ''', (environment.env_name, environment.python_version, environment.repository.model_type, serialized_env))
            self.connection.commit()
            print("Insertion success")
            return True
        except sqlite3.Error:
            print("Insertion Failure")
            return False

    def delete_environment_by_id(self, env_id: int) -> bool:
        """
        Deletes an environment from the database by its unique identifier.

        Args:
            env_id (int): The unique identifier of the environment to delete.

        Returns:
            bool: True if the environment was successfully deleted, False otherwise.

        Raises:
            sqlite3.Error: If an error occurs during the database query execution.
        """
        try:
            self.cursor.execute("DELETE FROM conda_environments WHERE id = ?", (env_id,))
            self.connection.commit()
            return True
        except sqlite3.Error:
            return False

    def delete_environment_by_name(self, env_name: str) -> bool:
        """
        Deletes an environment from the database by its name.

        Args:
            env_name (str): Name of the environment to delete.

        Returns:
            bool: True if the environment was successfully deleted, False otherwise.
        """
        try:
            self.cursor.execute("DELETE FROM conda_environments WHERE env_name = ?", (env_name,))
            self.connection.commit()
            return True
        except sqlite3.Error:
            return False

    def locate_environment_by_id(self, env_id: int) -> bool:
        """
        Checks if an environment exists in the database by its unique identifier.

        Args:
            env_id (int): The unique identifier of the environment to locate.

        Returns:
            bool: True if the environment exists, False otherwise.

        Raises:
            sqlite3.Error: If an error occurs during the database query execution.
        """
        try:
            self.cursor.execute("SELECT * FROM conda_environments WHERE id = ?", (env_id,))
            return self.cursor.fetchone() is not None
        except sqlite3.Error:
            return False

    def locate_environment_by_name(self, env_name: str) -> bool:
        """
        Checks if an environment exists in the database by its name.

        Args:
            env_name (str): The name of the environment to locate.

        Returns:
            bool: True if the environment exists, False otherwise.

        Raises:
            sqlite3.Error: If an error occurs during the database query execution.
        """
        try:
            self.cursor.execute("SELECT * FROM conda_environments WHERE env_name = ?", (env_name,))
            return self.cursor.fetchone() is not None
        except sqlite3.Error:
            return False

    def get_environment_by_id(self, env_id: int) -> CondaEnvironment | None:
        """
        Retrieves a CondaEnvironment object from the database by its unique identifier.

        Args:
            env_id (int): The unique identifier of the Conda environment to retrieve.

        Returns:
            CondaEnvironment | None: The CondaEnvironment object if found; otherwise, None.

        Raises:
            sqlite3.Error: If an error occurs during the database query execution.
        """

        try:
            self.cursor.execute("SELECT serialized_env FROM conda_environments WHERE id = ?", (env_id,))
            row = self.cursor.fetchone()
            if row:
                print("Found env")
                return pickle.loads(row[0])
            print("Not found")
            return None
        except sqlite3.Error:
            return None

    def get_environment_by_name(self, env_name: str) -> CondaEnvironment | None:
        """
        Retrieves a Conda environment by its name from the database.

        Args:
            env_name (str): Name of the environment to retrieve.

        Returns:
            CondaEnvironment | None: The retrieved Conda environment or None if not found.
        """
        try:
            self.cursor.execute("SELECT serialized_env FROM conda_environments WHERE env_name = ?", (env_name,))
            row = self.cursor.fetchone()
            if row:
                print("Found env")
                return pickle.loads(row[0])
            print("Not found")
            return None
        except sqlite3.Error:
            return None

    def close(self) -> None:
        """Closes the database connection."""
        self.connection.close()

if __name__ == "__main__":
    import os

    def delete_environment_cli(db: Database) -> None:
        """
        Command-line interface function to delete an environment from the database by its ID.

        Args:
            db (Database): The database object to interact with.

        Raises:
            ValueError: If the input is not a valid integer.
        """
        try:
            env_id = int(input("Enter the ID of the environment to delete: "))
            db.delete_environment_by_id(env_id)
        except ValueError:
            print("Please enter a valid integer for the environment ID.")

    def select_environment_cli(db: Database) -> None:
        """
        Command-line interface function to fetch and display details of an environment from the database by its ID.

        Args:
            db (Database): The database object to interact with.

        Raises:
            ValueError: If the input is not a valid integer.
        """
        try:
            env_name = str(input("Enter the ID of the environment to pull from database: "))
            db.fetch_environment_by_id(env_name)
        except ValueError:
            print("Please enter a valid integer for the environment ID.")

    def main():
        """
        Main function to run the command-line interface for managing environments in the database.

        This function sets up the database connection, provides a menu for user interaction,
        and handles user commands to list, delete, or fetch environments.
        """
        db_path = os.path.abspath("/home/mldesk/Desktop/Repos/FocalAI/databases/conda_environments.db")
        db = Database(db_path)
        
        commands = {
            1: ("List first 10 environments", lambda: print(db)),
            2: ("Delete environment by ID", lambda: delete_environment_cli(db)),
        }

        while True:
            print("\nAvailable Commands:")
            for cmd in commands:
                print(f"{cmd}: {commands[cmd][0]}")
            print("-1: Exit")

            try:
                command_number = int(input("Enter command number: "))
                if command_number == -1:
                    print("Exiting...")
                    db.close()
                    break
                elif command_number in commands:
                    commands[command_number][1]()
                else:
                    print("Invalid command number.")
            except ValueError:
                print("Please enter a valid integer.")
            except Exception as e:
                print(f"An error occurred: {e}")

        db.close()  # Ensure database is closed before exiting

    main()
