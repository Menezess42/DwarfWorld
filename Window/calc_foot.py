from PySide6.QtCore import QPointF
from PySide6.QtGui import QImage, QPixmap

from PySide6.QtCore import QPointF
from PySide6.QtGui import QImage, QPixmap


def calculate_foot_offset(pixmap: QPixmap, foot_height: int = 3, alpha_threshold: int = 10) -> QPointF:
    """
    Calcula o offset para alinhar o centro visível da base dos pés
    ao ponto central do tile (gridMiddle).
    """
    image: QImage = pixmap.toImage()
    width = image.width()
    height = image.height()

    start_y = max(0, height - foot_height)
    end_y = height

    x_coords = []

    for y in range(start_y, end_y):
        for x in range(width):
            if image.pixelColor(x, y).alpha() > alpha_threshold:
                x_coords.append(x)

    if not x_coords:
        mean_x = width / 2
    else:
        mean_x = sum(x_coords) / len(x_coords)

    offset_x = width / 2 - mean_x
    offset_y = -end_y  # alinha a base inferior com o ponto do tile

    return QPointF(offset_x, offset_y)

# from PySide6.QtGui import QPixmap, QImage
# from PySide6.QtCore import QPointF

# def calculate_foot_offset(pixmap: QPixmap, foot_height: int = 10, alpha_threshold: int = 10) -> QPointF:
#     """
#     Analisa os últimos `foot_height` pixels verticais da imagem para encontrar 
#     o centro médio dos pés (pixels visíveis) e retorna um offset apropriado.

#     :param pixmap: QPixmap do frame atual do personagem
#     :param foot_height: Altura (em px) da faixa inferior a ser analisada
#     :param alpha_threshold: Valor mínimo de alpha para considerar o pixel visível (0–255)
#     :return: QPointF(offset_x, offset_y) para usar com setOffset()
#     """
#     image: QImage = pixmap.toImage()
#     width = image.width()
#     height = image.height()

#     start_y = max(0, height - foot_height)
#     end_y = height

#     x_coords = []

#     for y in range(start_y, end_y):
#         for x in range(width):
#             alpha = image.pixelColor(x, y).alpha()
#             if alpha > alpha_threshold:
#                 x_coords.append(x)

#     if not x_coords:
#         # Nenhum pixel visível encontrado — usa centro horizontal como fallback
#         mean_x = width / 2
#     else:
#         mean_x = sum(x_coords) / len(x_coords)

#     offset_x = -mean_x
#     offset_y = -end_y  # Move a base da faixa para o ponto de ancoragem

#     return QPointF(offset_x, offset_y)
