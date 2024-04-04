from typing import Callable
from model_player import ModelPlayer
class Adapter:

    def __init__(self, parent_page) -> None:
        self.parent_page: ModelPlayer  = parent_page # The parent page will have the input and output interface

    def get_model_input(self, model_type: str | None = None) -> Callable:
        """
        Configures the model_page to the right model type and makes the input of the model come from the drag on drop

        Args:
            - model_type: str | None ; Model type string. Options are "ASR", "OBJ", and "LLM"
        
        Returns:
            - False if model_type is not supported
            - True if pipe is successful
        """

        if model_type == "ASR":
            return self._asr_inteface() 
        elif model_type == "OBJ":
            return self._obj_interface()
        elif model_type == "LLM":
            return self._llm_interface()            
        else:
            return self._default_interface()
        
    def _asr_interface(self) -> str | None:
        """
        Fetches the file from the drag-and-drop, checks its type to make sure
        it is a valid audio file, and returns the path if valid.

        Returns:
            str | None: Path of the input audio file (from drag-and-drop) if valid,
                        None otherwise.
        """
        result_path: str = self.parent_page.input_path
        valid_extensions = ('.mp3', '.wav', '.aac', '.flac')

        # Check if result_path has a valid audio file extension
        if result_path.endswith(valid_extensions):
            return result_path  # Return path if it's a valid audio file
        
        return None  # Return None if the file is not a valid audio file
    
    def _obj_interface(self) -> str | None:
        """
        Fetches the file from the drag-and-drop, checks its type to make sure
        it is a valid image file, and returns the path if valid.

        Returns:
            str | None: Path of the input image file (from drag-and-drop) if valid,
                        None otherwise.
        """
        result_path: str = self.parent_page.input_path
        valid_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')

        # Check if result_path has a valid image file extension
        if result_path.endswith(valid_extensions):
            return result_path  # Return path if it's a valid image file
        
        return None  # Return None if the file is not a valid image file


    def _llm_interface(self) -> str | None:
        pass
        











