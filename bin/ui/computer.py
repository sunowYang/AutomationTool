#! coding=utf8
import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from style import Style


class TaskSetting(QDialog):
    def __init__(self, parent=None):
        super(TaskSetting, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.setStyleSheet(Style.COMMON_STYLE)
        tree = ComputerTree2()
        layout = QVBoxLayout()
        layout.addWidget(tree)
        self.setWindowTitle('任务设置')
        self.setLayout(layout)


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
        self.tree.takeTopLevelItem(self.tree.currentIndex().row())

    def add_window(self):
        window = AddComputer(self)
        if window.exec_():
            pass
        computer = window.info


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
        self.initUI()

    def initUI(self):
        self.resize(600, 400)
        self.setWindowTitle("添加电脑")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = ComputerTree2()
    main_window.insert_computers([['john', 'win10', 'X64', '192.168.1.112', '这个是跨磁盘系统'],
                                  ['python', 'win7', 'X64', '192.168.1.111', '跨磁盘系统']])
    # main_window = TaskSetting()
    main_window.show()
    sys.exit(app.exec_())
