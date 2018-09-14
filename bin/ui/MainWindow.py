#! coding=utf8
import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from option import OptionWnd
from Left import LeftSide
from Right import RightSide


class MainWindow(QMainWindow):
    """
    界面初始化：
        创建1个main layout,包括左右两个子layout
    """
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        # 创建主界面layout
        main_layout = QHBoxLayout()
        left_side = LeftSide()
        right_side = RightSide()
        main_layout.addWidget(left_side)
        main_layout.addWidget(right_side)
        # 设置左右框占比
        main_layout.setStretchFactor(left_side, 1)
        main_layout.setStretchFactor(right_side, 4)

        # 设置主界面相关
        main_frame = QWidget()
        main_frame.setLayout(main_layout)
        self.setCentralWidget(main_frame)
        self.setWindowTitle('TB Automation Tool')
        self.setWindowIcon(QIcon(r'..\res\icon.png'))
        self.setAutoFillBackground(True)
        self.resize(1084, 646)
        self.setBackgroundColor(QColor('#FFFFFF'))
        self.setAutoFillBackground(True)

    def setBackgroundColor(self, color):
        pal = QPalette()
        pal.setColor(QPalette.Background, color)
        self.setPalette(pal)
        self.setAutoFillBackground(True)

    # 设置备份还原自动化参数界面
    def option_ui(self):
        option = OptionWnd()
        if option.exec_():
            print("Create a new task")

    def backup_dialog_init(self):
        pass

    def button_able(self):
        self.proceed_button.setEnabled(True)
        self.edit_button.setEnabled(True)
        self.delete_button.setEnabled(True)

    def button_unable(self):
        self.proceed_button.setEnabled(False)
        self.edit_button.setEnabled(False)
        self.delete_button.setEnabled(False)


def run():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
