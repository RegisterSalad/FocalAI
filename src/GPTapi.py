import requests
import os
import api_caller

class GPTCaller: 
    """
    Interacts with the PapersWithCode API.

    Attributes:
       
    """
    filename = 'key.txt'
    api_key = None

    def __init__(self) -> None:
        """
        Initialize the API caller with the chatGPT client.
        """
        if os.path.isfile(self.filename):
            # File exists, so read from it
            with open(self.filename, 'r') as file:
                self.api_key = file.read().strip()  # Ensure api_key is read correctly and stripped of any whitespace
        else:
            # File does not exist, prompt for API key and write it
            self.api_key = input("No API key previously found\nPlease enter your API key: ").strip()  # Strip to ensure clean input
            with open(self.filename, 'w') as file:
                file.write(self.api_key)
                print(f"File '{self.filename}' was created and the API key was written to it.")
        
    def get_chat_response(self, api_key: str, documentation: str, request: str) -> None:
        """
        Make an API request to generate a response to a user's message.

        Parameters:
        - api_key: str. The user's API key for authentication.
        - documentation: str. The given documentation from the model
        - request: str. The users request given based off the function called

        Returns:
        None. Prints the response from ChatGPT or an error message.
        """
            # Set Up the API Request
        endpoint = "https://api.openai.com/v1/chat/completions"  # Correct endpoint for chat models
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "gpt-3.5-turbo",  # Assuming this is the correct model identifier
            "messages": [
                {"role": "system", "content": "You are a helpful assistant that helps look at AI model documentation."},
                {"role": "user", "content": documentation + "\n" + request}  # User's question or message
            ]
        }

        # Make the Request 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
        response = requests.post(endpoint, json=data, headers=headers)

        # Handle the Response
        if response.status_code == 200:
            choices = response.json().get("choices", [])
            if choices:
                # Extracting the response text
                print("Response from ChatGPT:\n", choices[0].get("message", {}).get("content"))
            else:
                print("Received an unexpected response format.")
        else:
            print(f"Failed to get a response: {response.status_code} - {response.text}")

    def make_sample_code(self,api_key: str) -> str:
        """
        Generates sample code for using a specified model.

        Parameters:
        - api_key: str. API key.

        Returns:
        str. A string containing the sample code.
        """
        request = "With this given documentation, give me just the sample code needed to run this"
        obj = api_caller.APICaller()
        obj.__init__()
        documentation = obj.get_readme_contents("https://github.com/openai/whisper")
        sample_code = self.get_chat_response(api_key, documentation, request)
        return sample_code
    
    def find_model_parameters(self, api_key: str) -> None:
        """
        Finds the number of parameters for a specified model.

        Parameters:
        - api_key: str. API key.
        """
        request = "With this given documentation, what are the parameters needed to run this?"
        obj = api_caller.APICaller()
        obj.__init__()
        documentation = obj.get_readme_contents("https://github.com/openai/whisper")
        self.get_chat_response(api_key, documentation, request)

    def find_model_datasets(self, api_key: str) -> None:
        """
        Identifies the datasets used by a specified model.

        Parameters:
        - api_key: str. API key.
        """
        request = "With this given documentation, what are the datasets this model uses?"
        obj = api_caller.APICaller()
        obj.__init__()
        documentation = obj.get_readme_contents("https://github.com/openai/whisper")
        self.get_chat_response(api_key, documentation, request)

    def find_model_content(self, api_key: str) -> None:
        """
        Provides information on where to find content about using a specified model.

        Parameters:
        - api_key: str. API key.
        """
        request = "With this given documentation, where can i find more information on this model?"
        obj = api_caller.APICaller()
        obj.__init__()
        documentation = obj.get_readme_contents("https://github.com/openai/whisper")
        self.get_chat_response(api_key, documentation, request)

    def write_model_report(self, api_key: str) -> None:
        """
        Writes a report about a specified model.

        Parameters:
        - api_key: str. API key.
        """
        request = "With this given documentation, give me a basic report about the model"
        obj = api_caller.APICaller()
        obj.__init__()
        documentation = obj.get_readme_contents("https://github.com/openai/whisper")
        self.get_chat_response(api_key, documentation, request)

    def delete_api_key(self):
        """
        Deletes a specified file if it exists.
        """
        # Check if the file exists
        if os.path.isfile('key.txt'):
            # File exists, attempt to delete it
            try:
                os.remove('key.txt')
                print(f"File 'key.txt' has been deleted.")
            except Exception as e:
                print(f"An error occurred while trying to delete the file 'key.txt': {e}")
        else:
            print(f"File 'key.txt' does not exist, so it cannot be deleted.")

def main():
    ## Will change on implementation
    print("A")
    gpt_caller = GPTCaller()
    print("A")
    gpt_caller.__init__()
    print("B")
    gpt_caller.find_model_parameters(gpt_caller.api_key)

if __name__ == "__main__":
    main()
