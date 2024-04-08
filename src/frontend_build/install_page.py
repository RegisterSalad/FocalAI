from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame, QWidget
from PySide6.QtCore import Qt
from PySide6.QtWebEngineWidgets import QWebEngineView  # Import QWebEngineView
import markdown
import sys
import os
from PySide6.QtGui import QIcon
from typing import Callable

# Working dir imports
from model_player import ModelPlayer
from styler import Styler

# Calculate the path to the directory containing
module_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if module_dir not in sys.path:
    sys.path.append(module_dir)

# Project imports
from repo import Repository
from database import DatabaseManager

class InstallPage(QFrame):
    def __init__(self, styler, model_page, install_commands: list[str]):
        super().__init__()
        self.model_page = model_page
        self.styler = styler
        self.install_commands_list = install_commands
        print(self.install_commands_list)
        self.command_count = len(self.install_commands_list)
        self.commands_to_run_set: set = set()
        self.success = False
        self.init_ui()

    def init_ui(self):
        self.css = self.styler.doc_css
        self.page_layout = QVBoxLayout()
        ''' Level 1 Hierarchy '''
        self.install_frame = QFrame()
        self.to_run_frame = QFrame()

        self.install_frame_layout = QHBoxLayout()
        self.to_run_frame_layout = QHBoxLayout()
        
        self.install_frame.setLayout(self.install_frame_layout)
        self.to_run_frame.setLayout(self.to_run_frame_layout)
        '''-------------------'''

        ''' Level 2 Hierarchy '''
        self.install_display_widget = QWidget()
        self.to_run_display_widget = QWidget()

        self.install_display_layout = QHBoxLayout()
        self.to_run_display_layout = QHBoxLayout()

        self.install_display_widget.setLayout(self.install_display_layout)
        self.to_run_display_widget.setLayout(self.to_run_display_layout)
        '''-------------------'''

        ''' Level 2 Hierarchy '''
        self.install_button_widget = QWidget()
        self.to_run_button_widget = QWidget()

        self.install_button_layout = QVBoxLayout()
        self.to_run_button_layout = QVBoxLayout()

        self.install_button_widget.setLayout(self.install_button_layout)
        self.to_run_button_widget.setLayout(self.to_run_button_layout)
        '''-------------------'''

        ''' Level 3 Hierarchy '''
        self.commands_displayer_engine = QWebEngineView()
        self.to_run_engine = QWebEngineView()

        #Add engines to layouts
        self.install_display_layout.addWidget(self.commands_displayer_engine)
        self.to_run_display_layout.addWidget(self.to_run_engine)
        '''-------------------'''

        #Set the engine content for the original commands
        self.set_engine_content(self.install_commands_list, self.commands_displayer_engine)
        #Add the buttons for original commands
        self.create_add_buttons()

        self.run_button = QPushButton('Run Selected Commands')
        self.run_button.clicked.connect(self.run_selected_commands)
        self.back_button = QPushButton('<<')
        self.back_button.setToolTip("Return to Model Page")
        self.back_button.setMaximumSize(30, 30)
        self.back_button.clicked.connect(self.change_to_main_model_page)
        self.page_layout.addWidget(self.back_button, 0, Qt.AlignTop | Qt.AlignLeft)
        
        self.page_layout.addWidget(QLabel('Install Commands:'))
        self.install_frame_layout.addWidget(self.install_display_widget)
        self.install_frame_layout.addWidget(self.install_button_widget)
        self.page_layout.addWidget(self.install_frame)

        self.page_layout.addWidget(QLabel('Commands to Run:'))
        self.to_run_frame_layout.addWidget(self.to_run_display_widget)
        self.to_run_frame_layout.addWidget(self.to_run_button_widget)
        self.page_layout.addWidget(self.to_run_frame)
        self.page_layout.addWidget(self.run_button)
        self.setLayout(self.page_layout)

    def set_engine_content(self, content: list[str] | set, engine: QWebEngineView) -> None:
        lines = [markdown.markdown(line, extensions=['tables', 'fenced_code', 'codehilite', 'extra']) for line in content]
        html_text: str = ""
        for line in lines:
            html_text += f"{markdown.markdown(line, extensions=['tables', 'fenced_code', 'codehilite', 'extra'])}\n"

        html_text = f"<style>{self.css}</style>{html_text}"
        engine.setHtml(html_text)


    def create_add_buttons(self) -> None:
        """
        Creates the buttons for each command in install_commands and connects the the copy_command_to_run with the install command at that index to each.
        Adds the buttons the correct layout: self.commands_layout
        """
        print(self.command_count)

        for idx in range((self.command_count)):
            btn = QPushButton('+')
            btn.setMaximumSize(30, 30)
            btn.clicked.connect(lambda idx=idx: self.copy_command_to_run(self.install_commands_list[idx]))
            self.install_button_layout.addWidget(btn) # Where should I put these buttons?

    def copy_command_to_run(self, command: str) -> None:
        """
        Displays the command in the to_run engine
        Add the button for it
        """
        self.commands_to_run_set.add(command)
        self.set_engine_content(self.commands_to_run_set, self.to_run_engine)
        btn = QPushButton('-')
        btn.setMaximumSize(30, 30)
        btn.clicked.connect(lambda: self.remove_command_from_run(command, btn))
        self.to_run_button_layout.addWidget(btn)

    def remove_command_from_run(self, command: str, btn: QPushButton) -> None:
        self.commands_to_run_set.remove(command)
        self.to_run_button_layout.removeWidget(btn)

    def run_selected_commands(self):
        # Implement command execution logic
        print("Running commands:", self.commands_to_run_set)

    def hide_all(self) -> None:
        layout = self.layout()  # Get the layout of the frame
        if layout is not None:
            for i in range(layout.count()):
                item = layout.itemAt(i)
                widget = item.widget()
                if widget is not None:  # Check if the item is a widget
                    widget.setDisabled(True)
                    widget.hide()  # Hide the widget

    def show_all(self) -> None:
        layout = self.layout()  # Get the layout of the frame
        if layout is not None:
            for i in range(layout.count()):
                item = layout.itemAt(i)
                widget = item.widget()
                if widget is not None:  # Check if the item is a widget
                    widget.setEnabled(True)
                    widget.show()  # Show the widget

    def change_to_main_model_page(self):
        self.hide_all()
        self.model_page.show_all()