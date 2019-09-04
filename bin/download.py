#! coding=utf8


import os
import sys
from shutil import copy, copytree
from bin.log import MyLog

# reload(sys)
# sys.setdefaultencoding('utf8')


class Download:
    def __init__(self, log):
        self.log = log

    def download(self, source, target, _filter=None, ignore=None):
        # source = source.encode('gbk')
        self.log.logger.info('Start to download file or dir')
        try:
            if source.startswith('http') or source.startswith('www'):
                return self.download_from_net(source, target)
            elif os.path.isdir(source):
                return self.download_dir(source, target, _filter, ignore)
            elif os.path.isfile(source):
                return self.download_file(source, target)
        except Exception as e:
            self.log.logger.error(e)
            raise IOError('Download file or dir error:' % e)
        # self.log.logger.info('Download file or dir end')

    @staticmethod
    def download_file(file_source, file_target):
        if not os.path.exists(file_source):
            raise IOError('The source file is not exist:%s' % file_source)
        if not os.path.isfile(file_source):
            raise IOError('The source is not a file')
        # create dir if needed
        if not os.path.exists(file_target):
            os.makedirs(file_target)
        copy(file_source, file_target)
        _path, _name = os.path.split(file_source)
        return os.path.join(file_target, _name)

    def download_dir(self, dir_source, dir_target, _filter=None, ignore=None):
        if not os.path.exists(dir_source):
            raise IOError('The source dir is not exist:%s' % dir_source)
        if not os.path.isdir(dir_source):
            raise IOError('The source is not a dir')
        # create if needed
        if not os.path.exists(dir_source):
            os.makedirs(dir_source)
        _path, _name = os.path.split(dir_source)
        target = os.path.join(dir_target, _name)
        # copy specify file from a dir
        if _filter is not None:
            _filter = [_filter] if ',' not in _filter else _filter.split(',')
            target_path = []
            for __filter in _filter:
                for file_name in os.listdir(dir_source):
                    item = os.path.join(dir_source, file_name)
                    if file_name.endswith(__filter) and os.path.isfile(item):
                        self.log.logger.info('Find item and download:%s' % file_name)
                        target_path.append(self.download_file(item, target))
                if not target_path:
                    raise IOError('No found file %s,and download error' % __filter)
            return target_path
        # copy a dir tree
        else:
            print(1111)
            copytree(dir_source, target, ignore=ignore)
            return target

    def download_from_net(self, address, target):
        self.log.logger.info('Download from net')

    def uncompress(self, package_path, target, tool_path):
        self.log.logger.info('Start to uncompress file')
        if not os.path.exists(package_path):
            raise IOError('No found package:%s' % package_path)
        if os.path.exists(target) and os.system('rd /S /Q "%s"' % target) != 0:
            if os.system('rd /S /Q "%s"' % target) != 0:
                raise SyntaxError('Delete existing folder error:%s' % target)
        # if has uncompress tool
        if not os.path.exists(tool_path):
            raise IOError('No found uncompress tool:%s' % tool_path)
        uncompress_command = r'""%s" -q -x "%s" -d"%s"' % (tool_path, package_path, target)
        if os.system(uncompress_command) != 0:
            raise SyntaxError('Execute uncompress command error')
        self.log.logger.info('Uncompress file end')
        return target


if __name__ == '__main__':
    log = MyLog(r'C:\Users\yuanbin\Desktop', 'log.log')
    download = Download(log)
    print(download.download(r'C:\Users\yuanbin\Desktop\TB_md5', r'D:\setup', _filter='.py,.doc'))
