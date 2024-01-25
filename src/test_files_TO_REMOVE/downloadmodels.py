import requests

def get_readme_contents(repo_url):
    # Extract the repo's owner and name from the URL
    parts = repo_url.rstrip('/').split('/')
    repo_owner, repo_name = parts[-2], parts[-1]

    # GitHub API URL for the README.md file
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/readme"

    # Send a GET request to the GitHub API
    response = requests.get(api_url)

    if response.status_code == 200:
        # Extract the download URL for the README.md content
        download_url = response.json().get('download_url')

        if download_url:
            # Fetch the actual content of README.md
            readme_response = requests.get(download_url)
            if readme_response.status_code == 200:
                return readme_response.text
            else:
                return "Failed to fetch the README.md file content."
        else:
            return "README.md file does not have a download URL."
    else:
        return "Failed to fetch README.md file from GitHub."

repo_link = "https://github.com/openai/whisper"  # Replace with actual GitHub repo URL
print(get_readme_contents(repo_link))