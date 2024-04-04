class Adapter:

    def __init__(self) -> None:
        pass

    def set_model_input(self, model_type: str | None = None) -> bool:
        """
        Configures the model_page to the right model type and makes the input of the model come from the drag on drop

        Args:
            - model_type: str | None ; Model type string. Options are "ASR", "OBJ", and "LLM"
        
        Returns:
            - False if model_type is not supported
            - True if pipe is successful
        """

        if 








