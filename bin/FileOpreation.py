#! coding=utf8

# from ConfigParser import ConfigParser
from configparser import ConfigParser
import os
import chardet
import locale


class FileHandle(ConfigParser):
    def __init__(self, config_path):
        self.config_path = config_path
        if not os.path.exists(self.config_path):
            raise IOError('No found config file:%s' % self.config_path)
        ConfigParser.__init__(self)
        self.defaults = "defaults"
        self.file_encode = self.get_file_code()

    def _read_file(self):
        self.read(self.config_path, encoding=self.file_encode)

    def get_file_code(self):
        default_code = locale.getpreferredencoding()
        with open(self.config_path, mode="rb") as f:
            file_code = chardet.detect(f.read())["encoding"]
        if not file_code:
            return default_code
        # BOM单独处理, 与文本内容隔离开
        if "utf-8" in file_code.lower():
            return "utf-8-sig"
        if "utf-16" in file_code.lower():
            return "utf16"
        return default_code

    def optionxform(self, optionstr):
        """-------------------------------------------
        Author: sunow
        Function: optionxform
        Description: 覆写ConfigParser中optionxform方法optionstr.lower()
        Input:
        Return:
        -------------------------------------------"""
        return optionstr

    def get_sections(self):
        """-------------------------------------------
        Author: sunow
        Function: get_sections
        Description: 获取所有标签名
        Input:
        Return: list[tag,tag1,tag2]
        -------------------------------------------"""
        try:
            self.read(self.config_path, encoding=self.file_encode)
            return self.sections()
        except Exception as e:
            raise IOError('get sections fail:%s' % e)

    def get_sections_info(self, *filter_options):
        """-------------------------------------------
        Author: sunow
        Function: get_sections_info
        Description: 获取所有标签内容
        Input: filter_options过滤标签下option
        Return: {tag1:{option:xx},tag2:{option:xx}}
        -------------------------------------------"""
        try:
            self.read(self.config_path)
            d = dict(self._sections)
            for k in d:
                if filter_options:
                    d[k] = dict((key, value) for key, value in d[k].items() if key in filter_options)
                # d[k] = dict(d[k])
            return d
        except Exception as e:
            raise IOError('get sections info fail:%s' % e)

    def get_section_option(self, section, option):
        """-------------------------------------------
        Author: sunow
        Function: get_section_option
        Description: 获取某个标签（key=value）下value值
        Input: section标签名，option
        Return: {tag1:{option:xx},tag2:{option:xx}}
        -------------------------------------------"""
        try:
            self.read(self.config_path, self.file_encode)
            return self.get(section, option)
        except Exception as e:
            raise IOError('get section option fail:%s' % e)

    def del_section(self, section):
        """-------------------------------------------
        Author: sunow
        Function: del_section
        Description: 删除标签及其下内容
        Input: section标签名
        Return:
        -------------------------------------------"""
        try:
            self.read(self.config_path, encoding=self.file_encode)
            self.remove_section(section)
            with open(self.config_path, "w+", encoding=self.file_encode) as f:
                self.write(f)
        except Exception as e:
            raise IOError('del section fail:%s' % e)

    def create_section(self, section):
        """-------------------------------------------
        Author: sunow
        Function: create_section
        Description: 创建标签
        Input: section标签名
        Return:
        -------------------------------------------"""
        try:
            if not self.has_section(section):
                self.read(self.config_path, encoding=self.file_encode)
                self.add_section(section)
                with open(self.config_path, "w+", encoding=self.file_encode) as f:
                    self.write(f)
        except Exception as e:
            raise IOError('create section fail:%s' % e)

    def set_option(self, section, data):
        """-------------------------------------------
        Author: sunow
        Function: set_option
        Description: 添加标签下内容，相同替换
        Input: section标签名，data字典{key:value,key2:value2}
        Return:
        -------------------------------------------"""
        try:
            self.read(self.config_path, encoding=self.file_encode)
            if not self.has_section(section):
                self.add_section(section)
            for key, value in data.items():
                if isinstance(value, list) and len(value) > 1:
                    value = ','.join(iter(value))
                elif isinstance(value, list) and len(value) == 1:
                    value = value[0]
                self.set(section, key, value)
            with open(self.config_path, "w+", encoding=self.file_encode) as f:
                self.write(f)
        except Exception as e:
            raise IOError('set options fail:%s' % e)

    def del_option(self, section, data):
        """-------------------------------------------
        Author: sunow
        Function: del_option
        Description: 删除标签下内容
        Input: section标签名，data删除内容key
        Return:
        -------------------------------------------"""
        try:
            self.read(self.config_path, encoding=self.file_encode)
            self.remove_option(section, data)
            with open(self.config_path, "w+", encoding=self.file_encode) as f:
                self.write(f)
        except Exception as e:
            raise IOError('set options fail:%s' % e)

    def create_file(self):
        """-------------------------------------------
        Author: sunow
        Function: create_file
        Description: 创建文件
        Input:
        Return:
        -------------------------------------------"""
        if not os.path.exists(self.config_path):
            open(self.config_path, 'w').close()

    def save_file(self):
        with open(self.config_path, "w+", encoding=self.file_encode) as f:
            self.write(f)
