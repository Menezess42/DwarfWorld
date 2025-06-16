# Importations
import os
import random
import sys
from pathlib import Path

from PySide6 import QtCore, QtGui, QtWidgets

from Window.calc_foot import calculate_foot_offset

# CONSTANTS
BASE_DIR = Path(__file__).parent.parent
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
print(SRC_DIR)
ASSETS_PATH = os.path.join(BASE_DIR, "Assets")
BlOCK_W = 32
BLOCK_H = 32
TILE_W = 32
TILE_H = 16


class TransparentWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()  # Import all the functionalities
        self.grid = []  # Save the coordinates for the tile placing grid
        # self.setAttribute(
        #     QtCore.Qt.WA_TranslucentBackground
        # )  # Removing background and set to transluce
        # self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # Removing the window's frame
        # self.setStyleSheet(
        #     "Background-color: transparent;"
        # )  # Set the background color to be transparent
        self.setWindowTitle("DwarfWorldWindow")  # Set the window name

        layout = QtWidgets.QVBoxLayout(
            self
        )  # Set the parent for all the widgets. In this case all the widgets are childrens of this class

        # self.scene = QtWidgets.QGraphicsScene(0, 0, 640, 360)
        self.scene = QtWidgets.QGraphicsScene(0, 0, 640, 360)
        self.scene.addRect(0, 0, 640, 360)  # Vai aparecer no canto superior esquerdo do view

        # scene = QGraphicsScene(-50, -50, 100, 100)
        # scene.addRect(0, 0, 50, 50)  # O retângulo vai aparecer deslocado (vai precisar ajustar o view)

        self.creating_Tiles(size=2)
        self.see_Tile_Coordinates()

        view = QtWidgets.QGraphicsView(self.scene)
        view.setInteractive(False)
        view.setMinimumSize(660, 380)
        view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        layout.addWidget(view)
        layout.setContentsMargins(0, 0, 0, 0)

    def creating_Tiles(self, size: int):
        """Create a ismotric tile grid.

        Seting all the png to simulate a isometric tile grid layout.

        Args:
            <size int>: set the grid size, qtde of tiles.
        """
        for line in range(size):
            for column in range(size):
                block_pixmap = QtGui.QPixmap(f"{ASSETS_PATH}/Blocks/grama32.png")
                debug_block_pixmap = QtGui.QPixmap(block_pixmap)

                offset_x = TILE_W/2
                offset_y = TILE_H/2

                painter = QtGui.QPainter(debug_block_pixmap)
                pen = QtGui.QPen(QtGui.QColor("red"))
                pen.setWidth(1)
                painter.setPen(pen)
                painter.drawEllipse(QtCore.QPointF(offset_x, offset_y), 1, 1)
                painter.end()

                debug_block_pixmap.save(f"{BASE_DIR}/Window/debug_image.png")

                block_item = self.scene.addPixmap(debug_block_pixmap)
                block_item.setOffset(offset_x, offset_y)

                x = (column - line) * (TILE_W / 2)
                y = (column - line) * (TILE_H / 2)

                block_item.setPos(x, y)

                self.grid.append([x, y])

    def see_Tile_Coordinates(self):
        for i in self.grid:
            item = f"{int(i[0])}:{int(i[1])}"
            itemScene = self.scene.addText(item)
            itemScene.setPos(i[0], i[1])
            itemScene.setDefaultTextColor("black")


def Frame():
    app = QtWidgets.QApplication([])
    window = TransparentWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    Frame()
