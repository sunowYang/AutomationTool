# -*- coding: utf-8 -*-#


from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from bin.ui.style import Style


class ExecutePage(QWidget):
    def __init__(self, parent=None):
        super(ExecutePage, self).__init__(parent)
        self.initUI()

    def initUI(self):
        # 设置背景为白色
        self.setBackgroundColor(QColor("#FFFFFF"))
        # 设置各个控件的样式
        self.setStyleSheet(Style.COMMON_STYLE)
        # 设置layout
        self.setLayout(self.parameterLayout())

    def setSpecifyCase(self):
        if self.specify_case.isChecked():
            self.from_case.setEnabled(True)
            self.to_case.setEnabled(True)
        else:
            self.from_case.setEnabled(False)
            self.to_case.setEnabled(False)

    def setBackgroundColor(self, color):
        pal = QPalette()
        pal.setColor(QPalette.Background, color)
        self.setPalette(pal)
        self.setAutoFillBackground(True)

    def parameterLayout(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.addLayout(self.execute_time_layout())
        main_layout.addLayout(self.priority_layout())
        main_layout.addLayout(self.execute_case_layout())
        # main_layout.addLayout(self.execute_model_layout())
        main_layout.addStretch()
        return main_layout

    def execute_time_layout(self):
        # 设置执行次数
        _execute_time_layout = QHBoxLayout()
        _execute_time_layout.setSpacing(10)
        execute_time_label = QLabel('执行次数：')
        self.execute_time_spinbox = QSpinBox()
        self.execute_time_spinbox.setRange(1, 100)
        self.execute_time_spinbox.setValue(1)
        _execute_time_layout.addWidget(execute_time_label)
        _execute_time_layout.addWidget(self.execute_time_spinbox)
        _execute_time_layout.addStretch()
        return _execute_time_layout

    def priority_layout(self):
        _priority_layout = QVBoxLayout()
        _priority_layout.setSpacing(10)
        priority_label = QLabel('优先级设置（只执行选中的优先级）')
        priority_button_layout = QHBoxLayout()
        priority_button_layout.addWidget(QLabel('  '))
        # 设置优先级
        self.priority0 = QCheckBox('0')
        self.priority1 = QCheckBox('1')
        self.priority2 = QCheckBox('2')
        self.priority3 = QCheckBox('3')
        self.priority0.setChecked(True)
        self.priority1.setChecked(True)
        self.priority2.setChecked(True)
        self.priority3.setChecked(True)
        priority_button_layout.addWidget(self.priority0)
        priority_button_layout.addWidget(self.priority1)
        priority_button_layout.addWidget(self.priority2)
        priority_button_layout.addWidget(self.priority3)
        priority_button_layout.addStretch(1)
        _priority_layout.addWidget(priority_label)
        _priority_layout.addLayout(priority_button_layout)
        return _priority_layout

    def execute_case_layout(self):
        # 设置执行用例
        _execute_case_layout = QVBoxLayout()
        _execute_case_layout.setSpacing(5)
        self.radio_group = QButtonGroup()
        self.all_case = QRadioButton('所有用例')
        self.specify_case = QRadioButton('指定用例:')
        # 设置信号
        self.specify_case.clicked.connect(self.setSpecifyCase)
        self.all_case.clicked.connect(self.setSpecifyCase)
        self.radio_group.addButton(self.all_case)
        self.radio_group.addButton(self.specify_case)

        specify_case_layout = QHBoxLayout()
        self.from_case = QSpinBox()
        self.to_case = QSpinBox()
        # 设置默认关闭，当选择指定用例时打开
        self.from_case.setEnabled(False)
        self.to_case.setEnabled(False)
        specify_case_layout.addWidget(QLabel('  '))
        specify_case_layout.addWidget(self.specify_case)
        specify_case_layout.addWidget(QLabel('从'))
        specify_case_layout.addWidget(self.from_case)
        specify_case_layout.addWidget(QLabel('到'))
        specify_case_layout.addWidget(self.to_case)
        specify_case_layout.addStretch()

        all_case_layout = QHBoxLayout()
        all_case_layout.addWidget(QLabel('  '))
        all_case_layout.addWidget(self.all_case)
        all_case_layout.addStretch()

        # 设置默认值
        self.all_case.setChecked(True)
        _execute_case_layout.addWidget(QLabel('选择执行用例:'))
        _execute_case_layout.addLayout(all_case_layout)
        _execute_case_layout.addLayout(specify_case_layout)


        return _execute_case_layout

    def execute_model_layout(self):
        _execute_model_layout = QVBoxLayout()
        self.all_model = QRadioButton('所有模块')
        self.specify_model = QRadioButton('指定模块')
        self.model_group = QButtonGroup()
        self.model_group.addButton(self.all_model)
        self.model_group.addButton(self.specify_model)

        all_model_layout = QHBoxLayout()
        all_model_layout.addWidget(QLabel('  '))
        all_model_layout.addWidget(self.all_model)
        all_model_layout.addStretch()
        # 设置默认值，默认选择all
        self.all_model.setChecked(True)

        specify_model_layout = QHBoxLayout()
        specify_model_layout.addWidget(QLabel('  '))
        specify_model_layout.addWidget(self.specify_model)
        specify_model_layout.addStretch()

        # 设置模块checkbox
        model_checkbox_layout = QGridLayout()
        self.file_backup = QCheckBox('文件备份')
        self.disk_backup = QCheckBox('磁盘备份')
        self.mail_backup = QCheckBox('邮件备份')
        self.sql_backup = QCheckBox('sql备份')
        self.exchange_backup = QCheckBox('exchange备份')
        self.schedule = QCheckBox('schedule')
        self.option = QCheckBox('option')
        self.clone = QCheckBox('克隆')
        self.cleanup = QCheckBox('镜像清理')
        self.task_import = QCheckBox('任务导入导出')
        self.p2v = QCheckBox('p2v')
        self.mount = QCheckBox('mount')
        # 设置默认勾选
        self.file_backup.setChecked(True)
        self.disk_backup.setChecked(True)
        self.mail_backup.setChecked(True)
        self.sql_backup.setChecked(True)
        self.exchange_backup.setChecked(True)
        self.schedule.setChecked(True)
        self.option.setChecked(True)
        self.clone.setChecked(True)
        self.cleanup.setChecked(True)
        self.task_import.setChecked(True)
        self.p2v.setChecked(True)
        self.mount.setChecked(True)
        model_checkbox_layout.addWidget(self.file_backup, 1, 1)
        model_checkbox_layout.addWidget(self.disk_backup, 1, 2)
        model_checkbox_layout.addWidget(self.mail_backup, 1, 3)
        model_checkbox_layout.addWidget(self.sql_backup, 1, 4)
        model_checkbox_layout.addWidget(self.exchange_backup, 2, 1)
        model_checkbox_layout.addWidget(self.schedule, 2, 2)
        model_checkbox_layout.addWidget(self.option, 2, 3)
        model_checkbox_layout.addWidget(self.cleanup, 2, 4)
        model_checkbox_layout.addWidget(self.p2v, 3, 1)
        model_checkbox_layout.addWidget(self.mount, 3, 2)
        model_checkbox_layout.addWidget(self.clone, 3, 3)
        model_checkbox_layout.addWidget(self.task_import, 3, 4)

        _execute_model_layout.addWidget(QLabel('选择执行模块：'))
        _execute_model_layout.addLayout(all_model_layout)
        _execute_model_layout.addLayout(specify_model_layout)
        _execute_model_layout.addLayout(model_checkbox_layout)
        return _execute_model_layout
