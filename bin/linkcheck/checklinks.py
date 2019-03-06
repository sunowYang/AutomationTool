#! coding=utf8

import os
from bin.config import Config


class CheckLink:
    def __init__(self, log, strings, package_path, base_path):
        self.log = log
        self.strings = strings
        self.package_path = package_path
        self.language_config_path = os.path.join(base_path, 'config', 'linkcheck', 'language.ini')
        self.language, self.version = self.get_language_version()
        self.package_path = self.get_package_path()
        self.id = strings['ID'] if 'ID' in strings.keys() else None
        self.link = strings['link'] if 'link' in strings.keys() else None
        self.language = strings['language'] if 'language' in strings.keys() else None
        self.outer_link_id = ['CTPANL', 'STARTP', 'UNINST', 'INSTALL', 'UNINSTALL',
                              'HELP_ONLINE', 'ID_LINK_BUY_', 'ID_LINK_HONE_BUY']

        self.failed_excel_link = ''
        self.failed_program_link = ''

    def get_package_path(self):
        version = self.version if self.version == 'trial' else 'trial_' + self.version
        if isinstance(self.package_path, list):
            for package in self.package_path:
                if package.lower().endswith(version):
                    break
            else:
                raise IOError('No found version package path:%s' % self.version)
            return package
        else:
            return self.package_path


    def get_language_version(self):
        if self.strings['language']:
            language = self.strings['language']
            if language == 'xagon':
                version = 'xagon'
                language = '日语'
            elif '_' in language:
                version = language.split('_')[0]
                language = language.split('_')[1].encode('utf8')
            else:
                version = 'trial'
                language = language.encode('utf8')
        else:
            self.log.logger.error('No found "language" row in test.xls')
            return False
        if '链接' in language:
            language = language.replace('链接', '')
        return language, version

    def get_excel_link(self):
        return self.strings['link'].lower().strip()

    def get_program_link(self):
        for outer_id in self.outer_link_id:
            if outer_id in self.id:
                program_link = self.get_program_link_from_install_file()
                break
        else:
            program_link = self.get_program_link_from_ini()
        return program_link

    def get_program_link_from_ini(self):
        # 根据version language 获取common_url.ini文件位置
        ini_path = self.get_common_url_path()
        if not ini_path:
            return False
        config = Config(self.log, ini_path)
        url = config.read('text') if self.id.lower() != 'email' else config.read('ContactProductManegerUrl')
        if self.id.lower() not in url.keys():
            self.log.logger.error('No found key:%s in common_url.ini' % self.id)
            return False
        link = url[self.id.lower()].lower()
        return link if 'mailto' not in link else link.split(':')[1]

    def get_program_link_from_install_file(self):
        return GetLinkFromInstallFile(self.language, self.version, self.id, self.package_path).get_link()

    def get_common_url_path(self):
        if self.package_path.endswith(self.version):
            if self.version == 'xagon':
                url_path = os.path.join(self.package_path, r'{app}\bin', 'common_url,2.ini')
            else:
                url_name = Config(self.log, self.language_config_path).read('url')
                url_path = os.path.join(self.package_path, r'{app}\bin', url_name[self.language])
            # TB特殊处理efrontier日语版(链接文件为common_url,12.ini)
            if self.version == 'efrontier' and self.language == '日语':
                url_path = os.path.join(self.package_path, r'{app}\bin', 'common_url,12.ini')
            # 特殊处理ad版本(链接文件编号+11)
            if self.version == 'ad':
                url_path_list = url_path.split(',')
                url_path_index = int(url_path_list[1].split('.')[0])
                # 日语本来的index是11，但是这里插队了，插在波兰语(index=6)前面，后续语言一次+1
                if url_path_index == 11:
                    url_path = url_path_list[0] + ',17.ini'
                elif url_path_index >= 6:  # 波兰语后面的语言+12
                    url_path = url_path_list[0] + ',' + str(url_path_index + 12) + '.ini'
                else:  # 波兰语前面的语言+11
                    url_path = url_path_list[0] + ',' + str(url_path_index + 11) + '.ini'
        else:
            raise IOError('package path and version is not matching')
        return url_path

    def check(self):
        excel_link = self.get_excel_link()
        program_link = self.get_program_link()
        if excel_link == program_link:
            result = 'success'
        elif excel_link.endswith("/") and excel_link[:-1] == program_link:   # 排除最后斜杠
            result = 'success'
        elif 'www.' in excel_link and excel_link.replace('www.', '') == program_link:
            result = 'success'
        else:
            self.log.logger.info('The program link is:%s' % program_link)
            self.log.logger.info('The excel   link is:%s' % excel_link)
            result = 'Failed'
            self.failed_excel_link = excel_link
            self.failed_program_link = program_link
        return result


class GetLinkFromInstallFile:
    def __init__(self, language, version, _id, package_path):
        self.language = language
        self.version = version
        self.id = _id
        self.package_path = package_path

    def filter_link(self, file_name=u'安装脚本.iss'):
        file_path = os.path.exists(os.path.join(self.package_path, file_name))
        if not file_path:
            raise IOError('No found iss file:%s' % file_path)
        with open(file_path, 'r') as f:
            content = f.read()
        link_dict = dict()
        for i in content.split('\n'):
            if 'http' in i:
                key = i[:i.find('=')]
                value = i[i.find('=') + 1:]
                link_dict[key] = value
        return link_dict

    def get_link(self):
        file_key = ''
        dic = self.filter_link()
        # 处理XAGON版本
        if self.version.upper() == 'XAGON':
            file_key = self.id if self.id.split('_')[-1].upper() != 'XAGON' else self.id + '_XAGON'
        # 处理EFRONTIER的日语版
        elif self.version.upper() == "EFRONTIER" and self.language.upper() == "JAPANESE" and \
                ("BUY" in self.id or '_INSTALL' in self.id):
            if 'BUY' in self.id:
                file_key = self.id + "_EFRONTIER" if self.id.split('_')[-1].upper() != "EFRONTIER" else self.id
            elif "_INSTALL" in self.id:
                file_key = 'ID_LINK_INSTALL_EFRONTIER'
        # 处理EFRONTIER版本free版本安装时的购买链接，做变形
        elif self.id == 'ID_LINK_BUY_EFRONTIER':
            file_key = self.language + '.' + 'ID_LINK_HOME_BUY'
        else:
            file_key = self.language + '.' + self.id
        if file_key in dic.keys():
            return dic[file_key]
        else:
            return False
