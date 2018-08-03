# -*- coding: utf-8 -*-#

import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from style import Style
from pages import *


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
        self.rowWidth = 200

        self.setMouseTracking(True)
        # self.setMinimumWidth(180)

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
        painter.setPen(QPen(QColor('#666666'), 0.5))
        painter.setBrush(QColor(self.backgroundColor))

        painter.drawRect(self.rect())
        # painter.drawRect(0, 0, 200, 340)
        # painter.drawRect(200, 0, 800, 340)
        # painter.drawRect(0, 340, 800, 400)

        # 绘所有选项, 根据不同状态，设置不同画笔
        for i in range(len(self.listItems)):
            image = QImage(r'..\res\backup_option\Email.png')
            itemPath = QPainterPath()
            itemPath.addRect(QRectF(0, i * self.rowHeight+1, self.width()-1, self.rowHeight-1))
            if i == self.currentIndex:
                painter.setPen(QPen(QColor('#48A6F5'), 4))  # 选中就重新设置画笔，线条加粗
                painter.fillPath(itemPath, QColor(self.selectedColor))
                painter.drawLine(QLine(self.width(), i * self.rowHeight, self.width(), (i + 1) * self.rowHeight))
                image = QImage(r'..\res\backup_option\Email_active.png')
            elif i == self.cursorIndex:
                painter.setPen(QColor('#666666'))
                painter.fillPath(itemPath, QColor(self.selectedColor))
            else:
                painter.setPen(QColor('#666666'))
                painter.fillPath(itemPath, QColor(self.backgroundColor))
            painter.drawImage(QRect(10, i * self.rowHeight + 18, 15, 15), image)
            painter.drawText(QRect(30, i * self.rowHeight, self.width(), self.rowHeight),
                             Qt.AlignVCenter | Qt.AlignLeft, self.listItems[i])

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


class SvnPageTest(QWidget):
    def __init__(self, text, parent=None):
        super(SvnPageTest, self).__init__(parent)
        self.style = Style.COMMON_STYLE
        self.backgroundColor = ''
        self.pages = text
        self.initUI()

    def initUI(self):
        self.backgroundColor = '#FFFFFF'
        box = QCheckBox(self.pages)
        box.setGeometry(0, 0, 0, 0)
        combox = QComboBox()
        combox.addItems(['1', '2', '3'])
        layout = QHBoxLayout(self)
        layout.addWidget(box)
        layout.addWidget(combox)
        pal = QPalette()
        pal.setColor(QPalette.Background, QColor(self.backgroundColor))
        self.setPalette(pal)
        self.setAutoFillBackground(True)

        self.setStyleSheet(self.style)
        ft = QFont()
        ft.setPointSize(18)
        ft.setFamily("宋体")
        # self.show()

    def svnLayout(self):
        layout = QHBoxLayout()


    def setPages(self, pages):
        self.pages = pages

    def addPage(self, page):
        self.pages.append(page)

    def setBackgroundColor(self, color):
        self.backgroundColor = color

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)

        # 设置画笔
        painter.setFont(QFont("Timers", 11))  # 字体设置
        painter.setPen(QPen(QColor('#666666')))
        painter.setBrush(QColor(self.backgroundColor))

        # painter.drawRect(self.rect())
        painter.drawLine(0, 0, self.width(), 0)
        painter.drawText(QRect(0, 100, self.width(), 120), Qt.AlignVCenter | Qt.AlignLeft, self.pages)


class OptionWnd(QDialog):
    def __init__(self):
        super(OptionWnd, self).__init__()
        self.initUI()

    def initUI(self):
        self.setFixedSize(800, 400)
        self.setWindowTitle(u'任务设置')

        mainWidget = QWidget()
        navigationWidget = NavigationWidget()
        navigationWidget.setRowHeight(50)
        navigationWidget.setItems([u'更新安装包', u'更新脚本', u'执行模块', u'邮件通知', u'执行计划'])

        self.page1 = SvnPage()
        self.page2 = SvnPageTest('程序更新设置')

        self.tipsLabel = QLabel(u"请选择：")

        self.option = AddOptions(self)

        mainLayout = QHBoxLayout(mainWidget)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setSpacing(0)
        mainLayout.addWidget(navigationWidget, 1)
        # mainLayout.addWidget(self.tipsLabel, 3, Qt.AlignHCenter)
        mainLayout.addWidget(self.page1, 3)
        mainLayout.addWidget(self.page2, 3)

        navigationWidget.currentItemChanged[int, str].connect(self.slotCurrentItemChanged)
        navigationWidget.setCurrentIndex(0)
        self.setLayout(mainLayout)
        # self.show()

    def slotCurrentItemChanged(self, index, content):
        self.tipsLabel.setText(u"Current index and content：{} ---- {}".format(index, content))
        if index == 1:
            self.page1.setHidden(False)
            self.page2.setHidden(True)
        else:
            self.page1.setHidden(True)
            self.page2.setHidden(False)


class AddOptions(QWidget):
    def __init__(self, parent=None):
        super(AddOptions, self).__init__(parent)
        self.initUi()

    def initUi(self):
        self.setLayout(self.update_package_layout())
        # self.show()

    def get_layout(self, index):
        if index == 1:
            return self.update_package_layout()
        return 1

    def update_package_layout(self):
        package_path_layout = QHBoxLayout()
        package_label = QLabel('       package path: ')
        package_line_edit = QLineEdit()
        package_path_layout.addWidget(package_label)
        package_path_layout.addWidget(package_line_edit)

        package_version_layout = QHBoxLayout()
        package_version_label = QLabel('       package version: ')
        package_version_list = ['1', '2', '3', '4']
        package_version_combobox = QComboBox()
        package_version_combobox.addItems(package_version_list)
        package_version_layout.addWidget(package_version_label)
        package_version_layout.addWidget(package_version_combobox)
        # add_label = LabelClick()
        # add_label.setText('Add...')
        # package_version_layout.addWidget(add_label)
        # package_version_layout.addWidget(QLabel('Add...'))

        package_layout = QVBoxLayout()
        package_checkout = QCheckBox('Use newest package')
        package_layout.addWidget(package_checkout)
        package_layout.addLayout(package_path_layout)
        package_layout.addLayout(package_version_layout)
        package_layout.addStretch(1)
        # package_layout.setEnabled(False)
        return package_layout


def main():
    app = QApplication(sys.argv)
    ft = QFont()
    ft.setPointSize(11)
    ft.setFamily("宋体")
    app.setFont(ft)
    mainWnd = OptionWnd()
    mainWnd.show()
    # wnd = AddOptions()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
