# main.py
from PySide6.QtWidgets import QApplication
from Window.main import TransparentWindow
from World.main import WorldGenerator
from Char.main import CharManager
from PySide6 import QtGui, QtWidgets

def main():
    SIZE = 13
    app = QApplication()
    scene = QtWidgets.QGraphicsScene(0, 0, 690, 400)
    grid = []

    world = WorldGenerator()
    char_manager = CharManager(scene)

    # Conecta o sinal
    world.matriz_criada.connect(char_manager.receber_matriz)


    # Janela criada vazia por enquant
    window = TransparentWindow(scene)
    window.show()

    # chama geração do mundo (tiles, overlay, matriz de obstáculos)
    world.gerar_mundo(scene, grid, SIZE, "tiles.json")
    
    app.exec()

if __name__ == "__main__":
    main()
