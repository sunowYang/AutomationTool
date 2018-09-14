# -*- coding: utf-8 -*-#


import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from bin.ui.style import Style


# 设置主界面左侧
class LeftSide(QWidget):
    def __init__(self, parent=None):
        super(LeftSide, self).__init__(parent)
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tasks())
        main_layout.addWidget(self.new_task())
        main_layout.addWidget(self.link())
        main_layout.addWidget(self.antivirus())
        main_layout.addWidget(self.config_file())
        main_layout.addWidget(self.md5())
        main_layout.addWidget(self.schedule())
        main_layout.addWidget(self.digital())
        main_layout.addStretch()
        self.setLayout(main_layout)
        self.setBackgroundColor(QColor("#FFFFFF"))
        self.setAutoFillBackground(True)

    def setBackgroundColor(self, color):
        pal = QPalette()
        pal.setColor(QPalette.Background, color)
        self.setPalette(pal)
        self.setAutoFillBackground(True)

    @staticmethod
    def tasks():
        task_button = QPushButton("工具列表")
        task_button.setStyleSheet(Style.TASKS_BUTTON)
        return task_button

    @staticmethod
    def new_task():
        new_task_button = QPushButton("自动化")
        new_task_button.setStyleSheet(Style.LEFT_SIDE_BUTTON)
        return new_task_button

    @staticmethod
    def link():
        link_button = QPushButton("检查链接")
        link_button.setStyleSheet(Style.LEFT_SIDE_BUTTON)
        return link_button

    @staticmethod
    def antivirus():
        antivirus_button = QPushButton("安装杀毒")
        antivirus_button.setStyleSheet(Style.LEFT_SIDE_BUTTON)
        return antivirus_button

    @staticmethod
    def config_file():
        config_file_button = QPushButton("检查配置文件")
        config_file_button.setStyleSheet(Style.LEFT_SIDE_BUTTON)
        return config_file_button

    @staticmethod
    def md5():
        md5_button = QPushButton("MD5对比")
        md5_button.setStyleSheet(Style.LEFT_SIDE_BUTTON)
        return md5_button

    @staticmethod
    def schedule():
        schedule_button = QPushButton("计划检查")
        schedule_button.setStyleSheet(Style.LEFT_SIDE_BUTTON)
        return schedule_button

    @staticmethod
    def digital():
        digital_button = QPushButton("检查数字签名")
        digital_button.setStyleSheet(Style.LEFT_SIDE_BUTTON)
        return digital_button

    @staticmethod
    def reset_time():
        reset_button = QPushButton("重置时间")
        reset_button.setStyleSheet(Style.LEFT_SIDE_BUTTON)
        return reset_button


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ft = QFont()
    ft.setPointSize(11)
    ft.setFamily("宋体")
    app.setFont(ft)
    box = LeftSide()
    box.show()
    sys.exit(app.exec_())

