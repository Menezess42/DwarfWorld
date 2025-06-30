# # World/main.py
# import json
# import random
# from pathlib import Path
# import numpy as np
# from PySide6 import QtCore, QtGui, QtWidgets
# from PySide6.QtCore import QObject, Signal, QPointF
# from PySide6.QtGui import QPolygonF, QPen
#
# ASSETS_PATH = Path(__file__).parent.parent / "Assets" / "Blocks"
# TILE_W, TILE_H = 32, 16
#
# class WorldGenerator(QObject):
#     matriz_criada = Signal(object)
#
#     def __init__(self):
#         super().__init__()
#
#     def gerar_mundo(self, scene, grid, size: int, json_path: str):
#         self._criar_tiles(scene, grid, size)
#         tiles_data = self._criar_overlay(scene, grid, size, json_path)
#         matriz = self.__criar_matriz_obstaculos(scene, json_path)
#         self.matriz_criada.emit(matriz)
#
#     def _criar_tiles(self, scene, grid_ref, size: int):
#         for line in range(size):
#             for column in range(size):
#                 pixmap = QtGui.QPixmap(str(ASSETS_PATH/"grama32.png"))
#                 item = scene.addPixmap(pixmap)
#                 x = ((column-line)+19)*(TILE_W/2)
#                 y = ((column+line)+6)*(TILE_H/2)
#                 item.setPos(x, y)
#                 grid_ref.append((x, y))
#
#     def _criar_overlay(self, scene, grid, size, json_path):
#         """
#         Gera o JSON de overlay *e* desenha sobre a cena um polygon para cada tile.
#         """
#         tiles_data = []
#         for idx, (x, y) in enumerate(grid):
#             row = idx // size
#             col = idx % size
#             # centro do losango
#             cx, cy = x + TILE_W/2, y + TILE_H/2
#             # vértices
#             verts = {
#                 "N": (cx,           y),
#                 "E": (x + TILE_W,   cy),
#                 "S": (cx,   y + TILE_H),
#                 "W": (x,      cy),
#             }
#             tiles_data.append({
#                 "grid":    [row, col],
#                 "world":   [cx, cy],
#                 "vertices": verts,
#                 "type":    "ground",
#                 "occupied": False,
#                 "layer":   col
#             })
#
#             # --- desenha o losango na cena ---
#             poly = QPolygonF([
#                 QPointF(*verts["N"]),
#                 QPointF(*verts["E"]),
#                 QPointF(*verts["S"]),
#                 QPointF(*verts["W"]),
#             ])
#             item = QtWidgets.QGraphicsPolygonItem(poly)
#             # usa caneta vermelha tracejada para ficar visível
#             pen = QPen(QtCore.Qt.red)
#             pen.setStyle(QtCore.Qt.DashLine)
#             item.setPen(pen)
#             scene.addItem(item)
#
#         # salva o JSON
#         with open(json_path, "w") as f:
#             json.dump(tiles_data, f, indent=2)
#
#         return tiles_data
#
#     def __criar_matriz_obstaculos(self, scene, json_path: str):
#         with open(json_path, "r") as f:
#             json_object = json.load(f)
#         layer = json_object[-1]['layer'] + 1
#         matriz = np.zeros((layer, layer, 4), dtype=int)
#         for d in json_object:
#             x, y = d['grid']
#             worldX, worldY = d['world']
#             matriz[x, y][0], matriz[x, y][1] = worldX, worldY
#
#         matriz = self.__gerar_labirinto_prim(matriz)
#
#         # desenha bolinha nos obstáculos
#         for element in matriz.reshape(-1, 4):
#             if element[2] == 1:
#                 dot = QtWidgets.QGraphicsEllipseItem(0, 0, 5, 5)
#                 dot.setBrush(QtGui.QBrush(QtGui.QColor("black")))
#                 dot.setPen(QtGui.QPen(QtCore.Qt.NoPen))
#                 dot.setPos(element[0]-1, element[1]-1)
#                 scene.addItem(dot)
#         return matriz
#
#     def __in_bounds(self, r, c, len_matriz):
#         return 0 <= r < len_matriz and 0 <= c < len_matriz
#
#     def __gerar_labirinto_prim(self, matriz):
#         matriz[:, :, 2] = 1
#         len_matriz = len(matriz)
#         start_row = random.randrange(1, len_matriz, 2)
#         start_col = random.randrange(1, len_matriz, 2)
#         matriz[start_row][start_col][2] = 0
#         paredes = []
#         for dr, dc in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
#             nr, nc = start_row + dr, start_col + dc
#             if self.__in_bounds(nr, nc, len_matriz):
#                 paredes.append((nr, nc, start_row, start_col))
#             while paredes:
#                 idx = random.randint(0, len(paredes) - 1)
#                 r, c, pr, pc = paredes.pop(idx)
#                 if not self.__in_bounds(r, c, len_matriz):
#                     continue
#                 if matriz[r][c][2] == 0:
#                     continue
#                 mid_r, mid_c = (r + pr) // 2, (c + pc) // 2
#                 if matriz[r][c][2] == 1:
#                     matriz[r][c][2] = 0
#                     matriz[mid_r][mid_c][2] = 0
#                     for dr, dc in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
#                         nr, nc = r + dr, c + dc
#                         if self.__in_bounds(nr, nc, len_matriz) and matriz[nr][nc][2] == 1:
#                             paredes.append((nr, nc, r, c))
#         return matriz

