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
TILE_W = 32
TILE_H = 32


class TransparentWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()  # Importa as funcionalidades do QWidget
        self.grid = []
        self.gridMiddle = []
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # Janela transparente
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)       # Sem bordas
        self.setStyleSheet("background-color: transparent;")    # Fundo transparente
        layout = QtWidgets.QVBoxLayout(self)
        self.setWindowTitle("DwarfWorldWindow")

        self.scene = QtWidgets.QGraphicsScene(0, 0, 0, 0)
        self.creatingTiles()  # Preenche self.grid com posições isométricas
        self.seeTileCoordinates()
        self.seeMiddleTileCoordinates()

        self.sprite_sheet = QtGui.QPixmap(f"{ASSETS_PATH}finalChar.png")
        self.fw = 18
        self.fh = 24
        self.direction_index = 3
        self.current_index = 0
        self.target_index = 0

        self.x, self.y = self.gridMiddle[55]

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
        with open(f'{ASSETS_PATH}noise.json', 'r') as file:
            data = json.load(file)
        for linha in range(20):       # eixo Y lógico
            for coluna in range(20):  # eixo X lógico
                # v = data[linha][coluna]
                # print(v)
                # if v < 0.45:
                #     pixmap = QtGui.QPixmap(f".{ASSETS_PATH}agua32.png")
                # # elif v < 0.45:
                # #     pixmap = QtGui.QPixmap(f"../{ASSETS_PATH}areia.png")
                # else:
                #     pixmap = QtGui.QPixmap(f"{ASSETS_PATH}grama32.png")
                pixmap = QtGui.QPixmap(f"{ASSETS_PATH}grama32.png")
                pixmapitem = self.scene.addPixmap(pixmap)

                # Conversão de coordenadas de grid para coordenadas isométricas
                x = (coluna - linha) * (TILE_W / 2)
                y = (coluna + linha) * (TILE_H / 4)
                pixmapitem.setPos(x-(TILE_W/3), y+(TILE_H/2))
                # x1 = x + (TILE_W / 2)
                # y1 = y + (TILE_H / 4)
                x1 = x
                y1 = y+8
                self.gridMiddle.append([x1,y1])
                self.grid.append([x,y])
    
    def seeTileCoordinates(self):
        for i in self.grid:
            item = "."
            itemScene = self.scene.addText(item)
            print(i)
            itemScene.setPos(i[0], i[1])
            itemScene.setDefaultTextColor('orange')
            
    def seeMiddleTileCoordinates(self):
        for i in self.gridMiddle:
            item = ";"
            itemScene = self.scene.addText(item)
            itemScene.setPos(i[0], i[1])
            itemScene.setDefaultTextColor('black')


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
