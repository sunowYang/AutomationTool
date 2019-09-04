#! coding=utf8

import os
import xlrd
import xlwt
from xlutils.copy import copy


class Excel(object):
    def __init__(self, excel_path):
        self.excel_path = excel_path
        self._path, self._name = os.path.split(self.excel_path)

        if not self.excel_path.endswith('.xls') and not self.excel_path.endswith('.xlsx'):
            raise IOError('Parameter "excel_path" is not a excel path:%s' % self.excel_path)

    def create_new(self, sheet_name="Sheet1"):
        if os.path.exists(self.excel_path):
            return self.excel_path

        if not os.path.exists(self._path):
            os.makedirs(self._path)
        elif os.path.isdir(self.excel_path):
            raise IOError('Method "create_new" needs a file path,not a dir path:%s' % self.excel_path)

        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet(sheet_name, cell_overwrite_ok=True)
        workbook.save(self.excel_path)
        return self.excel_path

    def set_titles(self, titles, sheet_name="Sheet1"):
        workbook = xlrd.open_workbook(self.excel_path)
        workbook_copy = copy(workbook)
        sheet = workbook_copy.get_sheet(sheet_name)
        for index in range(len(titles)):
            sheet.write(0, index, titles[index])
        workbook_copy.save(self.excel_path)

    def set_col_width(self, sheet_name, **strings):
        pass


class WriteExcel(Excel):
    def __init__(self, excel_path, target_path=None):
        Excel.__init__(self, excel_path)
        self.target_path = target_path
        if not os.path.exists(self.excel_path):
            self.create_new()
        self.workbook = xlrd.open_workbook(self.excel_path)
        self.workbook_copy = copy(self.workbook)

    def check_if_exist(self):
        if not os.path.exists(self.excel_path):
            raise IOError('No found excel from path:%s' % self.excel_path)

    def write_cell(self, row, col, string, sheet_name="Sheet1", style=None):
        self.check_if_exist()
        try:
            style = xlwt.easyxf(style)
            self.workbook_copy.get_sheet(sheet_name).write(row, col, string, style)
        except Exception as e:
            raise IOError('Write excel failed:%s' % e)

    def write_col(self, sheet_name, col, strings, start_row=0, style=None):
        self.check_if_exist()
        style = xlwt.easyxf(style)
        try:
            for row in range(start_row, len(strings)):
                self.workbook_copy.get_sheet(sheet_name).write(row, col, strings[row-start_row], style)
            self.workbook_copy.save(self.excel_path)
        except Exception as e:
            raise IOError('Write excel failed:%s' % e)

    def write_row(self, row, strings, sheet_name='Sheet1', start_col=0, style=None):
        self.check_if_exist()
        style = xlwt.easyxf(style)
        try:
            for col in range(0, len(strings)):
                self.workbook_copy.get_sheet(sheet_name).write(row, col+start_col, strings[col], style)
        except Exception as e:
            raise IOError('Write excel failed:%s' % e)

    def save_workbook(self):
        if self.target_path:
            self.workbook_copy.save(self.target_path)
        else:
            self.workbook_copy.save(self.excel_path)

    def write_row_by_title(self, row, strings, sheet_name='Sheet1', style=None):
        self.check_if_exist()
        style = xlwt.easyxf(style)
        try:
            sheet = self.workbook.sheet_by_name(sheet_name)
            for key in strings.keys():
                for index in range(sheet.ncols):
                    if sheet.cell_value(0, index) == key:
                        col = index
                        break
                else:
                    raise IOError('No found col:%s when write excel' % key)
                self.workbook_copy.get_sheet(sheet_name).write(row, col, strings[key], style)
        except Exception as e:
            raise IOError('Write excel failed:%s' % e)

    def set_col_width(self, sheet_name='Sheet1', **strings):
        self.check_if_exist()
        try:
            table = self.workbook_copy.get_sheet(sheet_name)
            for key in strings.keys():
                for index in range(table.last_used_col+1):
                    if self.workbook.sheet_by_name(sheet_name).cell(0, index).value == key:
                        table.col(index).width = strings[key]
        except Exception as e:
            raise IOError('Set excel width failed:%s' % e)


class ReadExcel(Excel):
    def __init__(self, excel_path):
        Excel.__init__(self, excel_path)
        if not os.path.exists(self.excel_path):
            raise IOError('No found excel from path:%s' % self.excel_path)

    def read_cell(self, row, col, sheet_name='Sheet1'):
        sheet = xlrd.open_workbook(self.excel_path).sheet_by_name(sheet_name)
        return sheet.cell_value(row, col)

    def read_row(self, row, sheet_name='Sheet1'):
        values = []
        sheet = xlrd.open_workbook(self.excel_path).sheet_by_name(sheet_name)
        if row >= sheet.nrows:
            raise IOError('Read excel failed,the max row is %d,and given row: %d' % (sheet.nrows, row))

        for col in range(sheet.ncols):
            values.append(sheet.cell_value(row, col))
        return values

    def read_row_by_title(self, row, sheet_name='Sheet1', *titles):
        values = {}
        sheet = xlrd.open_workbook(self.excel_path).sheet_by_name(sheet_name)
        if row >= sheet.nrows:
            raise IOError('Read excel failed,the max row is %d,and given %d' % (sheet.nrows, row))

        for title in titles:
            for col in sheet.ncols:
                if sheet.cell_value(0, col) == title:
                    values[title] = sheet.cell_value(row, col)
                    break
            else:
                raise IOError('No found title:%s when read excel' % title)
        return values

    def read_col(self, col, sheet_name='Sheet1'):
        values = []
        sheet = xlrd.open_workbook(self.excel_path).sheet_by_name(sheet_name)
        if col >= sheet.ncols:
            raise IOError('Read excel failed,the max col is %d,and given col: %d' % (sheet.ncols, col))

        for row in range(sheet.nrows):
            values.append(sheet.cell_value(row, col))
        return values

    def read_col_by_count(self, col, rows, start_row=0, sheet_name='Sheet1'):
        values = []
        sheet = xlrd.open_workbook(self.excel_path).sheet_by_name(sheet_name)
        if col >= sheet.ncols:
            raise IOError('Read excel failed,the max col is %d,and given col:%d' % (sheet.ncols, col))
        if rows > sheet.nrows:
            raise IOError('Read excel failed,the max row is %d,and given rows: %d' % (sheet.ncols, col))
        elif rows+start_row > sheet.nrows:
            raise IOError('Read excel failed,the max row is %d,and given rows+start_row:%d' % (sheet.ncols, rows+start_row))

        for row in range(start_row, rows+start_row):
            values.append(sheet.cell_value(row, col))
        return values


if __name__ == '__main__':
    excel = WriteExcel(r'C:\Users\Administrator\Desktop\result_20190902_112505.xls')
    excel.write_row(1, ['row1', 'row2', 'row3'], style='font: colour_index 0x02')
    # excel.set_col_width('user info result', rid=8000, aid=10000)
    excel.save_workbook()
