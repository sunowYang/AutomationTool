#! coding=utf8

import os
from ConfigParser import ConfigParser


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


class ConfigRead:
    """
    Read the config file and return data
    """
    def __init__(self, config_path):
        self.config_path = config_path

    def read(self, section=None):
        dic = {}
        if not os.path.exists(self.config_path):
            raise IOError('No found file:%s' % self.config_path)
        config = ConfigParser()
        config.read(self.config_path)
        if section is None:
            # Get all data of file
            for _section in config.sections():
                for key in config.options(_section):
                    dic[key] = config.get(_section, key)
        else:
            # Get data with specify section
            sections = [section] if ',' not in section else section.split(',')
            for _section in sections:
                if _section in config.sections():
                    for key in config.options(_section):
                        dic[key] = config.get(_section, key)
                else:
                    raise IOError('No found section:%s in %s' % (_section, self.config_path))
        return dic
