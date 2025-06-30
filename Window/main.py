# Window/main.py
from PySide6 import QtWidgets, QtGui, QtCore

class TransparentWindow(QtWidgets.QWidget):
    '''
    Cria a janela transparente e sem bordas.
    '''
    def __init__(self, scene):
        super().__init__()
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setStyleSheet("Background-color: transparent;")
        self.setWindowTitle("DwarfWorldWindow")

        self.scene = scene

        view = QtWidgets.QGraphicsView(self.scene)
        view.setInteractive(False)
        view.setMinimumSize(690, 400)
        view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(view)
        layout.setContentsMargins(0, 0, 0, 0)
