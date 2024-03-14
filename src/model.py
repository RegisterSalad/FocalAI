from typing import Optional, Dict
from repo import Repository

class Model:
    """
    This dataclass contains all the metadata about the an installed model.

    Attributes:
        on_disk_size_mbyte (float): Stores the value of the size of the model on disk
        model_name (str): The name of the individual model
        model_path (str): Path of the model within local file system
    """
    def __init__(self, model_path, model_name) -> None:
        """
        Sets and initializes class attributes

        Args:
            model_name (str): The name of the individual model
            model_path (str): Path of the model within local file system
        """
        pass
    
    def _set_size() -> None:
        """
        Finds and sets the value of model_size in MB (Bytes)
        """
        pass



    def __str__(self) -> str:
        
        pass
