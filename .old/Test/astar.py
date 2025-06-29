# Algoritmo A* — Pseudocódigo explicativo (com yield passo a passo)
import queue

import numpy as np


class Astar:
    def heuristica(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def __init__(self, *args, **kwargs):
        # Iniciando estrutura de dados
        if args:  # Inicializando sem passar nome de variável
            self.start = args[0]
            self.goal = args[1]
            self.matriz = args[2]
        elif kwargs:  # Inicializando passando nome de variável
            self.start = kwargs.get("start")
            self.goal = kwargs.get("goal")
            self.matriz = kwargs.get("matriz")
        self.matriz_linha, self.matriz_col = self.matriz.shape[:2]
        self.matriz_shape = self.matriz.shape
        # Inicializando a fila com prioridade
        self.priority_queue = queue.PriorityQueue()

        # Inicializando o dicionário de g_scores com o primeiro ponto que é o de partida e dando 0 para o g_score dele
        self.g_score = {self.start: 0}

        # Inicializando o dicionário que guarda o caminho que foi percorrido
        self.came_from = {}

        # Inicializando f_score, g_score, h_score
        f_score, g_score, h_score = self.f_score(self.start, self.goal)

        # Adicionando o primeiro tile a fila de prioridade
        # Que neste caso é o starting point
        self.priority_queue.put(
            (f_score, g_score, self.start)
        )  # (f_score, g_score, posicao)

    def f_score(self, start_coords, end_coords):
        g_score = self.g_score.get(start_coords, float("inf"))
        h_score = self.heuristica(start_coords, end_coords)
        f_score = h_score + g_score
        return f_score, g_score, h_score

    def cruz_vizinhos(self, point):
        matriz = self.matriz
        row, col = point
        vizinhos = []
        direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # cima, baixo, esquerda, direita

        for dr, dc in direcoes:
            nr, nc = row + dr, col + dc
            if (
                0 <= nr < self.matriz_linha and 0 <= nc < self.matriz_col
            ):  # dentro dos limites da matriz
                if matriz[nr][nc][3] == 0:  # não é parede
                    vizinhos.append((nr, nc))

        return vizinhos

    # def step_generator(self):
    #     while not self.priority_queue.empty():
    #         new_point = self.priority_queue.get()
    #         cruz_vizinhos = self.cruz_vizinhos(new_point[2])
    #         yield new_point[2], cruz_vizinhos
    #         if new_point[2] == self.goal:
    #             self.came_from[self.goal] = new_point[2]
    #             return

    def reconstruir_caminho(self, atual):
        caminho = [atual]
        while atual in self.came_from:
            atual = self.came_from[atual]
            caminho.append(atual)
        caminho.reverse()
        return caminho

    def step_generator(self):
        while not self.priority_queue.empty():
            f_atual, g_atual, atual = self.priority_queue.get()

            # Visitação atual e vizinhos (para animação da busca)
            vizinhos = self.cruz_vizinhos(atual)
            yield atual, vizinhos

            if atual == self.goal:
                caminho_final = self.reconstruir_caminho(atual)
                for passo in caminho_final:
                    yield passo, []  # Aqui o senhor pode diferenciar visualmente
                return

            for vizinho in vizinhos:
                g_tentativo = g_atual + 1
                if g_tentativo < self.g_score.get(vizinho, float("inf")):
                    self.came_from[vizinho] = atual
                    self.g_score[vizinho] = g_tentativo
                    f_vizinho, _, _ = self.f_score(vizinho, self.goal)
                    self.priority_queue.put((f_vizinho, g_tentativo, vizinho))

# [X] 1. Inicialize a estrutura de dados:
#   [X] - Crie uma fila de prioridade chamada "open_set"
#   [X] - E insira o nó inicial com f=0
#   [X] - Crie um dicionário "g_score" para armazenar o custo do início até cada célula
#   [X] - Crie um dicionário "came_from" para guardar o caminho percorrido

# [x] 2. Enquanto houver elementos no open_set:
#    [x] a) Pegue o nó com menor f (menor prioridade) da fila
#    [ ] b) Se esse nó for o destino, pare e reconstrua o caminho usando "came_from"

# 3. Para cada vizinho (cima, baixo, esquerda, direita) do nó atual:
#    a) Ignore se estiver fora da matriz ou for parede
#    b) Calcule o custo g do caminho até o vizinho (g atual + 1)
#    c) Se esse caminho for melhor que o anterior registrado:
#       - Atualize g_score do vizinho
#       - Calcule f = g + h (heurística: distância de Manhattan até o objetivo)
#       - Registre que veio desse nó (came_from)
#       - Adicione o vizinho na fila com prioridade f

# 4. Após visitar todos os vizinhos, use yield:
#    - Retorne o nó atual e seus vizinhos válidos para pintar na tela

# 5. Quando encontrar o objetivo:
#    - Reconstrua o caminho final de trás pra frente usando came_from
#    - Para cada célula do caminho, pinte com uma cor especial (ex: roxo)
#    - Use yield a cada célula para animar o caminho final passo a passo

# 6. Ao terminar, pare o gerador com StopIteration
