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

        # Sprites animados
        self.sprites = [
            QtGui.QPixmap(f"{IMAGES_PATH}/1.png").scaled(100, 100, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation),
            QtGui.QPixmap(f"{IMAGES_PATH}/2.png").scaled(100, 100, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation),
            QtGui.QPixmap(f"{IMAGES_PATH}/3.png").scaled(100, 100, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation),
            QtGui.QPixmap(f"{IMAGES_PATH}/4.png").scaled(100, 100, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation),
        ]
        self.sprite_index = 0

        self.frame_count = 0  # Contador de frames
        self.sprite_update_interval = 5  # Trocar sprite a cada 5 frames
        # Label de imagem
        self.emoji = QtWidgets.QLabel(self)
        self.emoji.setPixmap(self.sprites[self.sprite_index])
        self.emoji.move(0, 200)

        self.emoji_alive = True
        self.emoji_visible = True
        self.emoji_x = 0

        # Timer de movimento
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.move_emoji)
        self.timer.start(30)

        # Posição da janela
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

            self.frame_count += 1
            if self.frame_count % self.sprite_update_interval == 0:
                self.change_sprite()

    def change_sprite(self):
        self.sprite_index = (self.sprite_index + 1) % len(self.sprites)
        self.emoji.setPixmap(self.sprites[self.sprite_index])

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
