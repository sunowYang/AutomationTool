# -*- coding: utf-8 -*-#

import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class NavigationWidget(QWidget):
    currentItemChanged = pyqtSignal([int, str])

    def __init__(self, parent=None):
        super(NavigationWidget, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.backgroundColor = '#FFFFFF'
        self.selectedColor = '#ECF6FE'
        self.rowHeight = 40
        self.currentIndex = 0  # 当前选择的项索引
        self.listItems = []
        self.cursorIndex = -1  # 当前光标所在位置的项索引

        self.setMouseTracking(True)
        self.setMinimumWidth(180)

    def addItem(self, item):
        self.listItems.append(item)
        self.update()

    def setItems(self, items):
        self.listItems = items
        self.update()

    def setBackgroundColor(self, color):
        self.backgroundColor = color
        self.update()

    def setSelectColor(self, color):
        self.selectedColor = color
        self.update()

    def setRowHeight(self, height):
        self.rowHeight = height
        self.update()

    def setCurrentIndex(self, idx):
        self.currentIndex = idx
        self.currentItemChanged.emit(idx, self.listItems[idx])
        self.update()

    def paintEvent(self, evt):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)

        # 设置画笔
        painter.setFont(QFont("Roman times", 11))  # 字体设置
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(self.backgroundColor))
        painter.drawRect(self.rect())

        # 绘所有选项
        for i in range(len(self.listItems)):
            itemPath = QPainterPath()
            itemPath.addRect(QRectF(0, i * self.rowHeight, self.width() - 1, self.rowHeight - 1))
            if i == self.currentIndex:
                painter.setPen(QPen(QColor('#48A6F5'), 6))  # 选中就重新设置画笔，线条加粗
                painter.fillPath(itemPath, QColor(self.selectedColor))
            elif i == self.cursorIndex:
                painter.setPen(QColor('#666666'))
                painter.fillPath(itemPath, QColor(self.selectedColor))
            else:
                painter.setPen(QColor('#666666'))
                painter.fillPath(itemPath, QColor(self.backgroundColor))
            painter.drawImage(QRect(10, i * self.rowHeight + 18, 15, 15), QImage(r'..\res\icon_execute.png'))
            painter.drawText(QRect(30, i * self.rowHeight, self.width(), self.rowHeight),
                             Qt.AlignVCenter | Qt.AlignLeft, self.listItems[i])
            painter.drawLine(QLine(self.width(), i * self.rowHeight, self.width(), (i+1) * self.rowHeight))

    def mouseMoveEvent(self, evt):
        idx = evt.y() / self.rowHeight
        if idx >= len(self.listItems):
            idx = -1
        if idx < len(self.listItems) and idx != self.cursorIndex:
            self.update()
            self.cursorIndex = idx

    def mousePressEvent(self, evt):
        idx = evt.y() / self.rowHeight
        if idx < len(self.listItems):
            self.currentIndex = idx
            self.currentItemChanged.emit(idx, self.listItems[idx])
            self.update()

    def leaveEvent(self, QEvent):
        self.cursorIndex = -1
        self.update()


class OptionWnd(QDialog):
    def __init__(self):
        super(OptionWnd, self).__init__()
        self.initUI()

    def initUI(self):
        self.resize(800, 400)
        self.setWindowTitle(u'任务设置')

        mainWidget = QWidget()
        # self.setCentralWidget(mainWidget)

        navigationWidget = NavigationWidget()
        navigationWidget.setRowHeight(50)
        navigationWidget.setItems([u'更新安装包', u'更新脚本', u'执行模块', u'邮件通知', u'执行计划'])

        self.tipsLabel = QLabel(u"请选择：")

        mainLayout = QHBoxLayout(mainWidget)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setSpacing(10)
        mainLayout.addWidget(navigationWidget, 1)
        mainLayout.addWidget(self.tipsLabel, 3, Qt.AlignCenter)

        navigationWidget.currentItemChanged[int, str].connect(self.slotCurrentItemChanged)
        navigationWidget.setCurrentIndex(2)
        self.setLayout(mainLayout)
        # self.show()

    def slotCurrentItemChanged(self, index, content):
        self.tipsLabel.setText(u"Current index and content：{} ---- {}".format(index, content))


def main():
    app = QApplication(sys.argv)
    mainWnd = OptionWnd()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
