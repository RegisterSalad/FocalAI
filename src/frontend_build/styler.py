from PySide6.QtWidgets import (QApplication)
from PySide6.QtGui import QPalette, QColor
from PySide6.QtCore import Qt
from pygments.formatters import HtmlFormatter
import os
import sys

module_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if module_dir not in sys.path:
    sys.path.append(module_dir)

class Styler:

    """
    Manages the application-wide styling, including the dynamic toggling between dark and light themes. 
    This class also keeps track of components that need style updates when themes are switched.

    Attributes:
        dark_mode_enabled (bool): Flag to determine if the dark mode is currently enabled.
        components (list): A list of UI components that require styling updates when the theme changes.
    """
    def __init__(self):
        """
        Initializes the Styler class, setting dark mode to disabled by default and initializing an empty list for components.
        """
        self.dark_mode_enabled = False
        self.components = []

    def style_me(self) -> None:
        """
        Applies styling to all registered components. This method is left empty for possible future use or specific implementations.
        """
        
        pass

        # for component in self.components:
        #     component.setStyleSheet(
        #         """
        #         QWidget {
        #             border-radius: 5px;
        #         }
        #         QTextEdit, QLineEdit {
        #             border-radius: 15px;
        #             background-color: #f0f0f0;
        #         }"""
        #                             )

    def register_component(self, component):
        """
        Registers a UI component for styling updates. When the theme is toggled, `update_style` will be called on each registered component.

        Args:
            component (QWidget): The component to register for styling updates.
        """
        
        self.components.append(component)
        component.update_style()

    def toggle_dark_mode(self):
        """
        Toggles the application's color scheme between dark and light modes. This adjusts the color palette of the entire application.

        Utilizes the QApplication instance to change palette settings globally.
        """
        self.dark_mode_enabled = not self.dark_mode_enabled
        app = QApplication.instance()
        palette = QPalette()

        if self.dark_mode_enabled:
            # Configure palette for dark mode
            palette.setColor(QPalette.Window, QColor(53, 53, 53))
            palette.setColor(QPalette.WindowText, Qt.white)
            palette.setColor(QPalette.Base, QColor(25, 25, 25))
            palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
            palette.setColor(QPalette.Text, Qt.white)
            palette.setColor(QPalette.Button, QColor(53, 53, 53))
            palette.setColor(QPalette.ButtonText, Qt.white)
            palette.setColor(QPalette.Link, QColor(42, 130, 218))
            palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
            palette.setColor(QPalette.HighlightedText, Qt.black)
        else:
            # Reset to default palette
            palette = app.style().standardPalette()

        app.setPalette(palette)
        self.update_styles()

    def update_styles(self):
        """
        Updates the styles for all registered components by calling their `update_style` method. This ensures all components reflect the current theme.
        """
        for component in self.components:
            component.update_style()
    

    @property
    def doc_css(self) -> HtmlFormatter:
        """
        Generates CSS for HTML content, adjusted for either dark or light mode. This is particularly useful for styling HTML views within the application.

        Returns:
            str: A string containing CSS rules formatted for HTML content, tailored to the current theme (dark or light).
        """
        # Common CSS for both dark and light modes
        css = HtmlFormatter().get_style_defs('.codehilite')
        css += """
        table {
            border-collapse: collapse;
            width: 100%;
        }
        th, td {
            border: 1px solid #dddddd;
            text-align: left;
            padding: 8px;
        }
        img {
            max-width: 50%;
            height: auto;
        }
        """
        
        # Conditional CSS for dark and light modes
        if self.dark_mode_enabled:  # Dark mode settings
            css += """
        body {
            background-color: #1e1e1e;
            color: white;
        }
        tr:nth-child(even) {
            background-color: #262626;
        }
        a {
            color: #add8e6;  # Light blue for better visibility in dark mode
        }
        pre {
            border: 1px solid #000000;
            color: #ffffff;
            font-size: 15px;
            line-height: 1.6;
            background-color: #181818
        }
            """
        else:  # Light mode settings
            css += """
        body {
            background-color: #f0f0f0;
            color: #333;
        }
        tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        a {
            color: purple;  # Default purple color for hyperlinks in light mode
        }
        pre {
            border: 1px solid #ffffff;
            color: #000000;
            font-size: 15px;
            line-height: 1.6;
        }
            """
        return css
