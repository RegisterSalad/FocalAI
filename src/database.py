from database_util import Database
from conda_env import CondaEnvironment
import os
def main() -> None:
    # Define the parameters for the new Conda environment
    python_version = "3.11.5"
    models = ["example_model"]
    repository_name = "my_test_env"
    pip_list_directory = os.path.abspath("../pip_reqs/requirements.txt")
    logging_directory = os.path.abspath("../logging")
    
    # Create an instance of CondaEnvironment
    env = CondaEnvironment(python_version, models, repository_name, pip_list_directory, logging_directory)
    
    # Create the Conda environment
    env.create()
    
    # Initialize the Database object, pointing to your .db file
    db_path = os.path.abspath('../databases/conda_environments.db')
    db = Database(db_path)
    
    # Insert the created environment into the database
    db.insert_environment(env)
    
    # Retrieve the environment from the database (optional, to verify insertion)
    retrieved_env = db.get_environment(repository_name)
    if retrieved_env:
        print(f"Retreived Environment: \n {retrieved_env}")
    else:
        print("Environment not found in the database.")
    
    print(db)

    # Close the database connection
    db.close()

if __name__ == "__main__":
    main()