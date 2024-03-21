import re
import requests  # Import requests for synchronous HTTP calls
from typing import List
from paperswithcode import PapersWithCodeClient
from paperswithcode.models.repository import Repositories, Repository
from paperswithcode.models.paper import Paper
from secret import PWC_KEY 

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

    def extract_code_blocks(self, markdown_content: str) -> List[str]:
        """
        Extract code blocks from Markdown content.

        Args:
            markdown_content (str): The Markdown content.

        Returns:
            List[str]: A list of code blocks.
        """
        code_blocks = re.findall(r'```[\s\S]+?```', markdown_content)
        return code_blocks

    def check_for_install(self, code_block: str) -> bool:
        """
        Check if a code block contains an installation command.

        Args:
            code_block (str): The code block to check.

        Returns:
            bool: True if an installation command is found, False otherwise.
        """
        return bool(re.search(r'\binstall\b', code_block, re.IGNORECASE))

    def extract_commands(self, install_blocks: List[str]) -> List[str]:
        """
        Extract commands from code blocks.

        Args:
            install_blocks (List[str]): List of code blocks.

        Returns:
            List[str]: List of extracted commands.
        """
        commands = []
        for block in install_blocks:
            lines = block.strip('```').strip().split('\n')
            for line in lines:
                if not line.strip().startswith('#') and line.strip() and not re.search(r'\bbash\b', line, re.IGNORECASE):
                    commands.append(line.strip())
        return commands

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

    def find_paper_from_selected_repo(self, selected_index: int, repo_list: Repositories) -> Paper | None:
        if selected_index < len(repo_list.results):
            repo: Repository = repo_list.results[selected_index]
            if repo.description:
                paper_query = repo.description
                papers = self.client.paper_list(title=paper_query).results
                if papers:
                    return papers[0]
        return None

    def print_repo_list(self, repo_list: Repositories) -> None:
        """
        Print the list of repositories.

        Args:
            repo_list (Repositories): The list of repositories.
        """
        for idx, repo in enumerate(repo_list.results):
            print(f"ID: [{idx}]\n{repo.name}\n{repo.owner}\n{repo.description}\n{repo.url}\n{'-' * 10}\n\n")

def main():
    api_caller = APICaller()
    repo_link = "https://github.com/openai/whisper"  # Test repo link
    readme = api_caller.get_readme_contents(repo_url=repo_link)
    if readme:
        code_blocks = api_caller.extract_code_blocks(readme)
        install_commands = [command for block in code_blocks if api_caller.check_for_install(block)
                            for command in api_caller.extract_commands([block])]
        for command in install_commands:
            print(command)

        repo_list = api_caller.get_repo_list(query="whisper")
        if isinstance(repo_list, Repositories):
            api_caller.print_repo_list(repo_list)
            selected_idx = int(input("Enter Selected Repo: "))
            paper = api_caller.find_paper_from_selected_repo(selected_index=selected_idx, repo_list=repo_list)
            if paper:
                print(f"Paper Found:\nTitle: {paper.title}\nAuthors: {paper.authors}\n{'-' * 10}\n\n")

if __name__ == "__main__":
    main()