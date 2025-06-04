import os
import random
import sys
from pathlib import Path
import random

from PySide6 import QtCore, QtGui, QtWidgets
from calc_foot import calculate_foot_offset
import json
# CONSTANTS
BASE_DIR = Path(__file__).parent
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_PATH = os.path.join(SRC_DIR, "Assets", "Tests")
ASSETS_PATH = "./Assets/Tests/"
TILE_W = 64
TILE_H = 64


class TransparentWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()  # Importa as funcionalidades do QWidget
        self.grid = []
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # Janela transparente
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)       # Sem bordas
        self.setStyleSheet("background-color: transparent;")    # Fundo transparente
        layout = QtWidgets.QVBoxLayout(self)
        self.setWindowTitle("DwarfWorldWindow")

        self.scene = QtWidgets.QGraphicsScene(0, 0, 0, 0)
        self.creatingTiles()  # Preenche self.grid com posições isométricas

        self.sprite_sheet = QtGui.QPixmap(f"{ASSETS_PATH}Char.png")
        self.fw = 39
        self.fh = 58
        self.direction_index = 0
        self.current_index = 0
        self.target_index = 0

        start_x, start_y = self.grid[55]
        self.x, self.y = start_x, start_y
        self.target_x, self.target_y = start_x, start_y

        self.sprite_item = self.scene.addPixmap(self.get_current_frame())
        a = calculate_foot_offset(self.get_current_frame())
        self.sprite_item.setOffset(a)
        self.sprite_item.setZValue(1)  # Fica acima dos tiles
        self.sprite_item.setPos(self.x, self.y)

        view = QtWidgets.QGraphicsView(self.scene)
        view.setInteractive(False)
        view.setMinimumSize(640, 360)
        view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        layout.addWidget(view)
        layout.setContentsMargins(0, 0, 0, 0)

    def creatingTiles(self):
        """
        Cria uma grade isométrica de 10x10 tiles.
        Cada tile é posicionado de forma a simular perspectiva isométrica.
        """
        with open(f'../{ASSETS_PATH}noise.json', 'r') as file:
            data = json.load(file)
        for linha in range(10):       # eixo Y lógico
            for coluna in range(10):  # eixo X lógico
                v = data[linha][coluna]
                print(v)
                if v < 0.45:
                    pixmap = QtGui.QPixmap(f"../{ASSETS_PATH}agua.png")
                # elif v < 0.45:
                #     pixmap = QtGui.QPixmap(f"../{ASSETS_PATH}areia.png")
                else:
                    pixmap = QtGui.QPixmap(f"../{ASSETS_PATH}grama.png")
                pixmapitem = self.scene.addPixmap(pixmap)

                # Conversão de coordenadas de grid para coordenadas isométricas
                x = (coluna - linha) * (TILE_W / 2)
                y = (coluna + linha) * (TILE_H / 4)
                self.grid.append([x,y])
                pixmapitem.setPos(x, y)


    def choose_new_target(self):
        possible_targets = list(range(len(self.grid)))
        possible_targets.remove(self.current_index)  # Remove o índice atual para não escolher o mesmo
        self.target_index = random.choice(possible_targets)


    def get_current_frame(self):
        """
        Retorna o QPixmap da direção atual.
        """
        frame = self.sprite_sheet.copy(
            0,  # x sempre 0, já que só há uma coluna
            self.direction_index * self.fh,
            self.fw,
            self.fh
        )
        return frame



def Frame():
    app = QtWidgets.QApplication([])
    window = TransparentWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    Frame()
