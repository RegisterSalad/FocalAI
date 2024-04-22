import re
from api_caller import APIManager
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
        Initializes a Repository instance with a GitHub repository URL and a description. 
        It extracts features from the repository's README, such as installation commands, tables, and model type.

        Args:
        repo_url (str): URL of the GitHub repository.
        description (str): Description of the repository to be analyzed.
        """
        
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
        """
        Parses the repository name from a GitHub URL.

        Args:
            repo_url (str): The complete GitHub repository URL.

        Returns:
            str: The name of the repository.
        """
        repo_url: str = repo_url.rstrip('/')
        return repo_url.rstrip('/').split('/')[-1]

    def fetch_features(self) -> None:
        """Fetch repository features from its README and update object attributes."""
        self.readme_content = APIManager.get_readme_contents(repo_url=self.repo_url)
        if self.readme_content:
            self.install_commands = self.parse_readme_contents()
            self.tables = self.get_tables()
            self.model_type = self.get_model_type()

    def get_model_type(self) -> str | None:
        """
        Determines the type of model based on keywords found in the README content.

        Returns:
            str | None: The identified model type based on key terminology ('ASR', 'OBJ', 'LLM'), or None if no type is identified.
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
        Extracts code blocks from the repository's README Markdown content.

        Returns:
            list[str]: A list of extracted code blocks.
        """
        code_blocks = re.findall(r'```[\s\S]+?```', self.readme_content)
        return code_blocks

    def extract_tab_code(self) -> list[str]:
        """
        Extracts indented code lines from the repository's README Markdown content.

        Returns:
            list[str]: A list of extracted code lines considered as code due to Markdown indentation.
        """
        tab_code_blocks = re.findall(r'    .+', self.readme_content)
        return [line.strip() for block in tab_code_blocks for line in block.split('\n') if self._check_for_install(line)]

    @staticmethod
    def extract_commands(install_blocks: list[str]) -> list[str]:
        """
        Extracts installation commands from provided code blocks.

        Args:
            install_blocks (list[str]): List of code blocks potentially containing installation commands.

        Returns:
            list[str]: List of extracted installation commands.
        """
        commands = []
        for block in install_blocks:
            lines = block.strip('```').strip().split('\n')
            commands.extend([line.strip() for line in lines if Repository._check_for_install(line) and not line.strip().startswith('#')])
        return commands

    @staticmethod
    def _check_for_install(code_block: str) -> bool:
        """
        Checks if a code block contains an installation command by searching for the keyword 'install'.

        Args:
            code_block (str): The code block to be checked.

        Returns:
            bool: True if the block contains an installation command, otherwise False.
        """
        return bool(re.search(r'\binstall\b', code_block, re.IGNORECASE))
    
    def parse_readme_contents(self) -> list[str]:
        """
        Parses the README content for installation commands and extracts tables and model type.

        Returns:
            list[str]: A list of installation commands derived from the README.
        """
        code_blocks = self.extract_code_blocks() + self.extract_tab_code()
        install_commands = self.extract_commands(code_blocks)
        self.tables = self.get_tables()
        self.model_type = self.get_model_type()
        return install_commands

    def get_tables(self) -> None:
         """
        Extracts markdown tables from the README content stored in this class. 
        Identifies tables using regular expressions and stores them in a list attribute for further use.

        This method modifies the `tables` attribute of the instance, storing all found tables formatted as strings.
        """
        table_pattern = r'\|.*\|\n\|.*\|'
        self.tables = re.findall(table_pattern, self.readme_content, re.MULTILINE)
        self.tables = [''.join(table) for table in self.tables]
    

    def get_model_type(self) -> str:
        """
        Determines the model type based on keywords found in the README content. Utilizes regular expressions to search for
        specific phrases associated with different types of models.

        Returns:
            str: The identified model type ('ASR' for audio/speech recognition, 'OBJ' for object detection, 'LLM' for language models),
                 or 'N/A' if no specific model type can be identified.
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
        """
        Provides a human-readable string representation of the repository, summarizing its key attributes.

        Returns:
            str: A formatted string that lists the repository's URL, name, owner, model type, installation commands,
             markdown tables, and a snippet or the full content of the README.
        """
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
        """
        Converts the repository attributes into a dictionary, making it suitable for serialization, particularly to JSON format.

        Returns:
            dict: A dictionary representation of the repository, including its URL, name, owner, installation commands,
              markdown tables, model type, and README content.
        """
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
    """
    A JSON encoder subclass for serializing Repository objects.

    This encoder extends the default JSONEncoder and provides a method to convert Repository objects into
    a JSON-serializable format by calling their `to_dict()` method.

    Attributes:
        Inherits all attributes from json.JSONEncoder.

    Methods:
        default(obj): Overrides the default method to provide a custom serialization strategy for Repository objects.
    """
    def default(self, obj):
        """
        Convert Repository objects into dictionaries, which are JSON-serializable.

        Args:
            obj (any): The object to serialize. If it's a Repository instance, it gets converted using its `to_dict()` method.

        Returns:
            dict: The JSON-serializable dictionary representation of the Repository if the object is an instance of Repository.
        
        Raises:
            TypeError: If the object is not an instance of Repository, it calls the superclass's default method,
                       which may raise a TypeError if `obj` is not otherwise serializable.
        """
        if isinstance(obj, Repository):
            return obj.to_dict()
        return super().default(obj)

# If this script is the main program being executed,
# then perform the following operations:
if __name__ == "__main__":
    # Create an instance of the Repository class with a specific GitHub URL
    # Open a file for writing. The file is named 'to_delete.json'.
    repo = Repository("https://github.com/openai/whisper")
    with open("to_delete.json", "w") as file:
        json.dump(repo, file, cls=RepositoryEncoder)
        # Serialize the `repo` object to a JSON formatted string and write it into the file.
        # The `cls` parameter specifies a custom JSONEncoder (RepositoryEncoder) that knows how to handle Repository objects.
    
    # Open the same file for reading.
    # Load the JSON content from the file and deserialize it into a Python dictionary.
    # Print the dictionary to the console.
    with open("to_delete.json", "r") as file:
        data = json.load(file)
        print(data)
