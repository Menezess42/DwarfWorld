from PySide6 import QtWidgets, QtCore, QtGui
from pathlib import Path
# Only needed for access to command line arguments
import sys

# CONSTANTS
BASE_DIR = Path(__file__).parent

def get_resource_path(filename: str) -> Path:
    return BASE_DIR/filename


class TransparentWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setStyleSheet("background-color: transparent;")
        self.setFixedHeight(480)
        self.setFixedWidth(640)
        self.setWindowOpacity(0.0)
        self.setWindowTitle("DwarfWorldWindow")  # Define um título
        self.setObjectName("DwawrfWorldWindow")   # Alternativa para match de regras

def main():
    app = QtWidgets.QApplication([])
    window = TransparentWindow()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
