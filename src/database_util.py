import sqlite3
from conda_env import CondaEnvironment
import pickle

class Database:
    """Represents a database connection to manage Conda environments."""

    def __init__(self, db_path: str) -> None:
        """Initializes the database with a connection to the specified path."""
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self) -> bool:
        """Creates a table for Conda environments if it doesn't exist."""
        try:
            if not self.check_for_table("conda_environments"):
                self.cursor.execute('''
                    CREATE TABLE conda_environments (
                        id INTEGER PRIMARY KEY,
                        env_name TEXT UNIQUE,
                        python_version TEXT,
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
                           models: list[str], repository_name: str, logging_directory: str) -> bool:
        """
        Creates a new CondaEnvironment and inserts it into the database.

        Args:
            python_version (str): The Python version for the new conda environment.
            pip_list_directory (str): The directory for pip requirements.
            models (list[str]): The names of models currently installed.
            repository_name (str): The repository name, used as the environment name.
            logging_directory (str): The directory where logging files are stored.

        Returns:
            bool: True if the environment was successfully created and inserted, False otherwise.
        """
        try:
            # Create a new CondaEnvironment object with the provided details
            new_env = CondaEnvironment(
                python_version=python_version,
                pip_list_directory=pip_list_directory,
                models=models,
                repository_name=repository_name,
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
        """Inserts a new Conda environment."""
        try:
            serialized_env = pickle.dumps(environment)
            self.cursor.execute('''
                INSERT INTO conda_environments (env_name, python_version, serialized_env)
                VALUES (?, ?, ?)
            ''', (environment.env_name, environment.python_version, serialized_env))
            self.connection.commit()
            return True
        except sqlite3.Error:
            return False

    def delete_environment_by_id(self, env_id: int) -> bool:
        """Deletes an environment by its ID."""
        try:
            self.cursor.execute("DELETE FROM conda_environments WHERE id = ?", (env_id,))
            self.connection.commit()
            return True
        except sqlite3.Error:
            return False

    def delete_environment_by_name(self, env_name: str) -> bool:
        """Deletes an environment by its name."""
        try:
            self.cursor.execute("DELETE FROM conda_environments WHERE env_name = ?", (env_name,))
            self.connection.commit()
            return True
        except sqlite3.Error:
            return False

    def locate_environment_by_id(self, env_id: int) -> bool:
        """Locates an environment by its ID."""
        try:
            self.cursor.execute("SELECT * FROM conda_environments WHERE id = ?", (env_id,))
            return self.cursor.fetchone() is not None
        except sqlite3.Error:
            return False

    def locate_environment_by_name(self, env_name: str) -> bool:
        """Locates an environment by its name."""
        try:
            self.cursor.execute("SELECT * FROM conda_environments WHERE env_name = ?", (env_name,))
            return self.cursor.fetchone() is not None
        except sqlite3.Error:
            return False

    def get_environment_by_id(self, env_id: int) -> CondaEnvironment | None:
        """Retrieves a CondaEnvironment by its ID."""
        try:
            self.cursor.execute("SELECT serialized_env FROM conda_environments WHERE id = ?", (env_id,))
            row = self.cursor.fetchone()
            if row:
                return pickle.loads(row[0])
            return None
        except sqlite3.Error:
            return None

    def get_environment_by_name(self, env_name: str) -> CondaEnvironment | None:
        """Retrieves a CondaEnvironment by its name."""
        try:
            self.cursor.execute("SELECT serialized_env FROM conda_environments WHERE env_name = ?", (env_name,))
            row = self.cursor.fetchone()
            if row:
                return pickle.loads(row[0])
            return None
        except sqlite3.Error:
            return None

    def close(self) -> None:
        """Closes the database connection."""
        self.connection.close()

if __name__ == "__main__":
    import os

    def delete_environment_cli(db: Database) -> None:
        try:
            env_id = int(input("Enter the ID of the environment to delete: "))
            db.delete_environment_by_id(env_id)
        except ValueError:
            print("Please enter a valid integer for the environment ID.")

    def select_environment_cli(db: Database) -> None:
        try:
            env_name = str(input("Enter the ID of the environment to pull from database: "))
            db.fetch_environment_by_id(env_name)
        except ValueError:
            print("Please enter a valid integer for the environment ID.")

    def main():
        db_path = os.path.abspath('../databases/conda_environments.db')
        db = Database(db_path)
        
        commands = {
            1: ("Remove duplicates", db.remove_duplicates),
            2: ("List first 10 environments", lambda: print(db)),
            3: ("Delete environment by ID", lambda: delete_environment_cli(db)),
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