import os
import random
import sys
from pathlib import Path
import random

from PySide6 import QtCore, QtGui, QtWidgets

# CONSTANTS
BASE_DIR = Path(__file__).parent
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_PATH = os.path.join(SRC_DIR, "Assets", "Tests")
ASSETS_PATH = "./Assets/Tests/"
TILE_W = 64
TILE_H = 64

test = [
        [0.0, 0.0], [32.0, 16.0], [64.0, 32.0], [96.0, 48.0], [128.0, 64.0], [160.0, 80.0], [192.0, 96.0], [224.0, 112.0], [256.0, 128.0], [288.0, 144.0], [-32.0, 16.0], [0.0, 32.0], [32.0, 48.0], [64.0, 64.0], [96.0, 80.0], [128.0, 96.0], [160.0, 112.0], [192.0, 128.0], [224.0, 144.0], [256.0, 160.0], [-64.0, 32.0], [-32.0, 48.0], [0.0, 64.0], [32.0, 80.0], [64.0, 96.0], [96.0, 112.0], [128.0, 128.0], [160.0, 144.0], [192.0, 160.0], [224.0, 176.0], [-96.0, 48.0], [-64.0, 64.0], [-32.0, 80.0], [0.0, 96.0], [32.0, 112.0], [64.0, 128.0], [96.0, 144.0], [128.0, 160.0], [160.0, 176.0], [192.0, 192.0], [-128.0, 64.0], [-96.0, 80.0], [-64.0, 96.0], [-32.0, 112.0], [0.0, 128.0], [32.0, 144.0], [64.0, 160.0], [96.0, 176.0], [128.0, 192.0], [160.0, 208.0], [-160.0, 80.0], [-128.0, 96.0], [-96.0, 112.0], [-64.0, 128.0], [-32.0, 144.0], [0.0, 160.0], [32.0, 176.0], [64.0, 192.0], [96.0, 208.0], [128.0, 224.0], [-192.0, 96.0], [-160.0, 112.0], [-128.0, 128.0], [-96.0, 144.0], [-64.0, 160.0], [-32.0, 176.0], [0.0, 192.0], [32.0, 208.0], [64.0, 224.0], [96.0, 240.0], [-224.0, 112.0], [-192.0, 128.0], [-160.0, 144.0], [-128.0, 160.0], [-96.0, 176.0], [-64.0, 192.0], [-32.0, 208.0], [0.0, 224.0], [32.0, 240.0], [64.0, 256.0], [-256.0, 128.0], [-224.0, 144.0], [-192.0, 160.0], [-160.0, 176.0], [-128.0, 192.0], [-96.0, 208.0], [-64.0, 224.0], [-32.0, 240.0], [0.0, 256.0], [32.0, 272.0], [-288.0, 144.0], [-256.0, 160.0], [-224.0, 176.0], [-192.0, 192.0], [-160.0, 208.0], [-128.0, 224.0], [-96.0, 240.0], [-64.0, 256.0], [-32.0, 272.0], [0.0, 288.0]]


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
        self.direction_index = 3

        self.current_index = 0
        self.target_index = 0

        # Inicializa as posições do personagem com base na grid
        start_x, start_y = self.grid[self.current_index]
        self.x, self.y = start_x, start_y
        self.target_x, self.target_y = start_x, start_y

        self.sprite_item = self.scene.addPixmap(self.get_current_frame())
        self.sprite_item.setZValue(1)  # Fica acima dos tiles
        self.sprite_item.setPos(self.x, self.y)

        self.move_timer = QtCore.QTimer()
        self.move_timer.timeout.connect(self.update_position)
        self.move_timer.start(500)

        self.choose_new_target()

        view = QtWidgets.QGraphicsView(self.scene)
        view.setInteractive(False)
        view.setMinimumSize(640, 480)
        view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        layout.addWidget(view)
        layout.setContentsMargins(0, 0, 0, 0)

    def creatingTiles(self):
        """
        Cria uma grade isométrica de 10x10 tiles.
        Cada tile é posicionado de forma a simular perspectiva isométrica.
        """
        for linha in range(10):       # eixo Y lógico
            for coluna in range(10):  # eixo X lógico
                pixmap = QtGui.QPixmap(f"{ASSETS_PATH}grama.png")
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

    def update_position(self):
        if self.current_index == self.target_index:
            self.choose_new_target()
            return
        
        # Simplesmente caminha em direção ao target index um passo (tile) por vez
        if self.current_index < self.target_index:
            self.current_index += 1
            self.direction_index = 0  # ou ajuste a direção conforme a necessidade
        else:
            self.current_index -= 1
            self.direction_index = 2  # exemplo de direção oposta

        # Atualiza as coordenadas baseadas no tile atual
        self.x, self.y = self.grid[self.current_index]

        # Atualiza o sprite visual e a posição na cena
        self.sprite_item.setPixmap(self.get_current_frame())
        self.sprite_item.setPos(self.x, self.y)


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
