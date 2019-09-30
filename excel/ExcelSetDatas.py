# 修改excel中的数据

from xlutils import copy
import xlrd


class ExcelSetDatas():
    def __init__(self,exceladdress):
        """
        打开一个表格并修改其内容（原理：复制一个新的表格，然后修改内容。原表格的格式会被取消）
        :param exceladdress: 原表格的地址
        """
        self.excelpath =exceladdress
        self.rbook = xlrd.open_workbook(self.excelpath,formatting_info=True)#打开文件
        self.wbook = copy.copy(self.rbook)#复制文件并保留格式

    def set_datas(self,rowindex,colindex,value,sheetid=0):
        """
        写入（修改）数据
        :param rowindex: 行数下标（从0开始）
        :param colindex: 列数下标（从0开始）
        :param value: 要写入的数据
        :param sheetid: sheet页下标（从0开始）
        :return:
        """
        w_sheet = self.wbook.get_sheet(sheetid)  #定位sheet页
        w_sheet.write(rowindex,colindex,value)

    def close_workbook(self):
        """
        保存修改后的excel表格
        :return:
        """
        self.wbook.save(self.excelpath) #保存文件


if __name__ == '__main__':
    exceladdress = r'C:\Users\admin\Desktop\test.xls'

    a = ExcelSetDatas(exceladdress)

    a.set_datas(4,1,'test')
    a.close_workbook()