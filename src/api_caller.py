import re
import os
import sys
import requests  # Import requests for synchronous HTTP calls
from paperswithcode import PapersWithCodeClient
from paperswithcode.models.repository import Repositories
from PySide6.QtWidgets import (QWidget, QInputDialog, QMessageBox) # This module has frontend components but is not part of the frontend_build

module_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if module_dir not in sys.path:
    sys.path.append(module_dir)

from directories import PWC_KEY_TXT
from directories import OPENAI_KEY_TXT

class APIManager(QWidget):
    """
    Manages API interactions and key validations, including interfacing with specific APIs.

    Attributes:
        api_type (str): Type of API, 'openai' or 'pwc' to handle different APIs.
        client (PapersWithCodeClient | None): API client for PapersWithCode, or other clients for different APIs.
    """
    abort_flag: bool = False

    def __init__(self):
        """
        Initializes an instance of the APIManager class. This constructor sets up the client for the PapersWithCode API by calling the init_pwc_client method, which handles API key retrieval and client initialization.
        """
        super().__init__()
        self.client = None
        self.init_pwc_client()

    def init_pwc_client(self):
        """
        Initializes the PapersWithCode client using an API key stored in a local file or obtained through user input.
        Raises an exception if the API key is not found or the client cannot be initialized.
        """
        api_key = self.get_and_save_key("pwc")
        if api_key:
            self.client = PapersWithCodeClient(token=api_key)
        else:
            raise ValueError("PWC KEY not found")
    
    def get_and_save_key(self, key_type: str) -> str | None:
        """
        Retrieves and saves the API key from a file or through user input validation.

        Args:
            key_type (str): Specifies the type of API key to retrieve ('openai' or 'pwc').

        Returns:
            str | None: Returns the API key if found or validated, None if the operation is aborted or fails.
        """
        key_file = OPENAI_KEY_TXT if key_type == 'openai' else PWC_KEY_TXT
        key_name = "Open AI" if key_type == 'openai' else "Papers With Code"
        validate_api_key = self.is_openai_api_key_valid if key_type == 'openai' else self.is_pwc_api_key_valid

        if os.path.isfile(key_file):
            with open(key_file, 'r') as file:
                return file.read().strip()

        while not self.abort_flag:
            api_key, ok = QInputDialog.getText(self, 'Key Request', f'Please enter your {key_name} API key:')
            if ok and validate_api_key(api_key):
                with open(key_file, 'w') as file:
                    file.write(api_key)
                return api_key
            elif not ok:
                self.abort_flag = True
                return None
            else:
                QMessageBox.warning(self, "Invalid Key", "The provided API key is invalid, please try again.")
                
    @staticmethod
    def get_readme_contents(repo_url: str) -> str | None:
        """
        Retrieves the README.md content of a GitHub repository using the GitHub API.

        Args:
            repo_url (str): The URL of the GitHub repository from which to fetch the README content.

        Returns:
            str | None: The content of the README file if successful, None if the operation fails.
        """
        parts = repo_url.rstrip('/').split('/')
        repo_owner, repo_name = parts[-2], parts[-1]
        api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/readme"
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            download_url = data.get('download_url')
            if download_url:
                readme_response = requests.get(download_url)
                if readme_response.status_code == 200:
                    return readme_response.text
        return None

    def get_repo_list(self, query: str = None) -> Repositories | None:
        """
        Fetches a list of repositories matching a specific query from PapersWithCode.

        Args:
            query (str): A search term to filter the repositories. Optional.

        Returns:
            Repositories | None: An object containing repository data if successful, None if no data found or an error occurs.
        """
        if query is not None:
            return self.client.repository_list(name=query)

    def is_openai_api_key_valid(self, api_key: str) -> bool:
        """
        Validates a PapersWithCode API key by making a test request using the client.

        Args:
            api_key (str): The API key to validate.

        Returns:
            bool: True if the API key is valid and the test request succeeds, False otherwise.
        """
        url = "https://api.openai.com/v1/engines"
        headers = {"Authorization": f"Bearer {api_key}"}
        try:
            response = requests.get(url, headers=headers)
            return response.status_code == 200
        except requests.RequestException:
            return False

    def is_pwc_api_key_valid(self, api_key: str) -> bool:
        """
        Validates a PapersWithCode API key by making a test request using the client.

        Args:
            api_key (str): The API key to validate.

        Returns:
            bool: True if the API key is valid and the test request succeeds, False otherwise.
        """
        temp = PapersWithCodeClient(token=api_key)
        try:
            test = temp.repository_list(name="whisper")
            return True
        except Exception as e:
            print(e)
            return False


