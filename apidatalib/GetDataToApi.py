# @Time: 2019/11/24 11:07 PM
# @User: Mac-lhy
# @IDE: PyCharm
# @Author: lhy
# @File: GetDataToApi.py

import datetime

import config.baseconfig as config
from publib.excellib.ExcelGetDatas import ExcelGetDatas
from publib.pubdef.AssertMsg import AssertMsg as AM
from publib.database.ConnectDb2 import ConnectDb2
from publib.savedata.savelogs.SaveLog import SaveLog

savelog = SaveLog().save_log()

class GetDataToApi:
    def __init__(self):
        self.am = AM()
        self.cndb = ConnectDb2()

    def get_excel_sheet_data(self, filename, sheetname):
        """
        从excel获取指定sheet的内容
        :param str类型，filename: 文件名（文件路径从配置文件获取）
        :param str类型，sheetname: sheet名
        :return: 返回一个list，第一个元素=1时，第二个元素为获取到的信息，第二个元素=0时，第二个元素为错误提示信息
        """
        errorresult = config.get_excel_errornotice(filename, sheetname)
        getexceldata = ExcelGetDatas(config.get_fileaddr(filename))
        exceldata = getexceldata.get_info(searchsheetname=sheetname)
        if exceldata:
            sheetdata = exceldata.get(sheetname, '')
            if not sheetdata:
                return errorresult
            else:
                return [1, sheetdata]
        else:
            return errorresult

    def get_wanted(self, thetype, thestring, temp, rownum=None, wantrownum=1, lhytype=1, upstr=None):
        """
        辅助get_excel_dict函数，完成数据的重构
        :param thetype: 当前单元格字段的类型，char，String，Object，ArrayList
        :param thestring:当前单元格内容
        :param temp:临时变量，用于记录当前单元格所属对象
        :param rownum:当前单元格所处的行数（从0开始）
        :param wantrownum:用例数据对应的行数（从0开始）
        :param lhytype:特殊字符，=1时表示需要根据thetype在temp中新增对象，=0时表示从temp中取出对应的对象
        :param upstr:当前单元格的上层内容
        :return:返回在temp中新增或取到的对象，以及当前单元格的内容
        """
        savelog.debug([thetype, thestring, temp, rownum, wantrownum, lhytype, upstr])
        if isinstance(temp, list):
            if thetype == 'Object':
                if lhytype:
                    temp.append({})
                temp = temp[-1]
            elif thetype == 'ArrayList':
                if lhytype:
                    temp.append([])
                temp = temp[-1]
            # elif thetype in ['String','char','integer']:
            else:
                if rownum == wantrownum:
                    thestring = float(thestring) if thetype == 'Decimal' else thestring
                    temp.append(thestring)
        elif isinstance(temp, dict):
            if thetype == 'Object':
                if lhytype:
                    temp[thestring] = {}
                temp = temp[thestring]
            elif thetype == 'ArrayList':
                if lhytype:
                    temp[thestring] = []
                temp = temp[thestring]
            # elif thetype in ['String','char','integer']:
            else:
                if rownum == wantrownum:
                    thestring = float(thestring) if thetype == 'Decimal' else thestring
                    temp[upstr] = thestring
                else:
                    temp[thestring] = ""

        return temp, thestring

    def get_excel_dict(self, filename, sheetname, casename, **kg):
        """
        读取excel文件，并返回一个dict类型的数据，用于从excel中获取header和body结构及数据
        :param filename: str类型，文件名（文件路径从配置文件获取）
        :param sheetname: str类型，sheet名
        :param casename: str类型，对应的测试用例
        :param kg: dict类型，额外补充的参数
        :return: 返回一个list，第一个元素=1时，第二个元素为获取到的信息，第一个元素=0时，第二个元素为错误提示信息
        """
        if sheetname == 'head':
            if '__' in casename:
                casename = casename.split('__')[0]

        errorresult = config.get_excel_errornotice(filename, sheetname, casename)
        sheetdatalist = self.get_excel_sheet_data(filename, sheetname)
        if not sheetdatalist[0]:
            return sheetdatalist
        else:
            sheetdata = sheetdatalist[1]
            rownums = len(sheetdata)
            colnums = len(sheetdata[0])
            typerownum, wantrownum, level1rownum, endrownum = [0] * 4

            # 获取基本参数（数据类型的行数，实际数据的行数，第一层级的行数，分割行（testcasename)的行数)
            for rownum in range(rownums):
                nowdata = sheetdata[rownum][0]
                if nowdata == 'type':
                    typerownum = rownum
                elif nowdata == casename:
                    wantrownum = rownum
                elif nowdata == 'level1':
                    level1rownum = rownum
                elif nowdata == 'testcasename':
                    endrownum = rownum
            if typerownum and wantrownum and level1rownum and endrownum:
                pass
            else:
                return errorresult

            wantdict = {}  # 最终所需要的数据
            typedict = {}  # 临时数据，存储每行的类型及字段值，当单元格为空时，如果在typedict中可以查到对应的数据，则直接调用

            # 循环每一列数据
            for colnum in range(1, colnums):
                nowtype = sheetdata[typerownum][colnum]
                wantedata = sheetdata[wantrownum][colnum]
                tempdict = wantdict  # 临时内容，根据单元格的位置取出对应的内容，然后将单元格的内容适当的放入其中
                upstr = ''  # 存储当列上一行的数据（有可能是取的前一列的上一行数据）
                lastrowdata = ''  # 定义本行上方的数据（仅查询level1到testcasename之间的数据）
                for rownum in (list(range(typerownum + 1, endrownum)) + [wantrownum]):  # 循环每一行数据
                    nowstring = sheetdata[rownum][colnum]
                    lhytype = 1  # =1时，默认新建或新增，dict，list，string等
                    if wantedata:  # 用例行有数据，插入数据
                        if nowstring:
                            thetype = nowtype
                            thestring = nowstring
                            lastrowdata = nowstring
                        else:
                            lhytype = 0
                            if lastrowdata:  # 本行上方已有数据，则直接跳过，继续执行下一行
                                continue
                            leveltypedata = typedict.get(sheetdata[rownum][0], '')
                            if leveltypedata:
                                thetype, thestring = leveltypedata
                            else:
                                continue
                    else:  # 用例行无数据，创建数据结构
                        if nowstring:
                            if rownum == level1rownum:
                                typedict = {}

                            typedict[sheetdata[rownum][0]] = [nowtype, nowstring]
                            thetype, thestring = nowtype, nowstring
                        else:  # 当前行无值
                            # 当前行的下一行到testcasename行，是否有数据，如有数据，则继续执行，如无数据，则直接退出当前列，开始下一列
                            if ''.join(map(lambda lhyrownum: sheetdata[lhyrownum][colnum],
                                           list(range(rownum + 1, endrownum)))):
                                lhytype = 0
                                leveltypedata = typedict.get(sheetdata[rownum][0], '')
                                if leveltypedata:
                                    thetype, thestring = leveltypedata
                                else:
                                    typedict[sheetdata[rownum][0]] = [nowtype, nowstring]
                                    thetype, thestring = nowtype, nowstring
                            else:
                                break
                    # 针对部分变量，采取动态的方式获取具体的值
                    nowdatetime = datetime.datetime.now()
                    if thestring == 'nowdate':
                        thestring = nowdatetime.strftime('%Y%m%d')
                    elif thestring == 'nowtime':
                        thestring = nowdatetime.strftime('%H%M%S')
                    elif thestring == 'nowdatetime':
                        thestring = nowdatetime.strftime('%Y%m%d%H%M%S')
                    elif thestring.startswith('PUB'):  # 字段值如果是PUB开头，则从公共变量中取值
                        thestring = config.PUBINFO[thestring]
                    else:
                        pass

                    tempdict, upstr = self.get_wanted(thetype, thestring, temp=tempdict,
                                                      rownum=rownum, wantrownum=wantrownum, lhytype=lhytype,
                                                      upstr=upstr)

        wantdict.update(kg)
        savelog.debug(wantdict)
        return [1, wantdict]

    def get_excel_url(self, filename, sheetname, host=None, source=None):
        """
        读取excel文件，返回一个url链接
        :param filename: str类型，文件名（文件路径从配置文件获取）
        :param sheetname: str类型，sheet名
        :param host: 主动传入的路由地址
        :param source: 主动传入的接口地址
        :return: 返回一个list，第一个元素=1时，第二个元素为获取到的信息，第一个元素=0时，第二个元素为错误提示信息
        """
        errorresult = config.get_excel_errornotice(filename, sheetname)
        sheetdatalist = self.get_excel_sheet_data(filename, sheetname)
        if not sheetdatalist[0]:
            return sheetdatalist
        else:
            sheetdata = sheetdatalist[1]
            host0, source0 = ['', '']
            for rowdata in sheetdata:
                if len(rowdata) > 1:
                    if rowdata[0] == '路由':
                        host0 = rowdata[1]
                    elif rowdata[0] == '接口':
                        source0 = rowdata[1]
                    if host0 and source0:
                        break
            wanthost = host if host else host0
            wantsource = source if source else source0
            if wanthost and wantsource:
                return [1, ''.join([wanthost, wantsource])]
            else:
                return errorresult

    def get_expect_data(self, filename='测试案例.xls', sheetname=None, casename=None, databasename='db99',justreturncolnum=0):
        """

        :param filename:
        :param sheetname:
        :param casename:
        :return:
        """
        errorresult = config.get_excel_errornotice(filename, sheetname, casename)
        sheetdatalist = self.get_excel_sheet_data(filename, sheetname)
        if not sheetdatalist[0]:
            return sheetdatalist
        else:
            sheetdata = sheetdatalist[1]
            rownums = len(sheetdata)
            colnums = len(sheetdata[0])
            checkmsgcolnum,checkcodecolnum,resultrownum,resultcolnum = 0, 0, 0, 0
            expectdata = ''
            expectcheckcode = ''
            # 查找预期数据的列号
            for colnum in range(colnums):
                nowdata = sheetdata[0][colnum]
                if nowdata == '预期结果':
                    checkmsgcolnum = colnum
                elif nowdata == '预期code':
                    checkcodecolnum = colnum
                elif nowdata == '执行结果':
                    resultcolnum = colnum

            # 根据用例名，查找预期数据
            for rownum in range(rownums):
                nowdata = sheetdata[rownum][0]
                if nowdata == casename:
                    resultrownum = rownum
                    expectcheckcode = sheetdata[rownum][checkcodecolnum]
                    expectdata = sheetdata[rownum][checkmsgcolnum]
                    break
            if checkmsgcolnum and checkcodecolnum and resultrownum and resultcolnum:
                if justreturncolnum:
                    return resultrownum, resultcolnum
                if expectdata.startswith('SQL'):
                    expectsql = expectdata.replace('SQL', '')
                    expectdatadict = self.cndb.get_db2_data(expectsql, dbbasename=databasename)
                    expectdata = self.cndb.filterdict(expectdatadict)
                    print(expectdata)
                return expectcheckcode, expectdata, resultrownum, resultcolnum
            else:
                self.am.assertlist1(errorresult)



if __name__ == "__main__":
    pass