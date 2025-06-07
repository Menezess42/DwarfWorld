import os
import random
import sys
from pathlib import Path
from PySide6 import QtCore, QtGui, QtWidgets
from calc_foot import calculate_foot_offset
import json

BASE_DIR = Path(__file__).parent
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_PATH = "./Assets/Tests/"
TILE_W = 32
TILE_H = 32

class TranparentWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.grid = []
        self.gridMiddle = []
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # Janela transparente
        # self.setWindowFlag(QtCore.Qt.FramelessWindowHint)       # Sem bordas
        self.setStyleSheet("background-color: transparent;")    # Fundo transparente
        layout = QtWidgets.QVBoxLayout(self)
        self.setWindowTitle("DwarfWorldWindow")
        
        
        self.scene = QtWidgets.QGraphicsScene(0, 0, 0, 0)
        self.creatingTiles()  # Preenche self.grid com posições isométricas
        self.seeGrid()
        
        self.sprite_sheet = QtGui.QPixmap(f"{ASSETS_PATH}/finalChar.png")
        self.fw = 18
        self.fh = 24
        self.direction_index = 3
        self.current_index = 0
        self.target_index = 0
        
        self.x, self.y = self.grid[0]
        
        #self.sprite_item = self.scene.addPixmap(self.get_current_frame())
        pixmap = self.get_current_frame()
        
        pixmap_copy = QtGui.QPixmap(pixmap)
        painter = QtGui.QPainter(pixmap_copy)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        
        pen = QtGui.QPen(QtGui.QColor("red"))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor("red")))
        
        radius = 1
        
        foot_offset = calculate_foot_offset(pixmap)
        
        a = calculate_foot_offset(self.get_current_frame())
        x, y = a.toTuple()
        
        painter.drawEllipse(QtCore.QPointF(x, y), radius, radius)
        pixmap_copy.save("frame_debug.png", "PNG")
        painter.end()
        
        self.sprite_item = self.scene.addPixmap(pixmap_copy)
        self.sprite_item.setOffset(x, y)
        self.sprite_item.setZValue(1)
        self.sprite_item.setPos(self.x, self.y)
        
        print(self.sprite_item.offset())
        
        view = QtWidgets.QGraphicsView(self.scene)
        view.setInteractive(False)
        view.setMinimumSize(640, 360)
        view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        layout.addWidget(view)
        layout.setContentsMargins(0, 0, 0, 0)
        
        
 
    def creatingTiles(self):
        """
        Cria uma grade 10x10 de pontos visíveis com espaçamento adequado.
        """
        spacing = 30  # Espaço entre os pontos para evitar sobreposição
        for linha in range(10):
            for coluna in range(10):
                x = coluna * spacing + 100
                y = linha * spacing + 100
                self.grid.append([x, y])
      
    # def creatingTiles(self):
    #     """
    #     Cria uma grade isométrica de 10x10 tiles.
    #     Cada tile é posicionado de forma a simular perspectiva isométrica.
    #     """
    #     # with open(f'{ASSETS_PATH}noise.json', 'r') as file:
    #     #     data = json.load(file)
    #     for linha in range(10):       # eixo Y lógico
    #         for coluna in range(10):  # eixo X lógico
    #             # x = (coluna - linha) * (TILE_W / 2)
    #             # y = (coluna + linha) * (TILE_H / 4)
    #             # x1 = x + (TILE_W / 2)
    #             # y1 = y + (TILE_H / 4)
    #             # x1 = x
    #             # y1 = y+8
    #             # self.gridMiddle.append([x1,y1])
    #             self.grid.append([coluna+100, linha+100])
                
    def seeGrid(self):
        for i in self.grid:
            item = "."
            itemScene = self.scene.addText(item)
            itemScene.setPos(i[0], i[1])
            itemScene.setDefaultTextColor('orange')
            
            
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
        print(type(frame))
        return frame
    
    
def Frame():
    app = QtWidgets.QApplication([])
    window = TranparentWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    Frame()
