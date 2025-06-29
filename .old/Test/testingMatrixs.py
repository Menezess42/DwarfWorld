# Importações
import os
import random
import sys
from pathlib import Path
import json
from PySide6 import QtCore, QtGui, QtWidgets
import numpy as np
from queue import PriorityQueue
from astar import Astar

# CONSTANTES
BASE_DIR = Path(__file__).parent.parent
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_PATH = os.path.join(BASE_DIR, "Assets")

# MATRIZ 20x20x4
matriz = np.zeros((20, 20, 5), dtype=int)

# Classes com IDs
class Char:
    def __init__(self):
        self.id = 1

class Wrench:
    def __init__(self):
        self.id = 2

dummy = Char()
wrench = Wrench()

# Leitura do arquivo tiles.json
a = ""
file_path = f"{BASE_DIR}/Test/tiles.json"
with open(file_path) as f:
    a = json.load(f)

while a:
    b = a.pop(0)
    row, col = b.get("grid")
    matriz[row][col][0:2] = b.get("world")

# Função para verificar se a célula está dentro dos limites
def in_bounds(r, c):
    return 0 <= r < 20 and 0 <= c < 20

# Geração de labirinto com algoritmo de Prim

def gerar_labirinto_prim(matriz):
    matriz[:, :, 3] = 1
    start_row = random.randrange(1, 20, 2)
    start_col = random.randrange(1, 20, 2)
    matriz[start_row][start_col][3] = 0
    paredes = []
    for dr, dc in [(-2,0), (2,0), (0,-2), (0,2)]:
        nr, nc = start_row + dr, start_col + dc
        if in_bounds(nr, nc):
            paredes.append((nr, nc, start_row, start_col))
    while paredes:
        idx = random.randint(0, len(paredes) - 1)
        r, c, pr, pc = paredes.pop(idx)
        if not in_bounds(r, c):
            continue
        if matriz[r][c][3] == 0:
            continue
        mid_r, mid_c = (r + pr) // 2, (c + pc) // 2
        if matriz[r][c][3] == 1:
            matriz[r][c][3] = 0
            matriz[mid_r][mid_c][3] = 0
            for dr, dc in [(-2,0), (2,0), (0,-2), (0,2)]:
                nr, nc = r + dr, c + dc
                if in_bounds(nr, nc) and matriz[nr][nc][3] == 1:
                    paredes.append((nr, nc, r, c))

# Executa labirinto
gerar_labirinto_prim(matriz)

# Posicionamento

def place_wrench():
    row, col = random.randint(0, 19), random.randint(0, 19)
    while matriz[row][col][3] > 0:
        row, col = random.randint(0, 19), random.randint(0, 19)
    matriz[row][col][2] = wrench.id
    return (row, col)

def place_dummy():
    row, col = random.randint(0, 19), random.randint(0, 19)
    while matriz[row][col][2] > 0 or matriz[row][col][3] > 0:
        row, col = random.randint(0, 19), random.randint(0, 19)
    matriz[row][col][2] = dummy.id
    return (row, col)

wren_coords = place_wrench()
dummy_coords = place_dummy()

# Interface Gráfica
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from PySide6.QtGui import QPainter, QColor

CELL_SIZE = 20
GRID_SIZE = 20

class GridWidget(QWidget):
    def __init__(self, matriz):
        super().__init__()
        self.matriz = matriz
        self.setFixedSize(GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE + 40)
        self.astar_gen = None
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.proximo_passo)

    def iniciar_astar(self):
        self.astar = Astar(start=dummy_coords, goal=wren_coords, matriz=matriz)
        self.astar_gen = self.astar.step_generator()
        self.timer.start() # meio segundo


    def proximo_passo(self):
        try:
            current, vizinhos = next(self.astar_gen)
            row, col = current

            if not vizinhos:
                self.matriz[row][col][4] = -3  # roxo (caminho final)
            else:
                self.matriz[row][col][4] = -1  # verde (atual)
                for vr, vc in vizinhos:
                    if self.matriz[vr][vc][4] == 0:
                        self.matriz[vr][vc][4] = -2  # vermelho (vizinhos)
            self.update()
        except StopIteration:
            self.timer.stop()

    def paintEvent(self, event):
        painter = QPainter(self)
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                cell = self.matriz[row][col]
                x, y = col * CELL_SIZE, row * CELL_SIZE

                if cell[3] == 1:
                    color = QColor(0, 0, 0)  # parede
                elif cell[2] > 0:
                    color = QColor(0, 0, 255)  # objeto (azul) → prioridade máxima
                elif cell[4] == -1:
                    color = QColor(0, 255, 0)  # atual (verde)
                elif cell[4] == -2:
                    color = QColor(255, 0, 0)  # vizinho (vermelho)
                elif cell[4] == -3:
                    color = QColor(128, 0, 128)  # caminho final (roxo)
                else:
                    color = QColor(255, 255, 255)  # vazio

                painter.fillRect(x, y, CELL_SIZE, CELL_SIZE, color)
                painter.setPen(QColor(200, 200, 200))
                painter.drawRect(x, y, CELL_SIZE, CELL_SIZE)


# Execução
if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = QWidget()
    layout = QVBoxLayout()
    grid = GridWidget(matriz)
    btn = QPushButton("Iniciar A*")
    btn.clicked.connect(grid.iniciar_astar)
    layout.addWidget(grid)
    layout.addWidget(btn)
    janela.setLayout(layout)
    janela.show()
    sys.exit(app.exec())
