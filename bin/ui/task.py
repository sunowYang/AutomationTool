#! coding=utf8
import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from style import Style


class TaskSetting(QDialog):
    def __init__(self, parent=None):
        super(TaskSetting, self).__init__(parent)
        self.case_location = QLineEdit()
        self.result_location = QLineEdit()
        self.task_name = QLineEdit()
        self.initUI()

    def initUI(self):
        tree = ComputerTree3()

        case_layout = QHBoxLayout()
        browse_btn1 = QPushButton('浏览')
        browse_btn1.clicked.connect(self.browse1)
        case_layout.addWidget(self.case_location)
        case_layout.addWidget(browse_btn1)

        result_layout = QHBoxLayout()
        browse_btn2 = QPushButton('浏览')
        browse_btn2.clicked.connect(self.browse2)
        result_layout.addWidget(self.result_location)
        result_layout.addWidget(browse_btn2)

        option_schedule_layout = QHBoxLayout()
        option_label = MyLabel("设置选项")
        option_label.LabelClicked.connect(self.option)
        option_label.setStyleSheet(Style.CLICK_LABEL)
        schedule_label = MyLabel("设置计划")
        schedule_label.LabelClicked.connect(self.schedule)
        schedule_label.setStyleSheet(Style.CLICK_LABEL)
        option_schedule_layout.addSpacing(50)
        option_schedule_layout.addWidget(option_label)
        option_schedule_layout.addSpacing(40)
        option_schedule_layout.addWidget(schedule_label)
        option_schedule_layout.addStretch(1)

        btn_layout = QHBoxLayout()
        proceed_btn = QPushButton('执行')
        proceed_btn.clicked.connect(self.proceed)
        cancel_btn = QPushButton('取消')
        cancel_btn.clicked.connect(self.close)
        btn_layout.addStretch(1)
        btn_layout.addWidget(proceed_btn)
        btn_layout.addSpacing(10)
        btn_layout.addWidget(cancel_btn)


        layout = QVBoxLayout()
        layout.addWidget(QLabel('请选择要执行任务的计算机：'))
        layout.addWidget(tree)
        layout.addWidget(QLabel('请选择要执行的用例和结果存放路径：'))
        layout.setSpacing(10)
        layout.addLayout(case_layout)
        layout.setSpacing(7)
        layout.addLayout(result_layout)
        layout.addWidget(QLabel('请设置任务名：'))
        layout.addWidget(self.task_name)
        layout.addSpacing(10)
        layout.addLayout(option_schedule_layout)
        layout.addSpacing(30)
        layout.addLayout(btn_layout)

        layout.addStretch(1)
        layout.setContentsMargins(10, 5, 10, 10)
        self.setStyleSheet(Style.COMMON_STYLE)
        self.setFixedSize(820, 640)
        self.setWindowTitle('自动化任务')
        self.setLayout(layout)

    def browse1(self):
        file_name, file_type = QFileDialog.getOpenFileName(None, '选择用例', './', '*.xlsx')
        self.case_location.setText(file_name)

    def browse2(self):
        dir_name = QFileDialog.getExistingDirectory(None, '选择结果存放地址', '.')
        self.result_location.setText(dir_name)

    def option(self):
        pass

    def schedule(self):
        pass

    def proceed(self):
        pass


class ComputerTree(QWidget):
    def __init__(self, parent=None):
        super(ComputerTree, self).__init__(parent)
        self.tree = QTreeView()
        self.tree_model = QStandardItemModel()
        self.computer_count = 0
        self.checklist = []
        self.column_count = 6
        self.initUI()

    def initUI(self):
        self.tree.setStyleSheet(Style.COMPUTER_TREE)
        self.tree.setFont(QFont("Roman times", 11))
        # 设置缩进距离
        self.tree.setIndentation(1)
        # 取消item选中后的虚线框
        self.tree.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tree.setFocusPolicy(Qt.NoFocus)
        # 隐藏表头
        self.tree.setHeaderHidden(True)
        self.tree.setModel(self.tree_model)
        self.tree_model.setColumnCount(self.column_count)
        self.tree.setColumnWidth(0, self.width()/4)
        self.tree.setColumnWidth(1, self.width()/8)
        self.tree.setColumnWidth(2, self.width()/8)
        self.tree.setColumnWidth(3, self.width()/5)
        self.tree.setColumnWidth(4, self.width()/3)
        # 增加默认的本机电脑
        local_computer = QStandardItem('这台电脑')
        local_computer.setCheckable(True)
        self.tree_model.setItem(0, 0, local_computer)
        # 增加最后一行的添加按钮
        add = QStandardItem('添加电脑')
        self.tree_model.setItem(1, 0, add)
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.tree)
        self.setMinimumSize(800, 620)
        self.setStyleSheet(Style.COMMON_STYLE)
        self.setLayout(main_layout)

    def add_computer(self, computer):
        item_list = []
        for index in range(len(computer)):
            child = QStandardItem(computer[index])
            if index == 0:
                child.setCheckable(True)
            elif index == self.column_count:   # 超过最大列数，后续数据不显示
                return
            item_list.append(child)
        item_list.append(QStandardItem('Delete'))
        self.tree_model.insertRow(self.computer_count + 1, item_list)

        self.computer_count += 1

    def add_computers(self, computers):
        for computer in computers:
            self.add_computer(computer)


