# 创建excel，并插入数据

import xlwt


class ExcelNewDatas:
    def __init__(self):
        """
        新建一个工作表格，并插入相应的数据
        """
        pass

    def add_excel(self):
        """
        初始化一个excel
        :return: 创建好的excel
        """
        newexcel = xlwt.Workbook(encoding='utf-8')
        return newexcel

    def add_sheet(self, newexcel,sheetname):
        """
        新建一个sheet页
        :param newexcel: 创建好的excel
        :param sheetname: 创建的sheet页名称
        :return:创建好的sheet
        """
        newsheet = newexcel.add_sheet(sheetname,cell_overwrite_ok=True)
        return newsheet

    def add_info(self, newsheet, rownum, colnum, datas,style=None):
        """
        插入数据
        :param newexcel: 创建好的excel
        :param newsheet: 创建好的sheet
        :param rownum: 行数下标（从0开始）
        :param colnum: 列数下标（从0开始）
        :param datas: 要插入的数据
        :param style: 插入的数据是否需要带格式，默认不带
        :return:
        """
        if style:
            newsheet.write(rownum, colnum, datas, style)  # 写入带字体样式的内容
        else:
            newsheet.write(rownum, colnum, datas)  # 写入不带字体样式的内容

    def set_col_width(self,newsheet,num,widthnum=None,rowheight = None):
        """
        设置num列的列宽
        :param newsheet:
        :param num:列数，从0开始
        :param widthnum:# 设置列宽，一个中文等于两个英文等于两个字符，10=5个汉字的宽度
        :param rowheight:# 设置行高，800
        :return:
        """
        if widthnum:
            newsheet.col(num).width = widthnum * 256  # widthnum为字符数，256为衡量单位
        if rowheight:
            newsheet.row(0).height_mismatch = True
            newsheet.row(0).height = rowheight  # 设置行高  800






    def set_merge(self,newsheet,rowbegin=None,rowend=None,colbegin=None,colend=None,datas = None,style=None):
        """
        合并单元格，合并第rowbegin行到第rowend行的第colbegin列到第colend列（无法对第0行和第0列第数据合并）
        :param newsheet:sheet对象
        :param rowbegin:开始行
        :param rowend:结束行
        :param colbegin:开始列
        :param colend:结束列
        :param style:格式
        :return:
        """
        if rowbegin and rowend and colbegin and colend:
            if style:
                if datas:
                    newsheet.write_merge(rowbegin, rowend, colbegin, colend,datas, style)  # 带格式，有数据
                else:
                    newsheet.write_merge(rowbegin, rowend, colbegin, colend, style)  # 带格式，无数据
            else:
                if datas:
                    newsheet.write_merge(rowbegin, rowend, colbegin, colend,datas)  # 无格式，有数据
                else:
                    newsheet.write_merge(rowbegin, rowend, colbegin, colend)  # 无格式，无数据


    def save_excel(self,newexcel,address):
        """
        保存新建的excel表格
        :param newexcel: 创建好的excel
        :param address: 保存路径（路径和名称）
        :return:
        """
        newexcel.save(address)









if __name__ == '__main__':
    from lib.ExcelGetDatas import ExcelGetDatas as EGD
    egd = EGD(r'C:\Users\Administrator\Desktop\test.xls')
    newdatalist = egd.get_info2('Sheet1')['Sheet1']
    print(newdatalist)

    address = r'C:\Users\Administrator\Desktop\test1.xls'
    aa = ExcelNewDatas()
    newexcel = aa.add_excel()
    newsheet = aa.add_sheet(newexcel,'bb')

    for rownum,rowdatas in enumerate(newdatalist):
        for colnum,coldata in enumerate(rowdatas):
            aa.add_info(newsheet,rownum, colnum, coldata)




    aa.save_excel(address=r'C:\Users\Administrator\Desktop\test.xls')
