#! coding=utf8

import sys
from PyQt5.QtWidgets import *


class BackDialog(QDialog):
    def __init__(self, parent=None):
        super(BackDialog, self).__init__(parent)
        back_dial = QDial()
        back_dial.setWindowTitle("Backup")
        back_dial.resize(800, 500)
        # back_dial.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = BackDialog()
    dialog.show()
    app.exec_()

