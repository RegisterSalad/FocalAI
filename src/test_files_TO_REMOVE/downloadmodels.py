import requests
import re
import subprocess

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

def extract_code_blocks(markdown_content) -> list[str]:
    # Regex to find code blocks
    code_blocks = re.findall(r'```[\s\S]+?```', markdown_content)
    return code_blocks

def check_for_install(code_block: str) -> bool:
    '''This function returns true if a block of multiple commands contains the keyword "install" '''
    # Using `lower()` method to convert the text to lowercase
    confirmation = re.findall("install", code_block.lower())

    # Check if the list `confirmation` is not empty
    return bool(confirmation)

def extract_commands(install_blocks: list[str]):
    commands = []
    for block in install_blocks:
        # Remove the backticks and split the block into lines
        lines = block.strip('```').strip().split('\n')
        for line in lines:
            # Ignore comments and empty lines
            if not line.strip().startswith('#') and line.strip() and not re.findall("bash", line.lower()):
                commands.append(line.strip())
    return commands

def main():
    repo_link = "https://github.com/openai/whisper"  # Test repo link

    # Get readme
    readme = get_readme_contents(repo_url=repo_link)

    code_blocks = extract_code_blocks(readme)

    install_commands = [] 

    for code_block in code_blocks:
        if check_for_install(code_block):
            install_commands.extend(extract_commands([code_block]))
    
    for command in install_commands:
        print(command)


if __name__ == "__main__":
    main()