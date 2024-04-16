import re
from api_caller import APICaller
import json

class Repository:
    """
    Manages a GitHub repository's README analysis for installation commands and model information.
    
    Attributes:
        - repo_url (str): URL of the GitHub repository.
        - install_commands (List[str] | None): Extracted installation commands from README.
        - tables (List[str] | None): Markdown tables found in README.
        - repo_name (str): Name of the repository.
        - owner (str): Owner of the repository.
        - readme_content (str): Content of the README file.
        - model_type (str | None): Type of the model (ASR, OBJ, or LLM), or None if none found or unsupported

    Methods:
        - __init__(repo_url: str): Initialize with the repository's URL.
        - fetch_features(): Fetch and update repository features from README.
        - extract_code_blocks() -> list[str]: Extract code blocks from README content.
        - extract_tab_code() -> list[str]: Extract indented code blocks considered as code in Markdown.
        - extract_commands(install_blocks: list[str]) -> list[str]: Extract installation commands from code blocks.
        - _check_for_install(code_block: str): Check if a code block contains installation commands.
        - parse_readme_contents() -> list[str]: Parses README for installation commands and tables.
        - get_tables(): Finds and stores markdown tables from README.
        - __str__(): String representation summarizing repository attributes.
    """
    def __init__(self, repo_url: str, description) -> None:
        """
        Initializes the Repository object with a GitHub repo URL and fetches its features.

        Args:
            repo_url (str): URL of the GitHub repository to analyze.
        """
        
        self.caller = APICaller()
        self.repo_url: str = repo_url.rstrip('/')
        parts = repo_url.rstrip('/').split('/')
        repo_owner, repo_name = parts[-2], parts[-1]
        self.install_commands: list[str] | None = None
        self.tables: list[str] | None = None
        self.repo_name: str = repo_name
        self.owner: str = repo_owner
        self.model_type: str | None = None
        self.description: str = description
        self.fetch_features()
    
    @staticmethod
    def parse_name(repo_url: str) -> str:
        repo_url: str = repo_url.rstrip('/')
        return repo_url.rstrip('/').split('/')[-1]

    def fetch_features(self) -> None:
        """Fetch repository features from its README and update object attributes."""
        self.readme_content = self.caller.get_readme_contents(self.repo_url)
        if self.readme_content:
            self.install_commands = self.parse_readme_contents()
            self.tables = self.get_tables()
            self.model_type = self.get_model_type()

    def get_model_type(self) -> str | None:
        """
        Looks through the readme to find the model type using regex patterns.
        """

        # Pattern for speech recognition
        if re.search(r'speech recognition', self.readme_content, re.IGNORECASE):
            return "ASR"
        # Pattern for classification or segmentation
        elif re.search(r'classification|segmentation', self.readme_content, re.IGNORECASE):
            return "OBJ"
        # Pattern for language model or <any_integer>B
        elif re.search(r'language model|\d+B', self.readme_content, re.IGNORECASE):
            return "LLM"
        # If none of the patterns match
        return None

    def extract_code_blocks(self) -> list[str]:
        """
        Extract code blocks from Markdown content.

        Returns:
            list[str]: A list of code blocks.
        """
        code_blocks = re.findall(r'```[\s\S]+?```', self.readme_content)
        return code_blocks

    def extract_tab_code(self) -> list[str]:
        """
        Extract indented code blocks considered as code in Markdown.

        Returns:
            list[str]: A list of indented code lines with installation commands.
        """
        tab_code_blocks = re.findall(r'    .+', self.readme_content)
        return [line.strip() for block in tab_code_blocks for line in block.split('\n') if self._check_for_install(line)]

    @staticmethod
    def extract_commands(install_blocks: list[str]) -> list[str]:
        """
        Extract commands from code blocks.

        Args:
            install_blocks (list[str]): list of code blocks.

        Returns:
            list[str]: list of extracted commands.
        """
        commands = []
        for block in install_blocks:
            lines = block.strip('```').strip().split('\n')
            commands.extend([line.strip() for line in lines if Repository._check_for_install(line) and not line.strip().startswith('#')])
        return commands

    @staticmethod
    def _check_for_install(code_block: str) -> bool:
        """
        Check if a code block contains an installation command.

        Args:
            code_block (str): The code block to check.

        Returns:
            bool: True if an installation command is found, False otherwise.
        """
        return bool(re.search(r'\binstall\b', code_block, re.IGNORECASE))
    
    def parse_readme_contents(self) -> list[str]:
        """
        Parses README for installation commands and tables.

        Returns:
            list[str]: A list of installation commands.
        """
        code_blocks = self.extract_code_blocks() + self.extract_tab_code()
        install_commands = self.extract_commands(code_blocks)
        self.tables = self.get_tables()
        self.model_type = self.get_model_type()
        return install_commands

    def get_tables(self) -> None:
        """
        Finds and stores markdown tables from README.
        """
        table_pattern = r'\|.*\|\n\|.*\|'
        self.tables = re.findall(table_pattern, self.readme_content, re.MULTILINE)
        self.tables = [''.join(table) for table in self.tables]
    

    def get_model_type(self) -> str:
        """
        Looks through the readme to find the model type using regex patterns and keyword lists, correcting syntax for raw strings.
        """

        # Define keyword lists for each model type
        asr_keywords = ['speech recognition', 'voice recognition', 'audio processing']
        obj_keywords = ['classification', 'segmentation', 'object detection']
        llm_keywords = ['language model', 'natural language processing', 'text generation']
        llm_size_indicators = [r'\d+B parameters', r'\d+ billion parameters']  # Corrected with raw string notation

        # Join keywords into patterns for regex search
        asr_pattern = '|'.join(asr_keywords)
        obj_pattern = '|'.join(obj_keywords)
        llm_pattern = '|'.join(llm_keywords)
        llm_size_pattern = '|'.join(llm_size_indicators)

        # Pattern for speech recognition
        if re.search(asr_pattern, self.readme_content, re.IGNORECASE):
            return "ASR"
        # Pattern for classification or segmentation
        elif re.search(obj_pattern, self.readme_content, re.IGNORECASE):
            return "OBJ"
        # Pattern for language model
        elif any(re.search(pattern, self.readme_content, re.IGNORECASE) for pattern in [llm_pattern, llm_size_pattern]) \
            and re.search(r'large|massive|extensive', self.readme_content, re.IGNORECASE):
            return "LLM"
        # If none of the patterns match
        else:
            return "N/A"



    def __str__(self) -> str:
        """String representation summarizing repository attributes."""
        details = [
            f"Repository URL: {self.repo_url}",
            f"Repository Name: {self.repo_name}",
            f"Owner: {self.owner}",
            f"Model Type: {self.model_type or 'N/A'}",
            "Installation Commands:" + ("\n" + "\n".join(f"  - {cmd}" for cmd in self.install_commands) if self.install_commands else " None"),
            "Markdown Tables:" + ("\n" + "\n".join(self.tables) if self.tables else " None"),
            f"README Content: {(self.readme_content[:75] + '...') if len(self.readme_content) > 75 else self.readme_content or 'N/A'}"
        ]
        return "\n".join(details)
    
    def to_dict(self) -> dict:
        """Converts the repository object into a dictionary suitable for JSON serialization."""
        return {
            "repo_url": self.repo_url,
            "repo_name": self.repo_name,
            "owner": self.owner,
            "install_commands": self.install_commands,
            "tables": self.tables,
            "model_type": self.model_type,
            "readme_content": self.readme_content
        }

class RepositoryEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Repository):
            return obj.to_dict()
        return super().default(obj)

if __name__ == "__main__":
    repo = Repository("https://github.com/openai/whisper")
    with open("to_delete.json", "w") as file:
        json.dump(repo, file, cls=RepositoryEncoder)

    with open("to_delete.json", "r") as file:
        data = json.load(file)
        print(data)