#! coding=utf8

import sys
from PyQt5.QtWidgets import *
from LabelClick import LabelClick


def read_version():
    return list('12345')


class BackDialog(QDialog):
    def __init__(self, parent=None):
        super(BackDialog, self).__init__(parent)
        # self.ui_init()
        self.setWindowTitle("Settings")
        self.resize(600, 400)
        self.setLayout(self.add_layout())

    def ui_init(self):
        back_dial = QDial()
        back_dial.setWindowTitle("Backup")
        back_dial.resize(600, 300)
        back_dial.setLayout(self.add_layout())

    def add_layout(self):
        main_layout = QVBoxLayout()
        main_layout.addLayout(self.add_script_layout())
        # main_layout.addLayout()
        main_layout.addLayout(self.add_package_layout())
        main_layout.addLayout(self.add_mail_layout())
        main_layout.addStretch(1)
        button_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        main_layout.addWidget(button_box)
        return main_layout

    def add_split_layout(self):
        split_layout = QVBoxLayout()

    def add_script_layout(self):
        svn_path_layout = QHBoxLayout()
        svn_label = QLabel('       svn path:   ')
        svn_line_edit = QLineEdit()
        svn_path_layout.addWidget(svn_label)
        svn_path_layout.addWidget(svn_line_edit)

        local_path_layout = QHBoxLayout()
        local_path_label = QLabel('       local path: ')
        local_path_line_edit = QLineEdit()
        local_path_layout.addWidget(local_path_label)
        local_path_layout.addWidget(local_path_line_edit)

        script_layout = QVBoxLayout()
        script_checkout = QCheckBox('Use newest script')
        script_layout.addWidget(script_checkout)
        script_layout.addLayout(svn_path_layout)
        script_layout.addLayout(local_path_layout)

        return script_layout

    def add_package_layout(self):
        package_path_layout = QHBoxLayout()
        package_label = QLabel('       package path: ')
        package_line_edit = QLineEdit()
        package_path_layout.addWidget(package_label)
        package_path_layout.addWidget(package_line_edit)

        package_version_layout = QHBoxLayout()
        package_version_label = QLabel('       package version: ')
        package_version_list = read_version()
        package_version_combobox = QComboBox()
        package_version_combobox.addItems(package_version_list)
        package_version_layout.addWidget(package_version_label)
        package_version_layout.addWidget(package_version_combobox)
        add_label = LabelClick()
        add_label.setText('Add...')
        package_version_layout.addWidget(add_label)
        # package_version_layout.addWidget(QLabel('Add...'))

        package_layout = QVBoxLayout()
        package_checkout = QCheckBox('Use newest package')
        package_layout.addWidget(package_checkout)
        package_layout.addLayout(package_path_layout)
        package_layout.addLayout(package_version_layout)
        package_layout.addStretch(1)

        return package_layout

    def add_mail_layout(self):
        mail_layout = QVBoxLayout()
        mail_layout.addWidget(QCheckBox('Send mail'))
        return mail_layout



if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = BackDialog()
    dialog.show()
    app.exec_()

