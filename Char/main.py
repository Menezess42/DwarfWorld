# Char/main.py
import json
from PySide6 import QtCore

class CharAnimator:
    def __init__(self, char_item, frame_w: int, frame_h: int):
        self.char_item = char_item
        self.char_fw = frame_w
        self.char_fh = frame_h
        self.timer = QtCore.QTimer()
        self.step_index = 0
        self.path_points = []

    def load_path_from_json(self, json_path: str):
        with open(json_path, "r") as f:
            data = json.load(f)
        self.path_points = [tuple(tile["world"]) for tile in data]

    def start(self, delay_ms: int = 1000):
        self.step_index = 0

        def move_step():
            if self.step_index >= len(self.path_points):
                self.timer.stop()
                return
            x, y = self.path_points[self.step_index]
            self.char_item.setPos(x - self.char_fw / 2, y - self.char_fh)
            self.step_index += 1

        self.timer.timeout.connect(move_step)
        self.timer.start(delay_ms)
