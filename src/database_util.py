import sqlite3
from conda_env import CondaEnvironment
import pickle

class Database:
    """Represents a database connection to manage Conda environments.

    Attributes:
        connection: A SQLite database connection object.
        cursor: A cursor object used to execute SQL commands.
    """
    
    def __init__(self, db_path: str) -> None:
        """Initializes the database with a connection to the specified database path."""
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self.create_table()


    def __str__(self) -> str:
        """Returns a string representation of the first 10 environments in the database."""
        self.cursor.execute("SELECT id, env_name, python_version FROM conda_environments LIMIT 10")
        rows = self.cursor.fetchall()
        environments_str = [f"ID: {row[0]}, Name: {row[1]}, Python Version: {row[2]}" for row in rows]
        return "\n".join(environments_str)

    def create_table(self) -> None:
        """Creates a table for storing Conda environments, updating the schema if necessary."""
        self.cursor.execute("DROP TABLE IF EXISTS conda_environments")  # This line drops the existing table
        self.cursor.execute('''
            CREATE TABLE conda_environments (
                id INTEGER PRIMARY KEY,
                env_name TEXT UNIQUE,
                python_version TEXT,
                serialized_env BLOB
            )
        ''')
        self.connection.commit()


    def insert_environment(self, environment: CondaEnvironment) -> None:
        """Inserts a new environment into the database if it doesn't already exist.

        Args:
            environment: The CondaEnvironment object to insert.
        """
        # Serialize the CondaEnvironment object
        serialized_env = pickle.dumps(environment)
        # Check if an environment with the same name already exists
        self.cursor.execute('SELECT env_name FROM conda_environments WHERE env_name = ?', (environment.env_name,))
        if self.cursor.fetchone() is None:
            self.cursor.execute('''INSERT INTO conda_environments(env_name, python_version, serialized_env)
                                    VALUES (?, ?, ?)''', 
                                (environment.env_name, environment.python_version, serialized_env))
            self.connection.commit()
        else:
            print(f"Environment named '{environment.env_name}' already exists. Skipping insertion.")


    def remove_duplicates(self) -> None:
        """Removes duplicate environments based on their name, keeping only the first entry."""
        # Fetch all environment names with duplicate entries
        self.cursor.execute('''SELECT env_name FROM conda_environments
                               GROUP BY env_name
                               HAVING COUNT(env_name) > 1''')
        duplicate_names = [row[0] for row in self.cursor.fetchall()]

        for name in duplicate_names:
            # For each duplicate, delete all but the first entry
            # First, select all IDs for the given duplicate name
            self.cursor.execute('''SELECT id FROM conda_environments WHERE env_name = ?''', (name,))
            ids = [row[0] for row in self.cursor.fetchall()]
            
            # Skip the first ID and delete others
            for id_to_delete in ids[1:]:
                self.cursor.execute('''DELETE FROM conda_environments WHERE id = ?''', (id_to_delete,))
        
        self.connection.commit()

    def delete_environment_by_id(self, env_id: int) -> None:
        """Deletes an environment from the database by its ID.

        Args:
            env_id: The ID of the environment to delete.
        """
        self.cursor.execute('DELETE FROM conda_environments WHERE id = ?', (env_id,))
        self.connection.commit()
        print(f"Environment with ID {env_id} has been deleted.")

    def get_environment(self, env_name: str) -> CondaEnvironment | None:
        """Retrieves a CondaEnvironment object by its name.

        Args:
            env_name: The name of the environment to retrieve.

        Returns:
            A CondaEnvironment object if found, otherwise None.
        """
        self.cursor.execute('SELECT serialized_env FROM conda_environments WHERE env_name = ?', (env_name,))
        row = self.cursor.fetchone()
        if row:
            return pickle.loads(row[0])
        return None

    def close(self) -> None:
        """Closes the database connection."""
        self.connection.close()

if __name__ == "__main__":
    import os

    def delete_environment_cli(db: Database):
        try:
            env_id = int(input("Enter the ID of the environment to delete: "))
            db.delete_environment_by_id(env_id)
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