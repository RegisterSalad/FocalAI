import requests  # Import requests for synchronous HTTP calls
from paperswithcode import PapersWithCodeClient
from secret import PWC_KEY

class APICaller:
    """
    Interacts with the PapersWithCode API.

    Attributes:
        client (PapersWithCodeClient): API client.
    """

    def __init__(self) -> None:
        """
        Initialize the API caller with a PapersWithCode client.
        """
        self.client = PapersWithCodeClient(token=PWC_KEY)

    def get_readme_contents(self, repo_url: str) -> str | None:
        parts = repo_url.rstrip('/').split('/')
        repo_owner, repo_name = parts[-2], parts[-1]
        api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/readme"
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            download_url = data.get('download_url')
            print(download_url)
            if download_url:
                readme_response = requests.get(download_url)
                if readme_response.status_code == 200:
                    content = self.parse_readme_contents(readme_response.text,repo_name)
                    return content
        return None

