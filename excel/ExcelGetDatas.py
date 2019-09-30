# 获取excel数据

import xlrd,pprint,datetime

class ExcelGetDatas():
    def __init__(self,exceladdress=r'C:\Users\admin\Desktop\test.xls'):
        """
        打开工作表格，获取及统计相关信息
        :param exceladdress:
        """
        self.exceladdress= exceladdress
        self.workbook = xlrd.open_workbook(self.exceladdress)
        self.sheetnamelist = self.workbook.sheet_names()

    def set_type(self,ctype,cellvalue):
        """
        格式处理
        :param ctype: 单元格类型，#  0. empty（空的）,1 string（text）, 2 number, 3 date, 4 boolean, 5 error， 6 blank（空白表格）
        :param cellvalue: 单元格内容
        :return: 返回转码后的单元格内容
        """
        if ctype == 2 and cellvalue % 1 == 0:  # 如果是整形
            cellvalue = int(cellvalue)
        elif ctype == 3:  # =3 为时间格式，转成datetime对象后再转化为字符串格式
            # cellvalue = xlrd.xldate.xldate_as_datetime(cellvalue, 0)  # 0代表以1900-01-01为基准，1代表以1904-01-01为基准
            # cellvalue = cellvalue.strftime('%Y-%m-%d')
            cellvalue = xlrd.xldate.xldate_as_datetime(cellvalue, 0).__str__()  # 0代表以1900-01-01为基准，1代表以1904-01-01为基准
        elif ctype == 4:
            cellvalue = True if cellvalue == 1 else False
        return cellvalue

    def get_info2(self,searchsheetname=None):
        """
        获取所打开excel文件的所有内容
        :param searchsheetname: 如果传入了需要获取内容的sheetname则只获取单个sheet的内容,如果未传值，则获取整个excel的内容
        :return: 以字典形式存储，key为sheet的名字，value为每个sheet的内容（列表格式）
        """
        """
        获取所打开excel文件的所有内容
        :return: 所有内容，以字典形式存储，key为sheet的名字，value为每个sheet的内容（列表格式）
        """
        allinfosdict = {}  # 存储本文件的所有内容
        for sheetname in self.sheetnamelist:
            allinfoslist = []  # 存储本sheet页的内容
            if searchsheetname and searchsheetname!=sheetname:
                continue
            sheet = self.workbook.sheet_by_name(sheetname)
            rowsnum = sheet.nrows # 本sheet页行数
            colsnum = sheet.ncols # 本sheet页列数
            for rownum in range(rowsnum):
                rowinfolist = [] # 存储本行数据
                for colnum in range(colsnum):
                    ctype = sheet.cell(rownum, colnum).ctype
                    cellvalue = sheet.cell_value(rownum, colnum)
                    # 根据不同的数据类型，处理数据
                    cellvalue = self.set_type(ctype,cellvalue)

                    # 存储每一行的数据
                    rowinfolist.append(cellvalue)
                # 存储每一个sheet的数据
                allinfoslist.append(rowinfolist)
            # 存储整个文件的数据
            allinfosdict[sheetname] = allinfoslist
        print(allinfosdict)

        return allinfosdict




if __name__ == '__main__':
    exceladdress = r'C:\Users\admin\Desktop/test.xls'
    aa1 = ExcelGetDatas(exceladdress)
    bdict = {}
    cc = aa1.get_info2('Sheet1')
    print('-----------------------------')
    print(cc)

