# -*- coding: utf-8 -*-#


import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from style import Style


class SvnPage(QWidget):
    def __init__(self, parent=None):
        super(SvnPage, self).__init__(parent)
        self.initUI()

    def initUI(self):
        # 设置背景为白色
        self.setBackgroundColor(QColor("#FFFFFF"))
        # 设置各个控件的样式
        self.setStyleSheet(Style.COMMON_STYLE)
        # 设置layout
        self.svnLayout()
        self.image = QImage(r'../res/1.png')


    def setBackgroundColor(self, color):
        pal = QPalette()
        pal.setColor(QPalette.Background, color)
        self.setPalette(pal)
        self.setAutoFillBackground(True)

    def svnLayout(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        update_checkbox = QCheckBox("更新脚本")
        update_checkbox.stateChanged.connect(self.checkboxSignal)

        svn_address_label = QLabel("    svn地址")
        svn_address_lineedit = QLineEdit()
        svn_address_layout = QHBoxLayout()
        svn_address_layout.addWidget(svn_address_label, 1)
        svn_address_layout.addWidget(svn_address_lineedit, 4)

        local_address_label = QLabel("    目标地址")
        local_address_lineedit = QLineEdit()
        local_address_layout = QHBoxLayout()
        local_address_layout.addWidget(local_address_label, 1)
        local_address_layout.addWidget(local_address_lineedit, 4)

        svn_label = QLabel("    svn用户名: ")
        svn_edit = QLineEdit()
        svn_layout = QHBoxLayout()
        svn_layout.addWidget(svn_label)
        svn_layout.addWidget(svn_edit)

        psd_label = QLabel("密码:")
        psd_edit = QLineEdit()
        psd_layout = QHBoxLayout()
        psd_layout.addWidget(psd_label)
        psd_layout.addWidget(psd_edit)

        user_psd_layout = QHBoxLayout()
        user_psd_layout.addLayout(svn_layout)
        user_psd_layout.addStretch()
        user_psd_layout.addLayout(psd_layout)

        option_layout = QVBoxLayout()
        self
        option_layout.addLayout(svn_address_layout)
        option_layout.addSpacing(6)
        option_layout.addLayout(local_address_layout)
        option_layout.addSpacing(6)
        option_layout.addLayout(user_psd_layout)

        main_layout.addWidget(update_checkbox)
        main_layout.addSpacing(15)
        main_layout.addLayout(option_layout)
        main_layout.addStretch()

    def checkboxSignal(self):




