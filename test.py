
import sys
import math
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QPainter, QColor, QPolygonF
from PySide6.QtCore import Qt, QPointF

import pymunk
from noise import pnoise2  # Perlin noise

# --- Configurações principais ---
GRID_WIDTH = 10
GRID_HEIGHT = 10
HEX_SIZE = 30  # Raio do hexágono
SCALE = 0.1  # Escala do Perlin noise
HEIGHT_MULTIPLIER = 20  # Elevação máxima

# --- Função para obter vértices do hexágono ---
def hex_corner(center, size, i):
    angle_deg = 60 * i + 30
    angle_rad = math.radians(angle_deg)
    return QPointF(
        center.x() + size * math.cos(angle_rad),
        center.y() + size * math.sin(angle_rad)
    )

# --- Função para converter coordenadas hex para tela isométrica ---
def hex_to_pixel(q, r):
    x = HEX_SIZE * (3/2 * q)
    y = HEX_SIZE * (math.sqrt(3) * (r + q / 2))
    return QPointF(x, y)

# --- Janela principal ---
class HexTerrain(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Terreno com Perlin + pymunk")
        self.resize(800, 600)

        self.space = pymunk.Space()
        self.space.gravity = (0, 900)

        self.terrain = []
        self.generate_terrain()

    def generate_terrain(self):
        for q in range(-GRID_WIDTH // 2, GRID_WIDTH // 2):
            for r in range(-GRID_HEIGHT // 2, GRID_HEIGHT // 2):
                pos = hex_to_pixel(q, r)
                noise = pnoise2(q * SCALE, r * SCALE, octaves=3)
                height = (noise + 1) / 2 * HEIGHT_MULTIPLIER
                pos.setY(pos.y() - height)

                # Cria um hexágono visual e corpo estático no pymunk
                corners = [hex_corner(pos, HEX_SIZE, i) for i in range(6)]
                poly = [(p.x(), p.y()) for p in corners]

                body = pymunk.Body(body_type=pymunk.Body.STATIC)
                shape = pymunk.Poly(body, poly)
                self.space.add(body, shape)

                self.terrain.append((pos, corners, height))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)

        for pos, corners, height in self.terrain:
            color = QColor.fromHsv(100 + int(height * 5) % 255, 200, 150)
            painter.setBrush(color)
            painter.setPen(Qt.black)
            painter.drawPolygon(QPolygonF(corners))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HexTerrain()
    window.show()
    sys.exit(app.exec())

# import pymunk
# import math
# from noise import pnoise2
#
# # === Configurações do mapa ===
# MAP_WIDTH = 10   # Quantos hexágonos na horizontal
# MAP_HEIGHT = 10  # Quantos hexágonos na vertical
# HEX_RADIUS = 30  # Raio do hexágono
# PERLIN_SCALE = 0.1
# AMPLITUDE = 50   # Altura máxima do terreno com base no Perlin
#
# # === Funções de utilidade ===
#
# def perlin_height(x, y, seed=0):
#     """Gera altura baseada em Perlin"""
#     return pnoise2(x * PERLIN_SCALE, y * PERLIN_SCALE, octaves=2, base=seed) * AMPLITUDE
#
# def hex_to_pixel(q, r):
#     """Converte coordenadas hex (cúbicas axial) para coordenadas x/y isométricas"""
#     x = HEX_RADIUS * 3/2 * q
#     y = HEX_RADIUS * math.sqrt(3) * (r + q / 2)
#     return (x, y)
#
# def create_hexagon(center_x, center_y, height):
#     """Cria um polígono de 6 lados com pymunk, deslocado para altura"""
#     angle_offset = math.pi / 6  # Para isometria "deitada"
#     points = []
#     for i in range(6):
#         angle = 2 * math.pi / 6 * i + angle_offset
#         x = center_x + HEX_RADIUS * math.cos(angle)
#         y = center_y + HEX_RADIUS * math.sin(angle) - height
#         points.append((x, y))
#     return points
#
# # === Inicialização do mundo físico ===
#
# space = pymunk.Space()
# space.gravity = (0, -981)
#
# # === Geração do terreno ===
#
# for q in range(MAP_WIDTH):
#     for r in range(MAP_HEIGHT):
#         cx, cy = hex_to_pixel(q, r)
#         h = perlin_height(q, r)
#         vertices = create_hexagon(cx, cy, h)
#
#         # pymunk precisa de um corpo estático e uma forma poligonal
#         body = pymunk.Body(body_type=pymunk.Body.STATIC)
#         shape = pymunk.Poly(body, vertices)
#         shape.friction = 0.5
#
#         space.add(body, shape)
#
#         # Debug textual: posição e altura do hexágono
#         print(f"Hex ({q},{r}) → pos=({cx:.1f},{cy:.1f}) altura={h:.1f}")