class ComputerTree2(QWidget):
    def __init__(self, parent=None):
        super(ComputerTree2, self).__init__(parent)
        self.tree = QTreeWidget(self)
        self.computer_count = 2
        self.current_index = -1
        self.initUI()

    def initUI(self):
        self.tree.setColumnCount(6)
        # 设置文字
        self.tree.setFont(QFont('Roman times', 11))
        self.tree.setStyleSheet(Style.COMPUTER_TREE)
        # 隐藏头部
        self.tree.setHeaderHidden(True)
        # 设置第一列边距
        self.tree.setIndentation(0)
        # 设置选择item后，不显示边框虚线
        self.tree.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tree.setFocusPolicy(Qt.NoFocus)
        # 设置列宽
        self.setMinimumSize(800, 620)
        self.tree.setColumnWidth(0, self.width()/4)
        self.tree.setColumnWidth(1, self.width()/8)
        self.tree.setColumnWidth(2, self.width()/8)
        self.tree.setColumnWidth(3, self.width()/6)
        self.tree.setColumnWidth(4, self.width()/4)
        self.tree.setColumnWidth(5, self.width()/13)
        # 添加默认的开始和结束列
        self.add_first_and_end_column()
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.tree)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet(Style.COMMON_STYLE)
        self.setMouseTracking(True)
        self.tree.setMouseTracking(True)

        self.setLayout(main_layout)

    def add_first_and_end_column(self):
        # 添加第一行本机电脑
        local_computer = QTreeWidgetItem(['本机电脑'])
        local_computer.setCheckState(0, Qt.Checked)
        add = QTreeWidgetItem()
        add_button = QPushButton('添加...')
        add_button.setStyleSheet(Style.TREE_ADD_BUTTON)
        add_button.setFixedWidth(2000)
        add_button.clicked.connect(self.add_window)
        self.tree.addTopLevelItem(local_computer)
        self.tree.addTopLevelItem(add)
        self.tree.setItemWidget(add, 0, add_button)

    def insert_computer(self, computer):
        item = QTreeWidgetItem(computer)
        del_label = MyLabel("Delete")
        del_label.setStyleSheet(Style.TREE_DEL_LABEL)
        del_label.LabelClicked.connect(self.delete_computer)
        item.setCheckState(0, Qt.Unchecked)
        self.tree.insertTopLevelItem(self.computer_count-1, item)
        self.tree.setItemWidget(item, 5, del_label)
        self.computer_count += 1

    def insert_computers(self, computers):
        for computer in computers:
            self.insert_computer(computer)

    def delete_computer(self):
        # self.tree.takeTopLevelItem(self.tree.currentIndex().row())
        self.tree.takeTopLevelItem(self.current_index)

    def add_window(self):
        window = AddComputer(self)
        if window.exec_():
            pass
        computer = window.info

    def mouseMoveEvent(self, evt):
        self.current_index = evt.y()/36
        print self.current_index


