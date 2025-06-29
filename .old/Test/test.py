import math
import random
import os
import time

# Configurações
TAMANHO = 8
ESCALA = 0.2
SEED = 42

# Símbolos e cores ANSI
BLOCOS = [
    ('[a]', '\033[44m'),  # Água (azul)
    ('[v]', '\033[46m'),  # Vitória-régia (ciano)
    ('[d]', '\033[106m'), # Beira d’água (azul claro)
    ('[r]', '\033[103m'), # Areia (amarelo)
    ('[b]', '\033[101m'), # Barro (vermelho claro)
    ('[x]', '\033[42m'),  # Grama (verde)
    ('[c]', '\033[102m'), # Grama alta (verde claro)
    ('[q]', '\033[105m'), # Grama roxa (roxo)
]

# Função simples de Perlin 2D fake (só pra visualização, sem lib externa)
def interpolar(a, b, t):
    return a + t * (b - a)

def gradiente(x, y):
    random.seed((x * 49632) ^ (y * 325176) ^ SEED)
    return random.uniform(-1, 1), random.uniform(-1, 1)

def perlin(x, y):
    x0 = int(math.floor(x))
    x1 = x0 + 1
    y0 = int(math.floor(y))
    y1 = y0 + 1

    sx = x - x0
    sy = y - y0

    g00 = gradiente(x0, y0)
    g10 = gradiente(x1, y0)
    g01 = gradiente(x0, y1)
    g11 = gradiente(x1, y1)

    def dot_grid_gradient(ix, iy, x, y, g):
        dx = x - ix
        dy = y - iy
        return dx * g[0] + dy * g[1]

    n00 = dot_grid_gradient(x0, y0, x, y, g00)
    n10 = dot_grid_gradient(x1, y0, x, y, g10)
    n01 = dot_grid_gradient(x0, y1, x, y, g01)
    n11 = dot_grid_gradient(x1, y1, x, y, g11)

    ix0 = interpolar(n00, n10, sx)
    ix1 = interpolar(n01, n11, sx)
    value = interpolar(ix0, ix1, sy)

    return (value + 1) / 2  # normalizar pra 0-1

# Mapeamento de valor para bloco
def mapear_bloco(valor):
    if valor < 0.10: return 0
    elif valor < 0.20: return 1
    elif valor < 0.30: return 2
    elif valor < 0.45: return 3
    elif valor < 0.60: return 4
    elif valor < 0.75: return 5
    elif valor < 0.90: return 6
    else: return 7

# Função para limpar terminal (Windows/Linux)
def limpar_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

# Geração do mapa
mapa = [['' for _ in range(TAMANHO)] for _ in range(TAMANHO)]

for y in range(TAMANHO):
    for x in range(TAMANHO):
        valor = perlin(x * ESCALA, y * ESCALA)
        indice_bloco = mapear_bloco(valor)
        simbolo, cor = BLOCOS[indice_bloco]
        mapa[y][x] = (simbolo, cor)

        # Exibir enquanto gera
        limpar_terminal()
        print("Gerando mapa...\n")
        for yy in range(TAMANHO):
            linha = ""
            for xx in range(TAMANHO):
                if mapa[yy][xx] == '':
                    linha += "   "
                else:
                    s, c = mapa[yy][xx]
                    linha += f"{c} {s} \033[0m"
            print(linha)
        time.sleep(0.1)

# Exibir resultado final
print("\nMapa final:")
for y in range(TAMANHO):
    linha = ""
    for x in range(TAMANHO):
        s, c = mapa[y][x]
        linha += f"{c} {s} \033[0m"
    print(linha)
print(f"Legenda:\n{BLOCOS[0][:]}")
