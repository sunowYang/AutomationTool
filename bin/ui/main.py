#! coding=utf8
import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from task import TaskSetting
from style import Style
from bin.automation.runcase import *


class MainWindow(QMainWindow):
    """
    界面初始化：
        创建1个main layout,包括左右两个子layout
    """
    def __init__(self, tasks, parent=None):
        super(MainWindow, self).__init__(parent)
        self.tasks = tasks
        # 初始化界面
        self.initUI()

    def initUI(self):
        # 创建主界面layout
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(LeftSide())
        splitter.addWidget(RightSide(self.tasks))
        # 设置splitter的宽度以及比例
        splitter.setHandleWidth(4)
        splitter.setStretchFactor(1, 3)
        main_layout.addWidget(splitter)
        # 设置主界面相关
        main_frame = QWidget()
        main_frame.setLayout(main_layout)
        self.setStyleSheet(Style.COMMON_STYLE)
        self.setCentralWidget(main_frame)
        self.setWindowTitle('TB Automation Tool')
        self.setWindowIcon(QIcon(r'res/icon.ico'))
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
        self.setMaximumWidth(400)
        self.setLayout(main_layout)
        self.setStyleSheet(Style.LEFT_SIDE_BUTTON)
        self.setBackgroundColor(QColor("#FFFFFF"))
        self.setAutoFillBackground(True)

    def setBackgroundColor(self, color):
        pal = QPalette()
        pal.setColor(QPalette.Background, color)
        self.setPalette(pal)
        self.setAutoFillBackground(True)

    def task_setting(self):
        task = TaskSetting(self)
        if task.exec_():
            print '1111'

    def tasks(self):
        task_button = QPushButton("工具列表")
        task_button.setGeometry(0, 0, 80, 30)
        task_button.setIcon(QIcon('res/icon_task.png'))
        task_button.setIconSize(QSize(20, 20))
        task_button.setStyleSheet(Style.TASKS_BUTTON)
        return task_button

    def new_task(self):
        new_task_button = QPushButton("自动化任务")
        new_task_button.setIcon(QIcon('res/addtask.png'))
        new_task_button.setIconSize(QSize(17, 17))
        new_task_button.setStyleSheet(Style.LEFT_SIDE_TASK_BUTTON)
        new_task_button.clicked.connect(self.task_setting)
        return new_task_button

    @staticmethod
    def link():
        link_button = QPushButton("检查链接")
        # link_button.setIcon(QIcon('res/icon_tool.png'))
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
    def __init__(self, tasks, parent=None):
        super(RightSide, self).__init__(parent)
        self.tasks = tasks
        self.up_side = RightUpSide(self)    # 上侧布局
        self.down_side = RightDownSide(self.tasks, self)  # 下侧布局
        self.initUI()

    def initUI(self):
        # 设置各个控件的样式
        self.setStyleSheet(Style.OTHER_BUTTON)
        # 设置主layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 0, 20, 0)  # 设置边框距离 左上右下的顺序
        main_layout.addWidget(self.up_side)
        main_layout.setSpacing(0)
        main_layout.addWidget(self.down_side)

        self.up_side.currentButtonPressed[int].connect(self.click_button)
        self.setLayout(main_layout)
        self.setBackgroundColor(QColor("#FFFFFF"))
        self.setAutoFillBackground(True)

    def setBackgroundColor(self, color):
        pal = QPalette()
        pal.setColor(QPalette.Background, color)
        self.setPalette(pal)
        self.setAutoFillBackground(True)

    def click_button(self, index):
        # task_name = ""
        if index == -1:
            return
        else:
            select_task = self.down_side.selected_task
            select_task_row = select_task.row()
            if select_task_row == -1:   # 未选择任务
                QMessageBox.warning(self, '错误', '请选择一个任务后再执行')
                return
            else:
                # 获取选中行的第一列的数据，即任务名
                first_column = QModelIndex(select_task)
                first_column = first_column.sibling(select_task_row, 0)
                task_name = self.down_side.tree_model.itemData(first_column).values()[0]
                print ('select task: %s' % task_name)
        if index == 2:
            self.execute(task_name)
            # 执行计划
        elif index == 1:
            # 编辑计划
            pass
        elif index == 0:
            # 删除计划
            pass

    def execute(self, task_name):
        # 执行任务，根据给定任务名查找任务，读取任务配置信息，然后执行
        pass



