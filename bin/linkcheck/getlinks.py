#! coding=utf-8
"""
    time:2019.2.20
    author:yangguangxue
    Get useful message from specify excel,and save as a new excel
"""

import os
import xlrd
import xlwt
import time
from xlutils.copy import copy


class GetLink:
    def __init__(self, log, base_path, excel_path):
        self.log = log
        self.base_path = base_path
        self.excel_path = excel_path
        # _path, name = os.path.split(excel_path)
        now_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
        self.new_excel_path = os.path.join(self.base_path, 'result', 'linkcheck', 'result_' + now_time + '.xls')
        if not os.path.exists(excel_path):
            raise IOError('No found excel:%s' % excel_path)
        if not excel_path.endswith('xls') and not excel_path.endswith('xlsx'):
            raise IOError('The file is not a excel file:%s' % excel_path)

        self.create_flag = True  # 创建excel标志
        self.write_row = 1       # 写入excel行数

    def version_filter(self, checked_version, version):
        if version not in checked_version:
            self.log.logger.info('No need to get version:%s links' % version)
            return False
        return True

    def get_link(self, checked_version=None, checked_language=None):
        self.log.logger.info('Start to get link from link excel')
        strings = {'ID': '', 'link': '', 'language': ''}    # 定义要获取的数据
        excel_open = xlrd.open_workbook(self.excel_path)

        for sheet_name in excel_open.sheet_names():
            # python3中无需转码
            # sheet_name = sheet_name.encode('utf-8')

            version = self.convert_version(sheet_name)
            # 筛选要检查的版本
            if not self.version_filter(checked_version, version):
                continue
            sheet = excel_open.sheet_by_name(sheet_name)
            start_row, start_col = self.get_start_row_and_col(sheet)
            # 遍历行和列获取链接
            for col in range(start_col, sheet.ncols):
                # 筛选要检查的语言(区分各个版本)
                if version == 'trial' or version == 'xagon':
                    language = sheet_name
                else:
                    # python3中无需转码
                    # language = sheet.cell_value(start_row, col).encode('utf-8')
                    language = sheet.cell_value(start_row, col)
                language = language if '链接' not in language else language.replace('链接', '')
                if language not in checked_language:
                    self.log.logger.info('No need to get language:%s links' % language)
                    continue

                for row in range(start_row + 1, sheet.nrows):
                    strings['ID'] = sheet.cell_value(row, 0)
                    strings['link'] = sheet.cell_value(row, col)
                    if sheet_name == 'efrontier' or sheet_name == '广告':
                        strings['language'] = sheet_name + '_' + language
                    else:
                        # python3中无需转码
                        strings['language'] = sheet_name
                        # strings['language'] = sheet_name.decode('utf8')
                    # 排除ROW23这一列
                    if strings['ID'] == 'ROW_23':
                        continue
                    self.write_data(self.write_row, strings)
        return self.write_row

    @staticmethod
    def convert_version(sheet_name):
        if sheet_name == 'xagon' or sheet_name == 'efrontier':
            return sheet_name
        elif sheet_name == "广告":
            return 'ad'
        else:
            return 'trial'


    def write_data(self, row, strings):
        # 检查路径是否存在
        _path, name = os.path.split(self.new_excel_path)
        if not os.path.exists(_path):
            os.makedirs(_path)

        if self.create_flag:
            file_open = xlwt.Workbook()
            sheet = file_open.add_sheet('Sheet1', cell_overwrite_ok=True)
            sheet.write(0, 0, 'ID')
            sheet.write(0, 1, 'link')
            sheet.write(0, 2, 'language')
            sheet.write(0, 3, 'result')
            file_open.save(self.new_excel_path)
            self.create_flag = False
        a = xlrd.open_workbook(self.new_excel_path)
        w = copy(a)
        w.get_sheet(0).write(row, 0, strings['ID'])
        w.get_sheet(0).write(row, 1, strings['link'])
        w.get_sheet(0).write(row, 2, strings['language'])
        w.get_sheet(0).col(0).width = 8888
        w.get_sheet(0).col(1).width = 18000
        w.get_sheet(0).col(2).width = 4444
        w.save(self.new_excel_path)
        self.write_row += 1

    def read_data_by_row(self, row):
        data = {}
        if not os.path.exists(self.new_excel_path):
            raise IOError('No found excel:%s' % self.new_excel_path)
        sheet = xlrd.open_workbook(self.new_excel_path).sheet_by_index(0)
        data['ID'] = sheet.cell_value(row, 0)
        data['link'] = sheet.cell_value(row, 1)
        data['language'] = sheet.cell_value(row, 2)
        return data

    @staticmethod
    def get_start_row_and_col(sheet):
        start_col = 4
        # 找到起始行，因为文档起始行不固定，这里以‘ID’出现行为标志
        for row in range(sheet.nrows):
            if sheet.cell_value(row, 0) == 'ID':
                start_row = row
                break
        else:
            start_row = 0
        return start_row, start_col
