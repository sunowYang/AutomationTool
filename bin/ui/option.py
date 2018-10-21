# -*- coding: utf-8 -*-#

import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from bin.ui.pages import SvnPage, PackagePage, ExecutePage
from bin.ui.style import Style


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
            image = QImage('../../res/backup_option/Email.png')
            itemPath = QPainterPath()
            itemPath.addRect(QRectF(0, i * self.rowHeight+1, self.width()-1, self.rowHeight-1))
            if i == self.currentIndex:
                painter.setPen(QPen(QColor('#4BAEB3'), 4))  # 选中就重新设置画笔，线条加粗
                painter.fillPath(itemPath, QColor(self.selectedColor))
                painter.drawLine(QLine(self.width(), i * self.rowHeight, self.width(), (i + 1) * self.rowHeight))
                image = QImage('../../res/backup_option/Email_active.png')
            elif i == self.cursorIndex:
                painter.setPen(QColor('#4BAEB3'))
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


class OptionWnd(QDialog):
    def __init__(self):
        super(OptionWnd, self).__init__()
        self.svn = SvnPage.SvnPage()
        self.svn_parameter = SvnPage.SvnParameter()
        self.package = PackagePage.PackagePage()
        self.execute = ExecutePage.ExecutePage()
        self.initUI()

    def initUI(self):
        self.setFixedSize(800, 400)
        self.setWindowTitle(u'任务设置')

        mainWidget = QWidget()
        navigationWidget = NavigationWidget()
        navigationWidget.setRowHeight(50)
        navigationWidget.setItems([u'更新脚本', u'更新安装包', u'执行模块', u'邮件通知', u'执行计划'])

        self.page1 = SvnPage.SvnPage()
        self.page2 = PackagePage.PackagePage()
        self.page3 = ExecutePage.ExecutePage()
        self.tipsLabel = QLabel(u"请选择：")
        self.option = AddOptions(self)

        mainLayout = QVBoxLayout(mainWidget)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setSpacing(0)

        # 上面一部分layout，主要是左侧栏和右侧栏
        up_layout = QHBoxLayout()
        up_layout.addWidget(navigationWidget, 1)
        up_layout.addWidget(self.page1, 3)
        up_layout.addWidget(self.page2, 3)
        up_layout.addWidget(self.page3, 3)
        # 下面栏是保存取消按钮
        self.button = Save(self)
        self.button.button_save.clicked.connect(self.save)
        self.button.button_cancel.clicked.connect(self.close)
        # 整体布局
        navigationWidget.currentItemChanged[int, str].connect(self.slotCurrentItemChanged)
        navigationWidget.setCurrentIndex(2)
        mainLayout.addLayout(up_layout, 8)
        mainLayout.addWidget(self.button, 1)

        self.setLayout(mainLayout)

    def slotCurrentItemChanged(self, index, content):
        self.tipsLabel.setText(u"Current index and content：{} ---- {}".format(index, content))
        if index == 0:
            self.page1.setHidden(False)
            self.page2.setHidden(True)
            self.page3.setHidden(True)
        elif index == 1:
            self.page1.setHidden(True)
            self.page2.setHidden(False)
            self.page3.setHidden(True)
        else:
            self.page1.setHidden(True)
            self.page2.setHidden(True)
            self.page3.setHidden(False)

    def save(self):
        data = {}
        # 读取SVN页面参数
        if self.svn.update_checkbox.isChecked():
            data['svn'] = '1'
            data['address'] = self.svn_parameter.svn_address_lineedit.text()
            print len(data['address'])
            if data['address'] == '':
                self.button.error_message = 'SVN 地址不能为空'
            data['localaddress'] = self.svn_parameter.local_address_lineedit.text()
            data['username'] = self.svn_parameter.user_edit.text()
            data['password'] = self.svn_parameter.psd_edit.text()
            print data['address'], data['localaddress']
            print 1111
        # 读取安装包页面参数
        if self.package.update_checkbox.isChecked():
            data['package'] = '1'
            data['address'] = self.package.address_lineedit.text()
            data['language'] = self.package.language_combobox.currentText()



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


class Save(QWidget):
    def __init__(self, parent=None):
        super(Save, self).__init__(parent)
        # 设置参数Widget，方便在uncheck时隐藏，layout无隐藏方法
        self.initUI()

    def initUI(self):
        # 设置背景为白色
        self.setBackgroundColor(QColor("#FFFFFF"))
        # 设置各个控件的样式
        self.setStyleSheet(Style.COMMON_STYLE)
        # 设置layout
        self.mainLayout()
        # 还需读取配置文件，设置各参数状态

    def setBackgroundColor(self, color):
        pal = QPalette()
        pal.setColor(QPalette.Background, color)
        self.setPalette(pal)
        self.setAutoFillBackground(True)

    def mainLayout(self):
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        # 添加save cancel按钮框
        self.button_save = QPushButton('保存')
        self.button_save.setStyleSheet(Style.PROCEED_BUTTON)
        self.button_cancel = QPushButton('取消')
        # 添加错误说明
        # self.error_message = QLabel()
        # self.error_message.setStyleSheet(Style.ERROR_lABEL)
        main_layout.addStretch(1)
        # main_layout.addWidget(self.error_message)
        main_layout.addWidget(self.button_save)
        main_layout.addWidget(self.button_cancel)


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
