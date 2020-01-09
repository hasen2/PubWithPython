# @Time: 2019/11/30 11:58 PM
# @User: Mac-lhy
# @IDE: PyCharm
# @Author: lhy
# @File: SaveLog.py


import os
import logging.config
import config.baseconfig as cf

class SaveLog:
    def __init__(self):
        _logfile = cf.LOGFILE
        # 判断log要存储的文件夹是否存在，如果不存在则创建相应的目录
        if not os.path.exists(os.path.dirname(_logfile)):
            os.makedirs(os.path.dirname(_logfile))

        # 创建一个日志流
        logger_name = "autotest"
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)  # 设置默认输出级别

        # 将日志输出到文件
        _fh = logging.FileHandler(_logfile, encoding='utf-8')
        _fh.setLevel(logging.INFO)  # 设置等级

        # 将日志输出到控制台
        _fs = logging.StreamHandler()

        # 设置格式输出格式
        fmt = '%(asctime)s [%(name)s] [%(levelname)s] %(filename)s[%(lineno)d] %(message)s'
        datefmt = '%Y-%m-%d %H:%M:%S'
        formatter = logging.Formatter(fmt, datefmt)

        # 将输出路径和输出格式，加入到日志流中
        _fh.setFormatter(formatter)
        _fs.setFormatter(formatter)
        if not self.logger.handlers:  # 如果已经有handlers，则不再添加，否则日志会重复打印
            self.logger.addHandler(_fh)
            self.logger.addHandler(_fs)

    def save_log(self):
        return self.logger


if __name__ == '__main__':
    loger = SaveLog().save_log()
    loger.debug('log debugdddddd得到')
    loger.info('log info')
    loger.warning('log warning')
    loger.error('log error')
    loger.critical('log critical')
    
    aa = SaveLog()
    aa.save_log.info('test')
    
    # from publib.saveinfo.SaveLog import SaveLog
    # saveinfo = SaveLog().save_log()

