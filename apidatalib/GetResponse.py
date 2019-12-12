# @Time: 2019/11/24 9:06 PM
# @User: Mac-lhy
# @IDE: PyCharm
# @Author: lhy
# @File: GetResponse.py

import os
import json
import requests
import datetime

import config.baseconfig as config
from publib.apidatalib.GetDataToApi import GetDataToApi as GDTA
from publib.pubdef.AssertMsg import AssertMsg as AM
from publib.excellib.ExcelSetDatas import ExcelSetDatas
from publib.savedata.savelogs.SaveLog import SaveLog

savelog = SaveLog().save_log()

class GetResponse:
    def __init__(self):
        self.gdta = GDTA()
        self.am = AM()
        self.esd = ExcelSetDatas(config.get_fileaddr())

    def get_requestdata_res(self, postname, casename, bodyfilename='请求报文体.xls', code='utf-8', host=None, headerdict=None):
        """
        调取接口并返回接口返回的原始内容
        :param postname: 接口名
        :param casename: 用例名
        :param bodyfilename: 报文体文件名，默认'请求报文体.xls'
        :param code: 字符编码，默认为'utf-8'
        :param host: host地址，默认从excel中取值
        :return:接口请求内容
        """

        messagedir = os.path.join(config.DATADIR, 'MyMessage', casename)
        if not os.path.exists(messagedir):
            savelog.info(f'新建目录{messagedir}')
            os.makedirs(messagedir)
        messagefile = os.path.join(messagedir, postname + '.txt')
        # 获取url
        theurl = self.am.assertlist1(self.gdta.get_excel_url(bodyfilename, postname, host=host))
        savelog.info(f'用例[{casename}]操作接口[{postname}]的URL:{theurl}')

        # 获取header
        if headerdict:
            pass
        else:
            headerdict = {"clientId": "pressureTest"}
        savelog.info(f'用例[{casename}]操作接口[{postname}]的请求头:{headerdict}')

        # 获取body
        thehead = self.am.assertlist1(self.gdta.get_excel_dict(bodyfilename, 'head', casename))
        thebody = self.am.assertlist1(self.gdta.get_excel_dict(bodyfilename, postname, casename))
        bodydict = {"head": thehead, "body": thebody}
        savelog.info(f'用例[{casename}]操作接口[{postname}]的请求体:{bodydict}')

        # 将请求报文写入到文档备份
        with open(messagefile, 'w', encoding='utf-8') as f:
            savelog.info(f'将用例[{casename}]操作接口[{postname}]的请求信息写入到:{messagefile}')
            f.write(f'{datetime.datetime.now()}\n\n请求URL：\n{theurl}')
            f.write('\n\n请求头：\n')
            json.dump(headerdict, f, indent=4, ensure_ascii=False)
            f.write('\n\n请求体：\n')
            json.dump(bodydict, f, indent=4, ensure_ascii=False)
            savelog.debug(f'用例[{casename}]操作接口[{postname}]的请求报文json:{json.dumps(bodydict)}')
        try:
            savelog.info(f'用例[{casename}]开始请求接口：{postname}_start')
            # 发起请求
            req = requests.post(url=theurl, headers=headerdict, data=json.dumps(bodydict))
            savelog.info(f'用例[{casename}]结束请求接口：{postname}_end')
            # 转码
            req.encoding = code
            return req, messagefile
        except Exception as b:
            assert 0, savelog.critical(f'用例[{casename}]操作接口[{postname}]-->请求失败:{b}')

    def get_response(self, postname, casename, host=None, headerdict=None):
        """
        请求接口，校验相关信息，并返回对应的内容，
        :param postname: 接口名，eg:002001
        :param casename: 用例名
        :param host: 端口
        :param headerdict: 请求头
        :return: 返回请求成功后的数据
        """
        # 用例开始执行时间
        rownum, colnum = self.gdta.get_expect_data(sheetname=postname, casename=casename, justreturncolnum=1)
        self.esd.save_testcase_status(rownum, colnum, postname, colour=2)
        # 调用接口数据
        res, messagefile = self.get_requestdata_res(postname=postname, casename=casename, host=host, headerdict=headerdict)
        # 断言：请求成功则继续后续操作；请求失败，打印出失败的status_code
        assert res.status_code == 200, savelog.error(f'请求失败：{res.status_code}')
        themessage = res.json()
        # 将返回报文追加到文档备份
        with open(messagefile, 'a', encoding='utf-8') as f:
            savelog.info(f'将用例[{casename}]操作接口[{postname}]的响应信息写入到:{messagefile}')
            f.write('\n\n\n\n返回报文：\n')
            json.dump(themessage, f, indent=4, ensure_ascii=False)

        statuscode = themessage.get('status', {}).get('statuscode', '')
        # 断言：如果可以获取到请求的statuscode，则继续后续操作；否则，打印出具体的信息
        assert statuscode, savelog.error(themessage)
        return statuscode, themessage


    def check_api_wrongmsg(self, postname, casename, host=None, headerdict=None,check='0', databasename='db99'):
        """
        验证请求参数错误时，相关提示信息是否正确
        :param postname: 接口名，eg:002001
        :param casename: 用例名
        :param host: 端口
        :param headerdict: 请求头
        :param check: 校验标志，=1只验证code，=2只验证提示信息，=3验证code验证提示信息
        :return:
        """
        statuscode,themessage = self.get_response(postname=postname, casename=casename, host=host, headerdict=headerdict)
        assert statuscode != '01', savelog.error(f'预期内容：!=01；实际内容：{statuscode}')
        statusmessage = themessage['status']['statusmessage']
        checkcode, checkmsg, rownum, colnum = self.gdta.get_expect_data(sheetname=postname, casename=casename, databasename=databasename)  # 从测试用例中，获取预期数据
        checkmsg = json.loads(checkmsg) if ('{' in checkmsg or '[' in checkmsg) else checkmsg
        savelog.debug(f'请求得到的数据：{statusmessage}')
        savelog.debug(f'从excel中得到的数据：{checkmsg}')

        def check_code():
            savelog.info(f'待验证内容：{checkcode}')
            assert statuscode == checkcode, savelog.error(f'预期内容：{checkcode}；实际内容：{statuscode}')

        def check_msg():
            assert checkmsg, savelog.error(f'未传入预期的错误提示信息：{checkmsg}')
            if isinstance(checkmsg, str):
                savelog.info(f'待验证内容：{checkmsg}')
                assert checkmsg in statusmessage, savelog.error(f'预期内容：{checkmsg}；实际内容：{statusmessage}')
            elif isinstance(checkmsg, list):
                for errormsgone in checkmsg:
                    savelog.info(f'待验证内容：{errormsgone}')
                    assert errormsgone in statusmessage, savelog.error(f'预期内容：{checkmsg}；实际内容：{statusmessage}')
        if check == '1':  # 验证checkcode是否正确
            check_code()
        elif check == '2':  # 验证提示信息是否正确
            check_msg()
        else:  # 验证checkcode是否正确，验证提示信息是否正确
            check_code()
            check_msg()
        savelog.info(f'用例[{casename}]对接口[{postname}]的错误提示信息的验证，测试通过！')
        self.esd.save_testcase_status(rownum, colnum, postname, type=1)

    def check_api_rightmsg(self, postname, casename, host=None, headerdict=None, check='0', databasename='db99'):
        """
        验证请求正确时，返回的信息是否正确
        :param postname: 接口名，eg:002001
        :param casename: 用例名
        :param host: 端口
        :param headerdict: 请求头
        :param check: 校验标志，默认不校验并返回获取的结果内容，=1时校验相关信息是否正确
        :return:
        """

        statuscode, themessage = self.get_response(postname=postname, casename=casename, host=host,
                                                    headerdict=headerdict)
        assert statuscode == '01', savelog.error(f'预期内容：01；实际内容：{statuscode}')
        resultmessage = themessage['result']
        checkcode, checkmsg, rownum, colnum = self.gdta.get_expect_data(sheetname=postname, casename=casename, databasename=databasename)  # 从测试用例中，获取预期数据
        checkmsg = json.loads(checkmsg) if ('{' in checkmsg or '[' in checkmsg) else checkmsg
        savelog.debug(f'实际获取到的内容：{resultmessage}')
        savelog.debug(f'需校验的内容：{checkmsg}')

        def check_code():
            savelog.info(f'待验证内容：{checkcode}')
            assert statuscode == checkcode, savelog.error(f'预期内容：{checkcode}；实际内容：{statuscode}')
        def check_msg():
            for checkkey, checkvalue in checkmsg.items():
                savelog.info(f'待验证内容：{checkkey}:{checkvalue}')
                assertlist = [checkvalue, resultmessage.get(checkkey, '实际结果无值')]
                self.am.assertlist2(assertlist)

        if check == '1':  # 验证返回信息是否正确
            check_code()
            check_msg()
            savelog.info(f'用例[{casename}]对接口[{postname}]的返回信息的验证，测试通过！')
            self.esd.save_testcase_status(rownum, colnum, postname, type=1)
        else:  # 不验证，直接返回获得的结果信息
            resultmessage = themessage['result']
            return resultmessage






if __name__ == "__main__":
    pass






