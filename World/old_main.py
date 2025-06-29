from perlin import gerar_mapa_perlin
import json
import numpy as np


# Exemplo mínimo
# noise = gerar_mapa_perlin(50, 50, seed=42)
# print(noise)
# Exemplo com tudo habilitado
noise = gerar_mapa_perlin(
    width=20,
    height=20,
    scale=15,
    octaves=4,
    persistence=0.55,
    lacunarity=2.3,
    seed=4,
    classificar=False,
    mostrar_plot=True,
)

print(noise)
noise = noise.tolist()
json_string = json.dumps(noise)
print(json_string)

# Save the JSON string to a file
with open("noise.json", "w") as json_file:
    json.dump(noise, json_file)
