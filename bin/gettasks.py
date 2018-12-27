#! coding=utf8

import os
from ConfigParser import ConfigParser


def get_tasks(log, task_path):
    tasks = []
    if not os.path.exists(task_path):
        log.logger.warn("No found directory of tasks")
        raise IOError("No found directory of tasks")
    for _dir in os.listdir(task_path):
        dir_path = os.path.join(task_path, _dir)
        # get task file *.ini
        if os.path.isdir(dir_path):
            task = parse(log, os.path.join(dir_path, _dir + '.ini'))
            if task:
                tasks.append(task)
        else:
            continue
    return tasks


def parse(log, file_path):
    data = []
    if not os.path.exists(file_path):
        log.logger.warn("Task file is not exist: %s" % file_path)
        return None
    config = ConfigParser()
    config.read(file_path)
    for section in config.sections():
        for key in config.options(section):
            data.append(config.get(section, key))
    return data


if __name__ == '__main__':
    get_tasks(r'C:\Users\yuanbin\Documents\GitHub\AutomationTool\tasks')