# World/main.py
import json
import random
from pathlib import Path
import numpy as np
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import QObject, Signal

# CONSTANTES GLOBAIS
ASSETS_PATH = Path(__file__).parent.parent / "Assets" / "Blocks"
TILE_W, TILE_H = 32, 16

class WorldGenerator(QObject):
    '''
    Cria a ilha e lida com tudo que e relacionado ao mundo
    '''
    matriz_criada = Signal(object) # Cria um sinal do tipo objeto: Sinal é como o Qt se comunica entre métodos e outras coisas quando é preciso trablhar fora do escopo de um codigo que roda top down. Parecido com as funcoes compartilhadas entre classe no javascript

    def __init__(self):
        super().__init__() # Heda todos os metodos da classe QObject

    def gerar_mundo(self, scene, grid, size: int, json_path: str):
        '''
        Funcao responsavel por criar o mundo visivel e o grid overlay que trabalha com posicionamento dos chars e outros objetos
        '''
        self._criar_tiles(scene, grid, size) # Cria os tiles png visiveis
        self._criar_overlay(grid, size, json_path) # Cria os tiles overlay
        matriz = self.__criar_matriz_obstaculos(scene, json_path) # Cria o labirinto
        self.matriz_criada.emit(matriz) # Emite o sinal de que a matriz esta pronta para uso

    def _criar_tiles(self, scene, grid_ref, size: int):
        '''
        Cria o tile isometrico visivel.
        Input:
            <scene> -- Cena onde tudo sera exibido e trabalhado;
            <grid_ref> -- Grid de referencia. Armazena o XY de cada bloco colocado na ilha
            <siz>: int -- tamanho do grid. Sendo a matriz de tamanho final size*size;

        '''
        for line in range(size):
            for column in range(size):
                pixmap = QtGui.QPixmap(str(ASSETS_PATH/"grama32.png")) # Converte o bloco isometrico de grama em um pixmap
                item = scene.addPixmap(pixmap) # adiciona o pixmap da grama a cena
                x = ((column-line)+19)*(TILE_W/2) # define a coordenada x para o posicionamento. (column-line)*(TILE_W/2) é conta para a isometrica ficar correta. O +19 é um valor que chegeui por tentativa para poder centralizar a ilha na cena e ainda nao entendi porque especificamente 19
                y = ((column+line)+6)*(TILE_H/2) # Define a coordenada y para o posicionamento.
                item.setPos(x,y) # Coloca o bloco de grama no lugar correto.
                grid_ref.append((x, y)) # Salva o XY numa lista auxiliar

    def _criar_overlay(self, grid, size, json_path):
        '''
        Metodo responsavel por criar o grid invisivel por cima do grid visivel. Esse grid invisivel e responsavel por todo o trabalhao de posicionamento de outros objetos e movimentacao de personagens.
        Inputs:
            <grid> -- Grid da configuracao do grid visivel;
            <size> -- valor que define o tamanho do grid. Sendo tamanho=size*size;
            <json_path> -- Caminho na qual o json com os dados do grid overlay sera adicionado;
        '''
        tiles_data = [] # os dados desse grid overlay serao armazenados aqui
        for idx, (x, y) in enumerate(grid): # Para cada (x, y) armazenado no grid. Assim como index da "contagem" da iteracao
            row = idx//size # Coluna e o index dividido pelo size (sem resto)
            col = idx%size # Coluna e o resto da divisao do index pelo size
            center = (x+TILE_W/2, y+TILE_H/2) # O centro do tile overlay e o ponto X mais o comprimento do tile/2 e Y mais a altura do tile dividido por 2
            tiles_data.append({
                # Cria o dicionario com todas as informacoes relevantes para serem armazenadas no json
                "grid": [row, col], # Posicao daquele tile no grid
                "world": list(center), # Guarda as coordenadas centrais do tile
                "vertices": { # Guarda os pontos N,E,S,W do tile caso seja preciso desenha-lo para depuracao
                    "N": [x + TILE_W/2, y],
                    "E": [x + TILE_W, y+TILE_H/2],
                    "S": [x + TILE_W/2, y + TILE_H],
                    "W": [x, y+TILE_H/2],
                    },
                "type": "ground", # Define o tipo. Ainda nao tem funcionalidade definida
                "occupied": False, # Define se esse tile esta ocupado ou nao. Ainda nao tem funcionalidade definida
                "layer": col # Layer sera utilizado futuramente para definir o Z-value dos objetos
                })
        with open(json_path, "w") as f:
            json.dump(tiles_data, f, indent=2) # Salva o dicionario

    def __criar_matriz_obstaculos(self, scene, json_path: str):
        '''Função que talvez não vale a pena comentar. É só uma função para testar outras funcionalidades do programa e que não cabe ao escopo do projeto e logo será enviada para a pasta .old. Ou talvez essa função seja rdesmantelada e aproveitada em partes para o uso futuro de posicionamento de arvores e outras coisas'''
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
        '''
        Metodo utilizado para verificar se um ponto esta constrito dentro dos limites possiveis
        '''
        return 0 <= r < len_matriz and 0 <= c < len_matriz

    def __gerar_labirinto_prim(self, matriz):
        '''
        Função de testes A*. Cria um labirinto. Não é aplicavel ao escopo do projeto e sera movida para o .old futuramente
        '''
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