class ComputerTree3(QTreeWidget):
    def __init__(self, parent=None):
        super(ComputerTree3, self).__init__(parent)
        self.computer_count = 2
        self.current_index = -1
        self.initUI()

    def initUI(self):
        self.setFixedHeight(300)
        self.setColumnCount(6)
        # 设置文字
        self.setFont(QFont('Roman times', 11))
        self.setStyleSheet(Style.COMPUTER_TREE)
        # 隐藏头部
        self.setHeaderHidden(True)
        # 设置第一列边距
        self.setIndentation(0)
        # 设置选择item后，不显示边框虚线
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setFocusPolicy(Qt.NoFocus)
        # 设置列宽
        self.setColumnWidth(0, self.width()/4)
        self.setColumnWidth(1, self.width()/8)
        self.setColumnWidth(2, self.width()/8)
        self.setColumnWidth(3, self.width()/6)
        self.setColumnWidth(4, self.width()/4)
        self.setColumnWidth(5, self.width()/13)
        # 添加默认的开始和结束列
        self.add_first_and_end_column()
        # self.setStyleSheet(Style.COMMON_STYLE)
        self.setMouseTracking(True)
        self.show()

    def add_first_and_end_column(self):
        # 添加第一行本机电脑
        local_computer = QTreeWidgetItem(['本机电脑'])
        local_computer.setCheckState(0, Qt.Checked)
        add = QTreeWidgetItem()
        add_button = QPushButton('添加...')
        add_button.setStyleSheet(Style.TREE_ADD_BUTTON)
        add_button.setFixedWidth(2000)
        add_button.clicked.connect(self.add_window)
        self.addTopLevelItem(local_computer)
        self.addTopLevelItem(add)
        self.setItemWidget(add, 0, add_button)

    def insert_computer(self, computer):
        item = QTreeWidgetItem(computer)
        del_label = MyLabel("Delete")
        del_label.setStyleSheet(Style.TREE_DEL_LABEL)
        del_label.LabelClicked.connect(self.delete_computer)
        item.setCheckState(0, Qt.Unchecked)
        self.insertTopLevelItem(self.computer_count-1, item)
        self.setItemWidget(item, 5, del_label)
        self.computer_count += 1

    def insert_computers(self, computers):
        for computer in computers:
            self.insert_computer(computer)

    def delete_computer(self):
        # self.takeTopLevelItem(self.tree.currentIndex().row())
        self.takeTopLevelItem(self.current_index)

    def add_window(self):
        window = AddComputer(self)
        if window.exec_():
            pass
        computer = window.info

    def mouseMoveEvent(self, evt):
        self.current_index = evt.y()/36
        print self.current_index


class MyLabel(QLabel):
    LabelClicked = pyqtSignal()

    def __init__(self, text=None):
        super(MyLabel, self).__init__()
        if text is not None:
            self.setText(text)

    def mousePressEvent(self, evt):
        self.LabelClicked.emit()


class AddComputer(QDialog):
    def __init__(self, parent=None):
        super(AddComputer, self).__init__(parent)
        self.info = []
        self.ip = QLineEdit()
        self.user = QLineEdit()
        self.psd = QLineEdit()
        self.connect_btn = QPushButton('连接')
        self.cancel_btn = QPushButton('取消')
        self.error_label = QLabel('请输入正确的用户名和密码')

        self.connect_btn.clicked.connect(self.connect)
        self.cancel_btn.clicked.connect(self.close)
        self.initUI()

    def initUI(self):
        # 设置IP、密码等格式
        rx = QRegExp("^((2[0-4]\\d|25[0-5]|[01]?\\d\\d?)\\.){3}(2[0-4]\\d|25[0-5]|[01]?\\d\\d?)$")
        self.ip.setValidator(QRegExpValidator(rx))
        self.ip.setPlaceholderText('192.168.0.1')  # 设置默认提示
        self.user.setPlaceholderText('用户名')
        self.psd.setPlaceholderText('密码')
        self.psd.setEchoMode(QLineEdit.Password)  # 设置密码形式
        self.resize(500, 350)
        self.setWindowTitle("添加电脑")
        self.error_label.setStyleSheet("color: red")
        self.error_label.setHidden(True)

        ip_label = QLabel('添加计算机的IP地址：')
        user_label = QLabel('请输入管理员用户名和密码:')
        layout = QVBoxLayout(self)
        layout.addWidget(ip_label)
        layout.addWidget(self.ip)
        layout.addWidget(user_label)
        layout.addWidget(self.user)
        layout.addWidget(self.psd)
        layout.addWidget(self.error_label)

        layout.addStretch(1)
        btn_layout = QHBoxLayout()
        btn_layout.addStretch(1)
        btn_layout.addWidget(self.connect_btn)
        btn_layout.setSpacing(20)
        btn_layout.addWidget(self.cancel_btn)
        layout.addLayout(btn_layout)

        self.setStyleSheet(Style.COMMON_STYLE)
        self.setLayout(layout)

    def connect(self):
        data = [self.ip.text(), self.user.text(), self.psd.text()]
        pass




if __name__ == '__main__':
    app = QApplication(sys.argv)
    # main_window = ComputerTree3()
    # main_window.insert_computers([['john', 'win10', 'X64', '192.168.1.112', '这个是跨磁盘系统'],
    #                               ['python', 'win7', 'X64', '192.168.1.111', '跨磁盘系统']])
    main_window = TaskSetting()
    main_window.show()
    sys.exit(app.exec_())
