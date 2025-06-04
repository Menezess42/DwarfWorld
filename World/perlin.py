import numpy as np
import matplotlib.pyplot as plt
from noise import pnoise2

def gerar_mapa_perlin(
    width: int = 100,
    height: int = 100,
    *,
    scale: float = 10.0,
    octaves: int = 1,
    persistence: float = 0.5,
    lacunarity: float = 2.0,
    seed: int | None = None,
    classificar: bool = False,
    mostrar_plot: bool = False,
):
    """
    Gera e (opcionalmente) classifica um mapa de Perlin 2-D.

    Parâmetros
    ----------
    width, height : int
        Largura e altura do mapa em número de células.
    scale : float
        Quanto maior, “mais esticado” fica o ruído (menos detalhes).
    octaves : int
        Camadas de detalhe. Valores maiores deixam o terreno mais complexo.
    persistence : float
        Influência de cada oitava subsequente (normalmente 0.3–0.6).
    lacunarity : float
        Frequência relativa entre oitavas (tipicamente 2.0).
    seed : int | None
        Semente aleatória para tornar o mapa reproduzível.
    classificar : bool
        Se True, devolve também uma matriz de strings (“água”, “areia”, “grama”).
    mostrar_plot : bool
        Se True, desenha o mapa com `matplotlib`.
    
    Retorna
    -------
    noise_map : np.ndarray
        Matriz `height × width` com valores float entre 0 e 1.
    classified_map : np.ndarray (opcional)
        Mesmas dimensões contendo strings, devolvido se `classificar=True`.
    """
    # Cria a grade vazia
    noise_map = np.empty((height, width), dtype=np.float32)

    # Normaliza coordenadas e gera ruído
    for y in range(height):
        for x in range(width):
            val = pnoise2(
                x / scale,
                y / scale,
                octaves=octaves,
                persistence=persistence,
                lacunarity=lacunarity,
                repeatx=1024,
                repeaty=1024,
                base=seed or 0,
            )
            noise_map[y, x] = (val + 1) / 2  # –1..1  →  0..1

    # Opcional: plot
    if mostrar_plot:
        plt.imshow(noise_map, cmap="terrain")
        plt.colorbar()
        plt.title("Mapa de Perlin (0=água · 0.3=areia · 0.6+=grama)")
        plt.show()

    # Opcional: classificação simples
    if classificar:
        def _classifica(v: float) -> str:
            if v < 0.3:
                return "água"
            elif v < 0.45:
                return "areia"
            else:
                return "grama"
        class_map = np.vectorize(_classifica)(noise_map)
        return noise_map, class_map

    return noise_map
