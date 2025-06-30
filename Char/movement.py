# Char/movement.py
from PySide6.QtCore import QTimer
from PySide6 import QtWidgets

TILE_H = 16  # só precisamos da altura para recalcular ground em cada tile

def mover_em_linha_reta(path, sprite_item: QtWidgets.QGraphicsPixmapItem,
                        matriz, delay=100, passos_por_tile=10, on_finish=None):
    if not path:
        return

    index = 0
    subpasso = 0
    timer = QTimer()

    def mover():
        nonlocal index, subpasso

        # fim do trajeto
        if index >= len(path) - 1:
            timer.stop()
            if on_finish:
                on_finish()
            return

        x1, y1 = path[index]
        x2, y2 = path[index + 1]
        px1, py1 = matriz[x1, y1, 0], matriz[x1, y1, 1]
        px2, py2 = matriz[x2, y2, 0], matriz[x2, y2, 1]

        t = subpasso / passos_por_tile
        nx = px1 + (px2 - px1) * t
        ny = py1 + (py2 - py1) * t

        # ajusta bottom‑center igual ao posicionamento inicial
        pixmap = sprite_item.pixmap()
        w, h = pixmap.width(), pixmap.height()
        sprite_item.setPos(nx - w/2, ny + TILE_H/2 - h)
        sprite_item.setZValue(y2 + 0.5)

        subpasso += 1
        if subpasso > passos_por_tile:
            subpasso = 0
            index += 1

    timer.timeout.connect(mover)
    timer.start(delay)
    sprite_item._timer = timer
