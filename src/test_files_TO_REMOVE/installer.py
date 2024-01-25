from typing import Optional

class Installer:
    '''
    The installer class takes a model name or URL as input and initializes the install process for said model.

    ### Inputs:
    - model_name: str
        Will be used to find if the model is im huggingface or to find the github repo url

    - url: str
        will be used to find the github repo and find and run the install commands.

    '''
    def __init__(self, model_name: Optional[str] ,url: Optional[str]) -> None:
        
        if url is not None:
            pass




if __name__ == "__main__":
    installer = In