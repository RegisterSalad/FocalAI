import re
import argparse
from api_caller import APICaller

class Repository:
    """
    Represents a GitHub repository with functionality to automatically
    fetch and parse its README for relevant installation and model information.

    Attributes:
        repo_url (str): URL of the GitHub repository.
        has_install (bool): True if installation commands are found in the README.
        install_commands (list[str]): Extracted installation commands from the README.
        tables (list[str])
    """
    def __init__(self, repo_url: str) -> None:
        """
        Initializes the Repository object with a GitHub repo URL and fetches
        its features such as installation commands and model information.

        Args:
            repo_url (str): URL of the GitHub repository to analyze.
        """
        self.caller = APICaller()
        self.repo_url: str = repo_url.rstrip('/')
        self.install_commands: list[str] = None
        self.tables: list[str] | None = None
        # Fetch and parse repository features
        self.fetch_features()

    def fetch_features(self) -> None:
        """
        Fetch repository features from its README and update object attributes.
        """
        self.readme_content = self.caller.get_readme_contents()
        if self.readme_content:
            self.install_commands = self.parse_readme_contents()

    def extract_code_blocks(self) -> list[str]:
        """
        Extract code blocks from Markdown content.

        Args:
            markdown_content (str): The Markdown content.

        Returns:
            List[str]: A list of code blocks.
        """
        code_blocks = re.findall(r'```[\s\S]+?```', self.readme_content)
        return code_blocks
    
    def extract_tab_code(self) -> list[str]:
        tab_code = re.findall(r'    [\s\S]+?\n', self.readme_content)
        code = []
        for block in tab_code:
            lines = block.strip('    ').strip().split('\n')
            for line in lines:
                if line.strip() and re.search(r'\binstall\b', line, re.IGNORECASE):
                    code.append(line.strip())
        return code

    def extract_commands(install_blocks: list[str]) -> list[str]:
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
                if not line.strip().startswith('#') and line.strip() and not re.search(r'\bbash\b', line, re.IGNORECASE) and re.search(r'\binstall\b', line, re.IGNORECASE):
                    commands.append(line.strip())
        return commands
    
    def parse_readme_contents(self, repo_name: str)->str:
        """
        Parses the readme text from getReadme and returns a formatted string that contains the installation commands.
        The Install commands are stored in a text file under the name of Install_commands_[the github repo's name].txt
        Any tables found in the readme file will be put in a text file under the name of [the github repo's name]_Tables.txt

        Args:
            The string containing the Readme text and the name of the github repository

        Returns:
            A String containing the installation commands for the AI model
        """
        code_blocks = self.extract_code_blocks()
        tab_code = self.extract_tab_code()
        self.tables = self.get_tables()

        install = [command for block in code_blocks if self.check_for_install(block) for command in self.extract_commands([block])]
        readme_contents: str
        readme_contents = f"#{repo_name}\n##Install commands: \n\t"
        for command in install:
            readme_contents += command+"\n\t"
        for tabs in tab_code:
            readme_contents += tabs+"\n\t"
        return readme_contents

    def get_tables(self, readme_content: str) -> None:
        """
        Finds markdown tables within the README content and stores them in a list.

        Args:
            readme_content (str): The content of the README file.
        """
        # Regular expression to match simple markdown tables
        table_pattern = r'\|.*\|\n\|.*\|'
        self.tables = re.findall(table_pattern, readme_content, re.MULTILINE)
        # Flatten the list of tuples returned by findall into a list of strings
        self.tables = [''.join(table) for table in self.tables]

    def __str__(self) -> str:
        """
        Provides a string representation of the Repository object, summarizing its
        attributes such as URL, Docker presence, installation commands, and more.

        Returns:
            str: A summary of the repository's characteristics.
        """
        attributes = [
        f"Repository URL: {self.repo_url}",
        "Installation Commands:\n" + ("\n".join(f"\t{cmd}" for cmd in self.install_commands) if self.install_commands else "\tNone"),
        "Markdown Tables:\n" + ("\n\n".join(self.tables) if self.tables else "\tNone")
        ]
        return "\n".join(attributes)

