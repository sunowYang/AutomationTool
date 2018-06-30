#! coding=utf8
import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from BackupDialog import BackDialog


class MainWindow(QMainWindow):
    """
    界面初始化：
        创建1个main layout,包括左右两个子layout
    """
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        # self.backup = BackDialog(self)

        # 创建主界面gridlayout
        main_layout = QHBoxLayout()
        # 创建左边以及右边的v_layout
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

        # 创建左边NEW TASK控件
        self.new_task_button = QPushButton('NEW TASK')
        self.new_task_button.isFlat()
        self.new_task_button.setMinimumSize(160, 50)
        # 创建左侧快速任务选择控件
        self.quick_label = QLabel(' ')
        self.quick_file = QPushButton('File Backup')
        self.quick_disk = QPushButton('Disk Backup')
        self.quick_mail = QPushButton('Mail Backup')
        self.quick_sql = QPushButton('SQL Backup')
        self.quick_link = QPushButton('LINK TEST')
        self.quick_checklist = QPushButton('Checklist')
        quick_test_v_layout = QVBoxLayout()
        quick_test_v_layout.addWidget(self.quick_label)
        quick_test_v_layout.addWidget(self.quick_file)
        quick_test_v_layout.addWidget(self.quick_disk)
        quick_test_v_layout.addWidget(self.quick_mail)
        quick_test_v_layout.addWidget(self.quick_sql)
        quick_test_v_layout.addWidget(self.quick_link)
        quick_test_v_layout.addWidget(self.quick_checklist)
        left_layout.addWidget(self.new_task_button)
        left_layout.addStretch(1)
        left_layout.addLayout(quick_test_v_layout)

        # 创建右侧按钮控件
        self.proceed_button = QPushButton('PROCEED')
        self.proceed_button.setEnabled(False)
        self.edit_button = QPushButton('EDIT')
        self.edit_button.setEnabled(False)
        self.delete_button = QPushButton('DELETE')
        self.delete_button.setEnabled(False)
        right_button_layout = QHBoxLayout()
        right_button_layout.addStretch(9)
        right_button_layout.addWidget(self.proceed_button)
        right_button_layout.addWidget(self.edit_button)
        right_button_layout.addWidget(self.delete_button)
        # 创建右侧task table
        self.task_table = QTableWidget()
        self.init_table()
        # self.task_table
        right_layout.addLayout(right_button_layout)
        right_layout.addWidget(self.task_table)
        # 设置主界面相关
        main_frame = QWidget()
        main_frame.setLayout(main_layout)
        self.setCentralWidget(main_frame)
        # MainWindow.setLayout(self, main_layout)
        # self.setLayout(main_layout)
        self.setWindowTitle('TB Automation Tool')
        self.setWindowIcon(QIcon(r'..\res\icon.png'))
        self.setAutoFillBackground(True)
        self.resize(800, 500)
        # self.connect(self.task_table, SIGNAL('itemClicked(QTableWidgetItem *)'), self.button_able)
        # self.connect(self.task_table, SIGNAL('itemSelectionChanged()'), self.button_unable)
        self.ui_signal()

    def ui_signal(self):
        self.new_task_button.clicked.connect(self.back_ui)
        self.task_table.itemClicked.connect(self.button_able)
        self.task_table.itemSelectionChanged.connect(self.button_unable)

    # 设置备份还原自动化参数界面
    def back_ui(self):
        backup = BackDialog(self)
        backup.resize(600, 400)
        backup.setWindowTitle("Backup")
        if backup.exec_():
            print("Create a new task")

    def init_table(self):
        # 先从数据库中读取任务数据
        self.task_table.setShowGrid(False)
        self.task_table.setColumnCount(4)
        self.task_table.verticalHeader().setVisible(False)
        self.task_table.setHorizontalHeaderLabels(['Name', 'Type', 'Status', 'Location'])
        self.task_table.setColumnWidth(0, 120)
        self.task_table.setColumnWidth(1, 120)
        self.task_table.setColumnWidth(2, 120)
        self.task_table.setColumnWidth(3, 250)
        self.task_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.task_table.setSelectionBehavior(QAbstractItemView.SelectRows)
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

    def button_able(self):
        self.proceed_button.setEnabled(True)
        self.edit_button.setEnabled(True)
        self.delete_button.setEnabled(True)

    def button_unable(self):
        self.proceed_button.setEnabled(False)
        self.edit_button.setEnabled(False)
        self.delete_button.setEnabled(False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