class RightUpSide(QWidget):
    currentButtonPressed = pyqtSignal(int)

    def __init__(self, parent=None):
        super(RightUpSide, self).__init__(parent)
        self.current_index = -1
        self.row_height = 60
        self.button_list = ['删除', '编辑', '执行']
        self.image_list = [QImage(r'res/icon_delete.png'),
                           QImage(r'res/icon_edit.png'),
                           QImage(r'res/icon_proceed.png')]
        self.initUI()

    def initUI(self):
        self.setMinimumHeight(62)
        self.setMouseTracking(True)
        self.setBackgroundColor(QColor('#FFFFFF'))
        # self.show()

    def setBackgroundColor(self, color):
        pal = QPalette()
        pal.setColor(QPalette.Background, color)
        self.setPalette(pal)
        self.setAutoFillBackground(True)

    def paintEvent(self, evt):
        painter = QPainter(self)
        # 设置反走样，防止出现锯齿
        painter.setRenderHint(QPainter.Antialiasing, True)
        # 设置默认画笔
        painter.setFont(QFont("Roman times", 12))
        painter.setPen(QPen(QColor('#FFFFFF'), 0.5))
        # 开始绘制
        self.draw_text(painter)
        self.draw_line(painter)
        self.draw_button(painter)

    def draw_text(self, painter):
        painter.setPen(QPen(QColor('#black')))
        painter.drawText(QRect(0, 0, 60, 60), Qt.AlignVCenter | Qt.AlignLeft, '任务')

    def draw_line(self, painter):
        painter.setPen(QPen(QColor('#4BAEB3')))
        painter.drawLine(QLine(0, 61, self.width(), 61))

    def draw_button(self, painter):
        painter.setFont(QFont('Roman times', 11))
        painter.setPen(QPen(QColor('#0E73AD')))
        for index in range(len(self.button_list)):
            button = QPainterPath()
            button.addRect(QRectF(self.width()-(index+1)*60, 0, 60, 60))
            if self.current_index == index:
                painter.fillPath(button, QColor('#ECF6F7'))
            painter.drawImage(QRect(QRect(self.width()-(index+1)*60+22, 14, 16, 16)),
                              self.image_list[index])
            painter.drawText(QRect(QRect(self.width()-(index+1)*60+18, 30, 60, 30)),
                             Qt.AlignVCenter | Qt.AlignTop, self.button_list[index])

    def mouseMoveEvent(self, evt):
        # 计算X坐标位于哪个控件上
        y = evt.y()
        x = evt.x()
        idx = (x - (self.width() - 180)) / self.row_height
        # 排除鼠标不在控件范围
        if y > 60 or x < self.width() - 180 or x > self.width():
            idx = -1
        else:
            # 变换位置
            if idx == 0:
                idx = 2
            elif idx == 2:
                idx = 0
        self.current_index = idx
        self.update()

    def mousePressEvent(self, evt):
        self.currentButtonPressed.emit(self.current_index)
        self.update()

    def leaveEvent(self, evt):
        self.current_index = -1
        self.update()


class RightDownSide(QWidget):
    def __init__(self, tasks, parent=None):
        super(RightDownSide, self).__init__(parent)
        self.tree = QTreeView()
        self.tree_model = QStandardItemModel(0, 4)
        self.header = ['任务名', '类型', '最后结果', '存储位置']
        self.tasks = tasks
        self.count = 0
        self.initUI()

    def initUI(self):
        self.tree.setFont(QFont("Roman times", 11))
        # 开启排序
        self.tree.setSortingEnabled(True)
        # 设置缩进距离
        self.tree.setIndentation(1)
        # 取消item选中后的虚线框
        self.tree.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tree.setFocusPolicy(Qt.NoFocus)

        self.tree_model.setHorizontalHeaderLabels(self.header)
        self.tree.setModel(self.tree_model)
        self.tree.setColumnWidth(0, self.tree.width()/4)
        self.tree.setColumnWidth(1, self.tree.width()/4)
        self.tree.setColumnWidth(2, self.tree.width()/4)
        # self.tree.setColumnWidth(3, self.tree.width()/4)
        self.add_tasks(self.tasks)
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.tree)

        self.setLayout(main_layout)

    def add_task(self, task):
        # 创建树的子项，也就是一个任务
        for index in range(4):
            self.tree_model.setItem(self.count, index, QStandardItem(task[index]))
        self.count += 1

    def add_tasks(self, tasks):
        for task in tasks:
            self.add_task(task)

    @property
    def task_count(self):
        return self.count

    @property
    def selected_task(self):
        return self.tree.currentIndex()


def run(tasks):
    app = QApplication(sys.argv)
    # main_window = LeftSide()
    main_window = MainWindow(tasks)
    main_window.show()
    sys.exit(app.exec_())


