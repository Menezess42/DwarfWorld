from PySide6.QtGui import QPixmap, QImage, QPainter, QColor, QPen
from PySide6.QtCore import QPointF

def calculate_foot_offset(pixmap: QPixmap, foot_height: int = 3, alpha_threshold: int = 0) -> QPointF:
    """
    Analisa os últimos `foot_height` pixels verticais da imagem para encontrar 
    o centro médio dos pés (pixels visíveis) e retorna um offset apropriado.
    Também salva uma imagem de depuração com o ponto médio desenhado.

    :param pixmap: QPixmap do frame atual do personagem
    :param foot_height: Altura (em px) da faixa inferior a ser analisada
    :param alpha_threshold: Valor mínimo de alpha para considerar o pixel visível (0–255)
    :return: QPointF(offset_x, offset_y) para usar com setOffset()
    """
    image: QImage = pixmap.toImage()
    width = image.width()
    height = image.height()

    start_y = max(0, height - foot_height)
    end_y = height

    x_coords = []

    for y in range(start_y, end_y):
        for x in range(width):
            alpha = image.pixelColor(x, y).alpha()
            if alpha > alpha_threshold:
                x_coords.append(x)

    if not x_coords:
        mean_x = width / 2
    else:
        mean_x = sum(x_coords) / len(x_coords)

    offset_x = int(mean_x)
    offset_y = int(end_y)
    
    print(offset_x)
    print(offset_y)

    # ========== GERAR VISUALIZAÇÃO ==========
    debug_image = QImage(image)  # Cópia da imagem original
    painter = QPainter(debug_image)

    pen = QPen(QColor(255, 0, 0, 255))  # Vermelho para destacar o ponto
    pen.setWidth(3)
    painter.setPen(pen)

    # Marca o ponto médio encontrado pelo scanner
    painter.drawPoint(int(mean_x), end_y - 1)

    painter.end()
    debug_image.save("debug_anchor_point.png")

    return QPointF(offset_x, offset_y)


# from PySide6.QtGui import QPixmap, QImage
# from PySide6.QtCore import QPointF
#
# def calculate_foot_offset(pixmap: QPixmap, foot_height: int = 3, alpha_threshold: int = 0) -> QPointF:
#     """
#     Analisa os últimos `foot_height` pixels verticais da imagem para encontrar 
#     o centro médio dos pés (pixels visíveis) e retorna um offset apropriado.
#
#     :param pixmap: QPixmap do frame atual do personagem
#     :param foot_height: Altura (em px) da faixa inferior a ser analisada
#     :param alpha_threshold: Valor mínimo de alpha para considerar o pixel visível (0–255)
#     :return: QPointF(offset_x, offset_y) para usar com setOffset()
#     """
#     image: QImage = pixmap.toImage()
#     width = image.width()
#     height = image.height()
#
#     start_y = max(0, height - foot_height)
#     end_y = height
#
#     x_coords = []
#
#     for y in range(start_y, end_y):
#         for x in range(width):
#             alpha = image.pixelColor(x, y).alpha()
#             if alpha > alpha_threshold:
#                 x_coords.append(x)
#
#     if not x_coords:
#         # Nenhum pixel visível encontrado — usa centro horizontal como fallback
#         mean_x = width / 2
#     else:
#         mean_x = sum(x_coords) / len(x_coords)
#
#     offset_x = -mean_x
#     offset_y = -end_y  # Move a base da faixa para o ponto de ancoragem
#
#     return QPointF(offset_x, offset_y)
