import os
import json

class JSONCaller():
    """
    A utility class designed to handle JSON file operations within a specified directory. 
    This class is responsible for processing JSON files to extract data, typically used to manage a list of models or configurations.

    Attributes:
        directory (str): The directory where JSON files are stored. It is dynamically set to the directory containing this script.
    """

    directory = None

    def __init__(self) -> None:
        """
        Initializes the JSONCaller instance by setting the directory attribute to the directory where the script resides.
        This setup allows the class to know where to look for JSON files to process.
        """
        self.directory = os.path.dirname(os.path.realpath(__file__))
    
    def process_json_files(self):
        """
        Processes all JSON files within a specified directory.
        Scans the designated directory for JSON files and processes each one to extract its contents.

        Args:
        directory (str): The path to the directory containing the JSON files.

        Returns:
        list[dict]: A list of dictionaries where each dictionary represents the parsed data from one JSON file in the directory
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
