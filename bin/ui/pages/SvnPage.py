# -*- coding: utf-8 -*-#


import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from bin.ui.style import Style


class SvnParameter(QWidget):
    def __init__(self, parent=None):
        super(SvnParameter, self).__init__(parent)
        # 定义控件
        self.svn_address_lineedit = QLineEdit()
        self.local_address_lineedit = QLineEdit()
        self.psd_edit = QLineEdit()
        self.user_edit = QLineEdit()
        self.initUI()

    def initUI(self):
        # 设置背景为白色
        self.setBackgroundColor(QColor("#FFFFFF"))
        # 设置各个控件的样式
        self.setStyleSheet(Style.COMMON_STYLE)
        # 设置layout
        self.parameterLayout()

    def setBackgroundColor(self, color):
        pal = QPalette()
        pal.setColor(QPalette.Background, color)
        self.setPalette(pal)
        self.setAutoFillBackground(True)

    def parameterLayout(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        svn_address_label = QLabel("    svn地址")
        svn_address_layout = QHBoxLayout()
        svn_address_layout.addWidget(svn_address_label, 1)
        svn_address_layout.addWidget(self.svn_address_lineedit, 4)

        local_address_label = QLabel("    目标地址")
        local_address_layout = QHBoxLayout()
        local_address_layout.addWidget(local_address_label, 1)
        local_address_layout.addWidget(self.local_address_lineedit, 4)

        svn_label = QLabel("    svn用户名: ")
        svn_layout = QHBoxLayout()
        svn_layout.addWidget(svn_label)
        svn_layout.addWidget(self.user_edit)

        psd_label = QLabel("密码:")
        psd_layout = QHBoxLayout()
        psd_layout.addWidget(psd_label)
        psd_layout.addWidget(self.psd_edit)

        user_psd_layout = QHBoxLayout()
        user_psd_layout.addLayout(svn_layout)
        user_psd_layout.addStretch()
        user_psd_layout.addLayout(psd_layout)

        main_layout.addLayout(svn_address_layout)
        main_layout.addSpacing(6)
        main_layout.addLayout(local_address_layout)
        main_layout.addSpacing(6)
        main_layout.addLayout(user_psd_layout)


class SvnPage(QWidget):
    def __init__(self, parent=None):
        super(SvnPage, self).__init__(parent)
        # 设置参数Widget，方便在uncheck时隐藏，layout无隐藏方法
        self.parameter = SvnParameter()
        self.parameter.setHidden(True)  # 默认为隐藏状态
        self.initUI()

    def initUI(self):
        # 设置背景为白色
        self.setBackgroundColor(QColor("#FFFFFF"))
        # 设置各个控件的样式
        self.setStyleSheet(Style.COMMON_STYLE)
        # 设置layout
        self.svnLayout()
        # 还需读取配置文件，设置各参数状态

    def setBackgroundColor(self, color):
        pal = QPalette()
        pal.setColor(QPalette.Background, color)
        self.setPalette(pal)
        self.setAutoFillBackground(True)

    def svnLayout(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        self.update_checkbox = QCheckBox("更新脚本")
        self.update_checkbox.stateChanged.connect(self.checkboxSignal)
        main_layout.addWidget(self.update_checkbox)
        main_layout.addWidget(self.parameter)
        main_layout.addStretch()

    def checkboxSignal(self):
        if self.update_checkbox.isChecked():
            self.parameter.setHidden(False)
        else:
            self.parameter.setHidden(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    box = SvnPage()
    box.show()
    sys.exit(app.exec_())

