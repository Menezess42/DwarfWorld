import math
import random
import os
import time

# Configurações
TAMANHO = 15
ESCALA = 0.4
SEED = 42

# Símbolos e cores ANSI
BLOCOS = [
    ('[a]', '\033[44m'),   # Água
    ('[v]', '\033[46m'),   # Vitória-régia
    ('[d]', '\033[106m'),  # Beira d’água
    ('[r]', '\033[103m'),  # Areia
    ('[b]', '\033[101m'),  # Barro
    ('[x]', '\033[42m'),   # Grama
    ('[c]', '\033[102m'),  # Grama alta
    ('[q]', '\033[105m'),  # Grama roxa
]

# Perlin simplificado (sem lib externa)
def interpolar(a, b, t):
    return a + t * (b - a)

def gradiente(x, y):
    random.seed((x * 49632) ^ (y * 325176) ^ SEED)
    return random.uniform(-1, 1), random.uniform(-1, 1)

def perlin(x, y):
    x0 = int(math.floor(x))
    y0 = int(math.floor(y))
    x1 = x0 + 1
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

    return (value + 1) / 2  # normalizado

# Mapeia valor [0,1] para tipo de bloco
def mapear_bloco(valor):
    #  '''
    # ('[a]', '\033[44m'),   # Água
    # ('[v]', '\033[46m'),   # Vitória-régia
    # ('[d]', '\033[106m'),  # Beira d’água
    # ('[r]', '\033[103m'),  # Areia
    # ('[b]', '\033[101m'),  # Barro
    # ('[x]', '\033[42m'),   # Grama
    # ('[c]', '\033[102m'),  # Grama alta
    # ('[q]', '\033[105m'),  # Grama roxa
    #  '''
    if valor < 0.10: return 0
    elif valor < 0.15: return 1
    elif valor < 0.30: return 2
    elif valor < 0.40: return 3
    elif valor < 0.48: return 4
    elif valor < 0.70: return 5
    elif valor < 0.85: return 6
    else: return 7

# Limpa terminal
def limpar_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

# Geração em espiral anti-horária a partir do centro
def espiral_antihorario(tamanho):
    x = y = tamanho // 2
    dx, dy = 0, -1
    passos = 1
    while True:
        for _ in range(2):
            for _ in range(passos):
                if 0 <= x < tamanho and 0 <= y < tamanho:
                    yield (x, y)
                x += dx
                y += dy
            dx, dy = -dy, dx  # girar anti-horário
        passos += 1
        if passos > tamanho:
            break

# Mapa vazio
mapa = [['' for _ in range(TAMANHO)] for _ in range(TAMANHO)]

# Geração do mapa
for x, y in espiral_antihorario(TAMANHO):
    valor = perlin(x * ESCALA, y * ESCALA)
    indice_bloco = mapear_bloco(valor)
    simbolo, cor = BLOCOS[indice_bloco]
    mapa[y][x] = (simbolo, cor)

    # Printando progresso
    limpar_terminal()
    print("Gerando mapa em espiral (anti-horário)...\n")
    for yy in range(TAMANHO):
        linha = ""
        for xx in range(TAMANHO):
            if mapa[yy][xx] == '':
                linha += "   "
            else:
                s, c = mapa[yy][xx]
                linha += f"{c} {s} \033[0m"
        print(linha)
    time.sleep(0.08)

# Exibe o resultado final
print("\nMapa final:")
for y in range(TAMANHO):
    linha = ""
    for x in range(TAMANHO):
        s, c = mapa[y][x]
        linha += f"{c} {s} \033[0m"
    print(linha)
print("\nLegenda:")
for simbolo, cor in BLOCOS:
    nome = {
        '[a]': "água",
        '[v]': "vitória-régia",
        '[d]': "beira d’água",
        '[r]': "areia",
        '[b]': "barro",
        '[x]': "grama",
        '[c]': "grama alta",
        '[q]': "grama roxa"
    }[simbolo]
    print(f"{cor} {simbolo} \033[0m = {nome}")
