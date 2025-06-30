# main.py
from PySide6.QtWidgets import QApplication
from Window.main import TransparentWindow
from World.main import Create_overlay_grid, Create_tile_grid, Create_column_row_indexation
from Char.main import CharAnimator
from PySide6 import QtGui, QtWidgets
from pathlib import Path

def main():
    app = QApplication([])

    # Criando cena e grid
    scene = QtWidgets.QGraphicsScene(0, 0, 690, 400)
    grid = []

    # Criando tiles e overlay
    Create_tile_grid(scene, grid, size=16)
    Create_overlay_grid(scene, grid, size=16, json_path="tiles.json")
    Create_column_row_indexation(scene, json_path="tiles.json")

    # Criando personagem
    char_pixmap = QtGui.QPixmap("Assets/Blocks/grama32.png")
    window = TransparentWindow(scene, char_pixmap)

    # Animando personagem
    animator = CharAnimator(window.char_item, frame_w=18, frame_h=24)
    animator.load_path_from_json("tiles.json")
    animator.start(delay_ms=500)

    window.show()
    app.exec()

if __name__ == "__main__":
    main()
