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



if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = ComputerTree()
    main_window.add_computers([['john', 'win10', 'X64', '192.168.1.112', '这个是跨磁盘系统'],
                               ['python', 'win7', 'X64', '192.168.1.111', '跨磁盘系统']])
    main_window.show()
    sys.exit(app.exec_())
