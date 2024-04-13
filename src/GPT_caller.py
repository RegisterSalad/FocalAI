import requests
import os
import api_caller

from PySide6.QtWidgets import (QWidget, QInputDialog)

class APIGrabber(QWidget):
    '''
    Gives a popup prompt to give API_key if a file of it isnt found
    '''
    def __init__(self):
        super().__init__()
            
    def initUI(self) -> str:
        # This method displays the input dialog
        API_key, ok = QInputDialog.getText(self, 'Key Request', 'Please enter your API key:')
        
        if ok:
            # If the user clicks OK and inputs text, print it to the console
            print(f'The API key that will be used is {API_key}')
            return API_key
        else:
            # If the user cancels the dialog, print a message
            print('User cancelled the dialog')

class GPTCaller: 
    """
    Interacts with the PapersWithCode API.

    Attributes:
       
    """
    filename = 'key.txt'
    api_key = None
    doc_url : str
    log_report : str

    def __init__(self, doc_url) -> None:
        """
        Initialize the API caller with the chatGPT client.
        """
        self.doc_url = doc_url
        self.log_report = None
        if os.path.isfile(self.filename):
            # File exists, so read from it
            with open(self.filename, 'r') as file:
                self.api_key = file.read().strip()  # Ensure api_key is read correctly and stripped of any whitespace
        else:
            # File does not exist, prompt for API key and write it
            popup = APIGrabber()
            self.api_key = popup.initUI()
            with open(self.filename, 'w') as file:
                file.write(self.api_key)
                print(f"File '{self.filename}' was created and the API key was written to it.")
        print(doc_url)
                
        
    def get_chat_response(self, api_key: str, documentation: str, request: str) -> str | None:
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
                #print("Response from ChatGPT:\n", choices[0].get("message", {}).get("content"))
                return choices[0].get("message", {}).get("content")
            else:
                #print("Received an unexpected response format.")
                return "Received an unexpected response format."
        else:
            #print(f"Failed to get a response: {response.status_code} - {response.text}")
            return f"Failed to get a response: {response.status_code} - {response.text}"

    def make_sample_code(self) -> str:
        """
        Generates sample code for using a specified model.

        Returns:
        str. A string containing the sample code.
        """
        request = "With this given documentation, give me just the sample code needed to run this"
        obj = api_caller.APICaller()
        obj.__init__()
        documentation : str = obj.get_readme_contents(self.doc_url)
        sample_code = self.get_chat_response(self.api_key, documentation, request)
        return sample_code
    
    def find_model_parameters(self) -> str:
        """
        Finds the number of parameters for a specified model.

        Parameters:
        - api_key: str. API key.
        """
        request = "With this given documentation, what are the parameters needed to run this?"
        obj = api_caller.APICaller()
        obj.__init__()
        documentation : str = obj.get_readme_contents(self.doc_url)
        ret = self.get_chat_response(self.api_key, documentation, request)
        return ret

    def find_model_datasets(self) -> str:
        """
        Identifies the datasets used by a specified model.

        Parameters:
        - api_key: str. API key.
        """
        request = "With this given documentation, what are the datasets this model uses?"
        obj = api_caller.APICaller()
        obj.__init__()
        documentation : str = obj.get_readme_contents(self.doc_url)
        ret = self.get_chat_response(self.api_key, documentation, request)
        return ret

    def find_model_content(self) -> str:
        """
        Provides information on where to find content about using a specified model.

        Parameters:
        - api_key: str. API key.
        """
        request = "With this given documentation, where can i find more information on this model?"
        obj = api_caller.APICaller()
        obj.__init__()
        documentation : str = obj.get_readme_contents(self.doc_url)
        ret = self.get_chat_response(self.api_key, documentation, request)
        return ret

    def write_model_report(self) -> str:
        """
        Writes a report about a specified model.

        Parameters:
        - api_key: str. API key.
        """
        request = "With this given documentation, give me a basic report about the model"
        obj = api_caller.APICaller()
        obj.__init__()
        documentation : str = obj.get_readme_contents(self.doc_url)
        ret = self.get_chat_response(self.api_key, documentation, request)
        return ret
    
    def output_log_test(self) -> str:
        """
        Writes a report about a specified model.

        Parameters:
        - api_key: str. API key.
        """
        request = "With this given output from the model, give me a basic report about the output"
        file_path = os.path.join('..', 'logging', 'output_log_test.txt')
        with open(file_path, 'r') as file:
            content = file.read()

        ret = self.get_chat_response(self.api_key, content, request)
    
        return ret

    def delete_api_key(self) -> str:
        """
        Deletes a specified file if it exists.
        """
        # Check if the file exists
        if os.path.isfile('key.txt'):
            # File exists, attempt to delete it
            try:
                os.remove('key.txt')
                #print(f"File 'key.txt' has been deleted.")
                return "File 'key.txt' has been deleted, you will be prompted to put in a new key on restart."
            except Exception as e:
                #print(f"An error occurred while trying to delete the file 'key.txt': {e}")
                return "An error occurred while trying to delete the file 'key.txt': {e}"
        else:
            #print(f"File 'key.txt' does not exist, so it cannot be deleted.")
            return "File 'key.txt' does not exist, so it cannot be deleted."

def main():
    ## Will change on implementation
    print("A")
    gpt_caller = GPTCaller()
    print("A")
    #gpt_caller.__init__()
    print("B")
    gpt_caller.find_model_parameters(gpt_caller.api_key)

if __name__ == "__main__":
    main()