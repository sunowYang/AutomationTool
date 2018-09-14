# -*- coding: utf-8 -*-#


import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from bin.ui.style import Style


# 设置主界面左侧
class RightSide(QWidget):
    def __init__(self, parent=None):
        super(RightSide, self).__init__(parent)
        self.initUI()

    def initUI(self):
        # 设置各个控件的样式
        self.setStyleSheet(Style.OTHER_BUTTON)
        # 设置主layout
        main_layout = QVBoxLayout()
        # 增加一个上侧的layout,用于安放执行按钮等控件
        up_layout = QHBoxLayout()
        task_label = QLabel('任务')
        task_label.setFixedHeight(50)
        up_layout.addWidget(task_label)
        up_layout.addStretch()
        up_layout.addWidget(self.proceed())
        up_layout.addWidget(QPushButton("编辑"))
        up_layout.addWidget(QPushButton("删除"))
        # 增加一个table
        self.task_table = QTableWidget()
        self.init_table()
        main_layout.addLayout(up_layout)
        main_layout.addWidget(self.task_table)
        self.setLayout(main_layout)
        self.setBackgroundColor(QColor("#FFFFFF"))
        self.setAutoFillBackground(True)

    def setBackgroundColor(self, color):
        pal = QPalette()
        pal.setColor(QPalette.Background, color)
        self.setPalette(pal)
        self.setAutoFillBackground(True)

    @staticmethod
    def proceed():
        proceed_button = QPushButton('执行')
        proceed_button.setStyleSheet(Style.PROCEED_BUTTON)
        proceed_button.setFixedHeight(31)
        return proceed_button

    def init_table(self):
        # 先从数据库中读取任务数据
        self.task_table.setFrameShape(QFrame.NoFrame)
        self.task_table.setShowGrid(False)
        self.task_table.setColumnCount(4)
        self.task_table.verticalHeader().setVisible(False)
        self.task_table.setHorizontalHeaderLabels(['任务名', '任务类型', '任务状态', '任务地址'])
        self.task_table.setColumnWidth(0, 200)
        self.task_table.setColumnWidth(1, 200)
        self.task_table.setColumnWidth(2, 200)
        self.task_table.setColumnWidth(3, 228)
        self.task_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.task_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.task_table.setStyleSheet(Style.TABLE)

        a = QTableWidgetItem()
        a.setText('File test')
        b = QTableWidgetItem('File')
        c = QTableWidgetItem('to do')
        d = QTableWidgetItem('11')
        self.task_table.setRowCount(1)
        self.task_table.setItem(0, 0, a)
        self.task_table.setItem(0, 1, b)
        self.task_table.setItem(0, 2, c)
        self.task_table.setItem(0, 3, d)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ft = QFont()
    ft.setPointSize(14)
    ft.setFamily("宋体")
    app.setFont(ft)
    box = RightSide()
    box.show()
    sys.exit(app.exec_())

