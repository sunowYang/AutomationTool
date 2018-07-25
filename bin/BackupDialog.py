#! coding=utf8

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from LabelClick import LabelClick


def read_version():
    return list('12345')


class OptionHeader(QWidget):
    currentItemChanged = pyqtSignal([int, str])

    def __init__(self, parent=None):
        super(OptionHeader, self).__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.backgroundColor = '#E4E4E4'
        self.selectedColor = '#2CA7F8'
        self.rowHeight = 40
        self.currentIndex = 0  # 当前选择的项索引
        self.listItems = []
        self.cursorIndex = -1  # 当前光标所在位置的项索引
        self.setMouseTracking(True)
        self.setMinimumWidth(120)

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

        #画背景色
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(self.backgroundColor))
        painter.drawRect(self.rect())

        #画子项
        for i in range(len(self.listItems)):
            itemPath = QPainterPath()
            itemPath.addRect(QRectF(0, i*self.rowHeight, self.width()-1, self.rowHeight-1))

            if i == self.currentIndex:
                painter.setPen(QColor('#FFFFFF'))
                painter.fillPath(itemPath, QColor(self.selectedColor))
            elif i == self.cursorIndex:
                painter.setPen(QColor('#FFFFFF'))
                painter.fillPath(itemPath, QColor(self.selectedColor))
            else:
                painter.setPen(QColor('#202020'))
                painter.fillPath(itemPath, QColor(self.backgroundColor))

            painter.drawText(QRect(0, i*self.rowHeight, self.width(), self.rowHeight), Qt.AlignVCenter|Qt.AlignHCenter, self.listItems[i])

    def mouseMoveEvent(self, evt):
        idx = evt.y() / self.rowHeight
        if idx >= len(self.listItems):
            idx = -1
        if idx < len(self.listItems) and idx != self.cursorIndex:
            self.update()
            self.cursorIndex = idx

    def mousePressEvent(self, evt):
        idx = evt.y()/self.rowHeight
        if  idx< len(self.listItems):
            self.currentIndex = idx
            self.currentItemChanged.emit(idx, self.listItems[idx])
            self.update()

    def leaveEvent(self, QEvent):
        self.cursorIndex = -1
        self.update()





class OptionsSettingWnd(QWidget):
    def __init__(self, parent=None):
        super(OptionsSettingWnd, self).__init__(parent)
        self.ui_init()
        # self.setWindowTitle("Settings")
        # self.resize(600, 400)
        # self.setLayout(self.add_layout())
        # signal
        # self.button_box.button(QDialogButtonBox.Cancel).clicked.connect(self.close)

    def ui_init(self):
        self.setWindowTitle("Backup")
        self.resize(600, 300)
        self.setLayout(self.add_layout())

    def add_layout(self):
        tab = QTabWidget()
        # tab.setTabPosition(QTabWidget.West)
        # tab.
        # bar = QTabBar()
        # bar.setShape(QTabBar.RoundedEast)
        # bar.setTabButton(0, QTabBar.LeftSide, QPushButton("test"))
        # tab.setTabBar(bar)
        tab.addTab(self.add_script_layout(), QIcon(r"..\res\icon_execute.png"), "Download")
        tab.addTab(QLabel("123"), "mail")
        main_layout = QVBoxLayout()
        main_layout.addWidget(tab)



        # main_layout.addLayout(self.add_script_layout())
        # main_layout.addLayout(self.add_package_layout())
        # main_layout.addLayout(self.add_mail_layout())
        # main_layout.addStretch(1)
        # self.button_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)

        # main_layout.addWidget(self.button_box)
        return main_layout

    def add_split_layout(self):
        split_layout = QVBoxLayout()

    def add_script_layout(self):
        svn_path_layout = QHBoxLayout()
        svn_label = QLabel('       svn path:   ')
        svn_line_edit = QLineEdit()
        svn_path_layout.addWidget(svn_label)
        svn_path_layout.addWidget(svn_line_edit)

        local_path_layout = QHBoxLayout()
        local_path_label = QLabel('       local path: ')
        local_path_line_edit = QLineEdit()
        local_path_layout.addWidget(local_path_label)
        local_path_layout.addWidget(local_path_line_edit)

        script_layout = QVBoxLayout()
        script_checkout = QCheckBox('Use newest script')
        script_layout.addWidget(script_checkout)
        script_layout.addLayout(svn_path_layout)
        script_layout.addLayout(local_path_layout)

        return script_layout

    def add_package_layout(self):
        package_path_layout = QHBoxLayout()
        package_label = QLabel('       package path: ')
        package_line_edit = QLineEdit()
        package_path_layout.addWidget(package_label)
        package_path_layout.addWidget(package_line_edit)

        package_version_layout = QHBoxLayout()
        package_version_label = QLabel('       package version: ')
        package_version_list = read_version()
        package_version_combobox = QComboBox()
        package_version_combobox.addItems(package_version_list)
        package_version_layout.addWidget(package_version_label)
        package_version_layout.addWidget(package_version_combobox)
        add_label = LabelClick()
        add_label.setText('Add...')
        package_version_layout.addWidget(add_label)
        # package_version_layout.addWidget(QLabel('Add...'))

        package_layout = QVBoxLayout()
        package_checkout = QCheckBox('Use newest package')
        package_layout.addWidget(package_checkout)
        package_layout.addLayout(package_path_layout)
        package_layout.addLayout(package_version_layout)
        package_layout.addStretch(1)

        return package_layout

    def add_mail_layout(self):
        mail_layout = QVBoxLayout()
        mail_layout.addWidget(QCheckBox('Send mail'))
        return mail_layout


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = OptionHeader()
    dialog.show()
    app.exec_()

