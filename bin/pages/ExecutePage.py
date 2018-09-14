# -*- coding: utf-8 -*-#


from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from bin.ui.style import Style


class ExecutePage(QWidget):
    def __init__(self, parent=None):
        super(ExecutePage, self).__init__(parent)
        # 设置参数Widget，方便在uncheck时隐藏，layout无隐藏方法
        self.parameter = ExecuteParameter()
        self.parameter.setHidden(True)  # 默认为隐藏状态
        self.initUI()

    def initUI(self):
        # 设置背景为白色
        self.setBackgroundColor(QColor("#FFFFFF"))
        # 设置各个控件的样式
        self.setStyleSheet(Style.COMMON_STYLE)
        # 设置layout
        self.ExecuteLayout()
        # 还需读取配置文件，设置各参数状态

    def setBackgroundColor(self, color):
        pal = QPalette()
        pal.setColor(QPalette.Background, color)
        self.setPalette(pal)
        self.setAutoFillBackground(True)

    def ExecuteLayout(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        self.execute_checkbox = QCheckBox("自定义设置")
        self.execute_checkbox.stateChanged.connect(self.checkboxSignal)
        main_layout.addWidget(self.execute_checkbox)
        main_layout.addWidget(self.parameter)
        main_layout.addStretch()

    def checkboxSignal(self):
        if self.execute_checkbox.isChecked():
            self.parameter.setHidden(False)
        else:
            self.parameter.setHidden(True)


class ExecuteParameter(QWidget):
    def __init__(self, parent=None):
        super(ExecuteParameter, self).__init__(parent)
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

        execute_time_layout = QHBoxLayout()
        execute_time_label = QLabel('执行次数')
        execute_time_spinbox = QSpinBox()
        execute_time_spinbox.setRange(1, 100)
        execute_time_spinbox.setValue(1)
        execute_time_layout.addWidget(execute_time_label)
        execute_time_layout.addWidget(execute_time_spinbox)
        execute_time_layout.addStretch()

        priority_layout = QVBoxLayout()
        priority_label = QLabel('优先级设置（只执行选中的优先级）')
        priority_button_layout = QHBoxLayout()
        priority_button_layout.addWidget(QLabel('  '))

        self.setStyleSheet(Style.SELECT_BUTTON)
        self.button0 = QPushButton('0')
        self.button1 = QPushButton('1')
        self.button2 = QPushButton('2')
        self.button3 = QPushButton('3')
        self.button0.clicked.connect(self.button0_click)
        priority_button_layout.addWidget(self.button0)
        priority_button_layout.addWidget(self.button1)
        priority_button_layout.addWidget(self.button2)
        priority_button_layout.addWidget(self.button3)
        priority_button_layout.addStretch(1)
        priority_layout.addWidget(priority_label)
        priority_layout.addLayout(priority_button_layout)

        main_layout.addLayout(execute_time_layout)
        main_layout.addLayout(priority_layout)

    def button0_click(self):
        self.button0
