import os
import json

class JSONCaller():

    directory = None

    def __init__(self) -> None:
        self.directory = os.path.dirname(os.path.realpath(__file__))
    
    def process_json_files(self):
        """
        Processes all JSON files within a specified directory.

        Args:
        directory (str): The path to the directory containing the JSON files.

        Returns:
        None
        """
        print(self.directory)
        installed_list = []
        # Iterate over each file in the directory
        for filename in os.listdir(self.directory):
            # Check if the file is a JSON file
            if filename.endswith('.json'):
                # Construct the full file path
                filepath = os.path.join(self.directory, filename)
                # Open and read the JSON file
                with open(filepath, 'r') as file:
                    data = json.load(file)
                    # Process the data (for demonstration, we'll just print it)
                    installed_list.append(data)

        return installed_list