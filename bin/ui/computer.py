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
        self.tree.setColumnWidth(1, self.width()/9)
        self.tree.setColumnWidth(2, self.width()/9)
        self.tree.setColumnWidth(3, self.width()/5)
        # 增加默认的本机电脑
        self.add_computer(['这台电脑'])
        # 增加最后一行的添加按钮
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.tree)

        self.setMinimumSize(800, 620)
        self.setStyleSheet(Style.COMMON_STYLE)
        self.setLayout(main_layout)

    def add_computer(self, computer):
        for index in range(len(computer)):
            child = QStandardItem(computer[index])
            if index == 0:
                child.setCheckable(True)
            elif index == self.column_count:   # 超过最大列数，后续数据不显示
                return
            self.tree_model.setItem(self.computer_count, index, child)
        # 除第一行本机外，其余行添加最后一列，显示删除图标
        if self.computer_count != 0:
            self.tree_model.setItem(self.computer_count, 6, QStandardItem('delete'))
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
