#! coding=utf-8


from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from style import Style


class LogUI(QWidget):
    def __init__(self, log, module, parent=None):
        super(LogUI, self).__init__(parent)
        self.log = log
        self.module = module

        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(100)
        self.text_box = QTextBrowser()
        self.ui()

    def ui(self):
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.progress_bar)
        main_layout.addWidget(self.text_box)

        self.setStyleSheet(Style.STYLE)
        self.setLayout(main_layout)
        self.setBackgroundColor(QColor('#FFFFFF'))

    def setBackgroundColor(self, color):
        pal = QPalette()
        pal.setColor(QPalette.Background, color)
        self.setPalette(pal)
        self.setAutoFillBackground(True)
