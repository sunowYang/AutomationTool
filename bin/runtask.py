#! coding=utf-8


import os
from parse import ConfigRead
from bin.signature.start import run


class RunTask:
    def __init__(self, task_path):
        self.task_path = task_path
        if os.path.exists(task_path):
            self.task_name = task_path.split('\\')[-1]
        else:
            raise IOError('No found task path:%s' % task_path)

    def read_data(self):
        config_path = os.path.join(self.task_path, self.task_name+'.ini')
        if not os.path.exists(config_path):
            raise IOError('No found task file:%s' % config_path)
        data = ConfigRead(config_path).read()

    def run(self):
