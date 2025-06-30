# Algoritmo A* — Pseudocódigo explicativo (com yield passo a passo)
import queue

import numpy as np


class Pathfind:
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
        direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dr, dc in direcoes:
            nr, nc = row + dr, col + dc
            if 0 <= nr < self.matriz_linha and 0 <= nc < self.matriz_col:
                # bloqueia paredes e só permite o goal mesmo se marcado ocupada
                if (nr, nc) == self.goal:
                    vizinhos.append((nr, nc))
                else:
                    # só adiciona se NÃO for parede E não estiver ocupado
                    if matriz[nr, nc, 2] == 0 and matriz[nr, nc, 3] == 0:
                        vizinhos.append((nr, nc))
        return vizinhos

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


def pathfind(start, goal, matriz) -> list:
    a_star = Pathfind(start=start, goal=goal, matriz=matriz)

    for passo, _ in a_star.step_generator():
        if passo == goal:
            return a_star.reconstruir_caminho(goal)
    return []
