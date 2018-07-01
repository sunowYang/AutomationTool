#! coding=utf8

from PyQt5.QtWidgets import *


class Layout:
    def __init__(self):
        self.v_layout = QVBoxLayout()
        self.h_layout = QHBoxLayout()


class PathLayout(Layout):
    def __init__(self, label_name, is_browse, label_length, line_edit_default_name=None):
        super(PathLayout, self) .__init__()
        self.label_name = label_name if len(label_name) >= label_length else label_name+' '*(label_length-len(label_name))
        self.line_edit_default_name = line_edit_default_name
        self.is_browse = is_browse
        self.add()

    def add(self):
        self.h_layout.addWidget(QLabel(self.label_name))
        self.h_layout.addWidget(QLineEdit())


