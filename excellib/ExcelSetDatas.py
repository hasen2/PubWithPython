# 修改excel中的数据

from xlutils import copy
import xlrd
import datetime

from publib.excellib.ExcelStyle import ExcelStyle

class ExcelSetDatas():
    def __init__(self, exceladdress):
        """
        打开一个表格并修改其内容（原理：复制一个新的表格，然后修改内容。原表格的格式会被取消）
        :param exceladdress: 原表格的地址
        """
        self.excelpath =exceladdress
        self.rbook = xlrd.open_workbook(self.excelpath,formatting_info=True)  # 打开文件
        self.wbook = copy.copy(self.rbook)  # 复制文件并保留格式

    def set_datas(self, rowindex, colindex, value, sheetid=0, sheetname=None, style=None):
        """
        写入（修改）数据
        :param rowindex: 行数下标（从0开始）
        :param colindex: 列数下标（从0开始）
        :param value: 要写入的数据
        :param sheetid: sheet页下标（从0开始）
        :param sheetname: 如果sheetname有值，则根据sheetname查询计算sheetid
        :param style: 插入的数据是否需要带格式，默认不带
        :return:
        """
        if sheetname:
            sheetid = self.wbook.sheet_index(sheetname)  # 根据sheetname获取sheetid
        w_sheet = self.wbook.get_sheet(sheetid)  # 定位sheet页
        if style:
            w_sheet.write(rowindex, colindex, value, style)
        else:
            w_sheet.write(rowindex, colindex, value)

        self.close_workbook()

    def close_workbook(self):
        """
        保存修改后的excel表格
        :return:
        """
        self.wbook.save(self.excelpath)  # 保存文件

    def save_testcase_status(self, rownum, colnum, postname,type=0, colour=0):
        estyle = ExcelStyle()
        style0 = estyle.style_new()  # 初始化
        estyle.style_frame(style0)  # 边框
        estyle.style_font(style0, colour=colour)  # 字体 0黑色，2红色

        valuestr = '通过' if type else '未通过'
        self.set_datas(rownum, colnum, valuestr, postname, style=style0)
        self.set_datas(rownum, colnum+1, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), postname, style=style0)

if __name__ == '__main__':
    exceladdress = r'C:\Users\admin\Desktop\test.xls'

    a = ExcelSetDatas(exceladdress)

    # a.set_datas(4, 1, '刘怀d远', sheetid=1)
    a.set_datas(4, 1, '刘怀d远111', sheetname='测试')
