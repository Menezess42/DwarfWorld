import json
from copy import deepcopy
from PIL import Image
import os
import sys
import json
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QMainWindow
from PySide6.QtGui import QPixmap, QKeyEvent
from PySide6.QtCore import QTimer, QRect, Qt
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_PATH = os.path.join(BASE_DIR, "Assets")

image_path = f"{ASSETS_PATH}/Chars/char.png"
json_path = f"{ASSETS_PATH}/Chars/char.json"

# Carregar os dados do JSON original
with open(json_path, "r") as f:
    data = json.load(f)

# Assume-se que os sprites tinham originalmente 28x27 de tamanho
pivot_x, pivot_y = 14, 23

# Criar uma nova cópia dos dados
adjusted_data = deepcopy(data)

# Para cada frame, calcular o offset em relação ao centro fixo
for frame_name, frame_data in adjusted_data["frames"].items():
    sprite_source = frame_data["spriteSourceSize"]
    trimmed_x = sprite_source["x"]
    trimmed_y = sprite_source["y"]

    offset_x = pivot_x - trimmed_x
    offset_y = pivot_y - trimmed_y

    frame_data["pivot"] = {"x": pivot_x, "y": pivot_y}
    frame_data["offset"] = {"x": offset_x, "y": offset_y}

# Salvar o novo JSON com os offsets
with open(f"{ASSETS_PATH}/Chars/char_trimmed_with_offsets.json", "w") as f:
    json.dump(adjusted_data, f, indent=2)
