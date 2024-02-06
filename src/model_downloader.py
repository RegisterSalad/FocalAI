import argparse
import requests
from typing import List, Optional
import re
from repo import Repository



class UbuntuCommandFetcher:
    """Fetch Ubuntu installation commands from a README file using a GitHub repo URL."""

    def __init__(self, repo_url: str) -> None:
        """Initialize with URL to the GitHub repository."""
        self.repo_url: str = repo_url
        self.commands: List[str] = []

    def fetch_readme(self) -> Optional[str]:
        """Fetch README content."""
        readme_content = self.get_readme_contents(self.repo_url)
        if readme_content:
            return readme_content
        else:
            print("Failed to fetch README.md content.")
            return None
        
    def find_install_types(self, readme_content: str) -> None:
        """
        Determine the installation types mentioned in the README content.

        This method updates the `install_types` attribute of the class based on
        keywords found in the README content.

        Args:
            readme_content (str): The content of the README file.
        """
        install_keywords = ['pip install', 'git clone', 'docker pull', 'conda install']
        self.install_types = [keyword for keyword in install_keywords if keyword in readme_content]
    
    def find_model_names(self, readme_content: str) -> None:
        """
        Extract model names from the README content.

        This method updates the `model_name` attribute of the class with model names
        found in the README. The implementation needs to be adapted based on the
        specific patterns used to mention model names in READMEs.

        Args:
            readme_content (str): The content of the README file.
        """
        # Placeholder implementation: adapt regex based on actual README patterns
        model_name_pattern = r"Model name:\s*([^\n,]+)"
        matches = re.findall(model_name_pattern, readme_content)
        self.model_name = matches if len(matches) > 1 else matches[0] if matches else None

    def has_docker_container(self, readme_content: str) -> None:
        """
        Check if the README content mentions a Docker container.

        This method updates the `has_docker` attribute of the class based on
        whether Docker-related keywords are found in the README content.

        Args:
            readme_content (str): The content of the README file.
        """
        self.has_docker = "docker" in readme_content.lower()

    def parse_commands(self, readme_content: str) -> list:
        """
        Parse command lines from the README content, preserving their original order.

        Args:
            readme_content (str): The content of the README file.

        Returns:
            list: A list of parsed command strings, in the order they appear in the README.
        """
        # Regular expression to match command lines within code blocks
        code_block_pattern = r'```[a-z]*\n(.*?)```|^( {4,}|\t)(.*)$'  # Matches fenced code blocks and indented lines
        command_lines = []

        # Split README content by lines to maintain order
        lines = readme_content.split('\n')
        inside_code_block = False
        for line in lines:
            if line.startswith('```'):  # Detect start/end of fenced code block
                inside_code_block = not inside_code_block
                continue  # Skip the line that starts or ends a code block
            if inside_code_block or line.startswith(('    ', '\t')):  # Check if line is inside a code block or indented
                command = line.strip()
                if command and not command.startswith('#'):  # Exclude commented lines
                    command_lines.append(command)
            elif not inside_code_block and re.match(code_block_pattern, line):
                # Handle single-line commands that might be outside standard blocks but are indented
                command = line.strip()
                if command and not command.startswith('#'):
                    command_lines.append(command)

        return command_lines

    def filter_installation_commands(self, commands: list) -> list:
        """
        Filter the extracted commands to keep only installation commands.

        Args:
            commands (list): A list of extracted command strings.

        Returns:
            list: A filtered list of command strings that are installation commands.
        """
        filtered_commands = []
        installation_keywords = ['git clone', 'apt install', 'apt-get install', 'pacman -S', 'brew install', 'choco install', 'scoop install', 'pip install']
        
        for command in commands:
            if any(keyword in command for keyword in installation_keywords):
                filtered_commands.append(command)
                
        return list(set(filtered_commands))  # Remove duplicates

    def __call__(self) -> list:
        """
        Execute fetching, parsing, and filtering to return installation commands.

        Returns:
            list: A list of filtered Ubuntu installation commands found in the README.
        """
        self.commands = []  # Reset commands list
        readme_content = self.fetch_readme()
        if readme_content:
            self.commands = self.parse_commands(readme_content)
            # Now filter the extracted commands to keep only installation commands
            self.commands = self.filter_installation_commands(self.commands)
        return self.commands
    
    def get_readme_contents(self, repo_url: str) -> str:
        """
        Fetch the contents of the README.md file from a given GitHub repository URL.

        This function now takes the repository URL, constructs the API URL for the
        repository's README, and fetches its content.

        Parameters:
            repo_url (str): The URL of the GitHub repository.

        Returns:
            str: The content of the README.md file or an error message.
        """
        # Normalize the repo URL to remove a trailing slash if present
        self.repo_url = repo_url.rstrip('/')
        # GitHub API URL for the repo
        self.api_url = f"https://api.github.com/repos/{'/'.join(repo_url.split('/')[-2:])}/readme"

        response = requests.get(self.api_url, headers={"Accept": "application/vnd.github+json"})
        if response.status_code == 200:
            download_url = response.json().get('download_url')
            if download_url:
                readme_response = requests.get(download_url)
                if readme_response.status_code == 200:
                    return readme_response.text
                else:
                    return "Failed to fetch the README.md file content."
            else:
                return "README.md file does not have a download URL."
        else:
            return "Failed to fetch README.md file from GitHub."


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch Ubuntu installation commands from a GitHub repository.")
    parser.add_argument("repo_url", type=str, help="URL to the GitHub repository")
    args = parser.parse_args()
    repo_url = args.repo_url
    fetcher = UbuntuCommandFetcher(repo_url)
    commands = fetcher()
    print("Commands:")
    for command in commands:
        print(command)

    