import sys
import json
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QMainWindow
from PySide6.QtGui import QPixmap, QKeyEvent
from PySide6.QtCore import QTimer, QRect, Qt

# Importations
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_PATH = os.path.join(BASE_DIR, "Assets")


class SpriteAnimator(QLabel):
    def __init__(self, sprite_path, json_path, parent=None):
        super().__init__(parent)

        self.spritesheet = QPixmap(sprite_path)
        with open(json_path, "r") as f:
            self.data = json.load(f)

        self.animations = {}
        self.durations = {}
        self.current_direction = "SE"
        self.current_frame_index = 0

        # Pré-carrega todos os frames de cada direção
        for tag in self.data["meta"]["frameTags"]:
            name = tag["name"]
            start = tag["from"]
            end = tag["to"]
            self.animations[name] = []
            self.durations[name] = []

            for i in range(start, end + 1):
                frame_data = self.data["frames"][f"DwarfChar{i}.ase"]
                rect = frame_data["frame"]
                duration = frame_data["duration"]

                qrect = QRect(rect["x"], rect["y"], rect["w"], rect["h"])
                cropped = self.spritesheet.copy(qrect)
                self.animations[name].append(cropped)
                self.durations[name].append(duration)

        # Timer de animação
        self.timer = QTimer()
        self.timer.timeout.connect(self.next_frame)
        self.timer.start(self.durations[self.current_direction][0])
        self.setPixmap(self.animations[self.current_direction][0])

    def set_direction(self, direction):
        if direction not in self.animations:
            return
        if direction != self.current_direction:
            self.current_direction = direction
            self.current_frame_index = 0
            self.setPixmap(self.animations[direction][0])
            self.timer.start(self.durations[direction][0])

    def next_frame(self):
        frames = self.animations[self.current_direction]
        durations = self.durations[self.current_direction]

        self.current_frame_index = (self.current_frame_index + 1) % len(frames)
        self.setPixmap(frames[self.current_frame_index])
        self.timer.start(durations[self.current_frame_index])


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sprite 8-Direction Animation")
        self.setFixedSize(300, 300)

        self.animator = SpriteAnimator(
            sprite_path=f"{ASSETS_PATH}/Chars/char.png",
            json_path=f"{ASSETS_PATH}/Chars/char.json",
        )

        layout = QVBoxLayout()
        layout.addWidget(self.animator)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Teclas ativas
        self.pressed_keys = set()

    def keyPressEvent(self, event: QKeyEvent):
        key = event.key()
        self.pressed_keys.add(key)
        self.update_direction()

    def keyReleaseEvent(self, event: QKeyEvent):
        key = event.key()
        if key in self.pressed_keys:
            self.pressed_keys.remove(key)
        self.update_direction()

    def update_direction(self):
        keys = self.pressed_keys

        # Mapeamento de direções com diagonais
        if Qt.Key_W in keys:
            self.animator.set_direction("NE")
        elif Qt.Key_S in keys:
            self.animator.set_direction("SW")
        elif Qt.Key_D in keys:
            self.animator.set_direction("SE")
        elif Qt.Key_A in keys:
            self.animator.set_direction("NW")
        elif Qt.Key_I in keys:
            self.animator.set_direction("Idle")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
