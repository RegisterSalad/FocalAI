from typing import Optional, Dict
from model import Model
class Repository:
    '''
    ## Description:
    
    This class will contain all of the logic for repositories

    ## Attributes
    
    - name: str
        Name of the repository itself 
    - owner: str
        Name of repository owner
    - github_url: str
        Url for the github repository
    - hugingface_url: Optional[str]
        Url of the associated HuggingFace entry for the repo, can be None if not available on HuggingFace
    - models_available_names: Dict[str, Model]
    '''
    def __init__(self) -> None:
        pass







