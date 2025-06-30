# World/main.py
import json
from pathlib import Path

from PySide6 import QtGui

ASSETS_PATH = Path(__file__).parent.parent / "Assets" / "Blocks"
TILE_W, TILE_H = 32, 16


def Create_tile_grid(scene, grid_ref: list, size: int):
    for line in range(size):
        for column in range(size):
            pixmap = QtGui.QPixmap(str(ASSETS_PATH / "grama32.png"))
            item = scene.addPixmap(pixmap)
            x = ((column - line) + 19) * (TILE_W / 2)
            y = ((column + line) + 6) * (TILE_H / 2)
            item.setPos(x, y)
            grid_ref.append((x, y))


def Create_overlay_grid(scene, grid: list, size: int, json_path: str):
    TILE_W, TILE_H = 32, 16
    tiles_data = []

    for idx, (x, y) in enumerate(grid):
        row = idx // size
        col = idx % size
        center = (x + TILE_W / 2, y + TILE_H / 2)

        tiles_data.append(
            {
                "grid": [row, col],
                "world": list(center),
                "vertices": {
                    "N": [x + TILE_W / 2, y],
                    "E": [x + TILE_W, y + TILE_H / 2],
                    "S": [x + TILE_W / 2, y + TILE_H],
                    "W": [x, y + TILE_H / 2],
                },
                "type": "ground",
                "occupied": False,
                "layer": col,  # row
            }
        )

    with open(json_path, "w") as f:
        json.dump(tiles_data, f, indent=2)


def Create_column_row_indexation(scene, json_path: str):
    # read json file
    with open(json_path, "r") as f:
        json_object = json.load(f)
    for element in json_object:
        x, y = element.get("grid")
        xpos, ypos = element.get("world")
        item = f"{x}:{y}"
        itemScene = scene.addText(item)
        itemScene.setPos(xpos, ypos)

def Create_visual_obstacles_index(scene, json_path: str):
    ...
