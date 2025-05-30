import os
import sys
from pathlib import Path

from PySide6 import QtCore, QtGui, QtWidgets

# CONSTANTS
BASE_DIR = Path(__file__).parent
SRC_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGES_PATH = os.path.join(SRC_DIR, "Assets", "Tests")


def get_resource_path(filename: str) -> Path:
    return BASE_DIR / filename


class TransparentWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setStyleSheet("background-color: transparent;")
        self.setFixedSize(640, 480)
        self.setWindowOpacity(0.0)
        self.setWindowTitle("DwarfWorldWindow")
        self.setObjectName("DwarfWorldWindow")

        # Emoji (como texto)
        # label = QtWidgets.QLabel(self)
        # label.setPixmap(QtGui.QPixmap("../Assets/Tests/littleDwarf.png"))
        # label.move(0, 200)

        label = QtWidgets.QLabel(self)
        pixmap = QtGui.QPixmap(f"{IMAGES_PATH}/littleDwarf.png")
        scaled_pixmap = pixmap.scaled(
            100, 100, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation
        )
        print(pixmap)
        print(scaled_pixmap)
        label.setPixmap(scaled_pixmap)
        label.move(0, 200)

        self.emoji = label
        self.emoji.setStyleSheet("font-size: 48px;")
        self.emoji.move(0, 200)

        # Estado interno
        self.emoji_alive = True
        self.emoji_visible = True
        self.emoji_x = 0

        # Timer de movimento
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.move_emoji)
        self.timer.start(30)  # milissegundos

        # Posição inicial da janela
        screen = QtWidgets.QApplication.primaryScreen()
        available_geometry = screen.availableGeometry()
        x = available_geometry.right() - self.width() - 8
        y = available_geometry.top() + 30
        self.move(x, y)

    def move_emoji(self):
        if self.emoji_alive and self.emoji_visible:
            self.emoji_x += 2
            if self.emoji_x > self.width():
                self.emoji_x = -40
            self.emoji.move(self.emoji_x, 200)

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        key = event.key()
        if key == QtCore.Qt.Key_X:
            self.emoji_alive = False
        elif key == QtCore.Qt.Key_L:
            self.emoji.setVisible(False)
            self.emoji_visible = False
        elif key == QtCore.Qt.Key_R:
            self.emoji_alive = True
            self.emoji_visible = True
            self.emoji.setVisible(True)


def Frame():
    app = QtWidgets.QApplication([])
    window = TransparentWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    Frame()
