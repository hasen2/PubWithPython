# @Time: 2019/12/5 18:43
# @User: Win-lhy
# @IDE: PyCharm
# @Author: lhy
# @File: CopyFile.py

import shutil
import datetime
from config import baseconfig as config
from publib.savedata.savelogs.SaveLog import SaveLog

savelog = SaveLog().save_log()

class CopyFile:
    def __init__(self):
        pass

    def copy_file(self,oldfile,newfile):
        """
        复制文件到一个新的地址
        :param oldfile: 原文件名（包含路径）
        :param newfile: 新文件名（包含路径）
        :return:
        """
        shutil.copy(oldfile, newfile)
        savelog.info(f'将[{oldfile}]复制到[{newfile}]')

    def copy_testcase(self):
        """
        将测试案例及请求报文分别复制一份到新的目录  （每次案例执行结束时调用该函数）
        :return:
        """
        nowdatastr = datetime.datetime.now().strftime('%Y-%m-%d')
        oldfile = config.get_fileaddr('测试案例.xls')
        newfile = config.get_fileaddr(f'casecopy/{nowdatastr}测试案例.xls')
        self.copy_file(oldfile, newfile)
        oldfile = config.get_fileaddr('请求报文体.xls')
        newfile = config.get_fileaddr(f'casecopy/{nowdatastr}请求报文体.xls')
        self.copy_file(oldfile, newfile)


if __name__ == '__main__':
    cf = CopyFile()
    oldfile = r'D:\www\aaa.txt'
    newfile = r'D:\wwww\bbb.txt'
    cf.copy_file(oldfile,newfile)

