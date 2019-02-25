#! coding=utf8

import os
import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from style import STYLE
from functools import partial
import threading
from time import sleep
from bin.ui.log import LogUI
from bin.config import Config
from Run import Run


reload(sys)
sys.setdefaultencoding('utf8')


class CheckLinkUI(QDialog):
    def __init__(self, log, run_path, parent=None):
        super(CheckLinkUI, self).__init__(parent)
        self.log = log
        self.run_path = run_path
        self.run = Run(self.log, self.run_path)
        self.message = 'Initialing...'

        # widget
        self.proceed_btn = QPushButton('执行')
        self.exit_btn = QPushButton('退出')

        self.setting_ui = SettingUI(self.log, self.run_path, self)
        self.log_ui = LogUI(self.log, self.run_path)
        self.log_ui.setVisible(False)
        self.ui()

    def ui(self):
        # ui layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.setting_ui, 10)
        layout.addWidget(self.log_ui, 10)
        layout.addStretch()
        layout.addLayout(self.proceed_layout(), 1)

        # ui settings
        self.setWindowTitle('链接检查')
        self.setStyleSheet(STYLE)
        self.resize(760, 400)
        self.setModal(True)
        self.setBackgroundColor(QColor('#FFFFFF'))
        self.show()

    def setBackgroundColor(self, color):
        pal = QPalette()
        pal.setColor(QPalette.Background, color)
        self.setPalette(pal)
        self.setAutoFillBackground(True)

    def proceed(self):
        self.setting_ui.sava()
        self.setting_ui.setVisible(False)
        self.log_ui.setVisible(True)
        self.proceed_btn.setVisible(False)
        _thread1 = threading.Thread(target=self.run.run)
        _thread2 = threading.Thread(target=self.set_progress, args=(_thread1, ))
        _thread1.start()
        _thread2.start()

    def set_progress(self, thread):
        sleep(0.2)
        while thread.isAlive():
            self.log_ui.progress_bar.setValue(self.run.progress)
            if self.message != self.run.text:
                self.log_ui.text_box.append(self.message)
            self.message = self.run.text
            sleep(0.1)
        self.log_ui.progress_bar.setValue(100)
        self.log_ui.text_box.append(self.run.text)
        self.log_ui.text_box.append('Check link end')


