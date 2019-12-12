# @Time: 2019/12/11 11:26
# @User: Win-lhy
# @IDE: PyCharm
# @Author: lhy
# @File: GetResponseMysql.py



import os
import json
import requests
import datetime

import config.baseconfig as config
from publib.apidatalib.MysqlGetData import MysqlGetData
from publib.pubdef.AssertMsg import AssertMsg as AM
from publib.database.ConnectDb2 import ConnectDb2
from publib.savedata.savelogs.SaveLog import SaveLog

savelog = SaveLog().save_log()

class GetResponseMysql:
    def __init__(self):
        self.mgd = MysqlGetData()
        self.am = AM()
        self.cndb = ConnectDb2()


    def get_requestdata_res(self, casename, code='utf-8', theheader=None):
        """
        调取接口并返回接口返回的原始内容
        :param apiname: 接口名
        :param casename: 用例名
        :param bodyfilename: 报文体文件名，默认'请求报文体.xls'
        :param code: 字符编码，默认为'utf-8'
        :param host: host地址，默认从excel中取值
        :return:接口请求内容
        """

        # 根据用例名查询接口名
        apiname = self.mgd.get_apiname(testcasename=casename)

        # 检查接口报文保存路径是否存在
        messagedir = os.path.join(config.MYMESSAGELOG, casename)
        if not os.path.exists(messagedir):   # 如果不存在，则新建一个
            savelog.info(f'新建目录{messagedir}')
            os.makedirs(messagedir)
        messagefile = os.path.join(messagedir, apiname + '.txt')  # 定义报文保存的文件名

        # 获取url
        theurl = self.mgd.get_url(apiname=apiname)
        savelog.info(f'用例[{casename}]操作接口[{apiname}]的URL:{theurl}')

        # 获取用例关联的公共资源调用（header，bodyhead）
        theheadertype,theheadtype = self.mgd.get_head_type(testcasename=casename)

        # 获取header
        if theheader:
            pass
        else:
            theheader = self.mgd.get_header(headertype=theheadertype)
        savelog.info(f'用例[{casename}]操作接口[{apiname}]的请求头:{theheader}')

        # 获取body
        thebodyhead = self.mgd.get_body_head(headtype=theheadtype)
        thebodybody = self.mgd.get_body_body(testcasename=casename, apiname=apiname)
        thebody = {"head": thebodyhead, "body": thebodybody}
        savelog.info(f'用例[{casename}]操作接口[{apiname}]的请求体:{thebody}')

        # 将请求报文写入到文档备份
        with open(messagefile, 'w', encoding='utf-8') as f:
            savelog.info(f'将用例[{casename}]操作接口[{apiname}]的请求信息写入到:{messagefile}')
            f.write(f'{datetime.datetime.now()}\n\n请求URL：\n{theurl}')
            f.write('\n\n请求头：\n')
            json.dump(theheader, f, indent=4, ensure_ascii=False)
            f.write('\n\n请求体：\n')
            json.dump(thebody, f, indent=4, ensure_ascii=False)
            savelog.debug(f'用例[{casename}]操作接口[{apiname}]的请求报文json:{json.dumps(thebody)}')
        try:
            savelog.info(f'用例[{casename}]开始请求接口：{apiname}_start')
            # 发起请求
            req = requests.post(url=theurl, headers=theheader, data=json.dumps(thebody))
            savelog.info(f'用例[{casename}]结束请求接口：{apiname}_end')
            # 转码
            req.encoding = code
            return req, messagefile, thebody
        except Exception as b:
            assert 0, savelog.critical(f'用例[{casename}]操作接口[{apiname}]-->请求失败:{b}')

    def get_response(self, casename, theheader=None):
        """
        请求接口，校验相关信息，并返回对应的内容，
        :param apiname: 接口名，eg:002001
        :param casename: 用例名
        :param host: 端口
        :param headerdict: 请求头
        :return: 返回请求成功后的数据
        """

        # 根据用例名查询接口名
        apiname = self.mgd.get_apiname(testcasename=casename)

        # 调用接口数据
        res, messagefile, thebody = self.get_requestdata_res(casename=casename, theheader=theheader)
        # 断言：请求成功则继续后续操作；请求失败，打印出失败的status_code
        assert res.status_code == 200, savelog.error(f'请求失败：{res.status_code}')
        themessage = res.json()
        # 将返回报文追加到文档备份
        with open(messagefile, 'a', encoding='utf-8') as f:
            savelog.info(f'将用例[{casename}]操作接口[{apiname}]的响应信息写入到:{messagefile}')
            f.write('\n\n\n\n返回报文：\n')
            json.dump(themessage, f, indent=4, ensure_ascii=False)

        statuscode = themessage.get('status', {}).get('statuscode', '')
        # 断言：如果可以获取到请求的statuscode，则继续后续操作；否则，打印出具体的信息
        assert statuscode, savelog.error(themessage)
        return statuscode, themessage, thebody




if __name__ == "__main__":
    grm = GetResponseMysql()
    aa = grm.check_api_rightmsg('002001_head1__正常参数_数据验证SQL','1')
    print(aa)





