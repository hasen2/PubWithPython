import xlwt

class ExcelStyle:
    def __init__(self):
        # 设置excel格式信息
        pass

    def style_new(self):
        style = xlwt.XFStyle() # 初始化样式
        return style

    def style_new_line(self,style,setalignment=0):
        # # 设置单元格自动换行
        style.alignment.wrap = setalignment # =1自动换行  # 仅针对str
        return style

    def style_font(self,style,name='微软雅黑',colour=0,height=10,bold=False,italic=False,underline=False,struck_out=False):
        # 设置字体
        font = xlwt.Font()  # 为样式创建字体
        # 字体类型：比如宋体、仿宋也可以是汉仪瘦金书繁
        font.name = name
        # 设置字体颜色
        font.colour_index = colour # 0黑色，2红色
        # 字体大小
        font.height = height * 20 #字体大小，height为字号，20为衡量单位
        # 是否为粗体
        font.bold = bold
        # 字体是否斜体
        font.italic = italic
        # 字体下划,当值为11时。填充颜色就是蓝色
        font.underline = underline
        # 字体中是否有横线struck_out
        font.struck_out = struck_out
        # 定义格式
        style.font = font
        return style

    def sytle_alignment(self,style,typelevel=0x02,typevertic=0x01):
        # 对齐方式
        # 设置单元格对齐方式
        alignment = xlwt.Alignment()
        # 0x01(左端对齐)、0x02(水平方向上居中对齐)、0x03(右端对齐)
        alignment.horz = typelevel
        # 0x00(上端对齐)、 0x01(垂直方向上居中对齐)、0x02(底端对齐)
        alignment.vert = typevertic


        style.alignment = alignment

        return style

    def style_colour(self,style,num=1):
        # 单元格背景色
        pattern = xlwt.Pattern()  # Create the Pattern
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN  # May be: NO_PATTERN, SOLID_PATTERN, or 0x00 through 0x12
        pattern.pattern_fore_colour = num
                # May be: 8 through 63. 0 = Black, 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow, 6 = Magenta,洋红色,
                # 7 = Cyan,青色, 16 = Maroon,褐红色, 17 = Dark Green,碧绿, 18 = Dark Blue, 19 = Dark Yellow , almost brown), 20 = Dark Magenta,
                # 21 = Teal，蓝绿色, 22 = Light Gray, 23 = Dark Gray, the list goes on...
        style.pattern = pattern # Add Pattern to Style
        return style

    def style_frame(self,style,typenum=1,typecolour=0):
        # 设置单元格边框
        borders = xlwt.Borders()
        # 细实线:1，小粗实线:2，细虚线:3，中细虚线:4，大粗实线:5，双线:6，细点虚线:7
        # 大粗虚线:8，细点划线:9，粗点划线:10，细双点划线:11，粗双点划线:12，斜点划线:13
        borders.left = typenum
        borders.right = typenum
        borders.top = typenum
        borders.bottom = typenum
        borders.left_colour = typecolour
        borders.right_colour = typecolour
        borders.top_colour = typecolour
        borders.bottom_colour = typecolour
        style.borders = borders     # Add Borders to Style





if __name__ == '__main__':
    estyle = ExcelStyle()
    style10 = estyle.style_new()
    estyle.style_new_line(style10,setalignment=1)
    estyle.style_frame(style10)
    estyle.style_colour(style10,5)
    estyle.style_font(style10,bold=True)
    estyle.sytle_alignment(style10)






    from lib.ExcelNewDatas import ExcelNewDatas as ENDate
    endate = ENDate()
    newexcel = endate.add_excel()
    newsheet = endate.add_sheet(newexcel,'name')
    endate.set_col_width(newsheet,3,8)
    endate.set_col_width(newsheet,3,8)
    endate.add_info(newsheet,0,0,'点点滴滴点点滴滴',style10)
    endate.add_info(newsheet,1,1,'点点滴滴点点滴滴')

    style11 = estyle.style_colour(style10,2)
    endate.add_info(newsheet,2,2,'点点滴滴点点滴滴',style10)
    endate.add_info(newsheet,3,3,'点点滴滴点点滴滴')
    endate.set_merge(newsheet,1,1,1,3)
    endate.save_excel(newexcel,'/Users/xxx/desktop/test1.xls')














