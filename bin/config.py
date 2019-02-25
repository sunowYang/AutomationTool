#! coding=utf8

from ConfigParser import ConfigParser
import os


class Config:
    """
        @requires:
                log-- an object for writing log
                config_path-- path of config file
        @return:
                a dictionary of data
        Read the config file and return
    """
    def __init__(self, log, config_path):
        self.config_path = config_path
        self.log = log
        self.config = ConfigParser()

    def read(self, section=None):
        dic = {}
        self.log.logger.info('Read config.ini')
        if not os.path.exists(self.config_path):
            raise IOError('No found config file')

        self.config.read(self.config_path)
        if section is None:
            # Get all sections and keys
            for section in self.config.sections():
                for key in self.config.options(section):
                    dic[key] = self.config.get(section, key)
        else:
            # get specify data
            sections = [section] if ',' not in section else section.split(',')
            try:
                for section in sections:
                    for key in self.config.options(section):
                        dic[key] = self.config.get(section, key)
            except Exception, e:
                self.log.logger.error(e)
                raise IOError('Read section %s failed:%s' % (section, e))
        return dic

    def write(self, data, section='config'):
        try:
            open(self.config_path, 'w').close()
            self.config.read(self.config_path)
            self.config.add_section(section)
            for key, value in data.items():
                if isinstance(value, list) and len(value) > 1:
                    value = ','.join(iter(value))
                self.config.set('signature', key, value)
            self.config.write(open(self.config_path, 'w'))
            self.log.logger.info('write config successfully')
        except Exception, e:
            self.log.logger.error(e)
            raise IOError('write config failed:%s' % e)

    def modify(self, section, data):
        try:
            self.config.read(self.config_path)
            if section not in self.config.sections():
                self.config.add_section(section)
            for key, value in data.items:
                if isinstance(value, list) and len(value) > 1:
                    value = ','.join(iter(value))
                elif isinstance(value, list) and len(value) == 1:
                    value = value[0]
                self.config.set(section, key, value)
            self.config.write(open(self.config_path, 'r+'))
            self.log.logger.info('save config successfully')
        except Exception, e:
            self.log.logger.error(e)
            raise IOError('write config failed:%s' % e)





if __name__ == '__main__':
    config = Config('log', r'd:\1.ini')
    config.write({'a': '123', 'b': '321'})
