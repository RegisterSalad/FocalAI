import os
import logging
import sys
# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_base_dir():
    """Determine and return the base path of the application."""
    if getattr(sys, 'frozen', False):
        # The application is frozen
        return os.path.dirname(sys.executable)
    else:
        # The application is not frozen
        return os.path.dirname(__file__)


# Base directory where your application resides
BASE_DIR = get_base_dir()
print(__file__)
# Child-level Directories
LOG_DIR = os.path.join(BASE_DIR, 'logs')
DATA_DIR = os.path.join(BASE_DIR, 'data')
TEMP_DIR = os.path.join(BASE_DIR, 'temp')
REPORTS_DIR = os.path.join(BASE_DIR, 'reports')
USER_SCRIPTS_DIR = os.path.join(BASE_DIR, 'user_scripts')
USER_GEN_DIR = os.path.join(BASE_DIR, 'user_gen')

# Grandchild-level directory
DRAG_N_DROP_DIR = os.path.join(TEMP_DIR, 'drag_n_drop') # Stores the file for the drag and drop module
REPO_JSONS_DIR = os.path.join(DATA_DIR, 'repo_jsons') # Stores the repository jsons directory
RUN_LOG_DIR = os.path.join(LOG_DIR, 'run_logs')
BUILD_LOG_DIR = os.path.join(LOG_DIR, 'build') # Stores the data for app build process
KEYS_DIR = os.path.join(USER_GEN_DIR, 'keys')

# Leaf file paths
DB_PATH = os.path.join(DATA_DIR, 'conda_environments.db') # Stores the data for the database of environments. Logic exists within the DatabaseManager to create the db file as needed
CALL_LOG = os.path.join(LOG_DIR, 'call.log') # Stores the data for the Anaconda environment calls
CREATE_LOG = os.path.join(LOG_DIR, 'create.log') # Stores the data for the Anaconda environment creation runs
DELETE_LOG = os.path.join(LOG_DIR, 'delete.log') # Stores the data for the Anaconda environment deletion runs
ENV_LIST_LOG = os.path.join(LOG_DIR, 'env_list_log.log') # Stores the data for the current shell env list runs
OPENAI_KEY_TXT = os.path.join(KEYS_DIR, 'openai_key.txt')
PWC_KEY_TXT = os.path.join(KEYS_DIR, 'pwc_key.txt')
# Function to create directories safely
def create_directory(path):
    try:
        os.makedirs(path, exist_ok=True)
        logging.info(f"Directory created or verified: {path}")
    except OSError as e:
        logging.error(f"Failed to create directory {path}: {e}")

# Ensure directories exist
directories = [
    LOG_DIR, DATA_DIR, TEMP_DIR, REPORTS_DIR, USER_SCRIPTS_DIR, USER_GEN_DIR, BUILD_LOG_DIR,
    DRAG_N_DROP_DIR, REPO_JSONS_DIR, RUN_LOG_DIR, KEYS_DIR
]
# Function to create directories safely
def create_directories(directory_list):
    for path in directory_list:
        try:
            os.makedirs(path, exist_ok=True)
            logging.info(f"Directory created or verified: {path}")
        except OSError as e:
            logging.error(f"Failed to create directory {path}: {e}")

# Ensure directories exist
create_directories(directories)

# # Check and log information about key files
# if os.path.isdir(KEYS_DIR):
#     logging.info(f"Key directory path ready: {KEYS_DIR}")
# else:
#     logging.error(f"Key directory does not exist: {KEYS_DIR}")

# # Display the database path for debugging purposes
# if os.path.isdir(os.path.dirname(DB_PATH)):
#     logging.info(f"Database path ready: {DB_PATH}")
# else:
#     logging.error(f"Database directory does not exist: {os.path.dirname(DB_PATH)}")

