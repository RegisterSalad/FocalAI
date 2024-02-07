def find_installed_environments() -> list[str]:
    """Finds the all of the installed Anaconda environments and returns a list of their names"""
    pass

class CondaEnvironment:
    """
    Represents an Anaconda environment
    Attributes:
        python_version (str): The Python version of the conda environment
        is_created (bool): A result of the check that finds if the environment is already part of the system
        pip_list_directory (str): The location of the pip requirements
        models (str | list[str]): The names of the models currently installed
    """
    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        pass

