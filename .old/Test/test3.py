from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtGui import QPixmap, QPainter
from PySide6.QtCore import QTimer, QRect, QPoint
import sys
import random

class SpriteWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Sprite com 4 direções empilhadas verticalmente
        self.sprite_sheet = QPixmap("./Assets/Tests/char.png")
        self.frame_width = 39
        self.frame_height = 58

        # Direção atual: 0 (direita), 1 (cima), 2 (esquerda), 3 (baixo)
        self.direction_index = 3  # Começa para baixo

        # Posição do boneco
        self.x = 0
        self.y = 0
        self.target_x = 0
        self.target_y = 0

        # Timer para movimentação
        self.move_timer = QTimer()
        self.move_timer.timeout.connect(self.update_position)
        self.move_timer.start(300)

        self.setFixedSize(640, 480)
        self.choose_new_target()

    def choose_new_target(self):
        max_x = (self.width() - self.frame_width) // self.frame_width
        max_y = (self.height() - self.frame_height) // self.frame_height
        self.target_x = random.randint(0, max_x) * self.frame_width
        self.target_y = random.randint(0, max_y) * self.frame_height

    def update_position(self):
        dx = self.target_x - self.x
        dy = self.target_y - self.y

        if dx == 0 and dy == 0:
            self.choose_new_target()
            return

        # Movimento em eixo único, sem diagonal
        if dx != 0:
            self.x += self.frame_width if dx > 0 else -self.frame_width
            self.direction_index = 0 if dx > 0 else 2  # Direita ou Esquerda
        elif dy != 0:
            self.y += self.frame_height if dy > 0 else -self.frame_height
            self.direction_index = 3 if dy > 0 else 1  # Baixo ou Cima

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        source_rect = QRect(0,
                            self.direction_index * self.frame_height,
                            self.frame_width,
                            self.frame_height)
        painter.drawPixmap(QPoint(self.x, self.y), self.sprite_sheet, source_rect)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = SpriteWidget()
    w.show()
    sys.exit(app.exec())