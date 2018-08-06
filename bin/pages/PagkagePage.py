# -*- coding: utf-8 -*-#


import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from bin.style import Style


class PackagePage(QWidget):
    def __init__(self, parent=None):
        super(PackagePage, self).__init__(parent)
        # 设置参数Widget，方便在uncheck时隐藏，layout无隐藏方法
        self.parameter = PackageParameter()
        self.parameter.setHidden(True)  # 默认为隐藏状态
        self.initUI()

    def initUI(self):
        # 设置背景为白色
        self.setBackgroundColor(QColor("#FFFFFF"))
        # 设置各个控件的样式
        self.setStyleSheet(Style.COMMON_STYLE)
        # 设置layout
        self.PackageLayout()
        # 还需读取配置文件，设置各参数状态

    def setBackgroundColor(self, color):
        pal = QPalette()
        pal.setColor(QPalette.Background, color)
        self.setPalette(pal)
        self.setAutoFillBackground(True)

    def PackageLayout(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        self.update_checkbox = QCheckBox("更新安装包")
        self.update_checkbox.stateChanged.connect(self.checkboxSignal)
        main_layout.addWidget(self.update_checkbox)
        main_layout.addWidget(self.parameter)
        main_layout.addStretch()

    def checkboxSignal(self):
        if self.update_checkbox.isChecked():
            self.parameter.setHidden(False)
        else:
            self.parameter.setHidden(True)


class PackageParameter(QWidget):
    def __init__(self, parent=None):
        super(PackageParameter, self).__init__(parent)
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

        address_label = QLabel("    安装包地址")
        self.address_lineedit = QLineEdit()
        address_button = QPushButton('浏览')
        address_button.clicked.connect(self.browse)
        package_address_layout = QHBoxLayout()
        package_address_layout.addWidget(address_label, 1)
        package_address_layout.addWidget(self.address_lineedit, 4)
        package_address_layout.addWidget(address_button)

        language_label = QLabel("    安装语言")
        self.language_combobox = QComboBox()
        self.language_combobox.setFixedSize(120, 30)
        # self.language_combobox.set
        self.language_lineedit = QLineEdit()
        # self.language_lineedit.setMaxLength(5)
        language_button = QPushButton('添加语言')
        language_button.clicked.connect(self.add)
        language_layout = QHBoxLayout()
        language_layout.addWidget(language_label)
        language_layout.addSpacing(4)
        language_layout.addWidget(self.language_combobox)
        language_layout.addStretch()
        language_layout.addWidget(self.language_lineedit)
        language_layout.addWidget(language_button)

        main_layout.addLayout(package_address_layout)
        main_layout.addSpacing(6)
        main_layout.addLayout(language_layout)

    def browse(self):
        file_name, file_type = QFileDialog.getOpenFileName(self, '选择安装包', './', '*.py')
        self.address_lineedit.setText(file_name)

    def add(self):
        # 添加语言并且将添加的语言设置为最新的语言
        language = self.language_lineedit.text()
        self.language_combobox.addItem(language)
        self.language_combobox.setCurrentIndex(self.language_combobox.count() - 1)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    box = PackagePage()
    box.show()
    sys.exit(app.exec_())

