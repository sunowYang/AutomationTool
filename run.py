#! coding=utf8

from bin.ui.main import run

if __name__ == '__main__':
    # 先获取数据
    tasks = [['file', 'file backup', 'successful', r'C:\123\123']]
    run(tasks)
