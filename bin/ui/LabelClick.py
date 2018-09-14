#! coding=utf8

from PyQt5.QtWidgets import QLabel


class LabelClick(QLabel):
    def __init__(self, parent=None):
        super(LabelClick, self).__init__(parent)

    def mousePressEvent(self, QMouseEvent):
        print('gogogogogog')

    def mouseReleaseEvent(self, QMouseEvent):
        pass

