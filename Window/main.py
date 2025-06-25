
# Importations
import os
import random
import sys
from pathlib import Path
import json
from PySide6 import QtCore, QtGui, QtWidgets

from Window.calc_foot import calculate_foot_offset

# CONSTANTS
BASE_DIR = Path(__file__).parent.parent
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_PATH = os.path.join(BASE_DIR, "Assets")
BlOCK_W = 32
BLOCK_H = 32
TILE_W = 32
TILE_H = 16


class TransparentWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()  # Import all the functionalities
        self.grid = []  # Save the coordinates for the tile placing grid
        self.setAttribute(
            QtCore.Qt.WA_TranslucentBackground
        )  # Removing background and set to transluce
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # Removing the window's frame
        self.setStyleSheet(
            "Background-color: transparent;"
        )  # Set the background color to be transparent
        self.setWindowTitle("DwarfWorldWindow")  # Set the window name

        layout = QtWidgets.QVBoxLayout(
            self
        )  # Set the parent for all the widgets. In this case all the widgets are childrens of this class

        self.scene = QtWidgets.QGraphicsScene(0, 0, 690, 400)
        # self.scene.setBackgroundBrush(QtGui.QBrush(QtGui.QColor("magenta")))
        self.creating_Tiles(20)
        # self.makeGrid() a = self.scene.addRect(0, 0, 640, 384)  # O retângulo vai aparecer deslocado (vai precisar ajustar o view)
        # self.see_Tile_Coordinates()
        # self.create_overlay_grid(size=20)
        

        # creating ovelay matrix
        # self.overlay_matrix = [[0, 0, 0, 0]]
        # Char
        self.char = QtGui.QPixmap(f"{ASSETS_PATH}/Tests/FinalChar3.png")
        self.char_fw = 18
        self.char_fh = 24
        self.char_item = self.scene.addPixmap(self.char)
        self.animate_char_over_tiles()


        view = QtWidgets.QGraphicsView(self.scene)
        view.setInteractive(False)
        view.setMinimumSize(690, 400)
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
                block_item = self.scene.addPixmap(block_pixmap)
                x = ((column-line)+19) * (TILE_W / 2)
                y = ((column+line)+6) * (TILE_H / 2)
                block_item.setPos(x, y)

                self.grid.append([x, y])
    
    def see_Tile_Coordinates(self):
        for x, y in self.grid:
            dot = QtWidgets.QGraphicsEllipseItem(0, 0, 2, 2)
            dot.setBrush(QtGui.QBrush(QtGui.QColor("black")))
            dot.setPen(QtGui.QPen(QtCore.Qt.NoPen))
            dot.setPos(x - 1, y - 1)  # Centraliza o ponto no tile
            self.scene.addItem(dot)

    def makeGrid(self):
        i = 0
        j = 0
        while i < 640:
            j = 0
            while j <380:
                self.scene.addRect(i, j, 32, 32)
                j+=32
            i+=32

    def create_overlay_grid(
        self,
        size: int,
        json_path: str = "tiles.json",
        show_overlay: bool = False,
        show_centers: bool = False
    ):
        """
        Gera tiles isométricos com opcional overlay visual e exporta dados JSON com:
          - grid: linha, coluna
          - world: centro do tile
          - vertices: N, E, S, W do losango
          - type: 'ground'
          - occupied: False
        """

        tiles_data = []

        for idx, (x, y) in enumerate(self.grid):
            row = idx // size
            col = idx % size

            # Vértices do losango
            north = (x + TILE_W / 2, y)
            east  = (x + TILE_W, y + TILE_H / 2)
            south = (x + TILE_W / 2, y + TILE_H)
            west  = (x, y + TILE_H / 2)
            center = (x + TILE_W / 2, y + TILE_H / 2)

            # Visual do overlay
            if show_overlay:
                diamond = QtGui.QPolygonF([
                    QtCore.QPointF(*north),
                    QtCore.QPointF(*east),
                    QtCore.QPointF(*south),
                    QtCore.QPointF(*west),
                ])
                poly_item = QtWidgets.QGraphicsPolygonItem(diamond)
                poly_item.setBrush(QtGui.QBrush(QtGui.QColor(255, 0, 0, 60)))
                poly_item.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0, 50)))
                poly_item.setZValue(2)
                self.scene.addItem(poly_item)

            # Visual do ponto central
            if show_centers:
                dot = QtWidgets.QGraphicsEllipseItem(0, 0, 3, 3)
                dot.setBrush(QtGui.QBrush(QtGui.QColor("blue")))
                dot.setPen(QtGui.QPen(QtCore.Qt.NoPen))
                dot.setPos(center[0] - 1.5, center[1] - 1.5)
                dot.setZValue(3)
                self.scene.addItem(dot)

            # Registro de dados para JSON
            tiles_data.append({
                "grid":    [row, col],
                "world":   list(center),
                "vertices": {
                    "N": list(north),
                    "E": list(east),
                    "S": list(south),
                    "W": list(west)
                },
                "type":    "ground",
                "occupied": False
            })

        # Salvamento do JSON
        with open(f"{BASE_DIR}/Window/{json_path}", "w") as f:
            json.dump(tiles_data, f, indent=2)


    def animate_char_over_tiles(self, json_path="tiles.json", delay_ms=150):
        """
        Lê as coordenadas dos tiles no JSON e move o char sequencialmente por eles.
        """

        # Carrega os dados do JSON
        with open(f"{BASE_DIR}/Window/{json_path}", "r") as f:
            tile_data = json.load(f)

        # Salva os pontos (centros dos tiles)
        path_points = [tuple(tile["world"]) for tile in tile_data]

        # Cria um timer sequencial
        self.step_index = 0
        self.timer = QtCore.QTimer()
        
        def move_step():
            if self.step_index >= len(path_points):
                self.timer.stop()
                return

            cx, cy = path_points[self.step_index]
            
            # Aplica offset para centralizar o char no meio inferior
            self.char_item.setPos(cx - self.char_fw / 2, cy - self.char_fh)

            self.step_index += 1

        self.timer.timeout.connect(move_step)
        self.timer.start(delay_ms)

def Frame():
    app = QtWidgets.QApplication([])
    window = TransparentWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    Frame()
