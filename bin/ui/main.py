#! coding=utf8
import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from option import OptionWnd
from style import Style


class MainWindow(QMainWindow):
    """
    界面初始化：
        创建1个main layout,包括左右两个子layout
    """
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        # 初始化界面
        self.initUI()

    def initUI(self):
        # 创建主界面layout
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        spliter = QSplitter(Qt.Horizontal)
        spliter.addWidget(LeftSide())
        spliter.addWidget(RightSide())
        # 设置spliter的宽度以及比例
        spliter.setHandleWidth(5)
        spliter.setStretchFactor(1, 3)
        main_layout.addWidget(spliter)
        # 设置主界面相关
        main_frame = QWidget()
        main_frame.setLayout(main_layout)
        self.setStyleSheet(Style.COMMON_STYLE)
        self.setCentralWidget(main_frame)
        self.setWindowTitle('TB Automation Tool')
        self.setWindowIcon(QIcon(r'..\..\res\icon.png'))
        self.setAutoFillBackground(True)
        self.resize(1084, 646)
        self.setBackgroundColor(QColor('#FFFFFF'))
        self.setAutoFillBackground(True)

    def setBackgroundColor(self, color):
        pal = QPalette()
        pal.setColor(QPalette.Background, color)
        self.setPalette(pal)
        self.setAutoFillBackground(True)


class LeftSide(QWidget):
    def __init__(self, parent=None):
        super(LeftSide, self).__init__(parent)
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(1)
        main_layout.addWidget(self.tasks())
        main_layout.addWidget(self.new_task())
        main_layout.addWidget(self.link())
        main_layout.addWidget(self.antivirus())
        main_layout.addWidget(self.config_file())
        main_layout.addWidget(self.md5())
        main_layout.addWidget(self.schedule())
        main_layout.addWidget(self.digital())
        main_layout.addStretch()
        self.setMinimumSize(200, 400)
        self.setLayout(main_layout)
        self.setStyleSheet(Style.LEFT_SIDE_BUTTON)
        self.setBackgroundColor(QColor("#FFFFFF"))
        self.setAutoFillBackground(True)

    def setBackgroundColor(self, color):
        pal = QPalette()
        pal.setColor(QPalette.Background, color)
        self.setPalette(pal)
        self.setAutoFillBackground(True)

    def option_wnd(self):
        option = OptionWnd()
        if option.exec_():
            print '1111'

    def tasks(self):
        task_button = QPushButton("工具列表")
        task_button.setGeometry(0, 0, 80, 30)
        task_button.setStyleSheet(Style.TASKS_BUTTON)
        return task_button

    def new_task(self):
        new_task_button = QPushButton("自动化")
        new_task_button.clicked.connect(self.option_wnd)
        return new_task_button

    @staticmethod
    def link():
        link_button = QPushButton("检查链接")
        return link_button

    @staticmethod
    def antivirus():
        antivirus_button = QPushButton("安装杀毒")
        return antivirus_button

    @staticmethod
    def config_file():
        config_file_button = QPushButton("检查配置文件")
        return config_file_button

    @staticmethod
    def md5():
        md5_button = QPushButton("MD5对比")
        return md5_button

    @staticmethod
    def schedule():
        schedule_button = QPushButton("计划检查")
        return schedule_button

    @staticmethod
    def digital():
        digital_button = QPushButton("检查数字签名")
        return digital_button

    @staticmethod
    def reset_time():
        reset_button = QPushButton("重置时间")
        return reset_button


class RightSide(QWidget):
    def __init__(self, parent=None):
        super(RightSide, self).__init__(parent)
        # 定义控件
        self.task_table = QTableWidget()
        self.initUI()

    def initUI(self):
        # 设置各个控件的样式
        self.setStyleSheet(Style.OTHER_BUTTON)
        # 设置主layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 0, 20, 0)
        # 增加一个上侧的layout,用于安放执行按钮等控件
        up_layout = QHBoxLayout()
        task_label = QLabel('任务')
        task_label.setFixedHeight(60)
        up_layout.addWidget(task_label)
        up_layout.addStretch()
        up_layout.addLayout(self.button_box())
        # 增加一个table
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

    def button_box(self):
        btn_layout = QHBoxLayout()
        proceed_btn = QPushButton('执行')
        proceed_btn.setStyleSheet(Style.PROCEED_BUTTON)
        proceed_btn.setFixedHeight(31)
        edit_btn = QPushButton('编辑')
        delete_btn = QPushButton('删除')
        btn_layout.addWidget(proceed_btn)
        btn_layout.addWidget(edit_btn)
        btn_layout.addWidget(delete_btn)
        return btn_layout

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
    ft.setPointSize(11)
    ft.setFamily("宋体")
    app.setFont(ft)
    main_window = LeftSide()
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
