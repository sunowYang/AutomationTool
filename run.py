#! coding=utf8

import os
import sys
from bin.ui.main import run
from bin.gettasks import get_tasks
from PyQt5.QtWidgets import *
from bin.log import MyLog


# ********************************Get executing path******************************
if getattr(sys, 'frozen', False):
    BASE_PATH = os.path.dirname(sys.executable)
else:
    BASE_PATH = os.path.dirname(__file__)
# ********************************************************************************

LOG = MyLog(BASE_PATH, 'log.log')
TASK_PATH = os.path.join(BASE_PATH, 'tasks')

if __name__ == '__main__':
    try:
        run(get_tasks(LOG, TASK_PATH))
    except Exception as e:
        QMessageBox.error('错误', e)
