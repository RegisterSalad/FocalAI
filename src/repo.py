import requests
import re
from typing import Optional
import argparse

class Repository:
    """
    Represents a GitHub repository with functionality to automatically
    fetch and parse its README for relevant installation and model information.

    Attributes:
        repo_url (str): URL of the GitHub repository.
        has_docker (bool): Indicates if the repository mentions Docker usage.
        has_install (bool): True if installation commands are found in the README.
        install_types (list[str]): Detected types of installations (e.g., pip, git clone).
        model_name (Optional[list[str] | str]): Names of models found in the repository.
        is_installed (bool): Placeholder for tracking installation status on the system.
        install_commands (list[str]): Extracted installation commands from the README.
        tables (list[str]) 
    """
    def __init__(self, repo_url: str) -> None:
        """
        Initializes the Repository object with a GitHub repo URL and fetches
        its features such as installation commands and model information.

        Parameters:
            repo_url (str): URL of the GitHub repository to analyze.
        """
        self.repo_url: str = repo_url.rstrip('/')
        self.has_docker: bool = False
        self.has_install: bool = False
        self.install_types: list[str] = []
        self.model_name: Optional[list[str] | str] = None
        self.is_installed: bool = False  # Placeholder for future functionality
        self.install_commands: list[str] = []

        # Fetch and parse repository features
        self.fetch_features()

    def fetch_features(self) -> None:
        """
        Fetch repository features from its README and update object attributes.
        """
        readme_content = self.get_readme_contents()
        if readme_content:
            self.has_docker_container(readme_content)
            self.find_install_types(readme_content)
            self.get_tables(readme_content)
            self.find_model_names(readme_content)
            commands = self.parse_commands(readme_content)
            self.install_commands = self.filter_installation_commands(commands)
            self.has_install = bool(self.install_commands)

    def get_readme_contents(self) -> Optional[str]:
        """
        Fetches the README.md content from the GitHub repository using GitHub API.

        Returns:
            Optional[str]: The README.md file content if successful, None otherwise.
        """
        api_url = f"https://api.github.com/repos/{'/'.join(self.repo_url.split('/')[-2:])}/readme"
        response = requests.get(api_url, headers={"Accept": "application/vnd.github+json"})
        if response.status_code == 200:
            download_url = response.json().get('download_url')
            if download_url:
                readme_response = requests.get(download_url)
                return readme_response.text if readme_response.status_code == 200 else None
        
        return None

    def find_install_types(self, readme_content: str) -> None:
        """
        Identifies the types of installations mentioned in the README.

        Parameters:
            readme_content (str): The content of the README file.
        """
        install_keywords = ['pip install', 'git clone', 'docker pull', 'conda install']
        self.install_types = [keyword for keyword in install_keywords if keyword in readme_content]

    def find_model_names(self, readme_content: str) -> None:
        """
        Extracts the model name from the README content, assuming it is presented
        as the first line in the format of a markdown heading.

        Parameters:
            readme_content (str): The content of the README file.
        """
        # Adjusted pattern to match the first markdown heading as the model name
        model_name_pattern = r"^# (.+)"
        match = re.search(model_name_pattern, readme_content, re.MULTILINE)
        self.model_name = match.group(1) if match else None


    def has_docker_container(self, readme_content: str) -> None:
        """
        Determines if the README mentions Docker usage, indicating a Docker container.

        Parameters:
            readme_content (str): The content of the README file.
        """
        self.has_docker = "docker" in readme_content.lower()

    def parse_commands(self, readme_content: str) -> list[str]:
        """
        Parses and extracts command lines from the README content, preserving order.

        Parameters:
            readme_content (str): The content of the README file.

        Returns:
            list[str]: A list of command strings extracted from the README.
        """
        code_block_pattern = r'```[a-z]*\n(.*?)```|^( {4,}|\t)(.*)$'
        command_lines = []
        lines = readme_content.split('\n')
        inside_code_block = False
        for line in lines:
            if line.startswith('```'):
                inside_code_block = not inside_code_block
                continue
            if inside_code_block or line.startswith(('    ', '\t')):
                command = line.strip()
                if command and not command.startswith('#'):
                    command_lines.append(command)
        return command_lines

    def get_tables(self, readme_content: str) -> None:
        """
        Finds markdown tables within the README content and stores them in a list.

        Parameters:
            readme_content (str): The content of the README file.
        """
        # Regular expression to match simple markdown tables
        table_pattern = r"\|(.+\|)+\n\|([ -:|]+)\n(\|(.+\|)+\n)+"
        self.tables = re.findall(table_pattern, readme_content, re.MULTILINE)
        # Flatten the list of tuples returned by findall into a list of strings
        self.tables = [''.join(table) for table in self.tables]


    def filter_installation_commands(self, commands: list[str]) -> list[str]:
        """
        Filters the extracted commands to retain only those relevant for installation.

        Parameters:
            commands (list[str]): A list of command strings extracted from the README.

        Returns:
            list[str]: A filtered list of installation command strings.
        """
        installation_keywords = ['git clone', 'apt install', 'apt-get install', 'pacman -S', 
                                 'brew install', 'choco install', 'scoop install', 'pip install']
        return list(set(filter(lambda cmd: any(kw in cmd for kw in installation_keywords), commands)))

    def __str__(self) -> str:
        """
        Provides a string representation of the Repository object, summarizing its
        attributes such as URL, Docker presence, installation commands, and more.

        Returns:
            str: A summary of the repository's characteristics.
        """
        attributes = [
        f"Repository URL: {self.repo_url}",
        f"Has Docker: {self.has_docker}",
        f"Has Installation Commands: {self.has_install}",
        f"Installation Types: {', '.join(self.install_types) if self.install_types else 'None'}",
        f"Model Name(s): {self.model_name if self.model_name else 'Not specified'}",
        f"Is Installed: {self.is_installed}",
        "Installation Commands:" + ("\n".join(f"\t{cmd}" for cmd in self.install_commands) if self.install_commands else "\tNone"),
        "Markdown Tables:\n" + ("\n\n".join(self.tables) if self.tables else "\tNone")
        ]
        return "\n".join(attributes)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch Ubuntu installation commands from a GitHub repository.")
    parser.add_argument("repo_url", type=str, help="URL to the GitHub repository")
    args = parser.parse_args()
    repo_url = args.repo_url
    repo = Repository(repo_url=repo_url)
    print(repo)