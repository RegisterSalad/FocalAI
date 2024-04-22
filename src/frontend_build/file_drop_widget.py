import os
import sys
import shutil
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, Signal

# Remove for final build
module_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if module_dir not in sys.path:
    sys.path.append(module_dir)

from directories import DRAG_N_DROP_DIR

class FileDropWidget(QWidget):
    """A widget that supports dragging and dropping files into it.
    
    Attributes:
        filesDropped (Signal): Custom signal that emits the path of the dropped file.
    """
    
    
    filesDropped = Signal(str)  # Signal to emit when files have been dropped

    def __init__(self):
        """Initialize the FileDropWidget with drag and drop enabled."""
        super().__init__()
        self.setAcceptDrops(True)
        self.init_ui()

    def init_ui(self):
        """Set up the user interface of the widget."""
        self.setMinimumSize(400, 200)
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
                border: 2px dashed #cccccc;
                border-radius: 10px;
            }
        """)

        layout = QVBoxLayout()
        self.label = QLabel("Drag and drop files here")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("color: #888888; font-style: italic;")
        layout.addWidget(self.label)
        layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(layout)

    def dragEnterEvent(self, event):
        """Handle the event when a drag action enters the widget."""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.label.setStyleSheet("color: #555555; font-style: normal;")

    def dropEvent(self, event):
        """Handle the event when files are dropped onto the widget."""
        mime_data = event.mimeData()
        if mime_data.hasUrls():
            # Consider only the first file from the drop
            first_file_url = mime_data.urls()[0]
            if first_file_url.isLocalFile():
                src_path = first_file_url.toLocalFile()
                if os.path.isfile(src_path):  # Check if it's a file not a directory
                    file_name = os.path.basename(src_path)
                    dest_path = os.path.join(DRAG_N_DROP_DIR, file_name)

                    # Clear existing files in the directory
                    for existing_file in os.listdir(DRAG_N_DROP_DIR):
                        os.remove(os.path.join(DRAG_N_DROP_DIR, existing_file))

                    # Copy the new file
                    try:
                        shutil.copy(src_path, dest_path)
                        self.label.setText(file_name)  # Update label to show copied file
                        self.label.setStyleSheet("color: #000000; font-style: normal;")
                        self.filesDropped.emit(dest_path)  # Emit signal with path of copied file
                    except Exception as e:
                        print(f"Could not copy file {src_path} to {dest_path}: {e}")
