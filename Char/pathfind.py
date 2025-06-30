# Algoritmo A* — Pseudocódigo explicativo (com yield passo a passo)
import queue # Fila com prioridade

import numpy as np # My beloved numpy


class Pathfind: # A*
    def heuristica(self, a, b):
        '''Calcula a distancia Manhatan entre dois pontos'''
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

        self.matriz_linha, self.matriz_col = self.matriz.shape[:2] # Pegando o formato da linha e coluna da matriz
        self.matriz_shape = self.matriz.shape # Pegando o formato geral da matriz

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
        '''
        Funcao que calcula o f_score
        Inputs:
            <start_coords>: [x, y] -- coordenadas do ponto inicial;
            <end_coords>: [x, y] -- coordenadas do ponto final;
        '''
        g_score = self.g_score.get(start_coords, float("inf")) # PEga o G_score do ponto de inicio. Se não tiver o G_score então associa valor infinito
        h_score = self.heuristica(start_coords, end_coords) # Calcula o h_score
        f_score = h_score + g_score # Calcula o f_score
        return f_score, g_score, h_score # retorna o F_score e por precaucao retorna o G_score e o H_score

    def cruz_vizinhos(self, point):
        '''
        Avalia em cruz os vizinhos do point. Não avalia todos os 8 vizinhos pois nao e permitido andar em diagonal
        Inputs:
            <point>: [x, y]: Ponto na qual os vizinhos serao avaliados
        '''
        matriz = self.matriz # Recebe a matriz localmente
        row, col = point # Pega as coordenadas x y do point
        vizinhos = [] # Uma lista vazia para armazenar os vizinhos
        direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1)] # Direcoes na qual iremos avaliar

        for dr, dc in direcoes: # para dr dc em direcoes. tenta expandir para cada direcao
            nr, nc = row + dr, col + dc # Calcula a nova linha e coluna baseando-se na direcao
            if 0 <= nr < self.matriz_linha and 0 <= nc < self.matriz_col:
                # bloqueia paredes e só permite o goal mesmo se marcado ocupada
                if (nr, nc) == self.goal:
                    vizinhos.append((nr, nc))
                else:
                    # só adiciona se NÃO for parede E não estiver ocupado
                    if matriz[nr, nc, 2] == 0 and matriz[nr, nc, 3] == 0:
                        vizinhos.append((nr, nc))
        return vizinhos # retorna a lista de vizinhos possiveis

    def reconstruir_caminho(self, atual):
        '''
        Reconstroi o caminho apartir do atual. Funcao chamada apos o A* ter terminado de rodar e encontrado o melhor caminho.
        '''
        caminho = [atual] # Caminho é uma lista ja com o destino final
        while atual in self.came_from: # Para cada elemento=(x,y) dentro de came_from
            atual = self.came_from[atual] # atual recebe o novo atual
            caminho.append(atual) # caminho adiciona esse atual a lista
        caminho.reverse() # inverte o caminho para ele comecar no inicio e ir ate o objetivo
        return caminho # retorna o caminho

    def step_generator(self):
        '''
        Gerador. Que mostra o caminho passo a passo como está sendo calculado e após terminar mostra o caminho todo a ser percorrido do ponto inicial ate o final.
        Esse é o coracao dessa classe. O coracao do A*.
        '''
        while not self.priority_queue.empty():
            f_atual, g_atual, atual = self.priority_queue.get()

            # Visitação atual e vizinhos (para animação da busca)
            vizinhos = self.cruz_vizinhos(atual) # Pega os vizinhos
            yield atual, vizinhos # Retorna o atual e seus vizinhos

            if atual == self.goal: # Se o atual e o objetivo
                caminho_final = self.reconstruir_caminho(atual) # entao coleta o caminho final
                for passo in caminho_final: # para cada passo no caminho final retorna o passo e um vazio para os vizinhos
                    yield passo, []  # Aqui o senhor pode diferenciar visualmente
                return # retorna nada, ou seja, termina o A*

            for vizinho in vizinhos: # Para vizinho em vizinhos. Ou seja vai desempacotando vizinhos
                g_tentativo = g_atual + 1 # Calcula o G_score do possivel proximo atual
                if g_tentativo < self.g_score.get(vizinho, float("inf")): # Compra se o G_score da tentativa e menor que o g_score atual
                    self.came_from[vizinho] = atual # Adiciona ao dicionario do camiho de qual ponto o vizinhho veio
                    self.g_score[vizinho] = g_tentativo  # guarda o g_score da tentativa
                    f_vizinho, _, _ = self.f_score(vizinho, self.goal) # recebe o f_score do vizinhho
                    self.priority_queue.put((f_vizinho, g_tentativo, vizinho)) # adiciona o vizinho a lista com prioridade


def pathfind(start, goal, matriz) -> list:
    '''
    Funcao de encapsulamento para o A*. Para scripts que precisem usar ele como um metodo de retorno e nao um gerador.
    '''
    a_star = Pathfind(start=start, goal=goal, matriz=matriz)

    for passo, _ in a_star.step_generator():
        if passo == goal:
            return a_star.reconstruir_caminho(goal)
    return []
