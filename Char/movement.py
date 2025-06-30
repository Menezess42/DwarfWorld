# Char/movement.py
from PySide6.QtCore import QTimer
from PySide6 import QtWidgets

TILE_H = 16  # só precisamos da altura para recalcular ground em cada tile

def mover_em_linha_reta(path, sprite_item: QtWidgets.QGraphicsPixmapItem,
                        matriz, delay=100, passos_por_tile=10, on_finish=None):
    '''
    Metodo para fazer o anão se movimentar pelo campo
    inputs:
        <path>: list -- Lista de caminhhos do anão ate sua arma;
        <sprite_item>: QGraphicsPixmapItem -- sprite do anão, ja em formato de pixmapItem para a ser usado na cena;
        <matriz>: numpy matrix -- Matriz que representa o mundo de forma logica. Contem as coordenadas do ponto central dos tiles assim como se essa posicao esta ocupada ou nao e qual o ID do item que esta nessa posicao;
        <delay>: int -- Tempo de delay, atraso dos passos do anão. Quanto menor o valor, mais rapido o anão anda;
        <passo_por_tile>: int -- quantos passos ele da em cada tile, ou seja, o quanto leva para ele andar de um tile para o outro;
        <on_finish>: method -- Passa o metodo privado _inicia_ciclo do Char.main.CharManager para realizar callback quando o anão chegar ao seu objetivo e parar de andar;
    '''
    if not path: # Se o caminho é vazio, se nao existe caminho do anão ate sua arma entao nao faz nada
        return

    # Inicializacao de variaveis
    index = 0 
    subpasso = 0 # Valor incremental que representa o quanto o anão já andou na direção de sair do tile: exemplo se passos_por_tile=10 e subpasso está em 5, significa que o anão já andou .5, ou 50%, do caminho da transição entre tiles
    timer = QTimer() # Classe que permite agendar a execucao de funcoes apos um certo tempo ou repetidamente em intervalos regulares

    def mover():
        '''
        Metodo principal. Responsavel por fazer o anao andar visualmente sem ficar pulando de tile em tile
        '''
        nonlocal index, subpasso # Declaracao de variaveis nao locais. As criadas anteriormente

        # fim do trajeto - O anão andou ate seu objetivo
        if index >= len(path) - 1: # Se o index ja e maior que o len da lista path
            timer.stop() # Para o relogio
            if on_finish: # Se terminou entao 
                on_finish() # faz callback da funcao privada _inicia_ciclo
            return # se nao conseguir fazer callback retorna vazio

        x1, y1 = path[index] # Pega as cordenadas do primeiro ponto do caminho A* (Coordenadas da matriz, ou seja, linha coluna. Não as coordenadas do tile em si)
        x2, y2 = path[index + 1] # Pega as coordendas do segundo ponto do caminho A*
        px1, py1 = matriz[x1, y1, 0], matriz[x1, y1, 1] # Pega as coordendas do ponto central do tile do primeiro ponto do caminho A*
        px2, py2 = matriz[x2, y2, 0], matriz[x2, y2, 1] # Pega as coordenadas do ponto central do tile do segundo ponto do caminho A*

        t = subpasso / passos_por_tile # t é um valor que vai de 0 até 1, representando o quão longe ele já foi na transição entre dois tiles.

        # LERP
        # É a interpolacao: Dado um ponto inicial (px1, py1) e um final (px2, py2), e um valor t entre 0 e 1, isso calcula um ponto entre os dois proporcional a t.
        #   Se t=0, ele esta no inicio;
        #   se t=1, ele chegou no final;
        #   se t=.5, ele esta no meio do caminho;
        nx = px1 + (px2 - px1) * t
        ny = py1 + (py2 - py1) * t

        # ajusta bottom‑center igual ao posicionamento inicial
        pixmap = sprite_item.pixmap() # Pega o sprite em formato pixmap
        w, h = pixmap.width(), pixmap.height() # Pega a largura e altura do sprite
        sprite_item.setPos(nx - w/2, ny + TILE_H/2 - h) # Aqui e onde e realizado a forma correta de ancoragem visual para que o sprite fique em cima do tile e nao em cima do bloco.
        sprite_item.setZValue(y2 + 0.5) # Define o zvalue do sprite para que ele fique na frente do que deve e atrás do que deve

        subpasso += 1 # incrementa subpasso
        if subpasso > passos_por_tile: # Se subpasso chegou ao limite entao
            subpasso = 0 # zera o subpasso
            index += 1 # incrementa o index

    timer.timeout.connect(mover) # Conecta o sinal de timeout do QTimer com a funcao mover. Que deve ser executada periodicamente. O QTimer dispara o sinal a cada delay milisegundos.
    timer.start(delay) # Liga o timer para disparar os tiques a cada milesegundos definidos no delay
    sprite_item._timer = timer # Gambiarra útil. Guarda o timer dentro do sprite para evitar que ele seja coletado pelo garbage collector