class SettingUI(QWidget):
    def __init__(self, log, run_path, parent=None):
        super(SettingUI, self).__init__(parent)
        self.log = log
        self.run_path = run_path
        self.config_path = os.path.join(run_path, 'config', 'config.ini')
        self.data = Config(log, self.config_path).read() if os.path.exists(self.config_path) else None

        # qt widget
        self.add_version_edit = QLineEdit()
        self.add_version_btn = QPushButton('添加')

        self.radio_specify = QRadioButton("指定安装包或解压包")
        self.edit_specify = QLineEdit()
        self.specify_btn_file = QPushButton('文 件')
        self.specify_btn_dir = QPushButton('文件夹')

        self.radio_download = QRadioButton('下载安装包')
        self.edit_download = QLineEdit()
        self.download_btn_dir = QPushButton('浏览')

        self.group_box = QButtonGroup()
        self.group_box.addButton(self.radio_specify)
        self.group_box.addButton(self.radio_download)

        # self.mail_label = M

        # default data
        self.checked_style = 'background-color:#4BAEB3;color:#FFFFFF;border:1px solid #4BAEB3;'
        self.display_versions = ['trail', 'ad', 'efrontier', 'xagon']
        self.display_languages = ['All', '德语', '英语', '法语', '繁中', '韩语',
                                  '日语', '波兰', '中文', '西班牙', '葡萄牙', '意大利']
        self.display_language_buttons = []
        self.checked_versions = []
        self.checked_languages = []

        self.download = 0
        self.initial_data()
        self.ui()

    def initial_data(self):
        if self.data and 'versions' in self.data.keys():
            versions = self.data['versions']
            self.display_versions = [versions] if ',' not in versions else versions.split(',')
        if self.data and 'languages' in self.data.keys():
            languages = self.data['languages']
            self.display_languages = [languages] if ',' not in languages else languages.split(',')
        if self.data and 'checkversion' in self.data.keys():
            checked_versions = self.data['checkversion']
            self.checked_versions = [checked_versions] if ',' not in checked_versions else checked_versions.split(',')
        if self.data and 'checklanguage' in self.data.keys():
            checked_languages = self.data['checklanguage']
            if checked_languages == 'All':
                self.checked_languages = [i for i in self.display_languages]
            else:
                self.checked_languages = [checked_languages] if ',' not in checked_languages else checked_languages.split(',')

        if self.data and 'download' in self.data.keys():
            download = self.data['download']
            self.download = 0 if download == '0' else 1
        if self.data and 'downloadpath' in self.data.keys():
            self.edit_download.setText(self.data['downloadpath'])

        self.radio_download.setChecked(True) if self.download else self.radio_specify.setChecked(True)
        self.radio_logic()

        if self.data and 'specifypath' in self.data.keys():
            self.edit_specify.setText(self.data['specifypath'])

    def ui(self):
        layout = QVBoxLayout(self)
        layout.addSpacing(10)
        layout.addWidget(QLabel('检查版本'))
        layout.addSpacing(10)
        layout.addLayout(self.display_versions_layout())
        layout.addSpacing(20)
        layout.addWidget(QLabel('检查语言'))
        layout.addLayout(self.display_languages_layout())
        layout.addSpacing(20)

        layout.addWidget(self.radio_specify)
        layout.addlayout(self.specify_layout())
        layout.addWidget(self.radio_download)
        layout.addlayout(self.download_layout())
        layout.addSpacing(20)
        layout.addStretch()

        # ui settings
        self.setStyleSheet(STYLE)
        self.setBackgroundColor(QColor('#FFFFFF'))
        # signals
        self.signals()

    def setBackgroundColor(self, color):
        pal = QPalette()
        pal.setColor(QPalette.Background, color)
        self.setPalette(pal)
        self.setAutoFillBackground(True)

    def display_versions_layout(self):
        layout = QHBoxLayout()
        layout.addSpacing(40)
        for i in range(len(self.display_versions)):
            button = QPushButton(self.display_versions[i])
            # 按钮加宽
            if len(self.display_versions[i]) > 5:
                button.setFixedWidth(10 * (len(self.display_versions[i]) - 5) + 60)
            # 判断按钮初始状态
            if self.display_versions[i] in self.checked_versions:
                button.setStyleSheet(self.checked_style)
            button.clicked.connect(partial(self.display_btn_click, button))
            layout.addWidget(button)
            layout.addStretch()
            return layout

    def display_languages_layout(self):
        layout = QGridLayout()
        _all = False   # 全选标志
        for i in range(len(self.display_languages)):
            button = QPushButton(self.display_languages[i])
            self.display_language_buttons.append(button)
            # 检查是否是全选标志
            if _all:
                button.setStyleSheet(self.checked_style)
            elif button.text() in self.checked_languages:
                button.setStyleSheet(self.checked_style)

            # 处理全选标志
            if self.display_languages[i] == 'All' and self.display_languages[i] in self.checked_languages:
                button.setStyleSheet(self.checked_style)
                _all = True

            # 按钮布局
            half_count = len(self.display_languages) / 2 + len(self.display_languages) % 2
            if i < half_count:
                layout.addWidget(button, 0, 1)
                layout.setColumnStretch(i, 0)   # 设置按钮不拉伸
            else:
                layout.addWidget(button, 1, i-half_count)
            button.clicked.connect(partial(self.display_btn_click, button))
        layout.setColumnStretch(half_count, 10)   # 设置按钮不拉伸
        layout.setContentsMargins(40, 10, 10, 10)   # 设置按钮边间距
        return layout

    def specify_layout(self):
        layout = QHBoxLayout()
        layout.addWidget(self.edit_specify)
        layout.addWidget(self.specify_btn_file)
        layout.addWidget(self.specify_btn_dir)
        return layout

    def download_layout(self):
        layout = QHBoxLayout()
        layout.addWidget(self.edit_download)
        layout.addWidget(self.download_btn_dir)
        return layout

    def radio_logic(self):
        if self.radio_specify.isChecked():
            self.download = 0
            self.edit_download.setEnabled(False)
            self.download_btn_dir.setEnabled(False)
            self.edit_specify.setEnabled(True)
            self.specify_btn_file.setEnabled(True)
            self.specify_btn_dir.setEnabled(True)
        else:
            self.download = 1
            self.edit_download.setEnabled(True)
            self.download_btn_dir.setEnabled(True)
            self.edit_specify.setEnabled(False)
            self.specify_btn_file.setEnabled(False)
            self.specify_btn_dir.setEnabled(False)

    def signals(self):
        self.radio_specify.clicked.connect(self.radio_logic)
        self.radio_download.clicked.connect(self.radio_logic)

    def save(self):
        data = {}
        data['CheckVersion'] = self.checked_versions
        data['CheckLanguage'] = self.checked_languages
        data['SpecifyPath'] = self.edit_specify.text()
        data['download'] = '1' if self.download else '0'
        data['DownloadPath'] = self.edit_download.text()
        download_versions = []
        for version in self.checked_versions:
            if version == 'trail':
                download_versions.append('Trial.exe')
            else:
                download_versions.append('Trial_'+version+'.exe')
        data['version'] = download_versions
        config = Config(self.log, self.config_path)
        config.modify('TBConfig', data)

    def display_btn_click(self, btn):
        if isinstance(btn, QPushButton):
            name = btn.text()
        else:
            raise IOError('display_btn_click需要传递一个按钮对象')

        # 处理全选/全不选
        if name == 'All' and name in self.checked_languages:
            for button in self.display_language_buttons:
                button.setStyleSheet(STYLE)
                self.checked_languages = []
            return

        # 处理其它语言/版本
        if name in self.display_versions:
            if name in self.checked_versions:
                self.checked_versions.remove(name)
                btn.setStyleSheet(STYLE)
            else:
                self.checked_versions.append(name)
                btn.setStyleSheet(self.checked_style)
        else:
            if name in self.display_languages:
                self.checked_languages.remove(name)
                btn.setStyleSheet(STYLE)
                if 'All' in self.checked_languages:
                    self.checked_languages.remove('All')
                    self.display_language_buttons[0].setStyleSheet(STYLE)
            else:
                self.checked_languages.append(name)
                btn.setStyleSheet(self.checked_style)
                if len(self.checked_languages) == len(self.display_languages) - 1:
                    self.checked_languages.append('All')
                    self.display_language_buttons[0].setStyleSheet(self.checked_style)


def run(log, run_path, parent=None):
    app = QApplication(sys.argv)
    ft = QFont()
    ft.setPointSize(11)
    ft.setFamily('宋体')
    app.setFont(ft)
    window = CheckLinkUI(log, run_path, parent=parent)
    window.show()
    sys.exit(app.exec_())



