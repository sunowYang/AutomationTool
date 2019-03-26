#! coding=utf8


import os
import sys
import time
from bin.download import Download
from getlinks import GetLink
from checklinks import CheckLink
from bin.config import Config
from bin.excel import WriteExcel
from PyQt5.QtCore import *


class RunCheck(QObject):
    progress_message = pyqtSignal(int, str)
    stop_signal = pyqtSignal()

    def __init__(self, log, base_path, parent=None):
        super(RunCheck, self).__init__(parent)
        self.log = log
        self.base_path = base_path
        self.link_path = os.path.join(self.base_path, 'config', 'linkcheck', 'link.xls')
        self.config_path = os.path.join(self.base_path, 'config', 'linkcheck', 'config.ini')
        self.data = {}

    def run(self):
        new_link_excel = ''
        try:
            self.progress_message.emit(5, '正在初始化...')
            self.data = Config(self.log, self.config_path).read()
            self.progress_message.emit(10, '开始下载和解压...')
            uncompressed_path = self.download_and_uncompress()
            self.progress_message.emit(45, '下载解压完成,获取excel链接')

            link = GetLink(self.log, self.base_path, self.link_path)
            max_row = link.get_link(self.data['checkversion'], self.data['checklanguage'])
            new_link_excel = link.new_excel_path
            self.progress_message.emit(60, '开始检查excel链接')
            _progress = float(max_row)/40

            if 'click_tb' in self.data.keys() and self.data['click_tb'] == '1':
                self.progress_message.emit(60, '通过点击TB界面获取链接')
            for row in range(1, max_row):
                strings = link.read_data_by_row(row)
                # 增加点击TB界面获取链接的方式，2019.03.26 ygx
                if 'click_tb' in self.data.keys() and self.data['click_tb'] == '1':
                    result = 'success'
                else:
                    check = CheckLink(self.log, strings, uncompressed_path, self.base_path)
                    result = check.check()
                self.write_result(row, result, new_link_excel)
                progress = 60 + row/_progress
                if result == 'Failed':
                    self.progress_message.emit(progress,
                                               '第%d行检测到链接不相等\n文档链接:%s\n程序链接:%s'
                                               % (row+1, check.failed_excel_link, check.failed_program_link))
                elif row % _progress == 0 and row / _progress != 0:
                    self.progress_message.emit(progress, '')
            self.progress_message.emit(100, '检查完成')
            # 设置列宽
            self.set_col_width(new_link_excel)
        except Exception as e:
            self.progress_message.emit(100, '检查失败:\n%s' % e.message)
            raise Exception('检查失败\n%s' % e.message)
        finally:
            self.progress_message.emit(100, new_link_excel)


    def download_and_uncompress(self):
        download_flag = '0' if 'download' not in self.data.keys() else self.data['download']
        download = Download(self.log)
        if download_flag != '0':
            package_path = download.download(self.data['downloadpath'], r'C:\setup\package',
                                             _filter=self.data['version'])
        else:
            package_path = [self.data['specifypath']]

        uncompressed_path = []
        for package in package_path:
            if os.path.isdir(package):
                uncompressed_path.append(package)
            else:
                tool_path = os.path.join(self.base_path, 'tools', 'innounp.exe')
                uncompressed_path.append(download.uncompress(package, package[:-4], tool_path))
        return uncompressed_path


    def get_result_path(self):
        now_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
        return os.path.join(self.base_path, 'result', 'linkcheck', 'result_' + now_time + '.xls')

    @staticmethod
    def write_result(row, result, excel_path):
        excel = WriteExcel(excel_path)
        excel.write_row_by_title(row, result=result)

    @staticmethod
    def set_col_width(excel_path):
        excel = WriteExcel(excel_path)
        excel.set_col_width(ID=8888, link=18000, language=5000)

