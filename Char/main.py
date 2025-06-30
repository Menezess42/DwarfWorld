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
        super().__init__() # Importa todos os metodos de QObject
        self.scene         = scene # Recebe a cena na qual tudo é exibido e se move
        # Definicao de algumas variáveis a serem utilizadas
        self.matriz        = None
        self.dwarf_sprite  = None
        self.wrench_sprite = None
        self.dwarf_pos     = None
        self.wrench_pos    = None

    def receber_matriz(self, matriz: np.ndarray):
        '''
        Inicializa a matriz e da inicio a ciclo de vida do anão
        '''
        self.matriz = matriz
        self._iniciar_ciclo()

    def _iniciar_ciclo(self):
        '''
        Metodo que cria o ciclo de vida do anão
        '''
        # limpa ciclo anterior
        self._remover_sprite(self.dwarf_sprite)
        self._remover_sprite(self.wrench_sprite)
        self._limpar_id(1)
        self._limpar_id(2)

        # posiciona wrench e dwarf
        self.wrench_pos, self.wrench_sprite = self._posicionar_objeto(ASSETS_PATH / "wrench.png", 1)
        self.dwarf_pos,  self.dwarf_sprite  = self._posicionar_objeto(ASSETS_PATH / "dwarf.png", 2)

        # calcula caminho -- Bem simples por agora, um A* do anão até sua arma
        path = pathfind(self.dwarf_pos, self.wrench_pos, self.matriz)

        # Anima a movimentação do anão em direção da sua arma
        mover_em_linha_reta(path, self.dwarf_sprite, self.matriz, on_finish=self._iniciar_ciclo)

    def _posicionar_objeto(self, image_path: Path, obj_id: int):
        '''
        Input:
            image_path: Path -- Caminho até o sprite do objeto;
            obj_id: int -- numero inteiro, identificador do objeto;
            
        '''
        # escolhe tile livre (sem parede e sem ocupação)
        x, y = self._achar_pos_livre()
        # Posiciona o objeto na localização escolhida adicionando o ID dele a quarta posição de um elemento da matriz
        self.matriz[x, y, 3] = obj_id

        # Pegando coordenadas do ponto central do tile
        world_x = self.matriz[x, y, 0]
        world_y = self.matriz[x, y, 1]

        # Corrigindo posicionamento para ficar em cima do tile(32x16) e não em cima do bloco inteiro (32x32)
        ground_y = world_y + TILE_H/2

        # posiciona sprite bottom‑center
        pixmap = QtGui.QPixmap(str(image_path)) # Cria o pixmap do sprite
        w, h = pixmap.width(), pixmap.height() # pega a largura e altura do pixmap
        sprite = QtWidgets.QGraphicsPixmapItem(pixmap) # Converte o pixelmap em um objeto grafico para ser exibido na cena
        sprite.setZValue(y + 0.5) # Conigura a camada de exibicao do objeto para que ele se ja plotado mais a frente
        sprite.setPos(world_x - w/2, ground_y - h) # Configura a plotagem do objeto, corrigindo seu posicionamento para que a parte inferior do sprite fique bem no centro do tile.
        self.scene.addItem(sprite) # Por fim adiciona o objeto a cena

        return (x, y), sprite # Retorna a localização do objeto na matriz e o sprite dele

    def _achar_pos_livre(self):
        livres = [ # Lista de pontos livres na matri
            (i, j) # Posição i, j na qual
            for i in range(self.matriz.shape[0]) # i esta dentro do comprimento da matriz
            for j in range(self.matriz.shape[1])  # j esta dentro do comprimento da matriz
            if self.matriz[i, j, 2] == 0 and self.matriz[i, j, 3] == 0 # Se i e j não estão ocupados por outr entidade ou a localização não é obstrucao(por agora parede)
        ]
        return random.choice(livres) # retorna uma escolha "aleatoria" dos pontos livres

    def _limpar_id(self, obj_id: int):
        '''
        Metodo para limpar o id dos objetos da matriz
        '''
        for i in range(self.matriz.shape[0]): # para cada i no comprimento
            for j in range(self.matriz.shape[1]): # para cada j na altura
                if self.matriz[i, j, 3] == obj_id: # Se a quarta posicao do elemento da matriz for igual ao id do objeto
                    self.matriz[i, j, 3] = 0 # zera essa posicao

    def _remover_sprite(self, sprite):
        '''
        Remove o sprite da cena
        '''
        if sprite: # Se sprite existir
            self.scene.removeItem(sprite) # entao remove ele da cena