# World/main.py
import json
import random
from pathlib import Path
import numpy as np
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import QObject, Signal

ASSETS_PATH = Path(__file__).parent.parent / "Assets" / "Blocks"
TILE_W, TILE_H = 32, 16

class WorldGenerator(QObject):
    matriz_criada = Signal(object)

    def __init__(self):
        super().__init__()

    def gerar_mundo(self, scene, grid, size: int, json_path: str):
        self._criar_tiles(scene, grid, size)
        self._criar_overlay(grid, size, json_path)
        matriz = self.__criar_matriz_obstaculos(scene, json_path)
        self.matriz_criada.emit(matriz)

    def _criar_tiles(self, scene, grid_ref, size: int):
        for line in range(size):
            for column in range(size):
                pixmap = QtGui.QPixmap(str(ASSETS_PATH/"grama32.png"))
                item = scene.addPixmap(pixmap)
                x = ((column-line)+19)*(TILE_W/2)
                y = ((column+line)+6)*(TILE_H/2)
                item.setPos(x,y)
                grid_ref.append((x, y))

    def _criar_overlay(self, grid, size, json_path):
        tiles_data = []
        for idx, (x, y) in enumerate(grid):
            row = idx//size
            col = idx%size
            center = (x+TILE_W/2, y+TILE_H/2)
            tiles_data.append({
                "grid": [row, col],
                "world": list(center),
                "vertices": {
                    "N": [x + TILE_W/2, y],
                    "E": [x + TILE_W, y+TILE_H/2],
                    "S": [x + TILE_W/2, y + TILE_H],
                    "W": [x, y+TILE_H/2],
                    },
                "type": "ground",
                "occupied": False,
                "layer": col
                })
        with open(json_path, "w") as f:
            json.dump(tiles_data, f, indent=2)

    def __criar_matriz_obstaculos(self, scene, json_path: str):
        with open(json_path, "r") as f:
            json_object = json.load(f)
        layer = json_object[-1]['layer'] + 1
        matriz = np.zeros((layer, layer, 4), dtype=int)
        for d in json_object:
            x, y = d['grid']
            worldX, worldY = d['world']
            matriz[x, y][0], matriz[x, y][1] = worldX, worldY
        matriz = self.__gerar_labirinto_prim(matriz)
        for element in matriz.reshape(-1, 4):
            if element[2] == 1:
                dot = QtWidgets.QGraphicsEllipseItem(0, 0, 5, 5)
                dot.setBrush(QtGui.QBrush(QtGui.QColor("black")))
                dot.setPen(QtGui.QPen(QtCore.Qt.NoPen))
                dot.setPos(element[0]-1, element[1]-1)
                scene.addItem(dot)
        return matriz
#
    def __in_bounds(self, r, c, len_matriz):
        return 0 <= r < len_matriz and 0 <= c < len_matriz

    def __gerar_labirinto_prim(self, matriz):
        matriz[:, :, 2] = 1
        len_matriz = len(matriz)
        start_row = random.randrange(1, len_matriz, 2)
        start_col = random.randrange(1, len_matriz, 2)
        matriz[start_row][start_col][2] = 0
        paredes = []
        for dr, dc in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
            nr, nc = start_row + dr, start_col + dc
            if self.__in_bounds(nr, nc, len_matriz):
                paredes.append((nr, nc, start_row, start_col))
            while paredes:
                idx = random.randint(0, len(paredes) - 1)
                r, c, pr, pc = paredes.pop(idx)
                if not self.__in_bounds(r, c, len_matriz):
                    continue
                if matriz[r][c][2] == 0:
                    continue
                mid_r, mid_c = (r + pr) // 2, (c + pc) // 2
                if matriz[r][c][2] == 1:
                    matriz[r][c][2] = 0
                    matriz[mid_r][mid_c][2] = 0
                    for dr, dc in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
                        nr, nc = r + dr, c + dc
                        if self.__in_bounds(nr, nc, len_matriz) and matriz[nr][nc][2] == 1:
                            paredes.append((nr, nc, r, c))
        return matriz

