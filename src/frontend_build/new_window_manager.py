# from PySide6.QtCore import Slot, QObject
# import os
# import sys
# # Calculate the path to the directory containing database.py
# module_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
# if module_dir not in sys.path:
#     sys.path.append(module_dir)
# from pop_up import PopUp

# class NewWindowManager(QObject):
#     def __init__(self):
#         super().__init__()

#     @Slot(str)
#     def handle_content_change(self, content):
#         # Extract the model name from the file path or content (or pass it separately)
#         model_name = "Model Name"  # Example model name

#         # Create and show the new window with the model name
#         new_window = new_window(content)  # Pass the model name and content to the NewWindow constructor
#         new_window.show()
