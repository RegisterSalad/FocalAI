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
        super().__init__()
        self.client = None
        self.init_pwc_client()

    def init_pwc_client(self):
        api_key = self.get_and_save_key("pwc")
        if api_key:
            self.client = PapersWithCodeClient(token=api_key)
        else:
            raise ValueError("PWC KEY not found")

    def get_and_save_key(self, key_type: str) -> str | None:
        key_file = OPENAI_KEY_TXT if key_type == 'openai' else PWC_KEY_TXT
        validate_api_key = self.is_openai_api_key_valid if key_type == 'openai' else self.is_pwc_api_key_valid

        if os.path.isfile(key_file):
            with open(key_file, 'r') as file:
                return file.read().strip()

        while not self.abort_flag:
            api_key, ok = QInputDialog.getText(self, 'Key Request', 'Please enter your API key:')
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
        Fetches the README content from a GitHub repository.
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
        Retrieves a list of repositories based on a query.
        """
        if query is not None:
            return self.client.repository_list(name=query)

    def is_openai_api_key_valid(self, api_key: str) -> bool:
        url = "https://api.openai.com/v1/engines"
        headers = {"Authorization": f"Bearer {api_key}"}
        try:
            response = requests.get(url, headers=headers)
            return response.status_code == 200
        except requests.RequestException:
            return False

    def is_pwc_api_key_valid(self, api_key: str) -> bool:
        temp = PapersWithCodeClient(token=api_key)
        try:
            test = temp.repository_list(name="whisper")
            return True
        except Exception as e:
            print(e)
            return False


