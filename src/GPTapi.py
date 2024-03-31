import requests

def get_chat_response(api_key: str, documentation: str, request: str) -> None:
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
            print("Response from ChatGPT:", choices[0].get("message", {}).get("content"))
        else:
            print("Received an unexpected response format.")
    else:
        print(f"Failed to get a response: {response.status_code} - {response.text}")

def exit_program() -> None:
    print("Exiting...")
    exit()

def make_sample_code(api_key: str) -> str:
    """
    Generates sample code for using a specified model.

    Parameters:
    - api_key: str. API key.

    Returns:
    str. A string containing the sample code.
    """
    request = "With this given documentation, give me just the sample code needed to run this"
    documentation = input("documentation:")
    sample_code = get_chat_response(api_key, documentation, request)
    return sample_code

def find_model_parameters(api_key: str) -> None:
    """
    Finds the number of parameters for a specified model.

    Parameters:
    - api_key: str. API key.
    """
    request = "With this given documentation, what are the parameters needed to run this?"
    documentation = input("documentation:")
    get_chat_response(api_key, documentation, request)

def find_model_datasets(api_key: str) -> None:
    """
    Identifies the datasets used by a specified model.

    Parameters:
    - api_key: str. API key.
    """
    request = "With this given documentation, what are the datasets this model uses?"
    documentation = input("documentation:")
    get_chat_response(api_key, documentation, request)

def find_model_content(api_key: str) -> None:
    """
    Provides information on where to find content about using a specified model.

    Parameters:
    - api_key: str. API key.
    """
    request = "With this given documentation, where can i find more information on this model?"
    documentation = input("documentation:")
    get_chat_response(api_key, documentation, request)


def write_model_report(api_key: str) -> None:
    """
    Writes a report about a specified model.

    Parameters:
    - api_key: str. API key.
    """
    request = "With this given documentation, give me a basic report about the model"
    documentation = input("documentation:")
    get_chat_response(api_key, documentation, request)

MENU_TEXT = """
Choose an option for the ChatGPT API call:
0) Exit
1) Make sample code with documentation
2) Find the model's parameters
3) Find what datasets the model uses
4) Look for content based off this model
5) Write a report based off the model
"""

options = {
    0: exit_program,
    1: make_sample_code,
    2: find_model_parameters, #How many parameters does this model have
    3: find_model_datasets, #What datasets does this model use
    4: find_model_content, #Where can I find content about using this model
    5: write_model_report #Write a report about this model
}

api_key = None
def main() -> None:

    api_key: str = input("Please enter your API key: ")
    choice = None
    
    while choice != 7:
        print(MENU_TEXT)
        choice_input = input("Enter your choice: ")
        try:
            choice = int(choice_input)
            if choice in options:
                if choice == 0:
                    options[choice]()#in because code crashes on exit due to args
                options[choice](api_key)
            else:
                print("Invalid option. Please choose again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

if __name__ == "__main__":
    main()
