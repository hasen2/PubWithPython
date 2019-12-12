# @Time: 2019/12/12 12:56
# @User: Win-lhy
# @IDE: PyCharm
# @Author: lhy
# @File: GetDataFromXML.py

import datetime
from xml.dom.minidom import parse



class GetDataFromXML:
    def __init__(self):
        pass

    def get_xml_info(self,xmlfile):
        domTree = parse(xmlfile)
        # 获取根节点
        rootNode = domTree.documentElement
        return rootNode

    def get_testcase_execute(self, xmlfile):
        """
        根据执行结果XML文件，查找每个用例的执行情况
        :param xmlfile: XML文件
        :return:
        """

        wantdict = {}
        # 找到xml文件的根节点
        domtree = self.get_xml_info(xmlfile=xmlfile)
        # 查询出每个用例
        testcases = domtree.getElementsByTagName('test')
        if not testcases:
            return wantdict
        for testcase in testcases:
            # 用例名
            testcaseName = testcase.getAttribute("name")
            # 执行结果
            testcasestatus = testcase.getElementsByTagName('status')[-1]
            testcaseResult = testcasestatus.getAttribute("status")
            # 失败原因
            testcaseReason = ''
            if testcaseResult == 'PASS':
                pass
            else:
                msgs = testcase.getElementsByTagName('msg')
                for msg in msgs:
                    if msg.getAttribute("level") in ('ERROR', 'FAIL'):
                        testcaseReason += (' | ' + msg.firstChild.data)
            # 开始时间
            testcaseStarttime = testcasestatus.getAttribute("starttime")
            Starttime = datetime.datetime.strptime(testcaseStarttime, "%Y%m%d %H:%M:%S.%f")
            # 结束时间
            testcaseEndtime = testcasestatus.getAttribute("endtime")
            Endtime = datetime.datetime.strptime(testcaseEndtime, "%Y%m%d %H:%M:%S.%f")
            # 总耗时
            usertime = (Endtime - Starttime).total_seconds()

            wantdict[testcaseName] = [testcaseResult, testcaseReason, str(usertime)]

        return wantdict


    def get_testcase_result(self, xmlfile):
        """
        测试执行结果XML文件
        :param xmlfile: XML文件
        :return: (总用例数，通过用例数，失败用例数)
        """
        # 找到xml文件的根节点
        domtree = self.get_xml_info(xmlfile=xmlfile)
        # 查询总结果
        totals = domtree.getElementsByTagName('total')
        if not totals:
            return 0, 0, 0
        total = totals[-1]
        stat = total.getElementsByTagName('stat')[-1]
        passnum = int(stat.getAttribute("pass"))
        failnum = int(stat.getAttribute("fail"))
        allnum = passnum + failnum
        return allnum, passnum, failnum


if __name__ == '__main__':
    aa = GetDataFromXML()
    filename = r'E:\learn\apitest\myreport\output.xml'
    cc = aa.get_testcase_execute(filename)
    print(cc)
