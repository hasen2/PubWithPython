# @Time: 2019/12/9 17:11
# @User: Win-lhy
# @IDE: PyCharm
# @Author: lhy
# @File: MysqlGetData.py

import datetime
import re
import random

from publib.database.ConnectToMysql import ConnectToMysql
from publib.savedata.savelogs.SaveLog import SaveLog

savelog = SaveLog().save_log()

class MysqlGetData:
    def __init__(self):
        pass

    def get_data_from_mysql(self,sqllist):
        cm = ConnectToMysql()
        cm.connect_mysql('本地')
        return cm.get_datas(sqllist)

    def change_value(self, thevalue):
        """
        对thevalue进行转换
        :param thevalue: 字段值
        :return: 转换后的字段值
        """
        nowtime = datetime.datetime.now()
        if thevalue.upper() == 'NOWDATA':
            thevalue = nowtime.strftime('%Y%m%d')
        elif thevalue.upper() == 'NOWTIME':
            thevalue = nowtime.strftime('%H%M%S')
        elif thevalue.upper() == 'NOWDATETIME':
            thevalue = nowtime.strftime('%Y%m%d%H%M%S')
        elif thevalue.upper().startswith('RANDOM'):  # 生成随机数字(默认长度是14）
            findaddlen = re.search(r'RANDOM(\d+)', thevalue, re.I)
            addlen = int(findaddlen.group(1)) if findaddlen else 0
            nowtime = datetime.datetime.now()
            nowtimestr = nowtime.strftime('%Y%m%d%H%M%S')
            savelog.debug(f'本次生成的随机数长度为：{14+addlen}')
            thevalue = nowtimestr + str(random.randint(0, 9)) * addlen
        else:
            pass
        return thevalue

    def save_value(self, type, thedata, thekey, thevalue):
        """
        将数据存储到相应的结构数据中，根据thevalue的不同，对数据进行处理
        :param type: 变量类型
        :param thedata: 变量名
        :param thekey: 字段名
        :param thevalue: 字段内容
        :return:
        """
        if not thekey:  # 如果字段值thekey不存在，则不作任何操作，直接返回
            return
        if not isinstance(thevalue, list) and not isinstance(thevalue, dict):
          thevalue = self.change_value(thevalue)
        if type == 'DICT':
            thedata[thekey]=thevalue
        elif type == 'LIST':
            thedata.append(thevalue)
        return

    def set_data(self,alldata,testcasename,apiname,type='DICT'):
        """
        根据字段的不同，将数据进行层层封装
        :param alldata:查询出的数据
        :param testcasename: 案例名
        :param apiname:接口名
        :param type:数据类型，根据此类型查询不同的表
        :return:封装好的数据
        """
        def temp_get_handle_data(upperkey, inputtype='DICT'):
            """
            临时表，简化后续代码
            :param upperkey: 上一层的字段名
            :param inputtype: 数据类型，根据此类型查询不同的表
            :return: 返回从中间表中查询出的结果值
            """
            return self.get_handle_data(testcasename=testcasename, apiname=apiname, upperkey=upperkey, type=inputtype)

        def temp_search_data(thedata,alldata):
            for onerow in alldata:
                thekey = onerow[0]
                thevalue = onerow[1]
                if thevalue.startswith('DICT'):
                    wantdata = temp_get_handle_data(upperkey=thekey, inputtype='DICT')
                    thevalue = self.set_data(alldata=wantdata, testcasename=testcasename, apiname=apiname, type='DICT')
                elif thevalue.startswith('LIST'):
                    wantdata = temp_get_handle_data(upperkey=thekey, inputtype='LIST')
                    thevalue = self.set_data(alldata=wantdata, testcasename=testcasename, apiname=apiname, type='LIST')
                else:
                    thevalue = thevalue if thevalue else ""
                self.save_value(type=type, thedata=thedata, thekey=thekey, thevalue=thevalue)
            return

        savelog.debug(f'{type}:{alldata}')
        if type == 'DICT':  # 处理dict类型的数据
            thedata = {}
            temp_search_data(thedata=thedata, alldata=alldata)
        elif type == 'LIST':  # 处理list类型的数据
            thedata = []
            temp_search_data(thedata=thedata, alldata=alldata)
        else:
            thedata = ""

        return thedata


    def get_handle_data(self,testcasename,apiname,upperkey,type='DICT'):
        """
        从中间表查询dict或list的数据
        :param testcasename: 案例名
        :param apiname: 接口名
        :param upperkey: 上一层的字段名
        :param type: 数据类型，根据此类型查询不同的表
        :return:
        """
        if type == 'DICT':
            sqllist = [{'查询字典数据':f'''select thdd.NowKey,thdd.NowValue
                        from tb_handle_dict_data thdd
                        where thdd.TestCaseName='{testcasename}'
                        and thdd.ApiName = '{apiname}'
                        and thdd.upperkey = '{upperkey}';'''}]
            wantdata = self.get_data_from_mysql(sqllist)
        else:
            sqllist = [{'查询列表数据': f'''select thld.NowKey,thld.NowValue
                                from tb_handle_list_data thld
                                where thld.TestCaseName='{testcasename}'
                                and thld.ApiName = '{apiname}'
                                and thld.upperkey = '{upperkey}'
                                order by thld.nowkeysort;'''}]
            wantdata = self.get_data_from_mysql(sqllist)
        return wantdata


    def get_apiname(self,testcasename):
        getapisqllist = [{'查询用例对应的接口':f'''select apiname
                            from tb_test_case ttc
                            where ttc.TestCaseName='{testcasename}';'''}]
        theapinames = self.get_data_from_mysql(getapisqllist)
        theapiname = theapinames[0][0] if len(theapinames) == 1 else False
        assert theapiname, savelog.error(f'未查到案例[{testcasename}]对应的接口名称')
        return theapiname

    def get_url(self, apiname='002001', hostname='ZNTESTHOST'):
        """
        根据接口名和路由，获取并返回接口请求所需要的url地址
        :param apiname: 接口名（用户获取url）
        :param hostname: 路由名，用于获取ip
        :return: 返回拼接后的url
        """

        thehost = ''
        gethostsqllist = [{'查询host': f'''select tph.HostValue,tph.HostPost
                            from tb_pub_host tph
                            where tph.HostName='{hostname}';'''}]
        thehosts = self.get_data_from_mysql(gethostsqllist)
        for host in thehosts:
            thehost = host[0] + ':' + host[1] if host[1] else host[0]
            if thehost:
                break
            else:
                assert 0 == 1, savelog.error(f'未查询到[{hostname}]对应的host数据')

        theurl = ''
        geturlsqllist = [{'查询url': f'''select tau.api_url,tau.API_PARAMS
                            from tb_api_url tau
                            where tau.API_NAME='{apiname}';'''}]
        theurls = self.get_data_from_mysql(geturlsqllist)
        for url in theurls:
            theurl = url[0] + '?' + url[1]
            if theurl:
                break
            else:
                assert 0 == 1, savelog.error(f'未查询到[{apiname}]对应的url数据')
        return thehost+theurl


    def get_header(self, headertype='header001'):
        sqllist = [{'查询header':f'''select tph.headerkey,tph.headervalue
                    from tb_pub_header tph
                    where tph.HeaderClassType='{headertype}';'''}]
        theheaders = self.get_data_from_mysql(sqllist)
        theheader = self.set_data(theheaders, headertype, 'header')
        return theheader

    def get_head_type(self,testcasename):
        typesqllist = [{'查询header和head的类型': f'''select tabb.HeaderClassType,tabb.HeadClassType
                        from tb_api_body_body tabb
                        where tabb.TestCaseName='{testcasename}'
                        limit 1;'''}]
        thetypes = self.get_data_from_mysql(typesqllist)
        thetype = thetypes[0] if len(thetypes) == 1 else (False, False)
        savelog.debug(f'thetype:{thetype}')
        assert len(thetype) == 2, savelog.error(f'未查到案例[{testcasename}]对应的公共header和公共head')
        return thetype

    def get_body_head(self, headtype='head001'):
        sqllist = [{'查询body-head': f'''select tpbh.headkey,tpbh.headvalue
                    from tb_pub_body_head tpbh
                    where tpbh.headclasstype='{headtype}';'''}]
        thebodyheads = self.get_data_from_mysql(sqllist)
        thebodyhead = self.set_data(thebodyheads, headtype, 'head')
        return thebodyhead

    def get_body_body(self,testcasename,apiname):
        sqllist = [{'查询body-body': f'''select tabb.BodyKey,tabb.BodyValue
                    from tb_api_body_body tabb
                    where tabb.TestCaseName='{testcasename}'
                    and tabb.ApiName='{apiname}';'''}]
        thebodybodys = self.get_data_from_mysql(sqllist)
        thebodybody = self.set_data(thebodybodys, testcasename, apiname)
        return thebodybody

    def get_checkdata(self, testcasename):
        expectdatasqllist = [{'查询预期结果':f'''select ter.ExpectCode,ter.ExpectText
                                from tb_test_case ttc
                                inner join tb_expect_result ter on ttc.ExpectResult=ter.id
                                where ttc.TestCaseName='{testcasename}';
                                '''}]
        expectdatas = self.get_data_from_mysql(expectdatasqllist)
        theexpectdata = expectdatas[0] if len(expectdatas) == 1 else (False, False)
        savelog.debug(f'theexpectdata:{theexpectdata}')
        assert len(theexpectdata) == 2, savelog.error(f'未查到案例[{testcasename}]对应的预期内容[{expectdatas}]')
        return theexpectdata




if __name__ == '__main__':
    gdfm = MysqlGetData()
    theheader = gdfm.get_header()
    the_body_head = gdfm.get_body_head('head001')
    the_body_body = gdfm.get_body_body('002001_正常参数_数据验证','002001')
    # theurl = gdfm.get_url()
    theapi = gdfm.get_apiname('002001_正常参数_数据验证')
    get_checkdata = gdfm.get_checkdata('002001_正常参数_数据验证')
    print(theheader)
    print(the_body_head)
    print(the_body_body)
    print(theapi)
    print(get_checkdata)
