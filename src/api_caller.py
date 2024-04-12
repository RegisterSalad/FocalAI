import re
import requests  # Import requests for synchronous HTTP calls
from typing import List
from paperswithcode import PapersWithCodeClient
from paperswithcode.models.repository import Repositories, Repository
from paperswithcode.models.paper import Paper
from secret import PWC_KEY
import io

class APICaller:
    """
    Interacts with the PapersWithCode API.

    Attributes:
        client (PapersWithCodeClient): API client.
    """

    def __init__(self) -> None:
        """
        Initialize the API caller with a PapersWithCode client.
        """
        self.client = PapersWithCodeClient(token=PWC_KEY)

    def get_readme_contents(self, repo_url: str) -> str | None:
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
        Get a list of repositories from PapersWithCode.

        Args:
            query (str, optional): Query string to filter repositories. Defaults to None.

        Returns:
            Repositories | None: A list of repositories.
        """
        if query is not None:
            return self.client.repository_list(name=query)


def main():
    api_caller = APICaller()
    repo_link = "https://github.com/openai/whisper"  # Test repo link
    readme = api_caller.get_readme_contents(repo_url=repo_link)
    if readme:
        code_blocks = api_caller.extract_code_blocks(readme)

        install_commands = [command for block in code_blocks if api_caller.check_for_install(block)
                            for command in api_caller.extract_commands([block])]
        """ for command in install_commands:
            print(command)"""

        """repo_list = api_caller.get_repo_list(query="whisper")
        if isinstance(repo_list, Repositories):
            api_caller.print_repo_list(repo_list)
            selected_idx = int(input("Enter Selected Repo: "))
            paper = api_caller.find_paper_from_selected_repo(selected_index=selected_idx, repo_list=repo_list)
            if paper:
                print(f"Paper Found:\nTitle: {paper.title}\nAuthors: {paper.authors}\n{'-' * 10}\n\n")
"""
if __name__ == "__main__":
    main()
