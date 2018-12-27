#! coding=utf8

import os
import sys
import xlwt
import xlrd
import xlsxwriter

# ********************************Get executing path******************************
if getattr(sys, 'frozen', False):
    BASE_PATH = os.path.dirname(sys.executable)
else:
    BASE_PATH = os.path.dirname(__file__)
# ********************************************************************************

COMPARE_FILE = os.path.join(BASE_PATH, "base.xls")


class Signature:
    def __init__(self, compare_file=None):
        self.result_file = compare_file if compare_file else COMPARE_FILE

    def main(self):
        if os.path.exists(self.result_file):
            # start to compare
            self.compare()
        else:
            # start to create base file
            self.create()

    def compare(self):
        pass

    def create(self):
        pass


if __name__ == '__main__':
    pass
