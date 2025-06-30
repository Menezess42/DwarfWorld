# Char/main.py
from PySide6.QtCore import QObject
from PySide6 import QtGui, QtWidgets, QtCore
import numpy as np
import random
from pathlib import Path
from Char.pathfind import pathfind
from Char.movement import mover_em_linha_reta

ASSETS_PATH = Path(__file__).parent.parent / "Assets" / "Chars"
TILE_W, TILE_H = 32, 16

class CharManager(QObject):
    def __init__(self, scene):
        super().__init__()
        self.scene         = scene
        self.matriz        = None
        self.dwarf_sprite  = None
        self.wrench_sprite = None
        self.dwarf_pos     = None
        self.wrench_pos    = None

    def receber_matriz(self, matriz: np.ndarray):
        self.matriz = matriz
        self._iniciar_ciclo()

    def _iniciar_ciclo(self):
        # limpa ciclo anterior
        self._remover_sprite(self.dwarf_sprite)
        self._remover_sprite(self.wrench_sprite)
        self._limpar_id(1)
        self._limpar_id(2)

        # posiciona wrench e dwarf
        self.wrench_pos, self.wrench_sprite = self._posicionar_objeto(ASSETS_PATH / "wrench.png", 1)
        self.dwarf_pos,  self.dwarf_sprite  = self._posicionar_objeto(ASSETS_PATH / "dwarf.png", 2)

        # calcula caminho e anima
        path = pathfind(self.dwarf_pos, self.wrench_pos, self.matriz)
        mover_em_linha_reta(path, self.dwarf_sprite, self.matriz, on_finish=self._iniciar_ciclo)

    def _posicionar_objeto(self, image_path: Path, obj_id: int):
        # escolhe tile livre (sem parede e sem ocupação)
        x, y = self._achar_pos_livre()
        self.matriz[x, y, 3] = obj_id

        # coordenadas do tile
        world_x = self.matriz[x, y, 0]
        world_y = self.matriz[x, y, 1]
        ground_y = world_y + TILE_H/2

        # posiciona sprite bottom‑center
        pixmap = QtGui.QPixmap(str(image_path))
        w, h = pixmap.width(), pixmap.height()
        sprite = QtWidgets.QGraphicsPixmapItem(pixmap)
        sprite.setZValue(y + 0.5)
        sprite.setPos(world_x - w/2, ground_y - h)
        self.scene.addItem(sprite)

        return (x, y), sprite

    def _achar_pos_livre(self):
        livres = [
            (i, j)
            for i in range(self.matriz.shape[0])
            for j in range(self.matriz.shape[1])
            if self.matriz[i, j, 2] == 0 and self.matriz[i, j, 3] == 0
        ]
        return random.choice(livres)

    def _limpar_id(self, obj_id: int):
        for i in range(self.matriz.shape[0]):
            for j in range(self.matriz.shape[1]):
                if self.matriz[i, j, 3] == obj_id:
                    self.matriz[i, j, 3] = 0

    def _remover_sprite(self, sprite):
        if sprite:
            self.scene.removeItem(sprite)
# # Char/main.py
# from PySide6.QtCore import QObject
# from PySide6 import QtGui, QtWidgets, QtCore
# import numpy as np
# import random
# import json
# from pathlib import Path
# from Char.pathfind import pathfind
# from Char.movement import mover_em_linha_reta
#
# ASSETS_PATH     = Path(__file__).parent.parent / "Assets" / "Chars"
# TILES_JSON_PATH = Path(__file__).parent.parent / "tiles.json"
# TILE_W, TILE_H  = 32, 16
#
# class CharManager(QObject):
#     def __init__(self, scene):
#         super().__init__()
#         self.scene         = scene
#         self.matriz        = None
#         self.dwarf_sprite  = None
#         self.wrench_sprite = None
#         self.dwarf_pos     = None
#         self.wrench_pos    = None
#
#         # carrega o overlay JSON
#         with open(TILES_JSON_PATH, "r") as f:
#             self.tiles_data = json.load(f)
#
#     def receber_matriz(self, matriz: np.ndarray):
#         self.matriz = matriz
#         self._iniciar_ciclo()
#
#     def _iniciar_ciclo(self):
#         # limpa ciclo anterior
#         self._remover_sprite(self.dwarf_sprite)
#         self._remover_sprite(self.wrench_sprite)
#         self._limpar_id(1)
#         self._limpar_id(2)
#
#         # reposiciona
#         self.wrench_pos, self.wrench_sprite = self._posicionar_objeto(
#             ASSETS_PATH / "wrench.png", obj_id=1, color=QtGui.QColor("yellow")
#         )
#         self.dwarf_pos,  self.dwarf_sprite  = self._posicionar_objeto(
#             ASSETS_PATH / "dwarf.png",   obj_id=2, color=QtGui.QColor("red")
#         )
#
#         # calcula caminho e anima
#         path = pathfind(self.dwarf_pos, self.wrench_pos, self.matriz)
#         mover_em_linha_reta(path, self.dwarf_sprite, self.matriz, on_finish=self._iniciar_ciclo)
#
#     def _posicionar_objeto(self, image_path: Path, obj_id: int, color: QtGui.QColor):
#         # 1) tile livre
#         x, y = self._achar_pos_livre()
#         self.matriz[x, y, 3] = obj_id
#
#         # 2) encontra tile JSON por grid
#         tile_info = next(
#             (t for t in self.tiles_data if t["grid"] == [x, y]),
#             None
#         )
#         if tile_info is None:
#             raise RuntimeError(f"Tile grid={[x,y]} não encontrado em tiles.json")
#
#         # 3) desenha diamante com vértices reais
#         verts = tile_info["vertices"]
#         diamond = QtGui.QPolygonF([
#             QtCore.QPointF(*verts["N"]),
#             QtCore.QPointF(*verts["E"]),
#             QtCore.QPointF(*verts["S"]),
#             QtCore.QPointF(*verts["W"]),
#         ])
#         overlay = QtWidgets.QGraphicsPolygonItem(diamond)
#         overlay.setBrush(QtGui.QBrush(color))
#         overlay.setPen(QtGui.QPen(QtCore.Qt.NoPen))
#         overlay.setZValue(0)
#         self.scene.addItem(overlay)
#
#         # 4) posiciona sprite bottom‑center
#         world_x, world_y = tile_info["world"]
#         ground_y = world_y + TILE_H/2
#         pixmap = QtGui.QPixmap(str(image_path))
#         w, h = pixmap.width(), pixmap.height()
#         sprite = QtWidgets.QGraphicsPixmapItem(pixmap)
#         sprite.setZValue(y + 0.5)
#         sprite.setPos(world_x - w/2, ground_y - h)
#         self.scene.addItem(sprite)
#
#         return (x, y), sprite
#
#     def _achar_pos_livre(self):
#         livres = [
#             (i, j)
#             for i in range(self.matriz.shape[0])
#             for j in range(self.matriz.shape[1])
#             if self.matriz[i, j, 2] == 0 and self.matriz[i, j, 3] == 0
#         ]
#         return random.choice(livres)
#
#     def _limpar_id(self, obj_id: int):
#         for i in range(self.matriz.shape[0]):
#             for j in range(self.matriz.shape[1]):
#                 if self.matriz[i, j, 3] == obj_id:
#                     self.matriz[i, j, 3] = 0
#
#     def _remover_sprite(self, sprite):
#         if sprite:
#             self.scene.removeItem(sprite)
